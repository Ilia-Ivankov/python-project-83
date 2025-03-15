-- Таблица для хранения URL-адресов.
CREATE TABLE urls (
        id SERIAL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        name VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );