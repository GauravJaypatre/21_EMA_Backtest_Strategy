# 21_EMA_Backtest_Strategy

📌 Project Overview
This script analyzes historical stock data between March 1, 2024 and July 31, 2025, looking for breakout opportunities based on EMA21 crossover, and validates alignment with EMA50 and EMA100 before simulating a trade.

⚙️ Features
✅ Scans all Nifty 100 stocks (with .NS Yahoo Finance symbols)
📊 Calculates EMA 21, EMA 50, and EMA 100
📈 Detects breakout candle when price crosses above EMA 21
🎯 Enters trade if next day’s high breaks previous high (breakout confirmation)
📉 Applies 1% Target and 0.5% Stop Loss
💸 Deducts 0.00275% brokerage on buy and sell
📥 Outputs trade results in an Excel file
📊 Provides backtest summary:
    Total Trades
    Successful & Non-Successful Trades
    Success Rate
    Net Profit
    Capital After All Trades
    Total Brokerage Paid

🧠 Strategy Logic
Breakout Candle: Close price crosses above EMA21, after being below EMA21 on the previous day.
Buy Trigger: Next day’s high must break the breakout candle’s high.
Trade Simulation:
    Entry at breakout high
    Exit at:
        Target = Entry × 1.01 (1%)
        Stop Loss = Entry × 0.995 (0.5%)
        Or final close if neither triggered
Capital Management:
    Initial capital: ₹10,00,000
    Shares bought = Capital ÷ Entry price
    Capital is updated after each trade (profit/loss adjusted)
Brokerage Deduction: Applied once per trade (entry + exit combined)

📎 Notes
Data is fetched using Yahoo Finance (via yFinance)
Strategy works on daily timeframe
Supports customization of target, stop-loss, and brokerage in code

📫 Connect
If you find this useful or would like to collaborate on future trading strategy projects, feel free to connect on LinkedIn or open an issue on the repo.

NOTE:- THIS IS JUST A BACKTEST STRATEGY WHICH IS BASIC AND CAN BE USED FOR BACKTESTING ONLY. ITS NOT RECOMMENDED FOR LIVE TRADING.
