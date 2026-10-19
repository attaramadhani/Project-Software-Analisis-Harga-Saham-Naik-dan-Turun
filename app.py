"""
app.py
Aplikasi Web Dashboard Analisis 360° Saham Global Tercanggih
Menggabungkan Teknikal + Fundamental + Berita + AI Machine Learning + Market Scanner + Monte Carlo + Paper Trading + Manajemen Risiko.
Dirancang dengan antarmuka yang bersih, rapi, dan menyertakan nama perusahaan lengkap di setiap tampilan.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_loader import (
    POPULAR_TICKERS,
    load_stock_data,
    get_ticker_info,
    clean_ticker_symbol,
    get_company_name
)
from indicators import add_all_indicators
from strategies import generate_swing_signals, generate_daytrading_signals
from predictor import train_and_predict
from risk_manager import calculate_risk_plan
from backtester import run_backtest
from fundamentals import get_fundamental_data
from news_loader import get_stock_news, get_macro_news
from scanner import scan_market, SCAN_PRESETS
from monte_carlo import run_monte_carlo_simulation
from paper_trading import load_portfolio, execute_buy, execute_sell, reset_portfolio
from glossary import (
    render_header_guide,
    render_scanner_guide,
    render_chart_guide,
    render_ai_guide,
    render_monte_carlo_guide,
    render_fundamental_guide,
    render_news_guide,
    render_risk_guide,
    render_paper_trading_guide,
    render_backtest_guide,
    render_interactive_glossary
)

# ==========================================
# Konfigurasi Tampilan Halaman Streamlit
# ==========================================
st.set_page_config(
    page_title="AI Stock 360° Institutional Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling CSS agar tampilan rapi, elegan, dan enak dipandang
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #9E9E9E;
        margin-bottom: 0.9rem;
    }
    .composite-banner {
        background: linear-gradient(90deg, rgba(30,136,229,0.15) 0%, rgba(100,255,218,0.08) 100%);
        border: 1px solid rgba(30, 136, 229, 0.4);
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .metric-card {
        background-color: rgba(30, 136, 229, 0.08);
        border: 1px solid rgba(30, 136, 229, 0.2);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .signal-buy {
        background-color: rgba(46, 125, 50, 0.15);
        border: 1px solid #4CAF50;
        border-radius: 8px;
        padding: 10px 16px;
        color: #81C784;
        font-weight: bold;
    }
    .signal-sell {
        background-color: rgba(198, 40, 40, 0.15);
        border: 1px solid #E53935;
        border-radius: 8px;
        padding: 10px 16px;
        color: #E57373;
        font-weight: bold;
    }
    .signal-wait {
        background-color: rgba(117, 117, 117, 0.15);
        border: 1px solid #9E9E9E;
        border-radius: 8px;
        padding: 10px 16px;
        color: #BDBDBD;
        font-weight: bold;
    }
    .news-card {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 10px;
    }
    .company-badge {
        background-color: rgba(30, 136, 229, 0.12);
        border: 1px solid rgba(30, 136, 229, 0.3);
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 8px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# Sidebar: Kontrol & Pengaturan Parameter
# ==========================================
st.sidebar.markdown("## 🔍 Pemilihan Saham")

input_mode = st.sidebar.radio(
    "Metode Input Saham:",
    options=["✏️ Ketik Kode Bebas (Seluruh Dunia)", "📋 Pilih dari Katalog (70+ Saham)"],
    index=0
)

if "Ketik Kode Bebas" in input_mode:
    custom_input = st.sidebar.text_input(
        "Ketik Simbol / Kode Saham:",
        value="BBCA",
        help="Contoh Saham Indonesia: BBCA, BBRI, GOTO, ANTM, BREN, TLKM. Contoh Saham Luar: AAPL, NVDA, TSLA, PLTR, TSM, BTC-USD."
    )
    selected_ticker = clean_ticker_symbol(custom_input)
else:
    market_category = st.sidebar.selectbox(
        "Kategori Pasar:",
        options=list(POPULAR_TICKERS.keys())
    )
    ticker_dict = POPULAR_TICKERS[market_category]
    ticker_options = list(ticker_dict.keys())
    selected_ticker = st.sidebar.selectbox(
        "Pilih Saham:",
        options=ticker_options,
        format_func=lambda x: f"{x} - {ticker_dict[x]}"
    )

# Tampilkan Kotak Informasi Nama Perusahaan di Sidebar
full_company_name = get_company_name(selected_ticker)
st.sidebar.markdown(f"""
<div class='company-badge'>
    <span style='color:#9E9E9E; font-size:0.75rem; text-transform:uppercase;'>🏢 Perusahaan Terpilih:</span><br>
    <b style='color:#64FFDA; font-size:0.95rem;'>{full_company_name}</b><br>
    <span style='color:#BDBDBD; font-size:0.8rem;'>Kode Saham: <code style='color:#FFA726;'>{selected_ticker}</code></span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Pemilihan Gaya Trading
st.sidebar.markdown("## 🎯 Gaya Trading")
trading_style = st.sidebar.radio(
    "Pilih Gaya Analisis:",
    options=["Swing Trading (Harian / Jangka Menengah)", "Day Trading (Intraday / Jangka Pendek)"],
    index=0
)
is_swing = "Swing Trading" in trading_style

if is_swing:
    st.sidebar.info("💡 **Swing Trading**: Menganalisis tren harian. Posisi ditahan beberapa hari s/d minggu.")
    period = st.sidebar.selectbox("Rentang Data Historis", options=["6mo", "1y", "2y", "5y"], index=1)
    interval = st.sidebar.selectbox("Timeframe Candle", options=["1d", "1wk"], index=0)
