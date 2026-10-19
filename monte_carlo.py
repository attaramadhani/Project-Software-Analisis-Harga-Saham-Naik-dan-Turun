"""
monte_carlo.py
Modul Simulasi Stokastik Monte Carlo (1.000 Skenario Masa Depan) & Value at Risk (VaR).
Standar pemodelan risiko kuantitatif yang digunakan oleh institusi keuangan Wall Street & Hedge Fund.
"""

import numpy as np
import pandas as pd


def run_monte_carlo_simulation(
    df: pd.DataFrame,
    days_ahead: int = 30,
    num_simulations: int = 1000,
    tp_price: float = None,
    sl_price: float = None
) -> dict:
    """
    Menjalankan simulasi stokastik Geometric Brownian Motion (GBM) sebanyak 1.000 jalur.
    
    Parameters:
        df (pd.DataFrame): Dataframe harga saham (harus ada kolom 'Close')
        days_ahead (int): Berapa hari ke depan yang disimulasikan (default: 30 hari)
        num_simulations (int): Jumlah jalur skenario acak (default: 1.000 jalur)
        tp_price (float): Level Target Profit untuk diuji probabilitasnya
        sl_price (float): Level Stop Loss untuk diuji probabilitasnya
        
    Returns:
        dict: Hasil simulasi, kurva persentil (5%, 50%, 95%), VaR 95%, dan probabilitas TP vs SL.
    """
    close_prices = df['Close'].dropna()
    current_price = float(close_prices.iloc[-1])
    
    # Hitung logarithmic returns harian
    log_returns = np.log(close_prices / close_prices.shift(1)).dropna()
    
    # Estimasi parameter drift (mu) dan volatilitas (sigma)
    mu = log_returns.mean()
    sigma = log_returns.std()
    
    # Matriks acak standar normal (N(0, 1))
    np.random.seed(42)  # agar hasil konsisten untuk ticker yang sama
    daily_shocks = np.random.normal(size=(days_ahead, num_simulations))
    
    # Pertumbuhan per hari dengan formula Geometric Brownian Motion (GBM):
    # drift_term = (mu - 0.5 * sigma^2)
    drift = mu - (0.5 * (sigma ** 2))
    growth_factors = np.exp(drift + (sigma * daily_shocks))
    
    # Hitung jalur harga kumulatif
    simulated_paths = np.zeros((days_ahead + 1, num_simulations))
    simulated_paths[0] = current_price
    
    for t in range(1, days_ahead + 1):
        simulated_paths[t] = simulated_paths[t - 1] * growth_factors[t - 1]
        
    # Ambil nilai akhir (Terminal Prices di hari ke-T)
    terminal_prices = simulated_paths[-1]
    terminal_returns = (terminal_prices - current_price) / current_price
    
    # 1. Hitung Persentil Kunci untuk Kerucut Probabilitas (Confidence Cone)
    p5_path = np.percentile(simulated_paths, 5, axis=1)    # Skenario Buruk (Bearish 5th percentile)
    p50_path = np.percentile(simulated_paths, 50, axis=1)  # Skenario Median (Expected Path)
    p95_path = np.percentile(simulated_paths, 95, axis=1)  # Skenario Terbaik (Bullish 95th percentile)
    
    # 2. Value at Risk (VaR 95% dan 99%)
    # Mengukur kerugian maksimal yang diperkirakan terjadi pada tingkat keyakinan 95%
    var_95_pct = abs(float(np.percentile(terminal_returns, 5))) * 100.0
    var_95_amount = current_price * (var_95_pct / 100.0)
    
    expected_median_price = float(np.median(terminal_prices))
    expected_mean_price = float(np.mean(terminal_prices))
    best_case_price = float(np.percentile(terminal_prices, 95))
    worst_case_price = float(np.percentile(terminal_prices, 5))
    
    # 3. Probabilitas Kena Target Profit (TP) vs Kena Stop Loss (SL)
    prob_tp_first = 50.0
    prob_sl_first = 50.0
    neither_hit = 0.0
    
    if tp_price is not None and sl_price is not None and sl_price < current_price < tp_price:
        hit_tp_count = 0
        hit_sl_count = 0
        
        for sim in range(num_simulations):
            path = simulated_paths[:, sim]
            # Cari hari pertama kena TP atau SL
            tp_idx = np.where(path >= tp_price)[0]
            sl_idx = np.where(path <= sl_price)[0]
            
            first_tp_day = tp_idx[0] if len(tp_idx) > 0 else 999999
            first_sl_day = sl_idx[0] if len(sl_idx) > 0 else 999999
            
            if first_tp_day < first_sl_day:
                hit_tp_count += 1
            elif first_sl_day < first_tp_day:
                hit_sl_count += 1
                
        total_decided = hit_tp_count + hit_sl_count
        if total_decided > 0:
            prob_tp_first = round((hit_tp_count / num_simulations) * 100.0, 1)
            prob_sl_first = round((hit_sl_count / num_simulations) * 100.0, 1)
            neither_hit = round(100.0 - prob_tp_first - prob_sl_first, 1)
            
    # Siapkan DataFrame kurva persentil
    days_index = list(range(days_ahead + 1))
    cone_df = pd.DataFrame({
        "Hari": days_index,
        "Worst_5th": p5_path,
        "Median_50th": p50_path,
        "Best_95th": p95_path
    })
    
    # Sampel 30 jalur acak untuk visualisasi estetis 'spaghetti chart'
    sample_paths = simulated_paths[:, :30]
    
    return {
        "status": "success",
        "current_price": current_price,
        "days_ahead": days_ahead,
        "num_simulations": num_simulations,
        "expected_median_price": round(expected_median_price, 2),
        "expected_mean_price": round(expected_mean_price, 2),
        "best_case_p95": round(best_case_price, 2),
        "worst_case_p5": round(worst_case_price, 2),
        "var_95_pct": round(var_95_pct, 2),
        "var_95_amount": round(var_95_amount, 2),
        "prob_tp_first": prob_tp_first,
        "prob_sl_first": prob_sl_first,
        "neither_hit": neither_hit,
        "cone_df": cone_df,
        "sample_paths": sample_paths
    }
