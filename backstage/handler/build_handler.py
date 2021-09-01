import os
import os.path
import backstage
from shared import Jason


class BuildHandler:
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
    This command will run hooks if they exist.
    The legal hooks are:
    - pre_building_hook.py
    - post_building_hook.py
    """

    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._version = None
        self._pre_building_hook = None
        self._post_building_hook = None
        self._process(target, app_pkg)

    def _process(self, target, app_pkg):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        if not backstage.initialized(target, app_pkg):
            print("Please initialize this project first. Check 'help init'.")
            return
        if not self._check_if_build_wait_for_release(target, app_pkg):
            return
        backstage.hooks_runner("build", target)

    def _check_if_build_wait_for_release(self, target, app_pkg):
        """"""
        backstage_report_path = os.path.join(target,
                                             app_pkg,
                                             "pyrustic_data",
                                             "backstage",
                                             "report")
        jason = Jason("build_report", readonly=True,
                      location=backstage_report_path)
        if not jason.data:
            return True
        latest_build_report = jason.data[-1]
        if not latest_build_report["released"]:
            msg = "The latest build '{}' hasn't yet been released."
            print(msg.format(latest_build_report["app_version"]))
            msg = "Do you want to cancel the build operation ?"
            if backstage.ask_for_confirmation(msg):
                return False
            else:
                return True
        return True
