import os
import os.path
import shlex
import subrun
import backstage
from backstage import constant


def run(*commands, extra_args=None, project_dir=None):
    for i, command in enumerate(commands):
        if i == 0:
            command = _join_command(command, extra_args)
        info = subrun.run(command, cwd=project_dir)
        if not info.success:
            break


def get_tasks(project_dir=None):
    if not project_dir:
        project_dir = os.getcwd()
    filename = os.path.join(project_dir, "backstage.tasks")
    if not os.path.isfile(filename):
        filename = os.path.join(constant.BACKSTAGE_HOME, "backstage.tasks")
    if not os.path.isfile(filename):
        raise backstage.NoTasksFileError
    return _parse_tasks_file(filename)


def _parse_tasks_file(path):
    tasks = dict()
    with open(path, "r") as file:
        raw = file.read()
    lines = raw.splitlines()
    current_task = None
    for line in lines:
        if not line or line.isspace():
            continue
        if line.startswith("[") and line.endswith("]"):
            current_task = line.lstrip("[").rstrip("]")
            tasks[current_task] = list()
            continue
        if current_task:
            tasks[current_task].append(line)
    return tasks


def _join_command(command, extra_args):
    if not extra_args:
        return command
    try:
        extra_args = " ".join(shlex.quote(item) for item in extra_args)
    except Exception as e:
        msg = "Failed to join the extra_args"
        raise backstage.Error(msg) from None
    return "{} {}".format(command, extra_args)
