import os
import sample_data
from LcSqlParser import LcSqlParser
from sqlalchemy import create_engine


def connect_to_database():
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_DATABASE")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

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
