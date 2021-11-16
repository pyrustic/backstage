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
    pyrustic_data = os.path.join(app_dir, "pyrustic_data")
    backstage = os.path.join(pyrustic_data, "backstage")
    backstage_hooking = os.path.join(backstage, "hooking")
    backstage_hooking_init = os.path.join(backstage_hooking, "init.json")
    backstage_hooking_build = os.path.join(backstage_hooking, "build.json")
    backstage_hooking_release = os.path.join(backstage_hooking, "release.json")
    backstage_data = os.path.join(backstage, "data")
    backstage_data_build_report = os.path.join(backstage_data, "build_report.json")
    # loop
    items = (tests_init, tests_main, manifest, pyproject_toml, readme,
             setup_cfg, setup_py, version,
             gitignore, init_file, main_file, backstage_hooking_init,
             backstage_hooking_build, backstage_hooking_release,
             backstage_data_build_report)
    for item in items:
        if not os.path.isfile(item):
            return False
    return True


def initialize(project_dir, app_pkg):
    app_pkg = app_pkg if app_pkg else funcs.get_app_pkg(project_dir)
    # create package
    _make_packages(project_dir, app_pkg)
    # create folders
    _make_folders(project_dir, app_pkg)
    # add files
    _add_files(project_dir, app_pkg)
    # add json data files
    _add_json_data_files(project_dir, app_pkg)


def _make_packages(project_dir, app_pkg):
    packages = (app_pkg, "tests")
    for package in packages:
        funcs.build_package(project_dir, package)


def _make_folders(project_dir, app_pkg):
    # folders to make inside app_pkg
    app_dir = os.path.join(project_dir, app_pkg)
    pyrustic_data = os.path.join(app_dir, "pyrustic_data")
    backstage = os.path.join(pyrustic_data, "backstage")
    folders = (backstage, )
    for folder in folders:
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass


def _add_files(project_dir, app_pkg):
    resource_prefix = "template/"
    app_dir = os.path.join(project_dir, app_pkg)
    # add __main__.py
    data = _get_data("backstage", resource_prefix,
                     "main_template.txt")
    data = data.format(title=app_pkg)
    dest = os.path.join(app_dir, "__main__.py")
    _add_file(data, dest)
    # add tests/__main__.py
    data = _get_data("backstage", resource_prefix,
                     "tests_main_template.txt")
    data = data.format(title=app_pkg)
    dest = os.path.join(project_dir, "tests", "__main__.py")
    _add_file(data, dest)
    # add .gitignore
    data = _get_data("backstage", resource_prefix,
                     "gitignore_template.txt")
    dest = os.path.join(project_dir, ".gitignore")
    _add_file(data, dest)
    # add README.md
    data = _get_data("backstage", resource_prefix,
                     "readme_template.txt")
    dest = os.path.join(project_dir, "README.md")
    _add_file(data, dest)
    # add MANIFEST.in
    data = _get_data("backstage", resource_prefix,
                     "manifest_template.txt")
    data = data.format(app_pkg=app_pkg)
    dest = os.path.join(project_dir, "MANIFEST.in")
    _add_file(data, dest)
    # add setup.py
    data = _get_data("backstage", resource_prefix,
                     "setup_py_template.txt")
    dest = os.path.join(project_dir, "setup.py")
    _add_file(data, dest)
    # add setup.cfg
    data = _get_data("backstage", resource_prefix,
                     "setup_cfg_template.txt")
    data = data.format(project_name=os.path.basename(project_dir),
                       app_pkg=app_pkg)
    dest = os.path.join(project_dir, "setup.cfg")
    _add_file(data, dest)
    # add pyproject.toml
    data = _get_data("backstage", resource_prefix,
                     "pyproject_template.txt")
    dest = os.path.join(project_dir, "pyproject.toml")
    _add_file(data, dest)
    # add VERSION
    data = _get_data("backstage", resource_prefix,
                     "version_template.txt")
    dest = os.path.join(project_dir, "VERSION")
    _add_file(data, dest)


def _get_data(pkg, *resource):
    resource = "/".join(resource)
    return pkgutil.get_data(pkg, resource).decode("utf-8")


def _add_json_data_files(project_dir, app_pkg):
    pyrustic_data_dir = os.path.join(project_dir, app_pkg, "pyrustic_data")
    backstage_path = os.path.join(pyrustic_data_dir, "backstage")
    backstage_hooking_dir = os.path.join(backstage_path, "hooking")
    backstage_data_dir = os.path.join(backstage_path, "data")
    # add init.json in hooking dir
    jason = Jason("init.json", location=constant.BACKSTAGE_HOOKING_DIR)
    global_data = jason.data
    Jason("init.json", default=global_data, location=backstage_hooking_dir)
    # add build.json in hooking dir
    jason = Jason("build.json", location=constant.BACKSTAGE_HOOKING_DIR)
    global_data = jason.data
    Jason("build.json", default=global_data, location=backstage_hooking_dir)
    # add release.json in hooking dir
    jason = Jason("release.json", location=constant.BACKSTAGE_HOOKING_DIR)
    global_data = jason.data
    Jason("release.json", default=global_data, location=backstage_hooking_dir)
    # add build_report.json in data dir
    Jason("build_report.json", default=[], location=backstage_data_dir)


def _add_file(data, dest):
    if os.path.exists(dest):
        return
    with open(dest, "w") as file:
        file.write(data)
    
        
class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message
