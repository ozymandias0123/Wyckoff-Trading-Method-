//+------------------------------------------------------------------+
//|                                          WyckoffTradingBot.mq5   |
//|                        Copyright 2026, Wyckoff Trading Method    |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2026, Wyckoff Trading Method"
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "Automated trading bot implementing the Wyckoff Trading Method"
#property description "Analyzes accumulation/distribution phases, volume spread, and price action"

#include <Trade\Trade.mqh>
#include "..\\Include\\Wyckoff\\WyckoffAnalysis.mqh"

//--- Input parameters
input group "General Settings"
input int      MagicNumber = 123456;           // Magic number for trades
input string   TradeComment = "Wyckoff Bot";   // Trade comment

input group "Risk Management"
input double   RiskPercent = 1.0;              // Risk per trade (%)
input double   MaxLotSize = 10.0;              // Maximum lot size
input double   MinLotSize = 0.01;              // Minimum lot size
input int      MaxSpread = 30;                 // Maximum spread in points

input group "Wyckoff Parameters"
input int      AccumulationBars = 50;          // Bars for accumulation detection
input int      VolumePeriod = 20;              // Volume moving average period
input double   VolumeThreshold = 1.5;          // Volume threshold multiplier
input int      TrendPeriod = 50;               // Trend identification period
input bool     TradeAccumulation = true;       // Trade accumulation phases
input bool     TradeDistribution = true;       // Trade distribution phases

input group "Exit Settings"
input double   TakeProfitMultiplier = 2.0;     // Take profit multiplier (x ATR)
input double   StopLossMultiplier = 1.0;       // Stop loss multiplier (x ATR)
input int      ATRPeriod = 14;                 // ATR period
input bool     UseTrailingStop = true;         // Use trailing stop
input double   TrailingStopMultiplier = 1.5;   // Trailing stop (x ATR)

//--- Global variables
CTrade trade;
CWyckoffAnalysis wyckoff;
datetime lastBarTime = 0;
int atrHandle = INVALID_HANDLE;

//+------------------------------------------------------------------+
//| Expert initialization function                                     |
//+------------------------------------------------------------------+
int OnInit()
{
    //--- Set trade parameters
    trade.SetExpertMagicNumber(MagicNumber);
    trade.SetMarginMode();
    trade.SetTypeFillingBySymbol(_Symbol);
    
    //--- Initialize Wyckoff analyzer
    wyckoff.Init(_Symbol, _Period, AccumulationBars, VolumePeriod, VolumeThreshold, TrendPeriod);
    
    //--- Initialize ATR indicator
    atrHandle = iATR(_Symbol, _Period, ATRPeriod);
    if(atrHandle == INVALID_HANDLE)
    {
        Print("Error creating ATR indicator: ", GetLastError());
        return INIT_FAILED;
    }
    
    //--- Print initialization message
    Print("Wyckoff Trading Bot initialized successfully");
    Print("Symbol: ", _Symbol, " Period: ", EnumToString(_Period));
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    //--- Release indicator handle
    if(atrHandle != INVALID_HANDLE)
        IndicatorRelease(atrHandle);
    
    Print("Wyckoff Trading Bot stopped. Reason: ", reason);
}

//+------------------------------------------------------------------+
//| Expert tick function                                              |
//+------------------------------------------------------------------+
void OnTick()
{
    //--- Check for new bar
    datetime currentBarTime = iTime(_Symbol, _Period, 0);
    if(currentBarTime == lastBarTime)
        return;
    lastBarTime = currentBarTime;
    
    //--- Check spread
    double spread = SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
    if(spread > MaxSpread)
    {
        Print("Spread too high: ", spread, " points");
        return;
    }
    
    //--- Update Wyckoff analysis
    wyckoff.Analyze();
    
    //--- Manage existing positions
    ManagePositions();
    
    //--- Check for new trading signals
    CheckForSignals();
}

//+------------------------------------------------------------------+
//| Check for trading signals                                         |
//+------------------------------------------------------------------+
void CheckForSignals()
{
    //--- Get current position
    if(PositionSelect(_Symbol))
        return; // Already in position
    
    //--- Get Wyckoff phase and signal
    ENUM_WYCKOFF_PHASE phase = wyckoff.GetCurrentPhase();
    ENUM_WYCKOFF_SIGNAL signal = wyckoff.GetTradingSignal();
    
    //--- Check for buy signal (end of accumulation)
    if(TradeAccumulation && signal == SIGNAL_BUY)
    {
        if(phase == PHASE_ACCUMULATION_END || phase == PHASE_MARKUP_BEGIN)
        {
            OpenBuyPosition();
        }
    }
    
    //--- Check for sell signal (end of distribution)
    if(TradeDistribution && signal == SIGNAL_SELL)
    {
        if(phase == PHASE_DISTRIBUTION_END || phase == PHASE_MARKDOWN_BEGIN)
        {
            OpenSellPosition();
        }
    }
}

