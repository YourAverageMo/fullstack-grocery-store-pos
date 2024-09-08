-- This document is just reference sql queries that were used throughout the project and aren't actively used.
-- 
-- 
-- 
-- 
-- intitial table creations
CREATE TABLE
    `products` (
        `product_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        `name` TEXT NOT NULL,
        `uom_id` INTEGER NOT NULL,
        `price_per_unit` REAL NOT NULL
    )
CREATE TABLE
    `uom` (
        `uom_id` INTEGER PRIMARY KEY NOT NULL,
        `uom_name` TEXT NOT NULL
    )
CREATE TABLE
    "orders_details" (
        `order_id` INTEGER PRIMARY KEY NOT NULL,
        `product_id` INTEGER NOT NULL,
        `quantity` REAL NOT NULL,
        `total_price` REAL NOT NULL
    )
CREATE TABLE
    "orders" (
        `order_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        `customer_name` TEXT NOT NULL,
        `total` REAL NOT NULL,
        `datetime` DATETIME NOT NULL
    );

--
-- adding references (foriegn keys)
--
PRAGMA foreign_keys = OFF;

BEGIN;

CREATE TABLE
    "products" (
        `product_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        `name` TEXT NOT NULL,
        `uom_id` INTEGER NOT NULL REFERENCES `uom` (`uom_id`) ON UPDATE CASCADE,
        `price_per_unit` REAL NOT NULL
    )
INSERT INTO
    `products_tmp` (`product_id`, `name`, `uom_id`, `price_per_unit`)
SELECT
    `product_id`,
    `name`,
    `uom_id`,
    `price_per_unit`
FROM
    `products`;

DROP TABLE `products`;

ALTER TABLE `products_tmp`
RENAME TO `products`;

COMMIT;

PRAGMA foreign_keys = ON;

,
() PRAGMA foreign_keys = OFF;

--
--
--
BEGIN;

CREATE TABLE
    `orders_details_tmp` (
        `order_id` INTEGER PRIMARY KEY NOT NULL REFERENCES `orders` (`order_id`) ON UPDATE CASCADE,
        `product_id` INTEGER NOT NULL REFERENCES `products` (`product_id`) ON UPDATE CASCADE,
        `quantity` REAL NOT NULL,
        `total_price` REAL NOT NULL
    );

INSERT INTO
    `orders_details_tmp` (
        `order_id`,
        `product_id`,
        `quantity`,
        `total_price`
    )
SELECT
    `order_id`,
    `product_id`,
    `quantity`,
    `total_price`
FROM
    `orders_details`;

DROP TABLE `orders_details`;

ALTER TABLE `orders_details_tmp`
RENAME TO `orders_details`;

COMMIT;

PRAGMA foreign_keys = ON;

,
()
--
-- useful queries
--
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'products';
--
--
--

UPDATE `products` SET `product_id` = ? WHERE `rowid` IS ? AND `product_id` IS ?
[2, 14, 14]
