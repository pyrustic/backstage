import os
import os.path
import time
import subrun
from shared import Jason


def main():
    project_dir = os.getcwd()
    if not _project_is_releasable(project_dir):
        exit(1)
    command = "twine upload --skip-existing dist/*"
    info = subrun.run(command)
    if info.success:
        _update_build_report(project_dir)
    else:
        exit(1)


def _update_build_report(project_dir):
    backstage_data_path = os.path.join(project_dir,
                                       ".pyrustic",
                                       "backstage")
    jason = Jason("build_report.json", default=[],
                  location=backstage_data_path)
    if not jason.data:
        return
    for item in jason.data:
        if not item["release_timestamp"]:
            item["release_timestamp"] = int(time.time())
    jason.save()


def _project_is_releasable(project_dir):
    """"""
    backstage_data_path = os.path.join(project_dir,
                                       ".pyrustic",
                                       "backstage")
    jason = Jason("build_report.json", readonly=True,
                  location=backstage_data_path)
    if not jason.data:
        print("No build to release !")
        return False
    latest_build_report = jason.data[0]
    if latest_build_report["release_timestamp"] is None:
        return True
    msg = "The latest build '{}' has already been released."
    print(msg.format(latest_build_report["version"]))
    print("You should make a new build !")
    return False


if __name__ == "__main__":
    main()
