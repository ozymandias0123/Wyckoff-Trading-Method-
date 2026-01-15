# Wyckoff Trading Bot for MetaTrader 5

A complete implementation of the Wyckoff Trading Method as an automated trading bot for MetaTrader 5.

## Features

- **Five-Step Approach to the Market**
- **Accumulation/Distribution Phases (A-E)**
- **All Wyckoff Events Detection:**
  - PS (Preliminary Support)
  - SC (Selling Climax)
  - AR (Automatic Rally)
  - ST (Secondary Test)
  - Spring
  - SOS (Sign of Strength)
  - LPS (Last Point of Support)
  - BC (Buying Climax)
  - UTAD (Upthrust After Distribution)
  - SOW (Sign of Weakness)
  - LPSY (Last Point of Supply)
- **Supply & Demand Analysis**
- **Effort vs Result (Volume-Price Divergence)**
- **Nine Buying/Selling Tests**
- **Telegram Notifications**

## Requirements

```
MetaTrader5
pandas
numpy
requests
```

## Installation

1. Install Python 3.8+
2. Install MetaTrader 5 terminal
3. Install dependencies:

```bash
pip install MetaTrader5 pandas numpy requests
```

4. Create `wyckoff_config.json` with your settings:

```json
{
    "mt5_login": 12345678,
    "mt5_password": "your_password",
    "mt5_server": "Your-Server",
    
    "telegram_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID",
    
    "symbol": "EURUSD",
    "timeframe": "M15",
    "lot_size": 0.01,
    
    "risk_per_trade": 0.02,
    "max_lot_size": 1.0,
    
    "accumulation_threshold": 0.015,
    "volume_spike_threshold": 2.0,
    "spring_depth": 0.0005,
    
    "magic_number": 234567
}
```

## Usage

```bash
python Wyckoff.py
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `symbol` | Trading symbol | EURUSD |
| `timeframe` | Chart timeframe (M1, M5, M15, M30, H1, H4, D1, W1) | M15 |
| `lot_size` | Default lot size | 0.01 |
| `risk_per_trade` | Risk per trade (2% = 0.02) | 0.02 |
| `max_lot_size` | Maximum lot size | 1.0 |
| `volume_spike_threshold` | Volume spike multiplier | 2.0 |
| `spring_depth` | Spring detection depth | 0.0005 |
| `magic_number` | EA magic number | 234567 |

## Risk Warning

Trading involves substantial risk. This bot is for educational purposes. Always test on demo account first.

## License

MIT License
