//+------------------------------------------------------------------+
//|                                          WyckoffAnalysis.mqh      |
//|                        Copyright 2025, Wyckoff Trading Method    |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, Wyckoff Trading Method"
#property link      "https://www.mql5.com"
#property version   "1.00"

//--- Wyckoff phases enumeration
enum ENUM_WYCKOFF_PHASE
{
    PHASE_ACCUMULATION,         // Accumulation phase
    PHASE_ACCUMULATION_END,     // End of accumulation
    PHASE_MARKUP_BEGIN,         // Beginning of markup
    PHASE_MARKUP,               // Markup phase
    PHASE_DISTRIBUTION,         // Distribution phase
    PHASE_DISTRIBUTION_END,     // End of distribution
    PHASE_MARKDOWN_BEGIN,       // Beginning of markdown
    PHASE_MARKDOWN,             // Markdown phase
    PHASE_NEUTRAL               // Neutral/Ranging phase
};

//--- Trading signals enumeration
enum ENUM_WYCKOFF_SIGNAL
{
    SIGNAL_NONE,                // No signal
    SIGNAL_BUY,                 // Buy signal
    SIGNAL_SELL,                // Sell signal
    SIGNAL_SPRING,              // Spring detected (fake breakdown)
    SIGNAL_UPTHRUST,            // Upthrust detected (fake breakout)
    SIGNAL_SOS,                 // Sign of Strength
    SIGNAL_SOW                  // Sign of Weakness
};

//+------------------------------------------------------------------+
//| Wyckoff Analysis Class                                            |
//+------------------------------------------------------------------+
class CWyckoffAnalysis
{
private:
    //--- Private variables
    string            m_symbol;
    ENUM_TIMEFRAMES   m_period;
    int               m_accumulationBars;
    int               m_volumePeriod;
    double            m_volumeThreshold;
    int               m_trendPeriod;
    
    ENUM_WYCKOFF_PHASE m_currentPhase;
    ENUM_WYCKOFF_SIGNAL m_currentSignal;
    
    double            m_avgVolume;
    double            m_tradingRangeHigh;
    double            m_tradingRangeLow;
    bool              m_inTradingRange;
    
    //--- Volume analysis
    double CalculateAverageVolume();
    bool IsHighVolume(long volume);
    bool IsLowVolume(long volume);
    
    //--- Price action analysis
    bool DetectSpring();
    bool DetectUpthrust();
    bool DetectSignOfStrength();
    bool DetectSignOfWeakness();
    
    //--- Range analysis
    void UpdateTradingRange();
    bool IsPriceInRange(double price);
    
    //--- Trend analysis
    int DetermineTrend();
    
public:
    //--- Constructor/Destructor
    CWyckoffAnalysis();
    ~CWyckoffAnalysis();
    
    //--- Initialization
    void Init(string symbol, ENUM_TIMEFRAMES period, int accumBars, int volPeriod, 
              double volThreshold, int trendPeriod);
    
    //--- Main analysis function
    void Analyze();
    
    //--- Getters
    ENUM_WYCKOFF_PHASE GetCurrentPhase() { return m_currentPhase; }
    ENUM_WYCKOFF_SIGNAL GetTradingSignal() { return m_currentSignal; }
    double GetTradingRangeHigh() { return m_tradingRangeHigh; }
    double GetTradingRangeLow() { return m_tradingRangeLow; }
    bool IsInTradingRange() { return m_inTradingRange; }
};

//+------------------------------------------------------------------+
//| Constructor                                                       |
//+------------------------------------------------------------------+
CWyckoffAnalysis::CWyckoffAnalysis()
{
    m_currentPhase = PHASE_NEUTRAL;
    m_currentSignal = SIGNAL_NONE;
    m_avgVolume = 0;
    m_tradingRangeHigh = 0;
    m_tradingRangeLow = 0;
    m_inTradingRange = false;
}

//+------------------------------------------------------------------+
//| Destructor                                                        |
//+------------------------------------------------------------------+
CWyckoffAnalysis::~CWyckoffAnalysis()
{
}

//+------------------------------------------------------------------+
//| Initialize analyzer                                               |
//+------------------------------------------------------------------+
void CWyckoffAnalysis::Init(string symbol, ENUM_TIMEFRAMES period, int accumBars, 
                            int volPeriod, double volThreshold, int trendPeriod)
{
    m_symbol = symbol;
    m_period = period;
    m_accumulationBars = accumBars;
    m_volumePeriod = volPeriod;
    m_volumeThreshold = volThreshold;
    m_trendPeriod = trendPeriod;
}

