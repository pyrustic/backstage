import os
import os.path
import re
import time
import pathlib
from collections import OrderedDict
from backstage import error
from backstage.pattern import Pattern
from backstage import constant
from backstage import util


def run(runner, element, items=None):
    items = items if items else dict()
    handler = HANDLERS.get(element)
    if not handler:
        msg = "Unknown element '{}'.".format(element)
        raise error.Error(msg)
    handler(runner, items)


def append_to_file(runner, items):
    variable = items.get("var")
    filename_var = items.get("filename_var")
    content = runner.get(variable)
    filename = runner.get(filename_var)
    filename = util.normpath(filename)
    if not os.path.isfile(filename):
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(filename, "w") as file:
            pass
    with open(filename, "a") as file:
        file.write(content)


def assertion_handler(runner, items):
    result = util.eval_assertion(runner, items)
    runner.set("R", int(result))
    if not result and runner.config["TestMode"]:
        raise error.FailedAssertion


def branch_subtask(runner, items):
    subtask = items.get("subtask")
    arguments = items.get("arguments")
    util.branch(runner, subtask, arguments, new_thread=False)


def break_handler(runner, items):
    scopes = runner.scopes
    loop_spotted = False
    for scope in reversed(scopes):
        if scope["name"] in (Pattern.WHILE.name, Pattern.FOR.name,
                             Pattern.FROM.name, Pattern.BROWSE.name):
            loop_spotted = True
            scope["active"] = False
            break
    if not loop_spotted:
        msg = "Use 'break' only to stop the execution of loops."
        raise error.Error(msg)


def call_func(runner, items):
    module_name = items.get("module")
    callable_name = items.get("function")
    args = items.get("arguments")
    args = args.split() if args else list()
    module = runner.modules.get(module_name)
    c = util.get_callable(module, callable_name)
    if c is None:
        msg = "The callable '{}' doesn't exist.".format(callable_name)
        raise error.Error(msg)
    arguments = list()
    for arg in args:
        arg = arg.strip(" ,")
        if not arg:
            continue
        arguments.append(runner.get(arg))
    runner.set("ERROR", str())
    runner.set("R", str())
    #try:
    r = c(*arguments)
    #except Exception as e:
    #    runner.set("ERROR", str(e))
    #    return
    r = _update_return_type(r)
    runner.set("R", r)


def change_dir(runner, items):
    new_dir_var = items.get("dirname_var")
    new_dir = runner.get(new_dir_var)
    new_dir = util.normpath(new_dir)
    if not os.path.isdir(new_dir):
        msg = "This path doesn't exist: {}".format(new_dir)
        raise error.Error(msg)
    os.chdir(new_dir)


def check_var(runner, items):
    variable = items.get("var")
    try:
        content = runner.get(variable)
    except error.VariableError as e:
        runner.clear("R")
    else:
        datatype = "str"
        types_map = [(list, "list"), (tuple, "list"), (int, "int"),
                     (float, "float"), (dict, "dict")]
        for x in types_map:
            if isinstance(content, x[0]):
                datatype = x[1]
        runner.set("R", datatype)


def clear_var(runner, items):
    variables = items.get("vars", str()).split()
    if not variables:
        raise error.InterpretationError
    for variable in variables:
        runner.set(variable, str())


def configure(runner, items):
    options = items.get("options").split()
    if not options:
        raise error.InterpretationError
    values = list()
    for option in options:
        cache = option.split("=", maxsplit=1)
        if len(cache) == 2:
            option, value = cache
            try:
                value = bool(int(value))
            except ValueError as e:
                msg = "The configuration option value must be 0 or 1."
                raise error.Error(msg)
        else:
            option, value = cache[0], None
        if option not in constant.CONFIG_OPTIONS:
            msg = "Unknown configuration option '{}'. Valid options: {}"
            msg = msg.format(option, "  ".join(constant.CONFIG_OPTIONS))
            raise error.Error(msg)
        if value is None:
            value = runner.config.get(option)
        else:
            runner.config[option] = value
        values.append(int(value))
    if len(values) == 1:
        runner.set("R", values[0])
    else:
        runner.set("R", values)


def copy_resource(runner, items):
    src_path_var = items.get("src_path_var")
    dest_path_var = items.get("dest_path_var")
    src = runner.get(src_path_var)
    dest = runner.get(dest_path_var)
    src = util.normpath(src)
    dest = util.normpath(dest)
    util.copyto(src, dest)


def count(runner, items):
    element = items.get("element")
    variable = items.get("var")
    tag = items.get("tag")
    content_iterator = util.get_content_iterator(runner, element, variable, tag)
    i = 0
    for _ in content_iterator:
        i += 1
    runner.set("R", i)


