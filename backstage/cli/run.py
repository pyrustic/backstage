import os
import os.path
import backstage as api


def process(project_dir, *args):
    """
    Description
    -----------
    Use this command to run a module.
    The module can be located either in the project directory or in
    a regular place where Python stores packages.
    Only dotted name of a module is allowed, so please ignore
    the extension ".py".

    Usage
    -----
    - Description: Run a module
    - Command: run <the.module.name>

    - Description: Run the project
    - Command: run
    Note: Backstage will implicitly run APP_DIR/__main__.py

    - Description: Run a module with some arguments
    - Command: run <the.module.name> <argument_1> <argument_2>

    Example
    -------
    - Description: Run the module
    - Preliminary: Assume that "my_view.py" is in the "view" package
    - Command: run view.my_view

    - Description: Run the module with arguments
    - Preliminary: Assume that "my_view.py" is in the "view" package
    - Command: run view.my_view argument_1 "argument 2"

    - Description: Display the Zen of Python
    - Command: run this

    Note: Please use simple or double quotes as delimiters if a string
    contains space.
    """
    api.backstage_setup()
    app_pkg = api.get_app_pkg(project_dir)
    if not args and not project_dir:
        _print_catalog("missing_project_dir")
        return
    if not args and not os.path.exists(os.path.join(project_dir, app_pkg)):
        print("Please initialize this project first. Check 'help init'.")
        return
    if not args and project_dir:
        args = ["-m", app_pkg]
    else:
        args = ["-m", *args]
    name = _stringify_command(args)
    _print_catalog("running", module=name)
    api.run(args, cwd=project_dir)


def _stringify_command(args):
    cache = []
    for arg in args:
        if " " in arg:
            arg = "\"{}\"".format(arg)
        cache.append(arg)
    return " ".join(cache)


def _print_catalog(item, **kwargs):
    message = ""
    if item == "missing_project_dir":
        message = "Please link a project directory first. Check 'help project_dir'."
    elif item == "running":
        message = "Running: python {}\n...".format(kwargs["module"])
    elif item == "missing_app_pkg":
        message = "Please init the project first. Check 'help init'."
    print(message)
