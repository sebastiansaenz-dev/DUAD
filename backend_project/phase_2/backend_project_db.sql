

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT datetime('now')
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    price REAL NOT NULL,
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
    quantity INTEGER NOT NULL DEFAULT 1,
    UNIQUE (cart_id, product_id)
);

CREATE TABLE payment_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    cart_id INTEGER NOT NULL REFERENCES carts(id),
    payment_method_id INTEGER NOT NULL REFERENCES payment_methods(id),
    total REAL NOT NULL,
    date TIMESTAMP DEFAULT datetime('now'),
    type VARCHAR(20) NOT NULL CHECK (type IN ('sale', 'refund')) DEFAULT 'sale',
    parent_sale_id INTEGER REFERENCES sales(id) --Null when type is 'sale'
);

CREATE TABLE products_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL REFERENCES sales(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    UNIQUE (sale_id, product_id)
);

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE users_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    role_id INTEGER NOT NULL REFERENCES roles(id)
);