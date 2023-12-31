import re
import pandas as pd


class LcSqlParser:
    __HEADER_IDX = 2  # The index of the header row in this list (if the input is clean) is always 2
    __TABLE_NAME_IDX = 0  # The table name is always in the first line

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

    class Table:
        """
        This class' sole purpose is to hold a dataframe with a bit of metadata (the name of the SQL table)
        """
        def __init__(self, df: pd.DataFrame, name: str) -> None:
            """Constructor"""
            self.__df = df
            self.__name = name

        def __str__(self) -> str:
            """Stringify"""
            return self.__name

        def df(self) -> pd.DataFrame:
            return self.__df

        def name(self) -> str:
            return self.__name

    def __init__(self, raw_str):
        """Constructor"""
        self.__raw_str = raw_str.strip()
        self.__tables_raw = self.__separate_tables()
        self.__tables = list()

        for table_raw in self.__tables_raw:
            self.__tables.append(self.__parse_table(table_raw))

    def __separate_tables(self) -> list[str]:
        """
        This function splits the raw input string on empty lines.

        :return: Returns a list of raw table strings.
        """

        return re.split(r'\n\s*\n', self.__raw_str)

    def __parse_table(self, table_raw) -> Table:
        """
        This function parses a raw table string and creates a DataFrame as the value of the table's key.

        :param table_raw: The raw string of the table.
        :return:
        """
        raw_split = table_raw.split("\n")
        table_name = LcSqlParser.__get_table_name(raw_split[self.__TABLE_NAME_IDX])
        table_headers = LcSqlParser.__get_table_headers(raw_split[self.__HEADER_IDX])
        table_2d_array = LcSqlParser.__parse_table_contents(raw_split[self.__HEADER_IDX+1:])
        df = pd.DataFrame(table_2d_array, columns=table_headers)
        df = df.apply(pd.to_numeric, errors="coerce").fillna(df)
        df.replace("null", None, inplace=True)

        return LcSqlParser.Table(df=df, name=table_name)

    @staticmethod
    def __is_table_name(line: str) -> bool:
        """
        This functions determines whether the line contains the table's name.

        :line: A string to inspect.
        :return: Returns True if the line contains a table's name, False otherwise.
        """

        regex_pattern = r'^\w+\s*(?: table)?\:?$'
        return LcSqlParser.__regex_match(regex_pattern, line)

    @staticmethod
    def __get_table_name(name_line: str) -> str:
        """
        This function parses the table input and returns the table's name.

        :param name_line: A string which contains line of the table's name
        :return: Returns the table's name.
        """

        if not LcSqlParser.__is_table_name(name_line):
            raise LcSqlParser.NoTableNameError()
        return name_line.split()[0]

    @staticmethod
    def __get_table_headers(header_line: str) -> list:
        """
        This function parses a LeetCode SQL table input, and returns its headers

        :param header_line: A string of the line where the headers are found.
        :return: Returns a list of the table's headers.
        """

        regex_pattern = r"^|\s+((?:[^\s|]+\s*\|\s*)*[^\s|]+)$"
        if not re.match(regex_pattern, header_line):
            raise LcSqlParser.InvalidHeaderLineError()
        return [i.strip() for i in header_line.split("|") if i]

    @staticmethod
    def __is_delim_line(line: str) -> bool:
        """
        This function determines whether a string is a row delimiter line or not.

        :param: :line: String input.
        :return: Returns True if the string is a delimiter line, False otherwise.
        """

        regex_pattern = r"^[\+\-]+\s*$"
        return LcSqlParser.__regex_match(regex_pattern, line)

    @staticmethod
    def __regex_match(pattern: str, s: str) -> bool:
        """
        Simple regex matching utility.

        :param s: String to match.
        :param pattern: RegEx pattern.
        :return:
        """
        ret = True
        if not re.match(pattern, s):
            ret = False
        return ret

    @staticmethod
    def __parse_table_contents(table_raw: list[str]) -> list:
        """
        Parses the table string into a 2D array.

        :param: table_raw: List of the row strings.
        :return: 2D array for the DataFrame.
        """
        only_rows = [line for line in table_raw if not LcSqlParser.__is_delim_line(line)]
        for index, row in enumerate(only_rows):
            only_rows[index] = [i.strip() for i in row.split("|") if i]
        return only_rows

    def tables(self) -> list:
        """
        Returns a list of the existing tables.

        :return: Returns a list of the existing tables.
        """
        return list(self.__tables)

    def upload_to_database(self, sql_cnx):
        for table in self.__tables:
            table.df().to_sql(name=table.name(), con=sql_cnx, if_exists="replace", index=False)
