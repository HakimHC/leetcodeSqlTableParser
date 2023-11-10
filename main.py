import sample_data
from LcSqlParser import LcSqlParser

def main():
    mydb = LcSqlParser(sample_data.table_raw)
    print(f"All the tables: {mydb.get_tables()}")

    for table in mydb.get_tables():
        print("Name:", table.name)
        print(table.df)


if __name__ == "__main__":
    main()
