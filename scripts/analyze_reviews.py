import pandas as pd
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Load preprocessed reviews
reviews_df = pd.read_csv('data/raw/reviews.csv')

# Initialize NLP tools
nlp = spacy.load('en_core_web_sm')
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Preprocess text
def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

reviews_df['processed_review'] = reviews_df['review'].apply(preprocess_text)

# Perform sentiment analysis
def get_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

reviews_df[['sentiment_label', 'sentiment_score']] = reviews_df['processed_review'].apply(lambda x: pd.Series(get_sentiment(x)))

# Aggregate sentiment by bank and rating
sentiment_agg = reviews_df.groupby(['bank', 'rating']).agg({'sentiment_score': 'mean'}).reset_index()

# Extract themes using TF-IDF
try:
    tfidf = TfidfVectorizer(max_features=20)  # Increased to support more keywords
    tfidf_matrix = tfidf.fit_transform(reviews_df['processed_review'])
    feature_names = tfidf.get_feature_names_out()

    def get_top_keywords(matrix, features, top_n=15):
        return [features[i] for i in matrix.indices[:top_n]] if matrix.indices.size else []

    reviews_df['keywords'] = [get_top_keywords(matrix, feature_names) for matrix in tfidf_matrix]
    print("Keywords extraction completed. Sample keywords:", reviews_df['keywords'].head().tolist())
except Exception as e:
    print(f"Error in keywords extraction: {e}")

# Manually group themes
def assign_themes(keywords, bank):
    themes = []
    # Screenshot Restrictions
    if any(kw in ['screenshot', 'gallery', 'photo', 'image', 'capture', 'snap', 'picture', 'save', 'evidence'] for kw in keywords):
        themes.append('Screenshot Restrictions')
    # App Stability
    if any(kw in ['crash', 'bug', 'unreliable', 'fail', 'freeze', 'error', 'slow', 'lag', 'down'] for kw in keywords):
        themes.append('App Stability')
    # Security Features
    if any(kw in ['security', 'developer', 'option', 'lock', 'verify', 'password', 'auth', 'access', 'protect'] for kw in keywords):
        themes.append('Security Features')
    # Transaction Issues
    if any(kw in ['transaction', 'payment', 'transfer', 'delay', 'debit', 'withdraw', 'deposit', 'issue', 'fund'] for kw in keywords):
        themes.append('Transaction Issues')
    return themes[:3]  # Allow up to 3 themes for KPI

try:
    reviews_df['themes'] = [assign_themes(kw, bank) for kw, bank in zip(reviews_df['keywords'], reviews_df['bank'])]
    print("Themes assignment completed. Sample themes:", reviews_df['themes'].head().tolist())
except Exception as e:
    print(f"Error in themes assignment: {e}")

# Save results
os.makedirs('data/analyzed', exist_ok=True)
print("Columns before saving:", reviews_df.columns.tolist())
try:
    reviews_df.to_csv('data/analyzed/analyzed_reviews.csv', index=False)
    sentiment_agg.to_csv('data/analyzed/sentiment_agg.csv', index=False)
    print("Files saved successfully.")
except PermissionError as pe:
    print(f"Permission denied while saving files: {pe}. Please close any open files or run as administrator.")
except Exception as e:
    print(f"Error saving files: {e}")

print(f"Analyzed {len(reviews_df)} reviews with sentiment scores and initial themes.")