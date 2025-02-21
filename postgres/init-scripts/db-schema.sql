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

-- ******************* Create tables for pdf data ***********************************

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS dev.pdf_data (
    source VARCHAR,
    page_content VARCHAR,
    page_number INTEGER,
    page_content_embeddings vector(768)
);


-- ******************* Create tables for questioner ***********************************

-- Drop tables if they already exist to avoid conflicts during initialization
DROP TABLE IF EXISTS dev.status_guidance_of_question;
DROP TABLE IF EXISTS dev.supporting_evidence;
DROP TABLE IF EXISTS dev.question_guidance;
DROP TABLE IF EXISTS dev.guidance;
DROP TABLE IF EXISTS dev.question;
DROP TABLE IF EXISTS dev.sub_domain;
DROP TABLE IF EXISTS dev.domain;

-- Create the domain table
CREATE TABLE IF NOT EXISTS dev.domain (
    domain_id VARCHAR(10) PRIMARY KEY,
    domain_name VARCHAR(100) NOT NULL
);

-- Create the sub_domain table with a foreign key to domain
CREATE TABLE IF NOT EXISTS dev.sub_domain (
    sub_domain_id VARCHAR(10) PRIMARY KEY,
    sub_domain_name VARCHAR(100) NOT NULL,
    domain_id VARCHAR(10) REFERENCES dev.domain(domain_id) ON DELETE CASCADE
);

-- Create the question table with a foreign key to sub_domain
CREATE TABLE IF NOT EXISTS dev.question (
    question_id VARCHAR(10) PRIMARY KEY,
    question TEXT NOT NULL,
    sub_domain_id VARCHAR(10) REFERENCES dev.sub_domain(sub_domain_id) ON DELETE CASCADE
);

-- Create the guidance table
CREATE TABLE IF NOT EXISTS dev.guidance (
    guidance_id VARCHAR(10) PRIMARY KEY,
    guidance TEXT NOT NULL
);

-- Create the question_guidance table with foreign keys to question and guidance
CREATE TABLE IF NOT EXISTS dev.question_guidance (
    question_id VARCHAR(10) REFERENCES dev.question(question_id) ON DELETE CASCADE,
    guidance_id VARCHAR(10) REFERENCES dev.guidance(guidance_id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, guidance_id)
);

-- Create the supporting_evidence table with a foreign key to question
CREATE TABLE IF NOT EXISTS dev.supporting_evidence (
    evidence_id VARCHAR(10) PRIMARY KEY,
    evidence TEXT NOT NULL,
    question_id VARCHAR(10) REFERENCES dev.question(question_id) ON DELETE CASCADE
);

-- Create the status_guidance_of_question table with a foreign key to question
CREATE TABLE IF NOT EXISTS dev.status_guidance_of_question (
    status_guidance_id VARCHAR(10) PRIMARY KEY,
    guidance TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    question_id VARCHAR(10) REFERENCES dev.question(question_id) ON DELETE CASCADE
);