//+------------------------------------------------------------------+
//| Open buy position                                                 |
//+------------------------------------------------------------------+
void OpenBuyPosition()
{
    double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    double atr = GetATR();
    
    //--- Calculate stop loss and take profit
    double stopLoss = ask - (atr * StopLossMultiplier);
    double takeProfit = ask + (atr * TakeProfitMultiplier);
    
    //--- Calculate position size
    double lotSize = CalculateLotSize(ask - stopLoss);
    
    //--- Open position
    if(trade.Buy(lotSize, _Symbol, ask, stopLoss, takeProfit, TradeComment))
    {
        Print("Buy position opened: Lot=", lotSize, " SL=", stopLoss, " TP=", takeProfit);
    }
    else
    {
        Print("Error opening buy position: ", GetLastError());
    }
}

//+------------------------------------------------------------------+
//| Open sell position                                                |
//+------------------------------------------------------------------+
void OpenSellPosition()
{
    double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    double atr = GetATR();
    
    //--- Calculate stop loss and take profit
    double stopLoss = bid + (atr * StopLossMultiplier);
    double takeProfit = bid - (atr * TakeProfitMultiplier);
    
    //--- Calculate position size
    double lotSize = CalculateLotSize(stopLoss - bid);
    
    //--- Open position
    if(trade.Sell(lotSize, _Symbol, bid, stopLoss, takeProfit, TradeComment))
    {
        Print("Sell position opened: Lot=", lotSize, " SL=", stopLoss, " TP=", takeProfit);
    }
    else
    {
        Print("Error opening sell position: ", GetLastError());
    }
}

//+------------------------------------------------------------------+
//| Manage existing positions                                         |
//+------------------------------------------------------------------+
void ManagePositions()
{
    if(!PositionSelect(_Symbol))
        return;
    
    if(!UseTrailingStop)
        return;
    
    //--- Get position details
    ulong ticket = PositionGetInteger(POSITION_TICKET);
    long posType = PositionGetInteger(POSITION_TYPE);
    double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
    double currentSL = PositionGetDouble(POSITION_SL);
    double currentTP = PositionGetDouble(POSITION_TP);
    
    double atr = GetATR();
    double trailingDistance = atr * TrailingStopMultiplier;
    
    //--- Update trailing stop for buy position
    if(posType == POSITION_TYPE_BUY)
    {
        double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
        double newSL = bid - trailingDistance;
        
        if(newSL > currentSL && newSL < bid)
        {
            trade.PositionModify(ticket, newSL, currentTP);
            Print("Trailing stop updated for buy: New SL=", newSL);
        }
    }
    
    //--- Update trailing stop for sell position
    if(posType == POSITION_TYPE_SELL)
    {
        double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
        double newSL = ask + trailingDistance;
        
        if((currentSL == 0 || newSL < currentSL) && newSL > ask)
        {
            trade.PositionModify(ticket, newSL, currentTP);
            Print("Trailing stop updated for sell: New SL=", newSL);
        }
    }
}

//+------------------------------------------------------------------+
//| Calculate lot size based on risk                                  |
//+------------------------------------------------------------------+
double CalculateLotSize(double stopLossDistance)
{
    double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
    double riskAmount = accountBalance * RiskPercent / 100.0;
    
    double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
    double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
    double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
    
    double lotSize = 0;
    if(stopLossDistance > 0)
    {
        lotSize = riskAmount / (stopLossDistance / tickSize * tickValue);
    }
    
    //--- Normalize lot size
    double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
    double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
    
    lotSize = MathFloor(lotSize / stepLot) * stepLot;
    lotSize = MathMax(minLot, MathMin(lotSize, maxLot));
    lotSize = MathMax(MinLotSize, MathMin(lotSize, MaxLotSize));
    
    return lotSize;
}

//+------------------------------------------------------------------+
//| Get ATR value                                                     |
//+------------------------------------------------------------------+
double GetATR()
{
    double atrBuffer[];
    ArraySetAsSeries(atrBuffer, true);
    
    if(CopyBuffer(atrHandle, 0, 0, 1, atrBuffer) <= 0)
    {
        Print("Error copying ATR data: ", GetLastError());
        return 0;
    }
    
    return atrBuffer[0];
}
//+------------------------------------------------------------------+
