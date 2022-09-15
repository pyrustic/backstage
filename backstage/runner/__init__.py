"""Project Backstage API"""
import os
import os.path
import sys
import time
import textwrap
import subprocess
import traceback
import random
import shlex
import subrun
import oscan
from threading import Thread
from tempfile import TemporaryDirectory
from subrun import pipeline
from backstage import error, util
from backstage import core
from backstage import constant
from backstage.pattern import Pattern
from backstage.usage import Usage


class Runner:
    def __init__(self, backstage, task, rid, arguments=None, config=None):
        self._backstage = backstage
        self._task = task
        self._rid = rid
        if isinstance(arguments, str):
            arguments = shlex.split(arguments, posix=True)
        self._arguments = list(arguments) if arguments else list()
        new_config = config if config else dict()
        self._config = {"FailFast": False, "ReportException": False,
                        "ShowTraceback": False, "TestMode": False,
                        "AutoLineBreak": True}
        self._config.update(new_config)
        self._task_body = None
        self._tempdir = TemporaryDirectory()
        self._local_vars = util.create_env_vars(self._arguments, self._tempdir)
        self._global_vars = backstage.global_vars
        self._database_vars = backstage.database_vars
        self._lock = backstage.lock
        self._threads = list()
        self._threads_timeouts = list()
        self._index = 0
        self._active = False
        self._expired = False
        self._is_success = False
        self._expected_indent = None  # (int_n_indents, bool_strict)
        default_scope = {"name": "MAIN", "index": 0, "active": True,
                         "indents": 0, "data": None}
        self._scopes = list()
        self._scopes.append(default_scope)
        self._push_cache = None
        self._modules = dict()
        self._return_value = str()
        self._indents = 0
        self._cached_indents = 0
        self._indent_shift = 0
        self._setup()

    @property
    def backstage(self):
        return self._backstage

    @property
    def task(self):
        return self._task

    @property
    def rid(self):
        return self._rid

    @property
    def task_body(self):
        return self._task_body

    @property
    def arguments(self):
        return self._arguments

    @property
    def local_vars(self):
        return self._local_vars

    @property
    def global_vars(self):
        return self._global_vars

    @property
    def database_vars(self):
        return self._database_vars

    @property
    def active(self):
        return self._active

    @property
    def expired(self):
        return self._expired

    @property
    def lock(self):
        return self._lock

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val

    @property
    def expected_indent(self):
        return self._expected_indent

    @expected_indent.setter
    def expected_indent(self, val):
        self._expected_indent = val

    @property
    def scope(self):
        return self._scopes[-1]

    @property
    def scopes(self):
        return self._scopes

    @property
    def push_cache(self):
        return self._push_cache

    @push_cache.setter
    def push_cache(self, val):
        self._push_cache = val

    @property
    def modules(self):
        return self._modules

    @property
    def config(self):
        return self._config

    @property
    def is_success(self):
        return self._is_success

    @property
    def return_value(self):
        return self._return_value

    def start(self):
        """
        task is a string
        """
        if self._active or self._expired:
            return False
        self._active = True
        with self._lock:
            self._backstage.runners.append(self)
            if self._task != "":
                cache = (self._rid, int(time.time()), None)
                self._backstage.execution_log.append(cache)
        cached_exception = None
        try:
            self._run()
        except Exception as e:
            cached_exception = e
        # join threads
        for i, thread in enumerate(self._threads):
            try:
                thread.join(self._threads_timeouts[i])
            except KeyboardInterrupt as e:
                print()
        with self._lock:
            if self._task != "":
                cache = (self._rid, int(time.time()), self._is_success)
                self._backstage.execution_log.append(cache)
        # cleanup
        self._tempdir.cleanup()
        self._expired = True
        if cached_exception:
            raise cached_exception
        return True

    def branch(self, subtask, arguments=None, new_thread=False):
        if self._expired:
            return False
        new_rid = self._backstage.gen_rid()
        inherited_config = self._config.copy()
        new_runner = Runner(self._backstage, subtask, new_rid, arguments, inherited_config)
        del inherited_config["AutoLineBreak"]
        if new_thread:
            thread = Thread(target=new_runner.start)
            self._threads.append(thread)
            timeout = self._local_vars["TIMEOUT"]
            self._threads_timeouts.append(timeout)
            thread.start()
        else:
            new_runner.start()
            self.set("R", new_runner.return_value)
        return True

    def get(self, variable):
        number = util.str_to_number(variable)
        if number is not None:
            return number
        if isinstance(variable, str):
            var_info = util.scan_var(variable)
        else:
            var_info = variable
        namespace = var_info["namespace"]
        var = var_info["var"]
        access = var_info["access"]
        access_spec = var_info["access_spec"]
        # update some env vars
        self.set("CWD", os.getcwd())
        self.set("DATE", util.get_date())
        self.set("NOW", int(time.time()))
        self.set("RANDOM", random.randint(0, 255))
        self.set("TIME", util.get_time())
        #
        vars_dict = dict()
        # global
        if namespace == "G":
            vars_dict = self._global_vars
        # database
        elif namespace == "D":
            vars_dict = self._database_vars
        # local
        elif namespace == "L":
            vars_dict = self._local_vars
        #
        try:
            val = vars_dict[var]
        except KeyError:
            raise error.VariableError(var)
        if access:
            return val[access_spec]
        return val

    def set(self, variable, value):
        if isinstance(variable, str):
            var_info = util.scan_var(variable)
        else:
            var_info = variable
        namespace = var_info["namespace"]
        var = var_info["var"]
        access = var_info["access"]
        access_spec = var_info["access_spec"]
        #if access:
        #    data = self.get(var_info)
        #    data[access_spec] = value
        #    return
        if namespace == "G":
            with self._lock:
                self._global_vars[var] = value
        elif namespace == "D":
            with self._lock:
                self._database_vars[var] = value
        elif namespace == "L":
            if var.isupper() and (var not in constant.ENVIRONMENT_VARS):
                msg = "New environment variables can't be created by the user."
                raise error.Error(msg)
            if access:
                self._local_vars[var][access_spec] = value
            else:
                self._local_vars[var] = value

    def clear(self, variable):
        self.set(variable, None)

    def delete(self, variable):
        if isinstance(variable, str):
            var_info = util.scan_var(variable)
        else:
            var_info = variable
        namespace = var_info["namespace"]
        var = var_info["var"]
        try:
            if namespace == "G":
                with self._lock:
                    del self._global_vars[var]
            elif namespace == "D":
                with self._lock:
                    del self._database_vars[var]
            elif namespace == "L":
                del self._local_vars[var]
        except KeyError:
            pass

    def fail(self):
        raise error.Fail("Deliberate failure")

    def quit(self, return_value):
        self._return_value = return_value
        raise error.Return

    def _setup(self):
        #if not isinstance(self._arguments, str):
        #    self._arguments = shlex.join(self._arguments)
        self._task_body = self._get_task_body()
        # add an empty comment at the end
        self._task_body.append("return")

    def _get_task_body(self):
        task_body = self._backstage.tasks.get(self._task)
        if task_body is None:
            msg = "There is no such task named '{}' !".format(self._task)
            print(msg)
            task_body = list()
        return task_body

    def _run(self):
        while True:
            try:
                line = self._task_body[self._index]
            except IndexError:
                return
            # update environment vars TASK and LINE
            self.set("TASK", self._task)
            self.set("LINE", self._index + 1)
            try:
                self._interpret(line)
            except error.Exit as e:
                raise e
            except error.FailedAssertion:
                line = self.get("LINE")
                task = self.get("TASK")
                msg = "FAILED ASSERTION at line {} of [{}]"
                print(msg.format(line, task))
                return
            except error.Return as e:
                self._is_success = True
                return
            except error.Continue as e:
                continue
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                error_name = e.__class__.__name__
                self.set("EXCEPTION", error_name)
                self.set("TRACEBACK", traceback.format_exc())
                msg = "{} at line {} of [{}] !"
                line_number = self._index + 1
                msg = msg.format(error_name, line_number, self._task)
                #
                if isinstance(e, error.InterpretationError):
                    self._config["FailFast"] = True
                    self._config["ReportException"] = True
                #
                if self._config["ReportException"]:
                    print(msg)
                    self._process_exception(e, line)
                if self._config["ShowTraceback"]:
                    traceback.print_exc()
                if self._config["FailFast"] or isinstance(e, error.Fail):
                    raise error.Exit
                #return
            else:
                if line and not line.isspace():
                    self.clear("EXCEPTION")
                    self.clear("TRACEBACK")
            self._index += 1

    def _interpret(self, line):
        if not line or line.isspace():
            return
        info = oscan.match(line, Pattern)
        if not info:
            raise error.InterpretationError
        element, items = info.name, info.groups_dict
        if element in (Pattern.COMMENT.name, Pattern.LINE.name):
            return
        self._indents = self._check_indent(items.get("indent"))
        if element in (Pattern.IF.name, Pattern.ELIF.name, Pattern.ELSE.name,
                       Pattern.WHILE.name, Pattern.FOR.name, Pattern.BROWSE.name,
                       Pattern.FROM.name):
            self._add_scope(element, items)
            return
        self._indent_shift = self._check_indent_shift()
        self._cleanup_scope()
        self._update_expected_indent()
        if not self.scope["active"]:
            return
        core.run(self, element, items)

    def _check_indent(self, spaces):
        indents = self._count_indents(spaces)
        if not self._expected_indent:
            return indents
        expected_indents, strict = self._expected_indent
        if strict and expected_indents != indents:
            plural = "s" if expected_indents > 1 else ""
            msg = "Expected {} indent{}."
            msg = msg.format(expected_indents, plural)
            raise error.IndentError(msg)
        if indents > expected_indents:
            msg = "Over-indented."
            raise error.IndentError(msg)
        return indents

    def _check_indent_shift(self):
        result = self._indents - self._cached_indents
        self._cached_indents = self._indents
        return result

    def _count_indents(self, spaces):
        spaces = len(spaces)
        if (spaces % constant.INDENT) != 0:
            raise error.IndentError
        return spaces // constant.INDENT

    def _add_scope(self, name, data):
        #active = False
        #if not self._scopes or (self._scopes and self._scopes[-1]["active"]):
        #    data = self._compute_scope(name, data)
        #    active = True if data else False
        exception = None
        try:
            data = self._compute_scope(name, data)
        except Exception as e:
            exception = e
            data = None
        active = True if data else False
        scope = {"name": name, "index": self._index,
                 "indents": self._indents, "data": data,
                 "active": active}
        self._scopes.append(scope)
        self._expected_indent = (self._indents + 1, True)
        if exception:
            raise exception

    def _update_expected_indent(self):
        if len(self._scopes) == 1:
            self._expected_indent = None
        else:
            self._expected_indent = self.scope["indents"] + 1, False

    def _cleanup_scope(self):
        if self._indent_shift >= 0:
            return
        for scope in reversed(self._scopes):
            scope_name = scope["name"]
            if scope_name == "MAIN":
                break
            if scope["indents"] < self._indents:
                continue
            if scope_name in (Pattern.WHILE.name, Pattern.FOR.name,
                              Pattern.FROM.name, Pattern.BROWSE.name):
                self._update_loop(scope_name)
            self._scopes.pop()

    def _compute_scope(self, name, data):
        funcs = {Pattern.IF.name: self._compute_if_scope,
                 Pattern.ELIF.name: self._compute_elif_scope,
                 Pattern.ELSE.name: self._compute_else_scope,
                 Pattern.WHILE.name: self._compute_while_scope,
                 Pattern.FOR.name: self._compute_for_scope,
                 Pattern.FROM.name: self._compute_from_scope,
                 Pattern.BROWSE.name: self._compute_browse_scope}
        func = funcs[name]
        return func(data)

    def _compute_if_scope(self, data):
        result = util.eval_assertion(self, data)
        data = data if result else None
        return data

    def _compute_elif_scope(self, data):
        track = self._build_conditionals_track(Pattern.ELIF.name)
        if not self._is_conditionals_track_open(track):
            return None
        result = util.eval_assertion(self, data)
        data = data if result else None
        return data

    def _compute_else_scope(self, data):
        track = self._build_conditionals_track(Pattern.ELIF.name)
        if not self._is_conditionals_track_open(track):
            return None
        return data

    def _compute_while_scope(self, data):
        # update N
        n = data.get("N", -1) + 1
        data["N"] = n
        self.set("N", n)
        #
        result = util.eval_assertion(self, data)
        data = data if result else None
        return data

    def _compute_for_scope(self, data):
        # update N
        n = data.get("N", -1) + 1
        data["N"] = n
        self.set("N", n)
        #
        content_iterator = data.get("iterator")
        element = data.get("element")
        if not content_iterator:
            tag = data.get("tag")
            content_iterator = util.get_content_iterator(self, element,
                                                         data["var"], tag)
        try:
            cache = next(content_iterator)
        except StopIteration as e:
            return None
        else:
            self.set(element, cache)
        data["iterator"] = content_iterator
        return data

    def _compute_from_scope(self, data):
        # update N
        n = data.get("N", -1) + 1
        data["N"] = n
        self.set("N", n)
        #
        start, end = data["start_var"], data["end_var"]
        if isinstance(start, str):
            start, end = int(self.get(start)), int(self.get(end))
        order = data.get("order")
        if not order:
            order = "asc" if start <= end else "desc"
        self.set("R", start)
        if order == "asc":
            if start > end:
                return None
            start += 1
        elif order == "desc":
            if start < end:
                return None
            start -= 1
        data["start_var"], data["end_var"] = start, end
        data["order"] = order
        return data

    def _compute_browse_scope(self, data):
        # update N
        n = data.get("N", -1) + 1
        data["N"] = n
        self.set("N", n)
        #
        files_tag = data.get("files")
        dirs_tag = data.get("dirs")
        if not files_tag and not dirs_tag:
            msg = "Resource to browse should be 'files' and or 'dirs'."
            raise error.Error(msg)
        dirname_var = data.get("dirname_var")
        dirname = util.normpath(self.get(dirname_var))
        content_iterator = data.get("iterator")
        if not content_iterator:
            content_iterator = os.walk(dirname)
        try:
            cache = next(content_iterator)
        except StopIteration as e:
            return None
        else:
            root_dir, directories, filenames = cache
            self.set("R", root_dir)
            if files_tag:
                self.set("files", filenames)
            if dirs_tag:
                self.set("dirs", directories)
        data["iterator"] = content_iterator
        return data

    def _update_loop(self, name):
        scope = self.scope
        if not scope["active"]:
            return
        cache = self._compute_scope(name, scope["data"])
        if cache is None:
            return
        scope["data"] = cache
        self._index = scope["index"] + 1
        self._expected_indent = scope["indents"] + 1, False
        raise error.Continue

    def _build_conditionals_track(self, candidate):
        cache = list()
        for scope in self._scopes:
            if scope["indents"] == self._indents:
                if scope["name"] in (Pattern.IF.name, Pattern.ELIF.name,
                                     Pattern.ELSE.name):
                    cache.append(scope)
                else:
                    cache = list()
        error_msg = "Conditionals should be ordered as: if... elif... else"
        if not cache and candidate in (Pattern.ELIF.name, Pattern.ELSE.name):
            raise error.InterpretationError(error_msg)
        if candidate in (Pattern.ELIF.name, Pattern.ELSE.name):
            if cache:
                for item in cache:
                    if item["name"] == Pattern.ELSE.name:
                        raise error.InterpretationError(error_msg)
            else:
                raise error.InterpretationError(error_msg)
        return cache

    def _is_conditionals_track_open(self, track):
        for scope in track:
            if scope["active"]:
                return False
        return True

    def _process_exception(self, e, line):
        if isinstance(e, error.InterpretationError):
            if e.args:
                msg = " ".join(e.args)
            else:
                msg = self._get_usage(line)
            if msg:
                print(msg)
        elif isinstance(e, error.IndentError):
            if e.args:
                msg = " ".join(e.args)
            else:
                msg = "Indents should be made of {} spaces."
                msg = msg.format(constant.INDENT)
            print(msg)
        elif isinstance(e, error.VariableError):
            if not e.args:
                return
            varname = e.args[0]
            msg = "Undefined variable: '{}'.".format(varname)
            print(msg)
        elif isinstance(e, error.SubprocessError):
            if e.args:
                msg = " ".join(e.args)
            else:
                msg = "Failed to run the subprocess command."
            print(msg)
        elif isinstance(e, error.Error):
            if not e.args:
                return
            print(" ".join(e.args))
        else:
            if not e.args:
                return
            print(e.args[-1])

    def _get_usage(self, line):
        try:
            cache = line.split()
            element = constant.ELEMENTS[cache[0]]
        except (IndexError, KeyError):
            elements = "  ".join(constant.ELEMENTS.keys())
            usage = "Valid instructions: {}".format(elements)
            usage = "\n".join(textwrap.wrap(usage))
            return usage
        usage = None
        for item in Usage:
            if item.name == element:
                usage = item.value
                break
        if not usage:
            return
        usage = "\n".join(usage) if isinstance(usage, (tuple, list)) else usage
        return "Usage: {}".format(usage)
