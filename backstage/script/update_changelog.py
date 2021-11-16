import os
import os.path
import time
import backstage as api
from datetime import datetime
from shared import Jason


def get_date():
    """ Returns the current date. Format: Month day, year.
    Example: January 15, 2020
    """
    MONTHS = ("January", "February", "March", "April", "May",
              "June", "July", "August", "September", "October",
              "November", "December")
    dt = datetime.fromtimestamp(time.time())
    text = "{month} {day}, {year}".format(month=MONTHS[dt.month - 1],
                                          day=dt.day, year=dt.year)
    return text


def get_latest_build_version(target, app_pkg):
    backstage_report_path = os.path.join(target, app_pkg,
                                         "pyrustic_data",
                                         "backstage", "data")
    jason = Jason("build_report.json", location=backstage_report_path)
    latest_build_report = jason.data[0]
    return latest_build_report["version"]


def update_changelog(path, data, version):
    """ Update the file CHANGELOG.md located at path, with data and version """
    if not data:
        return
    cache = "## Version {} of {}\n"
    data.insert(0, cache.format(version, get_date()))
    data.append("\n\n\n")
    data = "".join(data)
    try:
        with open(path, "r+") as file:
            cache = file.readlines()
            cache.insert(0, data)
            file.seek(0)
            file.write("".join(cache))
            file.truncate()
    except Exception as e:
        pass


def main():
    target = os.getcwd()
    app_pkg = api.get_app_pkg(target)
    version = get_latest_build_version(target, app_pkg)
    # cut LATEST_RELEASE.md content and then log it in CHANGELOG.md
    latest_release_path = os.path.join(target, "LATEST_RELEASE.md")
    try:
        with open(latest_release_path, "r+") as file:
            cache = file.readlines()
            file.seek(0)
            file.write("")
            file.truncate()
    except Exception as e:
        pass
    else:
        changelog_path = os.path.join(target, "CHANGELOG.md")
        update_changelog(changelog_path, cache, version)


if __name__ == "__main__":
    main()
