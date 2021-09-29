from backstage import constant
from shared import Jason
from backstage.handler.link_handler import LinkHandler
import os.path


class RelinkHandler:
    """
    Description
    -----------
    Link again the previously linked Target or one of
    recent linked Targets.

    Usage
    -----
    - Description: Link again the previously linked Target
    - Command: relink

    - Description: Link again a recently linked Target with
    its index
    - Command: relink <index>

    Example
    -------
    - Description: Link again a previously linked Target
    - Preliminary: Assume you want to link again the Target
    with index #2 (found the index with the command "recent")
    - Command: relink 2
    """
    def __init__(self, target,
                 app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._process(args)

    @property
    def target(self):
        return self._target

    def _process(self, args):
        jason = Jason("recent.json", readonly=True,
                      location=constant.BACKSTAGE_DATA_PATH)
        if not jason.data:
            print("- Empty -")
            return
        path = jason.data[-1]
        if len(args) == 1:
            try:
                index = int(args[0])
                path = list(reversed(jason.data))[index]
            except Exception as e:
                print("Wrong index")
                return
        elif len(args) > 1:
            print("Wrong usage of this command")
            return
        link_handler = LinkHandler(self._target, self._app_pkg, *[path])
        self._target = link_handler.target

    def _check_path(self, path):
        """ Returns True if the path is valid, else False """
        if not os.path.exists(path):
            print("{}".format(path))
            print("This path doesn't exist")
            return False
        return True
