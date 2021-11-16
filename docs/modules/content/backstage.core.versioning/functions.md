Back to [Modules overview](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md)
  
# Module documentation
>## backstage.core.versioning
No description
<br>
[functions (3)](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.versioning/functions.md)


## Functions
```python
def get_version(project_dir):
    """
    This function read the VERSION file in the project_dir project
    then returns the version (str) of the project.
    
    Parameters:
         - project_dir: str, path to the project_dir project
    
    Returns: str, version extracted from $PROJECT_DIR/VERSION or None
    """

```

```python
def interpret_version(cur_version, new_version):
    """
    This function interprets the command to set a new version.
    
    Parameters:
        - cur_version: str, the current version, the one to alter.
        - new_version: str, the command to set a new version.
    
    A command can be an actual new version string, or one of the keywords:
     - "maj": to increment the major number of the current version,
     - "min": to increment the minor number of the current version,
     - "rev": to increment the revision number of the current version.
    
    Returns: The new version as it should be saved in version.py
    """

```

```python
def set_version(project_dir, version):
    """
    This function edits the content of $PROJECT_DIR/VERSION
    
    Parameters:
         - project_dir: str, path to the project_dir project
         - version: str, the version
    
    Returns:
        - bool, False, if the module version.py is missing
        - bool, True if all right
    """

```

