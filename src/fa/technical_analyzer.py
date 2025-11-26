import talib as ta
import pynance as pn
import pandas as pd
import mplfinance as mpf
from pathlib import Path

class TechnicalAnalyzer:
    """
    Handles technical indicator calculation (using TA-Lib) and visualization.
    Accepts standard OHLCV column names (case-insensitive).
    """
    def __init__(self, df: pd.DataFrame, ticker: str):
        # Normalize column names to title-case (Open, High, Low, Close, Volume)
        df = df.copy()
        df.columns = df.columns.str.strip().str.title()
        
        # Validate required columns (now in title-case)
        required = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}. Found: {list(df.columns)}")
        
        self.df = df
        self.ticker = ticker
        Path("reports/indicators").mkdir(parents=True, exist_ok=True)
        print(f"✅ Technical Analyzer initialized for {self.ticker}.")

    def calculate_indicators(self):
        """Calculates key technical indicators using TA-Lib."""
        close = self.df['Close'].values
        high = self.df['High'].values
        low = self.df['Low'].values

        # Moving Averages
        self.df['SMA_50'] = ta.SMA(close, timeperiod=50)
        self.df['EMA_20'] = ta.EMA(close, timeperiod=20)
        
        # RSI
        self.df['RSI'] = ta.RSI(close, timeperiod=14)
        
        # MACD
        macd, macd_signal, _ = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.df['MACD'] = macd
        self.df['MACD_Signal'] = macd_signal
        
        print("✅ Technical indicators calculated.")
        return self.df

    def plot_indicators(self, save_name="technical_indicators.png"):
        """Plots candlestick + indicators using mplfinance."""
        df_plot = self.df.dropna(subset=['Open', 'High', 'Low', 'Close']).copy()
        
        # mplfinance requires exact column names: Open, High, Low, Close, Volume
        # (we already ensured this in __init__)
        
        # Addplots
        macd_plots = [
            mpf.make_addplot(df_plot['MACD'], panel=2, color='red', title='MACD'),
            mpf.make_addplot(df_plot['MACD_Signal'], panel=2, color='blue')
        ]
        
        rsi_plot = [
            mpf.make_addplot(df_plot['RSI'], panel=3, color='purple', ylim=[0, 100], title='RSI'),
            mpf.make_addplot([70]*len(df_plot), panel=3, color='gray', linestyle='--'),  # Overbought
            mpf.make_addplot([30]*len(df_plot), panel=3, color='gray', linestyle='--')   # Oversold
        ]

        mpf.plot(
            df_plot,
            type='line',
            style='charles',
            mav=(20, 50),       # Plots EMA_20 and SMA_50 on main chart
            volume=True,
            addplot=macd_plots + rsi_plot,
            title=f"Technical Analysis for {self.ticker}",
            ylabel='Price ($)',
            figsize=(14, 10),
            savefig=f"reports/indicators/{save_name}",
        )
        print(f"✅ Plot saved: reports/indicators/{save_name}")

    def get_pynance_metrics(self):
        """
        Compute financial metrics using PyNance-style log returns.
        
        """
        import numpy as np
        close = self.df['Close'].values
        
        # PyNance-style log returns 
        log_ret = np.diff(np.log(close))  # same as pn.data.logret()

        # Annualized volatility
        vol_ann = float(np.std(log_ret) * np.sqrt(252))

        # Max Drawdown
        cum_ret = np.cumprod(1 + log_ret)
        running_max = np.maximum.accumulate(cum_ret)
        drawdown = (cum_ret / running_max) - 1
        max_dd = float(np.min(drawdown))

        # Annualized return
        total_ret = (close[-1] / close[0]) - 1
        ann_ret = (1 + total_ret) ** (252 / len(self.df)) - 1

        return {
            'Ticker': self.ticker,
            'Annualized Return (PyNance-style)': f"{ann_ret:.2%}",
            'Annualized Volatility (PyNance-style)': f"{vol_ann:.2%}",
            'Max Drawdown (PyNance-style)': f"{max_dd:.2%}",
            'Avg Daily Volume': f"{int(self.df['Volume'].mean()):,}"
        }