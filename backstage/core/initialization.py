import os
import os.path
import pkgutil
from shared import Jason
from backstage.core import funcs
from backstage import constant


def init(target, app_pkg):
    # create package
    _make_packages(target, app_pkg)
    # create folders
    _make_folders(target, app_pkg)
    # add files
    _add_files(target, app_pkg)
    # add json data files
    _add_json_data_files(target, app_pkg)


def _make_packages(target, app_pkg):
    packages = (app_pkg, "tests")
    for package in packages:
        funcs.build_package(target, package)


def _make_folders(target, app_pkg):
    # folders to make inside app_pkg
    app_dir = os.path.join(target, app_pkg)
    pyrustic_data = os.path.join(app_dir, "pyrustic_data")
    backstage = os.path.join(pyrustic_data, "backstage")
    hubstore = os.path.join(pyrustic_data, "hubstore")
    folders = (backstage, hubstore)
    for folder in folders:
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass


def _add_files(target, app_pkg):
    resource_prefix = "template/"
    app_dir = os.path.join(target, app_pkg)
    # add VERSION
    resource = resource_prefix + "version_template.txt"
    dest_path = os.path.join(target, "VERSION")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add __main__.py
    resource = resource_prefix + "main_template.txt"
    dest_path = os.path.join(app_dir, "__main__.py")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    data = data.format(title=app_pkg)
    _add_file(dest_path, data)
    # add .gitignore
    resource = resource_prefix + "gitignore_template.txt"
    dest_path = os.path.join(target, ".gitignore")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add LICENSE
    #resource = resource_prefix + "license_template.txt"
    #dest_path = os.path.join(target, "LICENSE")
    #data = pkgutil.get_data("backstage", resource).decode("utf-8")
    #_add_file(dest_path, data)
    # add README.md
    resource = resource_prefix + "readme_template.txt"
    dest_path = os.path.join(target, "README.md")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add MANIFEST.in
    resource = resource_prefix + "manifest_template.txt"
    dest_path = os.path.join(target, "MANIFEST.in")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    data = data.format(app_pkg=app_pkg)
    _add_file(dest_path, data)
    # add setup.py
    resource = resource_prefix + "setup_py_template.txt"
    dest_path = os.path.join(target, "setup.py")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add setup.cfg
    resource = resource_prefix + "setup_cfg_template.txt"
    dest_path = os.path.join(target, "setup.cfg")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    data = data.format(project_name=os.path.basename(target),
                       app_pkg=app_pkg)
    _add_file(dest_path, data)
    # add pyproject.toml
    resource = resource_prefix + "pyproject_template.txt"
    dest_path = os.path.join(target, "pyproject.toml")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add LATEST_RELEASE.Md
    resource = resource_prefix + "latest_release_template.txt"
    dest_path = os.path.join(target, "LATEST_RELEASE.md")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add CHANGELOG.Md
    resource = resource_prefix + "changelog_template.txt"
    dest_path = os.path.join(target, "CHANGELOG.md")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    """
    # add ante_build_hook.py
    resource = resource_prefix + "ante_build_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "ante_build_hook.py")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add post_build_hook.py
    resource = resource_prefix + "post_build_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "post_build_hook.py")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add ante_release_hook.py
    resource = resource_prefix + "ante_release_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "ante_release_hook.py")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    # add post_release_hook.py
    resource = resource_prefix + "post_release_hook_template.txt"
    dest_path = os.path.join(target, app_pkg,
                             "hooking",
                             "post_release_hook.py")
    data = pkgutil.get_data("backstage", resource).decode("utf-8")
    _add_file(dest_path, data)
    """


def _add_json_data_files(target, app_pkg):
    pyrustic_data_path = os.path.join(target, app_pkg,
                                        "pyrustic_data")
    backstage_path = os.path.join(pyrustic_data_path, "backstage")
    backstage_config_path = os.path.join(backstage_path, "config")
    backstage_report_path = os.path.join(backstage_path, "report")
    backstage_data_path = os.path.join(backstage_path, "data")
    hubstore_path = os.path.join(pyrustic_data_path, "hubstore")
    # add init.json
    jason = Jason("init", location=constant.BACKSTAGE_CONFIG_PATH)
    global_data = jason.data
    Jason("init", default=global_data, location=backstage_config_path)
    # add build.json
    jason = Jason("build", location=constant.BACKSTAGE_CONFIG_PATH)
    global_data = jason.data
    Jason("build", default=global_data, location=backstage_config_path)
    # add release.json
    jason = Jason("release", location=constant.BACKSTAGE_CONFIG_PATH)
    global_data = jason.data
    Jason("release", default=global_data, location=backstage_config_path)
    # add build_report.json
    Jason("build_report", default=[], location=backstage_report_path)
    # add release_report.json
    Jason("release_report", default=[], location=backstage_report_path)
    # add github_release_form.json in backstage/data
    default = dict().fromkeys(("owner", "repository", "release_name",
                               "tag_name", "target_commitish", "description",
                               "is_prerelease", "is_draft", "upload_asset",
                               "asset_name", "asset_label"))
    Jason("github_release_form", default=default, location=backstage_data_path)
    # add img.json for Hubstore
    Jason("img", default={"small_img": None, "large_img": None},
          location=hubstore_path)
    # add promotion.json for Hubstore
    Jason("promotion", default={}, location=hubstore_path)


def _add_file(path, data):
    if os.path.exists(path):
        return
    with open(path, "w") as file:
        file.write(data)
    
        
class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message
