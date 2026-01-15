# Installation Guide

## Prerequisites

- MetaTrader 5 platform installed
- Basic understanding of trading and risk management
- Active trading account (demo or live)

## Installation Steps

### 1. Locate Your MT5 Data Folder

1. Open MetaTrader 5
2. Click **File** → **Open Data Folder**
3. This will open your MT5 data directory

### 2. Copy the Expert Advisor Files

Copy the files to your MT5 data folder structure:

```
<MT5 Data Folder>/
├── MQL5/
│   ├── Experts/
│   │   └── WyckoffTradingBot.mq5
│   └── Include/
│       └── Wyckoff/
│           └── WyckoffAnalysis.mqh
```

**Step-by-step:**

1. Navigate to the `MQL5/Experts/` folder in your MT5 data directory
2. Copy `WyckoffTradingBot.mq5` into the `Experts` folder
3. Navigate to `MQL5/Include/` and create a folder named `Wyckoff` if it doesn't exist
4. Copy `WyckoffAnalysis.mqh` into the `Include/Wyckoff/` folder

### 3. Compile the Expert Advisor

1. In MetaTrader 5, open the **MetaEditor** (press F4 or click the IDE icon)
2. In MetaEditor, navigate to **File** → **Open** 
3. Find and open `WyckoffTradingBot.mq5` from the Experts folder
4. Click **Compile** (F7) or the compile button in the toolbar
5. Check the **Errors** tab at the bottom - it should say "0 error(s), 0 warning(s)"
6. If successful, you'll see the message: "WyckoffTradingBot.mq5 successfully compiled"

### 4. Attach the EA to a Chart

1. In MT5, open a chart for your desired trading instrument (e.g., EURUSD)
2. Choose your preferred timeframe (H1 or H4 recommended for beginners)
3. In the **Navigator** panel (Ctrl+N), expand **Expert Advisors**
4. Find `WyckoffTradingBot` in the list
5. Drag and drop it onto your chart

### 5. Configure the Settings

A settings dialog will appear. Configure the following parameters:

#### General Settings
- **Magic Number**: Unique identifier for this EA's trades (default: 123456)
- **Trade Comment**: Comment to appear on trades (default: "Wyckoff Bot")

#### Risk Management
- **Risk Percent**: Risk per trade as % of account balance (recommended: 1.0-2.0%)
- **Max Lot Size**: Maximum position size (default: 10.0)
- **Min Lot Size**: Minimum position size (default: 0.01)
- **Max Spread**: Maximum spread in points to allow trading (default: 30)

#### Wyckoff Parameters
- **Accumulation Bars**: Lookback period for phase detection (default: 50)
- **Volume Period**: Period for volume moving average (default: 20)
- **Volume Threshold**: Multiplier for high volume detection (default: 1.5)
- **Trend Period**: Period for trend identification (default: 50)
- **Trade Accumulation**: Enable trading accumulation phases (default: true)
- **Trade Distribution**: Enable trading distribution phases (default: true)

#### Exit Settings
- **Take Profit Multiplier**: TP distance in ATR multiples (default: 2.0)
- **Stop Loss Multiplier**: SL distance in ATR multiples (default: 1.0)
- **ATR Period**: Period for ATR calculation (default: 14)
- **Use Trailing Stop**: Enable trailing stop (default: true)
- **Trailing Stop Multiplier**: Trailing distance in ATR multiples (default: 1.5)

### 6. Enable Automated Trading

1. Click the **Algo Trading** button in the MT5 toolbar (or press Ctrl+E)
2. Verify that the button turns green, indicating automated trading is enabled
3. You should see a smiling face emoji (😊) in the top-right corner of the chart

### 7. Verify Installation

Check the **Experts** tab in the Terminal window (Ctrl+T) for the message:
```
Wyckoff Trading Bot initialized successfully
Symbol: EURUSD Period: H1
```

## Troubleshooting

### Compilation Errors

**Error: "Cannot open include file"**
- Verify that `WyckoffAnalysis.mqh` is in the correct location: `MQL5/Include/Wyckoff/`
- Check the path in the include statement in `WyckoffTradingBot.mq5`

**Error: "Trade.mqh not found"**
- This is a standard MT5 library. Reinstall MetaTrader 5 if this error occurs

### Runtime Issues

**EA not trading:**
- Verify automated trading is enabled (green Algo Trading button)
- Check the spread is within the MaxSpread parameter
- Ensure there are no position limits on your account
- Review the Experts log for error messages

**"Trade context busy" errors:**
- This is normal during high-volatility periods
- The EA will retry automatically
- Reduce the number of EAs running simultaneously if this persists

**"Not enough money" errors:**
- Reduce the Risk Percent parameter
- Ensure your account has sufficient free margin
- Check the Min Lot Size setting

### Testing on Demo Account

**Strongly recommended before live trading:**

1. Open a demo account if you don't have one (File → Open Account)
2. Install and configure the EA on the demo account first
3. Let it run for at least 2-4 weeks to understand its behavior
4. Monitor the trading logic and results in the Strategy Tester

## Strategy Tester

To backtest the EA:

1. Open Strategy Tester (Ctrl+R or View → Strategy Tester)
2. Select `WyckoffTradingBot` from the Expert Advisor dropdown
3. Choose your symbol and timeframe
4. Set the date range for testing
5. Configure the input parameters
6. Click **Start** to run the backtest
7. Review results in the **Results**, **Graph**, and **Report** tabs

## Support

For issues or questions:
- Review the MT5 documentation
- Check the MT5 community forums
- Consult with your broker's support team

## Important Notes

⚠️ **Risk Warning**: Trading foreign exchange and CFDs carries a high level of risk. Only trade with money you can afford to lose. Past performance is not indicative of future results.

✅ **Best Practices**:
- Always test on a demo account first
- Start with small position sizes
- Monitor the EA regularly, especially in the first few weeks
- Keep your MetaTrader 5 platform and the EA updated
- Ensure stable internet connection when running automated trading