def create_resource(runner, items):
    element = items.get("element")
    path_var = items.get("path_var")
    path = runner.get(path_var)
    path = util.normpath(path)
    if element == "dir":
        if os.path.isfile(path):
            msg = "Cannot create this directory since a file with same name exists."
            raise error.Error(msg)
        if os.path.exists(path):
            return
        try:
            os.makedirs(path)
        except Exception:
            pass
    elif element == "file":
        if os.path.isdir(path):
            msg = "Cannot create this file since a directory with same name exists."
            raise error.Error(msg)
        if os.path.exists(path):
            return
        directory = os.path.dirname(path)
        try:
            os.makedirs(directory)
        except Exception:
            pass
        try:
            with open(path, "w") as file:
                pass
        except Exception:
            pass


def default_var(runner, items):
    variables = items.get("vars")
    variables = variables.split() if variables else list()
    if not variables:
        raise error.InterpretationError
    for variable in variables:
        items = {"var": variable, "tag": "str",
                 "raw": "r", "value": str()}
        try:
            runner.get(variable)
        except error.VariableError:
            set_variable(runner, items)


def drop_var(runner, items):
    variables = items.get("vars").split()
    if not variables:
        raise error.InterpretationError
    for var in variables:
        runner.delete(var)


def enter_user_data(runner, items):
    variable = items.get("var")
    if not variable:
        input()
        return
    text = items.get("text", str())
    text = util.strip_delimiters(text)
    text = util.interpolate(runner, text, quote=False)
    value = input(text)
    runner.set(variable, value)


def exit_handler(runner, items):
    raise error.Exit


def expose(runner, items):
    variables = items.get("vars").split()
    if not variables:
        raise error.InterpretationError
    for variable in variables:
        namespace, var = util.split_var(variable)
        if namespace != "L" or not var.isidentifier or var.isupper():
            msg = "Only user-defined local variables can be exposed."
            raise error.Error(msg)
        value = runner.get(variable)
        with runner.lock:
            runner.global_vars[var] = value


def fail(runner, items):
    runner.fail()


def find(runner, items):
    find_all = items.get("all")
    category = items.get("category")
    dirname_var = items.get("dirname_var")
    regex_var = items.get("regex_var")
    field = items.get("field")
    preposition = items.get("preposition")
    timestamp1_var = items.get("timestamp1_var")
    timestamp2_var = items.get("timestamp2_var")
    find_all = bool(find_all)
    directory = runner.get(dirname_var)
    regex = runner.get(regex_var) if regex_var else None
    timestamp1 = runner.get(timestamp1_var) if timestamp1_var else None
    timestamp2 = runner.get(timestamp2_var) if timestamp2_var else None
    directory = util.normpath(directory)
    resources = list()
    runner.clear("R")
    if find_all:
        for root, dirs, files in os.walk(directory):
            if category == "paths":
                cache = dirs + files
            elif category == "dirs":
                cache = dirs
            elif category == "files":
                cache = files
            else:
                msg = "Unknown resource category '{}'".format(category)
                raise error.Error(msg)
            for x in cache:
                path = os.path.join(root, x)
                if util.match_resource(path, regex, field, preposition, timestamp1,
                                       timestamp2):
                    resources.append(path)
    else:
        for x in os.listdir(directory):
            path = os.path.join(directory, x)
            skip = True
            if os.path.isdir(path) and category in ("dirs", "paths"):
                skip = False
            elif os.path.isfile(path) and category in ("files", "paths"):
                skip = False
            if skip:
                continue
            if util.match_resource(path, regex, field, preposition, timestamp1,
                                   timestamp2):
                resources.append(path)
    runner.set("R", resources)


def get_handler(runner, items):
    element = items.get("element")
    index_var = items.get("index_var")
    variable = items.get("var")
    tag = items.get("tag")
    index = runner.get(index_var)
    index = int(index)
    content_iterator = util.get_content_iterator(runner, element, variable, tag)
    if index < 0:
        cache = [val for val in content_iterator]
        try:
            val = cache[index]
        except IndexError:
            raise error.Error("Index error.")
        else:
            runner.set("R", val)
            return
    for i, val in enumerate(content_iterator):
        if i == index:
            runner.set("R", val)
            return
    raise error.Error("Index error.")


def interface_module(runner, items):
    module = items.get("module")
    name = items.get("name")
    m = util.get_module(module)
    if not m:
        msg = "Module '{}' not found.".format(module)
        raise error.Error(msg)
    if name:
        runner.modules[name] = m
        return
    runner.modules[module] = m


def move_resource(runner, items):
    src_path_var = items.get("src_path_var")
    dest_path_var = items.get("dest_path_var")
    src = runner.get(src_path_var)
    dest = runner.get(dest_path_var)
    src = util.normpath(src)
    dest = util.normpath(dest)
    util.moveto(src, dest)


def pass_line(runner, items):
    pass


