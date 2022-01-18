import os
import sys
import backstage


def main():
    project_dir = os.getcwd()
    args = sys.argv[1:]
    app_pkg = backstage.get_app_pkg(project_dir)
    command = "python -m {}".format(app_pkg)
    backstage.run(command, extra_args=args)


if __name__ == "__main__":
    main()
