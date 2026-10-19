"""
risk_manager.py
Modul Manajemen Risiko & Pelindung Modal (Capital Preservation Engine).
Inilah modul paling krusial untuk mencegah 'kerugian yang sangat besar' dan menjaga konsistensi profit.
"""

def calculate_risk_plan(
    capital: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
    target_price_1: float,
    target_price_2: float,
    is_idx: bool = True
) -> dict:
    """
    Menghitung ukuran posisi (position sizing) yang aman secara matematis.
    
    Formula:
    1. Uang Maksimal Berani Rugi = Capital * (Risk % / 100)
    2. Kerugian per Lembar = Entry Price - Stop Loss Price
    3. Lembar Saham Maksimal = Uang Maksimal Berani Rugi / Kerugian per Lembar
    4. Jika Saham Indonesia: 1 Lot = 100 lembar
    
    Bahkan jika harga jatuh dan menyentuh Stop Loss, kerugian portofolio
    DIJAMIN HANYA SEBESAR RISK PERCENT (misal 1% atau 2%).
    """
    if capital <= 0 or entry_price <= 0:
        return {"status": "error", "message": "Modal dan harga entry harus lebih besar dari 0."}
        
    if stop_loss_price >= entry_price:
        return {
            "status": "error",
            "message": "Stop Loss harus berada di bawah harga Entry untuk posisi beli (Long)."
        }
        
    # Uang maksimal yang ditoleransi untuk rugi
    max_risk_amount = capital * (risk_percent / 100.0)
    
    # Risiko per lembar saham
    risk_per_share = entry_price - stop_loss_price
    
    # Hitung jumlah lembar saham aman
    safe_shares = int(max_risk_amount / risk_per_share)
    
    lot_size = 100 if is_idx else 1
    unit_name = "Lot (100 lbr)" if is_idx else "Lembar Saham"
    
    if is_idx:
        total_lots = safe_shares // 100
        actual_shares = total_lots * 100
    else:
        total_lots = safe_shares
        actual_shares = safe_shares
        
    # Total modal yang dipakai untuk membeli saham
    invested_capital = actual_shares * entry_price
    
    # Kerugian aktual jika terkena Stop Loss
    actual_loss_at_sl = actual_shares * risk_per_share
    actual_risk_pct = (actual_loss_at_sl / capital) * 100.0 if capital > 0 else 0.0
    
    # Potensi Keuntungan pada Target Profit 1 & 2
    profit_per_share_tp1 = target_price_1 - entry_price
    potential_gain_tp1 = actual_shares * profit_per_share_tp1
    rrr_1 = profit_per_share_tp1 / risk_per_share if risk_per_share > 0 else 0.0
    
    profit_per_share_tp2 = target_price_2 - entry_price
    potential_gain_tp2 = actual_shares * profit_per_share_tp2
    rrr_2 = profit_per_share_tp2 / risk_per_share if risk_per_share > 0 else 0.0
    
    # Analisis Keamanan & Peringatan
    warnings = []
    if total_lots == 0:
        min_modal = (100 * entry_price) if is_idx else entry_price
        min_risk_needed = (min_modal / capital) * 100.0 if capital > 0 else 0
        warnings.append(
            f"⚠️ Modal atau persentase risiko terlalu kecil untuk membeli 1 {unit_name}. "
            f"Dibutuhkan minimal modal sekitar Rp {min_modal:,.0f} atau naikkan risiko toleransi."
        )
    elif invested_capital > capital:
        warnings.append(
            "⚠️ Perhitungan lot ini membutuhkan modal lebih dari total saldo Anda (butuh leverage/margin). "
            "Sistem menyarankan membatasi pembelian maksimal seharga saldo tunai Anda."
        )
        # Cap to available capital
        max_affordable_shares = int(capital // entry_price)
        if is_idx:
            total_lots = max_affordable_shares // 100
            actual_shares = total_lots * 100
        else:
            total_lots = max_affordable_shares
            actual_shares = max_affordable_shares
        invested_capital = actual_shares * entry_price
        actual_loss_at_sl = actual_shares * risk_per_share
        actual_risk_pct = (actual_loss_at_sl / capital) * 100.0
        potential_gain_tp1 = actual_shares * profit_per_share_tp1
        potential_gain_tp2 = actual_shares * profit_per_share_tp2
        
    if rrr_1 < 1.5:
        warnings.append(
            "ℹ️ Risk-to-Reward Ratio TP1 di bawah 1:1.5. Untuk pertumbuhan akun yang sehat, "
            "disarankan hanya masuk transaksi jika potensi profit minimal 1.5x - 2x dari risiko rugi."
        )
        
    return {
        "status": "success",
        "capital": capital,
        "risk_percent": risk_percent,
        "entry_price": entry_price,
        "stop_loss_price": stop_loss_price,
        "target_price_1": target_price_1,
        "target_price_2": target_price_2,
        "total_lots": total_lots,
        "actual_shares": actual_shares,
        "unit_name": unit_name,
        "invested_capital": invested_capital,
        "actual_loss_at_sl": actual_loss_at_sl,
        "actual_risk_pct": round(actual_risk_pct, 2),
        "potential_gain_tp1": potential_gain_tp1,
        "potential_gain_tp2": potential_gain_tp2,
        "rrr_1": round(rrr_1, 2),
        "rrr_2": round(rrr_2, 2),
        "warnings": warnings
    }
