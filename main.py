import os
import sample_data
from LcSqlParser import LcSqlParser
from sqlalchemy import create_engine, URL


def connect_to_database(driver_name="postgresql+psycopg2"):
    """
    This function facilitates the connection to the database.

    :param driver_name: Database driver string (defaults to postgresql+psycopg2)
    :return: Returns the newly established database connection object
    """
    url_object = URL.create(
        driver_name,
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_DATABASE")
    )
    return create_engine(url_object)


def main():
    parser = LcSqlParser(sample_data.table_raw)
    print(f"All the tables: {parser.get_tables()}")

    for table in parser.get_tables():
        print("Name:", table.name)
        print(table.df)

    sql_cnx = connect_to_database()
    parser.upload_to_database(sql_cnx)


if __name__ == "__main__":
    main()
