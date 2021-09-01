import os
import backstage


def main():
    target = os.getcwd()
    app_pkg = backstage.get_app_pkg(target)
    backstage.init(target, app_pkg)
    print("Successfully initialized !")


if __name__ == "__main__":
    main()
