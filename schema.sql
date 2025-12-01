-- 1. Create Banks Table
CREATE TABLE IF NOT EXISTS banks(
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_id VARCHAR(100) NOT NULL
);

-- 2. Create Reviews Table
CREATE TABLE IF NOT EXISTS reviews (
    review_Id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50),
    CONSTRAINT fk_bank
        FOREIGN KEY(bank_id)
        REFERENCES banks(bank_id)
);