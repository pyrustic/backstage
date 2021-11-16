import os
import os.path
import shlex
from shared import Jason
from backstage.core import constant
from backstage import error
from backstage.core.runner import run


def hooks_runner(operation, project_dir):
    local_config = os.path.join(project_dir, "pyrustic_data", "config")
    local_config_file = os.path.join(local_config,
                                     "{}.json".format(operation))
    if os.path.isfile(local_config_file):
        jason = Jason("init.json", default=[], location=local_config)
    else:
        jason = Jason("{}.json".format(operation), default=[],
                      location=constant.BACKSTAGE_HOOKING_DIR)
    if not jason.data:
        raise error.NoHooksError
    for item in jason.data:
        cmd = shlex.split(item)
        cmd.insert(0, "-m")
        return_code = run(cmd, cwd=project_dir)
        if return_code != 0:
            return
