"""
paper_trading.py
Modul Simulator Portofolio Paper Trading (Uang Virtual).
Menyediakan fasilitas latihan transaksi tanpa risiko kehilangan uang riil.
Data portofolio tersimpan aman secara persisten di file JSON lokal.
"""

import json
import os
from datetime import datetime
import pandas as pd

PORTFOLIO_FILE = "paper_portfolio.json"


def get_default_portfolio(initial_balance: float = 50000000.0) -> dict:
    return {
        "initial_balance": initial_balance,
        "cash": initial_balance,
        "positions": [],
        "history": []
    }


def load_portfolio(initial_balance: float = 50000000.0) -> dict:
    """Memuat data portofolio dari file JSON lokal."""
    if not os.path.exists(PORTFOLIO_FILE):
        port = get_default_portfolio(initial_balance)
        save_portfolio(port)
        return port
    try:
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        port = get_default_portfolio(initial_balance)
        save_portfolio(port)
        return port


def save_portfolio(portfolio: dict):
    """Menyimpan data portofolio ke file JSON lokal."""
    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        json.dump(portfolio, f, indent=2, default=str)


def reset_portfolio(initial_balance: float = 50000000.0) -> dict:
    """Mereset saldo dan riwayat portofolio simulasi."""
    port = get_default_portfolio(initial_balance)
    save_portfolio(port)
    return port


def execute_buy(
    ticker: str,
    price: float,
    shares: int,
    sl: float,
    tp: float,
    is_idx: bool = True
) -> dict:
    """
    Membeli saham virtual dan mencatatnya ke portofolio.
    """
    port = load_portfolio()
    cost = price * shares
    
    if cost > port["cash"]:
        return {
            "status": "error",
            "message": f"Saldo tunai tidak mencukupi! Butuh Rp {cost:,.0f}, saldo Anda Rp {port['cash']:,.0f}."
        }
        
    port["cash"] -= cost
    lot_count = shares // 100 if is_idx else shares
    
    # Cek jika ticker sudah ada di posisi terbuka
    existing = False
    for pos in port["positions"]:
        if pos["ticker"] == ticker:
            # Rata-ratakan harga beli
            total_shares = pos["shares"] + shares
            pos["buy_price"] = ((pos["buy_price"] * pos["shares"]) + cost) / total_shares
            pos["shares"] = total_shares
            pos["lots"] = total_shares // 100 if is_idx else total_shares
            pos["sl"] = sl
            pos["tp"] = tp
            existing = True
            break
            
    if not existing:
        port["positions"].append({
            "ticker": ticker,
            "buy_price": price,
            "shares": shares,
            "lots": lot_count,
            "sl": sl,
            "tp": tp,
            "is_idx": is_idx,
            "buy_date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
    save_portfolio(port)
    return {"status": "success", "message": f"Berhasil membeli {lot_count:,} {'Lot' if is_idx else 'Lbr'} {ticker} @ {price:,.2f}!"}


def execute_sell(ticker: str, current_price: float, reason: str = "Ambil Untung / Manual") -> dict:
    """
    Menjual seluruh posisi saham virtual dan mencatat PnL ke riwayat.
    """
    port = load_portfolio()
    found_idx = None
    
    for idx, pos in enumerate(port["positions"]):
        if pos["ticker"] == ticker:
            found_idx = idx
            break
            
    if found_idx is None:
        return {"status": "error", "message": f"Posisi {ticker} tidak ditemukan di portofolio."}
        
    pos = port["positions"].pop(found_idx)
    proceeds = current_price * pos["shares"]
    cost = pos["buy_price"] * pos["shares"]
    pnl = proceeds - cost
    return_pct = ((current_price - pos["buy_price"]) / pos["buy_price"]) * 100.0
    
    port["cash"] += proceeds
    port["history"].append({
        "ticker": ticker,
        "buy_date": pos["buy_date"],
        "sell_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "buy_price": pos["buy_price"],
        "sell_price": current_price,
        "shares": pos["shares"],
        "lots": pos["lots"],
        "pnl": round(pnl, 2),
        "return_pct": round(return_pct, 2),
        "reason": reason
    })
    
    save_portfolio(port)
    return {"status": "success", "message": f"Berhasil menjual {ticker} @ {current_price:,.2f} (PnL: {pnl:+,.0f} / {return_pct:+.2f}%)"}
