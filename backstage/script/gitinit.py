import os
import subrun


def main():
    project_dir = os.getcwd()
    git_origin = input("Git origin: ")
    commands = ("git init", "git add .",
                "git commit -m \"First commit\"",
                "git remote add origin {}".format(git_origin))
    for command in commands:
        subrun.run(command, cwd=project_dir)


if __name__ == "__main__":
    main()
