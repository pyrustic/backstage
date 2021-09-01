import os
import os.path
import backstage


def main():
    target = os.getcwd()
    cur_version = backstage.get_version(target)
    print("")
    print("What is the next version of your project ?")
    print("Type 'maj', 'min' or 'rev' for a fast version increment.")
    print("Ignore it to increment the 'revision' number.")
    new_version = input("Submit the next version: ")
    if not new_version:
        new_version = "rev"
    version = backstage.interpret_version(cur_version, new_version)
    backstage.set_version(target, version)


if __name__ == "__main__":
    main()