def poke_resource(runner, items):
    path_var = items.get("path_var")
    path = runner.get(path_var)
    path = util.normpath(path)
    if not os.path.exists(path):
        runner.clear("R")
        return
    is_dir = is_file = 0
    if os.path.isfile(path):
        is_file = 1
    elif os.path.isdir(path):
        is_dir = 1
    stats = os.stat(path)
    attributes = ("st_size", "st_mtime", "st_ctime",
                  "st_atime", "st_nlink", "st_uid",
                  "st_gid", "st_mode", "st_ino", "st_dev")
    data = dict()
    for name in attributes:
        try:
            value = getattr(stats, name)
        except AttributeError as e:
            continue
        name = name.replace("st_", "")
        data[name] = value
    data["is_file"] = is_file
    data["is_dir"] = is_dir
    data["path"] = path
    runner.set("R")


def prepend_file(runner, items):
    variable = items.get("var")
    filename_var = items.get("filename_var")
    content = runner.get(variable)
    filename = runner.get(filename_var)
    filename = util.normpath(filename)
    if not os.path.isfile(filename):
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(filename, "w") as file:
            pass
    with open(filename, "r") as file:
        lines = file.readlines()
        lines.insert(0, content)
    with open(filename, "w") as file:
        file.write("".join(lines))


def print_text(runner, items):
    text = items.get("text", str())
    text = util.strip_delimiters(text)
    text = util.interpolate(runner, text, quote=False)
    end = str()
    auto_line_break = runner.config.get("AutoLineBreak")
    if auto_line_break:
        end = "\n"
    print(text, end=end)


def push(runner, items):
    variables = items.get("vars").split()
    if not vars:
        raise error.InterpretationError
    cache = list()
    for var in variables:
        data = runner.get(var)
        if isinstance(data, (list, tuple)):
            data = "\n".join(data)
        cache.append(data)
    push_cache = "\n".join(cache)
    runner.push_cache = push_cache.encode("utf-8")


def read_file(runner, items):
    index_var = items.get("index_var")
    filename_var = items.get("filename_var")
    filename = runner.get(filename_var)
    filename = util.normpath(filename)
    if not os.path.isfile(filename):
        msg = "File not found: {}".format(filename)
        raise error.Error(msg)
    runner.clear("R")
    if index_var == "*":
        with open(filename, "r") as file:
            data = file.read()
        runner.set("R", data)
        return
    index = runner.get(index_var)
    index = int(index)
    """
    if index < 0:
        with open(filename, "r") as file:
            data = file.read()
            lines = data.splitlines()
            try:
                line = lines[index]
            except IndexError:
                raise error.Error("Index error.")
            else:
                runner.set("R", line)
                return
    """
    iter_content = util.iterate_content(pathlib.Path(filename), "line")
    if index < 0:
        lines = [line for line in iter_content]
        try:
            line = lines[index]
        except IndexError:
            raise error.Error("Index error.")
        else:
            runner.set("R", line)
            return
    for i, line in enumerate(iter_content):
        if i == index:
            runner.set("R", line)
            return
    raise error.Error("Index error.")


def replace_text(runner, items):
    regex_var = items.get("regex_var")
    text_var = items.get("text_var")
    replacement_var = items.get("replacement_var")
    regex = runner.get(regex_var)
    text = runner.get(text_var)
    replacement = runner.get(replacement_var)
    text = re.sub(regex, replacement, text)
    runner.set("R", text)


def return_handler(runner, items):
    variable = items.get("var")
    return_value = None
    if variable:
        return_value = runner.get(variable)
    runner.quit(return_value)


def set_variable(runner, items):
    variable, tag, value = items.get("var"), items.get("tag"), items.get("value")
    if tag and tag not in constant.ASSIGNMENT_TAGS:
        msg1 = "Unknown assignment tag '{}'.".format(tag)
        msg2 = "Valid assignment tags: {}".format("  ".join(constant.ASSIGNMENT_TAGS))
        msg = "{}\n{}".format(msg1, msg2)
        raise error.Error(msg)
    # update tag (default to "str")
    tag = tag if tag else "str"
    # strip out backticks
    value = util.strip_delimiters(value)
    # perform interpolation if literal is not "raw"
    if tag != "raw":
        value = util.interpolate(runner, value, quote=False)
    var_info = util.scan_var(variable)
    # cast !
    if var_info["access"]:
        if tag in ("list", "dict"):
            tag = "str"
    value = util.apply_assignment_tag(value, tag)
    runner.set(var_info, value)


def sleep(runner, items):
    seconds_var = items.get("seconds_var")
    seconds = runner.get(seconds_var)
    s = float(seconds)
    time.sleep(s)


