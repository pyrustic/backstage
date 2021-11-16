import os
import os.path
import backstage as api
from backstage import error
from shared import Jason


def process(project_dir, *args):
    """
    Description
    -----------
    Use this command to build a distribution package
    that could be published later with the 'publish'
    command.
    The distribution package is a Wheel.

    Usage
    -----
    - Description: Build
    - Command: build

    Hooking
    -------
    Edit this file:
    $APP_DIR/pyrustic_data/backstage/hooking/build.json
    """
    api.backstage_setup()
    app_pkg = api.get_app_pkg(project_dir)
    if not api.initialized(project_dir, app_pkg):
        print("Please initialize this project first. Check 'help init'.")
        return
    if not _project_is_buildable(project_dir, app_pkg):
        return
    try:
        api.hooks_runner("build", project_dir)
    except error.NoHooksError:
        print("No hooks available !")


def _project_is_buildable(project_dir, app_pkg):
    """"""
    backstage_data_path = os.path.join(project_dir,
                                         app_pkg,
                                         "pyrustic_data",
                                         "backstage",
                                         "data")
    jason = Jason("build_report.json", readonly=True,
                  location=backstage_data_path)
    if not jason.data:
        return True
    latest_build_report = jason.data[0]
    if latest_build_report["release_timestamp"] is None:
        msg = "The latest build '{}' hasn't yet been released."
        print(msg.format(latest_build_report["version"]))
        msg = "Do you want to cancel the build operation ?"
        if api.ask_for_confirmation(msg):
            return False
        else:
            print()
            return True
    return True
