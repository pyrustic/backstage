<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/backstage/cover.jpg" alt="Demo" width="640">
    <p align="center">
    By © Jorge Royan&nbsp;/&nbsp;<a rel="nofollow" class="external free" href="http://www.royan.com.ar">http://www.royan.com.ar</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=23405928">Link</a>
    </p>
</div>



<!-- Intro Text -->
# Backstage
<b> Extensible command line tool for managing software projects </b>
    
This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Installation](#installation) . [Demo](#demo) . [Latest](https://github.com/pyrustic/backstage/tags) . [Documentation](https://github.com/pyrustic/backstage/tree/master/docs/modules#readme)

## Table of contents
- [Overview](#overview)
- [Example](#example)
- [API](#api)
- [Default behavior](#default-behavior)
- [Under the hood](#under-the-hood)
- [Installation](#installation)
- [Demo](#demo)


# Overview
**Backstage** is a **language-agnostic** command-line tool that allows the developer to define, coordinate and use the various resources at his disposal to create and manage a software project.

Concretely, the developer specifies in a `backstage.tasks` file placed at the **root** of a project, the **tasks** necessary for the creation and management of the project. A **task** is represented by a name and a sequence of **commands**. From the **command line**, the developer can launch the execution of a **task** with or without arguments which are automatically passed to the first command of the task.

# Example
Content of a fictitious `backstage.tasks` file:

```
[init]
# This command creates a brand new Python project.
templating --type "default-python-desktop-project"

[build]
# Test the project.
python -m test "test_*"
# Package the project if the tests are successful.
packager --dist "project.whl" --out "build_report.pdf"
# Notify me if the packaging is a success.
notifyme --to "my.email@invalid.earth" -f "build_report.pdf"

[commit]
# The following command accepts additional arguments.
# This example: backstage commit -m "This is a commit"
# is equivalent to: git commit -m "This is a commit"
git commit

[release]
# Release the latest package distribution to GitHub and PyPI.
uploader --dist "project.whl" --to "github-release"
uploader --dist "project.whl" --to "pypi"

```

As you might guess, there are four tasks in the file: `init`, `build`, `commit`, and `release`.

Here is how the `build` task can be started:

```bash
$ cd /path/to/project
$ backstage build
building...
```

To get the list of available tasks:

```bash
$ cd /path/to/project
$ backstage
Project Backstage
https://github.com/pyrustic/backstage

Available Tasks
===============

init  build  commit  release

```

# API
**Backstage** exposes an API (the same used by the CLI) with which you can interact programmatically in Python.

```python 
import backstage

# An arbitrary X project.
# X = an arbitrary programming language.
PROJECT_DIR = "/path/to/project"

# Get default tasks.
default_tasks = backstage.get_default_tasks()  # returns a hackernote structure

# Create default 'backstage.tasks'.
backstage.create_tasks_file(default_tasks, project_dir=PROJECT_DIR)

# Get the tasks defined in 'backstage.tasks'
tasks = backstage.get_tasks(PROJECT_DIR)  # returns a hackernote structure

# Get commands from 'release' task.
commands = tasks["release"]

# Run the commands of the 'release' task.
# Same as running in the command line: backstage release
backstage.run(*commands, project_dir=PROJECT_DIR)

```
As you can see, this API gives you full control over your projects.

> **Read the [modules documentation](https://github.com/pyrustic/backstage/tree/master/docs/modules#readme).**

# Default Behavior
If you issue the `backstage` command without any arguments, **Backstage** will offer to create a default `backstage.tasks` file in the current working directory if this file does not already exist.
This default `backstage.tasks` file is Python-focused since **Backstage** itself is written in Python.

You are free to update the default `backstage.tasks` file to suit your needs since **Backstage** is language agnostic.

## Default backstage.tasks file

This is the contents of the default `backstage.tasks` file:

```
[init]
# Initialize the Python project.
setupinit init

[check]
# Get the project version and latest build information.
buildver check

[test]
# Run tests.
python -m unittest discover -f -s tests -t .

[release]
# Build then release a new version of the project to PyPI.
# Note: you can extend this command in the CLI to set the next version.
# Example: backstage release then 3.0.0
# Example: backstage release then +maj
buildver build
twine upload --skip-existing dist/*

[gitinit]
# Initialize a new Git repository then create a new connection to the remote repository.
# Note: the user is prompted to submit the 'origin'.
git init
python -c 'import subrun; subrun.run("git remote add origin {}".format(input("Origin: ")))'

[gitcommit]
# Save your changes to the local repository.
# Note: the user is prompted to submit a commit message.
git add .
python -c 'import subrun; subrun.run("git commit -m \"{}\"".format(input("Commit message: ")))'

[gitpush]
# Send the commits from your local Git repository to the remote repository
git push origin master
```

As you can see, the default `backstage.tasks` file is self-explanatory since comment strings are supported. A comment line must start with a **hash** ("**#**") symbol as the first character of the line.

The tasks available in the default `backstage.tasks` file are enough to create a new Python project, create a distribution package, perform some basic Git commands, and publish a project to [PyPI](https://pypi.org).

Feel free to create and share `backstage.tasks` with many useful tasks for other developers. The only limit is your imagination.


# Under the hood
Under the hood, **Backstage** makes extensive use of some useful Python packages.

## Hackernote
A `backstage.tasks` file is actually a **hackernote** file whose content is parsed with the **Hackernote** library.

There are many use cases for **Hackernote**. For example, the codebase documentation for [Pyrustic](https://pyrustic.github.io) projects is generated with a tool that parses **docstrings** expressly written in the **hackernote** format.

> **Discover [Hackernote](https://github.com/pyrustic/hackernote) !**

## Subrun
**Backstage** uses the **Subrun** library to run the tasks defined in the `backstage.tasks` file.

**Subrun** is a library that exposes an intuitive API to safely start and communicate with processes in Python.

> **Discover [Subrun](https://github.com/pyrustic/subrun) !**

## Setupinit
In the default `backstage.tasks` file, the `init` task promises to create a standard Python project. This promise relies on the **Setupinit** library whose sole purpose is to ensure that you are working with a [standard Python project](https://packaging.python.org/tutorials/packaging-projects/) that can be packaged and distributed with confidence.

> **Discover [Setupinit](https://github.com/pyrustic/setupinit) !**

## Buildver
The default `backstage.tasks` file exposes a `release` task that aims to build and publish your project. This task uses **Buildver** which is a command line tool to build a Python distribution package from a project. This tool comes with a built-in versioning mechanism that works smoothly with the package builder while being intuitive for the user.

> **Discover [Buildver](https://github.com/pyrustic/buildver) !**

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

# Demo
A demo is available to play with as a **Github Gist**. Feel free to give a feedback in the comments section.

**Play with the [Demo](https://gist.github.com/pyrustic/b3729fd4822fb5048fd443cf7d64f686).**

<br>
<br>
<br>

[Back to top](#readme)
