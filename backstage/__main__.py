import os
import sys
import backstage as api
from backstage import cli


COMMANDS = {"setup": cli.setup, "init": cli.init,
            "run": cli.run, "build": cli.build,
            "release": cli.release, "version": cli.version}


def main():
    project_dir = os.getcwd()
    args = sys.argv[1:]
    COMMANDS["help"] = help_handler
    if not args:
        help_handler(project_dir, *args)
        return
    command = args[0]
    try:
        COMMANDS[command](project_dir, *args[1:])
    except KeyError as e:
        msg = "Unknown command. Type 'help' !"
        print(msg)


def help_handler(project_dir, *args):
    """Help me !"""
    intro = ("""Project Backstage {}\n""".format(api.dist_version("backstage"))
             + """Website: https://pyrustic.github.io\n"""
             + """This software is part of the Pyrustic Open Ecosystem.\n""")
    print("".join(intro))

    print("Available commands")
    print("==================")
    print(" ".join(COMMANDS.keys()))
    print()
    print("Type 'help <command>' for more information.")
    print()
    if not args:
        return
    command = args[0]
    try:
        doc = COMMANDS[command].__doc__
    except KeyError as e:
        print("Unknown command")
    else:
        title = "Command - {}".format(command)
        print(title)
        print("="*len(title))
        print(doc)


if __name__ == "__main__":
    main()
