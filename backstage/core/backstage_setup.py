import os
import os.path
import pkgutil
from shared import Jason
from backstage.core import constant
from backstage.error import Error


def process():
    """
    This function does this:
    - create user.json in data dir
    - fill the config directory
    """
    # create user.json
    _create_user_json()
    # create commands tasks files
    resource_prefix = "template"
    _create_tasks_file(resource_prefix)


def _create_user_json():
    jason = Jason("user.json", default={"name": None, "email": None},
                  location=constant.BACKSTAGE_HOME)
    if jason.new:
        print("Hello friend !")
        print()
        name = input("Your name: ")
        email = input("Your email: ")
        name = name if name else "Johnny Silverhand"
        email = email if email else "sapiens@earth.invalid"
        jason.data["name"] = name
        jason.data["email"] = email
        jason.save()
        msg = "You can edit 'user.json' located at '{}' at any time."
        msg = msg.format(constant.BACKSTAGE_HOME)
        print()
        print(msg)
        print()


def _create_tasks_file(resource_prefix):
    dest = os.path.join(constant.BACKSTAGE_HOME, "backstage.tasks")
    if os.path.isfile(dest):
        return
    data = _get_data("backstage", resource_prefix,
                     "tasks.txt")
    _add_file(data, dest)


def _makedir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except Exception:
        msg = "Failed to create the directory '{}'".format(path)
        raise Error(msg)


def _get_data(pkg, *resources):
    resource = "/".join(resources)
    return pkgutil.get_data(pkg, resource).decode("utf-8")


def _add_file(data, dest):
    if os.path.exists(dest):
        return
    with open(dest, "w") as file:
        file.write(data)
