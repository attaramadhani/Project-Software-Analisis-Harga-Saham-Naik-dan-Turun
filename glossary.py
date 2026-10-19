"""
glossary.py
Kamus Lengkap Istilah Pasar Modal, Trading Saham, Indikator Teknikal, Fundamental, AI & Manajemen Risiko.
Dibuat khusus dengan bahasa Indonesia yang santai, mudah dipahami pemula, dan disertai tips tindakan praktis.
"""

import streamlit as st

GLOSSARY_TERMS = {
    # --- UMUM & PESANAN ---
    "Lot Saham": {
        "kategori": "Umum & Satuan",
        "arti": "Satuan resmi pembelian saham di bursa. Di Indonesia (BEI/IDX), 1 Lot = 100 lembar saham. Di bursa Amerika Serikat (US), saham bisa dibeli per 1 lembar (bahkan pecahan/fractional shares).",
        "tips": "Jika harga saham Rp 500, maka untuk beli 1 lot modalnya adalah Rp 500 x 100 = Rp 50.000 saja. Jadi Anda tidak butuh modal jutaan rupiah untuk mulai membeli saham!"
    },
    "Ticker / Kode Saham": {
        "kategori": "Umum & Satuan",
        "arti": "Singkatan kode unik perusahaan di bursa efek. Di Indonesia terdiri dari 4 huruf (contoh: BBCA = Bank Central Asia, TLKM = Telkom). Di pasar AS terdiri dari 1-4 huruf (contoh: AAPL = Apple, NVDA = Nvidia).",
        "tips": "Akhiran '.JK' menandakan saham tersebut terdaftar di Jakarta (Bursa Efek Indonesia)."
    },
    "Bid & Ask (Haka & Haki)": {
        "kategori": "Umum & Satuan",
        "arti": "Bid adalah antrean harga bagi pembeli. Ask (Offer) adalah antrean harga bagi penjual. 'HAKA' (Hajar Kanan) artinya langsung beli di harga antrean penjual tanpa menunggu. 'HAKI' (Hajar Kiri) artinya langsung jual di harga antrean pembeli.",
        "tips": "Pemula disarankan membeli saat harga sedang istirahat (antre beli/bid) daripada mengejar harga yang sudah naik tinggi (FOMO)."
    },
    "Bullish & Bearish": {
        "kategori": "Kondisi Pasar",
        "arti": "Bullish artinya pasar/saham sedang dalam tren naik (seperti tandukan banteng yang mengarah ke atas). Bearish artinya pasar sedang dalam tren turun (seperti cakar beruang yang mencakar ke bawah).",
        "tips": "Lebih aman membeli saham saat trennya sedang Bullish daripada mencoba menebak dasar saham yang sedang Bearish terjun bebas."
    },
    "Reversal": {
        "kategori": "Kondisi Pasar",
        "arti": "Pembalikan arah tren harga. Misalnya dari sebelumnya tren turun (Bearish) berbalik arah menjadi mulai naik (Bullish), atau sebaliknya.",
        "tips": "Sinyal pembalikan arah paling valid jika didukung oleh lonjakan volume transaksi besar."
    },
    "Breakout": {
        "kategori": "Kondisi Pasar",
        "arti": "Kondisi ketika harga saham berhasil menembus level batas atas (Resistance) atau level harga tertinggi sebelumnya dengan kekuatan volume yang besar.",
        "tips": "Breakout sering kali menjadi awal dari kenaikan harga yang kencang dan cepat."
    },

    # --- INDIKATOR TEKNIKAL ---
    "Candlestick": {
        "kategori": "Analisis Teknikal",
        "arti": "Grafik lilin yang menggambarkan 4 harga penting dalam 1 periode waktu: Open (Harga Buka), High (Harga Tertinggi), Low (Harga Terendah), dan Close (Harga Tutup). Lilin Hijau = harga naik (Close > Open). Lilin Merah = harga turun (Close < Open).",
        "tips": "Buntut panjang di bawah lilin hijau menandakan ada dorongan beli yang kuat dari pembeli yang menolak penurunan harga."
    },
    "EMA (Exponential Moving Average)": {
        "kategori": "Analisis Teknikal",
        "arti": "Garis rata-rata pergerakan harga yang memberi bobot lebih besar pada data harga terkini sehingga lebih cepat merespons perubahan tren dibandingkan SMA biasa.",
        "tips": "Garis EMA 9 & 21 untuk melihat tren jangka pendek, EMA 50 untuk jangka menengah, dan SMA 200 untuk tren besar tahunan. Jika harga berada di atas EMA 50, tren saham tergolong sehat!"
    },
    "SMA 200 (Golden Cross & Death Cross)": {
        "kategori": "Analisis Teknikal",
        "arti": "Rata-rata harga selama 200 hari bursa (sekitar 1 tahun). Jika garis MA cepat memotong ke atas SMA 200 disebut 'Golden Cross' (sinyal Bullish besar). Jika memotong ke bawah disebut 'Death Cross' (sinyal waspada Bearish).",
        "tips": "Institusi besar dan manajer investasi dunia selalu memperhatikan garis SMA 200 sebagai benteng pertahanan tren jangka panjang."
    },
    "RSI (Relative Strength Index)": {
        "kategori": "Analisis Teknikal",
        "arti": "Indikator pengukur momentum dari angka 0 sampai 100. Angka di atas 70 disebut 'Overbought' (jenuh beli, harga rawan koreksi turun). Angka di bawah 30 disebut 'Oversold' (jenuh jual, harga sudah murah dan berpeluang membal naik).",
        "tips": "Hindari membeli saham jika RSI sudah di atas 75-80 karena sangat berisiko terkena aksi ambil untung (profit taking)."
    },
    "Bollinger Bands": {
        "kategori": "Analisis Teknikal",
        "arti": "Pita pembungkus harga yang terdiri dari garis atas (Upper Band), tengah, dan garis bawah (Lower Band). Mengukur tingkat volatilitas pasar.",
        "tips": "Jika lilin harga menyentuh pita bawah, harga sering kali memantul kembali ke pita tengah. Jika pita menyempit rapat, bersiaplah karena biasanya akan terjadi ledakan pergerakan harga besar."
    },
    "VWAP (Volume Weighted Average Price)": {
        "kategori": "Analisis Teknikal",
        "arti": "Harga rata-rata tertimbang berdasarkan volume transaksi. Ini adalah patokan harga wajar yang digunakan para trader besar dan institusi saat melakukan transaksi harian (Day Trading).",
        "tips": "Jika harga berada di atas garis VWAP, pembeli memegang kendali (sinyal kuat). Jika di bawah VWAP, penjual lebih dominan."
    },
    "ATR (Average True Range)": {
        "kategori": "Analisis Teknikal",
        "arti": "Indikator pengukur tingkat keganasan/fluktuasi pergerakan harga saham sehari-hari (volatilitas).",
        "tips": "Software ini menggunakan nilai ATR untuk otomatis menghitung jarak Stop Loss yang ideal agar posisi Anda tidak gampang terkena gocekan tipuan pasar."
    },
    "Volume Surge (Lonjakan Volume)": {
        "kategori": "Analisis Teknikal",
        "arti": "Volume transaksi hari ini melonjak berkali-kali lipat (minimal 1,5x sampai 2x) dibandingkan rata-rata 20 hari sebelumnya.",
        "tips": "Lonjakan volume menandakan ada 'Big Money', 'Paus', atau Investor Institusi yang sedang aktif memborong saham tersebut."
    },

    # --- MANAJEMEN RISIKO ---
    "Stop Loss (SL / Cut Loss)": {
        "kategori": "Manajemen Risiko",
        "arti": "Batas harga pengaman yang dipasang untuk otomatis menjual saham jika harga berlawanan dengan perkiraan, guna mencegah modal hangus atau rugi mendalam.",
        "tips": "Stop Loss adalah pelampung penyelamat trader. Jangan pernah malu melakukan cut loss kecil, karena tujuan trading bukan untuk selalu benar, melainkan menjaga modal agar tetap bisa trading di masa depan!"
    },
    "Take Profit (TP1 & TP2)": {
        "kategori": "Manajemen Risiko",
        "arti": "Target harga yang direncanakan untuk menjual saham dan mengunci keuntungan (cuan). TP1 adalah target realistis pertama, sedangkan TP2 adalah target optimis tren lanjutan.",
        "tips": "Strategi profesional: Jual 50% lot Anda di TP1 untuk mengamankan modal, lalu biarkan 50% sisanya melaju ke TP2 dengan menggeser Stop Loss ke harga modal (Trailing Stop)."
    },
    "Risk-to-Reward Ratio (RRR)": {
        "kategori": "Manajemen Risiko",
        "arti": "Perbandingan antara potensi risiko kerugian dibanding potensi keuntungan. Contoh 1:2 artinya jika Anda siap rugi Rp 100.000, maka potensi keuntungannya harus minimal Rp 200.000.",
        "tips": "Selalu tolak transaksi yang memiliki RRR di bawah 1:1,5. Dengan RRR 1:2 atau 1:3, meski tebakan Anda hanya benar 40% dari seluruh transaksi, akun Anda tetap akan menghasilkan profit bersih!"
    },
    "Aturan Risiko 1-2% (Position Sizing)": {
        "kategori": "Manajemen Risiko",
        "arti": "Aturan emas trader profesional: jangan pernah merisikokan kerugian lebih dari 1% sampai 2% dari total modal Anda dalam 1 transaksi jika terkena Stop Loss.",
        "tips": "Misal modal Rp 10.000.000, maksimal rugi jika kena SL hanya Rp 100.000 - Rp 200.000. Software ini otomatis menghitungkan berapa lot aman yang boleh dibeli agar tidak boncos."
    },
    "Drawdown (Penurunan Saldo)": {
        "kategori": "Manajemen Risiko",
        "arti": "Persentase penurunan nilai portofolio dari titik tertinggi (puncak modal) ke titik terendah selama periode trading.",
        "tips": "Max Drawdown yang sehat adalah di bawah 15-20%. Semakin kecil angka drawdown, semakin aman strategi tersebut untuk modal Anda."
    },

    # --- AI MACHINE LEARNING & SIMULASI ---
    "Machine Learning (Random Forest)": {
        "kategori": "AI & Kuantitatif",
        "arti": "Algoritma kecerdasan buatan yang mempelajari ratusan kombinasi pola teknikal masa lalu secara matematis untuk memperkirakan probabilitas arah harga ke depan tanpa emosi manusiawi.",
        "tips": "Gunakan prediksi AI sebagai konfirmasi tambahan (second opinion), jangan gunakan secara buta tanpa memasang Stop Loss."
    },
    "Probabilitas Prediksi (%)": {
        "kategori": "AI & Kuantitatif",
        "arti": "Tingkat keyakinan model AI terhadap arah pergerakan. Misalnya Peluang Naik 68% vs Turun 32%.",
        "tips": "Peluang di atas 60% tergolong sinyal yang memiliki keyakinan statistik cukup kuat."
    },
    "Simulasi Monte Carlo (1.000 Jalur)": {
        "kategori": "AI & Kuantitatif",
        "arti": "Simulasi matematika probabilitas yang melemparkan 1.000 skenario acak pergerakan harga di masa depan berdasarkan volatilitas dan riwayat harga saham ini.",
        "tips": "Membantu Anda melihat skenario terburuk (Worst Case P5) dan skenario terbaik (Best Case P95) sebelum Anda benar-benar mempertaruhkan uang Anda."
    },
    "Value at Risk (VaR 95%)": {
        "kategori": "AI & Kuantitatif",
        "arti": "Metrik risiko standar perbankan global: estimasi kerugian maksimal yang mungkin terjadi dengan tingkat keyakinan 95% dalam rentang hari ke depan.",
        "tips": "Jika VaR 95% menunjukkan angka -5%, artinya kemungkinan besar (95%) kerugian Anda tidak akan melampaui 5% dalam kondisi pasar normal."
    },

    # --- FUNDAMENTAL PERUSAHAAN ---
    "P/E Ratio (Price to Earnings Ratio)": {
        "kategori": "Analisis Fundamental",
        "arti": "Perbandingan antara harga saham saat ini dengan laba bersih per lembar saham (EPS). Menunjukkan berapa rupiah yang rela dibayar investor untuk setiap Rp 1 laba perusahaan.",
        "tips": "P/E di bawah 15x umumnya dianggap murah/wajar. Namun untuk saham teknologi yang tumbuh cepat, P/E tinggi sering kali wajar karena potensi laba masa depan yang besar."
    },
    "PBV (Price to Book Value)": {
        "kategori": "Analisis Fundamental",
        "arti": "Perbandingan harga saham dengan nilai buku kekayaan bersih perusahaan (ekuitas). PBV 1.0x artinya saham dihargai persis senilai harta bersihnya.",
        "tips": "PBV di bawah 1.0x sering kali menandakan saham sedang 'salah harga' (undervalued) atau diskon besar, cocok untuk investor nilai (Value Investing)."
    },
    "ROE (Return on Equity)": {
        "kategori": "Analisis Fundamental",
        "arti": "Kemampuan manajemen perusahaan dalam mencetak laba bersih dari setiap modal pemegang saham yang dikelolanya.",
        "tips": "Carilah perusahaan dengan ROE konsisten di atas 15%. Ini tanda bahwa bisnis tersebut memiliki mesin pencetak uang yang sangat efisien (seperti BBCA, BBRI)."
    },
    "Debt-to-Equity Ratio (DER)": {
        "kategori": "Analisis Fundamental",
        "arti": "Rasio perbandingan antara total utang berbunga perusahaan dengan total modal bersihnya.",
        "tips": "DER di bawah 100% (atau 1.0x) tergolong aman. Jika DER di atas 200-300%, perusahaan memiliki tumpukan utang yang berat dan berisiko jika suku bunga naik."
    },
    "Dividend Yield (Imbal Hasil Dividen)": {
        "kategori": "Analisis Fundamental",
        "arti": "Persentase keuntungan tunai yang dibagikan perusahaan kepada pemegang saham dibandingkan dengan harga saham saat ini.",
        "tips": "Dividend Yield di atas 5-8% setahun tergolong sangat menarik karena lebih tinggi dari bunga deposito bank biasa!"
    },
    "Skor Fundamental Terpadu": {
        "kategori": "Analisis Fundamental",
        "arti": "Skor kesehatan bisnis menyeluruh (0 sampai 100) yang dievaluasi otomatis oleh software berdasarkan laba, valuasi, rasio utang, dan kestabilan kas.",
        "tips": "Skor di atas 70 menandakan perusahaan mapan berfundamental sehat. Skor di bawah 40 patut diwaspadai karena kondisi finansialnya lemah."
    },

    # --- PORTOFOLIO & PAPER TRADING ---
    "Paper Trading": {
        "kategori": "Portofolio",
        "arti": "Simulasi jual beli saham menggunakan dana virtual (bukan uang sungguhan) dengan harga pasar sebenarnya secara langsung.",
        "tips": "Sangat disarankan bagi pemula untuk berlatih di Paper Trading minimal 2-4 minggu sampai terbiasa disiplin memasang Stop Loss sebelum memakai uang tabungan riil."
    },
    "Floating PnL (Unrealized Profit/Loss)": {
        "kategori": "Portofolio",
        "arti": "Keuntungan atau kerugian yang saat ini sedang berjalan karena posisi saham masih disimpan (belum dijual).",
        "tips": "Floating profit belum menjadi uang nyata sebelum Anda menekan tombol 'Jual' untuk menguncinya!"
    },
    "Realized PnL": {
        "kategori": "Portofolio",
        "arti": "Keuntungan atau kerugian yang sudah resmi menjadi saldo kas karena saham sudah selesai dijual.",
        "tips": "Fokus pada pertumbuhan konsisten Realized PnL dari bulan ke bulan."
    }
}


