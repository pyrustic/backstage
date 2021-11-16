Back to [Modules overview](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md)
  
# Module documentation
>## backstage.core.funcs
No description
<br>
[functions (14)](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.funcs/functions.md)


## Functions
```python
def ask_for_confirmation(message, default='y'):
    """
    Use this function to request a confirmation from the user.
    
    Parameters:
        - message: str, the message to display
        - default: str, either "y" or "n" to tell "Yes by default"
        or "No, by default".
    
    Returns: a boolean, True or False to reply to the request.
    
    Note: this function will append a " (y/N): " or " (Y/n): " to the message.
    """

```

```python
def build_package(target, package_name, prefix=''):
    """
    Literally build a package, returns None or the string pathname
    package represented by prefix must already exist
    """

```

```python
def copyto(src, dest):
    """
    Please make sure that DEST doesn't exist yet !
    Copy a file or contents of directory (src) to a destination file or folder (dest)
    """

```

```python
def create_kurl():
    """
    
    """

```

```python
def get_app_pkg(project_dir):
    """
    This function extracts the application package name from a project_dir path.
    Basically it extracts the basename from the path then turns dashes "-" into
    "underscores" "_".
    
    Parameters:
        - project_dir: str, path to the project_dir project
    
    Returns: str, the application package name.
    """

```

```python
def get_hub_url(res):
    """
    
    """

```

```python
def get_project_name(project_dir):
    """
    Returns the project name
    """

```

```python
def get_root_from_package(package_name):
    """
    Return the root from a dotted package name.
    Example the root here "my.package.is.great" is "my".
    """

```

```python
def module_name_to_class(module_name):
    """
    Convert a module name like my_module.py to a class name like MyModule
    """

```

```python
def moveto(src, dest):
    """
    If the DEST exists:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        - /home/ocean (DEST)
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/lake
        - /home/ocean/lake/fish.txt
    Else IF the DEST doesn't exist:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/fish.txt
    
    
    Move a file or directory (src) to a destination folder (dest)
    """

```

```python
def package_name_to_path(target, package_name, prefix=''):
    """
    
    """

```

```python
def strictly_capitalize(string):
    """
    
    """

```

```python
def wheels_assets(target):
    """
    
    """

```

