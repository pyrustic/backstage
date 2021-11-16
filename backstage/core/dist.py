"""Project Backstage API"""
import sys
import os
import os.path
from setuptools import config as setuptools_config

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


def dist_version(name):
    """
    Returns the version of the installed distribution package,
    otherwise returns None.
    """
    return metadata.version(name) if name else None


def dist_info(name):
    """
    Use this function to get some info about an installed
    distribution package

    Parameters:
        name: the distribution name, example: "wheel", "cyberpunk-theme"

    Returns: A dict with these keys:
        name, description, home_page, version,
        author, author_email, maintainer, maintainer_email.

    Note: All values in the returned dict are strings.
    """
    metadata_cache = None
    try:
        metadata_cache = metadata.metadata(name)
    except Exception:
        pass
    keys = (("author", "Author"),
            ("author_email", "Author-email"),
            ("description", "Summary"),
            ("home_page", "Home-page"),
            ("maintainer", "Maintainer"),
            ("maintainer_email", "Maintainer-email"),
            ("version", "Version"))
    data = None
    if metadata_cache:
        data = {"name": name}
        for item in keys:
            if item[1] in metadata_cache:
                data[item[0]] = metadata_cache[item[1]]
    return data


def get_setup_config(project_dir):
    return setuptools_config.read_configuration(os.path.join(project_dir, "setup.cfg"))
