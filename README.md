<!-- Intro Text -->
# Backstage
<b> Command line tool to manage, build and release your Python projects </b>

This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).

<!-- Quick Links -->
[Start a project](#start-a-project) | [Project structure](#project-structure) | [Installation](#installation) | [Reference](https://github.com/pyrustic/backstage/tree/master/docs/reference#readme)

## Overview
This is an overview of available commands in `Backstage`. You can learn more about any command with `help <command>`.

- `link`: Link your `Target project` to the Project Manager.
- `unlink`: Use this command to unlink the currently linked Target.
- `relink`: Link again the previously linked Target or one of
    recent linked Targets.
- `recent`: List of recent Targets.
- `target`: Use this command to check the currently linked Target.
- `init`: Use this command to initialize your project.
- `run`: Use this command to run a module.
- `build`: Use this command to build a distribution package
    that could be published later with the 'release'
    command.
- `release`: Use this command to publish the latest distribution
    package previously built with the command 'build'.
- `hub`: Use this command to retrieve useful information
    from a Github repository.
- `help`: List available commands with "help" or detailed help with "help cmd".
- `EOF`: Enter an [EOF](https://en.wikipedia.org/wiki/End-of-file) to leave.

You can issue these commands programmatically via the function `backstage.oneline.command`.

```python
from backstage.oneline import command

# build the demo project
command(line="build", target="/home/alex/demo")
```

`Backstage` exposes an `API` in the module `pyrustic.manager` (technically in `__init__.py` located in the package `pyrustic.manager`).

```python
import backstage

# build the demo project
target = "/home/alex/demo"
app_pkg = backstage.get_app_pkg(target)  # returns 'demo'
backstage.build(target, app_pkg)
```

Read more about the `API` and `pyrustic.manager.oneline.command` in the [reference](https://github.com/pyrustic/backstage/tree/master/docs/reference#readme).


## Start a project

Once you have [installed](https://github.com/pyrustic/backstage#installation) `backstage`, you can start a project:

```bash
$ backstage
Project Backstage 0.0.1
Website: https://pyrustic.github.io
This software is part of the Pyrustic Open Ecosystem.
Type "help" or "?" to list commands. Enter an EOF to exit.


>>

```

### Step 1: Link the project directory

Link the project to `backstage` by indicating the path of the project folder. This could be a relative path or even a dot to indicate the current working directory.

If you don't submit a path, a file-chooser dialog will open.

```bash
>> link /home/alex/demo
Successfully linked !
[demo] /home/alex/demo

Not yet initialized project (check 'help init')

```
From now on, the project linked to `backstage` will be called the `Target`. You can issue the `target` command to see the currently linked project.

```bash
>>> target
[demo] /home/alex/demo
Not yet initialized project (check 'help init')
```

### Step 2: Initialize the project directory

Now you can initialize your project with the command `init`. Initializing the project will simply create a basic [project structure](#projet-structure).

```bash
>>> init
Successfully initialized !
```
You can then run the project with the command `run`.

If you quit `backstage`, the next time you want to link the same project, run the `relink` command or use the `recent` command.



### One line command
You can initialize a project with just 1 step:
```bash
$ backstage init
```

`backstage` will assume that the `target` is the current working directory.

## Project structure

If you issue the command `init` in `backstage`, the `target` will be populated with files and directories to create a base project following the conventional Python project structure as described in the [Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/).

This is what your project structure will look like:

```bash
demo/  # the demo project ($PROJECT_DIR) [1]
    demo/  # this is the app package ($APP_PKG) [2]
        pyrustic_data/  # Pyrustic config here [3]
        __init__.py
        __main__.py  # the mighty entry point of your app ! [4]
    tests/
        __init__.py
    CHANGELOG.md  # populated with the content of LATEST_RELEASE.md
    LATEST_RELEASE.md  # text displayed on the Latest Release page
    LICENSE  # empty license file, please don't forget to fill it
    MANIFEST.in  # already filled with convenient lines of rules
    pyproject.toml  # the new unified Python project settings file [5]
    README.md  # default nice README (there are even an image inside) [6]
    setup.cfg  # define here your name, email, dependencies, and more [7]
    setup.py  # it is not a redundancy, don't remove it, don't edit it [8]
    VERSION  # unique location to define the version of the app [9]
    .gitignore  # you can edit it if you want
```

- `[1]` This is the project directory ($PROJECT_DIR), also knows as the `target`.
- `[2]` Your codebase lives in the app package ($APP_PKG).
- `[3]` More information later.
- `[4]` This is the entry point of your app.
- `[5]` Read [What the heck is pyproject.toml ?](https://snarky.ca/what-the-heck-is-pyproject-toml/) and the [PEP 518](https://www.python.org/dev/peps/pep-0518/).
- `[6]` The default README looks like [this](https://github.com/pyrustic/demo#readme).
- `[7]` Read this [user guide](https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html) to edit the `setup.cfg` file.
- `[8]` If you want editable installs you still need a `setup.py` [shim](https://twitter.com/pganssle/status/1241161328137515008).
- `[9]` You won't need to edit this file if you use the commands `build` and `release` that have an integrated versioning mechanism.

In order to avoid confusion, let's agree on the following points:
- `demo.core.module` is the dotted name of the `module.py` module present in the `core` package located in the `$APP_PKG`.
- `$APP_PKG.core.module` is the equivalent of `demo.core.module`.
- The `setup.cfg` file can be represented as `$PROJECT_DIR/setup.cfg` or `/path/to/setup.cfg` but never as `demo/setup.cfg` !
- `$APP_DIR` exists. See the next point.
- `$APP_DIR` and `$APP_PKG` represent the same directory. The nuance is that it is more elegant to write `$APP_DIR/misc/data.json` than `$APP_PKG/misc/data.json`.
- `$PROJECT_PKG` does not exist. Only `$PROJECT_DIR` exists.


## Installation
```bash
pip install backstage
```