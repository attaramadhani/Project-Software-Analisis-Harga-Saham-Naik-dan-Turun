"""
data_loader.py
Modul penarik data pasar saham global dari Yahoo Finance (yfinance).
Mendukung saham Indonesia (IDX), Amerika Serikat (US), Kripto, Komoditas, dan Pasar Global.
"""

import yfinance as yf
import pandas as pd

# Daftar ratusan ticker populer yang sudah dikelompokkan dengan rapi
POPULAR_TICKERS = {
    "🇮🇩 Saham Modal Ringan Indonesia (< Rp 1.000 / Lot Murah)": {
        "GOTO.JK": "GoTo Gojek Tokopedia (GOTO)",
        "BUMI.JK": "Bumi Resources (BUMI)",
        "BRMS.JK": "Bumi Resources Minerals (BRMS)",
        "ELSA.JK": "Elnusa (ELSA)",
        "PWON.JK": "Pakuwon Jati (PWON)",
        "WIKA.JK": "Wijaya Karya (WIKA)",
        "PTPP.JK": "PP (Persero) Tbk",
        "KIJA.JK": "Kawasan Industri Jababeka (KIJA)",
        "DOID.JK": "Delta Dunia Makmur (DOID)",
        "BUKA.JK": "Bukalapak.com (BUKA)",
        "SCMA.JK": "Surya Citra Media (SCMA)",
        "MNCN.JK": "Media Nusantara Citra (MNCN)",
        "ENRG.JK": "Energi Mega Persada (ENRG)",
        "SMRA.JK": "Summarecon Agung (SMRA)",
        "ACES.JK": "Aspirasi Hidup Indonesia / Ace (ACES)",
    },
    "🇺🇸 Saham AS Terjangkau (Budget-Friendly < $30)": {
        "SOFI": "SoFi Technologies Inc.",
        "PLTR": "Palantir Technologies",
        "GRAB": "Grab Holdings Limited",
        "NIO": "NIO Inc. (Electric Vehicles)",
        "RIVN": "Rivian Automotive",
        "F": "Ford Motor Company",
        "HOOD": "Robinhood Markets Inc.",
        "SNAP": "Snap Inc. (Snapchat)",
        "INTC": "Intel Corporation",
        "PFE": "Pfizer Inc.",
        "AAL": "American Airlines Group",
        "CCL": "Carnival Corporation",
        "WBD": "Warner Bros. Discovery",
        "LCID": "Lucid Group Inc.",
    },
    "🌐 Saham Pertumbuhan Global (Asia & US Growth)": {
        "SE": "Sea Limited (Shopee & Garena)",
        "BABA": "Alibaba Group",
        "TSM": "Taiwan Semiconductor (TSMC)",
        "AMD": "Advanced Micro Devices",
        "COIN": "Coinbase Global",
        "ARM": "Arm Holdings plc",
        "U": "Unity Software Inc.",
        "RBLX": "Roblox Corporation",
        "BIDU": "Baidu Inc.",
    },
    "🇮🇩 Saham Indonesia - Perbankan & Finansial": {
        "BBCA.JK": "Bank Central Asia (BBCA)",
        "BBRI.JK": "Bank Rakyat Indonesia (BBRI)",
        "BMRI.JK": "Bank Mandiri (BMRI)",
        "BBNI.JK": "Bank Negara Indonesia (BBNI)",
        "BRIS.JK": "Bank Syariah Indonesia (BRIS)",
        "BBTN.JK": "Bank Tabungan Negara (BBTN)",
        "BDMN.JK": "Bank Danamon (BDMN)",
        "ARTO.JK": "Bank Jago (ARTO)",
    },
    "🇮🇩 Saham Indonesia - Energi, Tambang & Minyak": {
        "ADRO.JK": "Adaro Energy (ADRO)",
        "PTBA.JK": "Bukit Asam (PTBA)",
        "ITMG.JK": "Indo Tambangraya Megah (ITMG)",
        "BYAN.JK": "Bayan Resources (BYAN)",
        "PGAS.JK": "Perusahaan Gas Negara (PGAS)",
        "ANTM.JK": "Aneka Tambang (ANTM)",
        "INCO.JK": "Vale Indonesia (INCO)",
        "MDKA.JK": "Merdeka Copper Gold (MDKA)",
        "MEDC.JK": "Medco Energi (MEDC)",
        "AMMN.JK": "Amman Mineral Internasional (AMMN)",
        "BUMI.JK": "Bumi Resources (BUMI)",
        "MBMA.JK": "Merdeka Battery Materials (MBMA)",
    },
    "🇮🇩 Saham Indonesia - Konsumer, Kesehatan & Retail": {
        "ICBP.JK": "Indofood CBP Sukses Makmur (ICBP)",
        "INDF.JK": "Indofood Sukses Makmur (INDF)",
        "UNVR.JK": "Unilever Indonesia (UNVR)",
        "MYOR.JK": "Mayora Indah (MYOR)",
        "AMRT.JK": "Sumber Alfaria Trijaya / Alfamart (AMRT)",
        "ACES.JK": "Aspirasi Hidup Indonesia / Ace (ACES)",
        "MAPI.JK": "Mitra Adiperkasa (MAPI)",
        "KLBF.JK": "Kalbe Farma (KLBF)",
        "SIDO.JK": "Industri Jamu Sido Muncul (SIDO)",
        "MIKA.JK": "Mitra Keluarga Karyasehat (MIKA)",
        "CPIN.JK": "Charoen Pokphand Indonesia (CPIN)",
    },
    "🇮🇩 Saham Indonesia - Telko, Teknologi & Konglomerasi": {
        "TLKM.JK": "Telkom Indonesia (TLKM)",
        "ISAT.JK": "Indosat Ooredoo Hutchison (ISAT)",
        "EXCL.JK": "XL Axiata (EXCL)",
        "GOTO.JK": "GoTo Gojek Tokopedia (GOTO)",
        "ASII.JK": "Astra International (ASII)",
        "BREN.JK": "Barito Renewables (BREN)",
        "BRPT.JK": "Barito Pacific (BRPT)",
        "TPIA.JK": "Chandra Asri Petrochemical (TPIA)",
        "SMGR.JK": "Semen Indonesia (SMGR)",
        "JSMR.JK": "Jasa Marga (JSMR)",
        "BSDE.JK": "Bumi Serpong Damai (BSDE)",
        "CTRA.JK": "Ciputra Development (CTRA)",
    },
    "🇺🇸 Saham AS - Big Tech & Megacap": {
        "AAPL": "Apple Inc.",
        "NVDA": "NVIDIA Corporation",
        "MSFT": "Microsoft Corporation",
        "GOOGL": "Alphabet / Google",
        "AMZN": "Amazon.com Inc.",
        "META": "Meta Platforms",
        "TSLA": "Tesla Inc.",
        "SPY": "S&P 500 Index ETF",
        "QQQ": "Invesco QQQ (Nasdaq 100)",
    },
    "🇺🇸 Saham AS - AI, Semikonduktor & Growth": {
        "AMD": "Advanced Micro Devices",
        "PLTR": "Palantir Technologies",
        "TSM": "Taiwan Semiconductor (TSMC)",
        "AVGO": "Broadcom Inc.",
        "ARM": "Arm Holdings",
        "COIN": "Coinbase Global",
        "NFLX": "Netflix Inc.",
        "BABA": "Alibaba Group",
    },
    "🪙 Kripto & Komoditas Dunia": {
        "BTC-USD": "Bitcoin (USD)",
        "ETH-USD": "Ethereum (USD)",
        "SOL-USD": "Solana (USD)",
        "GC=F": "Emas Berjangka (Gold Futures)",
        "CL=F": "Minyak Mentah (Crude Oil)",
        "SI=F": "Perak Berjangka (Silver Futures)",
    },
    "🌐 Indeks Saham Dunia": {
        "^JKSE": "IHSG (Indonesia Composite)",
        "^GSPC": "S&P 500 (US)",
        "^DJI": "Dow Jones Industrial Average",
        "^IXIC": "Nasdaq Composite",
        "^N225": "Nikkei 225 (Jepang)",
        "^HSI": "Hang Seng (Hong Kong)",
        "^FTSE": "FTSE 100 (Inggris)",
    }
}

