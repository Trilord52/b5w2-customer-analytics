# B5W2: Customer Experience Analytics for Fintech Apps
This repository contains code and data for analyzing Google Play Store reviews of Ethiopian banks (CBE, BOA, Dashen).

## Task 1: Data Collection and Preprocessing
- **Methodology**: Used `google-play-scraper` to scrape 400+ reviews per bank (CBE, BOA, Dashen) with `lang='en'` and `country='et'`. Preprocessed data by renaming columns and saving to `data/raw/reviews.csv`.
- **Output**: `data/raw/reviews.csv` with columns: review, rating, date, bank, source.