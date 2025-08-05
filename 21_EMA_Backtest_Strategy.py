# 21 EMA Backtest Strategy

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

nifty100 = [
    "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS",
    "ASIANPAINT.NS", "AUROPHARMA.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "BAJAJHLDNG.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHEL.NS",
    "BIOCON.NS", "BPCL.NS", "BRITANNIA.NS", "BSOFT.NS", "CIPLA.NS", "COALINDIA.NS", "COLPAL.NS",
    "CONCOR.NS", "CROMPTON.NS", "DABUR.NS", "DIVISLAB.NS", "DLF.NS", "DRREDDY.NS", "EICHERMOT.NS",
    "ESCORTS.NS", "GAIL.NS", "GLAND.NS", "GODREJCP.NS", "GRASIM.NS", "HAVELLS.NS", "HCLTECH.NS",
    "HDFC.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDPETRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDEA.NS",
    "IDFCFIRSTB.NS", "IGL.NS", "INDHOTEL.NS", "INDIACEM.NS", "INDIAMART.NS", "INDIGO.NS", "INDUSINDBK.NS",
    "INFY.NS", "INTELLECT.NS", "IOC.NS", "IPCALAB.NS", "ITC.NS", "JINDALSTEL.NS", "JSWSTEEL.NS",
    "JUBLFOOD.NS", "KOTAKBANK.NS", "L&TFH.NS", "LALPATHLAB.NS", "LICI.NS", "LT.NS", "LTIM.NS", "LTTS.NS",
    "LUPIN.NS", "M&M.NS", "M&MFIN.NS", "MARICO.NS", "MARUTI.NS", "MCDOWELL-N.NS", "METROPOLIS.NS",
    "MOTHERSON.NS", "MPHASIS.NS", "MRF.NS", "MUTHOOTFIN.NS", "NAUKRI.NS", "NESTLEIND.NS", "NMDC.NS",
    "NTPC.NS", "OBEROIRLTY.NS", "ONGC.NS", "PAGEIND.NS", "PEL.NS", "PETRONET.NS", "PIDILITIND.NS",
    "PIIND.NS", "POLYCAB.NS", "POWERGRID.NS", "PVRINOX.NS", "RAMCOCEM.NS", "RECLTD.NS", "RELIANCE.NS",
    "SAIL.NS", "SBICARD.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS", "SIEMENS.NS", "SRF.NS",
    "SUNPHARMA.NS", "SUNTV.NS", "TATACHEM.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATAPOWER.NS",
    "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TRENT.NS", "TVSMOTOR.NS",
    "UBL.NS", "ULTRACEMCO.NS", "UPL.NS", "VEDL.NS", "VOLTAS.NS", "WIPRO.NS", "ZEEL.NS"
]
start_date = "2024-03-01"
end_date = "2025-07-31"
initial_capital = 1000000

results = []
# Brokerage paid
total_brokerage_paid = 0

def calculate_emas(df):
    df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA_100'] = df['Close'].ewm(span=100, adjust=False).mean()
    return df

def backtest_stock(symbol, capital):
    df = yf.download(symbol, start=start_date, end=end_date)
    df = calculate_emas(df)
    df.reset_index(inplace=True)

    trade_log = []
    total_brokerage = 0
    i = 100

    while i < len(df) - 1:
        row = df.iloc[i]
        if (
            row['Close'].item() > row['EMA_21'].item() and
            row['Close'].item() > row['EMA_50'].item() and
            row['Close'].item() > row['EMA_100'].item() and
            df.iloc[i - 1]['Close'].item() < df.iloc[i - 1]['EMA_21'].item()
        ):
            breakout_high = row['High'].item()
            buy_day = df.iloc[i + 1]
            if buy_day['High'].item() > breakout_high:
                entry_price = breakout_high
                target_price = entry_price * 1.01
                stop_price = entry_price * 0.995

                # Capture the entry date
                entry_date = df.iloc[i + 1]['Date'].item().date()

                for j in range(i + 1, len(df)):
                    high = df.iloc[j]['High'].item()
                    low = df.iloc[j]['Low'].item()
                    if high >= target_price:
                        exit_price = target_price
                        result = "Target Hit"
                        exit_date = df.iloc[j]['Date'].item().date()
                        break
                    elif low <= stop_price:
                        exit_price = stop_price
                        result = "Stoploss Hit"
                        exit_date = df.iloc[j]['Date'].item().date()
                        break
                else:
                    exit_price = df.iloc[-1]['Close'].item()
                    result = "Open"
                    exit_date = df.iloc[-1]['Date'].item().date()

                shares_to_buy = capital // entry_price
                if shares_to_buy == 0 and capital >= entry_price:
                    shares_to_buy = 1

                brokerage = entry_price * shares_to_buy * 0.0000275
                total_brokerage += brokerage
                profit = (exit_price - entry_price) * shares_to_buy - brokerage
                capital += profit

                trade_log.append({
                    'Stock': symbol,
                    'Entry Date': entry_date,  # Add the entry date
                    'Exit Date': exit_date,
                    'Entry Price': entry_price,
                    'Exit Price': exit_price,
                    'Result': result,
                    'Profit': profit,
                    'Capital After Trade': capital
                })
                i = j
        i += 1

    return trade_log, capital, total_brokerage

# Run the backtest
capital = initial_capital
for stock in nifty100:
    trades, capital, stock_brokerage = backtest_stock(stock, capital)
    results.extend(trades)
    total_brokerage_paid += stock_brokerage

# Save to Excel
df_results = pd.DataFrame(results)
df_results.to_excel("Nifty100_EMA_Breakout_Backtest.xlsx", index=False)

# Summary
total_trades = len(df_results)
successful_trades = df_results[df_results['Result'] == 'Target Hit'].shape[0]
nonsuccessful_trades = df_results[df_results['Result'] == 'Stoploss Hit'].shape[0]
open_trades = df_results[df_results['Result'] == 'Open'].shape[0]
success_percentage = (successful_trades / total_trades) * 100 if total_trades > 0 else 0

net_profit = capital - initial_capital
current_capital = capital

print("\n----- BACKTEST SUMMARY -----")
print("Amount Invested       : ₹1,000,000")
print(f"Total Trades          : {total_trades}")
print(f"Successful Trades     : {successful_trades}")
print(f"Non-successful Trades : {nonsuccessful_trades}")
print(f"Open Trades           : {open_trades}")
print(f"Success Percentage    : {success_percentage:.2f}%")
print(f"Net Profit            : ₹{net_profit:,.2f}")
print(f"Total Capital         : ₹{current_capital:,.2f}")
print(f"Total Brokerage Paid  : ₹{total_brokerage_paid:,.2f}")