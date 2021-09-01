import time
import os
import os.path
import backstage
from shared import Jason
from backstage.core.funcs import wheels_assets


def build(target, app_pkg):
    # version
    version = backstage.get_version(target)
    args = ["setup.py", "--quiet", "sdist", "bdist_wheel"]
    code = backstage.run(args, cwd=target, interactive=False)
    if code == 0:
        _gen_build_report(target, app_pkg, version)
    else:
        raise backstage.BuildError


def _gen_build_report(target, app_pkg, version):
    backstage_data_path = os.path.join(target, app_pkg,
                                       "pyrustic_data",
                                       "backstage",
                                       "report")
    jason = Jason("build_report", default=[],
                  location=backstage_data_path)
    cache = dict()
    cache["timestamp"] = int(time.time())
    wheels_assets_list = wheels_assets(target)
    wheel_asset = None
    if wheels_assets_list:
        wheel_asset = wheels_assets_list[0]
    cache["app_version"] = version
    cache["wheel_asset"] = wheel_asset
    cache["released"] = False
    jason.data.append(cache)
    jason.save()


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message, self.code = (args[0], args[1]) if args else ("", None)
        super().__init__(self.message)

    def __str__(self):
        return self.message
