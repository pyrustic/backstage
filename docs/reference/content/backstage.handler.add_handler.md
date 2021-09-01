
Back to [Reference Overview](https://github.com/pyrustic/backstage/blob/master/docs/reference/README.md#readme)

# backstage.handler.add\_handler



<br>


```python

class AddHandler:
    """
    Description
    -----------
    Use this command to add an empty file, a package or a regular
    folder to the Target.
    
    Usage
    -----
    - Description: Add a package
    - Command: add <my.pack.age>
    
    - Description: Add a module
    - Command: add <destination> <file.py>
    
    - Description: Add multiple files
    - Command: add <destination> <file_1.ext> <file_2.ext>
    
    - Description: Add a file to the Target's APP_DIR
    - Command: add ./ <file.ext>
    
    Note: The destination is either a relative path to the
    Target's PROJECT_DIR, or a package name.
    
    Example
    -------
    - Description: Add a module
    - Preliminary: Assume you want to add "my_view.py"
    to the package 'demo.view'
    - Command: add demo.view my_view.py
    
    - Description: Add a package
    - Preliminary: Assume you want to add 'my.new.package'
    - Command: add my.new.package
    
    Note: Please use simple or double quotes as delimiters if a
    string contains space.
    """

    def __init__(self, target, app_pkg, *args):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

