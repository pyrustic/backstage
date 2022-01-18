Back to [All Modules](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md#readme)

# Module Overview

> **backstage.core.funcs**
> 
> No description
>
> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [\_sort\_wheels\_names](#_sort_wheels_names) &nbsp; [ask\_for\_confirmation](#ask_for_confirmation) &nbsp; [build\_package](#build_package) &nbsp; [copyto](#copyto) &nbsp; [create\_kurl](#create_kurl) &nbsp; [get\_app\_pkg](#get_app_pkg) &nbsp; [get\_hub\_url](#get_hub_url) &nbsp; [get\_project\_name](#get_project_name) &nbsp; [get\_root\_from\_package](#get_root_from_package) &nbsp; [module\_name\_to\_class](#module_name_to_class) &nbsp; [moveto](#moveto) &nbsp; [package\_name\_to\_path](#package_name_to_path) &nbsp; [strictly\_capitalize](#strictly_capitalize) &nbsp; [wheels\_assets](#wheels_assets)
>
> **Constants:** &nbsp; None

# All Functions
[\_sort\_wheels\_names](#_sort_wheels_names) &nbsp; [ask\_for\_confirmation](#ask_for_confirmation) &nbsp; [build\_package](#build_package) &nbsp; [copyto](#copyto) &nbsp; [create\_kurl](#create_kurl) &nbsp; [get\_app\_pkg](#get_app_pkg) &nbsp; [get\_hub\_url](#get_hub_url) &nbsp; [get\_project\_name](#get_project_name) &nbsp; [get\_root\_from\_package](#get_root_from_package) &nbsp; [module\_name\_to\_class](#module_name_to_class) &nbsp; [moveto](#moveto) &nbsp; [package\_name\_to\_path](#package_name_to_path) &nbsp; [strictly\_capitalize](#strictly_capitalize) &nbsp; [wheels\_assets](#wheels_assets)

## \_sort\_wheels\_names
No description



**Signature:** (data)



**Return Value:** None

[Back to Top](#module-overview)


## ask\_for\_confirmation
Use this function to request a confirmation from the user.

Parameters:
    - message: str, the message to display
    - default: str, either "y" or "n" to tell "Yes by default"
    or "No, by default".

Returns: a boolean, True or False to reply to the request.

Note: this function will append a " (y/N): " or " (Y/n): " to the message.



**Signature:** (message, default='y')



**Return Value:** None

[Back to Top](#module-overview)


## build\_package
Literally build a package, returns None or the string pathname
package represented by prefix must already exist



**Signature:** (target, package\_name, prefix='')



**Return Value:** None

[Back to Top](#module-overview)


## copyto
Please make sure that DEST doesn't exist yet !
Copy a file or contents of directory (src) to a destination file or folder (dest)



**Signature:** (src, dest)



**Return Value:** None

[Back to Top](#module-overview)


## create\_kurl
No description



**Signature:** ()



**Return Value:** None

[Back to Top](#module-overview)


## get\_app\_pkg
This function extracts the application package name from a project_dir path.
Basically it extracts the basename from the path then turns dashes "-" into
"underscores" "_".

Parameters:
    - project_dir: str, path to the project_dir project

Returns: str, the application package name.



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## get\_hub\_url
No description



**Signature:** (res)



**Return Value:** None

[Back to Top](#module-overview)


## get\_project\_name
Returns the project name



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


## get\_root\_from\_package
Return the root from a dotted package name.
Example the root here "my.package.is.great" is "my".



**Signature:** (package\_name)



**Return Value:** None

[Back to Top](#module-overview)


## module\_name\_to\_class
Convert a module name like my_module.py to a class name like MyModule



**Signature:** (module\_name)



**Return Value:** None

[Back to Top](#module-overview)


## moveto
If the DEST exists:
    * Before moveto *
    - /home/lake (SRC)
    - /home/lake/fish.txt
    - /home/ocean (DEST)
    * Moveto *
    moveto("/home/lake", "/home/ocean")
    * After Moveto *
    - /home/ocean
    - /home/ocean/lake
    - /home/ocean/lake/fish.txt
Else IF the DEST doesn't exist:
    * Before moveto *
    - /home/lake (SRC)
    - /home/lake/fish.txt
    * Moveto *
    moveto("/home/lake", "/home/ocean")
    * After Moveto *
    - /home/ocean
    - /home/ocean/fish.txt


Move a file or directory (src) to a destination folder (dest)



**Signature:** (src, dest)



**Return Value:** None

[Back to Top](#module-overview)


## package\_name\_to\_path
No description



**Signature:** (target, package\_name, prefix='')



**Return Value:** None

[Back to Top](#module-overview)


## strictly\_capitalize
No description



**Signature:** (string)



**Return Value:** None

[Back to Top](#module-overview)


## wheels\_assets
No description



**Signature:** (target)



**Return Value:** None

[Back to Top](#module-overview)


