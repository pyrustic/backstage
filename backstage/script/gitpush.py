import os
import subrun


def main():
    project_dir = os.getcwd()
    command = "git push origin master"
    subrun.run(command, cwd=project_dir)


if __name__ == "__main__":
    main()
