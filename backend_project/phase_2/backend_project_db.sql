

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT datetime('now')
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code CHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL,
    brand VARCHAR(50) NOT NULL,
    stock INTEGER NOT NULL,
    entry_date TIMESTAMP DEFAULT datetime('now')
);

CREATE TABLE carts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
);

CREATE TABLE products_carts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL REFERENCES carts(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL
);

CREATE TABLE payment_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    payment_method_id INTEGER NOT NULL REFERENCES payment_methods(id),
    total INTEGER NOT NULL,
    date TIMESTAMP DEFAULT datetime('now')
);

CREATE TABLE refunds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL REFERENCES sales(id),
    total INTEGER NOT NULL,
    date TIMESTAMP DEFAULT datetime('now')
);

CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code CHAR(10) NOT NULL UNIQUE,
    sale_id INTEGER NOT NULL REFERENCES sales(id),
    payment_method_id INTEGER NOT NULL REFERENCES payment_methods(id),
    total INTEGER NOT NULL,
    date TIMESTAMP DEFAULT datetime('now')
);

CREATE TABLE products_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL REFERENCES sales(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL
);

CREATE TABLE products_receipt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL REFERENCES receipts(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL
);

CREATE TABLE products_refunds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    refund_id INTEGER NOT NULL REFERENCES refunds(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL
);

