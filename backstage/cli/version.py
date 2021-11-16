import backstage as api


def process(project_dir, *args):
    """
    Description
    -----------
    Use this command to check or edit the version of the
    project.

    Usage
    -----
    - Description: Check the current version
    - Command: version

    - Description: Set a new version
    - Command: version <sequence>

    - Description: Increment the major number
    - Command: version maj

    - Description: Increment the minor number
    - Command: version min

    - Description: Increment the revision number
    - Command: version rev

    Example
    -------
    - Description: Increment the major number
    - Preliminary: Assume the current version 1.2.3
    - Command: version maj
    - Result: The new version is: 2.0.0

    - Description: Set a version
    - Command: version 2.0.1
    """
    api.backstage_setup()
    app_pkg = api.get_app_pkg(project_dir)
    if not api.initialized(project_dir, app_pkg):
        print("Please initialize this project first. Check 'help init'.")
        return
    version = api.get_version(project_dir)
    # no arg
    if not args:
        _show_current_version(project_dir, version)
    # set a new version
    elif len(args) == 1:
        _change_current_version(project_dir, version, args[0])
    # wrong usage of this command
    else:
        print("Wrong usage of this command")


def _show_current_version(project_dir, version):
    print("Project version: {}".format(version))
    new_version = input("New version: ")
    if new_version:
        print()
        _change_current_version(project_dir, version, new_version)


def _change_current_version(project_dir, version, new_version):
    new_version = api.interpret_version(version, new_version)
    api.set_version(project_dir, new_version)
    print("Previous value : {}".format(version))
    print("Current version: {}".format(new_version))
