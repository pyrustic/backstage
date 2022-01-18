"""Project Backstage API"""
from backstage.core import constant
from backstage.core.backstage_setup import process as backstage_setup
from backstage.core.tasks import run, get_tasks
from backstage.core.initialization import initialized
from backstage.core.versioning import get_version, set_version, interpret_version
from backstage.core.funcs import get_app_pkg, get_project_name
from backstage.core.dist import dist_version, dist_info, get_setup_config
from backstage.core.lite_test_runner import run_tests
from backstage.error import Error
from backstage.error import NoTasksFileError


__all__ = ["constant", "backstage_setup", "run", "initialized",
           "get_version", "set_version", "interpret_version",
           "get_app_pkg", "get_project_name", "dist_version",
           "dist_info", "get_setup_config", "get_tasks",
           "run_tests", "Error", "NoTasksFileError"]
