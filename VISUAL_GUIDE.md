# Wyckoff Method Visual Guide

## The Four Market Phases

```
                  DISTRIBUTION PHASE
                   (Smart Money Sells)
                        ___________
                       /           \
                      /   Phase 3   \
         MARKUP      /               \      MARKDOWN
         PHASE      /                 \      PHASE
        (Uptrend)  |    Phase 4        |   (Downtrend)
           |       |  (Markdown)       |       |
        Phase 2    |                   |    Phase 4
           |        \                  /       |
           |         \                /        |
           |          \______________/         |
           |                                   |
           |        ACCUMULATION PHASE         |
           |       (Smart Money Buys)          |
           |                                   |
          Buy                                 Sell
         Entry                               Entry
         
Phase 1: ACCUMULATION - Smart money accumulates positions
Phase 2: MARKUP - Price rises, retail follows the trend
Phase 3: DISTRIBUTION - Smart money distributes to retail
Phase 4: MARKDOWN - Price falls, retail holds losing positions
```

## Wyckoff Events and Trading Signals

### Accumulation Phase → Markup (BUY SIGNALS)

```
1. Spring Pattern (False Breakdown):
   
   Range High ────────────────────────────
                                          
   Price Range ███████████████████████████  ← Consolidation
                                          
   Range Low  ────────────────────────────
                       ↓ Price breaks below
                       │ (on low volume)
                       ↓
                    ───┴───  ← Spring
                       ↑ Price bounces back
                       │ 
                       → BUY SIGNAL


2. Sign of Strength (SOS):
   
              ████ ← Large bullish bar
             ████   with high volume
            ████
           ████
   ──────████────── ← Breaks above range
        ████
       ████
                    → BUY SIGNAL
```

### Distribution Phase → Markdown (SELL SIGNALS)

```
1. Upthrust Pattern (False Breakout):
   
                    ───┬───  ← Upthrust
                       ↓ Price breaks above
                       │ (on low volume)
                       ↓ 
   Range High ────────────────────────────
                       ↑ Price reverses down
   Price Range ███████████████████████████  ← Consolidation
                                          
   Range Low  ────────────────────────────
                    → SELL SIGNAL


2. Sign of Weakness (SOW):
   
       ████
        ████
   ──────████────── ← Breaks below range
          ████
           ████
            ████   Large bearish bar
             ████ ← with high volume
                    
                    → SELL SIGNAL
```

## Volume Analysis

```
High Volume Events:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
█████████████████ > 1.5x Average
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Indicates:
✓ Smart money activity
✓ Potential phase transition
✓ Confirms price movements

Low Volume Events:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
███████ < 0.67x Average
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Indicates:
✓ Lack of interest
✓ Potential false breakout/breakdown
✓ Spring or Upthrust setup
```

## Trade Management Flow

```
┌─────────────────────────────────────────┐
│   Bot Analyzes Every New Bar            │
├─────────────────────────────────────────┤
│                                         │
│  1. Calculate Average Volume            │
│  2. Identify Trading Range              │
│  3. Determine Current Phase             │
│  4. Detect Wyckoff Patterns             │
│                                         │
└────────────┬───────────────┬────────────┘
             │               │
        No Signal       Signal Found
             │               │
             ▼               ▼
      ┌──────────┐    ┌──────────────┐
      │   Wait   │    │ Check Spread │
      └──────────┘    └──────┬───────┘
                             │
                        Spread OK?
                             │
                    Yes ─────┴───── No
                     │              │
                     ▼              ▼
            ┌─────────────┐   ┌─────────┐
            │ Calculate   │   │  Skip   │
            │ Position    │   │  Trade  │
            │ Size        │   └─────────┘
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │ Open Trade  │
            │ Set SL & TP │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │   Monitor   │
            │  Position   │
            ├─────────────┤
            │ - Update    │
            │   Trailing  │
            │   Stop      │
            │ - Check TP  │
            │ - Check SL  │
            └─────────────┘
```

## Risk Management Calculation

```
Account Balance: $1,000
Risk Per Trade:  1% = $10

Entry Price:     1.1000
Stop Loss:       1.0950 (50 pips)
Take Profit:     1.1100 (100 pips)

Risk:Reward = 1:2 ✓

Position Size Calculation:
───────────────────────────
Risk Amount = $10
Stop Distance = 50 pips
Position Size = Risk / Stop Distance
              = $10 / (50 × $10 per pip)
              = 0.02 lots

With 0.02 lots:
- Risk: $10 (1% of account)
- Target: $20 (2% of account)
```

## Parameter Impact Visualization

```
Accumulation Bars Parameter:
═══════════════════════════════════════════════

Short Period (30 bars):
├──┼──┼──┼──┤
More sensitive, more signals, potentially more false signals


Medium Period (50 bars) - DEFAULT:
├──┼──┼──┼──┼──┼──┤
Balanced sensitivity and reliability


Long Period (80 bars):
├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
Less sensitive, fewer signals, higher quality


Volume Threshold Parameter:
═══════════════════════════════════════════════

Low Threshold (1.2x):
Volume ▓▓▓▓▓▓▓▓▓▓▓▓ → High Volume
More events detected, more trades


Medium Threshold (1.5x) - DEFAULT:
Volume ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ → High Volume
Balanced detection


High Threshold (2.0x):
Volume ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ → High Volume
Fewer events, stricter requirements
```

## Timeframe Comparison

