"""Project Backstage API"""
import os
import os.path
import sys
import subprocess
from backstage.core import installation, initialization, funcs, pymisc
from backstage.core import building, publishing, github_client
from shared import Jason
from backstage import constant
from backstage.core import funcs
from backstage.core.lite_test_runner import LiteTestRunner
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata
from backstage.core import pymisc


def dist_version(package):
    """
    Returns the version of the installed distribution package,
    otherwise returns None.
    """
    return metadata.version(package) if package else None


def install():
    """
    This function does this:
    - create directory ~/PyrusticMeta/backstage/config
    - fill the directory with config files
    - create data folder
    """
    installation.install()


def init(target, app_pkg=None):
    """
    Initialize a project by creating a basic project structure inside.

    Parameters:
        - target: str, path to the target project
        - app_pkg: str, the application package

    Note: use the function get_app_pkg to extract what could be a
    legal app_pkg from a target.
    """
    app_pkg = app_pkg if app_pkg else get_app_pkg(target)
    initialization.init(target, app_pkg)


def initialized(target, app_pkg=None):
    """Returns True if the target is initialized, else returns False"""
    app_pkg = app_pkg if app_pkg else get_app_pkg(target)
    tests = os.path.join(target, "tests")
    tests_init = os.path.join(tests, "__init__.py")
    manifest = os.path.join(target, "MANIFEST.in")
    pyproject_toml = os.path.join(target, "pyproject.toml")
    readme = os.path.join(target, "README.md")
    setup_cfg = os.path.join(target, "setup.cfg")
    setup_py = os.path.join(target, "setup.py")
    version = os.path.join(target, "VERSION")
    app_dir = os.path.join(target, app_pkg)
    init_file = os.path.join(app_dir, "__init__.py")
    main_file = os.path.join(app_dir, "__main__.py")
    pyrustic_data = os.path.join(app_dir, "pyrustic_data")
    backstage = os.path.join(pyrustic_data, "backstage")
    backstage_config = os.path.join(backstage, "config")
    backstage_config_init = os.path.join(backstage_config, "init.json")
    backstage_config_build = os.path.join(backstage_config, "build.json")
    backstage_config_release = os.path.join(backstage_config, "release.json")
    backstage_report = os.path.join(backstage, "report")
    backstage_report_build = os.path.join(backstage_report, "build_report.json")
    backstage_report_release = os.path.join(backstage_report, "release_report.json")
    backstage_data = os.path.join(backstage, "data")
    backstage_data_github_release_form = os.path.join(backstage_data,
                                                      "github_release_form.json")

    items = (tests_init, manifest, pyproject_toml, readme, setup_cfg,
             setup_py, version, init_file, main_file, backstage_config_init,
             backstage_config_build, backstage_config_release,
             backstage_report_build, backstage_report_release,
             backstage_data_github_release_form)
    for item in items:
        if not os.path.isfile(item):
            return False
    return True


def link(target):
    """
    Edits the content of ~/PyrusticData/manager/manager_shared_data.json

    This function will edit the "target" value and the "recent" list.
    """
    jason = Jason("recent",
                  location=constant.BACKSTAGE_DATA_PATH)
    recent_list = jason.data
    for i, item in enumerate(recent_list.copy()):
        if item == target:
            del recent_list[i]
    recent_list.append(target)
    len_recent_list = len(recent_list)
    max_items = 5
    if len_recent_list > max_items:
        for i in range(len_recent_list - max_items):
            del recent_list[0]
    recent_list.save()


def recent():
    """
    Returns a LIFO-sorting list of recently linked targets.
    """
    jason = Jason("recent", readonly=True,
                  location=constant.BACKSTAGE_DATA_PATH)
    return [*reversed(jason.data)]


