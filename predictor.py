"""
predictor.py
Modul Prediksi Arah Pergerakan Saham (Naik / Turun) menggunakan Machine Learning (Random Forest).
Memberikan probabilitas statistik arah harga berikutnya beserta fitur terpenting dan proyeksi nominal rentang harga.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def prepare_features(df: pd.DataFrame, forecast_horizon: int = 1):
    """
    Mempersiapkan fitur teknikal dan label target untuk Machine Learning.
    
    forecast_horizon: Berapa candle ke depan yang ingin diprediksi (1, 3, atau 5)
    Target: 1 jika harga penutupan N candle ke depan > harga saat ini, 0 jika sebaliknya.
    """
    data = df.copy()
    
    # 1. Feature Engineering
    # Return perubahan harga
    data['Return_1'] = data['Close'].pct_change(1)
    data['Return_3'] = data['Close'].pct_change(3)
    data['Return_5'] = data['Close'].pct_change(5)
    
    # Jarak persentase harga dari Moving Average
    data['Dist_EMA21'] = (data['Close'] - data['EMA_21']) / (data['EMA_21'] + 1e-10)
    data['Dist_EMA50'] = (data['Close'] - data['EMA_50']) / (data['EMA_50'] + 1e-10)
    
    # Rasio Volatilitas
    data['ATR_Pct'] = data['ATR_14'] / (data['Close'] + 1e-10)
    
    # Fitur daftar
    feature_cols = [
        'Return_1', 'Return_3', 'Return_5',
        'RSI_14', 'MACD_Hist',
        'Dist_EMA21', 'Dist_EMA50',
        'BB_PctB', 'BB_Width',
        'Vol_Ratio', 'ATR_Pct'
    ]
    
    # Label Target: Masa depan N candle
    future_close = data['Close'].shift(-forecast_horizon)
    data['Target'] = (future_close > data['Close']).astype(int)
    
    # Bersihkan NaN
    clean_data = data.dropna(subset=feature_cols)
    
    # Baris terakhir (tanpa target masa depan) adalah data 'Hari Ini' untuk diprediksi
    current_features = clean_data[feature_cols].iloc[-1:]
    
    # Data latihan (seluruh baris sebelum masa depan yang belum diketahui)
    training_data = clean_data.iloc[:-forecast_horizon].dropna(subset=['Target'])
    
    X = training_data[feature_cols]
    y = training_data['Target']
    
    return X, y, current_features, feature_cols


def train_and_predict(df: pd.DataFrame, forecast_horizon: int = 1) -> dict:
    """
    Melatih model Random Forest secara dinamis dan memprediksi arah serta rentang harga nominal candle ke depan.
    
    Returns:
        dict: Hasil analisis prediksi, probabilitas, akurasi, feature importance, dan proyeksi harga nominal.
    """
    current_close = float(df['Close'].iloc[-1])
    atr = float(df['ATR_14'].iloc[-1]) if ('ATR_14' in df.columns and not pd.isna(df['ATR_14'].iloc[-1])) else (current_close * 0.02)
    vol_step = atr * np.sqrt(forecast_horizon)
    
    default_projection = {
        "current_close": current_close,
        "target_price": current_close,
        "upper_bound": round(current_close + vol_step, 2),
        "lower_bound": round(current_close - vol_step, 2),
        "change_pct": 0.0
    }
    
    if len(df) < 60:
        return {
            "status": "warning",
            "message": "Data terlalu sedikit (minimal 60 baris) untuk melatih model Machine Learning yang valid.",
            "prediction": "NETRAL",
            "bullish_prob": 50.0,
            "bearish_prob": 50.0,
            "accuracy": 0.0,
            "top_features": [],
            "projected_prices": default_projection,
            "horizon": forecast_horizon
        }
        
    X, y, current_features, feature_cols = prepare_features(df, forecast_horizon=forecast_horizon)
    
    if len(X) < 40:
        return {
            "status": "warning",
            "message": "Data training tidak mencukupi setelah pembersihan indikator.",
            "prediction": "NETRAL",
            "bullish_prob": 50.0,
            "bearish_prob": 50.0,
            "accuracy": 0.0,
            "top_features": [],
            "projected_prices": default_projection,
            "horizon": forecast_horizon
        }
        
    # Split Data: 80% Training, 20% Out-of-Sample Testing
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    # Model Random Forest dengan regularisasi anti-overfitting
    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=5,
        min_samples_split=6,
        min_samples_leaf=4,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluasi akurasi out-of-sample (data yang belum pernah dilihat model)
    y_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred) if len(y_test) > 0 else 0.5
    
    # Latih ulang pada seluruh data yang tersedia untuk prediksi saat ini
    model.fit(X, y)
    
    # Prediksi untuk candle berikutnya
    probs = model.predict_proba(current_features)[0]
    
    # Tangani kasus jika kelas target hanya 1 kelas
    if len(probs) == 1:
        bullish_prob = 100.0 if model.classes_[0] == 1 else 0.0
    else:
        idx_bull = list(model.classes_).index(1) if 1 in model.classes_ else 0
        bullish_prob = float(probs[idx_bull] * 100)
        
    bearish_prob = 100.0 - bullish_prob
    
    if bullish_prob >= 58.0:
        direction = "NAIK (BULLISH)"
        target_price = current_close + (1.0 * vol_step)
        upper_bound = current_close + (1.6 * vol_step)
        lower_bound = current_close - (0.7 * vol_step)
    elif bearish_prob >= 58.0:
        direction = "TURUN (BEARISH)"
        target_price = current_close - (1.0 * vol_step)
        upper_bound = current_close + (0.7 * vol_step)
        lower_bound = current_close - (1.6 * vol_step)
    else:
        direction = "KONSOLIDASI / NETRAL"
        target_price = current_close
        upper_bound = current_close + (1.0 * vol_step)
        lower_bound = current_close - (1.0 * vol_step)
        
    expected_change_pct = ((target_price - current_close) / current_close) * 100.0
    
    # Feature Importance (Faktor apa yang paling berpengaruh)
    importances = model.feature_importances_
    feat_names = {
        'Return_1': 'Momentum 1-Bar Terakhir',
        'Return_3': 'Momentum 3-Bar Terakhir',
        'Return_5': 'Momentum 5-Bar Terakhir',
        'RSI_14': 'Kekuatan RSI (Oversold/Overbought)',
        'MACD_Hist': 'Momentum Akselerasi MACD',
        'Dist_EMA21': 'Jarak ke EMA-21 (Trend Menengah)',
        'Dist_EMA50': 'Jarak ke EMA-50 (Trend Utama)',
        'BB_PctB': 'Posisi Relatif Bollinger Bands',
        'BB_Width': 'Volatilitas Lebar Bollinger Bands',
        'Vol_Ratio': 'Lonjakan Volume Transaksi',
        'ATR_Pct': 'Persentase Volatilitas ATR'
    }
    
    sorted_features = sorted(
        zip([feat_names.get(f, f) for f in feature_cols], importances),
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        "status": "success",
        "prediction": direction,
        "bullish_prob": round(bullish_prob, 1),
        "bearish_prob": round(bearish_prob, 1),
        "accuracy": round(test_accuracy * 100, 1),
        "top_features": [(f, round(imp * 100, 1)) for f, imp in sorted_features[:4]],
        "horizon": forecast_horizon,
        "projected_prices": {
            "current_close": float(current_close),
            "target_price": float(round(target_price, 2)),
            "upper_bound": float(round(upper_bound, 2)),
            "lower_bound": float(round(lower_bound, 2)),
            "change_pct": float(round(expected_change_pct, 2))
        }
    }
