import pandas as pd
from scripts.analyze_reviews import preprocess_text

def test_preprocess_text():
    sample_text = "The app CRASHES often!!!"
    processed = preprocess_text(sample_text)
    assert "crash" in processed.lower(), "Preprocessed text should contain lemmatized 'crash'"
    assert "!!!" not in processed, "Punctuation should be removed"

if __name__ == "__main__":
    test_preprocess_text()
    print("Tests passed!")