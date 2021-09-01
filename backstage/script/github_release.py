import os
import os.path
import getpass
import backstage
from backstage.core.funcs import create_kurl
from shared import Jason


def get_build_version(target, app_pkg):
    backstage_report_path = os.path.join(target, app_pkg,
                                         "pyrustic_data",
                                         "backstage", "report")
    jason = Jason("build_report", location=backstage_report_path)
    latest_build_report = jason.data[-1]
    return latest_build_report["app_version"]


def _interpret_release_data(data):
    meta_code = data["meta_code"]
    status_code = data["status_code"]
    status_text = data["status_text"]
    if meta_code == 0:
        return True
    if meta_code == 1:
        print("Failed to create release.")
        if status_code:
            print("{} {}".format(status_code, status_text))
        else:
            print(status_text)
        return False
    if meta_code == 2:
        print("Failed to upload asset.\n{} {}".format(status_code,
                                                      status_text))
        return False
    print("Unknown error")
    return False


def main():
    target = os.getcwd()
    app_pkg = backstage.get_app_pkg(target)
    # get build version
    version = get_build_version(target, app_pkg)
    kurl = create_kurl()
    kurl.token = getpass.getpass("Your Github Token: ")
    print("Processing...")
    print("")
    try:
        data = backstage.release(kurl, target, app_pkg)
    except backstage.ReleaseError as e:
        print("Failed to publish the distribution package !")
    except backstage.InvalidReleaseFormError:
        msg = "Missing mandatory elements in 'github_release_form.json' !"
        print(msg)
    except backstage.MissingReleaseFormError:
        msg = ("Missing 'github_release_form.json' !\nPlease init your app via Backstage.")
        print(msg)
    else:
        success = _interpret_release_data(data)
        if success:
            msg = "Successfully published '{}' v{} !"
            print(msg.format(app_pkg, version))


if __name__ == "__main__":
    main()
