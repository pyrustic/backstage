import sys
import subprocess
from backstage.core import pymisc
from backstage import error


def run(cmd, cwd=None, python=True, interactive=True):
    """
    Execute a cmd. Cmd is either a list of args or a string.
    Example of commands:
        - "something 'path/to/dir'"
        - ["something", "path/to/dir"]

    Returns: This function returns the exit code.

    Exception:
        - MissingSysExecutableError: raised when sys.executable is missing.

    Note: this function will block the execution of the thread in
    which it is called till the subprocess returns.
    """
    if isinstance(cmd, str):
        cmd = pymisc.parse_cmd(cmd)
    if python:
        if not sys.executable:
            raise error.MissingSysExecutableError
        cmd.insert(0, sys.executable)
    stdin = None if interactive else subprocess.DEVNULL
    stdout = None if interactive else subprocess.DEVNULL
    stderr = None if interactive else subprocess.DEVNULL
    process = subprocess.Popen(cmd, stdin=stdin, stdout=stdout,
                               stderr=stderr, cwd=cwd)
    process.communicate()
    return process.returncode
