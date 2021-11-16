import os
import os.path
import shutil
from kurl import Kurl


def get_app_pkg(project_dir):
    """
    This function extracts the application package name from a project_dir path.
    Basically it extracts the basename from the path then turns dashes "-" into
    "underscores" "_".

    Parameters:
        - project_dir: str, path to the project_dir project

    Returns: str, the application package name.
    """
    if not project_dir:
        return None
    basename = os.path.basename(project_dir)
    cache = basename.split("-")
    app_pkg = "_".join(cache)
    return app_pkg


def get_project_name(project_dir):
    """Returns the project name"""
    return os.path.basename(project_dir)


def ask_for_confirmation(message, default="y"):
    """
    Use this function to request a confirmation from the user.

    Parameters:
        - message: str, the message to display
        - default: str, either "y" or "n" to tell "Yes by default"
        or "No, by default".

    Returns: a boolean, True or False to reply to the request.

    Note: this function will append a " (y/N): " or " (Y/n): " to the message.
    """
    cache = "Y/n" if default == "y" else "y/N"
    user_input = None
    try:
        user_input = input("{} ({}): ".format(message, cache))
    except EOFError as e:
        pass
    if not user_input:
        user_input = default
    if user_input.lower() == "y":
        return True
    return False


def wheels_assets(target):
    dist_folder = os.path.join(target,
                               "dist")
    if not os.path.exists(dist_folder):
        return []
    assets = []
    for item in os.listdir(dist_folder):
        _, ext = os.path.splitext(item)
        if ext != ".whl":
            continue
        path = os.path.join(dist_folder, item)
        if not os.path.isfile(path):
            continue
        assets.append(item)
    assets = _sort_wheels_names(assets)
    assets.reverse()
    return assets


def copyto(src, dest):
    """
    Please make sure that DEST doesn't exist yet !
    Copy a file or contents of directory (src) to a destination file or folder (dest)
    """
    if not os.path.exists(src) or os.path.exists(dest):
        return False
    if os.path.isdir(src):
        try:
            shutil.copytree(src, dest)
        except Exception as e:
            return False
    else:
        try:
            shutil.copy2(src, dest)
        except Exception as e:
            return False
    return True


def moveto(src, dest):
    """
    If the DEST exists:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        - /home/ocean (DEST)
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/lake
        - /home/ocean/lake/fish.txt
    Else IF the DEST doesn't exist:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/fish.txt


    Move a file or directory (src) to a destination folder (dest)
    """
    if not os.path.exists(src) or os.path.exists(dest):
        return False
    try:
        shutil.move(src, dest)
    except Exception as e:
        return False
    return True


def package_name_to_path(target, package_name, prefix=""):
    # returns a dotted package name to a regular pathname
    # example: package_name_to_path("/home/proj", "view.lol", prefix="tests.")
    return os.path.join(target, *((prefix + package_name).split(".")))


def build_package(target, package_name, prefix=""):
    """
    Literally build a package, returns None or the string pathname
    package represented by prefix must already exist
    """
    splitted = package_name.split(".")
    dir = package_name_to_path(target, prefix) if prefix else target
    for item in splitted:
        dir = os.path.join(dir, item)
        if not os.path.exists(dir):
            try:
                os.mkdir(dir)
            except Exception as e:
                pass
        init_file = os.path.join(dir, "__init__.py")
        if not os.path.exists(init_file):
            try:
                with open(init_file, "w") as file:
                    pass
            except Exception as e:
                pass
    if not os.path.isdir(dir):
        return None
    return dir


def module_name_to_class(module_name):
    """
    Convert a module name like my_module.py to a class name like MyModule
    """
    name = os.path.splitext(module_name)[0]
    # ...
    if not "_" in name:
        return strictly_capitalize(name)
    else:
        splitted = name.split("_")
        cache = []
        for x in splitted:
            cache.append(strictly_capitalize(x))
        return "".join(cache)


def strictly_capitalize(string):
    # I don't remember why I haven't used str.capitalize()
    return string[0].upper() + string[1:]


def get_root_from_package(package_name):
    """
    Return the root from a dotted package name.
    Example the root here "my.package.is.great" is "my".
    """
    splitted = package_name.split(".")
    root = None
    for x in splitted:
        if x == "" or x.isspace():
            continue
        root = x
        break
    return root


def create_kurl():
    headers = {"Accept": "application/vnd.github.v3+json",
               "User-Agent": "Pyrustic"}
    kurl = Kurl(headers=headers)
    return kurl


def get_hub_url(res):
    target = "https://api.github.com"
    return "{}{}".format(target, res)


def _sort_wheels_names(data):
    cache = list()
    for name in data:
        version = name.split("-")[1]
        cache.append((version, name))
    cache.sort(key=lambda s: [int(i) for i in s[0].split('.')])
    return [name for version, name in cache]
