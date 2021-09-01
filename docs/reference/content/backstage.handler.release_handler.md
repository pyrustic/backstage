
Back to [Reference Overview](https://github.com/pyrustic/backstage/blob/master/docs/reference/README.md#readme)

# backstage.handler.release\_handler



<br>


```python

class ReleaseHandler:
    """
    Description
    -----------
    Use this command to publish the latest distribution
    package previously built with the command 'build'.
    
    Usage
    -----
    - Description: Publish
    - Command: publish
    
    Hooking
    -------
    This command will run hooks if they exist.
    The legal hooks are:
    - pre_publishing_hook.py
    - post_publishing_hook.py
    """

    def __init__(self, target, app_pkg, *args):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

