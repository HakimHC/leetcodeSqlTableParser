import re


class Database:
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

        for table_raw in self.tables_raw:
            self.__parse_table(table_raw)

    def __separate_tables(self) -> list[str]:
        """
        This function splits the raw input string on empty lines.

        :return: Returns a list of raw table strings.
        """
        return re.split(r'\n\s*\n', self.raw_str)

    def __parse_table(self, table_raw):
        pass

    def __is_table_name(line: str) -> bool:
        """
        This functions determines whether the line contains the table's name.

        :line: A string to inspect.
        :return: Returns True if the line contains a table's name, False otherwise.
        """
        regex_pattern = r"^[a-zA-Z]+\s*table:\s*$"
        ret = True
        if not re.match(regex_pattern, line):
            ret = False
        return ret

    def get_table_name(name_line: str) -> str:
        """
        This function parses the table input and returns the table's name.

        :param name_line: A string which contains line of the table's name
        :return: Returns the table's name.
        """

        if not Database.__is_table_name(name_line):
            raise Database.NoTableNameError()
        return name_line.split()[0]

