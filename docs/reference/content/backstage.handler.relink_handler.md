
Back to [Reference Overview](https://github.com/pyrustic/backstage/blob/master/docs/reference/README.md#readme)

# backstage.handler.relink\_handler



<br>


```python

class RelinkHandler:
    """
    Description
    -----------
    Link again the previously linked Target or one of
    recent linked Targets.
    
    Usage
    -----
    - Description: Link again the previously linked Target
    - Command: relink
    
    - Description: Link again a recently linked Target with
    its index
    - Command: relink <index>
    
    Example
    -------
    - Description: Link again a previously linked Target
    - Preliminary: Assume you want to link again the Target
    with index #2 (found the index with the command "recent")
    - Command: relink 2
    """

    def __init__(self, target, app_pkg, *args):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

    @property
    def target(self):
        """
        
        """

```

