import os
import subrun


def main():
    project_dir = os.getcwd()
    message = input("Commit Message: ")
    message = "Update" if not message else message
    commands = ("git add .",
                "git commit -m \"{}\"".format(message))
    for command in commands:
        subrun.run(command, cwd=project_dir)


if __name__ == "__main__":
    main()
