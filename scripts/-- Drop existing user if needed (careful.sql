-- Drop existing user if needed (careful with data loss)
DROP USER bank_reviews CASCADE;

-- Create bank_reviews user
CREATE USER bank_reviews IDENTIFIED BY trilord52;
GRANT CREATE SESSION, CONNECT, RESOURCE, DBA TO bank_reviews;
ALTER USER bank_reviews DEFAULT TABLESPACE USERS QUOTA UNLIMITED ON USERS;

-- Connect as bank_reviews (add new connection with these creds if needed)
-- For now, create tables as SYSTEM
CREATE TABLE bank_reviews.Banks (
    bank_id NUMBER PRIMARY KEY,
    bank_name VARCHAR2(100) NOT NULL,
    created_date DATE DEFAULT SYSDATE
);

CREATE TABLE bank_reviews.Reviews (
    review_id NUMBER PRIMARY KEY,
    bank_id NUMBER,
    review_text VARCHAR2(1000),
    rating NUMBER,
    sentiment_label VARCHAR2(20),
    sentiment_score NUMBER,
    themes VARCHAR2(500),
    review_date DATE,
    FOREIGN KEY (bank_id) REFERENCES bank_reviews.Banks(bank_id)
);

CREATE SEQUENCE bank_reviews.seq_bank START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE bank_reviews.review_seq START WITH 1 INCREMENT BY 1;

COMMIT;
SELECT object_name FROM all_objects WHERE owner = 'BANK_REVIEWS' AND object_type IN ('TABLE', 'SEQUENCE');