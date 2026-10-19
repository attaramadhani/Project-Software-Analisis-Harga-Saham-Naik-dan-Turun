"""
indicators.py
Modul perhitungan indikator teknikal murni menggunakan Pandas dan NumPy.
Cepat, tanpa ketergantungan library C (seperti TA-Lib yang rumit di-install di Windows).
"""

import pandas as pd
import numpy as np


def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    """Menghitung Exponential Moving Average (EMA)."""
    return series.ewm(span=span, adjust=False).mean()


def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    """Menghitung Simple Moving Average (SMA)."""
    return series.rolling(window=window).mean()


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Menghitung Relative Strength Index (RSI).
    Formula standar Wilder's RSI.
    """
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    
    # Wilder's Smoothing
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """
    Menghitung Moving Average Convergence Divergence (MACD).
    Returns: (macd_line, signal_line, histogram)
    """
    fast_ema = calculate_ema(series, fast)
    slow_ema = calculate_ema(series, slow)
    macd_line = fast_ema - slow_ema
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(series: pd.Series, window: int = 20, num_std: float = 2.0):
    """
    Menghitung Bollinger Bands.
    Returns: (upper_band, middle_band, lower_band, band_width, pct_b)
    """
    middle_band = calculate_sma(series, window)
    std = series.rolling(window=window).std()
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    band_width = (upper_band - lower_band) / (middle_band + 1e-10)
    pct_b = (series - lower_band) / (upper_band - lower_band + 1e-10)
    return upper_band, middle_band, lower_band, band_width, pct_b


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Menghitung Average True Range (ATR).
    Pondasi utama untuk menentukan level Stop Loss yang dinamis berdasarkan volatilitas pasar.
    """
    high = df['High']
    low = df['Low']
    close_prev = df['Close'].shift(1)
    
    tr1 = high - low
    tr2 = (high - close_prev).abs()
    tr3 = (low - close_prev).abs()
    
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    return atr


def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """
    Menghitung Volume Weighted Average Price (VWAP).
    Sangat esensial untuk strategi Day Trading / Intraday.
    """
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3.0
    tp_v = typical_price * df['Volume']
    
    # Jika data memiliki tanggal harian di index (intraday), kelompokkan per hari
    try:
        if isinstance(df.index, pd.DatetimeIndex):
            dates = df.index.date
            cum_tp_v = tp_v.groupby(dates).cumsum()
            cum_v = df['Volume'].groupby(dates).cumsum()
            vwap = cum_tp_v / (cum_v + 1e-10)
            return vwap
    except Exception:
        pass
        
    # Fallback rolling/cumulative jika bukan intraday
    return tp_v.cumsum() / (df['Volume'].cumsum() + 1e-10)


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menambahkan seluruh indikator teknikal ke DataFrame.
    """
    data = df.copy()
    close = data['Close']
    
    # Moving Averages
    data['EMA_9'] = calculate_ema(close, 9)
    data['EMA_21'] = calculate_ema(close, 21)
    data['EMA_50'] = calculate_ema(close, 50)
    data['EMA_200'] = calculate_ema(close, 200)
    data['SMA_20'] = calculate_sma(close, 20)
    data['SMA_200'] = calculate_sma(close, 200)
    
    # Momentum
    data['RSI_14'] = calculate_rsi(close, 14)
    data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = calculate_macd(close)
    
    # Volatilitas
    data['BB_Upper'], data['BB_Mid'], data['BB_Lower'], data['BB_Width'], data['BB_PctB'] = calculate_bollinger_bands(close)
    data['ATR_14'] = calculate_atr(data, 14)
    
    # Intraday
    data['VWAP'] = calculate_vwap(data)
    
    # Volume Analisis
    data['Vol_SMA20'] = calculate_sma(data['Volume'], 20)
    data['Vol_Ratio'] = data['Volume'] / (data['Vol_SMA20'] + 1e-10)
    
    return data
