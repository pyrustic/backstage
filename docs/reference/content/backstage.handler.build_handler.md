
Back to [Reference Overview](https://github.com/pyrustic/backstage/blob/master/docs/reference/README.md#readme)

# backstage.handler.build\_handler



<br>


```python

class BuildHandler:
    """
    Description
    -----------
    Use this command to build a distribution package
    that could be published later with the 'publish'
    command.
    The distribution package is a Wheel.
    
    Usage
    -----
    - Description: Build
    - Command: build
    
    Hooking
    -------
    This command will run hooks if they exist.
    The legal hooks are:
    - pre_building_hook.py
    - post_building_hook.py
    """

    def __init__(self, target, app_pkg, *args):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