else:
    st.sidebar.info("⚡ **Day Trading**: Menganalisis momentum menit. Posisi ditutup di hari yang sama.")
    period = st.sidebar.selectbox("Rentang Data Intraday", options=["5d", "1mo", "60d"], index=1)
    interval = st.sidebar.selectbox("Timeframe Candle", options=["5m", "15m", "30m", "1h"], index=1)

st.sidebar.markdown("---")
st.sidebar.markdown("## 👁️ Pengaturan Grafik")
show_ema = st.sidebar.checkbox("Moving Averages (EMA)", value=True)
show_bb = st.sidebar.checkbox("Bollinger Bands", value=True)
show_vwap = st.sidebar.checkbox("VWAP", value=not is_swing)
show_levels = st.sidebar.checkbox("Garis SL & TP Terkini", value=True)


# ==========================================
# Pengunduhan & Pemrosesan Data
# ==========================================
@st.cache_data(ttl=120)
def fetch_and_process(ticker, p, i):
    raw_df = load_stock_data(ticker, period=p, interval=i)
    df_ind = add_all_indicators(raw_df)
    return df_ind

@st.cache_data(ttl=600)
def fetch_fundamentals(ticker):
    return get_fundamental_data(ticker)

@st.cache_data(ttl=300)
def fetch_news(ticker):
    return get_stock_news(ticker), get_macro_news()

try:
    with st.spinner(f"Menghubungkan data {full_company_name} ({selected_ticker})..."):
        df = fetch_and_process(selected_ticker, period, interval)
        info = get_ticker_info(selected_ticker)
        fund = fetch_fundamentals(selected_ticker)
        stock_news, macro_news = fetch_news(selected_ticker)
except Exception as e:
    st.error(f"Gagal mengambil data untuk ticker '{selected_ticker}': {e}")
    st.info("Tips: Pastikan kode saham benar. Untuk saham Indonesia gunakan 4 huruf (misal BBCA atau BBCA.JK).")
    st.stop()

# Terapkan Sinyal Trading
if is_swing:
    df = generate_swing_signals(df)
else:
    df = generate_daytrading_signals(df)

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest

is_idx = selected_ticker.endswith(".JK")
currency_symbol = "Rp" if is_idx else "$"

price_diff = latest['Close'] - prev['Close']
price_pct = (price_diff / prev['Close']) * 100.0 if prev['Close'] > 0 else 0.0

# ==========================================
# Hitung Skor Komposit 360° (Composite Grade)
# ==========================================
tech_score = 50
curr_sig = latest.get('Signal', 0)
if curr_sig == 1:
    tech_score += 25
elif curr_sig == -1:
    tech_score -= 20
if latest['Close'] > latest['EMA_50']:
    tech_score += 15
if 40 <= latest['RSI_14'] <= 65:
    tech_score += 10
tech_score = max(5, min(99, tech_score))

pos_news = sum(1 for n in stock_news if "POSITIF" in n.get('sentiment', {}).get('label', ''))
neg_news = sum(1 for n in stock_news if "WASPADA" in n.get('sentiment', {}).get('label', ''))
news_score = 75 if pos_news > neg_news else (35 if neg_news > pos_news else 55)

fund_score = fund.get('score', 50)
composite_score = round((0.40 * tech_score) + (0.40 * fund_score) + (0.20 * news_score), 1)

if composite_score >= 82:
    composite_grade = "A+ (EXCELLENT / PRIME SETUP)"
    grade_color = "#00E676"
elif composite_score >= 70:
    composite_grade = "A (VERY GOOD / STRONG ACCUMULATION)"
    grade_color = "#26A69A"
elif composite_score >= 55:
    composite_grade = "B (MODERATE / SELECTIVE BUY)"
    grade_color = "#29B6F6"
elif composite_score >= 42:
    composite_grade = "C (WAIT & SEE / NETRAL)"
    grade_color = "#FFD54F"
else:
    composite_grade = "D (HIGH RISK / AVOID)"
    grade_color = "#FF5252"

