import os
import os.path
import time
from shared import Jason
from backstage.core.funcs import wheels_assets, get_app_pkg
from backstage.core import versioning, runner
from backstage import error


def build(project_dir, app_pkg):
    app_pkg = app_pkg if app_pkg else get_app_pkg(project_dir)
    # version
    version = versioning.get_version(project_dir)
    args = ["setup.py", "--quiet", "sdist", "bdist_wheel"]
    code = runner.run(args, cwd=project_dir, interactive=False)
    if code == 0:
        _gen_build_report(project_dir, app_pkg, version)
    else:
        raise error.BuildError


def _gen_build_report(project_dir, app_pkg, version):
    backstage_data_path = os.path.join(project_dir, app_pkg,
                                       "pyrustic_data",
                                       "backstage",
                                       "data")
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
