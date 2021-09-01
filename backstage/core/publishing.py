import os
import os.path
from shared import Jason
import backstage
from backstage.core import github_client


def publish(kurl, target, app_pkg):
    version = _get_version(target, app_pkg)
    # publish
    try:
        data = _publish(kurl, target, app_pkg)
    except Exception as e:
        raise backstage.ReleaseError
    return data


def _get_version(target, app_pkg):
    backstage_report_path = os.path.join(target,
                                         app_pkg,
                                         "pyrustic_data",
                                         "backstage",
                                         "report")
    jason = Jason("build_report", readonly=True,
                  location=backstage_report_path)
    if not jason.data:
        raise backstage.ReleaseError("Missing valid 'build_report.json' !")
    latest_build_report = jason.data[-1]
    return latest_build_report["app_version"]


def _update_build_report(target, app_pkg):
    backstage_report_path = os.path.join(target,
                                         app_pkg,
                                         "pyrustic_data",
                                         "backstage",
                                         "report")
    jason = Jason("build_report",
                  location=backstage_report_path)
    if not jason.data:
        raise backstage.ReleaseError("Missing valid 'build_report.json' !")
    latest_build_report = jason.data[-1]
    latest_build_report["released"] = True
    jason.save()


def _publish(kurl, target, app_pkg):
    backstage_data_path = os.path.join(target, app_pkg,
                                       "pyrustic_data",
                                       "backstage", "data")
    release_form_path = os.path.join(backstage_data_path,
                                     "github_release_form.json")
    if not os.path.exists(release_form_path):
        raise backstage.MissingReleaseFormError
    jason = Jason("github_release_form", location=backstage_data_path)
    owner = jason.data.get("owner")
    repository = jason.data.get("repository")
    release_name = jason.data.get("release_name")
    tag_name = jason.data.get("tag_name")
    target_commitish = jason.data.get("target_commitish")
    description = jason.data.get("description")
    prerelease = jason.data.get("is_prerelease")
    draft = jason.data.get("is_draft")
    upload_asset = jason.data.get("upload_asset")
    asset_name = jason.data.get("asset_name")
    asset_path = os.path.join(target, "dist", asset_name)
    asset_path = None if not os.path.exists(asset_path) else asset_path
    asset_label = jason.data.get("asset_label")
    if (not release_name or not tag_name
            or not asset_path or not owner or not repository):
        raise backstage.InvalidReleaseFormError
    github_release = github_client.Release(kurl, owner, repository)
    data = github_release.publish(release_name, tag_name,
                                  target_commitish, description,
                                  prerelease, draft, upload_asset,
                                  asset_path, asset_name, asset_label)
    if data["meta_code"] == 0:
        _update_build_report(target, app_pkg)
    return data


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message, self.code = (args[0], args[1]) if args else ("", None)
        super().__init__(self.message)

    def __str__(self):
        return self.message