//+------------------------------------------------------------------+
//| Main analysis function                                            |
//+------------------------------------------------------------------+
void CWyckoffAnalysis::Analyze()
{
    //--- Calculate average volume
    m_avgVolume = CalculateAverageVolume();
    
    //--- Update trading range
    UpdateTradingRange();
    
    //--- Determine current trend
    int trend = DetermineTrend();
    
    //--- Reset signal
    m_currentSignal = SIGNAL_NONE;
    
    //--- Detect Wyckoff events
    if(DetectSpring())
    {
        m_currentSignal = SIGNAL_SPRING;
        m_currentPhase = PHASE_ACCUMULATION_END;
    }
    else if(DetectUpthrust())
    {
        m_currentSignal = SIGNAL_UPTHRUST;
        m_currentPhase = PHASE_DISTRIBUTION_END;
    }
    else if(DetectSignOfStrength())
    {
        m_currentSignal = SIGNAL_SOS;
        if(m_inTradingRange)
            m_currentPhase = PHASE_MARKUP_BEGIN;
        else
            m_currentPhase = PHASE_MARKUP;
    }
    else if(DetectSignOfWeakness())
    {
        m_currentSignal = SIGNAL_SOW;
        if(m_inTradingRange)
            m_currentPhase = PHASE_MARKDOWN_BEGIN;
        else
            m_currentPhase = PHASE_MARKDOWN;
    }
    else
    {
        //--- Determine phase based on trend and range
        if(m_inTradingRange)
        {
            if(trend > 0)
                m_currentPhase = PHASE_ACCUMULATION;
            else if(trend < 0)
                m_currentPhase = PHASE_DISTRIBUTION;
            else
                m_currentPhase = PHASE_NEUTRAL;
        }
        else
        {
            if(trend > 0)
                m_currentPhase = PHASE_MARKUP;
            else if(trend < 0)
                m_currentPhase = PHASE_MARKDOWN;
            else
                m_currentPhase = PHASE_NEUTRAL;
        }
    }
    
    //--- Generate trading signals based on phase
    if(m_currentPhase == PHASE_ACCUMULATION_END || m_currentPhase == PHASE_MARKUP_BEGIN)
    {
        if(m_currentSignal != SIGNAL_BUY)
            m_currentSignal = SIGNAL_BUY;
    }
    else if(m_currentPhase == PHASE_DISTRIBUTION_END || m_currentPhase == PHASE_MARKDOWN_BEGIN)
    {
        if(m_currentSignal != SIGNAL_SELL)
            m_currentSignal = SIGNAL_SELL;
    }
}

//+------------------------------------------------------------------+
//| Calculate average volume                                          |
//+------------------------------------------------------------------+
double CWyckoffAnalysis::CalculateAverageVolume()
{
    long volumeArray[];
    ArraySetAsSeries(volumeArray, true);
    
    if(CopyTickVolume(m_symbol, m_period, 0, m_volumePeriod, volumeArray) <= 0)
    {
        Print("Error copying volume data: ", GetLastError());
        return 0;
    }
    
    double sum = 0;
    for(int i = 0; i < m_volumePeriod; i++)
    {
        sum += volumeArray[i];
    }
    
    return sum / m_volumePeriod;
}

//+------------------------------------------------------------------+
//| Check if volume is high                                           |
//+------------------------------------------------------------------+
bool CWyckoffAnalysis::IsHighVolume(long volume)
{
    return (volume > m_avgVolume * m_volumeThreshold);
}

//+------------------------------------------------------------------+
//| Check if volume is low                                            |
//+------------------------------------------------------------------+
bool CWyckoffAnalysis::IsLowVolume(long volume)
{
    return (volume < m_avgVolume / m_volumeThreshold);
}

//+------------------------------------------------------------------+
//| Detect Spring (fake breakdown with low volume)                    |
//+------------------------------------------------------------------+
bool CWyckoffAnalysis::DetectSpring()
{
    if(!m_inTradingRange)
        return false;
    
    double close0 = iClose(m_symbol, m_period, 0);
    double close1 = iClose(m_symbol, m_period, 1);
    double low1 = iLow(m_symbol, m_period, 1);
    long volume1 = iVolume(m_symbol, m_period, 1);
    
    //--- Spring: Price breaks below range low but closes back inside on low volume
    if(low1 < m_tradingRangeLow && close1 > m_tradingRangeLow && close0 > close1)
    {
        if(IsLowVolume(volume1))
        {
            return true;
        }
    }
    
    return false;
}

//+------------------------------------------------------------------+
//| Detect Upthrust (fake breakout with low volume)                   |
//+------------------------------------------------------------------+
bool CWyckoffAnalysis::DetectUpthrust()
{
    if(!m_inTradingRange)
        return false;
    
    double close0 = iClose(m_symbol, m_period, 0);
    double close1 = iClose(m_symbol, m_period, 1);
    double high1 = iHigh(m_symbol, m_period, 1);
    long volume1 = iVolume(m_symbol, m_period, 1);
    
    //--- Upthrust: Price breaks above range high but closes back inside on low volume
    if(high1 > m_tradingRangeHigh && close1 < m_tradingRangeHigh && close0 < close1)
    {
        if(IsLowVolume(volume1))
        {
            return true;
        }
    }
    
    return false;
}

