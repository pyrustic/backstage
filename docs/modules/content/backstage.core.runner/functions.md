Back to [Modules overview](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md)
  
# Module documentation
>## backstage.core.runner
No description
<br>
[functions (1)](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.runner/functions.md)


## Functions
```python
def run(cmd, cwd=None, python=True, interactive=True):
    """
    Execute a cmd. Cmd is either a list of args or a string.
    Example of commands:
        - "something 'path/to/dir'"
        - ["something", "path/to/dir"]
    
    Returns: This function returns the exit code.
    
    Exception:
        - MissingSysExecutableError: raised when sys.executable is missing.
    
    Note: this function will block the execution of the thread in
    which it is called till the subprocess returns.
    """

```

