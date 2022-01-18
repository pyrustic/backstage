import os
import os.path
import sys
import backstage


def main():
    project_dir = os.getcwd()
    args = sys.argv[1:]
    version = backstage.get_version(project_dir)
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
    print("Type 'maj', 'min' or 'rev' for a fast version increment.")
    print("Project version: {}".format(version))
    new_version = input("New version: ")
    if new_version:
        print()
        _change_current_version(project_dir, version, new_version)


def _change_current_version(project_dir, version, new_version):
    new_version = backstage.interpret_version(version, new_version)
    backstage.set_version(project_dir, new_version)
    print("Previous value : {}".format(version))
    print("Current version: {}".format(new_version))


if __name__ == "__main__":
    main()
