INTRO = """\
Welcome to Pyrustic Backstage !
Ultimate task automation tool for hackers.\
"""

HELP = """\
Usage:
    backstage
    backstage <task> [<arg> ...]
    backstage <option> [<arg> ...]
    
Options:
    -i, --intro                     Show file introductory text
    -c, --check                     Show the list of tasks
    -C, --Check                     Show the descriptive list of tasks
    -d, --debug <task> [<arg> ...]  Run task in debug mode
    -t, --test [<task> ...]         Run tests
    -T, --Test [<task> ...]         Run tests in debug mode
    -s, --search <task>             Search for a task by its name
    -S, --Search <task>             Search for a task by keyword
    -h, --help [<task>]             Show help text

    The <task> string can use a glob-like syntax that allows 
    wildcards '*' and '?'. Therefore, 'task1' is identical to 'task*'.
    
Visit the webpage: https://github.com/pyrustic/backstage\
"""
