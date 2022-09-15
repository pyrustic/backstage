import os
import os.path
import shlex
import textwrap
import readline
import atexit
import re
from backstage import Backstage, constant, util, text


class Cli:
    def __init__(self, directory):
        self._directory = directory
        self._backstage = Backstage(directory)
        self._tasks = dict()
        self._docs = dict()
        self._intro = None
        self._setup()

    @property
    def directory(self):
        return self._directory

    @property
    def backstage(self):
        return self._backstage

    @property
    def tasks(self):
        return self._tasks

    def run(self, command):
        """command is either a string or a list"""
        if not command:
            return
        if isinstance(command, str):
            command = shlex.split(command, posix=True)
        name = command[0]
        args = command[1:]
        if not self._tasks and name not in ("-h", "--help"):
            print("There is no 'backstage.tasks' file in this directory !")
            return
        if name in ("-i", "--intro"):
            self._print_intro(*args)
        elif name in ("-t", "--tasks"):
            self._print_tasks_list(*args)
        elif name in ("-T", "--Tasks"):
            self._print_descriptive_tasks_list(*args)
        elif name in ("-d", "--doc"):
            self._print_task_description(*args)
        elif name in ("-c", "--check"):
            self._check_tasks(*args)
        elif name in ("-C", "--Check"):
            self._check_tasks_debug(*args)
        elif name in ("-s", "--search"):
            self._search_task(*args)
        elif name in ("-S", "--Search"):
            self._search_keyword(*args)
        elif name in ("-h", "--help"):
            print(text.INTRO)
            print()
            print(text.HELP)
        else:
            self._run_task(name, *args)

    def loop(self):
        if not self._tasks:
            print("There is no 'backstage.tasks' file in this directory !")
            return
        print(text.INTRO)
        print("Press 'Ctrl-c' or 'Ctrl-d' to quit.")
        print("Type '--help' or '-h' to show more information.")
        print()
        while True:
            self._activate_autocomplete()
            entry = self._wait_input()
            if entry is None:
                break
            command = shlex.split(entry, posix=True)
            if not command:
                continue
            self._disable_autocomplete()
            history_length = readline.get_current_history_length()
            self.run(command)
            self._update_history(history_length)

    def _setup(self):
        if not self._load_data():
            return
        readline.parse_and_bind("tab: complete")
        self._activate_autocomplete()
        history_filename = os.path.join(constant.BACKSTAGE_HOME, "history")
        if not os.path.isdir(constant.BACKSTAGE_HOME):
            os.makedirs(constant.BACKSTAGE_HOME)
        if not os.path.isfile(history_filename):
            with open(history_filename, "w") as file:
                pass
        readline.read_history_file(history_filename)
        save_history = lambda filename: readline.write_history_file(filename)
        atexit.register(save_history, history_filename)

    def _load_data(self):
        tasks = util.get_tasks(self._directory)
        if not tasks:
            return False
        self._intro = tasks.get("")
        for key, val in tasks.items():
            if key.startswith("_") or key == "":
                continue
            if key.endswith(".doc"):
                self._docs[key] = val
                continue
            self._tasks[key] = val
        return True

    def _wait_input(self):
        entry = None
        try:
            entry = input("(backstage) ")
        except (KeyboardInterrupt, EOFError) as e:
            print()
        return entry

    def _activate_autocomplete(self):
        words = list(self._tasks.keys())
        words.append("help")
        words = tuple(words)
        c = lambda text, state, words=words: complete_callback(text, state, words)
        readline.set_completer(c)

    def _disable_autocomplete(self):
        readline.set_completer(None)

    def _update_history(self, expected_length):
        while True:
            try:
                readline.remove_history_item(expected_length)
            except Exception:
                break

    def _run_task(self, name, *args):
        task = self._get_task(name)
        if not task:
            return
        self._backstage.run(task, args)

    def _print_intro(self, *args):
        intro = self._intro if self._intro else list()
        print("\n".join(intro).strip("- \n"))

    def _print_tasks_list(self, *args):
        keys = self._tasks.keys()
        results = [k for k in keys if k != "" and not k.endswith(".test")]
        if not results:
            print("No tasks available.")
            return
        n = len(results)
        print("Available tasks ({}):".format(n))
        cache = "  ".join(sorted(results))
        cache = textwrap.wrap(cache)
        cache = "\n".join(cache)
        cache = textwrap.indent(cache, "    ")
        print(cache)

    def _print_descriptive_tasks_list(self, *args):
        if not self._tasks:
            print("No tasks available.")
            return
        n = len(self._tasks)
        print("Available tasks ({}):\n".format(n))
        keys = self._tasks.keys()
        for key in sorted(keys):
            description = "No description"
            for line in self._docs.get(key + ".doc", list()):
                if not line or line.isspace():
                    continue
                description = line.strip()
                break
            print("   [{}]".format(key))
            print("   {}".format(description))
            print()

    def _print_task_description(self, *args):
        if not args:
            print("Incomplete command. The task name is missing.")
            return
        task = self._get_task(args[0])
        if not task:
            return
        try:
            doc = self._docs[task + ".doc"]
        except KeyError as e:
            msg = "Documentation for '{}' doesn't exist."
            print(msg.format(task))
        else:
            print("\n".join(doc).strip("- \n"))

    def _check_tasks(self, *args):
        self._run_tests(*args, debug=False)

    def _check_tasks_debug(self, *args):
        self._run_tests(*args, debug=True)

    def _search_task(self, *args):
        if not args:
            msg = "Incomplete command. The pattern is missing."
            print(msg)
            return
        pattern = args[0]
        results = self._find_tasks_by_pattern(pattern)
        if not results:
            print("No results found.")
            return
        results = [x for x in results if x != "" and not x.endswith(".test")]
        n = len(results)
        print("Results ({}):".format(n))
        cache = "  ".join(sorted(results))
        cache = textwrap.wrap(cache)
        cache = "\n".join(cache)
        cache = textwrap.indent(cache, "    ")
        print(cache)

    def _search_keyword(self, *args):
        if not args:
            msg = "Incomplete command. The pattern is missing."
            print(msg)
            return
        keyword = args[0]
        results = self._find_tasks_by_keyword(keyword)
        if not results:
            print("No results found.")
            return
        results = [x for x in results if x != "" and not x.endswith(".test")]
        n = len(results)
        print("Results ({}):".format(n))
        cache = "  ".join(sorted(results))
        cache = textwrap.wrap(cache)
        cache = "\n".join(cache)
        cache = textwrap.indent(cache, "    ")
        print(cache)

    def _get_task(self, pattern):
        if "*" in pattern or "?" in pattern:
            results = self._find_tasks_by_pattern(pattern)
            n = len(results)
            if n == 0:
                print("No matches.")
                return None
            if n > 1:
                print("Many tasks match this pattern:")
                cache = "  ".join(sorted(results))
                cache = textwrap.wrap(cache)
                cache = "\n".join(cache)
                cache = textwrap.indent(cache, "    ")
                print(cache)
                return None
            if n == 1:
                task = results[0]
                return task
            return None
        else:
            return pattern

    def _find_tasks_by_pattern(self, pattern):
        pattern = pattern.replace("?", r".")
        pattern = pattern.replace("*", r"[\S]*")
        results = list()
        for task in self._tasks.keys():
            if re.fullmatch(pattern, task):
                results.append(task)
        return results

    def _find_tasks_by_keyword(self, keyword):
        keyword = keyword.replace("?", r".")
        keyword = keyword.replace("*", r"[\S]*?")
        results = list()
        for task, body in self._docs.items():
            words = list()
            for line in body:
                for word in line.split():
                    words.append(word)
            for word in words:
                if re.fullmatch(keyword, word):
                    cache = task.split(".")
                    del cache[-1]
                    cache = ".".join(cache)
                    if cache in self._tasks:
                        results.append(cache)
                    break
        return results

    def _run_tests(self, *args, debug=False):
        candidates = list()
        if args:
            for item in args:
                task = self._get_task(item)
                if not task:
                    return
                candidates.append(task + ".test")
        else:
            for task in self._tasks.keys():
                if task.endswith(".test"):
                    candidates.append(task)
        report_exception = show_traceback = False
        if debug:
            report_exception = show_traceback = True
        config = {"FailFast": False, "ReportException": report_exception,
                  "ShowTraceback": show_traceback, "TestMode": True}
        n = len(candidates)
        for i, test in enumerate(candidates):
            if test not in self._tasks:
                msg = "Test skipped: '{}' doesn't exist."
                print(msg.format(test))
            else:
                self._backstage.run(test, config=config)
            if i + 1 != n:
                print()


def complete_callback(text, state, words=None):
    results = [w for w in words if w.startswith(text)]
    if state > len(results):
        return None
    return "{} ".format(results[state])
