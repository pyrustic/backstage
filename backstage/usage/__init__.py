from enum import Enum


class Usage(Enum):
    APPEND = "append <var> to <filename_var>"
    ASSERT = "assert (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ..."
    BRANCH = "& <subtask> [<argument> ...]"
    BREAK = "break"
    BROWSE = "browse [files] [and] [dirs] in <dirname_var>"
    CALL = "call <module>.<function>[(<argument_var>, ...)]"
    CD = "cd <dirname_var>"
    CHECK = "check <var>"
    CLEAR = "clear <var> ..."
    COMMENT = "# <comment>"
    CONFIG = "config <option> ..."
    COPY = "copy <src_path_var> to <dest_path_var>"
    COUNT = "count (chars|items|lines) in (<var>|<filename_var>) [(file)]"
    CREATE = "create (dir|file) <path_var>"
    DEFAULT = "default <var> ..."
    DROP = "drop <var> ..."
    ELIF = "elif (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ..."
    ELSE = "else"
    ENTER = "> [<var> [: <text>]]"
    EXIT = "exit"
    EXPOSE = "expose <var> ..."
    FAIL = "fail"
    FIND = ("find [all] (paths|files|dirs) in <dirname_var>",
            "find ... matching <regex_var>",
            "find ... [and] (accessed|modified|created) (at|after|before|between) <timestamp_var> [and <timestamp_var>]")
    FOR = "for (char|item|line) in (<var>|<filename_var>) [(file)]"
    FROM = "from <start> to <end>"
    GET = "get (char|item|line) <index> from (<var>|<filename_var>) [(file)]"
    IF = "if (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ..."
    INTERFACE = "interface with [<package>.]<module> [alias <name>]"
    LINE = "(=|-) ..."
    MOVE = "move <src_path_var> to <dest_path_var>"
    PASS = "pass"
    POKE = "poke <path_var>"
    PREPEND = "prepend <var> to <filename_var>"
    PRINT = ": <text>"
    PUSH = "push <var> ..."
    READ = "read (*|<index>) from <filename_var>"
    REPLACE = "replace <regex_var> in <text_var> with <replacement_var>"
    RETURN = "return [<var>]"
    SET = "set <var> [(raw)|(str)|(list)|(dict)|(int)|(float)|(date)|(time)|(dtime)|(tstamp))] = <value>"
    SLEEP = "sleep <seconds>"
    SPAWN = "$ <program> [<argument> ...]"
    SPLIT = "split <text_var> with <regex_var>"
    SPOT = "spot <regex_var> in <text_var>"
    STORE = "store <var> ..."
    THREAD = "~ <subtask> [<argument> ...]"
    WHILE = "while (<var1>|<regex_var>) (==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) <var2> [and|or] ..."
    WRITE = "write <var> to <filename_var>"