# ==========================================================
# FUNGSI RENDER MENU PENJELASAN UNTUK SETIAP BAGIAN SOFTWARE
# ==========================================================

def render_header_guide():
    """Penjelasan ringkas di bawah Metric Bar Header."""
    with st.expander("📖 Panduan Singkat Membaca Kartu Angka & Sinyal di Atas (Khusus Pemula)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **🏆 360° Overall Grade (A+, A, B, C, D):**
            - **Grade A+ / A**: Kondisi prima. Teknikal sedang Bullish, Fundamental sehat, dan Berita mendukung.
            - **Grade B**: Bagus, namun disarankan beli secara bertahap / selektif.
            - **Grade C / D**: Sebaiknya tunggu (*Wait & See*) atau hindari karena risiko penurunan masih tinggi.
            """)
        with c2:
            st.markdown("""
            **🛑 Level Stop Loss & Target Profit (TP1):**
            - **Stop Loss (SL)**: Batas harga pengaman. Jika harga turun menyentuh angka ini, Anda wajib keluar agar modal terlindungi dari kerugian besar.
            - **Target Profit (TP1)**: Sasaran kenaikan harga terdekat untuk mulai mencairkan keuntungan (cuan).
            """)
        with c3:
            st.markdown("""
            **🎯 Konsensus Analis & Skor Fundamental:**
            - **Konsensus Analis**: Rata-rata pendapat para analis riset sekuritas profesional dunia (apakah merekomendasikan Buy, Hold, atau Sell).
            - **Skor Fundamental**: Angka 0-100 mengukur kesehatan finansial emiten (laba, utang, dan valuasi harga saham).
            """)


def render_scanner_guide():
    """Penjelasan di bawah Radar Scanner Pasar."""
    with st.expander("📖 Penjelasan Istilah Tabel Radar Scanner & Tips Memilih Saham (Khusus Pemula)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **💰 Kolom 'Modal 1 Lot':**
            - Menunjukkan berapa rupiah / dolar uang yang Anda butuhkan untuk membeli 1 satuan saham tersebut.
            - Saham Indonesia dihitung 100 lembar.
            - Jika tertulis Rp 35.000, artinya dengan uang Rp 35.000 saja Anda sudah bisa menjadi pemegang saham resmi perusahaan tersebut!
            """)
        with c2:
            st.markdown("""
            **🔥 Kolom 'Volume Surge' & 'RSI 14':**
            - **Volume Surge**: Menandakan transaksi mendadak melonjak ramai. Sering kali ini jejak investor besar / bandar sedang mengumpulkan barang.
            - **RSI 14**: Nilai 30-50 biasanya adalah area pemantulan harga (*reversal*). Nilai di atas 70 menandakan harga sudah terlalu tinggi (*overbought*).
            """)
        with c3:
            st.markdown("""
            **🚀 Kolom 'Rekomendasi' & 'Skor Peluang':**
            - **STRONG BUY**: Semua indikator searah (tren naik + volume besar). Peluang terbaik untuk masuk.
            - **WAIT / NETRAL**: Pasar masih ragu, lebih baik sabar menunggu konfirmasi berikutnya.
            - **EXIT / WASPADA**: Tren sedang patah turun, hindari membeli saham ini.
            """)


