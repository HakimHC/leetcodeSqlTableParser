import re

import pandas as pd

from constants import (
    HEADER_IDX,
    TABLE_NAME_IDX
)
from utils import is_table_name
from sample_data import *
from exceptions import (
    InvalidHeaderLineError,
    NoTableNameError
)


def get_table_name(name_line: str) -> str:
    """
    This function parses the table input and returns the table's name.

    :param name_line: A string which contains line of the table's name
    :return: Returns the table's name.
    """

    if not is_table_name(name_line):
        raise NoTableNameError()
    return name_line.split()[0]


def get_headers(header_line: str) -> list:
    """
    This function parses a LeetCode SQL table input, and returns its headers

    :param header_line: A string of the line where the headers are found.
    :return: Returns a list of the table's headers.
    """

    regex_pattern = r"^|\s+((?:[^\s|]+\s*\|\s*)*[^\s|]+)$"
    if not re.match(regex_pattern, header_line):
        raise InvalidHeaderLineError()
    return [i.strip() for i in header_line.split("|") if i]


def extract_dataframe(table: str) -> pd.DataFrame:
    all_rows = table.split("\n")
    table_name = get_table_name(all_rows[TABLE_NAME_IDX])
    headers = get_headers(all_rows[HEADER_IDX])
    print(f"Table name: {table_name}")
    print(f"Headers: {headers}")
    return pd.DataFrame()


def main():
    extract_dataframe(sales)
    # print(get_table_name("No worries man table:"))
    pass


if __name__ == "__main__":
    main()
