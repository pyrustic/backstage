class L:
    def __init__(self, runner):
        self._runner = runner

    def __getattr__(self, item):
        return self._runner.local_vars[item]


class G:
    def __init__(self, runner):
        self._runner = runner

    def __getattr__(self, item):
        return self._runner.global_vars[item]


class D:
    def __init__(self, runner):
        self._runner = runner

    def __getattr__(self, item):
        return self._runner.database_vars[item]