def render_chart_guide():
    """Penjelasan di bawah Grafik Candlestick & Indikator Teknikal."""
    with st.expander("📖 Kamus & Cara Membaca Grafik Lilin (Candlestick) & Garis Indikator (Khusus Pemula)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **🕯️ Candlestick (Lilin Harga):**
            - **Lilin Hijau**: Harga ditutup lebih tinggi dari pembukaan (pembeli mendominasi).
            - **Lilin Merah**: Harga ditutup turun dari pembukaan (penjual menekan harga).
            - **Garis Ekor Bawah Lilin**: Menunjukkan perlawanan beli yang menolak harga turun lebih dalam.
            """)
        with c2:
            st.markdown("""
            **📉 Garis Rata-Rata EMA & SMA 200:**
            - **EMA 9 (Oranye) & EMA 21 (Biru)**: Menunjukkan arah tren cepat. Jika garis oranye berada di atas garis biru, harga sedang dalam momentum naik kencang.
            - **EMA 50 (Ungu) & SMA 200 (Putih Putus-putus)**: Benteng penahan tren utama. Selama harga berada di atas garis-garis ini, saham tergolong aman untuk dibeli.
            """)
        with c3:
            st.markdown("""
            **🌊 Bollinger Bands, VWAP & RSI:**
            - **Bollinger Bands**: Pita biru transparan. Jika harga menyentuh batas bawah pita, sering kali terjadi pantulan balik ke atas.
            - **VWAP (Kuning)**: Rata-rata harga tertimbang volume transaksi para pemain besar (institusi).
            - **RSI 14**: Garis ungu di panel paling bawah. Hindari membeli jika menyentuh garis merah atas (70).
            """)


def render_ai_guide():
    """Penjelasan di bawah Prediksi AI Machine Learning."""
    with st.expander("📖 Cara Memahami Hasil Prediksi Kecerdasan Buatan (AI) & Target Harga (Khusus Pemula)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **🤖 Arah Prediksi & Horison Waktu:**
            - **Horison Waktu**: Pilihan perkiraan ke depan (misal: 1 Hari = besok, 3 Hari = jangka pendek, 5 Hari = 1 minggu bursa).
            - **Prediksi AI**: Model Random Forest menganalisis perpaduan 11 indikator teknikal secara simultan untuk memprediksi probabilitas arah harga berikutnya.
            """)
        with c2:
            st.markdown("""
            **📊 Probabilitas Peluang & Akurasi Out-of-Sample:**
            - **Peluang Naik vs Turun**: Mengukur seberapa dominan sinyal kenaikan harga. Peluang di atas 60% tergolong sinyal yang meyakinkan.
            - **Akurasi Out-of-Sample**: Diuji pada data riil masa lalu yang belum pernah dilihat oleh AI untuk memastikan AI tidak sekadar menghafal (*overfitting*).
            """)
        with c3:
            st.markdown("""
            **🎯 Proyeksi Rentang Target Harga Nominal:**
            - **Target Harga**: Estimasi harga wajar terdekat berdasarkan proyeksi AI.
            - **Batas Atas (Bullish Target)**: Target optimis jika momentum kenaikan berlanjut kuat.
            - **Batas Bawah (Support Proteksi)**: Level batas bawah harga di mana Anda harus waspada jika ditembus.
            """)


