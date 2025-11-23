# scripts/eda_text.py
import pandas as pd
import re
import matplotlib.pyplot as plt
from pathlib import Path

# importing optional NLP tools 

from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud


def clean_headline(text):
    """Basic NLP-style cleaning: lower, remove noise, keep words."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)          # remove URLs
    text = re.sub(r"[^a-z0-9\s]", " ", text)    # keep letters, digits, space
    text = " ".join([w for w in text.split() if len(w) > 2])  # drop short words
    return text


def get_top_phrases(df, top_n=20):
    """
    Use CountVectorizer (NLP) to find frequent unigrams & bigrams.
    Returns phrases like 'price target', 'fda approval'.
    """
    if CountVectorizer is None:
        raise Exception("Install scikit-learn: pip install scikit-learn")

    # Clean all headlines
    clean = df["headline"].apply(clean_headline)

    # Extract 1-grams and 2-grams (keywords + phrases)
    vec = CountVectorizer(ngram_range=(1, 2), stop_words="english", min_df=5)
    X = vec.fit_transform(clean)
    
    # Get counts
    counts = X.sum(axis=0).A1
    terms = vec.get_feature_names_out()
    
    # Sort & return top
    result = pd.DataFrame({"phrase": terms, "count": counts})
    return result.sort_values("count", ascending=False).head(top_n)


def plot_wordcloud(df, save_path="reports/figures/wordcloud.png"):
    """Generate and save a simple word cloud."""
    if WordCloud is None:
        print("Skip word cloud: install with `pip install wordcloud matplotlib`")
        return

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    
    text = " ".join(df["headline"].astype(str).apply(clean_headline))
    wc = WordCloud(width=1000, height=500, background_color="white").generate(text)
    
    plt.figure(figsize=(12, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Top Words in Financial Headlines")
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f" Word cloud saved: {save_path}")