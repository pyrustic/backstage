import backstage as api
from backstage import error


def process(project_dir, *args):
    """
    Description
    -----------
    Use this command to initialize your project.
    Backstage will install a basic
    project structure in the Target.

    Usage
    -----
    - Description: Init your project
    - Command: init

    Hooking
    -------
    Edit this file:
    $APP_DIR/pyrustic_data/backstage/hooking/init.json
    """
    api.backstage_setup()
    if args:
        print("Wrong usage of this command. Check 'help init'.")
        return
    # init the target
    try:
        api.hooks_runner("init", project_dir)
    except error.NoHooksError:
        print("No hooks available !")
