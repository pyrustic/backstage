import os
import os.path
from backstage.core import constant
from shared import Jason


def process():
    """
    This function does this:
    - create directory ~/PyrusticData/backstage/hooking
    - create directory ~/PyrusticData/backstage/data
    - fill the hooking directory with hooking config files
    - app history.json to data dir
    """
    # create backstage hooking dir
    _makedir(constant.BACKSTAGE_HOOKING_DIR)
    # create backstage data dir
    _makedir(constant.BACKSTAGE_DATA_DIR)
    # init.json
    default = ["backstage.script.init_project"]
    Jason("init.json", default=default,
          location=constant.BACKSTAGE_HOOKING_DIR)
    # build.json
    default = ["backstage.script.build_project",
               "backstage.script.versioning"]
    Jason("build.json", default=default,
          location=constant.BACKSTAGE_HOOKING_DIR)
    # release.json
    default = []
    Jason("release.json", default=default,
          location=constant.BACKSTAGE_HOOKING_DIR)


def _makedir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except Exception:
        msg = "Failed to create the directory '{}'".format(path)
        raise Error(msg)


class Error(Exception):
    pass
