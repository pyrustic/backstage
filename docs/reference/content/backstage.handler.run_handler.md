
Back to [Reference Overview](https://github.com/pyrustic/backstage/blob/master/docs/reference/README.md#readme)

# backstage.handler.run\_handler



<br>


```python

class RunHandler:
    """
    Description
    -----------
    Use this command to run a module.
    The module can be located either in the Target or in
    a regular place where Python stores packages.
    Only dotted name of a module is allowed, so please ignore
    the extension ".py".
    
    Usage
    -----
    - Description: Run a module
    - Command: run <the.module.name>
    
    - Description: Run the Target
    - Command: run
    Note: Project Manager will implicitly run APP_DIR/__main__.py
    
    - Description: Run a module with some arguments
    - Command: run <the.module.name> <argument_1> <argument_2>
    
    Example
    -------
    - Description: Run the module
    - Preliminary: Assume that "my_view.py" is in the "view" package
    - Command: run view.my_view
    
    - Description: Run the module with arguments
    - Preliminary: Assume that "my_view.py" is in the "view" package
    - Command: run view.my_view argument_1 "argument 2"
    
    - Description: Display the Zen of Python
    - Command: run this
    
    Note: Please use simple or double quotes as delimiters if a string
    contains space.
    """

    def __init__(self, target, app_pkg, *args):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

