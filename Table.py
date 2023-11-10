import pandas as pd


class Table:
    def __init__(self, df: pd.DataFrame, name: str) -> None:
        self.df = df
        self.name = name

    def __str__(self) -> str:
        return self.name