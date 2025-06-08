import pandas as pd
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from utils import assign_themes, get_top_keywords

# Load preprocessed reviews
reviews_df = pd.read_csv('data/raw/reviews.csv')

# Initialize NLP tools
nlp = spacy.load('en_core_web_sm')
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Preprocess text
def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

reviews_df['processed_review'] = reviews_df['review'].apply(preprocess_text)

# Perform sentiment analysis
def get_sentiment(text):
    distilbert_result = sentiment_analyzer(text)[0]
    vader_result = vader_analyzer.polarity_scores(text)
    label = distilbert_result['label']
    score = distilbert_result['score']
    if -0.1 <= vader_result['compound'] <= 0.1:  # Neutral range
        label = 'NEUTRAL'
        score = vader_result['compound'] + 0.5  # Normalize to [0,1]
    return label, score

reviews_df[['sentiment_label', 'sentiment_score']] = reviews_df['processed_review'].apply(lambda x: pd.Series(get_sentiment(x)))

# Aggregate sentiment by bank and rating
sentiment_agg = reviews_df.groupby(['bank', 'rating']).agg({'sentiment_score': 'mean'}).reset_index()

# Extract themes using TF-IDF
try:
    tfidf = TfidfVectorizer(max_features=20)
    tfidf_matrix = tfidf.fit_transform(reviews_df['processed_review'])
    feature_names = tfidf.get_feature_names_out()

    reviews_df['keywords'] = [get_top_keywords(matrix, feature_names) for matrix in tfidf_matrix]
    print("Keywords extraction completed. Sample keywords:", reviews_df['keywords'].head().tolist())
except Exception as e:
    print(f"Error in keywords extraction: {e}")

# Assign themes
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