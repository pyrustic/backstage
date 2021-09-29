import os
import os.path
import sys
import backstage
from shared import Jason


DEFAULT_RELEASE_DESCRIPTION = \
"""
Project released with [Backstage]({backstage_link}).
"""


def get_release_description(target):
    latest_release_path = os.path.join(target, "LATEST_RELEASE.md")
    cache = None
    try:
        with open(latest_release_path, "r") as file:
            cache = file.read()
    except Exception as e:
        pass
    if cache:
        text = cache
    else:
        # default release description
        backstage_link = "https://github.com/pyrustic/backstage"
        text = DEFAULT_RELEASE_DESCRIPTION.format(backstage_link=backstage_link)
    return text


def update_release_jayson(target, build_report,
                          backstage_data_path):
    version = build_report["app_version"]
    jason = Jason("github_release_form.json", default=dict(),
                  location=backstage_data_path)
    # update owner
    if not jason.data.get("owner"):
        owner = input("Github owner: ")
        jason.data["owner"] = owner
    # update repo
    if not jason.data["repository"]:
        repo = os.path.basename(target)
        jason.data["repository"] = repo
    # update name
    repo = jason.data["repository"]
    name = "{} v{}".format(repo, version)
    jason.data["release_name"] = name
    # update tag name
    tag_name = "v{}".format(version)
    jason.data["tag_name"] = tag_name
    # update target commitish
    if not jason.data["target_commitish"]:
        jason.data["target_commitish"] = "master"
    # update description
    owner = jason.data["owner"]
    repository = jason.data["repository"]
    description = get_release_description(target)
    jason.data["description"] = description
    # update is_prerelease
    if not jason.data["is_prerelease"]:
        jason.data["is_prerelease"] = False
    # update is_draft
    if not jason.data["is_draft"]:
        jason.data["is_draft"] = False
    # update upload_asset
    if jason.data["upload_asset"] is None:
        jason.data["upload_asset"] = True
    # update asset name
    asset_name = build_report["wheel_asset"]
    jason.data["asset_name"] = asset_name
    # update asset label
    if not jason.data.get("asset_label"):
        jason.data["asset_label"] = "Download the Wheel"
    # save the changes
    jason.save()
    return True


def get_latest_build_report(backstage_report_path):
    jason = Jason("build_report.json", default=[],
                  location=backstage_report_path)
    latest_build_report = None
    try:
        latest_build_report = jason.data[-1]
    except IndexError:
        pass
    return latest_build_report


def main():
    target = os.getcwd()
    app_pkg = backstage.get_app_pkg(target)
    pyrustic_data_path = os.path.join(target, app_pkg,
                                      "pyrustic_data")
    backstage_report_path = os.path.join(pyrustic_data_path,
                                         "backstage", "report")
    backstage_data_path = os.path.join(pyrustic_data_path,
                                       "backstage", "data")
    # get build_report jayson
    build_report = get_latest_build_report(backstage_report_path)
    if not build_report:
        print("Missing build_report ! Please build the project first !")
        return False
    # check if latest build has already been released
    if build_report["released"]:
        cache = "The latest build version {} has already been released !"
        print(cache.format(build_report["app_version"]))
        return False

    # update release_info.json
    if not update_release_jayson(target, build_report,
                                 backstage_data_path):
        return False
    return True


if __name__ == "__main__":
    if not main():
        sys.exit(1)
