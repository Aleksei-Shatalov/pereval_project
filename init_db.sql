-- Создание таблицы pereval_added
CREATE TABLE IF NOT EXISTS pereval_added (
    id SERIAL PRIMARY KEY,
    date_added TIMESTAMP,
    raw_data JSON,
    images JSON,
    status VARCHAR(20) NOT NULL DEFAULT 'new'
);

-- Ограничение на допустимые значения поля status
ALTER TABLE pereval_added
ADD CONSTRAINT status_check CHECK (status IN ('new', 'pending', 'accepted', 'rejected'));

-- Создание таблицы pereval_areas
CREATE TABLE IF NOT EXISTS pereval_areas (
    id SERIAL PRIMARY KEY,
    id_parent BIGINT NOT NULL,
    title TEXT
);

-- Создание таблицы pereval_images
CREATE TABLE IF NOT EXISTS pereval_images (
    id SERIAL PRIMARY KEY,
    date_added TIMESTAMP DEFAULT NOW(),
    img BYTEA NOT NULL
);

-- Создание таблицы spr_activities_types
CREATE TABLE IF NOT EXISTS spr_activities_types (
    id SERIAL PRIMARY KEY,
    title TEXT
);