import os
import os.path


def get_version(project_dir):
    """
    This function read the VERSION file in the project_dir project
    then returns the version (str) of the project.

    Parameters:
         - project_dir: str, path to the project_dir project

    Returns: str, version extracted from $PROJECT_DIR/VERSION or None
    """
    path = os.path.join(project_dir, "VERSION")
    if not os.path.exists(path):
        return None
    with open(path, "r") as file:
        lines = file.readlines()
    if not lines:
        return None
    line = lines[0]
    cache = []
    for char in line:
        if char not in (" ", "\n"):
            cache.append(char)
    version = "".join(cache)
    version = None if not version else version
    return version


def set_version(project_dir, version):
    """
    This function edits the content of $PROJECT_DIR/VERSION

    Parameters:
         - project_dir: str, path to the project_dir project
         - version: str, the version

    Returns:
        - bool, False, if the module version.py is missing
        - bool, True if all right
    """
    if not os.path.exists(project_dir):
        return False
    path = os.path.join(project_dir, "VERSION")
    with open(path, "w") as file:
        file.write(version)
    return True


def interpret_version(cur_version, new_version):
    """
    This function interprets the command to set a new version.

    Parameters:
        - cur_version: str, the current version, the one to alter.
        - new_version: str, the command to set a new version.

    A command can be an actual new version string, or one of the keywords:
     - "maj": to increment the major number of the current version,
     - "min": to increment the minor number of the current version,
     - "rev": to increment the revision number of the current version.

    Returns: The new version as it should be saved in version.py
    """
    if new_version not in ("maj", "min", "rev"):
        return new_version
    cache = cur_version.split(".")
    if not cache:
        return "0.0.1"
    # normalize the size
    if len(cache) == 1:
        cache.extend(["0", "0"])
    elif len(cache) == 2:
        cache.append("0")
    # interpret 'maj', 'min' and 'rev'
    if new_version == "maj":
        number = int(cache[0]) + 1
        cache = [str(number), "0", "0"]
    elif new_version == "min":
        number = int(cache[1]) + 1
        cache = [cache[0], str(number), "0"]
    elif new_version == "rev":
        number = int(cache[2]) + 1
        cache = [cache[0], cache[1], str(number)]
    version = ".".join(cache)
    return version