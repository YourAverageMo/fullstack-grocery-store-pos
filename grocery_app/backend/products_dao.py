import sqlite3
import os


def connect_to_db():
    # sqlite3 doesnt accept relative paths. instead of using absolute path, grab absolute path via os
    # if '/db/store.db' doesnt work use '\\db\\store.db'
    path = os.path.dirname(os.path.realpath(__file__)) + '/db/store.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    return conn, cursor


def get_all_products(cursor: sqlite3.Cursor):
    cursor.execute("SELECT * FROM products")
    all_products = cursor.fetchall()
    return all_products


def insert_new_products(cursor: sqlite3.Cursor, products: list[tuple[str, int,
                                                                     int]]):
    cursor.executemany(
        "INSERT INTO `products` (`name`, `uom_id`, `price_per_unit`) VALUES (?, ?, ?)",
        products)
    return True


def delete_products(cursor: sqlite3.Cursor,
                    rows: list[tuple[int, int]],
                    reindex: bool = False):
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
    delete_products(cursor, [(0,0),],True)

    conn.commit()
    conn.close()
