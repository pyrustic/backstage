import backstage


class ReleaseHandler:
    """
    Description
    -----------
    Use this command to publish the latest distribution
    package previously built with the command 'build'.

    Usage
    -----
    - Description: Publish
    - Command: publish

    Hooking
    -------
    This command will run hooks if they exist.
    The legal hooks are:
    - pre_publishing_hook.py
    - post_publishing_hook.py
    """

    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._pre_publishing_hook = None
        self._post_publishing_hook = None
        self._process(target, app_pkg)

    def _process(self, target, app_pkg):
        if target is None:
            print("Please link a Target first. Check 'help target'.")
            return
        if not backstage.initialized(target, app_pkg):
            print("Please initialize this project first. Check 'help init'.")
            return
        backstage.hooks_runner("release", target)
