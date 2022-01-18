import os
import os.path
import time
import subrun
import backstage
from shared import Jason
from backstage.core.funcs import wheels_assets, ask_for_confirmation


def main():
    project_dir = os.getcwd()
    app_pkg = backstage.get_app_pkg(project_dir)
    if not _project_is_buildable(project_dir):
        return
    # version
    version = backstage.get_version(project_dir)
    command = "python -m setup --quiet sdist bdist_wheel"
    print("building v{} ...".format(version))
    info = subrun.ghostrun(command, cwd=project_dir)
    if info.return_code == 0:
        _gen_build_report(project_dir, version)
    else:
        print("Failed to build a distribution package")
        exit(1)
    print("Successfully built '{}' v{} !".format(app_pkg, version))
    _next_version(project_dir)


def _gen_build_report(project_dir, version):
    backstage_data_path = os.path.join(project_dir,
                                       ".pyrustic",
                                       "backstage")
    jason = Jason("build_report.json", default=[],
                  location=backstage_data_path)
    cache = dict()
    cache["build_timestamp"] = int(time.time())
    wheels_assets_list = wheels_assets(project_dir)
    wheel_asset = None
    if wheels_assets_list:
        wheel_asset = wheels_assets_list[0]
    cache["version"] = version
    cache["dist"] = wheel_asset
    cache["release_timestamp"] = None
    jason.data.insert(0, cache)
    jason.save()


def _project_is_buildable(project_dir):
    """"""
    backstage_data_path = os.path.join(project_dir,
                                       ".pyrustic", "backstage")
    jason = Jason("build_report.json", readonly=True,
                  location=backstage_data_path)
    if not jason.data:
        return True
    latest_build_report = jason.data[0]
    if latest_build_report["release_timestamp"] is None:
        msg = "The latest build '{}' hasn't yet been released."
        print(msg.format(latest_build_report["version"]))
        msg = "Do you want to cancel the build operation ?"
        if ask_for_confirmation(msg):
            return False
        else:
            print()
            return True
    return True


def _next_version(project_dir):
    cur_version = backstage.get_version(project_dir)
    print()
    print("What is the next version of your project ?")
    print("Type 'maj', 'min' or 'rev' for a fast version increment.")
    print("Ignore it to increment the 'revision' number.")
    new_version = input("Submit the next version: ")
    if not new_version:
        new_version = "rev"
    version = backstage.interpret_version(cur_version, new_version)
    backstage.set_version(project_dir, version)


if __name__ == "__main__":
    main()
