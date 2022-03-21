"""Project Backstage API"""
import os
import os.path
import shlex
import pkgutil
import pathlib
import subrun
import hackernote
from backstage import error


PYRUSTIC_HOME = os.path.join(os.path.expanduser("~"), "PyrusticHome")
BACKSTAGE_HOME = os.path.join(PYRUSTIC_HOME, "backstage")


def get_default_tasks():
    """
    Returns a hackernote structure that represents the default tasks Python-compatible.
    Note that the bodies of sections are strings, i.e., each value in this dict is a string.
    """
    res = "/default_tasks"
    data = pkgutil.get_data("backstage", res).decode("utf-8")
    return data


def create_tasks_file(source, project_dir=None, override=False):
    """
    Create a tasks-file in the project directory.

    [parameters]
    - source: a hackernote structure or a text string that will be saved in 'backstage.tasks'
    - project_dir: path, the project_dir
    - override: boolean, override the current tasks-file if it exists

    [return]
    Returns True or False
    """
    if not project_dir:
        project_dir = os.getcwd()
    data = source if isinstance(source, str) else hackernote.render(source)
    dest = os.path.join(project_dir, "backstage.tasks")
    if os.path.isfile(dest) and not override:
        return False
    with open(dest, "w") as file:
        file.write(data)
    return True


def run(*commands, extra_args=None, project_dir=None):
    """
    Run one or multiple commands with extra arguments

    [parameters]
    - *commands: a command string or multiple commands strings that will be run with the library 'subrun'
    - extra_args: a list of extra arguments to append to the first command only
    - project_dir: the path string

    [return]
    Nothing
    """
    first_command = True
    for command in commands:
        if command.startswith("#"):
            continue
        if first_command:
            first_command = False
            command = _join_command(command, extra_args)
        info = subrun.run(command, cwd=project_dir)
        if not info.success:
            break


def get_tasks(project_dir=None):
    """
    Get a dictionary of available tasks in the tasks file in this project_dir

    [parameters]
    - project_dir: string, path of the project_dir

    [exceptions]
    - error.NoTasksFileError: raised when the tasks file is missing

    [return]
    A dictionary of tasks. Each key is a task name, each value is a list of commands strings.
    Example: {"init": ["do this", "do that"], "build": ["do this", "command 2"]}
    """
    if not project_dir:
        project_dir = os.getcwd()
    filename = os.path.join(project_dir, "backstage.tasks")
    if not os.path.isfile(filename):
        raise error.NoTasksFileError
    return hackernote.parse(pathlib.Path(filename), compact=True)


def _join_command(command, extra_args):
    if not extra_args:
        return command
    try:
        extra_args = " ".join(shlex.quote(item) for item in extra_args)
    except Exception as e:
        msg = "Failed to join the extra_args"
        raise error.Error(msg) from None
    return "{} {}".format(command, extra_args)
