"""
strategies.py
Logika sinyal perdagangan untuk 2 gaya trading:
1. Swing Trading (Jangka Menengah / Harian)
2. Day Trading (Jangka Pendek / Intraday)
"""

import pandas as pd
import numpy as np


def generate_swing_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strategi Swing Trading:
    - Filosofi: Trend-Following & Pullback on Uptrend.
    - Menangkap gelombang kenaikan harga beberapa hari hingga beberapa minggu.
    - Meminimalisir 'false breakout' dengan filter tren EMA 50/200 dan momentum RSI/MACD.
    """
    data = df.copy()
    
    # 1. Definisi Tren Utama (Uptrend / Downtrend)
    uptrend_condition = (data['Close'] > data['EMA_50']) & (data['EMA_21'] > data['EMA_50'])
    if 'SMA_200' in data.columns and not data['SMA_200'].isna().all():
        uptrend_condition = uptrend_condition & (data['Close'] > data['SMA_200'])
        
    data['Trend_Bullish'] = uptrend_condition
    
    # 2. Kondisi Sinyal BUY Swing
    # - Tren sedang Bullish
    # - RSI berada di area sehat (40 - 65): bukan overbought, sedang memantul dari koreksi
    # - MACD Histogram positif atau MACD Line memotong ke atas Signal Line
    # - Konfirmasi candle hijau (Close > Open)
    macd_bullish = (data['MACD_Hist'] > 0) | (data['MACD'] > data['MACD_Signal'])
    rsi_healthy = (data['RSI_14'] >= 40) & (data['RSI_14'] <= 68)
    green_candle = data['Close'] > data['Open']
    
    buy_condition = uptrend_condition & rsi_healthy & macd_bullish & green_candle
    
    # 3. Kondisi Sinyal SELL / TAKE PROFIT / CUT LOSS
    # - Harga menembus ke bawah EMA 50 (tren patah)
    # - Atau RSI sudah sangat overbought (> 75) mulai berbalik arah
    # - Atau MACD death cross di area tinggi
    macd_bearish = (data['MACD'] < data['MACD_Signal']) & (data['MACD_Hist'] < 0)
    rsi_overbought = data['RSI_14'] > 75
    trend_broken = data['Close'] < data['EMA_50']
    
    sell_condition = trend_broken | (rsi_overbought & (data['Close'] < data['Open'])) | (macd_bearish & (data['Close'] < data['EMA_21']))
    
    # Menghasilkan sinyal numerik: 1 = BUY, -1 = SELL, 0 = HOLD/WAIT
    data['Signal'] = 0
    data.loc[buy_condition, 'Signal'] = 1
    data.loc[sell_condition, 'Signal'] = -1
    
    # Tentukan Level Stop Loss & Take Profit yang Direkomendasikan
    # Menggunakan Volatilitas ATR (1.5x ATR)
    atr = data['ATR_14'].fillna(data['Close'] * 0.02)
    data['Suggested_SL'] = data['Close'] - (1.5 * atr)
    data['Suggested_TP1'] = data['Close'] + (2.0 * 1.5 * atr)  # RRR 1:2
    data['Suggested_TP2'] = data['Close'] + (3.0 * 1.5 * atr)  # RRR 1:3
    
    return data


def generate_daytrading_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strategi Day Trading / Intraday:
    - Filosofi: VWAP Breakout, Fast EMA Momentum (9 & 21), dan Bollinger Mean Reversion.
    - Posisi cepat dibuka dan ditutup pada sesi yang sama.
    """
    data = df.copy()
    
    # Pastikan VWAP tersedia
    vwap = data['VWAP'] if 'VWAP' in data.columns else data['EMA_21']
    
    # 1. Setup A: Momentum Breakout di atas VWAP
    # - Harga berada di atas VWAP
    # - Fast EMA 9 > EMA 21
    # - Volume di atas rata-rata (Volume Spike > 1.1x)
    # - RSI > 50 dan < 72
    above_vwap = data['Close'] > vwap
    fast_momentum = data['EMA_9'] > data['EMA_21']
    volume_surge = data['Vol_Ratio'] >= 1.1
    rsi_momentum = (data['RSI_14'] >= 50) & (data['RSI_14'] <= 72)
    
    breakout_buy = above_vwap & fast_momentum & volume_surge & rsi_momentum
    
    # 2. Setup B: Mean Reversion Bouncing (Pantulan dari Lower Bollinger Band)
    # - Harga menyentuh / di bawah Lower Band
    # - RSI jenuh jual (Oversold < 35) dan mulai memantul
    bounce_buy = (data['Low'] <= data['BB_Lower']) & (data['RSI_14'] <= 38) & (data['Close'] > data['Open'])
    
    combined_buy = breakout_buy | bounce_buy
    
    # 3. Kondisi Sinyal EXIT Intraday
    # - Harga jatuh di bawah VWAP
    # - Atau menyentuh Upper Bollinger Band dengan candle rejection
    # - Atau Fast EMA 9 memotong ke bawah EMA 21
    below_vwap = data['Close'] < vwap
    bb_hit_reversal = (data['High'] >= data['BB_Upper']) & (data['Close'] < data['Open'])
    fast_cross_down = data['EMA_9'] < data['EMA_21']
    
    sell_condition = below_vwap | bb_hit_reversal | fast_cross_down
    
    data['Signal'] = 0
    data.loc[combined_buy, 'Signal'] = 1
    data.loc[sell_condition, 'Signal'] = -1
    
    # Tentukan Level Stop Loss & Take Profit Day Trading
    # Day trading memakai SL lebih ketat: 1.0x ATR
    atr = data['ATR_14'].fillna(data['Close'] * 0.01)
    data['Suggested_SL'] = data['Close'] - (1.0 * atr)
    data['Suggested_TP1'] = data['Close'] + (1.5 * atr)  # RRR 1:1.5
    data['Suggested_TP2'] = data['Close'] + (2.5 * atr)  # RRR 1:2.5
    
    return data
