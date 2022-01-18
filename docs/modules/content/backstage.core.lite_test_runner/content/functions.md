Back to [All Modules](https://github.com/pyrustic/backstage/blob/master/docs/modules/README.md#readme)

# Module Overview

> **backstage.core.lite\_test\_runner**
> 
> No description
>
> **Classes:** &nbsp; [LiteTestRunner](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.lite_test_runner/content/classes/LiteTestRunner.md#class-litetestrunner) &nbsp; [\_Reloader](https://github.com/pyrustic/backstage/blob/master/docs/modules/content/backstage.core.lite_test_runner/content/classes/_Reloader.md#class-_reloader)
>
> **Functions:** &nbsp; [run\_tests](#run_tests)
>
> **Constants:** &nbsp; None

# All Functions
[run\_tests](#run_tests)

## run\_tests
Runs the tests in the project_dir.

Parameters:
    - project_dir: str, path to the project_dir project

Returns: a tuple (bool, object). The bool indicate the success
(True) or the failure (False) of the tests.
The second item in the tuple can be None, an Exception instance, or a string.

Note: the tests should be located at $PROJECT_DIR/tests



**Signature:** (project\_dir)



**Return Value:** None

[Back to Top](#module-overview)