def spawn(runner, items):
    """
    $ command arg1 arg2 ... argx
    """
    mode = items.get("mode")
    captured = True if mode == "($)" else False
    input_data = runner.push_cache
    runner.push_cache = None
    program = items.get("program")
    arguments = items.get("arguments", str())
    command = "{} {}".format(program, arguments.strip())
    command = util.interpolate(runner, command)
    if not command or command.isspace():
        raise error.InterpretationError
    stdout = util.get_stream(runner, "STDOUT")
    stderr = util.get_stream(runner, "STDERR")
    commands = util.check_pipeline(command)
    is_pipeline = True if commands else False
    if is_pipeline:
        info = util.spawn_pipeline(runner, commands, input_data,
                                   stdout, stderr, captured)
    else:
        info = util.spawn(runner, command, input_data, stdout, stderr, captured)
    output_str = info.output.decode("utf-8") if info.output else str()
    error_str = info.error.decode("utf-8") if info.error else str()
    return_code = (info.return_codes
                   if is_pipeline else info.return_code)
    runner.set("R", return_code)
    runner.set("OUTPUT", output_str)
    runner.set("ERROR", error_str)


def split_text(runner, items):
    text_var = items.get("text_var")
    regex_var = items.get("regex_var")
    text = runner.get(text_var)
    regex = runner.get(regex_var)
    result = re.split(regex, text)
    runner.set("R", result)


def spot(runner, items):
    regex_var = items.get("regex_var")
    text_var = items.get("text_var")
    regex = runner.get(regex_var)
    text = runner.get(text_var)
    x = re.findall(regex, text)
    runner.set("R", len(x))


def store(runner, items):
    variables = items.get("vars").split()
    if not variables:
        raise error.InterpretationError
    for variable in variables:
        namespace, var = util.split_var(variable)
        if namespace != "L" or not var.isidentifier or var.isupper():
            msg = "Only user-defined local variables can be stored."
            raise error.Error(msg)
        value = runner.get(variable)
        with runner.lock:
            runner.database_vars[variable] = value


def thread_handler(runner, items):
    subtask = items.get("subtask")
    arguments = items.get("arguments")
    util.branch(runner, subtask, arguments, new_thread=True)


def write_file(runner, items):
    variable = items.get("var")
    filename_var = items.get("filename_var")
    content = runner.get(variable)
    filename = runner.get(filename_var)
    filename = util.normpath(filename)
    if not os.path.isfile(filename):
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(filename, "w") as file:
            pass
    with open(filename, "w") as file:
        file.write(content)


HANDLERS = {Pattern.APPEND.name: append_to_file,
            Pattern.ASSERT.name: assertion_handler,
            Pattern.BRANCH.name: branch_subtask,
            Pattern.BREAK.name: break_handler,
            Pattern.CALL.name: call_func,
            Pattern.CD.name: change_dir,
            Pattern.CHECK.name: check_var,
            Pattern.CLEAR.name: clear_var,
            Pattern.CONFIG.name: configure,
            Pattern.COPY.name: copy_resource,
            Pattern.COUNT.name: count,
            Pattern.CREATE.name: create_resource,
            Pattern.DEFAULT.name: default_var,
            Pattern.DROP.name: drop_var,
            Pattern.ENTER.name: enter_user_data,
            Pattern.EXIT.name: exit_handler,
            Pattern.EXPOSE.name: expose,
            Pattern.FAIL.name: fail,
            Pattern.FIND.name: find,
            Pattern.GET.name: get_handler,
            Pattern.INTERFACE.name: interface_module,
            Pattern.MOVE.name: move_resource,
            Pattern.PASS.name: pass_line,
            Pattern.POKE.name: poke_resource,
            Pattern.PREPEND.name: prepend_file,
            Pattern.PRINT.name: print_text,
            Pattern.PUSH.name: push,
            Pattern.READ.name: read_file,
            Pattern.REPLACE.name: replace_text,
            Pattern.RETURN.name: return_handler,
            Pattern.SET.name: set_variable,
            Pattern.SLEEP.name: sleep,
            Pattern.SPAWN.name: spawn,
            Pattern.SPLIT.name: split_text,
            Pattern.SPOT.name: spot,
            Pattern.STORE.name: store,
            Pattern.THREAD.name: thread_handler,
            Pattern.WRITE.name: write_file}


def _update_return_type(r):
    if r is None:
        return r
    if r is True:
        return 1
    if r is False:
        return 0
    if isinstance(r, str):
        return r
    if isinstance(r, list):
        return r
    if isinstance(r, dict):
        return OrderedDict(r)
    if isinstance(r, tuple):
        return list(r)
    if isinstance(r, int):
        return r
    if isinstance(r, float):
        return r
    msg1 = "Python functions should return one of these types: "
    msg2 = "str, int, float, list, dict, tuple, True, False, None"
    raise error.Error("".join([msg1, msg2]))
