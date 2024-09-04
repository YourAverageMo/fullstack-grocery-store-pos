# python file used to import into products_dao for easier reading
# when creating a new sql you can simply change the formatter sqlite3 to make it easier

select_all = "SELECT * FROM products ORDER BY `product_id` ASC"

insert_new_products = "INSERT INTO `products` (`name`, `uom_id`, `price_per_unit`) VALUES (?, ?, ?)"

delete_products = "DELETE FROM `products` WHERE (typeof(`rowid`) = 'integer' AND ((? <= `rowid` AND `rowid` <= ?)))"

edit_products = "UPDATE `products` SET `name` = ?, 'uom_id' = ?, price_per_unit = ? WHERE `rowid` IS ?"

reindex_update = "UPDATE `products` SET `product_id` = ? WHERE `rowid` IS ? AND `product_id` IS ?"

reset_seq = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'products'"
