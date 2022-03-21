import os
import os.path
import sys
import backstage
from backstage import error

__all__ = []


def main():
    project_dir = os.getcwd()
    args = sys.argv[1:]
    tasks = None
    try:
        tasks = backstage.get_tasks(project_dir)
    except error.NoTasksFileError:
        pass
    if not args:
        help_handler()
        if tasks:
            show_available_tasks(tasks)
        else:
            if ask_for_default_tasks_creation():
                create_default_tasks_file(project_dir)
        return
    task = args[0]
    if tasks:
        if task in tasks:
            backstage.run(*tasks[task], extra_args=args[1:])
        else:
            print("This task doesn't exist\n")
            show_available_tasks(tasks)
    else:
        help_handler()
        if ask_for_default_tasks_creation():
            create_default_tasks_file(project_dir)


def help_handler():
    """Help me !"""
    intro = ("Project Backstage\n",
             "https://github.com/pyrustic/backstage\n")
    print("".join(intro))


def show_available_tasks(tasks):
    print("Available Tasks")
    print("===============\n")
    print("  ".join(tasks.keys()))
    print()


def ask_for_default_tasks_creation():
    print("Missing 'backstage.tasks' file in the project root.")
    print("A default 'backstage.tasks' can be generated !")
    answer = input("Generate ? (y/N): ")
    if answer.lower() == "y":
        return True
    return False


def create_default_tasks_file(project_dir):
    default_tasks = backstage.get_default_tasks()
    if backstage.create_tasks_file(default_tasks, project_dir=project_dir, override=True):
        print("\nSuccessfully generated a default tasks file !\n")
        tasks = backstage.get_tasks(project_dir)
        if tasks:
            show_available_tasks(tasks)


if __name__ == "__main__":
    main()
