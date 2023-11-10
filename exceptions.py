class NoTableNameError(Exception):
    def __init__(self):
        super().__init__("No table name found in input.")


class InvalidHeaderLineError(Exception):
    def __init__(self):
        super().__init__("The header line of the table is not valid.")
