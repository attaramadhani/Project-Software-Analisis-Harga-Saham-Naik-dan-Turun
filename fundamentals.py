"""
fundamentals.py
Modul Analisis Fundamental Perusahaan, Valuasi, Kesehatan Finansial, dan Konsensus Analis.
Data ditarik secara gratis dan komprehensif melalui Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
from data_loader import clean_ticker_symbol


def get_fundamental_data(ticker: str) -> dict:
    """
    Mengambil data fundamental lengkap perusahaan:
    - Valuasi (P/E, Forward P/E, PBV, PEG)
    - Profitabilitas (ROE, ROA, Profit Margin, Operating Margin)
    - Kesehatan Neraca & Utang (Debt-to-Equity, Free Cashflow, Current Ratio)
    - Dividen (Yield, Payout Ratio)
    - Konsensus Analis (Target Price, Recommendation)
    - Skor Kesehatan Fundamental (0 - 100)
    """
    ticker_clean = clean_ticker_symbol(ticker)
    t = yf.Ticker(ticker_clean)
    info = t.info if hasattr(t, 'info') else {}
    
    # 1. Valuasi
    pe_trailing = info.get('trailingPE')
    pe_forward = info.get('forwardPE')
    pbv = info.get('priceToBook')
    peg = info.get('pegRatio')
    ev_ebitda = info.get('enterpriseToEbitda')
    
    # 2. Profitabilitas & Efisiensi
    roe = info.get('returnOnEquity')  # e.g. 0.218 -> 21.8%
    roa = info.get('returnOnAssets')
    profit_margin = info.get('profitMargins')
    operating_margin = info.get('operatingMargins')
    gross_margin = info.get('grossMargins')
    
    # 3. Neraca, Utang, & Arus Kas
    debt_to_equity = info.get('debtToEquity')  # e.g. 78.4 -> 78.4%
    current_ratio = info.get('currentRatio')
    free_cashflow = info.get('freeCashflow')
    total_cash = info.get('totalCash')
    total_debt = info.get('totalDebt')
    
    # 4. Pertumbuhan & Dividen
    revenue_growth = info.get('revenueGrowth')  # e.g. 0.16 -> 16%
    earnings_growth = info.get('earningsGrowth')
    dividend_yield = info.get('dividendYield')  # e.g. 5.69 or 0.0569
    dividend_rate = info.get('dividendRate')
    payout_ratio = info.get('payoutRatio')
    
    # 5. Konsensus Analis
    target_price = info.get('targetMeanPrice')
    target_high = info.get('targetHighPrice')
    target_low = info.get('targetLowPrice')
    analyst_opinion = info.get('recommendationKey', 'N/A')
    num_analysts = info.get('numberOfAnalystOpinions', 0)
    
    # 6. Hitung Skor Kesehatan Fundamental (0 - 100)
    score = 50  # base score
    score_reasons = []
    
    # Evaluasi ROE (Profitabilitas)
    if roe is not None:
        if roe >= 0.15:
            score += 15
            score_reasons.append(f"✅ ROE sangat prima ({roe*100:.1f}%), perusahaan sangat efisien menghasilkan laba.")
        elif roe >= 0.08:
            score += 5
            score_reasons.append(f"ℹ️ ROE cukup baik ({roe*100:.1f}%).")
        else:
            score -= 10
            score_reasons.append(f"⚠️ ROE rendah ({roe*100:.1f}%), efisiensi modal di bawah rata-rata.")
            
    # Evaluasi Margin Laba Bersih
    if profit_margin is not None:
        if profit_margin >= 0.15:
            score += 15
            score_reasons.append(f"✅ Profit margin tebal ({profit_margin*100:.1f}%), memiliki 'economic moat' yang kuat.")
        elif profit_margin > 0.05:
            score += 5
        else:
            score -= 10
            score_reasons.append(f"⚠️ Profit margin tipis ({profit_margin*100:.1f}%).")
            
    # Evaluasi Utang (Debt-to-Equity)
    # Catatan: Saham perbankan umumnya tidak memakai rasio DER tradisional
    if debt_to_equity is not None:
        if debt_to_equity <= 100.0:
            score += 10
            score_reasons.append(f"✅ Rasio utang sehat (DER: {debt_to_equity:.1f}%).")
        elif debt_to_equity > 200.0:
            score -= 15
            score_reasons.append(f"⚠️ Utang cukup tinggi (DER: {debt_to_equity:.1f}%), waspada beban bunga.")
            
    # Evaluasi Pertumbuhan Pendapatan
    if revenue_growth is not None:
        if revenue_growth > 0.10:
            score += 10
            score_reasons.append(f"✅ Pendapatan bertumbuh positif (+{revenue_growth*100:.1f}% YoY).")
        elif revenue_growth < 0:
            score -= 10
            score_reasons.append(f"⚠️ Pendapatan menyusut ({revenue_growth*100:.1f}% YoY).")
            
    # Evaluasi Valuasi P/E
    if pe_trailing is not None:
        if pe_trailing < 0:
            score -= 15
            score_reasons.append("⚠️ Perusahaan membukukan kerugian (P/E negatif).")
        elif 0 < pe_trailing <= 18.0:
            score += 10
            score_reasons.append(f"✅ Valuasi P/E menarik & terjangkau ({pe_trailing:.1f}x).")
        elif pe_trailing > 45.0:
            score -= 5
            score_reasons.append(f"ℹ️ Valuasi P/E premium/tinggi ({pe_trailing:.1f}x), pasar menaruh ekspektasi pertumbuhan tinggi.")
            
    score = max(0, min(100, score))
    
    # Label Kategori Fundamental
    if score >= 75:
        health_label = "SANGAT SEHAT (BLUE CHIP EXCELLENT)"
        health_color = "#00E676"
    elif score >= 55:
        health_label = "SEHAT / MODERAT (GOOD QUALITY)"
        health_color = "#29B6F6"
    elif score >= 40:
        health_label = "CUKUP / HATI-HATI (AVERAGE)"
        health_color = "#FFD54F"
    else:
        health_label = "BERISIKO TINGGI (HIGH RISK)"
        health_color = "#FF5252"
        
    return {
        "status": "success",
        "ticker": ticker,
        "name": info.get('longName', ticker),
        "sector": info.get('sector', 'N/A'),
        "industry": info.get('industry', 'N/A'),
        "country": info.get('country', 'N/A'),
        "score": score,
        "health_label": health_label,
        "health_color": health_color,
        "score_reasons": score_reasons,
        "valuation": {
            "pe_trailing": pe_trailing,
            "pe_forward": pe_forward,
            "pbv": pbv,
            "peg": peg,
            "ev_ebitda": ev_ebitda
        },
        "profitability": {
            "roe": roe,
            "roa": roa,
            "profit_margin": profit_margin,
            "operating_margin": operating_margin,
            "gross_margin": gross_margin
        },
        "balance_sheet": {
            "debt_to_equity": debt_to_equity,
            "current_ratio": current_ratio,
            "free_cashflow": free_cashflow,
            "total_cash": total_cash,
            "total_debt": total_debt
        },
        "growth_dividend": {
            "revenue_growth": revenue_growth,
            "earnings_growth": earnings_growth,
            "dividend_yield": dividend_yield,
            "dividend_rate": dividend_rate,
            "payout_ratio": payout_ratio
        },
        "analyst_consensus": {
            "target_mean": target_price,
            "target_high": target_high,
            "target_low": target_low,
            "opinion": analyst_opinion.replace('_', ' ').upper(),
            "num_analysts": num_analysts
        }
    }
