import os.path


BASENAME = "backstage.tasks"

USER_HOME = os.path.expanduser("~")

PYRUSTIC_HOME = os.path.join(USER_HOME, "PyrusticHome")

BACKSTAGE_HOME = os.path.join(PYRUSTIC_HOME, "backstage")

TRASH_DIR = os.path.join(PYRUSTIC_HOME, "trash")

DATATYPES = ("str", "list", "dict", "int", "float")

ASSIGNMENT_TAGS = ("raw", "str", "list", "dict", "int", "float",
                   "date", "time", "dtime", "tstamp")

OPERATION_TAGS = ("file", )

NAMESPACES = ("L", "G", "D")  # Local, Global, Database

INDENT = 4

BACKTICK = "`"

CONFIG_OPTIONS = ("FailFast", "ReportException", "ShowTraceback", "TestMode", "AutoLineBreak")

ENVIRONMENT_VARS = ("ARGS", "CWD", "DATE", "EMPTY", "ERROR", "EXCEPTION",
                    "FALSE", "HOME", "LINE", "N", "NOW", "ONE", "OS", "OUTPUT",
                    "R", "RANDOM", "SPACE", "STDERR", "STDIN", "STDOUT", "TASK",
                    "TIME", "TIMEOUT", "TMP", "TRACEBACK", "TRASH", "TRUE", "ZERO")

ELEMENTS = {"append": "APPEND",         "assert": "ASSERT",     "&": "BRANCH",
            "break": "BREAK",           "browse": "BROWSE",     "call": "CALL",
            "cd": "CD",                 "check": "CHECK",       "clear": "CLEAR",
            "#": "COMMENT",             "config": "CONFIG",     "copy": "COPY",
            "count": "COUNT",           "create": "CREATE",     "default": "DEFAULT",
            "drop": "DROP",             "elif": "ELIF",         "else": "ELSE",
            "enter": "ENTER",           "exit": "EXIT",         "expose": "EXPOSE",
            "fail": "FAIL",             "find": "FIND",         "for": "FOR",
            "from": "FROM",             "get": "GET",           "if": "IF",
            "interface": "INTERFACE",   "-": "LINE",            "=": "LINE",
            "move": "MOVE",             "pass": "PASS",         "poke": "POKE",
            "prepend": "PREPEND",       ":": "PRINT",           "push": "PUSH",
            "read": "READ",             "replace": "REPLACE",   "return": "RETURN",
            "set": "SET",               "sleep": "SLEEP",       "$": "SPAWN",
            "split": "SPLIT",           "spot": "SPOT",         "store": "STORE",
            "~": "THREAD",              "while": "WHILE",       "write": "WRITE"}
