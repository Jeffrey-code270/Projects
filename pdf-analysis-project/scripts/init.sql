CREATE TABLE IF NOT EXISTS keyword_frequency (
    id SERIAL PRIMARY KEY,
    pdf_name VARCHAR(255) NOT NULL,
    keyword VARCHAR(100) NOT NULL,
    frequency INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pdf_name, keyword)
);