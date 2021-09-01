import os
import os.path
import backstage


def main():
    target = os.getcwd()
    version = backstage.get_version(target)
    app_pkg = backstage.get_app_pkg(target)
    try:
        backstage.build(target, app_pkg)
    except backstage.BuildError:
        print("Failed to build a distribution package")
    else:
        print("Successfully built '{}' v{} !".format(app_pkg, version))


if __name__ == "__main__":
    main()
