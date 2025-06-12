from sklearn.feature_extraction.text import TfidfVectorizer

def get_top_keywords(matrix, features, top_n=15):
    return [features[i] for i in matrix.indices[:top_n]] if matrix.indices.size else []

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
    # Positive User Experience
    if not themes and any(kw in ['good', 'great', 'nice', 'easy', 'convenient'] for kw in keywords):
        themes.append('Positive User Experience')
    return themes[:3]  # Limit to 3 themes