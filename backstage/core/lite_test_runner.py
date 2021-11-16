import unittest
import os.path
import sys


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
    tests_dir = os.path.join(project_dir, "tests")
    tests_success = None
    tests_result = None
    if os.path.exists(tests_dir):
        test_host = LiteTestRunner(tests_dir, project_dir)
        tests_success, tests_result = test_host.run()
    return tests_success, tests_result


class LiteTestRunner:
    def __init__(self, tests_dir, project_dir):
        self._tests_dir = tests_dir
        self._project_dir = project_dir

    def run(self, failfast=True):
        if not os.path.exists(self._tests_dir):
            return False, "This tests directory doesn't exist: "
        if not os.path.exists(self._project_dir):
            return False, "This project directory doesn't exist: "
        reloader = _Reloader()
        reloader.save_state()
        cache = self._run(failfast)
        reloader.restore_state()
        return cache

    def _run(self, failfast):
        test_loader = unittest.TestLoader()
        suite = test_loader.discover(self._tests_dir, top_level_dir=self._project_dir)
        result = unittest.TestResult()
        try:
            result.startTestRun()
            result.failfast = failfast
            suite.run(result)
        except Exception as e:
            return False, e
        finally:
            result.stopTestRun()
        if suite.countTestCases() == 0:
            return None, None
        if result.wasSuccessful():
            return True, None
        else:
            return False, self._stringify_result(result)

    def _stringify_result(self, result):
        data = []
        if result.errors:
            for error in result.errors:
                cache = "{}\n{}".format(error[0], error[1])
                data.append(cache)
        if result.failures:
            for failure in result.failures:
                cache = "{}\n{}".format(failure[0], failure[1])
                data.append(cache)
        if result.unexpectedSuccesses:
            for expected_failure in result.expectedFailures:
                cache = "{}\n{}".format(expected_failure[0],
                                        expected_failure[1])
                data.append(cache)

        return "".join(data)


class _Reloader:
    def __init__(self):
        self._state = None

    def save_state(self):
        self._state = sys.modules.copy()

    def restore_state(self):
        for x in sys.modules.copy().keys():
            if x not in self._state:
                del sys.modules[x]
