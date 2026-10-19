"""
backtester.py
Modul Backtesting untuk menguji performa strategi pada data historis masa lalu.
Memberikan bukti objektif (Win Rate, Total Return, Max Drawdown) sebelum menaruh uang sungguhan.
"""

import pandas as pd
import numpy as np


def run_backtest(
    df: pd.DataFrame,
    initial_capital: float = 10000000.0,
    risk_per_trade: float = 0.01,
    is_idx: bool = True
) -> dict:
    """
    Simulasi backtest posisi Long berdasarkan kolom 'Signal', 'Suggested_SL', 'Suggested_TP1'.
    
    Signal = 1 (BUY)
    Signal = -1 (EXIT/SELL)
    """
    data = df.copy()
    
    cash = initial_capital
    position_shares = 0
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0
    entry_date = None
    
    trades = []
    equity_curve = []
    
    dates = data.index
    
    for i in range(len(data)):
        current_date = dates[i]
        row = data.iloc[i]
        current_price = row['Close']
        high_price = row['High']
        low_price = row['Low']
        signal = row.get('Signal', 0)
        
        # 1. Jika sedang memegang posisi, periksa Stop Loss / Take Profit / Sinyal Exit
        if position_shares > 0:
            exit_price = None
            exit_reason = None
            
            # Cek apakah terkena Stop Loss di candle ini
            if low_price <= stop_loss:
                exit_price = stop_loss
                exit_reason = "Kena Stop Loss (Cut Loss)"
            # Cek apakah terkena Take Profit di candle ini
            elif high_price >= take_profit:
                exit_price = take_profit
                exit_reason = "Target Profit Tercapai (TP1)"
            # Cek apakah ada sinyal Sell dari indikator
            elif signal == -1:
                exit_price = current_price
                exit_reason = "Sinyal Indikator Melemah"
                
            if exit_price is not None:
                proceeds = position_shares * exit_price
                pnl = proceeds - (position_shares * entry_price)
                return_pct = ((exit_price - entry_price) / entry_price) * 100.0
                cash += proceeds
                
                trades.append({
                    "Entry_Date": entry_date,
                    "Exit_Date": current_date,
                    "Entry_Price": entry_price,
                    "Exit_Price": exit_price,
                    "Shares": position_shares,
                    "PnL": pnl,
                    "Return_Pct": return_pct,
                    "Reason": exit_reason
                })
                
                position_shares = 0
                entry_price = 0.0
                stop_loss = 0.0
                take_profit = 0.0
                entry_date = None
                
        # 2. Jika belum memegang posisi dan ada sinyal BUY
        elif signal == 1:
            sl_candidate = row.get('Suggested_SL', current_price * 0.95)
            tp_candidate = row.get('Suggested_TP1', current_price * 1.10)
            
            if sl_candidate < current_price:
                # Hitung ukuran posisi aman
                max_risk_amount = cash * risk_per_trade
                risk_per_share = current_price - sl_candidate
                safe_shares = int(max_risk_amount / risk_per_share)
                
                # Batasi dengan cash yang tersedia
                max_affordable = int(cash // current_price)
                shares_to_buy = min(safe_shares, max_affordable)
                
                if is_idx:
                    shares_to_buy = (shares_to_buy // 100) * 100
                    
                if shares_to_buy > 0:
                    cost = shares_to_buy * current_price
                    cash -= cost
                    position_shares = shares_to_buy
                    entry_price = current_price
                    stop_loss = sl_candidate
                    take_profit = tp_candidate
                    entry_date = current_date
                    
        # Catat total ekuitas saat ini (Cash + Nilai Saham)
        current_equity = cash + (position_shares * current_price)
        equity_curve.append({
            "Datetime": current_date,
            "Equity": current_equity
        })
        
    equity_df = pd.DataFrame(equity_curve).set_index("Datetime")
    
    # Metrik Evaluasi
    trades_df = pd.DataFrame(trades)
    final_equity = equity_df['Equity'].iloc[-1] if not equity_df.empty else initial_capital
    total_return_pct = ((final_equity - initial_capital) / initial_capital) * 100.0
    
    # Hitung Maximum Drawdown
    equity_series = equity_df['Equity']
    peak = equity_series.cummax()
    drawdown = (equity_series - peak) / peak * 100.0
    max_drawdown = drawdown.min()
    
    if not trades_df.empty:
        winning_trades = trades_df[trades_df['PnL'] > 0]
        losing_trades = trades_df[trades_df['PnL'] < 0]
        win_rate = (len(winning_trades) / len(trades_df)) * 100.0
        
        gross_profit = winning_trades['PnL'].sum()
        gross_loss = abs(losing_trades['PnL'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)
    else:
        win_rate = 0.0
        profit_factor = 0.0
        winning_trades = pd.DataFrame()
        losing_trades = pd.DataFrame()
        
    return {
        "initial_capital": initial_capital,
        "final_equity": final_equity,
        "total_return_pct": round(total_return_pct, 2),
        "win_rate": round(win_rate, 1),
        "total_trades": len(trades_df),
        "winning_trades": len(winning_trades),
        "losing_trades": len(losing_trades),
        "max_drawdown_pct": round(max_drawdown, 2),
        "profit_factor": round(profit_factor, 2),
        "equity_df": equity_df,
        "trades_df": trades_df
    }
