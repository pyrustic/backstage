Back to [All Modules](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md#readme)

# Module Overview

**backstage**
 
Project Backstage API

> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [\_join\_command](#_join_command) &nbsp;&nbsp; [create\_tasks\_file](#create_tasks_file) &nbsp;&nbsp; [get\_default\_tasks](#get_default_tasks) &nbsp;&nbsp; [get\_tasks](#get_tasks) &nbsp;&nbsp; [run](#run)
>
> **Constants:** &nbsp; BACKSTAGE_HOME &nbsp;&nbsp; PYRUSTIC_HOME

# All Functions
[\_join\_command](#_join_command) &nbsp;&nbsp; [create\_tasks\_file](#create_tasks_file) &nbsp;&nbsp; [get\_default\_tasks](#get_default_tasks) &nbsp;&nbsp; [get\_tasks](#get_tasks) &nbsp;&nbsp; [run](#run)

## \_join\_command
None



**Signature:** (command, extra\_args)





**Return Value:** None.

[Back to Top](#module-overview)


## create\_tasks\_file
Create a tasks-file in the project directory.




**Signature:** (source, project\_dir=None, override=False)

|Parameter|Description|
|---|---|
|source|a hackernote structure or a text string that will be saved in 'backstage.tasks'|
|project\_dir|path, the project_dir|
|override|boolean, override the current tasks-file if it exists |





**Return Value:** ['Returns True or False']

[Back to Top](#module-overview)


## get\_default\_tasks
Returns a hackernote structure that represents the default tasks Python-compatible.
Note that the bodies of sections are strings, i.e., each value in this dict is a string.



**Signature:** ()





**Return Value:** None.

[Back to Top](#module-overview)


## get\_tasks
Get a dictionary of available tasks in the tasks file in this project_dir




**Signature:** (project\_dir=None)

|Parameter|Description|
|---|---|
|project\_dir|string, path of the project_dir |



|Exception|Description|
|---|---|
|error.NoTasksFileError|raised when the tasks file is missing |



**Return Value:** ['A dictionary of tasks. Each key is a task name, each value is a list of commands strings.', 'Example: {"init": ["do this", "do that"], "build": ["do this", "command 2"]}']

[Back to Top](#module-overview)


## run
Run one or multiple commands with extra arguments




**Signature:** (\*commands, extra\_args=None, project\_dir=None)

|Parameter|Description|
|---|---|
|\*commands|a command string or multiple commands strings that will be run with the library 'subrun'|
|extra\_args|a list of extra arguments to append to the first command only|
|project\_dir|the path string |





**Return Value:** ['Nothing']

[Back to Top](#module-overview)


