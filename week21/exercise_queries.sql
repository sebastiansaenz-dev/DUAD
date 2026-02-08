CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    author_id INTEGER REFERENCES authors(id)
);

CREATE TABLE rents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id),
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    state VARCHAR(10) NOT NULL CHECK (state IN ('On time', 'Returned', 'Overdue'))
);


INSERT INTO authors (name)
    VALUES 
        ('Miguel de Cervantes'),
        ('Dante Alighieri'),
        ('Takehiko Inoue'),
        ('Akira Toriyama'),
        ('Walt Disney');

INSERT INTO customers (name, email)
    VALUES
        ('John Doe', 'j.doe@email.com'),
        ('Jane Doe', 'jane@doe.com'),
        ('Luke Skywalker', 'darth.son@email.com');

INSERT INTO books (name, author_id)
    VALUES
        ('Don Quijote', 1),
        ('La Divina Comedia', 2),
        ('Vagabond 1-3', 3),
        ('Dragon Ball 1', 4),
        ('The Book of the 5 Rings', NULL);

INSERT INTO rents (book_id, customer_id, state)
    VALUES
        (1, 2, 'Returned'),
        (2, 2, 'Returned'),
        (1, 1, 'On time'),
        (3, 1, 'On time'),
        (2, 2, 'Overdue');


-- Obtenga todos los libros y sus autores
SELECT book.name, author.name FROM books AS book LEFT JOIN authors AS author ON book.author_id == author.id;

-- Obtenga todos los libros que no tienen autor
SELECT book.name, author.name FROM books AS book LEFT JOIN authors AS author ON book.author_id == author.id WHERE author.name IS NULL;

-- Obtenga todos los autores que no tienen libros
SELECT authors.name as authors_without_book FROM authors LEFT JOIN books ON authors.id == books.author_id WHERE books.id IS NULL;

-- Obtenga todos los libros que han sido rentados en algún momento
SELECT books.name as rented_books, rents.state FROM books INNER JOIN rents ON rents.book_id == books.id;

-- Obtenga todos los libros que nunca han sido rentados
SELECT books.name as never_rented_books FROM books LEFT JOIN rents ON rents.book_id == books.id WHERE rents.id IS NULL;

-- Obtenga todos los clientes que nunca han rentado un libro
SELECT customers.name FROM customers LEFT JOIN rents ON customers.id == rents.customer_id WHERE rents.customer_id IS NULL;

-- Obtenga todos los libros que han sido rentados y están en estado “Overdue”
SELECT books.name, rents.state FROM books INNER JOIN rents ON books.id == rents.book_id WHERE state == 'Overdue';


-- EJERCICIOS EXTRA

-- SEGUNDO EJERCICIO EXTRA
-- Obtenga el número total de veces que cada cliente ha rentado un libro
SELECT customers.name, COUNT(rents.id) as total_rents FROM customers INNER JOIN rents ON customers.id == rents.customer_id INNER JOIN books ON books.id == rents.book_id GROUP BY customers.name ORDER BY total_rents DESC LIMIT 3;

-- TERCER EJERCICIO EXTRA
SELECT customers.name AS customer, books.name AS book, IFNULL(authors.name, 'Without Author') AS author, rents.state FROM rents INNER JOIN customers ON rents.customer_id == customers.id INNER JOIN books ON rents.book_id == books.id LEFT JOIN authors ON authors.id == books.author_id;