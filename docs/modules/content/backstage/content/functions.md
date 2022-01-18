Back to [All Modules](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md#readme)

# Module Overview

> **backstage**
> 
> Project Backstage API
>
> **Classes:** &nbsp; [Error](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage/content/classes/Error.md#class-error) &nbsp; [NoTasksFileError](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage/content/classes/NoTasksFileError.md#class-notasksfileerror)
>
> **Functions:** &nbsp; [backstage\_setup](#backstage_setup) &nbsp; [dist\_info](#dist_info) &nbsp; [dist\_version](#dist_version) &nbsp; [get\_app\_pkg](#get_app_pkg) &nbsp; [get\_project\_name](#get_project_name) &nbsp; [get\_setup\_config](#get_setup_config) &nbsp; [get\_tasks](#get_tasks) &nbsp; [get\_version](#get_version) &nbsp; [initialized](#initialized) &nbsp; [interpret\_version](#interpret_version) &nbsp; [run](#run) &nbsp; [run\_tests](#run_tests) &nbsp; [set\_version](#set_version)
>
> **Constants:** &nbsp; constant

# All Functions
[backstage\_setup](#backstage_setup) &nbsp; [dist\_info](#dist_info) &nbsp; [dist\_version](#dist_version) &nbsp; [get\_app\_pkg](#get_app_pkg) &nbsp; [get\_project\_name](#get_project_name) &nbsp; [get\_setup\_config](#get_setup_config) &nbsp; [get\_tasks](#get_tasks) &nbsp; [get\_version](#get_version) &nbsp; [initialized](#initialized) &nbsp; [interpret\_version](#interpret_version) &nbsp; [run](#run) &nbsp; [run\_tests](#run_tests) &nbsp; [set\_version](#set_version)

## backstage\_setup
This function does this:
- create user.json in data dir
- fill the config directory



**Signature:** ()



**Return Value:** None

[Back to Top](#module-overview)


## dist\_info
Use this function to get some info about an installed
distribution package

Parameters:
    name: the distribution name, example: "wheel", "cyberpunk-theme"

Returns: A dict with these keys:
    name, description, home_page, version,
    author, author_email, maintainer, maintainer_email.

Note: All values in the returned dict are strings.



**Signature:** (name)



**Return Value:** None

[Back to Top](#module-overview)


## dist\_version
Returns the version of the installed distribution package,
otherwise returns None.



**Signature:** (name)



**Return Value:** None

[Back to Top](#module-overview)


## get\_app\_pkg
This function extracts the application package name from a project_dir path.
Basically it extracts the basename from the path then turns dashes "-" into
"underscores" "_".

Parameters:
    - project_dir: str, path to the project_dir project

Returns: str, the application package name.



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## get\_project\_name
Returns the project name



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## get\_setup\_config
No description



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## get\_tasks
No description



**Signature:** (project\_dir=None)



**Return Value:** None

[Back to Top](#module-overview)


## get\_version
This function read the VERSION file in the project_dir project
then returns the version (str) of the project.

Parameters:
     - project_dir: str, path to the project_dir project

Returns: str, version extracted from $PROJECT_DIR/VERSION or None



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## initialized
Returns True if the project_dir is initialized, else returns False



**Signature:** (project\_dir, app\_pkg=None)



**Return Value:** None

[Back to Top](#module-overview)


## interpret\_version
This function interprets the command to set a new version.

Parameters:
    - cur_version: str, the current version, the one to alter.
    - new_version: str, the command to set a new version.

A command can be an actual new version string, or one of the keywords:
 - "maj": to increment the major number of the current version,
 - "min": to increment the minor number of the current version,
 - "rev": to increment the revision number of the current version.

Returns: The new version as it should be saved in version.py



**Signature:** (cur\_version, new\_version)



**Return Value:** None

[Back to Top](#module-overview)


## run
No description



**Signature:** (\*commands, extra\_args=None, project\_dir=None)



**Return Value:** None

[Back to Top](#module-overview)


## run\_tests
Runs the tests in the project_dir.

Parameters:
    - project_dir: str, path to the project_dir project

Returns: a tuple (bool, object). The bool indicate the success
(True) or the failure (False) of the tests.
The second item in the tuple can be None, an Exception instance, or a string.

Note: the tests should be located at $PROJECT_DIR/tests



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## set\_version
This function edits the content of $PROJECT_DIR/VERSION

Parameters:
     - project_dir: str, path to the project_dir project
     - version: str, the version

Returns:
    - bool, False, if the module version.py is missing
    - bool, True if all right



**Signature:** (project\_dir, version)



**Return Value:** None

[Back to Top](#module-overview)