def render_monte_carlo_guide():
    """Penjelasan di bawah Simulasi Monte Carlo & VaR."""
    with st.expander("📖 Penjelasan Simulasi 1.000 Jalur Masa Depan Monte Carlo & Value at Risk (VaR)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **🎲 Apa itu Simulasi Monte Carlo?**
            - Karena masa depan tidak ada yang tahu pasti, algoritma ini menjalankan **1.000 kali simulasi acak** pergerakan harga ke depan berdasarkan volatilitas dan riwayat harga saham ini.
            - Menghasilkan rentang skenario terbaik (Garis Hijau), skenario rata-rata (Garis Biru), dan skenario terburuk (Garis Merah).
            """)
        with c2:
            st.markdown("""
            **⚖️ Peluang Kena TP1 Dulu vs Kena SL Dulu:**
            - Memberitahu Anda secara statistik: dari 1.000 kali pengujian, berapa persen kemungkinan harga akan mencapai Target Profit duluan dibanding menyentuh Stop Loss duluan.
            - Jika peluang kena TP1 lebih besar dari 60%, setup perdagangan tergolong sangat menguntungkan.
            """)
        with c3:
            st.markdown("""
            **🛡️ Value at Risk (VaR 95%):**
            - Metrik standar manajemen risiko perbankan global.
            - Menunjukkan potensi kerugian maksimal yang mungkin terjadi dengan tingkat keyakinan 95%. Ini membantu Anda menyiapkan mental dan modal sebelum bertransaksi.
            """)


def render_fundamental_guide():
    """Penjelasan di bawah Analisis Fundamental Perusahaan."""
    with st.expander("📖 Kamus Istilah Keuangan & Kesehatan Perusahaan (Khusus Pemula)", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""
            **🏷️ Valuasi (Murah / Mahal):**
            - **P/E Ratio**: Semakin rendah angkanya (< 15x), semakin murah harga saham dibanding laba yang dihasilkan.
            - **PBV**: Perbandingan harga dengan kekayaan bersih. Nilai di bawah 1.0x menandakan saham dijual di bawah nilai aset bersihnya (diskon).
            """)
        with c2:
            st.markdown("""
            **📈 Efisiensi Bisnis:**
            - **ROE (Return on Equity)**: Seberapa lihai perusahaan mencetak laba dari modal sendiri. Angka di atas 15% adalah bisnis yang sangat hebat!
            - **Net Profit Margin**: Persentase keuntungan bersih dari seluruh omset penjualan.
            """)
        with c3:
            st.markdown("""
            **💳 Neraca & Beban Utang:**
            - **Debt-to-Equity (DER)**: Mengukur tumpukan utang dibanding modal. Di bawah 100% sangat aman. Jika di atas 200%, perusahaan banyak menanggung bunga utang.
            - **Current Ratio**: Kemampuan membayar utang jangka pendek dengan kas lancar. Di atas 1.5x tergolong aman.
            """)
        with c4:
            st.markdown("""
            **🎁 Bagi Hasil Dividen:**
            - **Dividend Yield**: Persentase bagi hasil tunai tahunan ke rekening Anda. Yield di atas 5% setahun lebih menguntungkan daripada bunga deposito perbankan biasa.
            """)


