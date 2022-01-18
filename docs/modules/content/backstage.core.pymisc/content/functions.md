Back to [All Modules](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md#readme)

# Module Overview

> **backstage.core.pymisc**
> 
> No description
>
> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [convert\_dotted\_path](#convert_dotted_path) &nbsp; [convert\_size](#convert_size) &nbsp; [edit\_build\_version](#edit_build_version) &nbsp; [make\_archive](#make_archive) &nbsp; [parse\_cmd](#parse_cmd) &nbsp; [script](#script) &nbsp; [tab\_to\_space](#tab_to_space) &nbsp; [truncate\_str](#truncate_str)
>
> **Constants:** &nbsp; None

# All Functions
[convert\_dotted\_path](#convert_dotted_path) &nbsp; [convert\_size](#convert_size) &nbsp; [edit\_build\_version](#edit_build_version) &nbsp; [make\_archive](#make_archive) &nbsp; [parse\_cmd](#parse_cmd) &nbsp; [script](#script) &nbsp; [tab\_to\_space](#tab_to_space) &nbsp; [truncate\_str](#truncate_str)

## convert\_dotted\_path
No description



**Signature:** (root, dotted\_path, prefix='', suffix='')



**Return Value:** None

[Back to Top](#module-overview)


## convert\_size
Size should be in bytes.
Return a tuple (float_or_int_val, str_unit) 



**Signature:** (size)



**Return Value:** None

[Back to Top](#module-overview)


## edit\_build\_version
No description



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## make\_archive
- name is the zipfile name minus extension like 'my_archive_file';
- src is the root dir of the project to zip like '/path/to/project';
- dest is the dir where to save the final zip.
Dest should exist like '/path/to/dest'
format is "zip" or "tar" or "gztar" or "bztar" or “xztar”. Default to "zip"

Returns the zipfile path and error. Zipfile could be None or str.
error could be None or an exception instance



**Signature:** (name, src, dest, format='zip')



**Return Value:** None

[Back to Top](#module-overview)


## parse\_cmd
Split the cmd string. Delimiters are: space, simple and double quotes



**Signature:** (cmd)



**Return Value:** None

[Back to Top](#module-overview)


## script
Execute a cmd. Cmd is either a list of args or a string.
Example of commands:
    - "something 'path/to/dir'"
    - ["something", "path/to/dir"]



**Signature:** (cmd, cwd=None, interactive=True, python=False)



**Return Value:** None

[Back to Top](#module-overview)


## tab\_to\_space
No description



**Signature:** (text, tab\_size=4)



**Return Value:** None

[Back to Top](#module-overview)


## truncate\_str
No description



**Signature:** (data, max\_size=15, ellipsis='...')



**Return Value:** None

[Back to Top](#module-overview)