# ==========================================
# Header & Ringkasan 360°
# ==========================================
st.markdown(f"""
<div class='main-header'>
    🏢 {full_company_name} <span style='font-size:1.3rem; color:#64B5F6; font-weight:normal;'>({selected_ticker})</span>
</div>
""", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>Sektor: <b>{fund.get('sector', info.get('sector', 'N/A'))}</b> | Industri: <b>{fund.get('industry', info.get('industry', 'N/A'))}</b> | Mode: <b>{trading_style}</b></div>", unsafe_allow_html=True)

# Master Composite Grade Banner
st.markdown(f"""
<div class='composite-banner'>
    <div>
        <span style='color:#BDBDBD; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;'>🏆 360° Overall Investment & Trading Grade</span>
        <h3 style='margin:3px 0 0 0; color:{grade_color}; font-weight:800;'>{composite_grade}</h3>
    </div>
    <div style='text-align:right;'>
        <span style='color:#BDBDBD; font-size:0.8rem;'>Skor Terpadu:</span>
        <h3 style='margin:3px 0 0 0; color:#FFFFFF;'>{composite_score} <span style='font-size:1.0rem; color:#888;'>/ 100</span></h3>
    </div>
</div>
""", unsafe_allow_html=True)

# Metric Bar Utama
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric("Harga Terakhir", f"{currency_symbol} {latest['Close']:,.2f}", f"{price_diff:+,.2f} ({price_pct:+.2f}%)")
col_m2.metric("Skor Fundamental", f"{fund['score']} / 100", fund['health_label'].split()[0])
target_mean = fund['analyst_consensus'].get('target_mean')
if target_mean and target_mean > 0:
    target_upside = ((target_mean - latest['Close']) / latest['Close']) * 100.0
    col_m3.metric("Target Konsensus Analis", f"{currency_symbol} {target_mean:,.2f}", f"{target_upside:+.1f}% potensi")
else:
    col_m3.metric("Konsensus Analis", fund['analyst_consensus'].get('opinion', 'N/A'), "Rekomendasi")

col_m4.metric("Level Stop Loss Aman", f"{currency_symbol} {latest['Suggested_SL']:,.2f}", f"-{((latest['Close'] - latest['Suggested_SL']) / latest['Close']) * 100:.1f}% proteksi")
col_m5.metric("Target Profit (TP1)", f"{currency_symbol} {latest['Suggested_TP1']:,.2f}", f"+{((latest['Suggested_TP1'] - latest['Close']) / latest['Close']) * 100:.1f}% target")

# Banner Sinyal Saat Ini
current_signal = latest.get('Signal', 0)
if current_signal == 1:
    st.markdown(f"""
    <div class='signal-buy'>
        🟢 <b>SINYAL TEKNIKAL: POTENSI BUY (AKUMULASI / ENTRY)</b> — Setup strategi {trading_style} terpenuhi. Disarankan masuk dengan Stop Loss ketat di {currency_symbol} {latest['Suggested_SL']:,.2f}.
    </div>
    """, unsafe_allow_html=True)
elif current_signal == -1:
    st.markdown(f"""
    <div class='signal-sell'>
        🔴 <b>SINYAL TEKNIKAL: EXIT / AMBIL PROFIT / HINDARI BELI</b> — Momentum melemah atau tren patah. Disarankan keluar posisi untuk mengamankan keuntungan atau membatasi kerugian.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class='signal-wait'>
        ⚪ <b>SINYAL TEKNIKAL: WAIT & SEE (TUNGGU / DISIPLIN)</b> — Belum ada konfirmasi momentum kuat. Jangan memaksakan entry jika kriteria belum lengkap.
    </div>
    """, unsafe_allow_html=True)

st.write("")
render_header_guide()
st.write("")

# ==========================================
# Tabs Navigasi Rapi & Terstruktur (6 Master Tabs)
# ==========================================
tab_radar, tab_chart, tab_ai_monte, tab_fund_news, tab_risk_paper, tab_backtest_guide = st.tabs([
    "📡 1. Radar & Scanner Pasar",
    "📊 2. Analisis Teknikal & Grafik",
    "🤖 3. Prediksi AI & Monte Carlo",
    "🏢 4. Fundamental & Berita",
    "🛡️ 5. Manajemen Risiko & Paper Trading",
    "📈 6. Backtesting & Panduan Pemula"
])

# ----------------------------------------------------
# MASTER TAB 1: RADAR & SCANNER PASAR OTOMATIS
# ----------------------------------------------------
with tab_radar:
    st.markdown("### 📡 AI Market Scanner & Radar Peluang Pasar")
    st.markdown("Memindai puluhan saham secara otomatis. Menampilkan **Kode Ticker**, **Nama Perusahaan Lengkap**, serta **Modal 1 Lot** agar Anda bisa langsung memilih saham yang sesuai dengan modal Anda.")
    
    st.info("💡 **Untuk Modal Terbatas (Mulai Rp 50.000 - Rp 500.000)**: Pilih kelompok **'🇮🇩 Saham Indonesia Modal Ringan (< Rp 1.000 / Lot Murah)'** atau **'🇺🇸 Saham AS Terjangkau (< $30)'**. Modal beli 1 lot hanya mulai dari Rp 10.000 s/d Rp 70.000 saja!")
    
    scan_col1, scan_col2, scan_col3 = st.columns([2, 1, 1])
    with scan_col1:
        chosen_preset = st.selectbox(
            "Pilih Kelompok Pasar yang Ingin Dipindai:",
            options=list(SCAN_PRESETS.keys()),
            index=0
        )
    with scan_col2:
        filter_budget = st.checkbox("💰 Hanya Modal Terjangkau (< Rp 100rb / < $30)", value=False)
    with scan_col3:
        st.write("")
        run_scan_btn = st.button("🚀 Mulai Pindai Pasar Sekarang", use_container_width=True)
        
    if run_scan_btn or f"scan_{chosen_preset}" in st.session_state:
        st.session_state[f"scan_{chosen_preset}"] = True
        with st.spinner(f"Memindai seluruh saham di {chosen_preset}..."):
            scan_df = scan_market(chosen_preset, period="6mo")
            
        if not scan_df.empty:
            display_df = scan_df.copy()
            if filter_budget and "Modal_Val" in display_df.columns:
                is_us_group = "AS" in chosen_preset or "Global" in chosen_preset
                threshold = 30.0 if is_us_group else 100000.0
                display_df = display_df[display_df["Modal_Val"] <= threshold]
                
            cols_to_show = [c for c in display_df.columns if c != "Modal_Val"]
            display_df = display_df[cols_to_show]
            
            st.success(f"Berhasil memindai {len(display_df)} saham! Diurutkan dari skor peluang tertinggi:")
            
            st.dataframe(
                display_df.style.apply(
                    lambda x: ['background-color: rgba(0, 230, 118, 0.15)' if 'STRONG BUY' in str(v) else ('background-color: rgba(255, 82, 82, 0.15)' if 'EXIT' in str(v) else '') for v in x],
                    subset=['Rekomendasi']
                ),
                use_container_width=True,
                height=480
            )
            st.info("💡 **Tips Cepat**: Tertarik dengan salah satu saham di atas? Cukup ketik kode sahamnya di sidebar kiri untuk membuka grafik interaktif, analisis fundamental, dan hitungan lot amannya!")
        else:
            st.warning("Tidak dapat memuat data scan untuk preset ini saat ini.")
            
    st.write("")
    render_scanner_guide()

# ----------------------------------------------------
# MASTER TAB 2: ANALISIS TEKNIKAL & GRAFIK INTERAKTIF
# ----------------------------------------------------
with tab_chart:
    st.markdown(f"### 🕯️ Candlestick Chart & Indikator: {full_company_name} ({selected_ticker})")
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.60, 0.20, 0.20],
        subplot_titles=("Pergerakan Harga & Sinyal", "Volume Transaksi", "RSI (Relative Strength Index)")
    )
    
    # 1. Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name="Harga",
        increasing_line_color='#26A69A', decreasing_line_color='#EF5350'
    ), row=1, col=1)
    
    # Moving Averages
    if show_ema:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_9'], line=dict(color='#FFA726', width=1.2), name="EMA 9 (Fast)"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_21'], line=dict(color='#29B6F6', width=1.3), name="EMA 21 (Med)"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], line=dict(color='#AB47BC', width=1.5), name="EMA 50 (Trend)"), row=1, col=1)
        if 'SMA_200' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], line=dict(color='#FFFFFF', width=1.5, dash='dash'), name="SMA 200 (Major Trend)"), row=1, col=1)
            
    # Bollinger Bands
    if show_bb:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='rgba(150, 150, 255, 0.4)', width=1), name="BB Upper"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='rgba(150, 150, 255, 0.4)', width=1), fill='tonexty', fillcolor='rgba(150, 150, 255, 0.05)', name="BB Lower"), row=1, col=1)
        
    # VWAP
    if show_vwap and 'VWAP' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], line=dict(color='#FFD54F', width=1.5, dash='dot'), name="VWAP"), row=1, col=1)
        
    # Sinyal BUY & SELL
    buy_points = df[df['Signal'] == 1]
    sell_points = df[df['Signal'] == -1]
    if not buy_points.empty:
        fig.add_trace(go.Scatter(x=buy_points.index, y=buy_points['Low'] * 0.995, mode='markers', marker=dict(symbol='triangle-up', size=12, color='#00E676'), name="Sinyal BUY"), row=1, col=1)
    if not sell_points.empty:
        fig.add_trace(go.Scatter(x=sell_points.index, y=sell_points['High'] * 1.005, mode='markers', marker=dict(symbol='triangle-down', size=12, color='#FF1744'), name="Sinyal EXIT"), row=1, col=1)
        
    # Garis SL & TP Terkini
    if show_levels:
        fig.add_hline(y=latest['Suggested_SL'], line_dash="dash", line_color="#FF5252", line_width=1.5, annotation_text=f"SL: {latest['Suggested_SL']:,.2f}", row=1, col=1)
        fig.add_hline(y=latest['Suggested_TP1'], line_dash="dash", line_color="#69F0AE", line_width=1.5, annotation_text=f"TP1: {latest['Suggested_TP1']:,.2f}", row=1, col=1)
        fig.add_hline(y=latest['Suggested_TP2'], line_dash="dot", line_color="#00E676", line_width=1.2, annotation_text=f"TP2: {latest['Suggested_TP2']:,.2f}", row=1, col=1)

    # Volume & RSI
    vol_colors = ['#26A69A' if c >= o else '#EF5350' for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=vol_colors, name="Volume"), row=2, col=1)
    if 'Vol_SMA20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['Vol_SMA20'], line=dict(color='#FFA726', width=1.2), name="Vol SMA 20"), row=2, col=1)
        
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI_14'], line=dict(color='#BA68C8', width=1.5), name="RSI 14"), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="rgba(255, 82, 82, 0.6)", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="rgba(105, 240, 174, 0.6)", row=3, col=1)
    fig.add_hline(y=50, line_dash="dot", line_color="rgba(255, 255, 255, 0.3)", row=3, col=1)
    
    fig.update_layout(height=760, margin=dict(l=20, r=20, t=30, b=20), xaxis_rangeslider_visible=False, hovermode='x unified', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    st.write("")
    render_chart_guide()

# ----------------------------------------------------
# MASTER TAB 3: PREDIKSI AI & MONTE CARLO
# ----------------------------------------------------
with tab_ai_monte:
    subtab_ai, subtab_monte = st.tabs(["🤖 Prediksi AI & Target Nominal", "🎲 Simulasi Monte Carlo (1.000 Jalur) & VaR"])
    
    with subtab_ai:
        st.markdown(f"#### 🎯 Prediksi Machine Learning untuk **{full_company_name}**")
        
        col_h1, col_h2 = st.columns([1, 2])
        with col_h1:
            if is_swing:
                horizon_options = {1: "1 Hari ke Depan (Besok / H+1)", 3: "3 Hari ke Depan (Jangka Pendek)", 5: "5 Hari ke Depan (1 Minggu Bursa)"}
            else:
                horizon_options = {1: f"1 Candle Berikutnya ({interval})", 3: f"3 Candle Berikutnya (3x {interval})", 5: f"5 Candle Berikutnya (5x {interval})"}
            selected_horizon = st.selectbox("Pilih Horison Waktu Prediksi:", options=list(horizon_options.keys()), format_func=lambda x: horizon_options[x], index=0)
        with col_h2:
            st.caption(f"💡 Model Random Forest menganalisis kombinasi 11 indikator teknikal untuk memproyeksikan probabilitas pergerakan pada **{horizon_options[selected_horizon]}**.")
            
        with st.spinner("Menghitung model Machine Learning..."):
            ml_res = train_and_predict(df, forecast_horizon=selected_horizon)
            
        if ml_res['status'] == 'success':
            col_ai1, col_ai2, col_ai3 = st.columns(3)
            pred_label = ml_res['prediction']
            pred_color = "#00E676" if "NAIK" in pred_label else ("#FF5252" if "TURUN" in pred_label else "#FFD54F")
            
            col_ai1.markdown(f"""
            <div class='metric-card' style='border-left: 5px solid {pred_color};'>
                <h4 style='margin:0; color:#BDBDBD;'>Arah Prediksi AI</h4>
                <h2 style='margin:5px 0; color:{pred_color};'>{pred_label}</h2>
                <small>Estimasi probabilitas multi-faktor</small>
            </div>
            """, unsafe_allow_html=True)
            col_ai2.markdown(f"""
            <div class='metric-card'>
                <h4 style='margin:0; color:#BDBDBD;'>Probabilitas Peluang</h4>
                <h2 style='margin:5px 0; color:#29B6F6;'>Peluang Naik: {ml_res['bullish_prob']}%</h2>
                <small>Peluang Turun / Reversal: {ml_res['bearish_prob']}%</small>
            </div>
            """, unsafe_allow_html=True)
            col_ai3.markdown(f"""
            <div class='metric-card'>
                <h4 style='margin:0; color:#BDBDBD;'>Akurasi Out-of-Sample</h4>
                <h2 style='margin:5px 0; color:#AB47BC;'>{ml_res['accuracy']}%</h2>
                <small>Diuji pada data masa lalu yang belum pernah dilihat</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.markdown(f"##### 🎯 Proyeksi Rentang Target Harga Nominal (**{horizon_options[selected_horizon]}**):")
            proj = ml_res['projected_prices']
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            col_p1.metric("Harga Saat Ini", f"{currency_symbol} {proj['current_close']:,.2f}")
            col_p2.metric("Estimasi Target Harga", f"{currency_symbol} {proj['target_price']:,.2f}", f"{proj['change_pct']:+.2f}%")
            col_p3.metric("Batas Atas (Target Bullish)", f"{currency_symbol} {proj['upper_bound']:,.2f}", f"+{((proj['upper_bound'] - proj['current_close']) / proj['current_close']) * 100:.2f}%")
            col_p4.metric("Batas Bawah (Support Proteksi)", f"{currency_symbol} {proj['lower_bound']:,.2f}", f"{((proj['lower_bound'] - proj['current_close']) / proj['current_close']) * 100:.2f}%")
        else:
            st.warning(ml_res.get('message', 'Data tidak mencukupi.'))
            
        st.write("")
        render_ai_guide()
            
    with subtab_monte:
        st.markdown(f"#### 🎲 1.000 Skenario Masa Depan Monte Carlo & Value at Risk (VaR)")
        mc_days = st.slider("Hari Simulasi ke Depan:", min_value=10, max_value=60, value=30, step=5)
        
        with st.spinner("Menjalankan 1.000 jalur simulasi Monte Carlo..."):
            mc_res = run_monte_carlo_simulation(
                df=df, days_ahead=mc_days, num_simulations=1000,
                tp_price=float(latest['Suggested_TP1']), sl_price=float(latest['Suggested_SL'])
            )
            
        if mc_res['status'] == 'success':
            col_mc1, col_mc2, col_mc3, col_mc4 = st.columns(4)
            col_mc1.metric("Peluang Kena TP1 Dulu", f"{mc_res['prob_tp_first']}%", "Menyentuh Target Profit")
            col_mc2.metric("Peluang Kena SL Dulu", f"{mc_res['prob_sl_first']}%", "Menyentuh Stop Loss")
            col_mc3.metric("Value at Risk (VaR 95%)", f"-{mc_res['var_95_pct']:.2f}%", f"Maksimal rugi {currency_symbol} {mc_res['var_95_amount']:,.2f}")
            col_mc4.metric(f"Estimasi Median Hari ke-{mc_days}", f"{currency_symbol} {mc_res['expected_median_price']:,.2f}")
            
            fig_mc = go.Figure()
            sample_paths = mc_res['sample_paths']
            for s in range(sample_paths.shape[1]):
                fig_mc.add_trace(go.Scatter(x=list(range(mc_days + 1)), y=sample_paths[:, s], mode='lines', line=dict(color='rgba(255, 255, 255, 0.04)', width=1), showlegend=False, hoverinfo='skip'))
            cone = mc_res['cone_df']
            fig_mc.add_trace(go.Scatter(x=cone['Hari'], y=cone['Best_95th'], mode='lines', line=dict(color='#00E676', width=2), name="Skenario Terbaik (P95)"))
            fig_mc.add_trace(go.Scatter(x=cone['Hari'], y=cone['Median_50th'], mode='lines', line=dict(color='#29B6F6', width=2.5), name="Skenario Median (Expected)"))
            fig_mc.add_trace(go.Scatter(x=cone['Hari'], y=cone['Worst_5th'], mode='lines', line=dict(color='#FF5252', width=2), name="Skenario Terburuk (P5)"))
            fig_mc.add_hline(y=latest['Suggested_TP1'], line_dash="dash", line_color="#69F0AE", annotation_text="Target Profit 1")
            fig_mc.add_hline(y=latest['Suggested_SL'], line_dash="dash", line_color="#FF5252", annotation_text="Stop Loss")
            fig_mc.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20), template='plotly_dark', xaxis_title="Hari ke Depan", yaxis_title=f"Harga ({currency_symbol})")
            st.plotly_chart(fig_mc, use_container_width=True)
            st.write("")
            render_monte_carlo_guide()

# ----------------------------------------------------
# MASTER TAB 4: FUNDAMENTAL & BERITA GLOBAL
# ----------------------------------------------------
with tab_fund_news:
    subtab_fund, subtab_news = st.tabs(["🏢 Fundamental, Valuasi & Utang", "📰 Berita Emiten & Sentimen Makro"])
    
    with subtab_fund:
        st.markdown(f"#### 🏢 Evaluasi Bisnis & Kesehatan: **{full_company_name}**")
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            st.markdown(f"""
            <div class='metric-card' style='border-left: 6px solid {fund['health_color']}; text-align:center;'>
                <h4 style='margin:0; color:#BDBDBD;'>Skor Kesehatan Fundamental</h4>
                <h1 style='font-size:3.2rem; margin:8px 0; color:{fund['health_color']};'>{fund['score']} <span style='font-size:1.2rem; color:#888;'>/100</span></h1>
                <h4 style='margin:0; color:{fund['health_color']};'>{fund['health_label']}</h4>
            </div>
            """, unsafe_allow_html=True)
        with col_f2:
            st.markdown("##### 📋 Catatan Evaluasi Finansial:")
            for r in fund.get('score_reasons', []):
                st.markdown(f"- {r}")
                
        st.write("---")
        val, prof, bs, gd = fund['valuation'], fund['profitability'], fund['balance_sheet'], fund['growth_dividend']
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.markdown("**Valuasi:**")
            st.metric("P/E Ratio", f"{val['pe_trailing']:.1f}x" if val['pe_trailing'] else "N/A")
            st.metric("PBV (Price to Book)", f"{val['pbv']:.2f}x" if val['pbv'] else "N/A")
        with col_r2:
            st.markdown("**Profitabilitas:**")
            st.metric("ROE (Equity)", f"{prof['roe']*100:.1f}%" if prof['roe'] else "N/A")
            st.metric("Net Profit Margin", f"{prof['profit_margin']*100:.1f}%" if prof['profit_margin'] else "N/A")
        with col_r3:
            st.markdown("**Neraca & Utang:**")
            st.metric("Debt-to-Equity (DER)", f"{bs['debt_to_equity']:.1f}%" if bs['debt_to_equity'] else "N/A")
            st.metric("Current Ratio", f"{bs['current_ratio']:.2f}x" if bs['current_ratio'] else "N/A")
        with col_r4:
            st.markdown("**Dividen & Analis:**")
            st.metric("Dividend Yield", f"{gd['dividend_yield']*100:.2f}%" if (gd['dividend_yield'] and gd['dividend_yield'] < 1) else (f"{gd['dividend_yield']:.2f}%" if gd['dividend_yield'] else "N/A"))
            st.metric("Konsensus Analis", fund['analyst_consensus'].get('opinion', 'N/A'))
            
        st.write("")
        render_fundamental_guide()
            
    with subtab_news:
        st.markdown("#### 📰 Umpan Berita & Sentimen Pasar Terkini")
        n_col1, n_col2 = st.columns(2)
        with n_col1:
            st.markdown(f"##### 🗞️ Berita Terkait: **{full_company_name}**")
            if stock_news:
                for item in stock_news:
                    sent = item['sentiment']
                    st.markdown(f"""
                    <div class='news-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <small style='color:#9E9E9E;'>{item['source']} | {item['pub_date'][:16]}</small>
                            <span style='background:{sent['color']}22; color:{sent['color']}; border:1px solid {sent['color']}; font-size:0.75rem; padding:2px 8px; border-radius:4px; font-weight:bold;'>{sent['label']}</span>
                        </div>
                        <div style='margin-top:5px; font-weight:600; font-size:0.95rem;'>
                            <a href='{item['link']}' target='_blank' style='color:#E0E0E0; text-decoration:none;'>{item['title']}</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Tidak ada berita spesifik saat ini.")
        with n_col2:
            st.markdown("##### 🌍 Berita Finansial & Makroekonomi Dunia")
            if macro_news:
                for item in macro_news:
                    sent = item['sentiment']
                    st.markdown(f"""
                    <div class='news-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <small style='color:#9E9E9E;'>{item['source']} | {item['pub_date'][:16]}</small>
                            <span style='background:{sent['color']}22; color:{sent['color']}; border:1px solid {sent['color']}; font-size:0.75rem; padding:2px 8px; border-radius:4px; font-weight:bold;'>{sent['label']}</span>
                        </div>
                        <div style='margin-top:5px; font-weight:600; font-size:0.95rem;'>
                            <a href='{item['link']}' target='_blank' style='color:#E0E0E0; text-decoration:none;'>{item['title']}</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
        st.write("")
        render_news_guide()

# ----------------------------------------------------
# MASTER TAB 5: MANAJEMEN RISIKO & PAPER TRADING
# ----------------------------------------------------
with tab_risk_paper:
    subtab_risk, subtab_paper = st.tabs(["🛡️ Kalkulator Lot Aman (Anti-Rugi)", "💼 Portofolio Simulasi (Paper Trading)"])
    
    with subtab_risk:
        st.markdown(f"#### 🛡️ Hitung Ukuran Posisi Aman untuk: **{full_company_name}**")
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            default_capital = 50000000.0 if is_idx else 5000.0
            user_capital = st.number_input(f"Saldo Modal Anda ({currency_symbol})", min_value=100.0, value=default_capital, step=500000.0 if is_idx else 100.0, format="%.0f" if is_idx else "%.2f")
            user_risk_pct = st.slider("Risiko Maksimal per Transaksi (%)", min_value=0.5, max_value=5.0, value=1.5, step=0.5)
        with col_input2:
            user_entry = st.number_input(f"Harga Entry ({currency_symbol})", value=float(latest['Close']), step=10.0 if is_idx else 1.0, format="%.2f")
            user_sl = st.number_input(f"Stop Loss Proteksi ({currency_symbol})", value=float(latest['Suggested_SL']), step=10.0 if is_idx else 1.0, format="%.2f")
            user_tp1 = st.number_input(f"Target Profit 1 ({currency_symbol})", value=float(latest['Suggested_TP1']), step=10.0 if is_idx else 1.0, format="%.2f")
            user_tp2 = st.number_input(f"Target Profit 2 ({currency_symbol})", value=float(latest['Suggested_TP2']), step=10.0 if is_idx else 1.0, format="%.2f")
            
        risk_plan = calculate_risk_plan(capital=user_capital, risk_percent=user_risk_pct, entry_price=user_entry, stop_loss_price=user_sl, target_price_1=user_tp1, target_price_2=user_tp2, is_idx=is_idx)
        st.write("---")
        if risk_plan['status'] == 'success':
            for w in risk_plan.get('warnings', []):
                st.warning(w)
            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            r_col1.metric(f"Ukuran Posisi Aman", f"{risk_plan['total_lots']:,} {risk_plan['unit_name']}", f"{risk_plan['actual_shares']:,} Lembar")
            r_col2.metric("Modal Pembelian", f"{currency_symbol} {risk_plan['invested_capital']:,.0f}" if is_idx else f"{currency_symbol} {risk_plan['invested_capital']:,.2f}", f"{(risk_plan['invested_capital'] / user_capital) * 100:.1f}% Saldo")
            r_col3.metric("Maksimal Rugi Kena SL", f"{currency_symbol} {risk_plan['actual_loss_at_sl']:,.0f}" if is_idx else f"{currency_symbol} {risk_plan['actual_loss_at_sl']:,.2f}", f"{risk_plan['actual_risk_pct']:.2f}% Modal (Aman!)")
            r_col4.metric("Rasio Risk / Reward (RRR)", f"1 : {risk_plan['rrr_1']}", f"TP2: 1 : {risk_plan['rrr_2']}")
            
        st.write("")
        render_risk_guide()
            
    with subtab_paper:
        st.markdown("#### 💼 Portofolio Simulasi Paper Trading (Uang Virtual)")
        port = load_portfolio(initial_balance=50000000.0 if is_idx else 5000.0)
        
        unrealized_pnl = 0.0
        positions_value = 0.0
        for pos in port.get("positions", []):
            curr_p = float(latest['Close']) if pos['ticker'] == selected_ticker else pos['buy_price']
            pos_val = curr_p * pos['shares']
            positions_value += pos_val
            unrealized_pnl += pos_val - (pos['buy_price'] * pos['shares'])
            
        total_equity = port['cash'] + positions_value
        tot_ret_pct = ((total_equity - port['initial_balance']) / port['initial_balance']) * 100.0
        
        p_card1, p_card2, p_card3, p_card4 = st.columns(4)
        p_card1.metric("Total Saldo Ekuitas", f"{currency_symbol} {total_equity:,.0f}" if is_idx else f"{currency_symbol} {total_equity:,.2f}", f"{tot_ret_pct:+.2f}% total return")
        p_card2.metric("Saldo Kas Tersedia", f"{currency_symbol} {port['cash']:,.0f}" if is_idx else f"{currency_symbol} {port['cash']:,.2f}")
        p_card3.metric("Nilai Portofolio Terbuka", f"{currency_symbol} {positions_value:,.0f}" if is_idx else f"{currency_symbol} {positions_value:,.2f}")
        p_card4.metric("Floating PnL Berjalan", f"{currency_symbol} {unrealized_pnl:+,.0f}" if is_idx else f"{currency_symbol} {unrealized_pnl:+,.2f}")
        
        st.write("---")
        st.markdown(f"##### 🛒 Beli Saham Virtual: **{full_company_name}** ({selected_ticker})")
        buy_col1, buy_col2, buy_col3 = st.columns(3)
        with buy_col1:
            order_lots = st.number_input(f"Jumlah Lot Dibeli ({'Lot' if is_idx else 'Lembar'})", min_value=1, value=max(1, risk_plan.get('total_lots', 1)), step=1)
        with buy_col2:
            st.write(f"Harga: **{currency_symbol} {latest['Close']:,.2f}** | SL: **{currency_symbol} {latest['Suggested_SL']:,.2f}** | TP: **{currency_symbol} {latest['Suggested_TP1']:,.2f}**")
        with buy_col3:
            if st.button(f"🟢 Konfirmasi Beli {order_lots:,} {'Lot' if is_idx else 'Lbr'}", use_container_width=True):
                sh_count = order_lots * 100 if is_idx else order_lots
                b_res = execute_buy(selected_ticker, float(latest['Close']), sh_count, float(latest['Suggested_SL']), float(latest['Suggested_TP1']), is_idx)
                if b_res['status'] == 'success':
                    st.success(b_res['message'])
                    st.rerun()
                else:
                    st.error(b_res['message'])
                    
        st.write("")
        st.markdown("##### 📂 Posisi Saham Terbuka Saat Ini:")
        if port.get("positions"):
            for p in port["positions"]:
                c_name = get_company_name(p['ticker'])
                curr_p = float(latest['Close']) if p['ticker'] == selected_ticker else p['buy_price']
                pnl_val = (curr_p - p['buy_price']) * p['shares']
                pnl_pct = ((curr_p - p['buy_price']) / p['buy_price']) * 100.0
                
                p_c1, p_c2, p_c3, p_c4, p_c5 = st.columns([3, 2, 2, 2, 2])
                p_c1.write(f"**{c_name}** (`{p['ticker']}` - {p['lots']} Lot)")
                p_c2.write(f"Beli @ {p['buy_price']:,.2f}")
                p_c3.write(f"Kini @ {curr_p:,.2f}")
                p_c4.write(f"{currency_symbol} {pnl_val:+,.0f} ({pnl_pct:+.2f}%)")
                with p_c5:
                    if st.button("🔴 Jual", key=f"sell_{p['ticker']}"):
                        s_res = execute_sell(p['ticker'], curr_p, reason="Manual Take Profit / Cut Loss")
                        st.success(s_res['message'])
                        st.rerun()
        else:
            st.info("Belum ada posisi terbuka. Gunakan tombol beli di atas untuk mulai simulasi.")
            
        if port.get("history"):
            st.write("")
            st.markdown("##### 📜 Riwayat Transaksi Selesai:")
            st.dataframe(pd.DataFrame(port["history"]), use_container_width=True)
            
        st.write("")
        render_paper_trading_guide()

# ----------------------------------------------------
# MASTER TAB 6: BACKTESTING & PANDUAN PEMULA
# ----------------------------------------------------
with tab_backtest_guide:
    subtab_bt, subtab_guide, subtab_glossary = st.tabs([
        "📈 Bukti Performa & Backtesting",
        "📚 Panduan Mental & Aturan Trading",
        "📖 Kamus Istilah Saham Interaktif (A-Z)"
    ])
    
    with subtab_bt:
        st.markdown(f"#### 📈 Hasil Backtesting Strategi pada **{full_company_name}**")
        bt_res = run_backtest(df=df, initial_capital=user_capital, risk_per_trade=user_risk_pct / 100.0, is_idx=is_idx)
        b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
        b_col1.metric("Total Return (%)", f"{bt_res['total_return_pct']:+.2f}%")
        b_col2.metric("Win Rate", f"{bt_res['win_rate']:.1f}%", f"{bt_res['winning_trades']} Menang / {bt_res['losing_trades']} Kalah")
        b_col3.metric("Total Transaksi", f"{bt_res['total_trades']}")
        b_col4.metric("Max Drawdown", f"{bt_res['max_drawdown_pct']:.2f}%")
        b_col5.metric("Profit Factor", f"{bt_res['profit_factor']:.2f}")
        
        st.write("")
        st.markdown("##### 📊 Pertumbuhan Ekuitas (Equity Curve):")
        fig_eq = go.Figure()
        fig_eq.add_trace(go.Scatter(x=bt_res['equity_df'].index, y=bt_res['equity_df']['Equity'], mode='lines', line=dict(color='#00E676', width=2), fill='tozeroy', fillcolor='rgba(0, 230, 118, 0.08)', name="Ekuitas Akun"))
        fig_eq.update_layout(height=340, margin=dict(l=20, r=20, t=20, b=20), template='plotly_dark', yaxis_title=f"Saldo ({currency_symbol})")
        st.plotly_chart(fig_eq, use_container_width=True)
        st.write("")
        render_backtest_guide()
        
    with subtab_guide:
        st.markdown("#### 📚 Panduan Penting untuk Pemula: Cara Bertahan & Sukses di Trading")
        st.markdown("""
        ##### 1. Mengapa Perlu Analisis 360° (Teknikal + Fundamental + Berita)?
        - **Fundamental (Apa yang Dibeli)**: Memastikan Anda tidak membeli saham perusahaan busuk/bangkrut yang bisa disuspensi atau delisting.
        - **Teknikal (Kapan Beli & Jual)**: Membantu Anda masuk di harga diskon/reversal dan keluar sebelum penurunan tajam.
        - **Berita & Makro (Katalis & Waspada)**: Menghindarkan Anda dari jebakan berita dadakan (seperti keputusan suku bunga The Fed, perang dagang, atau laporan laba anjlok).

        ##### 2. Tiga Pilar Trading Profesional:
        1. **Metode (Strategi)**: Memiliki aturan entry dan exit yang jelas dan sudah di-backtest.
        2. **Manajemen Uang (Money Management)**: Tidak pernah merisikokan lebih dari 1%–2% total modal per transaksi.
        3. **Psikologi & Disiplin**: Menerima kekalahan kecil sebagai bagian normal dari bisnis trading, dan membiarkan posisi pemenang mencapai Target Profit (*cut losses short, let winners run*).
        """)

    with subtab_glossary:
        render_interactive_glossary()
