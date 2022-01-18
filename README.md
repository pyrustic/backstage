<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/backstage/cover.jpg" alt="Demo" width="640">
    <p align="center">
    By © Jorge Royan&nbsp;/&nbsp;<a rel="nofollow" class="external free" href="http://www.royan.com.ar">http://www.royan.com.ar</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=23405928">Link</a>
    </p>
</div>



<!-- Intro Text -->
# Backstage
<b> Intuitive and extensible command line tool for managing software projects </b>
    
This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Installation](#installation) . [Demo](#demo) . [Latest](https://github.com/pyrustic/backstage/tags) . [Documentation](https://github.com/pyrustic/backstage/tree/master/docs/modules#readme)

## Table of contents
- [Overview](#overview) 
- [Subrun](#subrun)
- [Default behavior](#default-behavior)
- [Installation](#installation)
- [Demo](#demo)


## Overview
**Backstage** is a command-line tool that allows the developer to define, coordinate and use the various resources at his disposal to create and manage a software project.

Concretely, the developer specifies in a `backstage.tasks` file placed at the root of his project, the **tasks** necessary for the creation and management of the project. A task is represented by a name and a sequence of commands. From the command line, the developer can launch the execution of a task with or without arguments which are automatically passed to the first command of the task.

Here is a fictional example of the contents of `backstage.tasks`:

```
[init]
templating --arg "default-python-desktop-project"

[build]
python -m test "test_*"
packager --dist "project.whl" --out "build_report.pdf"
notifyme --to "my.email@invalid.earth" -f "build_report.pdf"

[commit]
git commit

[release]
uploader --dist "project.whl" --to "github-release"
uploader --dist "project.whl" --to "pypi"

```

And this is how the `build` task can be launched:

```bash
> cd /path/to/project
> backstage build
building...
```

To get the list of available tasks:

```bash
> cd /path/to/project
> backstage
Project Backstage 0.0.5
https://pyrustic.github.io
This software is part of the Pyrustic Open Ecosystem.

Available Tasks
===============

init  run  build  release  version  test  gitinit  gitcommit  gitpush

```

**Backstage** exposes an API (the same used by the CLI) with which you can interact programmatically in Python:

```python 
import backstage

project_dir = "/path/to/project"

# get the tasks defined in 'backstage.tasks'
tasks = backstage.get_tasks(project_dir)

# commands for the 'build' task
commands = tasks["build"]

# run the commands
backstage.run(*commands, project_dir=project_dir)

```

Check the [modules documentation](https://github.com/pyrustic/backstage/tree/master/docs/modules#readme).

## Subrun
Under the hood, **Backstage** uses extensively the Python library **Subrun**. 

**Subrun** is an elegant API to safely start and communicate with processes in Python.

> **Discover [Subrun](https://github.com/pyrustic/subrun) !**

## Default Behavior
When a `backstage.tasks` file is missing in the root of your project, **Backstage** rely on a global `backstage.tasks` file located at `$HOME/PyrusticHome/backstage` and created upon the first usage of **Backstage**. This `backstage.tasks` file is made to create and manage Python projects.

This is the contents of the global `backstage.tasks` file:

```
[init]
python -m backstage.script.init

[run]
python -m backstage.script.run

[build]
python -m backstage.script.build

[release]
python -m backstage.script.release

[version]
python -m backstage.script.version

[test]
python -m unittest discover -f -s tests -t .

[gitinit]
python -m backstage.script.gitinit

[gitcommit]
python -m backstage.script.gitcommit

[gitpush]
python -m backstage.script.gitpush

```

Basically, the default behavior of **Backstage** allows the developer to create a packageable Python project with the `init` command, create distribution package with the `build` command that has an integrated automatic versioning system, publish the distribution package to PyPI, run some basic **Git** commands, et cetera.


> **Play with the [Demo](#demo) !**

# Installation
**Backstage** is **cross platform** and versions under **1.0.0** will be considered **Beta** at best. It is built on [Ubuntu](https://ubuntu.com/download/desktop) with [Python 3.8](https://www.python.org/downloads/) and should work on **Python 3.5** or **newer**.

## For the first time

```bash
$ pip install backstage
```

## Upgrade
```bash
$ pip install backstage --upgrade --upgrade-strategy eager

```

## Make your project packageable
**Backstage** is an extensible command line tool for managing software projects. By default, it supports Python, so you can run the `init` command to make your Python project [packageable](https://packaging.python.org/en/latest/tutorials/packaging-projects/):

```bash
$ cd /path/to/project
$ backstage init
Project successfully initialized !
```

You can also create a distribution package of your project with the `build` command, then publish it to [PyPI](https://pypi.org/) with the `release` command, et cetera.

**Discover [Backstage](https://github.com/pyrustic/backstage) !**


# Demo
A demo is available to play with as a **Github Gist**. Feel free to give a feedback in the comments section.

**Play with the [Demo](https://gist.github.com/pyrustic/b3729fd4822fb5048fd443cf7d64f686).**

<br>
<br>
<br>

[Back to top](#readme)
