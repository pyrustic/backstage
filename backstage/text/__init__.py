INTRO = """\
Welcome to Pyrustic Backstage !
Ultimate task automation tool for hackers.\
"""

HELP = """\
Usage:
    backstage
    backstage <task> [<argument> ...]
    backstage <option> [<argument> ...]
    
Options:
    -i, --intro                 Show file introductory text
    -t, --tasks                 Show the list of tasks
    -T, --Tasks                 Show the descriptive list of tasks
    -d, --doc <task>            Show documentation for a specific task
    -c, --check [<task> ...]    Run tests
    -C, --Check [<task> ...]    Run tests in debug mode
    -s, --search <task>         Search for a task by its name
    -S, --Search <task>         Search for a task by keyword
    -h, --help                  Show this information page

    The <task> string can use a glob-like syntax that allows 
    wildcards '*' and '?'. Therefore, 'task1' is identical to 'task*'.
    
Visit the webpage: https://github.com/pyrustic/backstage\
"""