def render_news_guide():
    """Penjelasan di bawah Berita & Sentimen Makro."""
    with st.expander("📖 Pengaruh Berita & Sentimen Pasar terhadap Pergerakan Harga (Khusus Pemula)", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            **📰 Berita Spesifik Emiten & Sentimen:**
            - Label **POSITIF (Hijau)**: Berita baik seperti laba meningkat tajam, dividen besar, atau memenangkan proyek baru. Biasanya memicu kenaikan harga.
            - Label **WASPADA (Merah)**: Berita kurang baik seperti tuntutan hukum, penurunan laba, atau pengunduran diri direksi utama.
            - Label **NETRAL (Abu-abu)**: Laporan operasional rutin tanpa dampak dramatis.
            """)
        with c2:
            st.markdown("""
            **🌍 Pengaruh Berita Makroekonomi Dunia:**
            - **Suku Bunga (The Fed / Bank Indonesia)**: Jika suku bunga naik, pasar saham biasanya tertekan. Jika suku bunga dipangkas, pasar saham cenderung bergairah naik.
            - **Inflasi & Kurs Dolar**: Mempengaruhi harga bahan baku emiten ekspor dan impor.
            - Berita makro membantu Anda memahami mengapa seluruh bursa saham bisa kompak naik atau kompak merah.
            """)


def render_risk_guide():
    """Penjelasan di bawah Kalkulator Lot Aman & Manajemen Risiko."""
    with st.expander("📖 Rahasia Tidak Boncos: Aturan Emas Manajemen Risiko & Ukuran Lot (Khusus Pemula)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **🛡️ Aturan Risiko 1%–2% per Transaksi:**
            - Trader pemula sering gagal karena membeli saham dengan seluruh uangnya sekaligus (*All-In*).
            - Trader profesional hanya merelakan maksimal **1% sampai 2% total modal** jika tebakannya salah dan terkena Stop Loss.
            - Dengan aturan ini, Anda harus kalah 50 sampai 100 kali berturut-turut sebelum modal Anda habis (sesuatu yang hampir mustahil terjadi).
            """)
        with c2:
            st.markdown("""
            **⚖️ Rasio Risk-to-Reward (RRR Minimal 1:2):**
            - Jangan masuk ke saham yang potensi untungnya lebih kecil dari potensi ruginya.
            - Contoh RRR 1:2: Jika Anda siap menanggung risiko rugi Rp 100.000, maka target keuntungannya harus minimal Rp 200.000.
            - Dengan rasio ini, meskipun dari 10 kali trading Anda hanya menang 4 kali dan kalah 6 kali, total saldo akun Anda tetap bertambah untung!
            """)
        with c3:
            st.markdown("""
            **📦 Ukuran Posisi Aman (Berapa Lot Dibeli):**
            - Software ini otomatis menghitungkan berapa lot maksimal yang boleh Anda beli berdasarkan jarak Stop Loss Anda.
            - Jika jarak Stop Loss lebar, jumlah lot otomatis dikecilkan agar total risiko rupiah tetap terkunci aman dan tidak melebihi batas toleransi Anda.
            """)


