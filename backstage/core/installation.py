import os
import os.path
from shared import Jason
from backstage.constant import BACKSTAGE_DATA_PATH, BACKSTAGE_CONFIG_PATH


def install():
    # mkdir $HOME/PyrusticMeta/backstage/config
    _makedirs()
    # init config files
    _init_config_files()
    # init data folder
    _init_data_folder()


def _makedirs():
    paths = (BACKSTAGE_DATA_PATH, BACKSTAGE_CONFIG_PATH)
    for path in paths:
        _make_directory(path)

def _make_directory(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except Exception:
        msg = "Failed to create directory {}".format(path)
        raise Error(msg)


def _init_config_files():
    # init.json
    default = ["backstage.script.init_project"]
    Jason("init", default=default,
          location=BACKSTAGE_CONFIG_PATH)
    # build.json
    default = ["backstage.script.run_tests",
               "backstage.script.build_project",
               "backstage.script.versioning"]
    Jason("build", default=default,
          location=BACKSTAGE_CONFIG_PATH)
    # release.json
    default = ["backstage.script.update_github_release_form",
               "backstage.script.github_release",
               "backstage.script.update_changelog"]
    Jason("release", default=default,
          location=BACKSTAGE_CONFIG_PATH)


def _init_data_folder():
    # recent.json
    default = []
    Jason("recent", default=default,
          location=BACKSTAGE_DATA_PATH)
    # cmd_history.txt
    path = os.path.join(BACKSTAGE_DATA_PATH,
                        "cmd_history.txt")
    if not os.path.exists(path):
        with open(path, "w") as file:
            pass


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message
