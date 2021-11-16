import os
import backstage as api


def main():
    project_dir = os.getcwd()
    app_pkg = api.get_app_pkg(project_dir)
    api.initialize(project_dir, app_pkg)
    print("Project successfully initialized !")


if __name__ == "__main__":
    main()
