Back to [All Modules](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md#readme)

# Module Overview

> **backstage.core.versioning**
> 
> No description
>
> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [get\_version](#get_version) &nbsp; [interpret\_version](#interpret_version) &nbsp; [set\_version](#set_version)
>
> **Constants:** &nbsp; None

# All Functions
[get\_version](#get_version) &nbsp; [interpret\_version](#interpret_version) &nbsp; [set\_version](#set_version)

## get\_version
This function read the VERSION file in the project_dir project
then returns the version (str) of the project.

Parameters:
     - project_dir: str, path to the project_dir project

Returns: str, version extracted from $PROJECT_DIR/VERSION or None



**Signature:** (project\_dir)



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


