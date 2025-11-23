import pandas as pd

def load_news_data(filepath):
    df = pd.read_csv(filepath)
    
    # use format='mixed' for mixed tz/no-tz strings
    df['date'] = pd.to_datetime(df['date'], format='mixed', utc=True)
    
    df['headline_len'] = df['headline'].str.len()
    df['date_only'] = df['date'].dt.date
    df['hour_utc'] = df['date'].dt.hour
    df['hour_est'] = (df['hour_utc'] - 4) % 24
    df['day_of_week'] = df['date'].dt.day_name()
    
    return df


if __name__ == "__main__":
    print("Testing data_loader.py...")
    filepath = "../data/newsData/raw_analyst_ratings.csv"
    try:
        df = load_news_data(filepath)
        print(f" Success! Loaded {len(df)} rows.")
        print("\nSample:")
        print(df[['date', 'headline', 'publisher']].head(3))
    except Exception as e:
        print(f" Error: {e}")
        
        # inspect first 5 raw dates
        raw = pd.read_csv(filepath)
        print("First 5 raw 'date' values:")
        print(raw['date'].head())