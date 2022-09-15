from enum import Enum


# namespace, base, index, key
VARIABLE_PATTERN = r"""\A(((?P<namespace>L|G|D):)|)(?P<base>[\S]+?)((\[(?P<index>-?[0-9]+)\])|(\.(?P<key>[\S]+))|)\Z"""


# var1, comparison1, var2, logic, var3, comparison2, var4
ASSERT_PATTERN = r"""(?P<var1>[\S]+) (?P<comparison1>==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) (?P<var2>[\S]+)(( (?P<logic>and|or) (?P<var3>[\S]+) (?P<comparison2>==|!=|<=|>=|<|>|in|!in|rin|!rin|matches|!matches) (?P<var4>[\S]+))|)[\s]*\Z"""


class Pattern(Enum):
    # indent, var, filename_var
    APPEND = r"""\A(?P<indent>[\s]*)append (?P<var>[\S]+) to (?P<filename_var>[\S]+)[\s]*\Z"""

    # indent, var1, comparison1, var2, logic, var3, comparison2, var4
    ASSERT = r"""\A(?P<indent>[\s]*)assert """ + ASSERT_PATTERN

    # indent, subtask, arguments
    BRANCH = r"""\A(?P<indent>[\s]*)& (?P<subtask>[\S]+)([\s]+(?P<arguments>[\s\S]*?)|)[\s]*\Z"""

    # indent
    BREAK = r"""\A(?P<indent>[\s]*)break[\s]*\Z"""

    # indent, files, dirs, dirname_var
    BROWSE = r"""\A(?P<indent>[\s]*)browse (((?P<files>files)|)(( and |)(?P<dirs>dirs)|)) in (?P<dirname_var>[\S]+)[\s]*\Z"""

    # indent, module, function, arguments
    CALL = r"""\A(?P<indent>[\s]*)call (?P<module>[\S]+)\.(?P<function>[\S]+?)(\((?P<arguments>[\s\S]*?)\)|)[\s]*\Z"""

    # indent, dirname_var
    CD = r"""\A(?P<indent>[\s]*)cd (?P<dirname_var>[\S]+)[\s]*\Z"""

    # indent, var
    CHECK = r"""\A(?P<indent>[\s]*)check (?P<var>[\S]+)[\s]*\Z"""

    # indent, vars
    CLEAR = r"""\A(?P<indent>[\s]*)clear (?P<vars>[\s\S]*?)[\s]*\Z"""

    # indent
    COMMENT = r"""\A(?P<indent>[\s]*)#[\s\S]*\Z"""

    # indent, options
    CONFIG = r"""\A(?P<indent>[\s]*)config (?P<options>[\s\S]*?)[\s]*\Z"""

    # indent, src_path_var, dest_path_var
    COPY = r"""\A(?P<indent>[\s]*)copy (?P<src_path_var>[\S]+) to (?P<dest_path_var>[\S]+)[\s]*\Z"""

    # indent, element, var, tag
    COUNT = r"""\A(?P<indent>[\s]*)count (?P<element>chars|items|lines) in (?P<var>[\S]+)( \((?P<tag>file)\)|)[\s]*\Z"""

    # indent, element, path_var
    CREATE = r"""\A(?P<indent>[\s]*)create (?P<element>dir|file) (?P<path_var>[\S]+)[\s]*\Z"""

    # indent, vars
    DEFAULT = r"""\A(?P<indent>[\s]*)default (?P<vars>[\s\S]*?)[\s]*\Z"""

    # indent, vars
    DROP = r"""\A(?P<indent>[\s]*)drop (?P<vars>[\s\S]*?)[\s]*\Z"""

    # indent, var1, comparison1, var2, logic, var3, comparison2, var4
    ELIF = r"""\A(?P<indent>[\s]*)elif """ + ASSERT_PATTERN

    # indent
    ELSE = r"""\A(?P<indent>[\s]*)else[\s]*\Z"""

    # indent, var, text
    ENTER = r"""\A(?P<indent>[\s]*)>( (?P<var>[\S]+)(| : (?P<text>[\s\S]*))|)[\s]*\Z"""

    # indent
    EXIT = r"""\A(?P<indent>[\s]*)exit[\s]*\Z"""

    # indent, vars
    EXPOSE = r"""\A(?P<indent>[\s]*)expose (?P<vars>[\s\S]*?)[\s]*\Z"""

    # indent
    FAIL = r"""\A(?P<indent>[\s]*)fail[\s]*\Z"""

    # indent, all, category, dirname_var, regex_var, field, preposition, timestamp1_var, timestamp2_var
    FIND = r"""\A(?P<indent>[\s]*)find (|(?P<all>all) )(?P<category>paths|dirs|files) in (?P<dirname_var>[\S]+)( matching (?P<regex_var>[\S]+)|)( (and |)(?P<field>accessed|created|modified) (?P<preposition>at|after|before|between) (?P<timestamp1_var>[\S]+)( and (?P<timestamp2_var>[\S]+)|)|)[\s]*\Z"""

    # indent, element, var, tag
    FOR = r"""\A(?P<indent>[\s]*)for (?P<element>char|item|line) in (?P<var>[\S]+)( \((?P<tag>file)\)|)[\s]*\Z"""

    # indent, start_var, end_var
    FROM = r"""\A(?P<indent>[\s]*)from (?P<start_var>[\S]+) to (?P<end_var>[\S]+)[\s]*\Z"""

    # indent, element, index_var, var, tag
    GET = r"""\A(?P<indent>[\s]*)get (?P<element>char|item|line) (?P<index_var>[\S]+) from (?P<var>[\S]+)( \((?P<tag>file)\)|)[\s]*\Z"""

    # indent, var1, comparison1, var2, logic, var3, comparison2, var4
    IF = r"""\A(?P<indent>[\s]*)if """ + ASSERT_PATTERN

    # indent, module, name
    INTERFACE = r"""\A(?P<indent>[\s]*)interface with (?P<module>[\S]+)( alias (?P<name>[\S]+)|)[\s]*\Z"""

    # indent
    LINE = r"""\A(?P<indent>[\s]*)[= -]+[\s]*\Z"""

    # indent, src_path_var, dest_path_var
    MOVE = r"""\A(?P<indent>[\s]*)move (?P<src_path_var>[\S]+) to (?P<dest_path_var>[\S]+)[\s]*\Z"""

    # indent
    PASS = r"""\A(?P<indent>[\s]*)pass[\s]*\Z"""

    # indent, path_var
    POKE = r"""\A(?P<indent>[\s]*)poke (?P<path_var>[\S]+)[\s]*\Z"""

    # indent, var, filename_var
    PREPEND = r"""\A(?P<indent>[\s]*)prepend (?P<var>[\S]+) to (?P<filename_var>[\S]+)[\s]*\Z"""

    # indent, text
    PRINT = r"""\A(?P<indent>[\s]*):(| (?P<text>[\s\S]*))\Z"""

    # indent, vars
    PUSH = r"""\A(?P<indent>[\s]*)push (?P<vars>[\s\S]*?)[\s]*\Z"""

    # indent, index_var, filename_var
    READ = r"""\A(?P<indent>[\s]*)read (?P<index_var>\*|[\S]+) from (?P<filename_var>[\S]+)[\s]*\Z"""

    # indent, regex_var, text_var, replacement_var
    REPLACE = r"""\A(?P<indent>[\s]*)replace (?P<regex_var>[\S]+) in (?P<text_var>[\S]+) with (?P<replacement_var>[\S]+)[\s]*\Z"""

    # indent, var
    RETURN = r"""\A(?P<indent>[\s]*)return( (?P<var>[\S]+)|)[\s]*\Z"""

    # indent, var, tag, value
    SET = r"""\A(?P<indent>[\s]*)set (?P<var>[\S]+) (|\((?P<tag>raw|str|list|dict|int|float|date|time|dtime|tstamp)\) )= (?P<value>[\s\S]*)\Z"""

    # seconds_var
    SLEEP = r"""\A(?P<indent>[\s]*)sleep (?P<seconds_var>[\S]+)[\s]*\Z"""

    # ident, mode, program, arguments
    #SPAWN = r"""\A(?P<indent>[\s]*)(?P<mode>\$|\(\$\)) (?P<command>[\s\S]+?)[\s]*\Z"""
    SPAWN = r"""\A(?P<indent>[\s]*)(?P<mode>\$|\(\$\)) (?P<program>[\S]+)([\s]+(?P<arguments>[\s\S]*?)|)[\s]*\Z"""

    # indent, text_var, regex_var
    SPLIT = r"""\A(?P<indent>[\s]*)split (?P<text_var>[\S]+) with (?P<regex_var>[\S]+)[\s]*\Z"""

    # indent, regex_var, text_var
    SPOT = r"""\A(?P<indent>[\s]*)spot (?P<regex_var>[\S]+) in (?P<text_var>[\S]+)[\s]*\Z"""

    # indent, vars
    STORE = r"""\A(?P<indent>[\s]*)store (?P<vars>[\s\S]*?)[\s]*\Z"""

    # indent, subtask, arguments
    THREAD = r"""\A(?P<indent>[\s]*)~ (?P<subtask>[\S]+)([\s]+(?P<arguments>[\s\S]*?)|)[\s]*\Z"""

    # indent, var1, comparison1, var2, logic, var3, comparison2, var4
    WHILE = r"""\A(?P<indent>[\s]*)while """ + ASSERT_PATTERN

    # indent, var, filename_var
    WRITE = r"""\A(?P<indent>[\s]*)write (?P<var>[\S]+) to (?P<filename_var>[\S]+)[\s]*\Z"""
