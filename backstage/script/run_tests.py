import os
import os.path
import backstage
import sys


def main():
    target = os.getcwd()
    message = "Do you want to run tests ?"
    if not backstage.ask_for_confirmation(message, "n"):
        print("")
        return True
    print("")
    print("Running tests...")
    test_success, test_result = backstage.run_tests(target)
    if test_success is None:
        return True
    if test_success:
        print("Testing passed\n")
        return True
    else:
        print("Testing failed")
        print("")
        print(test_result)
        return False


if __name__ == "__main__":
    if not main():
        sys.exit(1)
