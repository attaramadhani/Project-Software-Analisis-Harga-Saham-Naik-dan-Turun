# ⚡ AI Stock 360° Institutional Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-orange.svg)](https://plotly.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-yellow.svg)](https://scikit-learn.org/)
[![Yahoo Finance](https://img.shields.io/badge/Data-Yahoo%20Finance%20(Free)-green.svg)](https://finance.yahoo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> **Platform Analisis, Prediksi Arah Harga Saham Global (Teknikal + Fundamental + Berita + AI Machine Learning), Simulasi Stokastik Monte Carlo, serta Sistem Pelindung Modal (Anti-Rugi).**  
> Dirancang khusus bagi pemula maupun trader profesional untuk bertransaksi di bursa saham **tanpa mengalami kerugian besar**, tetap disiplin pada *money management*, dan meraih profit yang konsisten.

---

## 📸 Antarmuka & Tampilan Aplikasi

```
+--------------------------------------------------------------------------------------------------+
|  🏢 BANK CENTRAL ASIA (BBCA.JK) | Sektor: Financial Services | Mode: Swing Trading (Harian)     |
|  🏆 360° OVERALL GRADE: A+ (EXCELLENT / PRIME SETUP) | Skor Terpadu: 88.5 / 100                  |
+--------------------------------------------------------------------------------------------------+
|  Harga Terakhir  | Skor Fundamental | Konsensus Analis | Level Stop Loss (SL) | Target Profit 1  |
|  Rp 10.250 (+1.2%)| 90 / 100 (BlueChip)| BUY (+15% Upside)| Rp 9.850 (-3.9%)     | Rp 11.050 (+7.8%)|
+--------------------------------------------------------------------------------------------------+
|  [📡 1. Radar Scanner] [📊 2. Teknikal] [🤖 3. AI & Monte Carlo] [🏢 4. Fundamental] [🛡️ 5. Risiko]  |
+--------------------------------------------------------------------------------------------------+
```

---

## 🚀 8 Keunggulan Utama (Core Superpowers)

### 1. 🌐 Sumber Data Global 100% Gratis & Real-Time
- Mengambil data pasar langsung dari **Yahoo Finance (`yfinance`)** tanpa biaya langganan API berbayar.
- **Bursa Efek Indonesia (IDX)**: Otomatis mendeteksi 4 huruf ticker (`BBCA`, `BBRI`, `GOTO`, `TLKM`, `ASII`, `ANTM`, dll) dan menambahkan `.JK`.
- **Bursa Amerika Serikat (Wall Street)**: `AAPL`, `NVDA`, `TSLA`, `MSFT`, `PLTR`, `AMD`, `AMZN`, dll.
- **Pasar Global, Kripto & Komoditas**: `BTC-USD`, `ETH-USD`, `GC=F` (Emas), `CL=F` (Minyak), `^JKSE` (IHSG), `^GSPC` (S&P 500).

### 2. 🏆 Evaluasi Komposit Terpadu 360° (*Overall Grade*)
Sistem menggabungkan 3 pilar utama menjadi satu nilai komposit (*Composite Score* 0–100) dan predikat huruf:
- **Teknikal (40%)**: Posisi tren Moving Average (EMA 9, 21, 50, SMA 200), RSI 14, VWAP, Bollinger Bands.
- **Fundamental (40%)**: Kesehatan laba, valuasi (P/E, PBV), efisiensi modal (ROE), dan beban utang (DER).
- **Sentimen Berita & Makro (20%)**: Analisis sentimen berita terkini dan katalis makroekonomi (The Fed / BI Rate).
- **Hasil Grade**:
  - `A+` (Excellent / Prime Setup)
  - `A` (Very Good / Strong Accumulation)
  - `B` (Moderate / Selective Buy)
  - `C` (Wait & See / Netral)
  - `D` (High Risk / Avoid)

### 3. 📡 AI Market Radar & Scanner Pasar (Modal Terjangkau)
- Memindai puluhan saham sekaligus secara *multi-threaded* dalam hitungan detik.
- Menyediakan kolom **Nama Perusahaan Lengkap** dan **Modal 1 Lot** (mulai Rp 10.000 s/d Rp 70.000 untuk IDX) agar pemula dengan modal terbatas bisa langsung berpartisipasi.
- Filter bawaan (*Presets*):
  - 🇮🇩 Saham Indonesia Modal Ringan (< Rp 1.000 / Lot Murah)
  - 🇺🇸 Saham AS Terjangkau (Budget-Friendly < $30)
  - 🇮🇩 Top 20 Saham Terbesar Indonesia (IHSG Blue Chip)
  - 🇮🇩 Sektor Tambang & Energi
  - 🇮🇩 Sektor Perbankan & Finansial
  - 🇺🇸 AI, Semikonduktor & High Growth

### 4. 🤖 Prediksi Arah AI Machine Learning (Random Forest)
- Menggunakan algoritma **Random Forest Classifier** yang dilatih secara dinamis pada 11 fitur indikator teknikal.
- Menghitung **Probabilitas Statistik Arah** (Peluang Naik vs Peluang Turun) untuk horison waktu 1 hari (H+1), 3 hari, atau 5 hari ke depan.
- Menguji akurasi secara transparan pada data historis yang belum pernah dilihat model (*Out-of-Sample Accuracy*).
- Menghasilkan **Proyeksi Rentang Target Harga Nominal**: Harga Saat Ini, Estimasi Target Wajar, Batas Atas (*Bullish Target*), dan Batas Bawah (*Support Proteksi*).

### 5. 🎲 Simulasi Stokastik Monte Carlo (1.000 Jalur) & VaR
- Menjalankan **1.000 skenario acak masa depan** menggunakan *Geometric Brownian Motion (GBM)*.
- Menampilkan grafik sebaran *spaghetti chart* beserta kurva persentil:
  - Skenario Terbaik (P95 Bullish)
  - Skenario Median (Expected Path)
  - Skenario Terburuk (P5 Bearish)
- **Probabilitas Menyentuh TP vs SL**: Menguji berapa persen kemungkinan harga menyentuh Target Profit duluan dibanding Stop Loss duluan.
- **Value at Risk (VaR 95%)**: Menghitung potensi batas kerugian maksimal standar institusi keuangan Wall Street.

### 6. 🛡️ Mesin Pelindung Modal & Kalkulator Lot Aman (Anti-Rugi)
- Menerapkan **Aturan Emas Risiko 1% - 2%**: Membatasi kerugian jika terkena Stop Loss agar tidak pernah melebihi 1%–2% total modal akun Anda.
- Menghitung otomatis ukuran posisi aman:
  - Saham Indonesia: Dikonversi ke satuan **Lot resmi (100 lembar)**.
  - Saham AS / Global: Dikonversi ke satuan **Lembar saham (Shares)**.
- Menentukan level Stop Loss dinamis berbasis **Average True Range (1.5x ATR)** agar tidak mudah terkena gocekan tipuan pasar (*market noise*).
- Menghitung rasio **Risk-to-Reward (RRR)** dengan target minimal 1:2.

### 7. 💼 Simulator Portofolio Paper Trading (Uang Virtual)
- Fasilitas latihan transaksi jual-beli tanpa risiko kehilangan uang sungguhan.
- Data portofolio tersimpan secara persisten di file lokal `paper_portfolio.json`.
- Memantau Saldo Kas, Total Nilai Ekuitas, *Floating PnL* (keuntungan/kerugian berjalan secara *real-time*), dan riwayat transaksi selesai (*Realized PnL*).

### 8. 📖 Menu Penjelasan Istilah untuk Pemula & Kamus A-Z
- Di bawah **setiap kartu metrik, grafik, dan tab**, tersedia menu *dropdown* (`st.expander`) yang menerangkan arti indikator dan langkah praktis yang harus diambil.
- **Kamus Istilah Saham Interaktif (A-Z)** di Tab 6: Pengguna bisa mencari istilah apa saja (seperti *Lot, RSI, Cut Loss, Haka, Haki, Bandar, Breakout, PE Ratio, PBV, ROE, DER, VWAP, Golden Cross*) lengkap dengan tips praktis berbahasa Indonesia santai.

---

## 📁 Struktur File Proyek

```
Project-Software-Analisis-Harga-Saham-Naik-dan-Turun/
├── app.py              # Dashboard Web Interaktif Utama (Streamlit + Plotly)
├── data_loader.py      # Pengunduh data Yahoo Finance, kamus emiten & auto-detect ticker
├── indicators.py       # Engine teknikal murni (EMA, SMA, RSI, MACD, BB, ATR, VWAP)
├── strategies.py       # Logika sinyal Swing Trading (Harian) & Day Trading (Intraday)
├── predictor.py        # Model AI Machine Learning Random Forest & proyeksi nominal harga
├── fundamentals.py     # Analisis rasio keuangan, valuasi, solvabilitas & skor emiten
├── news_loader.py      # Pengambil berita Yahoo & Google News RSS + deteksi sentimen
├── scanner.py          # Screener pasar massal multi-threaded & filter budget
├── monte_carlo.py      # Simulasi 1.000 jalur stokastik GBM & Value at Risk (VaR 95%)
├── risk_manager.py     # Mesin kalkulasi lot aman & money management anti-boncos
├── backtester.py       # Backtesting historis (Win Rate, Total Return, Drawdown, Profit Factor)
├── paper_trading.py    # Simulator portofolio virtual persisten
├── glossary.py         # Kamus 32+ istilah pasar modal & fungsi panduan pemula
├── paper_portfolio.json# File penyimpanan portofolio virtual lokal
├── requirements.txt    # Daftar dependensi library Python
├── run.bat             # Peluncur aplikasi otomatis untuk Windows
├── .gitignore          # Konfigurasi pengabaian file sementara git
└── README.md           # Dokumentasi lengkap proyek
```

---

## 💻 Panduan Instalasi & Menjalankan

### Prasyarat
- Komputer dengan sistem operasi Windows, macOS, atau Linux.
- **Python 3.10 atau versi lebih baru** terpasang.

### 1. Kloning Repositori
```bash
git clone https://github.com/attaramadhani/Project-Software-Analisis-Harga-Saham-Naik-dan-Turun.git
cd Project-Software-Analisis-Harga-Saham-Naik-dan-Turun
```

### 2. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

#### Cara 1 (Paling Mudah di Windows):
Cukup klik dua kali (double-click) file:
👉 **`run.bat`**

#### Cara 2 (Lewat Terminal / Command Prompt / PowerShell):
```bash
streamlit run app.py
```
atau jika `streamlit` belum terdaftar di PATH:
```bash
python -m streamlit run app.py
```

Buka peramban (browser) Anda di:
🌐 **`http://localhost:8501`**

---

## 🎯 3 Pilar Trading Disiplin untuk Pemula

1. **Metode (Strategi 360°)**: Jangan membeli saham hanya karena "kata teman" atau rumor media sosial. Gunakan kombinasi teknikal, fundamental, dan sentimen berita.
2. **Manajemen Uang (Money Management)**: Jangan pernah *All-In* pada satu saham. Selalu batasi risiko kerugian maksimal **1% sampai 2% modal per transaksi**.
3. **Psikologi & Disiplin**: Selalu pasang **Stop Loss**. Kerugian kecil yang terukur adalah biaya wajar dalam bisnis trading; biarkan posisi yang menang mencapai **Target Profit** (*cut losses short, let winners run*).

---

## ⚖️ Disclaimer (Pernyataan Penyangkalan)

*Perangkat lunak ini dikembangkan untuk tujuan edukasi, riset, dan analisis data kuantitatif. Segala keputusan investasi dan trading merupakan tanggung jawab pribadi masing-masing pengguna. Kinerja masa lalu tidak menjamin hasil di masa depan.*

---

## 👤 Pengembang

Dikembangkan dengan dedikasi oleh **[Atta Ramadhani](https://github.com/attaramadhani)**.  
Kritik, saran, dan kontribusi pengembangan (Pull Request) selalu terbuka!
