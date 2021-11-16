import backstage as api


def process(project_dir, *args):
    if args:
        print("Wrong usage of this command. Check 'help setup'.")
        return
    # init the target
    api.backstage_setup()
    print("Setup made with success !")
