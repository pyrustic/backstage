Back to [Modules overview](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md)
  
# Module documentation
>## backstage.core.dist
Project Backstage API
<br>
[functions (3)](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.dist/functions.md)


## Functions
```python
def dist_info(name):
    """
    Use this function to get some info about an installed
    distribution package
    
    Parameters:
        name: the distribution name, example: "wheel", "cyberpunk-theme"
    
    Returns: A dict with these keys:
        name, description, home_page, version,
        author, author_email, maintainer, maintainer_email.
    
    Note: All values in the returned dict are strings.
    """

```

```python
def dist_version(name):
    """
    Returns the version of the installed distribution package,
    otherwise returns None.
    """

```

```python
def get_setup_config(project_dir):
    """
    
    """

```