```
Lower Timeframes (M15, M30):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Signals: ▓ ▓  ▓▓  ▓ ▓ ▓▓▓  ▓  ▓▓ ▓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
+ More frequent signals
+ Faster reaction to changes
- More noise and false signals
- Requires closer monitoring


Medium Timeframes (H1, H4) - RECOMMENDED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Signals:    ▓    ▓     ▓  ▓      ▓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
+ Good balance of frequency and quality
+ Clearer patterns
+ Reasonable monitoring needs


Higher Timeframes (D1, W1):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Signals:          ▓        ▓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
+ Very clear patterns
+ Higher quality signals
- Infrequent signals
- Requires patience
```

## Bot Decision Tree

```
                    New Bar
                       ↓
           ┌───────────────────────┐
           │  Is spread too high?  │
           └─────┬─────────┬───────┘
                 │         │
                Yes       No
                 │         │
                Wait      ↓
               ┌──────────────────────┐
               │  Existing position?  │
               └──────┬──────┬────────┘
                      │      │
                     Yes    No
                      │      │
                      │      ↓
                      │  ┌────────────────────┐
                      │  │ Analyze Volume &   │
                      │  │ Trading Range      │
                      │  └─────────┬──────────┘
                      │            │
                      │      ┌─────┴─────┐
                      │      │  Pattern  │
                      │      │  Detected?│
                      │      └─────┬─────┘
                      │            │
                      │    Yes ────┴──── No
                      │     │            │
                      │     ↓           Wait
                      │  ┌──────────┐
                      │  │  Entry   │
                      │  │ Criteria │
                      │  │   Met?   │
                      │  └────┬─────┘
                      │       │
                      │   Yes─┴─No
                      │    │    │
                      │    ↓   Wait
                      │ ┌────────┐
                      │ │ Open   │
                      │ │ Trade  │
                      │ └────────┘
                      ↓
               ┌──────────────┐
               │ Trail Stop?  │
               └──┬────────┬──┘
                  │        │
                 Yes      No
                  │        │
                  ↓       Wait
            ┌────────────┐
            │ Update SL  │
            └────────────┘
```

## Example Trade Visualization

```
EURUSD H1 Chart Example:

Price
1.1100 ─────────────────────────────────
                                    TP Hit! (+50 pips)
1.1075 ───────────────────────────↗─────
                               ↗
1.1050 ────────────────────↗─────────────
                        ↗
1.1025 ──────────────↗───────────────────
                  ↗ │
1.1000 ────────Entry │─────────────────── Entry: 1.1000
              ▲   │  │                    SL:    1.0950
              │   │  │                    TP:    1.1100
1.0975 ───────┼───┼──┼──────────────────
              │   │  │
1.0950 ───────●───●──●─────────────────── Stop Loss Level
           Spring Pattern
              
Volume:
████████ ← Low Volume (Spring signal)
▓▓▓▓▓▓▓▓▓▓▓ ← Average Volume
████████████████ ← High Volume (SOS confirmation)

Result: +50 pips profit (1:2 RR achieved)
```

## Configuration Profiles Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                   CONSERVATIVE PROFILE                       │
├─────────────────────────────────────────────────────────────┤
│ Risk: 0.5%  │ AccBars: 70  │ VolThresh: 1.8               │
│                                                             │
│ Signals: ▓      ▓         ▓                                │
│ (Fewer, higher quality)                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     MODERATE PROFILE                         │
├─────────────────────────────────────────────────────────────┤
│ Risk: 1.0%  │ AccBars: 50  │ VolThresh: 1.5               │
│                                                             │
│ Signals: ▓   ▓    ▓     ▓    ▓                             │
│ (Balanced frequency and quality)                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    AGGRESSIVE PROFILE                        │
├─────────────────────────────────────────────────────────────┤
│ Risk: 2.0%  │ AccBars: 35  │ VolThresh: 1.3               │
│                                                             │
│ Signals: ▓▓ ▓ ▓▓  ▓ ▓▓ ▓  ▓ ▓                              │
│ (More frequent, requires monitoring)                        │
└─────────────────────────────────────────────────────────────┘
```

## Key Concepts Summary

```
┌──────────────────────────────────────────────────────────┐
│                  WYCKOFF PRINCIPLES                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. Supply & Demand Control Price                       │
│     Price ↑ when Demand > Supply                        │
│     Price ↓ when Supply > Demand                        │
│                                                          │
│  2. Cause & Effect Relationship                         │
│     Accumulation Duration → Markup Extent               │
│     Distribution Duration → Markdown Extent             │
│                                                          │
│  3. Effort vs Result Analysis                           │
│     Volume (Effort) should confirm Price (Result)       │
│     Divergence suggests reversal                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Quick Reference Chart

```
┌─────────────┬────────────────┬──────────────┬─────────────┐
│   Phase     │   Character    │    Volume    │   Action    │
├─────────────┼────────────────┼──────────────┼─────────────┤
│Accumulation │ Sideways range │ High on dips │ Smart $ BUY │
│             │ Support holds  │ Low on fails │             │
├─────────────┼────────────────┼──────────────┼─────────────┤
│   Markup    │ Higher highs   │ High on rises│ Trend UP    │
│             │ Higher lows    │              │ Hold LONG   │
├─────────────┼────────────────┼──────────────┼─────────────┤
│Distribution │ Sideways range │ High on rally│ Smart $ SELL│
│             │ Resistance fail│ Low on fails │             │
├─────────────┼────────────────┼──────────────┼─────────────┤
│  Markdown   │ Lower lows     │ High on falls│ Trend DOWN  │
│             │ Lower highs    │              │ Hold SHORT  │
└─────────────┴────────────────┴──────────────┴─────────────┘
```

---

**Note**: These are simplified visualizations. Actual market conditions are more complex and nuanced. Always refer to the comprehensive documentation and test thoroughly on a demo account.