def render_paper_trading_guide():
    """Penjelasan di bawah Portofolio Simulasi Paper Trading."""
    with st.expander("📖 Panduan Istilah Portofolio & Latihan Paper Trading (Khusus Pemula)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **💼 Saldo Kas vs Total Ekuitas:**
            - **Saldo Kas**: Uang tunai virtual Anda yang sedang menganggur dan siap dibelikan saham baru.
            - **Total Saldo Ekuitas**: Nilai keseluruhan kekayaan akun Anda (Saldo Kas + Nilai pasar seluruh saham yang sedang Anda pegang).
            """)
        with c2:
            st.markdown("""
            **📊 Floating PnL (Untung/Rugi Berjalan):**
            - *PnL = Profit and Loss*.
            - **Floating PnL**: Keuntungan atau kerugian dari saham yang masih Anda simpan. Nilainya akan terus berubah naik turun mengikuti harga pasar secara langsung.
            - Jika berwarna hijau (+), Anda sedang untung. Jika merah (-), Anda sedang minus.
            """)
        with c3:
            st.markdown("""
            **🎯 Kapan Harus Menekan Tombol 'Jual'?**
            - Tekan tombol **Jual** jika harga sudah mencapai **Target Profit (TP1)** untuk mengamankan keuntungan nyata ke saldo kas Anda (*Take Profit*).
            - Tekan tombol **Jual** jika harga menembus **Stop Loss (SL)** agar kerugian tidak bertambah dalam (*Cut Loss*).
            """)


def render_backtest_guide():
    """Penjelasan di bawah Statistik Backtesting."""
    with st.expander("📖 Cara Membaca Uji Coba Riwayat Strategi (Backtesting) (Khusus Pemula)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            **🎯 Win Rate (% Kemenangan):**
            - Persentase transaksi yang berakhir dengan keuntungan.
            - *Fakta mengejutkan*: Trader hebat dunia rata-rata hanya memiliki Win Rate 45%–55%. Kunci kekayaan mereka bukan selalu benar, melainkan untung besar saat menang, dan rugi sangat kecil saat kalah!
            """)
        with c2:
            st.markdown("""
            **📉 Max Drawdown (Penurunan Modal Terparah):**
            - Mengukur seberapa dalam modal Anda sempat merosot dari titik puncak sebelum bangkit kembali.
            - Max Drawdown yang baik adalah di bawah 15%–20%. Semakin kecil, strategi semakin nyaman dan tidak bikin stres.
            """)
        with c3:
            st.markdown("""
            **💰 Profit Factor & Total Return:**
            - **Profit Factor**: Total jumlah keuntungan kotor dibagi total jumlah kerugian kotor. Angka di atas 1.5 menandakan strategi yang sangat menguntungkan.
            - **Equity Curve**: Grafik pertumbuhan saldo dari awal sampai akhir periode. Grafik yang menanjak mulus ke kanan atas menandakan strategi yang konsisten.
            """)


