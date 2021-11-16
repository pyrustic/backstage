import os
import os.path
import backstage as api
from backstage import error
from shared import Jason


def process(project_dir, *args):
    """
    Description
    -----------
    Use this command to release the latest distribution
    package previously built with the command 'build'.

    Usage
    -----
    - Description: Release
    - Command: release

    Hooking
    -------
    Edit this file:
    $APP_DIR/pyrustic_data/backstage/hooking/release.json
    """
    api.backstage_setup()
    app_pkg = api.get_app_pkg(project_dir)
    if not api.initialized(project_dir, app_pkg):
        print("Please initialize this project first. Check 'help init'.")
        return
    if not _project_is_releasable(project_dir, app_pkg):
        return
    try:
        api.hooks_runner("release", project_dir)
    except error.NoHooksError:
        print("No hooks available !")


def _project_is_releasable(project_dir, app_pkg):
    """"""
    backstage_data_path = os.path.join(project_dir,
                                       app_pkg,
                                       "pyrustic_data",
                                       "backstage",
                                       "data")
    jason = Jason("build_report.json", readonly=True,
                  location=backstage_data_path)
    if not jason.data:
        print("No build to release !")
        return False
    latest_build_report = jason.data[0]
    if latest_build_report["release_timestamp"] is None:
        return True
    msg = "The latest build '{}' has already been released."
    print(msg.format(latest_build_report["version"]))
    print("You should make a new build !")
    return False