# Daftar kode saham Indonesia 4-huruf yang umum untuk auto-detect
COMMON_IDX_CODES = {
    'BBCA', 'BBRI', 'BMRI', 'BBNI', 'BRIS', 'ASII', 'TLKM', 'AMMN', 'BREN', 'TPIA',
    'BYAN', 'GOTO', 'KLBF', 'UNVR', 'ICBP', 'INDF', 'CPIN', 'MDKA', 'ANTM', 'INCO',
    'MEDC', 'ADRO', 'PTBA', 'ITMG', 'PGAS', 'MYOR', 'AMRT', 'MIDI', 'ACES', 'MAPI',
    'ISAT', 'EXCL', 'BUKA', 'EMTK', 'SMGR', 'INTP', 'BRPT', 'ESSA', 'AKRA', 'UNTR',
    'JSMR', 'CTRA', 'BSDE', 'SMRA', 'PWON', 'MIKA', 'HEAL', 'SIDO', 'BBTN', 'BDMN',
    'BUMI', 'ARTO', 'MBMA', 'CUAN', 'BULL', 'DOID', 'HRUM', 'INDY', 'JPFA', 'MARK',
    'MNCN', 'MTEL', 'PGEO', 'SCMA', 'SSMS', 'TBIG', 'TINS', 'TOWR', 'WIKA', 'PTPP'
}


