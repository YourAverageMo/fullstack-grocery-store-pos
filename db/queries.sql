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
        `order_id` INTEGER PRIMARY KEY UNIQUE NOT NULL,
        `customer_name` TEXT NOT NULL,
        `total` REAL NOT NULL,
        `datetime` DATETIME NOT NULL
    )
