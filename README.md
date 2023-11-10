LeetCode SQL Table Parser
=========================

LeetCode SQL Table Parser is a tool that parses the example input of a SQL LeetCode
problem, so you can easily test your queries locally. \
All of the implementation is in one single Python class (LcSqlParser).

Example
=======

```Python
from sample_data import table_raw
from LcSqlParser import LcSqlParser


def connect_to_database(driver_name="postgresql+psycopg2") -> sqlalchemy.engine:


# Implement logic to connect to a database with SQLAlchemy
# ...

def main():
    parser = LcSqlParser(sample_data.table_raw)  # Check out the sample data example
    print(f"All the tables: {[table.name() for table in parser.tables()]}")

    for table in parser.tables():
        print("Name:", table.name())
        print(table.df())

    sql_cnx = connect_to_database()  # Error handling is omitted
    parser.upload_to_database(sql_cnx)
```

## Example input

```
table_raw = """
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+ 
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+

Product table:
+------------+--------------+
| product_id | product_name |
+------------+--------------+
| 100        | Nokia        |
| 200        | Apple        |
| 300        | Samsung      |
+------------+--------------+
"""
```

## Example output

```
All the tables: ['Sales', 'Product']

Name: Sales
  sale_id product_id  year quantity price
0       1        100  2008       10  5000
1       2        100  2009       12  5000
2       7        200  2011       15  9000

Name: Product
  product_id product_name
0        100        Nokia
1        200        Apple
2        300      Samsung
```

LcSqlParser class
=================

This class takes a multiline string of the SQL tables as the constructor, and parser all of the input.
The input ideally should be clean, as LeetCode always gives it in a clean format.
Minimal error handling is done (the string gets trimmed and gets checked for a valid name and valid headers).
\
\
This class only contains 2 public methods:
* ```LcSqlParser.tables()``` returns a list of ```LcSqlParser.Table``` objects. See more information about this subclass below.

* ```LcSqlParser.upload_to_database()``` creates the tables in the database (if the tables already exist, it drops them, and creates them again).

Table class
===========

This class is a subclass of the ```LcSqlParser``` class, and only contains access methods to its attributes.

* ```LcSqlParser.Table.df()``` returns the DataFrame contained by the Table object.
* ```LcSqlParser.Table.name()``` returns the name of the table.

Work in progress
================