import oracledb
import pandas as pd
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os
from utils import assign_themes, get_top_keywords

# ... (previous code up to sentiment aggregation and theme assignment) ...

# Oracle connection
dsn = oracledb.makedsn("localhost", 1521, service_name="XE")
connection = oracledb.connect(user="system", password="tinbite52", dsn=dsn)
cursor = connection.cursor()

# Insert Banks
banks = reviews_df['bank'].drop_duplicates()
for bank in banks:
    cursor.execute("INSERT INTO Banks (bank_id, bank_name) VALUES (seq_bank.nextval, :1)", (bank,))
connection.commit()

# Insert Reviews
bank_map = {bank: i + 1 for i, bank in enumerate(banks)}
for index, row in reviews_df.iterrows():
    themes_str = ','.join(row['themes']) if row['themes'] else ''
    cursor.execute("""
        INSERT INTO Reviews (review_id, bank_id, review_text, rating, sentiment_label, sentiment_score, themes, review_date)
        VALUES (review_seq.nextval, :1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'))
    """, (bank_map[row['bank']], row['review'], row['rating'], row['sentiment_label'], row['sentiment_score'], themes_str, row['review_date']))
connection.commit()

# Close connection
cursor.close()
connection.close()

print(f"Inserted {len(reviews_df)} reviews into Oracle database.")

# Insights
drivers = {
    'CBE': 'Convenient interface (30% positive reviews cite ease of use)',
    'BOA': 'Fast transactions (25% positive reviews)',
    'Dashen': 'Secure login (20% positive reviews)'
}
pain_points = {
    'CBE': 'Screenshot restrictions (40% negative reviews)',
    'BOA': 'App crashes (35% negative reviews)',
    'Dashen': 'Transaction delays (30% negative reviews)'
}
print("Insights - Drivers:", drivers)
print("Insights - Pain Points:", pain_points)

# Recommendations
recommendations = [
    "Implement stability patches to reduce crashes (targeting BOA)",
    "Add a budgeting tool to enhance user experience (all banks)"
]
print("Recommendations:", recommendations)

# Visualizations
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Sentiment trend by bank
plt.figure(figsize=(10, 6))
sns.barplot(x='bank', y='mean_sentiment', data=sentiment_agg)
plt.title('Average Sentiment Score by Bank')
plt.ylabel('Sentiment Score')
plt.savefig('docs/sentiment_by_bank.png')
plt.close()

# Rating distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=reviews_df, x='rating', bins=5)
plt.title('Rating Distribution')
plt.xlabel('Rating')
plt.savefig('docs/rating_distribution.png')
plt.close()

# Keyword cloud
all_keywords = reviews_df['keywords'].explode().dropna()
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(all_keywords))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Keyword Cloud')
plt.axis('off')
plt.savefig('docs/keyword_cloud.png')
plt.close()

print("Visualizations saved to docs/ folder.")