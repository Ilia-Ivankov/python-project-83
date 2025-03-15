-- Таблица для хранения URL-адресов.
CREATE TABLE urls (
    id SERIAL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Таблица для хранения данных URL.
CREATE TABLE url_data (
    id SERIAL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    response_code INTEGER,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


