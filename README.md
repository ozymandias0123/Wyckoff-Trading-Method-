# Wyckoff Trading Method - Automated Trading Bot

A complete implementation of the Wyckoff Trading Method as an automated trading bot for MetaTrader 5.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-MetaTrader%205-blue.svg)](https://www.metatrader5.com/)
[![Language](https://img.shields.io/badge/Language-MQL5-green.svg)](https://www.mql5.com/)

## Overview

This Expert Advisor (EA) implements the renowned Wyckoff Trading Method, a technical analysis approach developed by Richard Wyckoff in the early 1900s. The method focuses on understanding market structure through supply and demand dynamics, identifying accumulation and distribution phases, and trading the transitions between these phases.

### Key Features

- ✅ **Automated Phase Detection**: Identifies accumulation, markup, distribution, and markdown phases
- ✅ **Volume Spread Analysis**: Analyzes volume in relation to price movement
- ✅ **Pattern Recognition**: Detects Springs, Upthrusts, Signs of Strength, and Signs of Weakness
- ✅ **Risk Management**: Position sizing based on account risk percentage
- ✅ **ATR-Based Stops**: Dynamic stop loss and take profit based on market volatility
- ✅ **Trailing Stop**: Optional trailing stop to protect profits
- ✅ **Configurable Parameters**: Extensive customization options
- ✅ **Multi-Timeframe Support**: Works on any timeframe (M15, H1, H4, D1, etc.)
- ✅ **Multiple Symbols**: Can be applied to forex, stocks, commodities, indices

## Table of Contents

1. [The Wyckoff Method](#the-wyckoff-method)
2. [How It Works](#how-it-works)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Trading Signals](#trading-signals)
7. [Risk Management](#risk-management)
8. [Documentation](#documentation)
9. [Testing](#testing)
10. [Support](#support)
11. [License](#license)

## The Wyckoff Method

The Wyckoff Method is based on three fundamental laws:

1. **Law of Supply and Demand**: Prices rise when demand exceeds supply and fall when supply exceeds demand.
2. **Law of Cause and Effect**: The longer the accumulation or distribution (cause), the greater the subsequent move (effect).
3. **Law of Effort vs. Result**: Volume (effort) should confirm price movement (result). Divergence suggests change.

### Market Cycle Phases

```
Phase 1: ACCUMULATION → Smart money accumulates while retail sells
Phase 2: MARKUP → Price rises as trend is established  
Phase 3: DISTRIBUTION → Smart money distributes while retail buys
Phase 4: MARKDOWN → Price falls as trend reverses
```

## How It Works

### 1. Volume Analysis
- Calculates average volume over configurable period
- Identifies high volume (accumulation/distribution) and low volume (spring/upthrust)
- Confirms price action with volume

### 2. Range Detection
- Identifies consolidation zones (potential accumulation/distribution)
- Calculates support and resistance levels
- Determines if market is ranging or trending

### 3. Pattern Recognition

**Spring** (Buy Signal):
- Price breaks below support
- Closes back inside range on low volume
- Indicates end of accumulation

**Upthrust** (Sell Signal):
- Price breaks above resistance  
- Closes back inside range on low volume
- Indicates end of distribution

**Sign of Strength (SOS)** (Buy Signal):
- Strong bullish bar with high volume
- Breaks above range
- Confirms markup beginning

**Sign of Weakness (SOW)** (Sell Signal):
- Strong bearish bar with high volume
- Breaks below range
- Confirms markdown beginning

### 4. Trade Execution
- Enters positions at phase transitions
- Sets stop loss and take profit based on ATR
- Manages positions with optional trailing stop
- Closes positions at targets or stops

## Installation

### Quick Start

1. Download the repository files
2. Copy files to your MT5 data folder:
   ```
   MT5 Data Folder/
   ├── MQL5/
   │   ├── Experts/
   │   │   └── WyckoffTradingBot.mq5
   │   └── Include/
   │       └── Wyckoff/
   │           └── WyckoffAnalysis.mqh
   ```
3. Open MetaEditor (F4 in MT5)
4. Compile `WyckoffTradingBot.mq5`
5. Drag the EA onto a chart
6. Configure parameters
7. Enable Algo Trading (Ctrl+E)

📖 **Detailed Installation Guide**: See [INSTALLATION.md](INSTALLATION.md) for step-by-step instructions.

## Configuration

### Essential Parameters

#### Risk Management
```
RiskPercent = 1.0        // Risk 1% of account per trade
MaxLotSize = 10.0        // Maximum position size
MinLotSize = 0.01        // Minimum position size
MaxSpread = 30           // Don't trade if spread > 30 points
```

#### Wyckoff Analysis
```
AccumulationBars = 50     // Lookback period for phase detection
VolumePeriod = 20         // Period for volume average
VolumeThreshold = 1.5     // High volume = 1.5x average
TrendPeriod = 50          // Trend identification period
```

#### Exit Management
```
TakeProfitMultiplier = 2.0    // TP = 2x ATR
StopLossMultiplier = 1.0      // SL = 1x ATR  
ATRPeriod = 14                // ATR calculation period
UseTrailingStop = true        // Enable trailing stop
TrailingStopMultiplier = 1.5  // Trail at 1.5x ATR
```

### Recommended Settings

| Trading Style | Timeframe | RiskPercent | AccumulationBars | VolumeThreshold |
|---------------|-----------|-------------|------------------|-----------------|
| Conservative  | H4 / D1   | 0.5-1.0%    | 60-80           | 1.8-2.0         |
| Moderate      | H1 / H4   | 1.0-2.0%    | 50              | 1.5             |
| Aggressive    | M30 / H1  | 2.0-3.0%    | 30-40           | 1.2-1.3         |

## Usage

### Starting the Bot

1. **Choose Your Symbol**: Works best with major forex pairs (EURUSD, GBPUSD, USDJPY)
2. **Select Timeframe**: H1 or H4 recommended for beginners
3. **Attach EA**: Drag WyckoffTradingBot onto chart
4. **Configure Settings**: Adjust parameters based on your risk tolerance
5. **Enable Algo Trading**: Click the Algo Trading button (turns green)
6. **Monitor**: Check Experts tab for confirmation message

### What to Expect

- **Signal Frequency**: Varies by timeframe and market conditions
  - H1: 2-5 signals per week
  - H4: 1-2 signals per week  
  - D1: 1-2 signals per month

- **Win Rate**: Target 40-60% with proper 1:2 risk:reward ratio

- **Best Conditions**: 
  - Ranging markets transitioning to trends
  - Clear accumulation/distribution phases
  - Normal volatility

## Trading Signals

### Buy Signals Generated When:
- ✅ Spring detected (false breakdown)
- ✅ Sign of Strength at accumulation end
- ✅ Markup phase beginning confirmed

### Sell Signals Generated When:
- ✅ Upthrust detected (false breakout)
- ✅ Sign of Weakness at distribution end  
- ✅ Markdown phase beginning confirmed

### No Signal When:
- ❌ Market in middle of trend (no phase transition)
- ❌ Volume doesn't confirm pattern
- ❌ Spread too wide
- ❌ Unclear market structure

## Risk Management

### Built-in Safety Features

1. **Position Sizing**: Automatically calculates lot size based on risk %
2. **Stop Loss**: Every trade has a stop loss (1x ATR by default)
3. **Take Profit**: Every trade has a target (2x ATR by default)
4. **Spread Filter**: Avoids trading when spread is excessive
5. **Trailing Stop**: Protects profits as trade moves favorably

### Best Practices

⚠️ **Important Safety Guidelines**:

- Start with demo account (minimum 1 month)
- Never risk more than 2% per trade
- Keep total portfolio risk under 6-8%
- Monitor during first 2 weeks of live trading
- Disable during major news events
- Use VPS for 24/7 operation
- Maintain stable internet connection

## Documentation

📚 **Complete Documentation**:

- **[Installation Guide](INSTALLATION.md)**: Detailed setup instructions
- **[User Guide](USER_GUIDE.md)**: Comprehensive trading guide
  - Wyckoff Method explanation
  - Parameter configuration
  - Trading signals
  - Best practices
  - Troubleshooting

## Testing

### Backtesting

1. Open Strategy Tester (Ctrl+R)
2. Select `WyckoffTradingBot`
3. Choose symbol and timeframe
4. Set date range (minimum 1 year recommended)
5. Configure parameters
6. Run test
7. Analyze results

### Forward Testing

Before live trading:
1. Run on demo account for 1-2 months
2. Test across different market conditions
3. Verify signal quality
4. Confirm risk management works correctly
5. Monitor performance metrics

## Project Structure

```
Wyckoff-Trading-Method-/
├── MQL5/
│   ├── Experts/
│   │   └── WyckoffTradingBot.mq5          # Main Expert Advisor
│   └── Include/
│       └── Wyckoff/
│           └── WyckoffAnalysis.mqh        # Analysis engine
├── README.md                               # This file
├── INSTALLATION.md                         # Installation guide
└── USER_GUIDE.md                          # Comprehensive user guide
```

## Technical Requirements

- **Platform**: MetaTrader 5 (build 2600 or higher)
- **Account Type**: Any (Standard, ECN, etc.)
- **Minimum Balance**: $500 recommended for micro lots
- **Internet**: Stable connection required
- **OS**: Windows, Linux (via Wine), or Mac (via Wine/Virtual Machine)

## Support

### Getting Help

- 📖 Read the [User Guide](USER_GUIDE.md) for comprehensive information
- 📋 Check the [Installation Guide](INSTALLATION.md) for setup issues
- 💬 Review MT5 community forums for general EA questions
- 🔧 Contact your broker for platform-specific issues

### Common Issues

| Issue | Solution |
|-------|----------|
| Compilation errors | Verify files in correct folders |
| No trades | Check market conditions and parameters |
| "Not enough money" | Reduce RiskPercent or increase balance |
| Excessive losses | Test on demo, adjust parameters |

## Contributing

Contributions are welcome! If you'd like to improve the bot:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on demo account
5. Submit a pull request

## Disclaimer

⚠️ **Important Risk Disclosure**:

- Trading financial instruments carries substantial risk of loss
- Past performance is not indicative of future results  
- This EA is provided for educational purposes
- Only trade with money you can afford to lose
- Always test thoroughly on demo account before live trading
- The developers are not responsible for any losses incurred

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Richard Wyckoff for developing the original methodology
- The MetaTrader 5 community for MQL5 development resources
- Traders who have refined and shared Wyckoff techniques over the decades

## Version History

- **v1.00** (2026-01-15): Initial release
  - Core Wyckoff phase detection
  - Volume spread analysis
  - Pattern recognition (Spring, Upthrust, SOS, SOW)
  - Automated trade execution
  - Risk management and position sizing
  - Trailing stop functionality

---

**Made with ❤️ for traders who appreciate classical technical analysis**

*Happy Trading! May your accumulations be profitable and your distributions timely!* 📈
