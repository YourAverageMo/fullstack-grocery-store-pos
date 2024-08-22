import sqlite3
import os


def connect_to_db():
    """
    Connects to the SQLite database.

    Returns:
        tuple: A tuple containing:
            - conn (sqlite.Connection): The connection object to the SQLite database.
            - cursor (sqlite.Cursor): The cursor object for executing SQL queries.
    """
    # sqlite3 doesnt accept relative paths. instead of using absolute path, grab absolute path via os
    # if '/db/store.db' doesnt work use '\\db\\store.db'
    path = os.path.dirname(os.path.realpath(__file__)) + '/db/store.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    return conn, cursor


def get_all_products(cursor: sqlite3.Cursor):
    """Selects and returns all products from products table

    Args:
        cursor (sqlite3.Cursor): The SQLite3 cursor object to be used in the execute command

    Returns:
        sqlite3.cursor.Fetchall(): object from sqlite3 library in the form of nested lists where each item corresponds to a row in the database from the cursor input
    """
    cursor.execute("SELECT * FROM products")
    all_products = cursor.fetchall()
    return all_products


def insert_new_products(cursor: sqlite3.Cursor, products: list[tuple[str, int,
                                                                     int]]):
    """Inserts a new row item into the products table using the provided cursor

    Args:
        cursor (sqlite3.Cursor): The SQLite3 cursor object to be used in the execute command
        products (list[tuple[str, int, int]]): a list of tuples where each tuple represents the data to be inserted into the products table. In order from left to right on the table columns 

    Returns:
        bool: True if successfully inserted row
    """
    cursor.executemany(
        "INSERT INTO `products` (`name`, `uom_id`, `price_per_unit`) VALUES (?, ?, ?)",
        products)
    return True


def delete_products(cursor: sqlite3.Cursor,
                    rows: list[tuple[int, int]],
                    reindex: bool = False) -> bool:
    """Deletes rows from the products table, starting from index 0 to index 1 (both inclusive) in the 'rows' list. Use '(0,0)' if you only want to reindex. Set `reindex=True` to renumber the rows and reset the autoincrement if deleting rows from the middle of the table.

    Args:
        cursor (sqlite3.Cursor): The SQLite3 cursor object to be used in the execute command
        rows (list[tuple[int, int]]): The rows to be deleted
        reindex (bool, optional): renumber rows and reset autoincrement. Defaults to False.

    Returns:
        bool: True if successfully deleted rows
    """
    cursor.executemany(
        "DELETE FROM `products` WHERE (typeof(`rowid`) = 'integer' AND ((? <= `rowid` AND `rowid` <= ?)))",
        rows)
    # renumber product_id values (table index) to remove gaps in numbering
    if reindex:
        all_rows = cursor.execute(
            "SELECT * FROM products ORDER BY `product_id` ASC").fetchall()
        all_rows = [(new_index, old_index[0], old_index[0])
                    for new_index, old_index in enumerate(all_rows, 1)]
        print(all_rows)
        cursor.executemany(
            "UPDATE `products` SET `product_id` = ? WHERE `rowid` IS ? AND `product_id` IS ?",
            all_rows)
        cursor.execute(
            "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'products';")
    return True


if __name__ == '__main__':
    conn, cursor = connect_to_db()

    # print(get_all_products(cursor))
    # print("---")
    # insert_new_products(cursor, [("rice", 2, 5), ("rice", 2, 5)])
    delete_products(cursor, [
        (0, 0),
    ], True)

    conn.commit()
    conn.close()
