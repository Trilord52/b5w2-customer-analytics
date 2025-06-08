import pandas as pd
from google_play_scraper import app, Sort, reviews
import os

def scrape_reviews(app_ids, num_reviews=400):
    all_reviews = []
    for app_id, bank_name in app_ids.items():
        print(f"Scraping reviews for {bank_name}...")
        reviews_data = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.MOST_RELEVANT,
            count=num_reviews
        )
        # Debugging prints to inspect raw data
        print(f"Raw reviews data sample for {bank_name}: {reviews_data[0][:2]}")  # Show first 2 reviews
        print(f"Available keys for {bank_name}: {list(reviews_data[0][0].keys()) if reviews_data[0] else 'No data'}")

        # Convert to DataFrame and select correct columns
        reviews_df = pd.DataFrame(reviews_data[0])  # Extract reviews list
        reviews_df = reviews_df[['content', 'score', 'at']]  # Exclude appId
        reviews_df.columns = ['review', 'rating', 'date_raw']  # Temporary column names
        reviews_df['bank'] = bank_name  # Use bank_name from app_ids
        reviews_df['source'] = 'Google Play'
        reviews_df['date'] = pd.to_datetime(reviews_df['date_raw']).dt.date  # Convert to date
        reviews_df = reviews_df[['review', 'rating', 'date', 'bank', 'source']]  # Final column order
        all_reviews.append(reviews_df)

    # Concatenate and clean
    combined_df = pd.concat(all_reviews, ignore_index=True)
    return combined_df.drop_duplicates().dropna()

# App IDs for Ethiopian banks
app_ids = {
    'com.combanketh.mobilebanking': 'Commercial Bank of Ethiopia',
    'com.boa.boaMobileBanking': 'Bank of Abyssinia',
    'com.dashen.dashensuperapp': 'Dashen Bank'
}

# Scrape and save
reviews_df = scrape_reviews(app_ids)
os.makedirs('data/raw', exist_ok=True)
reviews_df.to_csv('data/raw/reviews.csv', index=False)
print(f"Scraped {len(reviews_df)} reviews.")