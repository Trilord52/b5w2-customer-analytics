import oracledb
import pandas as pd

# Load cleaned data
df = pd.read_csv('data/analyzed/analyzed_reviews.csv')

# Database connection as bank_reviews (recommended for data insertion)
connection = oracledb.connect(
    user='bank_reviews',
    password='trilord52',  # Adjust if password differs
    dsn='localhost:1521/XEPDB1'
)
cursor = connection.cursor()

# Insert banks
banks = df['bank'].unique()
for bank in banks:
    cursor.execute("SELECT bank_reviews.seq_bank.NEXTVAL FROM dual")
    bank_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO bank_reviews.Banks (bank_id, bank_name) VALUES (:1, :2)",
                   (bank_id, bank))

# Insert reviews
for index, row in df.iterrows():
    cursor.execute("SELECT bank_reviews.review_seq.NEXTVAL FROM dual")
    review_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO bank_reviews.Reviews (review_id, bank_id, review_text, rating, sentiment_label,
        sentiment_score, themes, review_date)
        VALUES (:1, (SELECT bank_id FROM bank_reviews.Banks WHERE bank_name = :2), :3, :4, :5, :6, :7, TO_DATE(:8, 'YYYY-MM-DD'))
    """, (review_id, row['bank'], row['review_text'], row['rating'], row['sentiment_label'],
          row['sentiment_score'], row['themes'], row['review_date']))

# Commit and close
connection.commit()
cursor.close()
connection.close()

print("Data inserted successfully.")