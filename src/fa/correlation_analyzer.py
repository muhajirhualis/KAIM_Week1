
import pandas as pd
from textblob import TextBlob
from pathlib import Path
import matplotlib.pyplot as plt

class CorrelationAnalyzer:
    """
    Analyzes the correlation between aggregated daily news sentiment
    and subsequent daily stock returns.
    """
    def __init__(self, news_df: pd.DataFrame, stock_df: pd.DataFrame, headline_col='headline'):
        self.news_df = news_df.copy()
        self.stock_df = stock_df.copy()
        self.headline_col = headline_col
        self.merged_df = None
        
        # Ensure necessary columns/index exist
        if headline_col not in self.news_df.columns:
             raise ValueError(f"News DataFrame must contain a '{headline_col}' column.")
        if 'Close' not in self.stock_df.columns:
             raise ValueError("Stock DataFrame must contain a 'Close' column.")

        print("✅ Correlation Analyzer initialized.")

    def perform_sentiment_analysis(self):
        """
        Applies TextBlob sentiment analysis to the news headlines.
        TextBlob's polarity ranges from -1.0 (Negative) to +1.0 (Positive).
        """
        if 'sentiment_score' in self.news_df.columns:
            print("Sentiment analysis already performed.")
            return

        # Simple lambda function to apply TextBlob
        self.news_df['sentiment_score'] = self.news_df[self.headline_col].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        print("✅ Sentiment analysis complete.")
        return self.news_df

    def align_and_aggregate_data(self):
        """
        1. Aligns news (sentiment) and stock data by date.
        2. Aggregates news sentiment to a daily average.
        3. Calculates lagged daily stock returns (The Predictive Feature).
        """
        # Step 1: Ensure dates are in the correct format for merging

        # News Data: Extract date (assuming 'date' is a datetime column or index)
        if self.news_df.index.name != 'Date':
            # Assuming a column named 'date' or 'Date' exists
            date_col = next((col for col in self.news_df.columns if 'date' in col.lower()), None)
            if date_col:
                self.news_df['Date'] = pd.to_datetime(self.news_df[date_col]).dt.date
                self.news_df.set_index('Date', inplace=True)
            else:
                 raise ValueError("Could not find a date column in the news data for alignment.")

        # Stock Data: Use existing Date index (from StockDataset loader)
        # self.stock_df.index = self.stock_df.index.date
        self.stock_df.index = pd.to_datetime(self.stock_df.index).date

        # Step 2: Aggregate daily sentiment
        daily_sentiment = self.news_df.groupby(self.news_df.index)['sentiment_score'].agg(['mean', 'count']).rename(
            columns={'mean': 'avg_daily_sentiment', 'count': 'daily_news_volume'}
        )
        print(f" Daily sentiment aggregated over {len(daily_sentiment)} days.")

        # Step 3: Calculate Stock Returns & Lagged Returns (The Target)
        self.stock_df['daily_return'] = self.stock_df['Close'].pct_change()
        
        # CRUCIAL: Lagged Return (Tomorrow's return)
        # We want to correlate TODAY's sentiment with TOMORROW's return.
        # Shift(-1) moves the return from today to yesterday's row (the previous day's news).
        self.stock_df['lagged_return'] = self.stock_df['daily_return'].shift(-1)
        
        # Step 4: Merge DataFrames
        self.merged_df = daily_sentiment.merge(
            self.stock_df[['Close', 'daily_return', 'lagged_return']], 
            left_index=True, 
            right_index=True, 
            how='inner'
        ).dropna(subset=['lagged_return']) # Drop last row since lagged_return is NaN

        print(f"✅ Data alignment and aggregation complete. Merged DF size: {len(self.merged_df)}")
        return self.merged_df

    def calculate_correlation(self):
        """
        Calculates the Pearson correlation between average daily sentiment 
        and the lagged daily stock return (the next day's movement).
        """
        if self.merged_df is None:
            raise ValueError("Data must be aligned and aggregated before calculating correlation.")
            
        # Calculate correlation between today's average sentiment and tomorrow's return
        correlation = self.merged_df['avg_daily_sentiment'].corr(self.merged_df['lagged_return'])

        print("-" * 50)
        print(f"Correlation between TODAY's Avg Sentiment and TOMORROW's Return: {correlation:.4f}")
        
        # Also calculate correlation with same-day return for comparison
        same_day_correlation = self.merged_df['avg_daily_sentiment'].corr(self.merged_df['daily_return'])
        print(f"Correlation between TODAY's Avg Sentiment and TODAY's Return: {same_day_correlation:.4f}")
        print("-" * 50)

        # Visualize correlation (scatter plot)
        plt.figure(figsize=(8, 6))
        plt.scatter(self.merged_df['avg_daily_sentiment'], self.merged_df['lagged_return'], alpha=0.6, color='skyblue')
        plt.title(f"Sentiment vs. Lagged Stock Return (Correlation: {correlation:.4f})")
        plt.xlabel("Average Daily Sentiment (TextBlob Polarity)")
        plt.ylabel("Lagged Daily Return (%)")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        Path("reports/figures").mkdir(parents=True, exist_ok=True)
        plt.savefig("reports/figures/sentiment_correlation.png")
        plt.close()
        print("✅ Correlation scatter plot saved: reports/figures/sentiment_correlation.png")
        
        return correlation