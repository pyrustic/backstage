Back to [Modules overview](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md)
  
# Module documentation
>## backstage.core.pymisc
No description
<br>
[functions (8)](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.pymisc/functions.md)


## Functions
```python
def convert_dotted_path(root, dotted_path, prefix='', suffix=''):
    """
    
    """

```

```python
def convert_size(size):
    """
    Size should be in bytes.
    Return a tuple (float_or_int_val, str_unit) 
    """

```

```python
def edit_build_version(app_dir):
    """
    
    """

```

```python
def make_archive(name, src, dest, format='zip'):
    """
    - name is the zipfile name minus extension like 'my_archive_file';
    - src is the root dir of the project to zip like '/path/to/project';
    - dest is the dir where to save the final zip.
    Dest should exist like '/path/to/dest'
    format is "zip" or "tar" or "gztar" or "bztar" or “xztar”. Default to "zip"
    
    Returns the zipfile path and error. Zipfile could be None or str.
    error could be None or an exception instance
    """

```

```python
def parse_cmd(cmd):
    """
    Split the cmd string. Delimiters are: space, simple and double quotes
    """

```

```python
def script(cmd, cwd=None, interactive=True, python=False):
    """
    Execute a cmd. Cmd is either a list of args or a string.
    Example of commands:
        - "something 'path/to/dir'"
        - ["something", "path/to/dir"]
    """

```

```python
def tab_to_space(text, tab_size=4):
    """
    
    """

```

```python
def truncate_str(data, max_size=15, ellipsis='...'):
    """
    
    """

```

