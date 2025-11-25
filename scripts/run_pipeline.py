import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)


from src import DataLoader
from src.eda import (
    EDA_Descriptive,
    EDA_Text,
    EDA_TimeSeries,
    EDA_Publisher
)

def main():
    loader = DataLoader("../data/raw_analyst_ratings.csv")
    df = loader.load()

    eda_desc = EDA_Descriptive(df)
    eda_text = EDA_Text(df)
    eda_ts = EDA_TimeSeries(df)
    eda_pub = EDA_Publisher(df)

    eda_desc.headline_length_stats()
    eda_desc.publisher_activity()

    print(eda_text.get_top_phrases())
    eda_text.plot_wordcloud()

    eda_ts.daily_volume_analysis()
    eda_ts.hourly_pattern_analysis()
    eda_ts.weekday_analysis()

    eda_pub.top_publishers()
    eda_pub.content_analysis()

if __name__ == "__main__":
    main()
