CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL DEFAULT 'customer'
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending'
);

INSERT INTO users (name, email, role)
VALUES
    ('Alice Silva', 'alice@example.com', 'admin'),
    ('Bruno Costa', 'bruno@example.com', 'customer')
ON CONFLICT (email) DO NOTHING;

INSERT INTO products (name, description, price, stock)
VALUES
    ('Notebook Pro', 'Notebook voltado para produtividade', 5999.90, 10),
    ('Mouse Wireless', 'Mouse sem fio ergonômico', 199.90, 50)
ON CONFLICT DO NOTHING;

INSERT INTO orders (user_id, product_id, quantity, status)
SELECT 1, 1, 1, 'pending'
WHERE NOT EXISTS (SELECT 1 FROM orders WHERE user_id = 1 AND product_id = 1);

