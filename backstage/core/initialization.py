import os
import os.path
import pkgutil
from shared import Jason
from backstage.core import funcs, constant


def initialized(project_dir, app_pkg=None):
    """Returns True if the project_dir is initialized, else returns False"""
    app_pkg = app_pkg if app_pkg else funcs.get_app_pkg(project_dir)
    tests = os.path.join(project_dir, "tests")
    tests_init = os.path.join(tests, "__init__.py")
    tests_main = os.path.join(tests, "__main__.py")
    manifest = os.path.join(project_dir, "MANIFEST.in")
    pyproject_toml = os.path.join(project_dir, "pyproject.toml")
    readme = os.path.join(project_dir, "README.md")
    setup_cfg = os.path.join(project_dir, "setup.cfg")
    setup_py = os.path.join(project_dir, "setup.py")
    version = os.path.join(project_dir, "VERSION")
    gitignore = os.path.join(project_dir, ".gitignore")
    app_dir = os.path.join(project_dir, app_pkg)
    init_file = os.path.join(app_dir, "__init__.py")
    main_file = os.path.join(app_dir, "__main__.py")
    pyrustic_data = os.path.join(project_dir, ".pyrustic")
    backstage = os.path.join(pyrustic_data, "backstage")
    backstage_config = os.path.join(backstage, "config")
    init_tasks_file = os.path.join(backstage_config, "init.tasks")
    build_tasks_file = os.path.join(backstage_config, "build.tasks")
    release_tasks_file = os.path.join(backstage_config, "release.tasks")
    backstage_data = os.path.join(backstage, "data")
    backstage_data_build_report = os.path.join(backstage_data, "build_report.json")
    # loop
    items = (tests_init, tests_main, manifest, pyproject_toml, readme,
             setup_cfg, setup_py, version, gitignore, init_file,
             main_file, init_tasks_file, build_tasks_file,
             release_tasks_file, backstage_data_build_report)
    for item in items:
        if not os.path.isfile(item):
            return False
    return True



class Error(Exception):
    pass
