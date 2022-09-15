import os
import os.path
import sys
import re
import time
import shlex
import string
import importlib
import random
import subprocess
import pathlib
import shutil
import shared
import oscan
import subrun
from datetime import datetime
from collections import OrderedDict
from string import Formatter
from subrun import pipeline as subrun_pipeline
from backstage.pattern import Pattern, VARIABLE_PATTERN
from backstage import constant, error


__all__ = []


SAFE_CHARS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "+", "-", "*", "/", "%", "(", ")", " ")


def scan(line):
    tokens = list()
    for info in oscan.scan(line, Pattern):
        element = info.name
        items = info.groups_dict
        tokens.append((element, items))
    return tokens


def get_tasks(directory):
    return shared.jesth_readonly(constant.BASENAME, default=None,
                                 directory=directory)


def create_env_vars(arguments, tempdir):
    env_vars = dict()
    env_vars["ARGS"] = arguments
    env_vars["CWD"] = os.getcwd()
    env_vars["DATE"] = get_date()
    env_vars["EMPTY"] = str()
    env_vars["ERROR"] = str()
    env_vars["EXCEPTION"] = str()
    env_vars["FALSE"] = int(0)
    env_vars["HOME"] = os.path.expanduser("~")
    env_vars["LINE"] = int(0)
    env_vars["N"] = int(0)
    env_vars["NOW"] = int(time.time())
    env_vars["ONE"] = int(1)
    env_vars["OS"] = str(sys.platform)
    env_vars["OUTPUT"] = str()
    env_vars["R"] = str()
    env_vars["RANDOM"] = random.randint(0, 255)   # Return Code
    env_vars["SPACE"] = str(" ")
    env_vars["STDERR"] = str()
    env_vars["STDIN"] = str()
    env_vars["STDOUT"] = str()
    env_vars["TASK"] = str()
    env_vars["TIME"] = str(get_time())
    env_vars["TIMEOUT"] = int(30)
    env_vars["TMP"] = str(tempdir.name)
    env_vars["TRACEBACK"] = str()
    env_vars["TRASH"] = str(constant.TRASH_DIR)
    env_vars["TRUE"] = int(1)
    env_vars["ZERO"] = int(0)
    # convenience args
    for i, arg in enumerate(arguments):
        name = "ARG{}".format(i)
        env_vars[name] = str(arg)
    return env_vars


def normpath(path, expand=True):
    path = path.replace("\n", "\\n").replace("\t", "\\t")
    path = path.replace("\\", "/") if os.sep == "/" else path.replace("/", "\\")
    path = os.path.abspath(path) if expand else path
    return path


def calc(expression):
    for quote in ("'", "\""):
        expression = expression.replace(quote, "")
    if not is_safe(expression):
        return str()
    return eval(expression)


def is_safe(expression):
    for char in expression:
        if char not in SAFE_CHARS:
            return False
    return True


def unescape(text):
    return text.encode("latin-1", "backslashreplace").decode("unicode-escape")


def str_to_dict(text):
    data = OrderedDict()
    cache = shlex.split(text, posix=True)
    for item in cache:
        keyval = item.split("=", maxsplit=1)
        if len(keyval) != 2:
            msg = "This str can't be converted to a dict."
            raise error.Error(msg)
        key, val = keyval
        data[key] = val
    return data


def dict_to_str(data):
    cache = list()
    for key, val in data.items():
        key = str() if key is None else key
        val = str() if val is None else val
        key, val = shlex.quote(str(key)), shlex.quote(str(val))
        keyval = "{}={}".format(key, val)
        cache.append(keyval)
    return " ".join(cache)


def str_to_number(text):
    if not isinstance(text, str):
        return None
    cache = text.split(".")
    for x in cache:
        if not x:
            continue
        try:
            int(x)
        except ValueError as e:
            return None
    if "." in text:
        try:
            return float(text)
        except ValueError as e:
            return None
    return int(text)


def interpolate(runner, text, quote=True, heredoc=True):
    """perform string interpolation"""
    runner.set("CWD", os.getcwd())
    runner.set("DATE", get_date())
    runner.set("NOW", time.time())
    runner.set("RANDOM", random.randint(0, 255))
    runner.set("TIME", get_time())
    if heredoc:
        text = unescape(text)
    formatter = Formatter()
    cache = list()
    for x in formatter.parse(text):
        cache.append(x[0])
        field = x[1]
        if x[2]:
            field = x[1] + ":" + x[2]
        if field is None:
            continue
        if field == "":
            msg = "Empty fields aren't allowed. String interpolation cancelled."
            raise error.Error(msg)
        cache.append(_expand_interpolation_field(runner, field, quote))
    return "".join(cache)


