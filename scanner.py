"""
scanner.py
Modul AI Market Scanner & Screener Otomatis.
Memindai puluhan saham secara multi-threaded untuk menemukan peluang terbaik secara instan.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from indicators import add_all_indicators
from strategies import generate_swing_signals
from data_loader import get_company_name

SCAN_PRESETS = {
    "🇮🇩 Saham Indonesia Modal Ringan (< Rp 1.000 / Lot Murah)": [
        "GOTO.JK", "BUMI.JK", "BRMS.JK", "ELSA.JK", "PWON.JK",
        "WIKA.JK", "PTPP.JK", "KIJA.JK", "DOID.JK", "BUKA.JK",
        "SCMA.JK", "MNCN.JK", "PSAB.JK", "SMRA.JK", "ACES.JK"
    ],
    "🇮🇩 Saham Indonesia Pertumbuhan (Mid-Cap Potensial)": [
        "MEDC.JK", "AKRA.JK", "CTRA.JK", "BSDE.JK", "SIDO.JK",
        "MYOR.JK", "BBTN.JK", "CPIN.JK", "INCO.JK", "ARTO.JK",
        "MBMA.JK", "PGEO.JK", "HRUM.JK", "INDY.JK", "TINS.JK", "ENRG.JK"
    ],
    "🇮🇩 Top 20 Saham Terbesar Indonesia (IHSG Blue Chip)": [
        "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "ASII.JK",
        "TLKM.JK", "AMMN.JK", "BREN.JK", "TPIA.JK", "BYAN.JK",
        "BRIS.JK", "GOTO.JK", "ICBP.JK", "INDF.JK", "UNVR.JK",
        "KLBF.JK", "ADRO.JK", "PTBA.JK", "MDKA.JK", "ANTM.JK"
    ],
    "🇮🇩 Sektor Tambang & Energi Indonesia": [
        "ADRO.JK", "PTBA.JK", "ITMG.JK", "BYAN.JK", "PGAS.JK",
        "ANTM.JK", "INCO.JK", "MDKA.JK", "MEDC.JK", "AMMN.JK",
        "BUMI.JK", "MBMA.JK", "HRUM.JK", "INDY.JK", "DOID.JK"
    ],
    "🇮🇩 Sektor Perbankan & Finansial Indonesia": [
        "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "BRIS.JK",
        "BBTN.JK", "BDMN.JK", "ARTO.JK", "BTPS.JK", "BTPN.JK"
    ],
    "🇺🇸 Saham AS Terjangkau (Budget-Friendly < $30)": [
        "GRAB", "NIO", "CLOV", "LCID", "SNAP",
        "AUR", "AAL", "F", "NU", "RIVN",
        "SOFI", "CCL", "WBD", "PFE"
    ],
    "🌐 Saham Pertumbuhan Global (Asia & US Growth)": [
        "SE", "BABA", "TSM", "AMD", "COIN",
        "ARM", "PLTR", "HOOD", "INTC", "U", "RBLX", "BIDU"
    ],
    "🇺🇸 Wall Street Megacap & Big Tech": [
        "AAPL", "NVDA", "MSFT", "GOOGL", "AMZN",
        "META", "TSLA", "AMD", "PLTR", "AVGO",
        "NFLX", "CRM", "INTC", "QCOM", "TXN"
    ],
    "🇺🇸 AI, Semikonduktor & High Growth": [
        "NVDA", "AMD", "PLTR", "TSM", "ARM",
        "AVGO", "SMCI", "COIN", "CRWD", "SNOW"
    ]
}


def scan_market(preset_name: str, period: str = "6mo") -> pd.DataFrame:
    """
    Memindai daftar saham dalam preset tertentu secara batch/multi-threaded.
    
    Returns:
        pd.DataFrame: Tabel peringkat saham dengan sinyal, volume surge, RSI, dan skor peluang.
    """
    tickers = SCAN_PRESETS.get(preset_name, SCAN_PRESETS["🇮🇩 Top 20 Saham Terbesar Indonesia (IHSG Blue Chip)"])
    
    # Download data secara massal (sangat cepat via multi-threading)
    try:
        raw_data = yf.download(tickers, period=period, interval="1d", group_by="ticker", progress=False, threads=True)
    except Exception as e:
        return pd.DataFrame()
        
    results = []
    
    for ticker in tickers:
        try:
            if len(tickers) == 1:
                df_ticker = raw_data.copy()
            else:
                if isinstance(raw_data.columns, pd.MultiIndex):
                    if ticker in raw_data.columns.get_level_values(0):
                        df_ticker = raw_data[ticker].dropna(subset=['Close'])
                    elif ticker in raw_data.columns.get_level_values(1):
                        df_ticker = raw_data.xs(ticker, level=1, axis=1).dropna(subset=['Close'])
                    else:
                        continue
                else:
                    df_ticker = raw_data.copy().dropna(subset=['Close'])
                
            if len(df_ticker) < 20:
                continue
                
            # Tambahkan indikator teknikal & sinyal
            df_ind = add_all_indicators(df_ticker)
            df_sig = generate_swing_signals(df_ind)
            
            latest = df_sig.iloc[-1]
            prev = df_sig.iloc[-2]
            
            close = float(latest['Close'])
            # Filter ketat sesuai batas harga di judul preset
            if "< $30" in preset_name and close >= 30.0:
                continue
            if "< Rp 1.000" in preset_name and close >= 1000.0:
                continue

            prev_close = float(prev['Close'])
            pct_change = ((close - prev_close) / prev_close) * 100.0
            
            rsi = float(latest['RSI_14'])
            vol_ratio = float(latest.get('Vol_Ratio', 1.0))
            signal = int(latest.get('Signal', 0))
            
            # Deteksi kriteria tren
            above_ema50 = close > float(latest['EMA_50'])
            golden_cross = float(latest['EMA_21']) > float(latest['EMA_50'])
            
            # Hitung Skor Peluang Trading (0 - 100)
            score = 50
            if signal == 1:
                score += 25
            elif signal == -1:
                score -= 20
                
            if above_ema50:
                score += 10
            if golden_cross:
                score += 5
                
            # RSI ideal untuk swing entry (45 - 65)
            if 45 <= rsi <= 65:
                score += 10
            elif rsi < 30:
                score += 5  # potensi oversold reversal
            elif rsi > 70:
                score -= 15  # sudah rawan profit taking
                
            # Volume surge
            if vol_ratio >= 1.3:
                score += 10
            elif vol_ratio >= 1.1:
                score += 5
                
            score = max(5, min(99, score))
            
            # Status rekomendasi
            if score >= 80:
                status = "🟢 STRONG BUY"
            elif score >= 65:
                status = "🟢 BUY (POTENSIAL)"
            elif score <= 35:
                status = "🔴 EXIT / DOWNTREND"
            else:
                status = "⚪ WAIT & SEE"
                
            is_idx_stock = ticker.endswith('.JK')
            modal_1lot_str = f"Rp {close * 100:,.0f}" if is_idx_stock else f"${close:,.2f}"
            modal_1lot_val = close * 100 if is_idx_stock else close

            results.append({
                "Ticker": ticker,
                "Nama Perusahaan": get_company_name(ticker),
                "Harga Terakhir": close,
                "Modal 1 Lot": modal_1lot_str,
                "Modal_Val": modal_1lot_val,
                "Perubahan (%)": round(pct_change, 2),
                "Rekomendasi": status,
                "Skor Peluang": score,
                "RSI (14)": round(rsi, 1),
                "Volume Surge": f"{vol_ratio:.1f}x",
                "Tren": "Uptrend" if above_ema50 else "Downtrend",
                "Target TP1": round(float(latest['Suggested_TP1']), 2),
                "Stop Loss": round(float(latest['Suggested_SL']), 2)
            })
        except Exception:
            continue
            
    if not results:
        return pd.DataFrame()
        
    df_res = pd.DataFrame(results)
    # Urutkan berdasarkan skor peluang tertinggi
    df_res = df_res.sort_values(by="Skor Peluang", ascending=False).reset_index(drop=True)
    return df_res