//+------------------------------------------------------------------+
//| Detect Sign of Strength                                           |
//+------------------------------------------------------------------+
bool CWyckoffAnalysis::DetectSignOfStrength()
{
    double close0 = iClose(m_symbol, m_period, 0);
    double open0 = iOpen(m_symbol, m_period, 0);
    double close1 = iClose(m_symbol, m_period, 1);
    double high0 = iHigh(m_symbol, m_period, 0);
    long volume0 = iVolume(m_symbol, m_period, 0);
    
    //--- SOS: Strong bullish bar with high volume breaking above range
    bool isBullish = close0 > open0;
    bool isStrong = (close0 - open0) > (high0 - close0) * 2; // Body > 2x upper wick
    bool hasHighVolume = IsHighVolume(volume0);
    bool breakingUp = m_inTradingRange && close0 > m_tradingRangeHigh;
    
    if(isBullish && isStrong && hasHighVolume && (breakingUp || !m_inTradingRange))
    {
        return true;
    }
    
    return false;
}

//+------------------------------------------------------------------+
//| Detect Sign of Weakness                                           |
//+------------------------------------------------------------------+
bool CWyckoffAnalysis::DetectSignOfWeakness()
{
    double close0 = iClose(m_symbol, m_period, 0);
    double open0 = iOpen(m_symbol, m_period, 0);
    double close1 = iClose(m_symbol, m_period, 1);
    double low0 = iLow(m_symbol, m_period, 0);
    long volume0 = iVolume(m_symbol, m_period, 0);
    
    //--- SOW: Strong bearish bar with high volume breaking below range
    bool isBearish = close0 < open0;
    bool isStrong = (open0 - close0) > (close0 - low0) * 2; // Body > 2x lower wick
    bool hasHighVolume = IsHighVolume(volume0);
    bool breakingDown = m_inTradingRange && close0 < m_tradingRangeLow;
    
    if(isBearish && isStrong && hasHighVolume && (breakingDown || !m_inTradingRange))
    {
        return true;
    }
    
    return false;
}

//+------------------------------------------------------------------+
//| Update trading range                                              |
//+------------------------------------------------------------------+
void CWyckoffAnalysis::UpdateTradingRange()
{
    double highArray[];
    double lowArray[];
    double closeArray[];
    ArraySetAsSeries(highArray, true);
    ArraySetAsSeries(lowArray, true);
    ArraySetAsSeries(closeArray, true);
    
    if(CopyHigh(m_symbol, m_period, 0, m_accumulationBars, highArray) <= 0 ||
       CopyLow(m_symbol, m_period, 0, m_accumulationBars, lowArray) <= 0 ||
       CopyClose(m_symbol, m_period, 0, m_accumulationBars, closeArray) <= 0)
    {
        Print("Error copying price data: ", GetLastError());
        return;
    }
    
    //--- Find highest and lowest in the period
    double periodHigh = highArray[ArrayMaximum(highArray)];
    double periodLow = lowArray[ArrayMinimum(lowArray)];
    double rangeSize = periodHigh - periodLow;
    
    //--- Calculate average true range to determine if in trading range
    double atr = 0;
    for(int i = 1; i < m_accumulationBars; i++)
    {
        double tr = MathMax(highArray[i] - lowArray[i],
                    MathMax(MathAbs(highArray[i] - closeArray[i-1]),
                            MathAbs(lowArray[i] - closeArray[i-1])));
        atr += tr;
    }
    atr /= (m_accumulationBars - 1);
    
    //--- In trading range if range is relatively small (less than 3x average ATR)
    m_inTradingRange = (rangeSize < atr * 3.0);
    
    if(m_inTradingRange)
    {
        m_tradingRangeHigh = periodHigh;
        m_tradingRangeLow = periodLow;
    }
}

//+------------------------------------------------------------------+
//| Check if price is in range                                        |
//+------------------------------------------------------------------+
bool CWyckoffAnalysis::IsPriceInRange(double price)
{
    if(!m_inTradingRange)
        return false;
    
    return (price >= m_tradingRangeLow && price <= m_tradingRangeHigh);
}

//+------------------------------------------------------------------+
//| Determine trend direction                                         |
//+------------------------------------------------------------------+
int CWyckoffAnalysis::DetermineTrend()
{
    double closeArray[];
    ArraySetAsSeries(closeArray, true);
    
    if(CopyClose(m_symbol, m_period, 0, m_trendPeriod, closeArray) <= 0)
    {
        Print("Error copying close data: ", GetLastError());
        return 0;
    }
    
    //--- Simple trend determination using moving average slope
    double ma1 = 0, ma2 = 0;
    int period1 = m_trendPeriod / 3;
    int period2 = m_trendPeriod;
    
    for(int i = 0; i < period1; i++)
        ma1 += closeArray[i];
    ma1 /= period1;
    
    for(int i = 0; i < period2; i++)
        ma2 += closeArray[i];
    ma2 /= period2;
    
    double diff = ma1 - ma2;
    double threshold = closeArray[0] * 0.001; // 0.1% threshold
    
    if(diff > threshold)
        return 1;  // Uptrend
    else if(diff < -threshold)
        return -1; // Downtrend
    else
        return 0;  // No clear trend
}
//+------------------------------------------------------------------+