def _expand_interpolation_field(runner, field, quote):
    val = runner.get(field)
    return stringify(val, quote)


def stringify(val, quote):
    if val is None:
        return str()
    if isinstance(val, str):
        if quote:
            return shlex.quote(val)
        return val
    if isinstance(val, (list, tuple)):
        updated_val = list()
        for item in val:
            if item is None:
                updated_val.append(str())
                continue
            updated_val.append(str(item))
        return shlex.join(updated_val)
    if isinstance(val, dict):
        return dict_to_str(val)
    if isinstance(val, (int, float)):
        return str(val)


def scan_var(variable):
    token = oscan.match(variable, pattern=VARIABLE_PATTERN)
    if not token:
        msg = "Failed to scan variable '{}'"
        raise error.Error(msg.format(variable))
    namespace = token.groups_dict.get("namespace")
    base = token.groups_dict.get("base")
    index = token.groups_dict.get("index")
    key = token.groups_dict.get("key")
    # check if base is valid Python identifier
    if not base.isidentifier():
        msg = "Invalid identifier '{}'.".format(base)
        raise error.Error(msg)
    if not namespace:
        namespace = "L"
    access = access_spec = None
    for item, name in ((key, "key"), (index, "index")):
        if item is not None:
            if name == "index":
                item = int(item)
            access = name
            access_spec = item
    info = {"namespace": namespace, "var": base,
            "access": access, "access_spec": access_spec}
    return info


def match_resource(path, regex=None, field=None, preposition=None,
                   timestamp1=None, timestamp2=None):
    false_results = 0
    if regex:
        p = path.replace("\\", "/")
        if not oscan.match(p, regex):
            false_results += 1
    if field:
        if field == "created":
            tstamp_src = os.stat(path).st_ctime
        elif field == "modified":
            tstamp_src = os.stat(path).st_mtime
        elif field == "accessed":
            tstamp_src = os.stat(path).st_atime
        else:
            msg = "Unknown time field '{}'".format(field)
            raise error.Error(msg)
        tstamp_src = int(tstamp_src)
        timestamp1 = None if timestamp1 is None else int(timestamp1)
        timestamp2 = None if timestamp2 is None else int(timestamp2)
        if preposition == "at":
            if tstamp_src != timestamp1:
                false_results += 1
        elif preposition == "before":
            if tstamp_src > timestamp1:
                false_results += 1
        elif preposition == "after":
            if tstamp_src < timestamp1:
                false_results += 1
        elif preposition == "between":
            if timestamp2 is None:
                raise error.Error("Missing second timestamp.")
            if tstamp_src < timestamp1 or tstamp_src > timestamp2:
                false_results += 1
    return not bool(false_results)


def save_execution_log(backstage, data):
    cache_dir = os.path.join(backstage.directory, ".backstage")
    filename = os.path.join(cache_dir, "execution.log")
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    if not os.path.isfile(filename):
        with open(filename, "w") as file:
            pass
    cache = list()
    for rid, timestamp, is_success in data:
        for runner in backstage.runners:
            if runner.rid == rid:
                task = runner.task
                x = "startup"
                if is_success is True:
                    x = "success"
                elif is_success is False:
                    x = "failure"
                line = "{} ({}) {}\n".format(timestamp_to_datetime(timestamp),
                                             x, task)
                cache.append(line)
                break
    reversed_cache = list()
    for x in reversed(cache):
        reversed_cache.append(x)
    with open(filename, "r") as file:
        lines = file.readlines()
    reversed_cache.extend(lines)
    log = "".join(reversed_cache[0:1000])
    with open(filename, "w") as file:
        file.write(log)


def backticked(text):
    cache = text.strip()
    if cache.startswith(constant.BACKTICK) and cache.endswith(constant.BACKTICK):
        return True
    return False


def strip_delimiters(text, delimiter=constant.BACKTICK):
    cache = text.strip()
    if cache.startswith(delimiter) and cache.endswith(delimiter):
        text = cache.strip(delimiter)
    return text


def get_module(canonical_name):
    try:
        module = importlib.import_module(canonical_name)
    except ModuleNotFoundError as e:
        return None
    return module


def get_callable(module, callable_name):
    try:
        callable_object = getattr(module, callable_name)
    except AttributeError as e:
        return None
    return callable_object


def eval_assertion(runner, data):
    var1 = data.get("var1")
    var2 = data.get("var2")
    var3 = data.get("var3")
    var4 = data.get("var4")
    comparison1 = data.get("comparison1")
    comparison2 = data.get("comparison2")
    logic = data.get("logic")
    result = eval_condition(runner, comparison1, var1, var2)
    if var3 is None:
        return result
    result1 = result
    result2 = eval_condition(runner, comparison2, var3, var4)
    if logic == "and":
        result = result1 and result2
    elif logic == "or":
        result = result1 or result2
    else:
        raise error.Error("Unknown logical operator '{}'".format(logic))
    return result


