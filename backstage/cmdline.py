import os
import os.path
import sys
import signal
import traceback
import backstage
from cmd import Cmd
from backstage.core import pymisc
from backstage.handler.link_handler import LinkHandler
from backstage.handler.unlink_handler import UnlinkHandler
from backstage.handler.relink_handler import RelinkHandler
from backstage.handler.target_handler import TargetHandler
from backstage.handler.recent_handler import RecentHandler
from backstage.handler.init_handler import InitHandler
from backstage.handler.run_handler import RunHandler
from backstage.handler.add_handler import AddHandler
from backstage.handler.build_handler import BuildHandler
from backstage.handler.release_handler import ReleaseHandler
from backstage.handler.hub_handler import HubHandler
from backstage.handler.version_handler import VersionHandler
from backstage.constant import BACKSTAGE_DATA_PATH
try:
    import readline
except ImportError:
    readline = None


PROMPT_1 = ">> "
PROMPT_2 = ">>> "


# decorator for all commands handlers
def guard(func):
    def obj(self, arg):
        cache = None
        try:
            arg = pymisc.parse_cmd(arg) if isinstance(arg, str) else arg
            cache = func(self, arg)
        except Exception as e:
            print("Oops... Exception occurred !\n")
            print("".join(traceback.format_exception(*sys.exc_info())))
        return cache
    return obj


class Cmdline(Cmd):
    intro = ("""Project Backstage {}\n""".format(backstage.dist_version("backstage"))
             + """Website: https://pyrustic.github.io\n"""
             + """This software is part of the Pyrustic Open Ecosystem.\n"""
             + """Type "help" or "?" to list commands. Enter an EOF to exit.\n\n""")

    prompt = PROMPT_1

    def __init__(self):
        super().__init__()
        self.__history_size = 420
        self.__history_file = None
        self.__target = None
        self.__app_pkg = None
        self.__setup()

    @property
    def target(self):
        if not self.__target:
            return None
        if not os.path.isabs(self.__target):
            self.__target = None
        return self.__target

    @target.setter
    def target(self, val):
        self.__target = val
        self.__app_pkg = None
        if val:
            Cmdline.prompt = PROMPT_2
        else:
            Cmdline.prompt = PROMPT_1

    @property
    def app_pkg(self):
        if not self.__app_pkg:
            self.__app_pkg = backstage.get_app_pkg(self.target)
        return self.__app_pkg

    @app_pkg.setter
    def app_pkg(self, val):
        self.__app_pkg = val

    @property
    def history_size(self):
        return self.__history_size

    @property
    def history_file(self):
        if not self.__history_file:
            self.__history_file = os.path.join(BACKSTAGE_DATA_PATH,
                                               "cmd_history.txt")
        return self.__history_file

    # ========== OVERRIDING ==========

    def preloop(self):
        if readline and self.history_file:
            readline.read_history_file(self.history_file)

    def postloop(self):
        if readline:
            readline.set_history_length(self.history_size)
            try:
                readline.write_history_file(self.history_file)
            except FileNotFoundError:
                pass

    def precmd(self, line):
        if line == "EOF":
            _exit_handler(self)
            #line = ""
        #print()
        return line

    def postcmd(self, stop, line):
        print("\n")
        return stop

    def emptyline(self):
        pass

    # ========== COMMANDS ==========

    @guard
    def do_link(self, args):
        link_handler = LinkHandler(self.target, self.app_pkg,
                                   *args)
        self.target = link_handler.target

    @guard
    def do_unlink(self, args):
        unlink_handler = UnlinkHandler(self.target,
                                       self.app_pkg,
                                       *args)
        self.target = unlink_handler.target
        self.app_pkg = unlink_handler.app_pkg

    @guard
    def do_relink(self, args):
        relink_handler = RelinkHandler(self.target,
                                       self.app_pkg,
                                       *args)
        self.target = relink_handler.target

    @guard
    def do_target(self, args):
        TargetHandler(self.target,
                      self.app_pkg,
                      *args)

    @guard
    def do_recent(self, args):
        RecentHandler(self.target,
                      self.app_pkg, *args)

    @guard
    def do_init(self, args):
        InitHandler(self.target,
                    self.app_pkg, *args)

    @guard
    def do_run(self, args):
        RunHandler(self.target,
                   self.app_pkg, *args)

    @guard
    def do_build(self, args):
        BuildHandler(self.target, self.app_pkg, *args)

    @guard
    def do_release(self, args):
        ReleaseHandler(self.target, self.app_pkg, *args)

    @guard
    def do_hub(self, args):
        HubHandler(self.target, self.app_pkg, *args)

    @guard
    def do_version(self, args):
       VersionHandler(self.target, self.app_pkg, *args)

    # ========== COMMANDS DOC ==========

    def help_link(self):
        print(LinkHandler.__doc__)

    def help_unlink(self):
        print(UnlinkHandler.__doc__)

    def help_relink(self):
        print(RelinkHandler.__doc__)

    def help_target(self):
        print(TargetHandler.__doc__)

    def help_recent(self):
        print(RecentHandler.__doc__)

    def help_init(self):
        print(InitHandler.__doc__)

    def help_run(self):
        print(RunHandler.__doc__)

    def help_build(self):
        print(BuildHandler.__doc__)

    def help_release(self):
        print(ReleaseHandler.__doc__)

    def help_hub(self):
        print(HubHandler.__doc__)

    def help_version(self):
        print(VersionHandler.__doc__)

    def __setup(self):
        # ensure install
        backstage.install()
        # Interrupt process (typically CTRL+C or 'delete' char or 'break' key)
        signal_num = signal.SIGINT
        handler = lambda signum, frame: None
        signal.signal(signal_num, handler)


def _exit_handler(cmdline):
    print("Goodbye !\n")
    cmdline.postloop()
    sys.exit()
