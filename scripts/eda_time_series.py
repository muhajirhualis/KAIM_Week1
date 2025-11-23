# scripts/eda_time_series.py
import pandas as pd
import matplotlib.pyplot as plt

def daily_volume_analysis(df, window=7):
    """
    Analyze daily article volume and detect spikes.
    
    Args:
        df: DataFrame with 'date_only' column (from data_loader)
        window: rolling window (days) for smoothing
    
    Returns:
        daily_counts: Series of articles per day
    """
    daily_counts = df.groupby('date_only').size()
    
    # Plot
    plt.figure(figsize=(14, 5))
    daily_counts.plot(label='Daily Volume', color='steelblue', alpha=0.7)
    
    # Add 7-day rolling mean to smooth noise
    rolling = daily_counts.rolling(window=window).mean()
    rolling.plot(label=f'{window}-Day Rolling Mean', color='crimson', linewidth=2)
    
    plt.title('Daily News Publication Volume')
    plt.ylabel('Number of Articles')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Highlight top 5 spike days
    top_spikes = daily_counts.nlargest(5)
    print(" Top 5 Highest-Volume Days:")
    for date, count in top_spikes.items():
        print(f"  {date} → {int(count):,} articles")
    
    return daily_counts


def hourly_pattern_analysis(df):
    """
    Analyze publishing hour (in EST) — critical for trading systems.
    """
    hourly = df['hour_est'].value_counts().sort_index()
    
    plt.figure(figsize=(10, 5))
    hourly.plot(kind='bar', color='seagreen', width=0.8)
    plt.title('Hourly News Publication Pattern (EST)')
    plt.xlabel('Hour of Day (EST)')
    plt.ylabel('Number of Articles')
    plt.xticks(range(0, 24), [f"{h}:00" for h in range(24)], rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    peak_hour = hourly.idxmax()
    peak_count = hourly.max()
    print(f" Peak publishing hour: {peak_hour}:00 EST ({peak_count:,} articles)")
    print(f"   → Likely aligned with market open (9:30 AM EST)")


def weekday_analysis(df):
    """
    Check if weekends have less news (they should!).
    """
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_counts = df['day_of_week'].value_counts().reindex(order)
    
    plt.figure(figsize=(8, 4))
    weekday_counts.plot(kind='bar', color='lightcoral')
    plt.title('News Volume by Day of Week')
    plt.ylabel('Articles')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    weekend_ratio = (weekday_counts['Saturday'] + weekday_counts['Sunday']) / weekday_counts.sum()
    print(f" Weekend (Sat+Sun) share: {weekend_ratio:.1%} of total news.")
    
def align_with_market_events(df, event_dates=None):
    """
    Check news volume on known market event days.
    Helps answer: 'Are spikes related to real market-moving events?'
    
    Args:
        df: DataFrame with 'date_only' (date-only, not datetime)
        event_dates: dict like {'2020-03-23': 'Fed Emergency Cut'}
    
    Returns:
        dict of event_dates (for later use in reports)
    """
    if event_dates is None:
        # Key 2020–2021 events (dataset appears ~2020–2021 based on samples)
        event_dates = {
            "2020-03-23": "Fed $2T Stimulus Announcement",
            "2020-06-10": "Fed Holds Rates, QE Extended",
            "2020-08-27": "Powell: Avg Inflation Targeting",
            "2020-11-09": "Pfizer Vaccine Efficacy (90%)",
            "2021-01-27": "Fed Meeting (Post-GameStop Volatility)",
            "2021-03-17": "Fed Raises Dot Plot, Yields Spike",
        }

    # Ensure 'date_only' is date type (not string)
    if not pd.api.types.is_datetime64_any_dtype(df['date_only']):
        df = df.copy()
        df['date_only'] = pd.to_datetime(df['date_only']).dt.date

    daily_volume = df.groupby('date_only').size()
    
    print("\n News Volume on Key Market Event Days:")
    print("-" * 50)
    for date_str, event in event_dates.items():
        event_date = pd.to_datetime(date_str).date()
        vol = daily_volume.get(event_date, 0)
        print(f"{date_str} | {int(vol):>5} articles | {event}")
    
    # Optional: highlight days with >2σ volume
    mean_vol = daily_volume.mean()
    std_vol = daily_volume.std()
    threshold = mean_vol + 2 * std_vol
    
    high_vol_events = [
        (date_str, event) 
        for date_str, event in event_dates.items()
        if daily_volume.get(pd.to_datetime(date_str).date(), 0) > threshold
    ]
    
    if high_vol_events:
        print(f"\n🚨 High-impact events (volume > {threshold:.0f}):")
        for date_str, event in high_vol_events:
            print(f"  → {date_str}: {event}")
    
    return event_dates