-- Create database only if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'docmind_db') THEN
        CREATE DATABASE docmind_db;
    END IF;
END $$;

-- Connect to the new database
\c docmind_db

-- Ensure PGVector extension is installed
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA pg_catalog;

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS dev;

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS dev.pdf_data (
    source VARCHAR,
    page_content VARCHAR,
    page_number INTEGER,
    page_content_embeddings vector(768)
);

-- Check the structure of the table
SELECT column_name, data_type, character_maximum_length 
FROM information_schema.columns 
WHERE table_schema = 'dev' AND table_name = 'pdf_data';

-- Describe another table (if it exists)
\d dev.pdf_data;
