import sample_data
from Database import Database


def main():
    mydb = Database(sample_data.table_raw)
    print(f"All the tables: {mydb.get_tables()}")

    for table in mydb.get_tables():
        print("Name:", table)
        print(mydb.table_to_df(table))


if __name__ == "__main__":
    main()
