import pandas as pd
from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(os.path.abspath(__file__)).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "yfinance_data" 
print(f"Stock loader look for data in: {DATA_DIR.resolve()}")

class StockDataset:
    """
    Load and validate stock price data.
    Expected columns: Date, Open, High, Low, Close, Volume
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.data_dir = DATA_DIR
        self.df = None
    
    def load(self, parse_dates=True):
        """Load CSV and ensure required columns."""
        path = self.data_dir / f"{self.ticker}.csv"
        
        # Check for directory existence and data file existence
        if not path.exists():
            raise FileNotFoundError(
                f"Stock data not found: {path}. Please ensure you have downloaded "
                f"the {self.ticker}.csv file into the expected directory."
            )
        
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip().str.title()  # ' OPEN ' → 'Open'
        if parse_dates and 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
        
        # Validate required columns
        required = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns in {self.ticker}: {missing}")
        
        # Rename columns to ALL CAPS for TA-Lib compatibility
        self.df = df[required].copy()
        self.df.columns = [col.upper() for col in required] 
        
        print(f"✅ Loaded {self.ticker}: {len(self.df)} rows, {self.df.index.min().date()} → {self.df.index.max().date()}")
        return self.df