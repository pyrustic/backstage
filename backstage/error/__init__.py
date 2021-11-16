class Error(Exception):
    pass


class NoHooksError(Error):
    pass


class BuildError(Error):
    pass


class MissingSysExecutableError(Error):
    pass
