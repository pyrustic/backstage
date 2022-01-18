Back to [All Modules](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md#readme)

# Module Overview

> **backstage.core.dist**
> 
> Project Backstage API
>
> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [dist\_info](#dist_info) &nbsp; [dist\_version](#dist_version) &nbsp; [get\_setup\_config](#get_setup_config)
>
> **Constants:** &nbsp; None

# All Functions
[dist\_info](#dist_info) &nbsp; [dist\_version](#dist_version) &nbsp; [get\_setup\_config](#get_setup_config)

## dist\_info
Use this function to get some info about an installed
distribution package

Parameters:
    name: the distribution name, example: "wheel", "cyberpunk-theme"

Returns: A dict with these keys:
    name, description, home_page, version,
    author, author_email, maintainer, maintainer_email.

Note: All values in the returned dict are strings.



**Signature:** (name)



**Return Value:** None

[Back to Top](#module-overview)


## dist\_version
Returns the version of the installed distribution package,
otherwise returns None.



**Signature:** (name)



**Return Value:** None

[Back to Top](#module-overview)


## get\_setup\_config
No description



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


