# B5W2: Customer Experience Analytics for Fintech Apps

This repository contains a data pipeline and analysis framework to scrape, preprocess, and analyze customer reviews from Google Play Store apps of Ethiopian fintech banks (Commercial Bank of Ethiopia, Bank of Abyssinia, Dashen Bank). The goal is to enable data-driven insights into customer sentiment and thematic issues for improving banking services.

🧭 Project Structure
b5w2-customer-analytics/
├── data/
│   ├── raw/
│   │   └── reviews.csv          # Raw scraped reviews
│   └── analyzed/
│       ├── analyzed_reviews.csv # Processed reviews with sentiment and themes
│       └── sentiment_agg.csv    # Aggregated sentiment by bank and rating
├── scripts/
│   ├── scrape_reviews.py        # Script to scrape and preprocess reviews
│   ├── analyze_reviews.py       # Script for sentiment and thematic analysis
│   ├── count_themed_reviews.py
│   └── utils.py                 # Shared utility 
├── .gitignore                    # Excludes local artifacts
├── requirements.txt             # Dependencies
└── README.md                    # You're here

📌 Project Objectives
Main goal: Analyze customer feedback from fintech apps to support service improvement and strategic decision-making.

- **Initial Setup and Project Structure**
  - ☑️ Set up GitHub repository with clear folder structure
  - ☑️ Define modular code layout (scripts/, data/, docs/)
  - ☑️ Add `.gitignore` to exclude local artifacts
  - ☑️ Create and document environment dependencies (requirements.txt)
  - ☑️ Create shared utility scripts for reuse

- **Data Collection and Preprocessing (Task 1)**
  - ☑️ Scrape 1,200+ reviews using `google-play-scraper`
  - ☑️ Clean data by removing duplicates and normalizing dates
  - ☑️ Generate cleaned dataset: `data/raw/reviews.csv`

- **Sentiment and Thematic Analysis (Task 2)**
  - ☑️ Perform sentiment analysis on 1,199 reviews using `distilbert-base-uncased-finetuned-sst-2-english`
  - ☑️ Extract themes (Screenshot Restrictions, App Stability, Security Features, Transaction Issues, Positive User Experience)
  - ☑️ Aggregate sentiment by bank and rating
  - ☑️ Save analyzed data: `data/analyzed/analyzed_reviews.csv` and `sentiment_agg.csv`

🔧 Data Pipeline
Implemented in `scripts/`:

- **scrape_reviews.py**:
  - Step: Scrape reviews for three banks
  - Step: Remove duplicates and handle missing data
  - Step: Normalize dates to YYYY-MM-DD
  - Callable via: `python scripts/scrape_reviews.py`

- **analyze_reviews.py**:
  - Step: Preprocess text with spaCy (lemmatization, stop-word removal)
  - Step: Perform sentiment analysis with distilbert and VADER (neutral detection)
  - Step: Extract 15 keywords per review using TF-IDF
  - Step: Assign themes based on keywords
  - Step: Aggregate sentiment by bank and rating
  - Callable via: `python scripts/analyze_reviews.py`

📊 EDA Highlights
- ☑️ Sentiment scores for 1,199 reviews (Positive, Negative, Neutral)
- ☑️ Five identified themes with keyword-based assignment
- ☑️ Aggregated sentiment statistics by bank and rating

🌍 Usage
1. **Setup Environment**
   ```bash
   git clone https://github.com/Trilord52/b5w2-customer-analytics.git
   cd b5w2-customer-analytics
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
2. **Run Data Collection**
    python scripts/scrape_reviews.py
3. **Run Analysis**
    python scripts/analyze_reviews.py

📈 Contribution Summary

Feature: Implemented
Data scraping pipeline: ☑️ scrape_reviews.py
Sentiment analysis: ☑️ analyze_reviews.py with distilbert and VADER
Thematic analysis: ☑️ 5 themes with TF-IDF keywords
Modular code design: ☑️ utils.py for shared logic
Git commits & PR hygiene: ☑️ Followed task-1 and task-2 branching