def eval_condition(runner, operation, left_var, right_var):
    left = runner.get(left_var)
    right = runner.get(right_var)
    #
    if operation in ("<=", ">=", "<", ">"):
        left, right = float(left), float(right)
    else:
        quote_left = quote_right = True
        if isinstance(left, str):
            quote_left = False
        if isinstance(right, str):
            quote_right = False
        left = stringify(left, quote_left)
        right = stringify(right, quote_right)
    #
    if operation == "==":
        if left == right:
            return True
    elif operation == "!=":
        if left != right:
            return True
    elif operation == "<=":
        if left <= right:
            return True
    elif operation == ">=":
        if left >= right:
            return True
    elif operation == "<":
        if left < right:
            return True
    elif operation == ">":
        if left > right:
            return True
    elif operation == "in":
        if left in right:
            return True
    elif operation == "!in":
        if left not in right:
            return True
    elif operation == "rin":
        regex, text = left, right
        if re.search(regex, text):
            return True
    elif operation == "!rin":
        regex, text = left, right
        if not re.search(regex, text):
            return True
    elif operation == "matches":
        regex, text = left, right
        if oscan.match(text, regex):
            return True
    elif operation == "!matches":
        regex, text = left, right
        if not oscan.match(text, regex):
            return True
    return False


def apply_assignment_tag(value, tag):
    if tag == "str":
        pass
    elif tag in ("int", "float"):
        value = value.strip()
        if not is_safe(value):
            raise error.Error("Unsafe expression !")
        try:
            value = calc(value)
        except Exception as e:
            raise error.Error("Unable to perform calculation !")
        if tag == "int":
            value = int(value)
        elif tag == "float":
            value = float(value)
    elif tag == "list":
        value = shlex.split(value, posix=True)
    elif tag == "dict":
        value = str_to_dict(value)
    elif tag in ("tstamp", "date", "time", "dtime"):
        if "-" in value and ":" in value:
            source = "dtime"
        elif "-" in value:
            source = "date"
        elif ":" in value:
            source = "time"
        else:
            source = "tstamp"
        try:
            value = cast_datetime(value, source, tag)
        except Exception:
            raise error.Error("Failed to convert datetime")
    return value


def cast_datetime(value, src, dest):
    if src == "tstamp":
        value = int(float(value))
        if dest == "tstamp":
            cache = timestamp_to_datetime(value)
            return datetime_to_timestamp(cache)
        if dest == "date":
            return timestamp_to_date(value)
        if dest == "time":
            return timestamp_to_time(value)
        if dest == "dtime":
            return timestamp_to_datetime(value)
    if src == "date":
        if dest == "tstamp":
            return date_to_timestamp(value)
        if dest == "date":
            cache = date_to_timestamp(value)
            return timestamp_to_date(cache)
        if dest == "time":
            cache = date_to_timestamp(value)
            return timestamp_to_time(cache)
        if dest == "dtime":
            cache = date_to_timestamp(value)
            return timestamp_to_datetime(cache)
    if src == "dtime":
        if dest == "tstamp":
            return datetime_to_timestamp(value)
        if dest == "date":
            cache = datetime_to_timestamp(value)
            return timestamp_to_date(cache)
        if dest == "time":
            cache = datetime_to_timestamp(value)
            return timestamp_to_time(cache)
        if dest == "dtime":
            cache = datetime_to_timestamp(value)
            return timestamp_to_datetime(cache)
    if src == "time":
        if dest == "tstamp":
            return time_to_timestamp(value)
        if dest == "date":
            cache = time_to_timestamp(value)
            return timestamp_to_date(cache)
        if dest == "time":
            cache = time_to_timestamp(value)
            return timestamp_to_time(cache)
        if dest == "dtime":
            cache = time_to_timestamp(value)
            return timestamp_to_datetime(cache)


def spawn(runner, command, input_data, stdout, stderr, captured=False):
    timeout = runner.local_vars["TIMEOUT"]
    timeout = timeout if timeout else None
    try:
        if captured:
            info = subrun.capture(command, input=input_data, timeout=timeout)
        else:
            info = subrun.run(command, input=input_data, stdout=stdout,
                              stderr=stderr, timeout=timeout, cwd=os.getcwd())
    except Exception as e:
        raise error.SubprocessError
    return info


def spawn_pipeline(runner, commands, input_data, stdout, stderr, captured=False):
    timeout = runner.local_vars["TIMEOUT"]
    timeout = timeout if timeout else None
    try:
        if captured:
            info = subrun_pipeline.capture(*commands, input=input_data, cwd=os.getcwd(),
                                           timeout=timeout)
        else:
            info = subrun_pipeline.run(*commands, input=input_data, stdout=stdout,
                                       stderr=stderr, cwd=os.getcwd(), timeout=timeout)
    except Exception as e:
        raise error.SubprocessError
    return info


