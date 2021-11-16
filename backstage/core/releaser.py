


def release(kurl, project_dir, app_pkg=None):
    """
    Publish the latest built distribution package of the project_dir project.

    Parameters:
        - kurl: a pyrustic.kurl.Kurl instance
        - project_dir: str, path to the project_dir project
        - app_pkg: str, application package

    Exception:
        - PublishingError: raised if the publishing failed

    Note: this function uses Github API to create a new release
    in the Github repository, then upload the distribution package
    as an asset.

    The JSON file "publishing.json" located at $APP_DIR/pyrustic_data
    is read to extract useful data to perform this operation.
    """

    return publishing.publish(kurl, project_dir, app_pkg)