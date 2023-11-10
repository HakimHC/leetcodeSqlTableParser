import re


class Database:
    HEADER_IDX = 3  # The index of the header row in this list (if the input is clean) is always 2
    TABLE_NAME_IDX = 1  # The table name is always in the first line

    class NoTableNameError(Exception):
        """"Exception derived class to indicate that the input table does not have a name"""
        def __init__(self):
            """Constructor"""
            super().__init__("No table name found in input.")

    class InvalidHeaderLineError(Exception):
        """"Exception derived class to indicate that the input table's headers are not valid"""
        def __init__(self):
            """Constructor"""
            super().__init__("The header line of the table is not valid.")

    def __init__(self, raw_str):
        """Constructor"""
        self.raw_str = raw_str
        self.tables_raw = self.__separate_tables()
        self.tables = dict()

        for table_raw in self.tables_raw:
            self.__parse_table(table_raw)

    def __separate_tables(self) -> list[str]:
        """
        This function splits the raw input string on empty lines.

        :return: Returns a list of raw table strings.
        """
        return re.split(r'\n\s*\n', self.raw_str)

    def __parse_table(self, table_raw):
        raw_split = table_raw.lstrip().split("\n")
        table_name = Database.__get_table_name(raw_split[self.TABLE_NAME_IDX])
        table_headers = Database.__get_table_headers(raw_split[self.HEADER_IDX])


    def __is_table_name(line: str) -> bool:
        """
        This functions determines whether the line contains the table's name.

        :line: A string to inspect.
        :return: Returns True if the line contains a table's name, False otherwise.
        """

        regex_pattern = r"^[a-zA-Z]+\s*table:\s*$"
        return Database.__regex_match(regex_pattern, line)

    def __get_table_name(name_line: str) -> str:
        """
        This function parses the table input and returns the table's name.

        :param name_line: A string which contains line of the table's name
        :return: Returns the table's name.
        """

        if not Database.__is_table_name(name_line):
            raise Database.NoTableNameError()
        return name_line.split()[0]

    def __get_table_headers(header_line: str) -> list:
        """
        This function parses a LeetCode SQL table input, and returns its headers

        :param header_line: A string of the line where the headers are found.
        :return: Returns a list of the table's headers.
        """

        regex_pattern = r"^|\s+((?:[^\s|]+\s*\|\s*)*[^\s|]+)$"
        if not re.match(regex_pattern, header_line):
            raise Database.InvalidHeaderLineError()
        return [i.strip() for i in header_line.split("|") if i]

    def __is_delim_line(line: str) -> bool:
        regex_pattern = r"^[+-]+$"
        return Database.__regex_match(regex_pattern, line)

    def __regex_match(pattern: str, s: str) -> bool:
        ret = True
        if not re.match(pattern, s):
            ret = False
        return ret
