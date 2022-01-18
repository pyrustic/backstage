import os
import pkgutil
import backstage
from backstage.core import funcs
from shared import Jason
from backstage import constant


def main():
    project_dir = os.getcwd()
    app_pkg = backstage.get_app_pkg(project_dir)
    initialize(project_dir, app_pkg)
    print("Project successfully initialized !")


def initialize(project_dir, app_pkg=None):
    app_pkg = app_pkg if app_pkg else funcs.get_app_pkg(project_dir)
    # create package
    _make_packages(project_dir, app_pkg)
    # create folders
    _make_folders(project_dir)
    # add files
    _add_app_files(project_dir, app_pkg)
    # add tasks file
    _add_tasks_file(project_dir)
    # add json data files
    _add_json_files(project_dir)


def _make_packages(project_dir, app_pkg):
    packages = (app_pkg, "tests")
    for package in packages:
        funcs.build_package(project_dir, package)


def _make_folders(project_dir):
    # folders to make inside app_pkg
    pyrustic_data = os.path.join(project_dir, ".pyrustic")
    backstage = os.path.join(pyrustic_data, "backstage")
    try:
        os.makedirs(backstage)
    except FileExistsError:
        pass


def _add_app_files(project_dir, app_pkg):
    resource_prefix = "template/app"
    app_dir = os.path.join(project_dir, app_pkg)
    # add __main__.py
    data = _get_data("backstage", resource_prefix,
                     "main_template.txt")
    data = data.format(title=app_pkg)
    dest = os.path.join(app_dir, "__main__.py")
    _add_file(data, dest)
    # add tests/__main__.py
    #data = _get_data("backstage", resource_prefix,
    #                 "tests_main_template.txt")
    #data = data.format(title=app_pkg)
    #dest = os.path.join(project_dir, "tests", "__main__.py")
    #_add_file(data, dest)
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
    jason = Jason("user.json", location=constant.BACKSTAGE_HOME)
    author = jason.data["name"]
    email = jason.data["email"]
    data = _get_data("backstage", resource_prefix,
                     "setup_cfg_template.txt")
    data = data.format(project_name=os.path.basename(project_dir),
                       app_pkg=app_pkg, author=author, email=email)
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


def _add_tasks_file(project_dir):
    src = os.path.join(constant.BACKSTAGE_HOME, "backstage.tasks")
    dest = os.path.join(project_dir, "backstage.tasks")
    with open(src, "r") as file:
        data = file.read()
        _add_file(data, dest)


def _add_json_files(project_dir):
    # ===
    pyrustic_data_dir = os.path.join(project_dir, ".pyrustic")
    backstage = os.path.join(pyrustic_data_dir, "backstage")
    # add build_report.json in data dir
    Jason("build_report.json", default=[], location=backstage)


def _get_data(pkg, *resources):
    resource = "/".join(resources)
    return pkgutil.get_data(pkg, resource).decode("utf-8")


def _add_file(data, dest):
    if os.path.exists(dest):
        return
    with open(dest, "w") as file:
        file.write(data)


if __name__ == "__main__":
    main()
