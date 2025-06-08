import pandas as pd
df = pd.read_csv('data/analyzed/analyzed_reviews.csv')
print(len(df[df['themes'].apply(len) > 0]))  # Number with themes