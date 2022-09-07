<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/backstage/cover.jpg" alt="Demo" width="640">
    <p align="center">
    By © Jorge Royan&nbsp;/&nbsp;<a rel="nofollow" class="external free" href="http://www.royan.com.ar">http://www.royan.com.ar</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=23405928">Link</a>
    </p>
</div>



<!-- Intro Text -->
# Pyrustic Backstage
<b> Three-speed scripting language and task automation tool </b>
    
This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Installation](#installation) . [Demo](#demo) . [Latest](https://github.com/pyrustic/backstage/tags) . [Modules](https://github.com/pyrustic/backstage/tree/master/docs/modules#readme)

**Note to HN user:** I will present this project soon on HN ;)

## Table of contents
- [Overview](#overview)
- [Spawning Processes](spawning-processes)
- [Variables and data types](#variables-and-data-types)
- [Namespaces and persistence](#namespaces-and-persistence)
- [Multithreading and control flow](#multithreading-and-control-flow)
- [Environment variables and operations](#environment-variables-and-operations)
- [File and directory manipulation](#file-and-directory-manipulation)
- [Interfacing with Python](#interfacing-with-python)
- [Embedded documentation and tests](#embedded-documentation-and-tests)
- [Command line interface](#command-line-interface)
- [Miscellaneous](#miscellaneous)
- [Demo](#demo)
- [Installation](#installation)

# Overview
**Backstage** is an **automation tool** that looks for a `backstage.tasks` file in the current working directory to run a specific task defined in that file on demand. Using an eponymous **three-speed scripting language** built for the `backstage.tasks` file, the programmer can define, coordinate and use the various resources at his disposal to automate things.

Let's dive into this concept of three-speed scripting in the following subsections.

## First gear
In first gear, a `backstage.tasks` file is intended to store a list of tasks related to a specific project, each task exposing a list of commands or subtasks to be executed. Here, a command represents a process or a pipeline of processes to be spawned. No other logic is involved.

## Second gear
In second gear, the `backstage.tasks` file not only stores the tasks like in first gear, but here logic intervenes, variables and control flow are used, built-in commands are called, etc. Basically, in second gear, Backstage unleashes its power and allows the programmer to anticipate problems, make sophisticated combinations of subtasks, in short to write a real script to automate tasks.

## Third gear
In third gear, the programmer can directly from the 'backstage.tasks' file, call Python functions with arguments and get the return ! Thanks to this third gear, any complex or overly verbose calculation can be written in Python and called from Backstage. This feature alone proves that Backstage is all about making the programmer's life better, not pretending to replace existing mature solutions that actually work.

## Quick recap
These three speeds make Backstage versatile enough to act either as a simple task runner or as a scripting language with a built-in bridge to the powerful Python ecosystem. Not only are tasks defined in 'backstage.tasks', but their documentation and tests can also be embedded there.

## And more
The command line interface allows the user to discover available tasks, read their documentation, use a glob-like syntax to search for a task by its name or by a keyword that is part of the documentation of the task.

## Example
In the `backstage.tasks` file located at `/home/alex/project`:

```

[task]
# this is a comment
set var (int) = 1 + 2

# default name
set default_name = `John Doe`

# print some text
: I can print your name {var} times in a row !

# take user input
> name : `What is your name ? `

if name == EMPTY
    set name = {default_name}

from 1 to var
    : {R} - Hello {name} !

# connect subtask '_task2' and pass it an argument
& _task2 {name}

[_task2]
# This is a private task (with an underscore as prefix)

# define the variable name (first argument passed to this task)
set name = {ARGS[0]}

# Just say Goodbye !
: Goodbye {name} !

[_task3]
# commands to spawn processes
$ python -m some.module
$ git -m commit "hello world"
$ program1 arg1 {HOME} | program2 "my arg"

[make_coffee]
interface with python.coffeemaker alias coffeebro
set sugar_cubes (int) = 1 + 1 + 1
call coffeebro.make(sugar_cubes)



```

From the command line:

```bash
$ cd /home/alex/project
$ backstage -t
Available tasks (2):
    make_coffee  task
$ backstage task
I can print your name 3 times in a row !
What is your name ? Alex
1 - Hello Alex !
2 - Hello Alex !
3 - Hello Alex !
Goodbye Alex !

```


Check the demo for a more sophisticated example.

# Spawning Processes
It is as simple as this:
```
[task]
$ program arg1 arg2
$ program1 arg1 | program2 "arg"
```

You can automatically send data to the input of a process or redirect STDOUT and STDERR:

```
[task]
# define variables name and age
set name = `John Doe`
set age (int) = 40 + 2

# redirect STDOUT and STDERR
set STDOUT = `/path/to/file_out`
set STDERR = `/path/to/file_err`

# name and age will be pushed to the input of the next spawned process
push name age
$ program1

# from now you can access via the environment variable R, the return code.
: The return code is {R}

# you can capture a process,
# so you will get a direct access to the output and error
($) program2
: Output -> {OUTPUT}
: Error -> {ERROR}

# cross platform DEVNULL:
set STDOUT = /dev/null
$ program3

```

# Variables and data types
Under the hood, **Backstage** works with five Python data types: `str`, `list`, `dict`, `int`, and `float`. But these data types aren't directly used by the programmer. Instead, `assignment tags` are used to tell the interpreter how to treat the variable by default.

These `assignment tags` are: `raw`, `str`, `list`, `dict`, `int`, `float`, `date`, `time`, `dtime`, and `tstamp`.

```
[task]
# this is a string
set var = 42

# this is a dict
set var (dict) = `user="John Doe" age=42 location=Kernel`

# this is an integer
set var (int) = 40 + 2

# this is a raw string
set regex (raw) = `[\S\s]*?`

# get the current timestamp
set now (int) = {NOW}
# 1662569326

# convert it into datetime
set var (dtime) = {now}
# 2022-09-07 17:48:46

```

Note that all variables have a string representation and backticks are used optionally as delimiters that will be ignored by the interpreter.

```
[task]
set var (list) = `a b c d`

# get the value of element at index 1
set data = {var[1]}
# now data contains the letter 'b'

set var (dict) = `name=John age=42`

# get the value of key 'name'
set data = {var.name}
# now data contains 'John'

```

# Namespaces and persistence
Three namespaces exist: `L` for Local, `G` for Global and `D` for Database:

```
[task]
# by default, variables are defined in Local,
# i.e. they are only visible in the scope of the current task
set var = 42
: Var contains {var}
: Var still contains {L:var}

# you can make local variables public
expose var
# from now, you can get a thread-safe access to var 
# from any running task:
: Global var contains {G:var}

# branch _task2
& _task2

[_task2]
: I got {G:var} !

```

You can persist data:

```
[task]
set var = 42
store var

# from now, var can be accessed
# in this current instance or this
# task or in the next instances
: Var contains {D:var}

# if you aren't sure about the existence
# of a variable, just do this:
default var

# it works with a bunch of variables too:
default var1 L:var2 D:var3 G:var4

# from now, if var1 hasn't been manually defined
# by the programmer, it will be
# automatically initialized and
# its value will be an empty string
```

# Multithreading and control flow
You can run a subtask in a new thread like this:

```
[task]
: Welcome !

# run an instance of subtask
# in the same main thread
& subtask

# run a new instance of subtask
# in a new thread !
~ subtask

# yeah this ~ symbol is handpicked by a legit human ;)

[subtask]
: Hello world !

# sleep for 5 seconds
sleep 5
```

Control flow:

```
[task]
set var1 = 1
set var2 = 2


if var1 == var2
    : Yeah var1 and var2 are same same
elif var1 == 3
    : In fact, var1 equals 3
else
    : Huh !

# loop from 0 to 10
# it works with variables too
from 0 to 10
    : {R}

# while loop
while var1 == EMPTY
    : Going to run subtask
    & subtask
    break
    
set string = `Hello world`
set list (list) = 0 1 2 3 4
set dict (dict) = `name=John age=42`

for char in string
    : {char}
    
for item in list
    : {item}

for item in dict
    : key -> {item[0]} ; val -> {item[1]}
    
[subtask]
pass
```

Regular expression in action:

```
[task]
set text = `Hello world`
set sub = `Hello`
set regex (raw) = [\S\s]*?

if text matches regex
    : Match !
elif text !matches regex
    : Mismatch !
elif sub in text
    : Oh sub sub !

```


# Environment variables and operations
Environment variables are local to each instance of task: `ARGS`, `CWD`, `DATE`, `EMPTY`, `ERROR`,`EXCEPTION`, `FALSE`, `HOME`, `LINE`, `N`, `NOW`, `ONE`, `OS`, `OUTPUT`, `R`, `RANDOM`, `SPACE`, `STDERR`, `STDIN`, `STDOUT`, `TASK`, `TIME`, `TIMEOUT`, `TMP`, `TRASH`, `TRUE`, `ZERO`.

I will make a table to give more information about these variables. It is easy to check their contents:

```
[task]
: HOME -> {HOME}
```

```bash
$ backstage task
HOME -> /home/alex
```

# File and directory manipulation
```
[task]
set var = `Hello World`
set path = /home/alex/file.txt
set folder = /home/alex
set regex (raw) = `[\S\s]*?`
set timestamp1 = 1223322233

append var to path
prepend var to path

for char in path (file)
    : Character -> char
    
for line in path (file)
    : {line}
    
browse files in folder
    : {files}

find files in folder matching regex and accessed between timestamp1 and NOW
: Results -> {R}
```


# Interfacing with Python
```
[task]
interface with python.module as my_module
set var1 = 1
set var2 = 2
set var3 = 3
call my_module.function(var1, var2, var3)
: Return -> {R}
```

# Embedded documentation and tests
```
[task]
pass


[task.doc]
This is the description line.

Usage:
    backstage task <option> <path>

Options:
    -m, --msg       Show message
    -x, --exit      Exit blah blah


[task.test]
# perform some test here
assert some_var == some_var
# ...




```


# Command line interface
```bash
$ backstage --help
Welcome to Pyrustic Backstage !
Ultimate task automation tool for hackers.

Usage:
    backstage
    backstage <task> [<argument> ...]
    backstage <option> [<argument> ...]
    
Options:
    -t, --tasks                 Show the list of tasks
    -T, --Tasks                 Show the descriptive list of tasks
    -d, --doc <task>            Show documentation for a specific task
    -c, --check [<task> ...]    Run tests
    -s, --search <pattern>      Search for a task by its name
    -S, --Search <pattern>      Search for a task by keyword
    -h, --help                  Show this information page

Note:
    The Pattern argument of the Search option uses glob-like syntax
    which allows wildcards '*' and '?'.
    
Visit the webpage: https://github.com/pyrustic/backstage

```

# Miscellaneous
**Backstage** itself as a project relies on a `backstage.tasks` file (check the root of this repository). You are reading a document about **Backstage** that has been updated with **Backstage** ! 

# Demo
**NOTE TO MYSELF:** this demo is deprecated (it still uses the previous naive iteration of Backstage).

A demo is available to play with as a **Github Gist**. Feel free to give a feedback in the comments section.

**Play with the [Demo](https://gist.github.com/pyrustic/b3729fd4822fb5048fd443cf7d64f686).**

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

<br>
<br>
<br>

[Back to top](#readme)
