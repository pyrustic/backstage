
Back to [Reference Overview](https://github.com/pyrustic/backstage/blob/master/docs/reference/README.md#readme)

# backstage.handler.version\_handler



<br>


```python

class VersionHandler:
    """
    Description
    -----------
    Use this command to check or edit the version of the
    Target project.
    
    Usage
    -----
    - Description: Check the current version
    - Command: version
    
    - Description: Set a new version
    - Command: version <sequence>
    
    - Description: Increment the major number
    - Command: version maj
    
    - Description: Increment the minor number
    - Command: version min
    
    - Description: Increment the revision number
    - Command: version rev
    
    Example
    -------
    - Description: Increment the major number
    - Preliminary: Assume the current version 1.2.3
    - Command: version maj
    - Result: The new version is: 2.0.0
    
    - Description: Set a version
    - Command: version 2.0.1
    """

    def __init__(self, target, app_pkg, *args):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

