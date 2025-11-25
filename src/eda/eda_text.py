import pandas as pd
import re
import matplotlib.pyplot as plt
from pathlib import Path

# importing NLP tools 
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

class EDA_Text:
    """
    NLP-focused EDA class.
    Performs:
    - headline cleaning
    - frequent phrases (1-grams + 2-grams)
    - word cloud generation
    """

    def __init__(self, df):
        self.df = df
        
    @staticmethod
    def clean_headline(text):
        """Basic NLP-style cleaning: lower, remove noise, keep words."""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"http\S+", "", text)          # remove URLs
        text = re.sub(r"[^a-z0-9\s]", " ", text)     # keep letters, digits, space
        
        # FIX: Loosen the word length filter to be less aggressive.
        # This prevents breaking up terms like 'Q1' or 'M&A'.
        text = " ".join([w for w in text.split() if len(w) > 2]) 
        
        return text

    # --- PRIVATE HELPER METHOD (The Core Logic) ---

    def _run_vectorization(self, top_n, ngram_range):
        """Internal method to handle the CountVectorizer logic."""
        if CountVectorizer is None:
            raise Exception("Install scikit-learn: pip install scikit-learn")

        # Clean all headlines using the static method
        clean = self.df["headline"].apply(EDA_Text.clean_headline)

        # Use the passed ngram_range
        vec = CountVectorizer(ngram_range=ngram_range, stop_words="english", min_df=5)
        X = vec.fit_transform(clean)
        
        # Get counts
        counts = X.sum(axis=0).A1
        terms = vec.get_feature_names_out()
        
        # Sort & return top
        result = pd.DataFrame({"phrase": terms, "count": counts})
        return result.sort_values("count", ascending=False).head(top_n)


    def get_top_keywords_and_phrases(self, top_n=20):
        """
        [Finds common keywords (unigrams) and phrases (bigrams).
        Used for a comprehensive view of the most frequent terms.
        """
        return self._run_vectorization(top_n=top_n, ngram_range=(1, 2))

    def get_top_signals_only(self, top_n=20):
        """
        [Finds targeted bigram signals like 'price target'.
        Used for isolating specific financial events and topics.
        """
        return self._run_vectorization(top_n=top_n, ngram_range=(2, 2))


    def plot_wordcloud(self, save_path="reports/figures/wordcloud.png"):
        """Generate and save a simple word cloud."""
        if WordCloud is None:
            print("Skip word cloud: install with `pip install wordcloud matplotlib`")
            return

        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Note: WordCloud is often best run on (1, 1) or a mix of n-grams.
        text = " ".join(self.df["headline"].astype(str).apply(EDA_Text.clean_headline))
        wc = WordCloud(width=1000, height=500, background_color="white").generate(text)
        
        plt.figure(figsize=(12, 5))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title("Top Words in Financial Headlines")
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        print(f" Word cloud saved: {save_path}")