def clean_ticker_symbol(user_input: str) -> str:
    """
    Membersihkan dan memformat kode ticker secara cerdas.
    Jika user mengetik saham Indonesia seperti 'BBCA' atau 'GOTO' tanpa '.JK',
    sistem akan otomatis menambahkan '.JK'.
    """
    raw = user_input.strip().upper()
    if not raw:
        return "BBCA.JK"
        
    # Jika sudah berakhiran .JK atau mengandung karakter simbol khusus (seperti ^, =, -)
    if raw.endswith('.JK') or any(char in raw for char in ['^', '=', '-']):
        return raw
        
    # Jika 4 huruf dan ada di daftar saham Indonesia yang umum
    if raw in COMMON_IDX_CODES:
        return f"{raw}.JK"
        
    # Jika user mengetik kode saham dengan format bursa lain, biarkan apa adanya
    return raw


# Kamus pencocokan nama perusahaan lengkap
COMPANY_NAME_LOOKUP = {}
for cat, tickers_dict in POPULAR_TICKERS.items():
    for sym, c_name in tickers_dict.items():
        COMPANY_NAME_LOOKUP[sym] = c_name
        if sym.endswith('.JK'):
            COMPANY_NAME_LOOKUP[sym.replace('.JK', '')] = c_name

EXTRA_NAMES = {
    # Saham Terjangkau / Modal Kecil Indonesia
    "GOTO.JK": "GoTo Gojek Tokopedia (GOTO)",
    "BUMI.JK": "Bumi Resources (BUMI)",
    "BRMS.JK": "Bumi Resources Minerals (BRMS)",
    "ELSA.JK": "Elnusa (ELSA)",
    "PWON.JK": "Pakuwon Jati (PWON)",
    "WIKA.JK": "Wijaya Karya (WIKA)",
    "PTPP.JK": "PP (Persero) Tbk",
    "KIJA.JK": "Kawasan Industri Jababeka (KIJA)",
    "DOID.JK": "Delta Dunia Makmur (DOID)",
    "BUKA.JK": "Bukalapak.com (BUKA)",
    "SCMA.JK": "Surya Citra Media (SCMA)",
    "MNCN.JK": "Media Nusantara Citra (MNCN)",
    "ENRG.JK": "Energi Mega Persada (ENRG)",
    "PSAB.JK": "J Resources Asia Pasifik (PSAB)",
    "SMRA.JK": "Summarecon Agung (SMRA)",
    "ACES.JK": "Aspirasi Hidup Indonesia / Ace (ACES)",
    "BTPS.JK": "Bank BTPN Syariah (BTPS)",
    "BTPN.JK": "Bank BTPN Tbk",
    "HRUM.JK": "Harum Energy (HRUM)",
    "INDY.JK": "Indika Energy (INDY)",
    "CUAN.JK": "Petrindo Jaya Kreasi (CUAN)",
    "PGEO.JK": "Pertamina Geothermal Energy (PGEO)",
    "UNTR.JK": "United Tractors (UNTR)",
    "AKRA.JK": "AKR Corporindo (AKRA)",
    "TINS.JK": "Timah Tbk (TINS)",
    # Saham Luar Negeri Terjangkau (< $30)
    "SOFI": "SoFi Technologies Inc.",
    "PLTR": "Palantir Technologies",
    "GRAB": "Grab Holdings Limited",
    "NIO": "NIO Inc. (Electric Vehicles)",
    "RIVN": "Rivian Automotive",
    "F": "Ford Motor Company",
    "HOOD": "Robinhood Markets Inc.",
    "SNAP": "Snap Inc. (Snapchat)",
    "INTC": "Intel Corporation",
    "PFE": "Pfizer Inc.",
    "AAL": "American Airlines Group",
    "CCL": "Carnival Corporation",
    "WBD": "Warner Bros. Discovery",
    "LCID": "Lucid Group Inc.",
    # Saham Pertumbuhan Global
    "SE": "Sea Limited (Shopee & Garena)",
    "BABA": "Alibaba Group",
    "TSM": "Taiwan Semiconductor (TSMC)",
    "AMD": "Advanced Micro Devices",
    "COIN": "Coinbase Global",
    "ARM": "Arm Holdings plc",
    "U": "Unity Software Inc.",
    "RBLX": "Roblox Corporation",
    "BIDU": "Baidu Inc.",
    "SMCI": "Super Micro Computer Inc.",
    "CRWD": "CrowdStrike Holdings",
    "SNOW": "Snowflake Inc.",
    "CRM": "Salesforce Inc.",
    "QCOM": "Qualcomm Inc.",
    "TXN": "Texas Instruments Inc."
}
COMPANY_NAME_LOOKUP.update(EXTRA_NAMES)