def add(target, destination, *files):  # TODO: os.path.normpath isn't enough !
    """
    Create files and packages in the target project.

    Parameters:
        - target: str, path to the target project
        - destination: str, dotted package name or path relative to the target.
        - files: str, filenames to create.

    Note:
        - The destination can be a dot (in this case, the target is the destination).
        - If a filename already exists, its content is preserved.
        - If destination doesn't exist, it's created.
    """
    # create destination if it doesn't exist
    if destination == "." or ("/" in destination or
                              "\\" in destination):
        destination = os.path.join(target, destination)
        destination = os.path.normpath(destination)
        if not os.path.exists(destination):
            os.makedirs(destination)
    else:
        destination = funcs.build_package(target, destination)
    # add files
    for item in files:
        path = os.path.join(destination, item)
        if os.path.exists(path):
            continue
        with open(path, "w") as file:
            pass


def get_version(target):
    """
    This function read the VERSION file in the target project
    then returns the version (str) of the project.

    Parameters:
         - target: str, path to the target project

    Returns: str, version extracted from $PROJECT_DIR/VERSION or None
    """
    path = os.path.join(target, "VERSION")
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
    return "".join(cache)


def set_version(target, version):
    """
    This function edits the content of $PROJECT_DIR/VERSION

    Parameters:
         - target: str, path to the target project
         - version: str, the version

    Returns:
        - bool, False, if the module version.py is missing
        - bool, True if all right
    """
    if not os.path.exists(target):
        return False
    path = os.path.join(target, "VERSION")
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


def build(target, app_pkg=None):
    """
    Build the target project. A Wheel distribution package is
    created and put in the "dist" folder ($PROJECT_DIR/dist).

    Parameters:
        - target: str, the target
        - app_pkg: str, the application package

    Exceptions:
        - BuildingError: raised if the build fails

    Note: this function uses setuptools to build both a source package distribution
    as well as a Wheel package distribution.
    """
    app_pkg = app_pkg if app_pkg else get_app_pkg(target)
    building.build(target, app_pkg)


def run_tests(target):
    """
    Runs the tests in the target.

    Parameters:
        - target: str, path to the target project

    Returns: a tuple (bool, object). The bool indicate the success
    (True) or the failure (False) of the tests.
    The second item in the tuple can be None, an Exception instance, or a string.

    Note: the tests should be located at $PROJECT_DIR/tests
    """
    test_path = os.path.join(target, "tests")
    test_success = None
    test_result = None
    if os.path.exists(test_path):
        test_host = LiteTestRunner(test_path, target)
        test_success, test_result = test_host.run()
    return test_success, test_result


def run(cmd, cwd=None, python=True, interactive=True):
    """
    Execute a cmd. Cmd is either a list of args or a string.
    Example of commands:
        - "something 'path/to/dir'"
        - ["something", "path/to/dir"]

    Returns: This function returns the exit code.

    Exception:
        - MissingSysExecutableError: raised when sys.executable is missing.

    Note: this function will block the execution of the thread in
    which it is called till the subprocess returns.
    """
    if isinstance(cmd, str):
        cmd = pymisc.parse_cmd(cmd)
    if python:
        if not sys.executable:
            raise MissingSysExecutableError
        cmd.insert(0, sys.executable)
    stdin = None if interactive else subprocess.DEVNULL
    stdout = None if interactive else subprocess.DEVNULL
    stderr = None if interactive else subprocess.DEVNULL
    process = subprocess.Popen(cmd, stdin=stdin, stdout=stdout,
                               stderr=stderr, cwd=cwd)
    process.communicate()
    return process.returncode


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


def get_app_pkg(target):
    """
    This function extracts the application package name from a target path.
    Basically it extracts the basename from the path then turns dashes "-" into
    "underscores" "_".

    Parameters:
        - target: str, path to the target project

    Returns: str, the application package name.
    """
    if not target:
        return None
    basename = os.path.basename(target)
    cache = basename.split("-")
    app_pkg = "_".join(cache)
    return app_pkg


