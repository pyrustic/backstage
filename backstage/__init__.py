"""Project Backstage API"""
import os
import os.path
import sys
import json
from threading import Lock
from backstage import util
from backstage.pattern import Pattern
from backstage import error
from backstage.runner import Runner
from backstage import constant


class Backstage:
    def __init__(self, directory):
        self._directory = directory
        self._cache_dir = os.path.join(directory, ".backstage")
        self._tasks = None
        self._runners = list()
        self._global_vars = dict()
        self._database_vars = dict()
        self._lock = Lock()
        self._i = 0
        self._execution_log = list()
        self._setup()

    @property
    def directory(self):
        return self._directory

    @property
    def tasks(self):
        return self._tasks

    @property
    def global_vars(self):
        return self._global_vars

    @property
    def database_vars(self):
        return self._database_vars

    @property
    def runners(self):
        return self._runners

    @property
    def lock(self):
        return self._lock

    @property
    def execution_log(self):
        return self._execution_log

    def run(self, task, arguments=None, config=None):
        """
        task is a string
        arguments is either None, a string or a list of strings
        """
        runner = Runner(self, task, self.gen_rid(), arguments, config)
        try:
            runner.start()
        except Exception as e:
            pass
        # store data
        filename = os.path.join(self._cache_dir, "database.json")
        with open(filename, "w") as file:
            json.dump(self._database_vars, file)
        # store execution log
        util.save_execution_log(self, self._execution_log)
        return runner

    def gen_rid(self):
        with self._lock:
            rid = self._i
            self._i += 1
            return rid

    def _setup(self):
        # allow python modules imports from backstage.tasks
        sys.path.insert(0, self._directory)
        # create cache_dir
        db_filename = os.path.join(self._cache_dir, "database.json")
        if not os.path.isdir(self._cache_dir):
            try:
                os.makedirs(self._cache_dir)
            except Exception as e:
                pass
            with open(db_filename, "w") as file:
                json.dump(self._database_vars, file)
        # load tasks
        tasks = util.get_tasks(self._directory)
        if not tasks:
            return
        self._tasks = {key: val for key, val in tasks.items() if not key.endswith(".doc")}
        # load stored vars
        
        with open(db_filename, "r") as file:
            database_vars = json.load(file)
        self._database_vars = database_vars if database_vars else dict()
