-- SQLite

-- CREATE TABLES

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    registration_date TIMESTAMP DEFAULT (datetime('now'))
);


CREATE TABLE payment_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(15) NOT NULL
);


CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code CHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    entry_date TIMESTAMP NOT NULL DEFAULT (datetime('now')),
    brand VARCHAR(30) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 1
);


CREATE TABLE shopping_carts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id)
);


CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_number CHAR(10) NOT NULL,
    purchase_date TIMESTAMP NOT NULL DEFAULT (datetime('now')),
    total INT NOT NULL,
    shopping_cart_id INTEGER NOT NULL REFERENCES shopping_carts(id),
    payment_method_id INTEGER NOT NULL REFERENCES payment_methods(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    buyers_phone VARCHAR(20) NOT NULL,
    employee_code VARCHAR(20) NOT NULL
);


CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT NOT NULL,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    date TIMESTAMP DEFAULT (datetime('now')),
    product_id INTEGER NOT NULL REFERENCES products(id),
    user_id INTEGER NOT NULL REFERENCES users(id)
);


CREATE TABLE product_shopping_cart (
    product_id INTEGER NOT NULL REFERENCES products(id),
    shopping_cart_id INTEGER NOT NULL REFERENCES shopping_carts(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (product_id, shopping_cart_id)
);


CREATE TABLE product_receipt (
    product_id INTEGER REFERENCES products(id),
    receipt_id INTEGER REFERENCES receipts(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    total INTEGER NOT NULL,
    PRIMARY KEY (product_id, receipt_id)
);


CREATE TABLE receipt_supplier (
    receipt_id INTEGER REFERENCES receipts(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    PRIMARY KEY (receipt_id, supplier_id)
);

-- INSERTS


INSERT INTO users (name, email)
    VALUES
        ('John Gonzales Pineda', 'john@gmail.com'),
        ('Sebastian Saenz Chavarria', 'sebas@gmail.com'),
        ('Santiago Alvarez Elizondo', 'santiago@gmail.com');


INSERT INTO payment_methods (type)
    VALUES
        ('cash'),
        ('card'),
        ('paypal');


INSERT INTO suppliers (name)
    VALUES
        ('Banco de Costa Rica'),
        ('BAC'),
        ('Banco Nacional'),
        ('Banco Popular'),
        ('Cash');


INSERT INTO products (code, name, price, brand, stock)
    VALUES
        ('A9A8S773', 'Ultra-Slim Laptop 14', 70000, 'Huawei', 5),
        ('9CD98D74', 'Hydrating Shampoo', 2000, 'Head and Shoulders', 34),
        ('74HR3EY3', 'Stainless Steel Water Bottle', 7000, 'Yeti', 17),
        ('7RH8YB3Y', 'High-Precision Optical Mouse', 15000, 'Apple', 27),
        ('382NVU43', 'Wireless Ergonomic Keyboard', 35000, 'Apple', 6),
        ('CRH3BY44', 'Polarized Sunglasses', 5000, 'Rayban', 8),
        ('HFDYE843', 'Wireless Bluetooth Headphones with Mic', 50000, 'Razer', 38),
        ('HFVY84IRU', '55-inch 4K Ultra HD Smart TV', 250000, 'Samsung', 5);


INSERT INTO shopping_carts (user_id)
    VALUES
        (1),
        (2),
        (3);


INSERT INTO receipts (receipt_number, total, shopping_cart_id, payment_method_id, user_id, buyers_phone, employee_code)
    VALUES
        (284737437, 41000, 1, 2, 1, 87432834, 43532),
        (5384934393, 29000, 2, 3, 2, 78234789, 43532),
        (4353234443, 10000, 3, 1, 3, 89765345, 437684),
        (2365543232, 254000, 1, 2, 1, 87432834, 437684),
        (5467934359, 100000, 2, 2, 2, 78234789, 43532);


INSERT INTO reviews (comment, rating, product_id, user_id)
    VALUES
        ('Perfect mouse for gaming', 5, 4, 2),
        ('Dont like how clicks sound but the mouse looks amazing', 3, 4, 3),
        ('Best TV!!', 5, 8, 1),
        ('Good shampoo', 4, 2, 2);


INSERT INTO product_shopping_cart (product_id, shopping_cart_id, quantity)
    VALUES
        (5, 1, 1),
        (5, 2, 1),
        (2, 1, 5),
        (4, 2, 2),
        (7, 2, 1),
        (3, 2, 2),
        (6, 3, 2),
        (8, 1, 1);


INSERT INTO product_receipt (product_id, receipt_id, quantity, total)
    VALUES
        (5, 1, 1, 35000),
        (5, 5, 1, 35000),
        (2, 4, 2, 4000),
        (4, 5, 1, 15000),
        (7, 5, 1, 50000),
        (3, 2, 2, 14000),
        (2, 1, 3, 6000),
        (4, 2, 1, 15000),
        (6, 3, 2, 10000),
        (8, 4, 1, 250000);


INSERT INTO receipt_supplier (receipt_id, supplier_id)
    VALUES
        (1, 2),
        (2, 5),
        (3, 5),
        (4, 1),
        (5, 2);


-- Obtenga todos los productos almacenados
SELECT * FROM products;

-- Obtenga todos los productos que tengan un precio mayor a 50000
SELECT * FROM products WHERE price > 50000;

-- Obtenga todas las compras de un mismo producto por id.
SELECT * FROM product_receipt WHERE product_id = 5;

-- Obtenga todas las compras agrupadas por producto, donde se muestre el total comprado entre todas las compras.
SELECT product_id, SUM(total) as total FROM product_receipt GROUP BY product_id;

-- Obtenga todas las facturas realizadas por el mismo comprador
SELECT * FROM receipts WHERE user_id = 1;

-- Obtenga todas las facturas ordenadas por monto total de forma descendente
SELECT * FROM receipts ORDER BY total DESC;

-- Obtenga una sola factura por número de factura.
SELECT * FROM receipts WHERE receipt_number = 284737437;


-- EJERCICIOS EXTRA

-- Cree la tabla categories con: id (PK autoincrement), name (UNIQUE, NOT NULL), description
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30) UNIQUE NOT NULL,
    description TEXT
);

-- Agregue a products la columna category_id (INTEGER, puede permitir NULL)
ALTER TABLE products
    ADD category_id INTEGER REFERENCES categories(id);


-- Inserte al menos 3 filas en categories
INSERT INTO categories (name)
    VALUES ('technology');

INSERT INTO categories (name, description)
    VALUES ('self-care', 'Personal care products designed to maintain daily hygiene, freshness, and well-being, including items such as shampoo, soap, deodorants, and other essential self-care items.');

INSERT INTO categories (name)
    VALUES ('accessories');

INSERT INTO categories (name)
    VALUES ('drinkware');


-- Actualice algunos products asignándoles un category_id
UPDATE products SET category_id = 1 WHERE id IN (1, 4, 5, 7, 8);

UPDATE products SET category_id = 2 WHERE id = 2;

UPDATE products SET category_id = 3 WHERE id = 6;

UPDATE products SET category_id = 4 WHERE id = 3;


-- Verifique con SELECT * FROM products (muestre id, product_name, price, quantity, category_id)
SELECT * FROM products;









