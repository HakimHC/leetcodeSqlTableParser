import re


def is_table_name(line: str) -> bool:
    """
    This function determines if a line is the line of the table's name, or not.

    :param line: A string containing a line of the table string input.
    :return: Returns True if the line contains the table's name, False if not.
    """

    regex_pattern = r"^[a-zA-Z]+\s*table:\s*$"
    ret = True
    if not re.match(regex_pattern, line):
        ret = False
    return ret
