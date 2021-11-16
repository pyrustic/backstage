"""Project Backstage API"""
from backstage.core import constant
from backstage.core.backstage_setup import process as backstage_setup
from backstage.core.initialization import initialized, initialize
from backstage.core.runner import run
from backstage.core.building import build
from backstage.core.lite_test_runner import run_tests
from backstage.core.releaser import release
from backstage.core.versioning import get_version, set_version, interpret_version
from backstage.core.funcs import get_app_pkg, get_project_name, ask_for_confirmation
from backstage.core.dist import dist_version, dist_info, get_setup_config
from backstage.core.hooking import hooks_runner


__all__ = ["constant", "backstage_setup", "initialized", "initialize", "run",
           "build", "run_tests", "release", "get_version", "set_version",
           "interpret_version", "get_app_pkg", "get_project_name", "ask_for_confirmation",
           "dist_version", "dist_info", "get_setup_config", "hooks_runner"]
