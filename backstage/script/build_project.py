import os
import os.path
import backstage as api
from backstage import error


def main():
    target = os.getcwd()
    version = api.get_version(target)
    app_pkg = api.get_app_pkg(target)
    try:
        api.build(target, app_pkg)
    except error.BuildError:
        print("Failed to build a distribution package")
        exit(1)
    except Exception:
        print("Unknown error while building a distribution package")
        exit(1)
    else:
        print("Successfully built '{}' v{} !".format(app_pkg, version))


if __name__ == "__main__":
    main()
