"""
news_loader.py
Modul penarik berita real-time dan analisis sentimen pasar:
1. Berita spesifik saham (Yahoo Finance News & Google News RSS)
2. Berita makroekonomi global (The Fed, Suku Bunga, Inflasi, Minyak, Geopolitik)
"""

import yfinance as yf
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
import re


def detect_sentiment(text: str) -> dict:
    """
    Analisis sentimen berbasis kata kunci finansial (Bahasa Indonesia & Bahasa Inggris).
    """
    text_lower = text.lower()
    
    positive_words = [
        'laba', 'naik', 'profit', 'dividen', 'rekor', 'lonjakan', 'optimis', 'tumbuh',
        'gain', 'surge', 'jump', 'bullish', 'expansion', 'beat', 'soar', 'record',
        'upgrade', 'buy', 'growth', 'strong', 'rally', 'positive'
    ]
    
    negative_words = [
        'rugi', 'turun', 'anjlok', 'gugatan', 'koreksi', 'inflasi', 'sanksi', 'waspada',
        'drop', 'fall', 'plunge', 'bearish', 'lawsuit', 'investigation', 'downgrade',
        'miss', 'loss', 'debt', 'cut', 'slump', 'weak', 'risk', 'warning'
    ]
    
    pos_score = sum(1 for w in positive_words if re.search(r'\b' + re.escape(w) + r'\b', text_lower))
    neg_score = sum(1 for w in negative_words if re.search(r'\b' + re.escape(w) + r'\b', text_lower))
    
    if pos_score > neg_score:
        return {"label": "POSITIF / BULLISH", "color": "#00E676", "score": pos_score}
    elif neg_score > pos_score:
        return {"label": "WASPADA / BEARISH", "color": "#FF5252", "score": -neg_score}
    else:
        return {"label": "NETRAL / INFORMASI", "color": "#BDBDBD", "score": 0}


def fetch_google_news_rss(query: str, max_results: int = 8) -> list:
    """
    Mengambil berita terkini dari Google News RSS Feed.
    Gratis, real-time, dan tanpa butuh API key.
    """
    articles = []
    try:
        encoded_query = urllib.parse.quote(query)
        # Menyesuaikan regional jika query bahasa Indonesia
        if "saham" in query.lower() or ".jk" in query.lower():
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=id&gl=ID&ceid=ID:id"
        else:
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        items = root.findall('.//item')[:max_results]
        
        for item in items:
            title = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else "#"
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            source = item.find('source').text if item.find('source') is not None else "Google News"
            
            sentiment = detect_sentiment(title)
            
            articles.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "source": source,
                "sentiment": sentiment
            })
    except Exception as e:
        pass
        
    return articles


from data_loader import clean_ticker_symbol


def get_stock_news(ticker: str) -> list:
    """
    Mengambil berita spesifik terkait saham/perusahaan yang sedang dianalisis.
    Mengkombinasikan Yahoo Finance News dan Google News RSS.
    """
    ticker_clean = clean_ticker_symbol(ticker)
    articles = []
    
    # 1. Coba ambil dari Yahoo Finance News (sangat bagus untuk saham US/Global)
    try:
        t = yf.Ticker(ticker_clean)
        raw_news = t.news if hasattr(t, 'news') else []
        for n in raw_news[:8]:
            # Kompatibilitas struktur yfinance v1.7+
            content = n.get('content', n)
            title = content.get('title')
            if not title:
                continue
            provider = content.get('provider', {})
            source = provider.get('displayName') if isinstance(provider, dict) else str(provider)
            link_obj = content.get('clickThroughUrl') or content.get('canonicalUrl') or {}
            link = link_obj.get('url', '#') if isinstance(link_obj, dict) else (n.get('link', '#'))
            pub_date = content.get('pubDate', '')
            
            articles.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "source": source or "Yahoo Finance",
                "sentiment": detect_sentiment(title)
            })
    except Exception:
        pass
        
    # 2. Jika berita sedikit atau untuk saham Indonesia (.JK), lengkapi dengan Google News
    if len(articles) < 4:
        query = f"saham {ticker_clean.replace('.JK', '')}" if ticker_clean.endswith('.JK') else f"{ticker_clean} stock news"
        rss_articles = fetch_google_news_rss(query, max_results=8)
        # Gabungkan dan buang duplikat berdasarkan judul
        existing_titles = {a['title'] for a in articles}
        for ra in rss_articles:
            if ra['title'] not in existing_titles:
                articles.append(ra)
                existing_titles.add(ra['title'])
                
    return articles[:10]


def get_macro_news() -> list:
    """
    Mengambil berita pasar global & makroekonomi (The Fed, Suku Bunga, Inflasi, Minyak, S&P 500).
    """
    macro_query = "stock market Fed interest rate inflation"
    return fetch_google_news_rss(macro_query, max_results=6)
