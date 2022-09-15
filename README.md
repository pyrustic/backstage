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
> [Installation](#installation) &nbsp; &nbsp; [Demo](#demo) &nbsp; &nbsp; [Latest](https://github.com/pyrustic/backstage/tags) &nbsp; &nbsp; [Modules](https://github.com/pyrustic/backstage/tree/master/docs/modules#readme)


## Table of contents
- [Overview](#overview)
- [Structure of the script file](#structure-of-the-script-file)
- [Spawning processes and branching subtasks](#spawning-processes-and-branching-subtasks)
- [Data types and control flow](#data-types-and-control-flow)
- [Namespaces and persistence](#namespaces-and-persistence)
- [Variable interpolation and escaping](variable-interpolation-and-escaping)
- [Environment variables and language syntax](#environment-variables-and-language-syntax)
- [File and directory manipulation](#file-and-directory-manipulation)
- [Exception handling and tests](#exception-handling-and-tests)
- [Interfacing with Python](#interfacing-with-python)
- [Embedded documentation and tests](#embedded-documentation-and-tests)
- [Command line interface and developer experience](#command-line-interface-and-developer-experience)
- [Miscellaneous](#miscellaneous)
- [Demo](#demo)
- [Installation](#installation)

# Overview
**Backstage** is a cross-platform **automation tool** that looks for a `backstage.tasks` file in the current working directory to run a specific task defined in that file on demand. The `backstage.tasks` file uses the [Jesth](https://github.com/pyrustic/jesth) (**J**ust **e**xtract **s**ections **t**hen **h**ack) file format inspired by the [INI file](https://en.wikipedia.org/wiki/INI_file) format.

 Using an eponymous **three-speed scripting language** designed for the automation tool, the programmer can, inside the `backstage.tasks` file, define, coordinate and use the various resources at his disposal to automate things.

The three-speed scripting language concept is inspired from the three forward gear ratios of early automobiles [transmission system](https://en.wikipedia.org/wiki/Manual_transmission). In the following subsections, we will explore each metaphorical gear of the **Backstage** scripting language, then we will briefly expose the automation tool itself.

## First gear
In first gear, a `backstage.tasks` file is intended to store a list of tasks related to a specific project, each task exposing a list of commands or subtasks to be executed. Here, a command represents a process or pipeline of processes to be spawned. [Environment variables](#environment-variables-and-language-syntax) can be used in commands via [variable interpolation](https://en.wikipedia.org/wiki/String_interpolation). No other logic is involved.

### Example
```
[task1]
# three commands to run sequentially
$ git commit -m 'Update'
$ python -m my.package.module
$ program1 arg1 | program2 {HOME}
---
# run the subtask 'task2'
& task2
---
# run the subtask 'task3' in a new thread
~ task3

[task2]
$ program val1 {CWD}
$ git push origin master

[task3]
# some heavy computation
$ engine -x 5000
$ engine --cleanup

[_task4]
# This is a private task (with an underscore as prefix)
$ clean dir
```

## Second gear
In second gear, the `backstage.tasks` file not only stores the tasks like in first gear, but here logic intervenes, variables are defined, control flow is used, built-in commands are called, et cetera. Basically, in second gear, **Backstage** unleashes its power and allows the programmer to anticipate problems, make sophisticated combinations of subtasks, in short to write a real **script to automate things**.

### Example
```
[task1]
# commit changes
$ git commit -m 'Update'
---
# tell user if 'Commit' has been success
if R == 0
    # print 'Success !'
    : Success !
else
    : Failed to commit changes
---
# say hello ten times
set age = 42
set name = `John Doe`
from 1 to 10
    $ python -m say.hello {name} {age}
---
# create a file in user home
set pathname = {HOME}/iliad.txt
create file pathname
---
# append some data to a file
set data = `\nHello World !`
append data to pathname
---
# browse current working directory
browse files and dirs in CWD
    : Directory -> {R}
    : Files ->
    for item in files
        : - {item}
    : Dirs ->
    for item in dirs
        : - {item}
```

## Third gear
In third gear, in addition with whatever can be done with previous gears, the programmer can directly from the `backstage.tasks` file, call [Python](https://www.python.org/about/) functions with arguments and get the return ! Thanks to this third gear, any too complex or overly verbose calculation can be written in **Python** and called from **Backstage**. This [functionality](#interfacing-with-python) alone proves that **Backstage** is all about making the programmer's life better, not pretending to replace existing mature solutions that actually work.

### Example
```
[task1]
interface with package.coffeemaker alias coffeebro

set sugar_cubes (int) = 1 + 1 + 1
set extra = `milk`

call coffeebro.make(sugar_cubes, extra, 42)

if R == 1
    : Coffee successfully made !
else
    : Oops, failed to make coffee...
    : Exception -> {EXCEPTION}
    : Traceback -> {TRACEBACK}
```

## Automation tool
The scripting language help to define tasks in the `backstage.tasks` file that is intended to be consumed by the automation tool. As an automation tool, **Backstage** exposes a [command line interface](#command-line-interface-and-developer-experience) that allows the user to **discover** available tasks, **run** a task with arguments, read a task [documentation](#embedded-documentation-and-tests), use a [glob](https://en.wikipedia.org/wiki/Glob_(programming))-like syntax to **search** for a task by its name or by a keyword that is part of the documentation of the task, et cetera.

### Example 1
Let's assume that there is a `backstage.tasks` file in the directory `/home/alex/project`. This `backstage.tasks` file contains three public tasks and one private tasks (prefixed with an underscore).

This example shows how one could use the automation tool to run a task defined in the `backstage.tasks` file:

```bash
$ cd /home/alex/project

$ backstage -t
Available tasks (3):
    make_coffee  task1  task2

$ backstage make_coffee
Making coffee...

$ backstage mak*
Making coffee...

$ backstage make_coffee sugar=3
Making coffee with 3 sugar cubes...
```

### Example 2
This is the contents of a `backstage.tasks` file located at `/home/alex/project`:

```
[task]
# define 'x' as a variable with an 'int' assignment tag
set x (int) = 1 + 1 + 1

# default name (by default, the assignment tag is 'str')
set default_name = `John Doe`

# print some text
: Hi and Welcome !
: I can print your name {x} times in a row !

# take user input (always a 'str')
> name : `What is your name ? `

# control flow
if name == EMPTY
    set name = {default_name}

# iteration
from 1 to x
    : {R} - Ave {name} !

# branch subtask '_task2' and pass it an argument
& _task2 {name}


[_task2]
# define the variable 'name' (first argument passed to this task)
set name = {ARGS[0]}

# Just say Goodbye !
: Goodbye {name} !

```

Let's run the task named `task` from the command line:

```bash
$ cd /home/alex/project

$ backstage task
Hi and Welcome !
I can print your name 3 times in a row !
What is your name ? Alex
1 - Ave Alex !
2 - Ave Alex !
3 - Ave Alex !
Goodbye Alex !
```

> **Note:** You can reproduce this example as it. Just [install](#installation) **Backstage**, copy-paste the script in a `backstage.tasks` file, then run `backstage task` in the command line.

## And more
There is more to talk about **Backstage**, like the ability to embed documentation and tests in the `backstage.tasks` file and access them from the command line. Backstage is enough versatile to do the job of a trivial task runner or to automate things with its scripting language that has a built-in bridge to the powerful Python ecosystem.

In the following sections, we will explore this project in depth. You can also jump to the [demo](#demo) to start playing with **Backstage** !

# Structure of the script file
As stated in the [Overview](#overview) section, a `backstage.tasks` file follows the [Jesth](https://github.com/pyrustic/jesth) (**J**ust **e**xtract **s**ections **t**hen **h**ack) file format inspired by the [INI file](https://en.wikipedia.org/wiki/INI_file) format.

In a `backstage.tasks` file, a section represents a task. The section title is the name of the task and the section body is made of commands to run and the constructs of the **Backstage** scripting language. A valid task name is an alphanumeric string that can contains an underscore.

```
You can write here at the top of the script,
a description of the script,
the date of its creation,
or any useful information.

[task1]
# body of task1
...

[task2]
# body of task2
...

[_private]
# prefix a task name with an underscore
# to turn it into a private task that
# won't appear in the list of available tasks
# when you will type 'backstage --tasks' in the command line
```

As you can guess, a line starting with `#` is a comment. But this is only true inside a task body, because in fact not all sections are tasks as described before: a section can also be an embedded test or documentation.


## Embedded documentation
You can embed documentation inside the `backstage.tasks` file. To create a documentation for a task, create a section which name is postfixed with `.doc`:

```
[task1]
pass


[task1.doc]
This is the description line.

Usage:
    backstage task <option> <path>

Options:
    -m, --msg       Show message
    -x, --exit      Exit blah blah

```

From the **command line**, you can read the documentation of an arbitrary task:

```bash
$ backstage -d task1
This is the description line.

Usage:
    backstage task <option> <path>

Options:
    -m, --msg       Show message
    -x, --exit      Exit blah blah
```

## Embedded tests

You can embed tests inside the `backstage.tasks` file. To create a test for a task, create a section which name is postfixed with `.test`:

```
[task1.test]
# perform some test here

# ...

assert some_var == some_var
```

From the **command line**, you can run the test of an arbitrary task:

```bash
$ backstage --check task1
```

or the tests of a bunch of tasks:

```bash
$ backstage --check task1 task2 task3
```

or run all tests defined in the `backstage.tasks` file:

```bash
$ backstage --check
```


# Spawning processes and branching subtasks
You can write commands to spawn a process or a pipeline of processes:

```
[task]
# spawn Git to perform a 'commit'
$ git commit -m "Update"

# spawn a pipeline of three processes
$ program1 arg1 | program2 arg2 | program3
```

Commands to spawn processes support variable interpolation:
```
[task]
# use HOME environment variable
$ ls {HOME}

# access the first index of the ARGS list
$ program {ARGS[0]}
```

You can **push** data to the **input** of a process:

```
[task]
# define variables name and age
set name = `John Doe`
set age (int) = 40 + 2

# name and age will be pushed to the input of the next spawned process
push name age
$ program1 {HOME}

# from now you can access via the environment variable R,
# the return code (exit status code)
: The return code is {R}
```


You can **capture** a process:

```
[task]
# you can capture a process,
# so you will get a direct access to the output and error
($) program2

# print the content of OUTPUT and ERROR
: Output -> {OUTPUT}
: Error -> {ERROR}
```


You can redirect **STDOUT** and **STDERR**:

```
[task]

# redirect STDOUT and STDERR
set STDOUT = `/path/to/file_out`
set STDERR = `/path/to/file_err`

$ program1

---

# cross platform DEVNULL:
set STDOUT = /dev/null

$ program2
```

## Branching subtasks
You can branch a subtask and pass arguments to it:

```
[task1]
# branch 'task2'
& task2 {HOME}

[task2]
# from task2, we can access arguments passed to it.
# ARGS (environment variable) is a list of arguments.
: Arguments -> {ARGS}
```

Whenever you branch a subtask, a new instance of this subtask is created, with its own variables. You can share data with a subtask with one of these three ways:
- pass arguments to the subtask while branching it;
- use the global [namespace](#namespaces-and-persistence);
- use the database [namespace](#namespaces-and-persistence).

A subtask can also return data that is cached in the `R` environment variable:

```
[task1]
& task2 "John Doe"
# from now, R contains 'Hello John Doe !'

[task2]
set result = `Hello {ARGS} !`
return result
```

### Multithreading
Branching a subtask is done in the main thread. But one can create a new thread for a subtask:

```
[task1]
# run an instance of task2 in a new thread
~ task2

# the next command won't wait 'task2' to complete
$ git commit -m "Update"


[task2]
# this task sleeps for 5 seconds
sleep 5
```


# Data types and control flow
In the next subsections we will talk about data types then control flow.

## Data types
**Backstage** supports [variables](https://en.wikipedia.org/wiki/Variable_(computer_science)) and let the programmer set, use, clear, and drop variables.

Under the hood, **Backstage** works with five **Python** data types: `str`, `list` (one-dimensional), `dict` (one-dimensional), `int`, and `float`. But these data types aren't intended to be directly used by the programmer. Instead, `assignment tags` are used to tell the interpreter how to treat a variable.

These `assignment tags` are: `raw`, `str`, `list`, `dict`, `int`, `float`, `date`, `time`, `dtime`, and `tstamp`.

```
[task]
# this is a string
set var = 42

# this is another string
set var (str) = `Hello World`

# this is a list
set var (list) = `reg green blue`

# this is the same list but edited
set var[0] = `yellow`
# var -> yellow green blue

# this is a dict
set var (dict) = `user="John Doe" age=42 location=Kernel`

# this is the same dict but edited
set var.user = `Jane Doe`
# var -> user='Jane Doe' age=42 location=Kernel

# this is an integer
set var (int) = 40 + 2
# var -> 42

# this is a raw string
set regex (raw) = `[\S\s]*?`

# get the current timestamp
set now (int) = {NOW}
# now -> 1662569326

# convert it into datetime
set var (dtime) = {now}
# var -> 2022-09-07 17:48:46

# go from a datetime to timestamp
set var (tstamp) = `2022-09-07 17:48:46`
# var -> 1662569326

# extract the time part of a timestamp
set var (time) = 1662569326
# var -> 17:48:46
```

> Note that all variables have a **string** representation and [backticks](https://en.wikipedia.org/wiki/Backtick) are used optionally as delimiters that will be ignored by the interpreter. So you can put backticks around an integer, and you can insert a list in a string.

### Here document
**Backstage** supports [here document](https://en.wikipedia.org/wiki/Here_document) for strings inside the `backstage.tasks` file:
```
[task]
# this is a text with two lines
set text (str) = `First line\nSecond line`

# this is another text with three lines
set text = `January\nFebruary\nMarch`

# this is not a text with two lines
set var (raw) = `Hello\nWorld`

# this is not a text with two lines
set var (str) = `Hello\\nWorld`
```

### Variable interpolation
[Variable interpolation](https://en.wikipedia.org/wiki/String_interpolation) is supported with the ability to access from a list or a string, the value at an arbitrary index, or from a dictionary, the value of a key.

```
[task]
# let's play with 'str' variables
set x = `red`
set var = `{x} green blue`
# var -> red green blue

# get the value of element at index 0
set value = {var[0]}
# value -> r

---

# let's play with a list
set x = `red`
set var (list) = `{x} green blue`

# get the value of element at index 0
set value = {var[0]}
# value -> red

---

# let's play with a dict
set x (int) = 40 + 2
set var (dict) = `name="John Doe" age={x}`

# get the value of key 'name'
set value = {var.name}
# value -> John Doe

# get the value of key 'age'
set value = {var.age}
# value -> 42

---

# cancel the variable interpolation
set var1 = `Hello` 
set var2 = `{{var1}} World`
# var2 -> {var1} World
```

## Control flow
**Backstage** implements conditionals and loops. A wide range of operators are available to compare values.
### Conditionals
```
[task]
set var1 = 1
set var2 = 1
set x = 2
set regex (raw) = `[\S\s]*?`
set text = `Hello world`
set y = `Hello`

# conditionals support the classic
# operators: == != > < >= <= 
if var1 == 1
    $ program1
elif var2 == x
    $ program2
else
    $ program3
   
# Backstage supports logical and/or 
if var1 == var2 and var1 >= 3
    $ program1

# use the 'matches' operator
# or the negated one: !matches
if regex matches text
    : Matched !
elif regex !matches text
    : Mismatched !
    
# you can use the in operator
# and also the negated one: !in
if y in text
    pass
elif y !in text
    pass

```


### Loops
```
[task]

# From To loop
from 10 to 0
    : {R}
    
# For loop - iterate over a string
set text = `Hello World`
for char in text
    # N is an environment variable that serves as counter
    # for all loops
    : {N}- {char}

# For loop - iterate over a list
set data (list) = `red green blue`
for item in data
    : {item}
    
# For loop - iterate over a dict
set data (dict) = `name="John Doe" age=42`
for item in data
    : key -> {item[0]}  value -> {item[1]}
    
# For loop - iterate over a file
set path = `/home/alex/iliad.txt`
for line in path (file)
    : Line {N}
    : {line}
    :
    
# while loop
set var = 1
while var == 1
    : One Time Hello
    break
    
# browse loop
set path = `/home/alex`
browse files and dirs in path
    : Directory -> {R}
    for item in files
        : {item}
    for item in dirs
        : {item} 
```



# Namespaces and persistence
[Namespaces](https://en.wikipedia.org/wiki/Namespace) are implemented in **Backstage** to provide convenient management of variables by defining three [scopes](https://en.wikipedia.org/wiki/Scope_(computer_science)): 
- `L` for **Local** scope;
- `G` for **Global** scope;
- `D` for **Database** scope.

By default, variables exist in the **Local** namespace and are only accessible to the running task.

To share data with a subtask, one can expose arbitrary variables that will be copied into the **Global** namespace which is readable and writable (thread-safe) by all subtasks.

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

Data can also be **persisted**:

```
[task]
set var = 42
store var

# from now, 'var' can be accessed by all tasks
# in this runtime but also in future runtimes
: Var contains {D:var}

# if you aren't sure about the existence
# of a variable, just do this:
default var

# it also works with a bunch of variables:
default var1 L:var2 D:var3 G:var4

# from now, if 'var1' hasn't been manually defined
# by the programmer, it will be
# automatically initialized and
# its value will be an empty string
```

Persisted variables are stored in `.backstage/database.json`.


# Variable interpolation and escaping
During the string interpolation of a command that spawn processes or branch a subtask, variables that are of the `str` type are automatically [shell-escaped](https://en.wikipedia.org/wiki/Escape_character).

```
[task]
# This is a 'str' variable (backticks aren't quotes, by the way!)
set name = `John Doe` 
set colors (list) = `red green blue`

: Welcome {name} !
# Welcome John Doe

$ program name={name} -c {colors}
# program name='John Doe' -c red green blue

# Notice the quotes automatically added around the name John Doe
```

# Environment variables and language syntax
Environment variables are local to each instance of task. They are defined as uppercase strings. One can edit their contents but can't create new environment variables.

This is the exhaustive list of environment variables:

|Variables|Description|
|---|---|
|`ARGS`|List of arguments passed to this task from the command line|
|`CWD`|Current working directory|
|`DATE`|The current date in the **YYYY-MM-DD** format|
|`EMPTY`|Just an empty string|
|`ERROR`|Error string from a process previously spawned|
|`EXCEPTION`|Name of the last exception raised|
|`FALSE`|The integer **0**|
|`HOME`|The path to `$HOME`. Example: `/home/alex`|
|`LINE`|The current line (1-based numbering) of execution in the task body|
|`N`|Counter for `while`, `for`, `from`, and `browse` loops|
|`NOW`|Current timestamp in seconds|
|`ONE`|The integer **1**|
|`OS`|The running operating system: `aix`, `linux`, `win32`, `cygwin`, `darwin`|
|`OUTPUT`|Output string from a process previously spawned|
|`R`|The **return** of Python functions, built-in commands, statements, constructs, or process exit status codes|
|`RANDOM`|Random integer between **0** and **255** (closed interval)|
|`SPACE`|One space ` ` character|
|`STDERR`|Use this variable to perform **STDERR** redirection|
|`STDIN`|Use this variable to perform **STDIN** redirection|
|`STDOUT`|Use this variable to perform **STDOUT** redirection|
|`TASK`|The name of the currently running task|
|`TIME`|The current time in the **HH:MM:SS** format|
|`TIMEOUT`|Timeout in seconds for commands that spawn processes. Default value: **30** seconds|
|`TMP`|Temporary directory. **Attention**, this directory will automatically disappear at the end of the runtime ! So think twice before moving files inside|
|`TRACEBACK`|[Traceback](https://en.wikipedia.org/wiki/Stack_trace#Python) of the last exception raised|
|`TRASH`|Path to the trash: `$HOME/PyrusticData/trash`|
|`TRUE`|The integer **1**|
|`ZERO`|The integer **0**|

> Note that the `TRACEBACK` and `EXCEPTION` variables are cleared after the next successful command. **Backstage** also generates for convenience, `ARG0`, `ARG1`, `ARGx`, according to the contents of `ARGS`. For example, if `ARGS`contains two arguments, you can expect that `ARG0` and `ARG1` exist.

## Language syntax
In this section we will explore the built-in commands, statements, keywords, symbols, and language constructs that make **Backstage**.

> Note that wherever a built-in command or statement expects a **variable** that will be **read**, for convenience you can instead of supplying a variable name, define an **inline** `int` or `float` literal.

> Also, consider that the `R` environment variable is your friend, since it is used to cache the data returned by a statement, a construct, or a command.

### APPEND
Append data to a file.

**Usage:** `append <var> to <filename_var>`


### ASSERT
Test is a condition is true.

**Usage:** `assert (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ...`

**Example:** `assert regex_var matches text_var and var1 in list`

Note that `!` is used to express negation and `rin` is a Regex-based `in`. A regexly-in operator ;)


### BRANCH
Branch a subtask. The syntax is similar to the one to spawn processes, i.e., a string of words. The syntax supports variable interpolation.

**Usage:** `& <subtask> [<argument> ...]`

**Example:** `& subtask1 name="John Doe" age=42 city={city}`

> In this example, the `city` variable will be automatically shell-escaped during its interpolation.


### BREAK
Break a loop.

**Usage:** `break`

### BROWSE
Loop construct to browse a directory.

**Usage:** `browse [files] [and] [dirs] in <dirname_var>`

**Example:**
```
[task]
browse files and dirs in dirname
    : Root -> {R}
    for item in files
        : {item}
    for item in dirs
        : {item}
        
browse files in dirname
    pass
    
browse dirs in dirname
    pass
```

### CALL
Call a **Python** function from **Backstage** with arguments, then get the return !

**Usage:** `call <module>.<function>[(<argument_var>, ...)]`

**Example:** 
```
[task]
# interface with the Python module
interface with package.coffee_module alias coffeemaker

# call the 'make' function with arguments then get the return
call coffeemaker.make(sugar_cube, extra, 42)
: Result -> {R}
```

### CD
Change directory.

**Usage:** `cd <dirname_var>`


### CHECK
Return the data type (`str`, `list`, `dict`, `int`, `float`) of a variable if it exists, else return an empty string.

**Usage:** `check <var>`

**Example:**
```
[task]
check myvar
if R == EMPTY
    : This variable doesn't exist at all !
else
    : 'myvar' exists, its data type is {R}
```

### CLEAR
Clear the content of a variable or a list of variables.

**Usage:** `clear <var> ...`

**Example:** `clear var1 var2 var3`

### COMMENT
Comment.

**Usage:** `# <comment>`


### CONFIG
Read and write configuration options (`FailFast`, `ReportException`, `ShowTraceback`, `TestMode`, `AutoLineBreak`).

**Usage:** `config <option> ...`

**Example:**
```
[task]
config FailFast=1 AutoLineBreak=0
config TestMode
if R == 1
    : Test Mode On
elif R == 0
    : Test Mode Off
```


### COPY
Copy a file or a directory tree to a new destination.

**Usage:** `copy <src_path_var> to <dest_path_var>`

### COUNT
Count `chars`, `items`, and `lines` in the content of a variable or inside a file (if the `(file)` tag is applied).

**Usage:** `count (chars|items|lines) in (<var>|<filename_var>) [(file)]`

**Example:**
```
[task]
set path = /home/alex/iliad.txt
count chars in path (file)
if R == 0
    : The file is empty !
```

### CREATE
Create a new file or directory.

**Usage:** `create (dir|file) <path_var>`

### DEFAULT
Define an empty variable (or a bunch of variables) if it doesn't exist yet in the namespace.

**Usage:** `default <var> ...`

**Example:**

```
[task]
# default two variables in the Local namespace
default var1 L:var2

# default one variable in the Database namespace
default D:name

# from now, 'D:name' can be safely accessed
# even though the 'database.json' file supposed
# to contain the 'name' value was inadvertently deleted.
```

### DROP
Destroy a variable (or a bunch of variables). 

**Usage:** `drop <var> ...`

### ELIF
Part of the `if` conditional construct.

**Usage:** `elif (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ...`

### ELSE
Part of the `if` conditional construct.

**Usage:** `else`

### ENTER
Invite user to submit data.

**Usage:** `> [<var> [: <text>]]`

**Example:**
```
[task]

> name : Please enter your name 
# have you spotted the space at the end the line above ?

# the same line can be rewritten like this:
> name : `Please enter your name `
# backticks serve as delimiters that will be ignored

# this one is also possible:
set msg = `Please enter your name `
> name : {msg}

# even this:
set info (dict) = name="John Doe" age=42
> info.name : `Please enter your name`
```

### EXIT
Exit.

**Usage:** `exit`

### EXPOSE
Copy a variable (or a bunch of variables) into the **Global** namespace.

**Usage:** `expose <var> ...`

### FAIL
Deliberately fail. It breaks the running task and mark it as a failure.

**Usage:** `fail`

### FIND
Find files and or directories paths.

**Usage 1:** `find [all] (paths|files|dirs) in <dirname_var>`

**Usage 2:** `find ... matching <regex_var>`

**Usage 3:** `find ... [and] (accessed|modified|created) (at|after|before|between) <timestamp_var> [and <timestamp_var>]`

**Example:** `find files in dirname matching regex and accessed between timestamp1 and timestamp2`

### FOR
A `for` loop to iterate the content of a variable or the content of a file (if you apply the `(file)` tag).

**Usage:** `for (char|item|line) in (<var>|<filename_var>) [(file)]`

**Example:**
```
[task]
# this code iterates over each character of the Iliad,
# and outputs it as it,
# with one twist: each line starts with its index (0-based)

set path = `/home/alex/iliad.txt`

# the print statement (:) won't anymore
# automatically add a line break !
config AutoLineBreak=0

for line in path (file)
    : `{N} `
    for char in line
        : {char}
    : \n
```


### FROM
A loop to go from an integer to another one. If the `start` integer is superior to the `end` integer, the count will decrease.

**Usage:** `from <start> to <end>`

**Example:**
```
[task]
from 10 to 0
    # here, N will go from 0 to 10
    # but R will go from 10 to 0
    # because N is a counter for all loops
    # while R is a cache for whatever is returned
    # by a command, a statement, or a construct
    : {N}\t{R}

# As you can see, I can add a Tab \t since
# Backstage supports natively here document ;)

# To get a simple backslash followed by a 't':  \\t
```

### GET
Get a `char`, an `item`, or a `line` at index `x` (including negative index) from a target. The target can be the content of a variable or a file (if you apply the `(file)` tag).

**Usage:** `get (char|item|line) <index> from (<var>|<filename_var>) [(file)]`

### IF
Conditional construct.

**Usage:** `if (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ...`

**Example:**
```
[task]
default var1 var2 var3 var4
if var1 == var2 or var3 == var4
    pass
elif EMPTY == EMPTY
    pass
else
    pass
```

### INTERFACE
Interface with a **Python** module.

**Usage:** `interface with [<package>.]<module> [alias <name>]`

**Example:** 

```
[task]
interface with package.mymodule alias module
default var1 var2
call module.function(var1, var2)
```

### LINE
Draw a line.

**Usage:** `(=|-) ...`

**Example:** `----------` or `==========`


### MOVE
Move a file or a directory tree to a new destination.

**Usage:** `move <src_path_var> to <dest_path_var>`

### PASS
Placeholder for the code that you might write in the future. This statement does nothing. It is the same as the eponymous one in **Python**.

**Usage:** `pass`

### POKE
Poke a file or directory to get access to a `dict` of properties if this path exists. Available properties: `size` `mtime` `ctime` `atime` `nlink` `uid` `gid` `mode` `ino` `dev`.

**Usage:** `poke <path_var>`

**Example:**
```
[task]
set path = /home/alex/iliad.txt
poke path
if R == EMPTY
    : Oops ! This file doesn't exist
else
    : File size -> {R.size}
```

### PREPEND
Prepend data to a file

**Usage:** `prepend <var> to <filename_var>`

### PRINT
Print data. You can use backquotes as delimiters. This statement supports variable interpolation.

**Usage:** `: <text>`

**Example:**
```
[task]
:  Hello World ! 
# Have you spotted the two extra spaces characters ?

: ` Hello World ! `
# hehehe, got you ! ;)
```

### PUSH
Push variables into the input of the next spawned process.

**Usage:** `push <var> ...`

### READ
Read all or a specific line index (including negative index) from a file.

**Usage:** `read (*|<index>) from <filename_var>`

### REPLACE
Replace some pattern in a text with a replacement value.

**Usage:** `replace <regex_var> in <text_var> with <replacement_var>`

### RETURN
Return from a task with a value.
 
**Usage:** `return [<var>]`

### SET
Define a new variable or update the content of an existing variable. You don't can't specify a data type, but instead you can apply an assigment tag that is one of: `(raw)` `(str)` `(list)` `(dict)` `(int)` `(float)` `(date)` `(time)` `(dtime)` `(tstamp)`. Note that backquotes can be used as delimiters for the value (right side of the equal sign). These delimiters will be ignored. Backticks aren't quotes. This statement supports variable interpolation.

**Usage:** `set <var> [(raw)|(str)|(list)|(dict)|(int)|(float)|(date)|(time)|(dtime)|(tstamp))] = <value>`

**Example:** `set var (int) = 1 + 2`


### SLEEP
Sleep for `x` seconds.

**Usage:** `sleep <seconds>`

### SPAWN
Spawn a new process.

**Usage:** `$ <program> [<argument> ...]`

**Example:** `$ program1 arg {var} | program2 `

### SPLIT
Split with a regex pattern a text into a list.

**Usage:** `split <text_var> with <regex_var>`

### SPOT
Count the number of occurrences of a regex pattern inside a text.

**Usage:** `spot <regex_var> in <text_var>`

### STORE
Store a variable (or a bunch of variables) in the **Database** namespace. A stored variable can be accessed like this: `D:var`

**Usage:** `store <var> ...`

### THREAD
Branch a subtask... but in a new thread. 

**Usage:** `~ <subtask> [<argument> ...]`

### WHILE
The `while` loop. Use `break` to break it, and check `N` if you need a counter. 

**Usage:** `while (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ...`

### WRITE
Erase the content of a file to write some data inside.

**Usage:** `write <var> to <filename_var>`


# File and directory manipulation
Let's explore how file and directory manipulatin is performed with **Backstage**.

## Resource creation

Create a file:
```
[task]
# create a file
set path = /home/alex/iliad.txt
create file path
```

Create a directory:

```
[task]
# create a directory
set path = /home/alex/new/directory
create dir path
```

## File edition

```
[task]
set path = /home/alex/iliad.txt
set var = Hello World

# write data
write var to path

# append data to a file
append var to path

# prepend data to a file
prepend var to path
```

## Read the content of a file
```
[task]
set path = /home/alex/iliad.txt

# read all from 'iliad.txt'
read * from path
: {R}

# read the line at index 3
set index (int) = 1 + 1 + 1
read index from path
: {R}

# just want to read the last line ?
read -1 from path 
: {R}
```

## Iterating the content of a file
```
[task]
set path = /home/alex/iliad.txt

# iterate over the characters in a file
for char in path (file)
    : Character -> char

# iterate over the lines in a file
for line in path (file)
    : {line}
```

## Browse a folder

```
[task]
set folder = /home/alex

browse files and dirs in folder
    : Directory -> {R}
    for item in files
        : {item}
    for item in dirs
        : {item}
```

## Find resources
The `find` statement is like Glob but on steroid:
```
[task]
set folder = /home/alex
set regex (raw) = `[\S\s]*?`
set timestamp1 = 1223322233

find files in folder matching regex and accessed between timestamp1 and NOW
: Results -> {R}

```

## Read resource properties
You can get from **Backstage** the properties of an arbitrary resource, like its size:

```
[task]
set path = /home/alex/iliad.txt

# poke a file
poke path
: Creation timestamp -> {R.ctime}
: Size -> {R.size}

```


# Interfacing with Python
Interfacing with **Python** is as simple as this:
```
[task]
interface with python.module as my_module
set name = `John Doe`
set age (int) = 40 + 2
call my_module.function(name, age)
: Return -> {R}
```

> **Allowed return data types:** `str`, `list` (one-dimensional),`tuple` (one-dimensional), `dict` (one-dimensional), `int`, and `float`. **Python** functions can also return `True`, `False`, and `None`, which will be converted to **1**, **0** and an **empty string**, respectively.

# Exception handling and tests
Whenever an exception is raised, the variables `EXCEPTION` and `TRACEBACK` are updated and **Backstage** continues calmly its execution.

Note that the variables `TRACEBACK` and `EXCEPTION` are cleared after the next successful command.

If you want the execution to stop whenever an exception is raised, just set `1` to the `FailFast` configuration option.

```
[task]
config FailFast=1
```

If you want to read a report of an exception when it's raised, just set `1` to the `ReportException` configuration option.

```
[task]
config ReportException=1
```

If you want to read the verbose [traceback](https://en.wikipedia.org/wiki/Stack_trace#Python) of an exception when it's raised, just set `1` to the `ShowTraceback` configuration option.

```
[task]
config ShowTraceback=1
```

You can edit these configuration options in the same command:

```
[task]
config FailFast=1 ReportException=1 ShowTraceback=0
```
You can read the current value of an arbitrary configuration option:

```
[task]
config FailFast
: FailFast -> {R}
```



## Tests
To create a test, just postfix `.test` to the name of a task. Then from the command line, just run the test `backstage --check task`.

### Example
```
[task]
set val (int) = {ARGS[0]} + {ARGS[1]}
return val

[task.test]
# here we branch the task with the arguments 40 and 2
& task 40 2
# we expect 42 as return 
assert R == 42
```

# Command line interface and developer experience

```bash
$ backstage --help
Welcome to Pyrustic Backstage !
Ultimate task automation tool for hackers.

Usage:
    backstage
    backstage <task> [<argument> ...]
    backstage <option> [<argument> ...]
    
Options:
    -i, --intro                 Show file introductory text
    -t, --tasks                 Show the list of tasks
    -T, --Tasks                 Show the descriptive list of tasks
    -d, --doc <task>            Show documentation for a specific task
    -c, --check [<task> ...]    Run tests
    -C, --Check [<task> ...]    Run tests in debug mode
    -s, --search <task>         Search for a task by its name
    -S, --Search <task>         Search for a task by keyword
    -h, --help                  Show this information page

    The <task> string can use a glob-like syntax that allows 
    wildcards '*' and '?'. Therefore, 'task1' is identical to 'task*'.
    
Visit the webpage: https://github.com/pyrustic/backstage
```

## Developer experience
**Backstage** will do its best to help you understand raised exceptions:

```bash
$ backstage task1
ZeroDivisionError at line 3 of [task1] !
division by zero

$ backstage task2
InterpretationError at line 7 of [task2] !
Usage: sleep <seconds>
```

When you run **Backstage** in the loop mode, you can enjoy the autocomplete functionality (use the Tab key to complete your input) and also the history functionality (use Up and Down arrows).

```bash
$ backstage
Welcome to Pyrustic Backstage !
Ultimate task automation tool for hackers.
Press 'Ctrl-c' or 'Ctrl-d' to quit.
Type '--help' or '-h' to show more information.

(backstage) task(Tab Tab)
task    task1   task2   task3

(backstage) --h(Tab)

...

```

# Miscellaneous
In the following subsections, we will explore some miscellaneous information.

## Dogfooding
**Backstage** itself as a project relies on a `backstage.tasks` file (check the root of this repository). You are reading a document about **Backstage** that has been updated with **Backstage** !

## Dependencies
**Backstage** relies on these **Python** packages:
- [Subrun](https://github.com/pyrustic/subrun) to spawn new processes;
- [Shared](https://github.com/pyrustic/shared) to store data;
- [Jesth](https://github.com/pyrustic/jesth) to parse `backstage.tasks` files;
- [Oscan](https://github.com/pyrustic/jesth) to extract tokens from the script.

## Indentation
Four (4) spaces by [indent](https://en.wikipedia.org/wiki/Indentation_(typesetting)#Indentation_in_programming). Period.

## Python 3
Inside the script file, you don't have to type `python3` in a command to spawn the **Python** interpreter. Just type `python` to spawn the same interpreter that is running **Backstage**:
```
[task]
$ python -m my.package.module
```

## Data cache
**Backstage** stores data in an automatically created directory `.backstage` located in the current working directory. Inside this directory you can find the `execution.log` and `database.json` files.

## Automatic line break
If you don't want anymore an extra line break at the end of printed strings, you can turn off this functionality:

```
[task]
# turn off auto line break
config AutoLineBreak=0
: `Hello `
: `World`
# turn on auto line break
config AutoLineBreak=1
: Hello World
```


## Lines
You can draw lines with the characters `=` or `-`. If you pick one, only this one is allowed to appear on the same line.
```
[task1]

$ program1
$ program2

-----------------

[task2]
pass

=================
```


# Demo
The demo is a [repository](https://github.com/pyrustic/project) that contains a [backstage.tasks](https://github.com/pyrustic/project/blob/master/backstage.tasks#L1) file similar to the one used to build, package and publish my projects. Your mission, if you accept it, is to clone the demo repository and run the `backstage.tasks` which contains tasks to create a new **Python** `Hello Friend !` project, build it, perform versioning, init **Git** , perform **Git** Commit and **Git** Push, and even push the latest built package to [PyPI](https://pypi.org) !

```bash
# 1- clone the repository
$ git clone https://github.com/pyrustic/project
$ cd project

# 2- install backstage
$ pip install backstage

# 3- install buildver
$ pip install buildver

# 4- install setupinit
$ pip install setupinit

# 5- list the tasks available in the `backstage.tasks` file
$ backstage -t
Available tasks (11):
    build  check  clean  gendoc  gitcommit  gitinit  gitpush  init
    release  test  upload2pypi

# 6- descriptive list of tasks
$ backstage -T

# 7- initialize the project
$ backstage init
Successfully initialized !

# 8- run the project
$ python3 -m project
Hello Friend !

# 9- build the project
$ backstage build
building v0.0.1 ...
Successfully built 'project' v0.0.1 !
VERSION file updated from 0.0.1 to 0.0.2

# 10- check the project
$ backstage check
project v0.0.2 (source)
.whl v0.0.1 (package) built 28 secs ago

# 11- initialize Git
$ backstage gitinit
Origin: https://github.com/pyrustic/project.git

# 12- perform a Git Commit
$ backstage gitcommit

# 13- perform a Git Push
$ backstage gitpush

# 14- upload to PyPI
$ backstage upload2pypi
```

> **Note:** Commands `9`, `12`, `13`, and `14` can be replaced with one command: `backstage release`



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