def render_interactive_glossary():
    """Widget Pencarian Kamus Istilah Interaktif A-Z untuk Pemula."""
    st.markdown("### 📖 Kamus Istilah Saham & Pasar Modal Interaktif (A-Z)")
    st.markdown("Ketik nama istilah, indikator, atau singkatan apa saja di bawah ini untuk melihat arti dan tips praktisnya dalam bahasa sehari-hari:")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        search_query = st.text_input("🔍 Cari Istilah (contoh: Lot, RSI, Stop Loss, PE Ratio, Breakout, Bandar, VWAP):", value="").strip().lower()
    with col_s2:
        category_filter = st.selectbox(
            "Filter Berdasarkan Kategori:",
            options=["Semua Kategori", "Umum & Satuan", "Kondisi Pasar", "Analisis Teknikal", "Analisis Fundamental", "Manajemen Risiko", "AI & Kuantitatif", "Portofolio"]
        )

    matched_items = {}
    for term, data in GLOSSARY_TERMS.items():
        cat_match = (category_filter == "Semua Kategori") or (data["kategori"] == category_filter)
        query_match = (search_query in term.lower()) or (search_query in data["arti"].lower()) or (search_query in data["tips"].lower())
        if cat_match and (not search_query or query_match):
            matched_items[term] = data

    st.markdown(f"Menampilkan **{len(matched_items)}** istilah:")
    
    if not matched_items:
        st.info("Istilah tidak ditemukan. Coba ketik kata kunci lain seperti 'RSI', 'Lot', 'Stop Loss', atau 'Utang'.")
    else:
        for term, data in matched_items.items():
            with st.expander(f"📌 **{term}** — *[{data['kategori']}]*", expanded=(len(matched_items) <= 3)):
                st.markdown(f"**Arti Sederhana:** {data['arti']}")
                st.info(f"💡 **Tips untuk Pemula:** {data['tips']}")