def get_company_name(ticker: str) -> str:
    """
    Mengembalikan nama lengkap perusahaan dari simbol ticker.
    Contoh: 'BBCA.JK' -> 'Bank Central Asia (BBCA)'
    """
    clean = clean_ticker_symbol(ticker)
    if clean in COMPANY_NAME_LOOKUP:
        return COMPANY_NAME_LOOKUP[clean]
    base = clean.replace('.JK', '')
    if base in COMPANY_NAME_LOOKUP:
        return COMPANY_NAME_LOOKUP[base]
    try:
        t = yf.Ticker(clean)
        info = t.info
        name = info.get('longName') or info.get('shortName')
        if name:
            COMPANY_NAME_LOOKUP[clean] = name
            return name
    except Exception:
        pass
    return clean



def load_stock_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Mengunduh data OHLCV dari Yahoo Finance dengan pembersihan data.
    """
    ticker_clean = clean_ticker_symbol(ticker)
    
    # Penyesuaian batas intraday Yahoo Finance (maksimal 60 hari)
    if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "1h"]:
        if period in ["1y", "2y", "5y", "max"]:
            period = "1mo"
            
    t = yf.Ticker(ticker_clean)
    df = t.history(period=period, interval=interval, auto_adjust=True)
    
    if df is None or df.empty:
        # Coba fallback jika user mengetik 4 huruf yang mungkin saham IDX tapi belum ada akhiran .JK
        if not ticker_clean.endswith('.JK') and len(ticker_clean) == 4 and ticker_clean.isalpha():
            fallback_ticker = f"{ticker_clean}.JK"
            t_fallback = yf.Ticker(fallback_ticker)
            df = t_fallback.history(period=period, interval=interval, auto_adjust=True)
            if df is not None and not df.empty:
                ticker_clean = fallback_ticker
                
    if df is None or df.empty:
        raise ValueError(f"Data tidak ditemukan untuk simbol '{ticker}'. Pastikan kode ticker terdaftar di Yahoo Finance (contoh saham Indonesia: BBCA.JK atau saham US: AAPL).")
        
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom {col} tidak ditemukan pada data ticker {ticker_clean}.")
            
    df = df[required_cols].dropna()
    
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
        
    df.index.name = "Datetime"
    return df


def get_ticker_info(ticker: str) -> dict:
    """
    Mengambil informasi dasar perusahaan dan harga terkini.
    """
    ticker_clean = clean_ticker_symbol(ticker)
    t = yf.Ticker(ticker_clean)
    info = {}
    try:
        raw_info = t.info
        info['name'] = raw_info.get('longName') or raw_info.get('shortName') or ticker_clean
        info['currency'] = raw_info.get('currency', 'USD')
        info['sector'] = raw_info.get('sector', 'N/A')
        info['industry'] = raw_info.get('industry', 'N/A')
        info['current_price'] = raw_info.get('currentPrice') or raw_info.get('regularMarketPrice')
        info['previous_close'] = raw_info.get('previousClose')
        info['day_high'] = raw_info.get('dayHigh')
        info['day_low'] = raw_info.get('dayLow')
        info['market_cap'] = raw_info.get('marketCap')
    except Exception:
        info['name'] = ticker_clean
        info['currency'] = 'IDR' if ticker_clean.endswith('.JK') else 'USD'
        info['current_price'] = None
        
    return info