def branch(runner, subtask, arguments, new_thread=False):
    arguments = arguments if arguments else str()
    command = "{} {}".format(subtask, arguments.strip())
    command = interpolate(runner, command)
    if not command or command.isspace():
        raise error.InterpretationError
    cache = command.split(maxsplit=1)
    subtask = cache[0]
    try:
        arguments = cache[1]
    except IndexError:
        arguments = None
    runner.branch(subtask, arguments, new_thread)


def get_stream_value(runner, stream):
    value = runner.local_vars[stream]
    value = value if value else None
    if value is None:
        return None
    if value == "/dev/null":
        return subprocess.DEVNULL
    return normpath(value)


def get_content_iterator(runner, element, variable, tag):
    content = runner.get(variable)
    if tag == "file":
        path = normpath(content)
        if not os.path.isfile(path):
            msg = "This file doesn't exist: {}".format(path)
            raise error.Error(msg)
        content = pathlib.Path(path)
    spec = element.rstrip("s")
    return iterate_content(content, spec)


def iterate_content(content, spec):
    if isinstance(content, pathlib.Path):
        filename = content.resolve()
        for x in _iterate_file(filename, spec):
            yield x
    elif spec == "char":
        if isinstance(content, dict):
            content = dict_to_str(content)
        elif isinstance(content, (list, tuple)):
            content = shlex.join(content)
        else:
            content = str(content)
        for char in content:
            yield char
    elif spec == "item":
        if isinstance(content, dict):
            cache = list()
            for key, val in content.items():
                cache.append([key, val])
            content = cache
        elif isinstance(content, (list, tuple)):
            pass
        else:
            content = shlex.split(str(content), posix=True)
        for item in content:
            yield item
    elif spec == "line":
        if isinstance(content, dict):
            content = dict_to_str(content)
        elif isinstance(content, (list, tuple)):
            content = shlex.join(content)
        else:
            content = str(content)
        for line in content.split("\n"):
            yield line


def _iterate_file(filename, spec):
    with open(filename, "r") as file:
        if spec == "item":
            data = file.read()
            for item in shlex.split(data, posix=True):
                yield item
            return
        while True:
            line = file.readline()
            if line == "":
                break
            if spec == "line":
                yield line.rstrip("\n")
            elif spec == "char":
                for char in line:
                    yield char


def copyto(src, dest):
    src = normpath(src)
    dest = normpath(dest)
    if not os.path.exists(src):
        msg = "The source resource doesn't exist: {}".format(src)
        raise error.Error(msg)
    if os.path.isfile(src):
        if not os.path.isdir(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        shutil.copy2(src, dest)
    elif os.path.isdir(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)


def moveto(src, dest):
    """
    WARNING: this function uses shutil.rmtree to remove the src directory
    """
    src = normpath(src)
    dest = normpath(dest)
    if not os.path.exists(src):
        msg = "The source resource doesn't exist: {}".format(src)
        raise error.Error(msg)
    if os.path.isfile(src):
        if not os.path.isdir(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        shutil.move(src, dest)
    elif os.path.isdir(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)
        shutil.rmtree(src, ignore_errors=True)


def check_pipeline(command):
    if "|" not in command:
        return None
    commands = list()
    cache = list()
    quote = None
    for char in command:
        if char in ("'", "\""):
            if char == quote:
                if cache and cache[-1] != "\\":
                    quote = None
            else:
                quote = char
        elif char == "|":
            if not quote:
                commands.append("".join(cache))
                cache = list()
                continue
        cache.append(char)
    if cache:
        commands.append("".join(cache))
    if len(commands) >= 2:
        return commands
    return None


def get_date():
    return timestamp_to_date()


def get_time():
    return timestamp_to_time()


def timestamp_to_date(val=time.time()):
    return datetime.fromtimestamp(val).strftime("%Y-%m-%d")


def timestamp_to_time(val=time.time()):
    return datetime.fromtimestamp(val).strftime("%H:%M:%S")


def timestamp_to_datetime(val=time.time()):
    return datetime.fromtimestamp(val).strftime("%Y-%m-%d %H:%M:%S")


def date_to_timestamp(val):
    return int(datetime.strptime(val, "%Y-%m-%d").timestamp())


def time_to_timestamp(val):
    return int(datetime.strptime(val, "%H:%M:%S").timestamp())


def datetime_to_timestamp(val):
    return int(datetime.strptime(val, "%Y-%m-%d %H:%M:%S").timestamp())
