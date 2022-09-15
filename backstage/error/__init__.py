"""Error classes"""


class Error(Exception):
    pass


class IndentError(Error):
    pass


class InterpretationError(Error):
    pass


class SubprocessError(Error):
    pass


class VariableError(Error):
    pass


class Break(Error):
    pass


class Fail(Error):
    pass


class Return(Error):
    pass


class Continue(Error):
    pass


class FailedAssertion(Error):
    pass


class Exit(Error):
    pass
