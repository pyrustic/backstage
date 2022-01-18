import os
import os.path
import sys
import backstage


def main():
    backstage.backstage_setup()
    project_dir = os.getcwd()
    args = sys.argv[1:]
    try:
        tasks = backstage.get_tasks(project_dir)
    except backstage.NoTasksFileError:
        tasks = dict()
    if not args:
        help_handler(project_dir, tasks)
        return
    task = args[0]
    if task not in tasks:
        help_handler(project_dir, tasks)
        return
    backstage.run(*tasks[task], extra_args=args[1:])


def help_handler(project_dir, tasks):
    """Help me !"""
    intro = ("""Project Backstage {}\n""".format(backstage.dist_version("backstage"))
             + """https://pyrustic.github.io\n"""
             + """This software is part of the Pyrustic Open Ecosystem.\n""")
    print("".join(intro))
    print("Available Tasks")
    print("===============\n")
    print("  ".join(tasks.keys()))
    print()


if __name__ == "__main__":
    main()
