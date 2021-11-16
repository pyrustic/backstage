Back to [Modules overview](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md)
  
# Module documentation
>## backstage.core.lite\_test\_runner
No description
<br>
[functions (1)](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.lite_test_runner/functions.md) &nbsp;.&nbsp; [classes (2)](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.lite_test_runner/classes.md)


## Functions
```python
def run_tests(project_dir):
    """
    Runs the tests in the project_dir.
    
    Parameters:
        - project_dir: str, path to the project_dir project
    
    Returns: a tuple (bool, object). The bool indicate the success
    (True) or the failure (False) of the tests.
    The second item in the tuple can be None, an Exception instance, or a string.
    
    Note: the tests should be located at $PROJECT_DIR/tests
    """

```

