import os
import os.path
import shutil
from kurl import Kurl


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
        if os.path.exists(dir):
            continue
        try:
            os.mkdir(dir)
            with open(os.path.join(dir, "__init__.py"), "w") as file:
                pass
        except Exception as e:
            return None
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