def github_repo_description(kurl, owner, repo):
    """
    Get useful information about a remote Github repository

    Returns: (status_code, status_text, data)

        The status_code is an int, status_text is a string and
        data = {"created_at": date, "description": str,
                "stargazers_count": int, "subscribers_count": int}
    """
    return github_client.repo_description(kurl, owner, repo)


def github_latest_release(kurl, owner, repo):
    """
    Get from a remote Github repository, useful information about
    the latest release (download count, published at, tag_name)

    Parameters:
        - kurl: python.kurl.Kurl instance
        - owner: str, the Github repository's owner name
        - repo: str, the Github repository's repo name

    Returns: (status_code, status_text, data)

        The status_code is an int, status_text is a string and
        data = {"tag_name": str, "published_at": date,
                "downloads_count": int}
    """
    return github_client.latest_release(kurl, owner, repo)


def github_downloads(kurl, owner, repo, maxi=10):
    """
    Get from a remote Github repository the total downloads count
    of the latest x (maxi) releases assets.

    Parameters:
        - kurl: python.kurl.Kurl instance
        - owner: str, the Github repository's owner name
        - repo: str, the Github repository's repo name
        - maxi: int, number of releases to take in consideration
         (from the latest to the oldest)

    Returns: (status_code, status_text, data)

        The status_code is an int, status_text is a string and
        data is an integer to indicate the downloads count
    """
    return github_client.latest_releases_downloads(kurl, owner, repo, maxi)


def release(kurl, target, app_pkg=None):
    """
    Publish the latest built distribution package of the target project.

    Parameters:
        - kurl: a pyrustic.kurl.Kurl instance
        - target: str, path to the target project
        - app_pkg: str, application package

    Exception:
        - PublishingError: raised if the publishing failed

    Note: this function uses Github API to create a new release
    in the Github repository, then upload the distribution package
    as an asset.

    The JSON file "publishing.json" located at $APP_DIR/pyrustic_data
    is read to extract useful data to perform this operation.
    """
    app_pkg = app_pkg if app_pkg else get_app_pkg(target)
    return publishing.publish(kurl, target, app_pkg)


def dist(name):
    """
    Use this function to get some info about an installed
    distribution package

    Parameters:
        name: the distribution name, example: "wheel", "cyberpunk-theme"

    Returns: A dict with these keys:
        name, description, home_page, version,
        author, author_email, maintainer, maintainer_email.

    Note: All values in the returned dict are strings.
    """
    metadata_cache = None
    try:
        metadata_cache = metadata.metadata(name)
    except Exception:
        pass
    keys = (("author", "Author"),
            ("author_email", "Author-email"),
            ("description", "Summary"),
            ("home_page", "Home-page"),
            ("maintainer", "Maintainer"),
            ("maintainer_email", "Maintainer-email"),
            ("version", "Version"))
    data = None
    if metadata_cache:
        data = {"name": name}
        for item in keys:
            if item[1] in metadata_cache:
                data[item[0]] = metadata_cache[item[1]]
    return data


def hooks_runner(operation, target):
    local_config = os.path.join(target, "pyrustic_data", "config")
    local_config_file = os.path.join(local_config,
                                     "{}.json".format(operation))
    if os.path.isfile(local_config_file):
        jason = Jason("init", default=[], location=local_config)
    else:
        jason = Jason(operation, default=[], location=constant.BACKSTAGE_CONFIG_PATH)
    for hook in jason.data:
        cmd = ["-m", hook]
        return_code = run(cmd, cwd=target)
        if return_code != 0:
            return


class Error(Exception):
    """ """
    def __init__(self, *args, **kwargs):
        """ """
        self.code = 0
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ReleaseError(Error):
    """ """
    pass


class MissingReleaseFormError(Error):
    """ """
    pass


class InvalidReleaseFormError(Error):
    """ """
    pass


class BuildError(Error):
    """ """
    pass


class MissingSysExecutableError(Error):
    """ """
    pass
