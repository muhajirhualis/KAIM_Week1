# import libraries
import pandas as pd
import matplotlib.pyplot as plt

def headline_length_stats(df):
    """Compute and display headline length statistics."""
    stats = df['headline_len'].describe()
    print("Headline Length Statistics:")
    print(stats.round(2))
    
    # Plot
    plt.figure(figsize=(8,4))
    df['headline_len'].hist(bins=40, color='skyblue', edgecolor='black')
    plt.title('Distribution of Headline Lengths (Characters)')
    plt.xlabel('Characters')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.3)
    plt.show()
    
    return stats

def publisher_activity(df, top_n=15):
    """Show top publishers and plot activity."""
    counts = df['publisher'].value_counts()
    print(f"\n Top {top_n} Publishers (out of {counts.nunique()} unique):")
    print(counts.head(top_n))
    
    plt.figure(figsize=(10,6))
    counts.head(top_n).plot(kind='barh', color='lightcoral')
    plt.gca().invert_yaxis()
    plt.title(f'Top {top_n} Publishers by Article Count')
    plt.xlabel('Number of Articles')
    plt.tight_layout()
    plt.show()
    
    return counts

def time_patterns(df):
    """Analyze daily & hourly publication patterns."""
    # Daily
    daily = df.groupby('date_only').size()
    
    # Hourly (EST)
    hourly = df['hour_est'].value_counts().sort_index()
    
    # Plot side by side
    fig, ax = plt.subplots(1, 2, figsize=(14,5))
    
    daily.plot(ax=ax[0], title='Daily News Volume (All Time)', color='steelblue')
    ax[0].set_ylabel('Articles')
    ax[0].grid(True, alpha=0.3)
    
    hourly.plot(kind='bar', ax=ax[1], color='seagreen', width=0.8)
    ax[1].set_title('Hourly Publication Pattern (EST)')
    ax[1].set_xlabel('Hour of Day (EST)')
    ax[1].set_ylabel('Articles')
    ax[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return daily, hourly