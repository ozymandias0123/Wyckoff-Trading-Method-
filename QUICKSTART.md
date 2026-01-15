# Quick Start Guide

Get up and running with the Wyckoff Trading Bot in 10 minutes!

## Prerequisites Checklist

- [ ] MetaTrader 5 installed
- [ ] Demo or live trading account active
- [ ] Basic understanding of trading concepts

## 5-Minute Installation

### Step 1: Download Files (1 min)
Clone or download this repository to your computer.

### Step 2: Copy Files (2 min)

1. Open MetaTrader 5
2. Press **Ctrl+Shift+D** or go to **File → Open Data Folder**
3. Copy files:

```
From Downloaded Folder          →    To MT5 Data Folder
─────────────────────────────────────────────────────────
MQL5/Experts/WyckoffTradingBot.mq5   →   MQL5/Experts/
MQL5/Include/Wyckoff/*                →   MQL5/Include/Wyckoff/
```

### Step 3: Compile (1 min)

1. In MT5, press **F4** to open MetaEditor
2. Navigate to **File → Open**
3. Open `WyckoffTradingBot.mq5`
4. Press **F7** or click **Compile**
5. Verify: "0 error(s), 0 warning(s)" at the bottom

### Step 4: Attach to Chart (1 min)

1. Open a chart (e.g., EURUSD on H1 timeframe)
2. Press **Ctrl+N** to open Navigator
3. Expand **Expert Advisors**
4. Drag **WyckoffTradingBot** onto your chart
5. Click **OK** on the settings dialog (use defaults for now)

### Step 5: Enable Trading (30 sec)

1. Click the **Algo Trading** button in toolbar (or press **Ctrl+E**)
2. Button should turn **GREEN**
3. Look for "😊" emoji in top-right corner of chart

## Verify Installation

Check the **Experts** tab at the bottom of MT5:

```
✅ You should see: "Wyckoff Trading Bot initialized successfully"
✅ Symbol and Period should be displayed: "Symbol: EURUSD Period: H1"
```

## Your First Day

### Recommended Initial Settings

For your first test, use these **CONSERVATIVE** settings on a **DEMO** account:

```
Risk Percent: 0.5%          (low risk)
Max Lot Size: 0.1           (small positions)
Accumulation Bars: 60       (requires clear patterns)
Volume Threshold: 1.8       (strict volume requirements)
Trade Accumulation: true    (trade buy signals)
Trade Distribution: false   (ignore sell signals for now)
```

### What to Watch

During your first day:

1. **Monitor the Experts Log**: Check for messages about:
   - Phase detection
   - Volume analysis
   - Trade signals

2. **Be Patient**: The bot waits for quality setups
   - May take hours or days for first signal
   - This is normal and expected

3. **Watch for These Messages**:
   ```
   ✅ "Buy position opened..." = Trade executed
   ⚠️ "Spread too high..." = Spread too wide (normal)
   ℹ️ "Current phase: ACCUMULATION" = Market analysis
   ```

## First Week Checklist

- [ ] **Day 1-2**: Bot running, watching for signals
- [ ] **Day 3-4**: Review any trades taken, check profit/loss
- [ ] **Day 5-6**: Adjust parameters if needed (small changes only)
- [ ] **Day 7**: Review weekly performance, decide on next steps

## Common First-Day Questions

### "Why hasn't it traded yet?"

**Normal!** The Wyckoff method waits for specific patterns:
- Accumulation/distribution phases
- Spring or Upthrust signals
- Volume confirmation

It may take days to find the perfect setup.

### "I see a trade but the SL/TP seem far away"

**By design!** The bot uses ATR (market volatility):
- Stop Loss = 1x ATR (adjustable)
- Take Profit = 2x ATR (adjustable)
- This adapts to each symbol's volatility

### "Can I run it on multiple charts?"

**Yes!** You can:
- Use different symbols (EURUSD, GBPUSD, etc.)
- Use different timeframes
- Each instance is independent

But start with just ONE chart for the first week.

### "Should I use live money immediately?"

**NO!** Always follow this progression:
1. ✅ Demo account: 2-4 weeks minimum
2. ✅ Micro live account: 1-2 months
3. ✅ Full live account: Only when consistently profitable

## Next Steps

After your first successful week:

1. **Read the Full Documentation**:
   - [USER_GUIDE.md](USER_GUIDE.md) - Comprehensive guide
   - [INSTALLATION.md](INSTALLATION.md) - Detailed installation

2. **Learn the Wyckoff Method**:
   - Read about Richard Wyckoff's principles
   - Understand accumulation and distribution
   - Watch video tutorials on Wyckoff trading

3. **Optimize Your Settings**:
   - Backtest different parameter combinations
   - Use Strategy Tester (Ctrl+R)
   - Test for at least 1 year of historical data

4. **Join the Community**:
   - MT5 forums
   - Trading Discord servers
   - Wyckoff trading groups

## Emergency Stops

### How to Stop the Bot Immediately

**Method 1**: Click the **Algo Trading** button (turns red/gray)

**Method 2**: Right-click chart → **Expert Advisors** → **Remove**

**Method 3**: Close MetaTrader 5

### When to Stop the Bot

Stop immediately if:
- ❌ Unexplained rapid losses
- ❌ Strange trade behavior
- ❌ Error messages you don't understand
- ❌ Major news events (NFP, FOMC, etc.)
- ❌ Broker platform issues

You can always restart after investigating!

## Getting Help

**Before asking for help**, check:

1. ✅ Error messages in Experts tab
2. ✅ [USER_GUIDE.md](USER_GUIDE.md) troubleshooting section
3. ✅ [INSTALLATION.md](INSTALLATION.md) for setup issues

**Still stuck?**
- Check MT5 community forums
- Consult your broker's support team
- Review MQL5 documentation

## Pro Tips

💡 **Tip 1**: Keep a trading journal
- Note when trades open/close
- Record market conditions
- Track what works and what doesn't

💡 **Tip 2**: Don't over-optimize
- Resist urge to constantly change settings
- Give each configuration at least 2 weeks
- Small adjustments are better than big changes

💡 **Tip 3**: Understand before automating
- Manually identify accumulation phases on charts
- Practice spotting Springs and Upthrusts
- This helps you trust the bot's decisions

💡 **Tip 4**: Combine with discipline
- Don't override the bot's decisions
- Let it follow the system
- Review results weekly, not hourly

## Success Metrics

After 1 month, evaluate:

| Metric | Target |
|--------|--------|
| Win Rate | 40-60% |
| Profit Factor | > 1.5 |
| Max Drawdown | < 20% |
| Average RR | 1:2 or better |
| Total Trades | 10+ |

If meeting these targets → Continue with confidence!
If not → Review settings and market conditions

## Final Reminders

⚠️ **Critical Safety Rules**:

1. **ALWAYS test on demo first** (no exceptions!)
2. **NEVER risk more than you can afford to lose**
3. **ALWAYS use stop losses** (bot does this automatically)
4. **NEVER let emotions override the system**
5. **ALWAYS maintain proper risk management**

---

## You're Ready!

You now have everything you need to start. Remember:

✅ Start small
✅ Be patient  
✅ Learn continuously
✅ Manage risk properly

**Happy Trading!** 📈

---

*For detailed information, see [USER_GUIDE.md](USER_GUIDE.md)*
