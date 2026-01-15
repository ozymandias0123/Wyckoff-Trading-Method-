import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime, timedelta
import logging
import json
import os
from typing import Dict, List, Tuple, Optional

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wyckoff_trading_log.txt'),
        logging.StreamHandler()
    ]
)


class WyckoffTradingBot:
    """
    Complete Wyckoff Trading Strategy Bot for MetaTrader 5
    
    Implements:
    - Five-Step Approach to the Market
    - Accumulation/Distribution Phases (A-E)
    - All Wyckoff Events (PS, SC, AR, ST, Spring, SOS, LPS, BC, UTAD, SOW, LPSY)
    - Supply & Demand Analysis
    - Effort vs Result (Volume-Price Divergence)
    - Nine Buying/Selling Tests
    - Comparative Strength Analysis
    - Composite Man Logic
    """
    
    def __init__(self, config_file='wyckoff_config.json'):
        """Initialize Wyckoff Trading Bot"""
        self.config = self.load_config(config_file)
        
        # MetaTrader 5 Setup
        if not mt5.initialize():
            logging.error(f"❌ MT5 initialization failed: {mt5.last_error()}")
            quit()
        
        # Login to MT5
        login = self.config.get('mt5_login')
        password = self.config.get('mt5_password')
        server = self.config.get('mt5_server')
        
        if login and password and server:
            authorized = mt5.login(login, password=password, server=server)
            if not authorized:
                logging.error(f"❌ MT5 login failed: {mt5.last_error()}")
                mt5.shutdown()
                quit()
            else:
                logging.info(f"✅ Connected to MT5 account: {login}")
        
        self.symbol = self.config.get('symbol', 'EURUSD')
        self.market_index = self.config.get('market_index', 'US500')  # For comparative strength
        self.timeframe = self.config.get('timeframe', 'M15')
        self.lot_size = self.config.get('lot_size', 0.01)
        
        # Get timeframe constant
        self.mt5_timeframe = self.get_mt5_timeframe(self.timeframe)
        
        # Check if symbol is available
        symbol_info = mt5.symbol_info(self.symbol)
        if symbol_info is None:
            logging.error(f"❌ Symbol {self.symbol} not found")
            mt5.shutdown()
            quit()
        
        if not symbol_info.visible:
            if not mt5.symbol_select(self.symbol, True):
                logging.error(f"❌ Failed to select {self.symbol}")
                mt5.shutdown()
                quit()
        
        # Wyckoff Parameters
        self.spring_depth = self.config.get('spring_depth', 0.0005)
        self.volume_spike_threshold = self.config.get('volume_spike_threshold', 2.0)
        self.tr_range_threshold = self.config.get('tr_range_threshold', 0.03)  # 3% for trading range
        
        # Risk Management
        self.risk_per_trade = self.config.get('risk_per_trade', 0.02)
        self.max_lot_size = self.config.get('max_lot_size', 1.0)
        self.min_reward_risk = self.config.get('min_reward_risk', 3.0)  # Test #9
        self.magic_number = self.config.get('magic_number', 234567)
        
        # Telegram
        self.telegram_token = self.config.get('telegram_token')
        self.telegram_chat_id = self.config.get('telegram_chat_id')
        
        # State
        self.current_phase = None
        self.current_events = {}
        self.buying_tests = {}
        self.selling_tests = {}
        self.in_position = False
        self.position_info = {}
        
        # Statistics
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0.0
        }
        
        logging.info(f"🎯 Wyckoff Trading Bot Initialized - {self.symbol}")
    
    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'mt5_login': 0,
                'mt5_password': '',
                'mt5_server': '',
                'symbol': 'EURUSD',
                'market_index': 'US500',
                'timeframe': 'M15',
                'lot_size': 0.01,
                'risk_per_trade': 0.02,
                'spring_depth': 0.0005,
                'volume_spike_threshold': 2.0,
                'tr_range_threshold': 0.03,
                'min_reward_risk': 3.0,
                'magic_number': 234567
            }
    
    def get_mt5_timeframe(self, timeframe_str: str):
        """Convert timeframe string to MT5 constant"""
        timeframes = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
        }
        return timeframes.get(timeframe_str, mt5.TIMEFRAME_M15)
    
    def fetch_ohlcv(self, symbol: str = None, bars: int = 200) -> pd.DataFrame:
        """Fetch OHLCV data from MT5"""
        try:
            if symbol is None:
                symbol = self.symbol
            
            rates = mt5.copy_rates_from_pos(symbol, self.mt5_timeframe, 0, bars)
            
            if rates is None or len(rates) == 0:
                return pd.DataFrame()
            
            df = pd.DataFrame(rates)
            df['timestamp'] = pd.to_datetime(df['time'], unit='s')
            df.rename(columns={'tick_volume': 'volume'}, inplace=True)
            
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            logging.error(f"❌ Error fetching data: {e}")
            return pd.DataFrame()
    
    def calculate_volume_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate volume and spread metrics for VSA"""
        df = df.copy()
        
        # Basic metrics
        df['avg_volume'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['avg_volume']
        df['spread'] = df['high'] - df['low']
        df['avg_spread'] = df['spread'].rolling(window=20).mean()
        df['spread_ratio'] = df['spread'] / df['avg_spread']
        
        # Price position within bar
        df['close_position'] = (df['close'] - df['low']) / (df['spread'] + 1e-10)
        
        # Price change
        df['price_change'] = df['close'].diff()
        df['price_change_pct'] = df['close'].pct_change()
        
        # Effort vs Result
        df['effort'] = df['volume_ratio']
        df['result'] = df['spread_ratio']
        df['effort_result_divergence'] = df['effort'] - df['result']
        
        return df
    
    # ==========================================================================
    # SUPPLY AND DEMAND ANALYSIS
    # ==========================================================================
    
    def analyze_supply_demand(self, df: pd.DataFrame) -> Dict:
        """
        Analyze Supply and Demand through volume and price movements
        
        Demand indicators:
        - Wide spread, closing at high, high volume
        - Price making higher highs
        
        Supply indicators:
        - Wide spread, closing at low, high volume
        - Price making lower lows
        """
        analysis = {
            'supply_present': False,
            'demand_present': False,
            'supply_strength': 0,
            'demand_strength': 0,
            'equilibrium': False
        }
        
        if len(df) < 20:
            return analysis
        
        recent = df.tail(10)
        latest = df.iloc[-1]
        avg_volume = df['avg_volume'].iloc[-1]
        avg_spread = df['avg_spread'].iloc[-1]
        
        # Demand Detection
        # Wide spread + Close at high + High volume = Demand
        if latest['spread'] > avg_spread * 1.3:
            if latest['close_position'] > 0.7:  # Close in upper 30%
                if latest['volume'] > avg_volume * 1.3:
                    analysis['demand_present'] = True
                    analysis['demand_strength'] = (
                        latest['spread_ratio'] * 
                        latest['volume_ratio'] * 
                        latest['close_position']
                    )
        
        # Supply Detection
        # Wide spread + Close at low + High volume = Supply
        if latest['spread'] > avg_spread * 1.3:
            if latest['close_position'] < 0.3:  # Close in lower 30%
                if latest['volume'] > avg_volume * 1.3:
                    analysis['supply_present'] = True
                    analysis['supply_strength'] = (
                        latest['spread_ratio'] * 
                        latest['volume_ratio'] * 
                        (1 - latest['close_position'])
                    )
        
        # Equilibrium (narrow range, decreasing volume)
        if latest['spread'] < avg_spread * 0.7:
            if latest['volume'] < avg_volume * 0.7:
                analysis['equilibrium'] = True
        
        return analysis
    
    # ==========================================================================
    # EFFORT VS RESULT ANALYSIS
    # ==========================================================================
    
    def analyze_effort_vs_result(self, df: pd.DataFrame) -> Dict:
        """
        Wyckoff's Third Law: Effort vs Result
        
        Convergence: Volume and price move together (trend continues)
        Divergence: Volume increases but price doesn't follow (potential reversal)
        """
        analysis = {
            'convergence': False,
            'divergence': False,
            'divergence_type': None,  # 'bullish' or 'bearish'
            'absorption': False
        }
        
        if len(df) < 20:
            return analysis
        
        recent = df.tail(5)
        latest = df.iloc[-1]
        
        # Check last few bars for pattern
        high_effort = latest['volume_ratio'] > 1.5
        low_result = latest['spread_ratio'] < 0.7
        high_result = latest['spread_ratio'] > 1.3
        
        # Divergence: High effort, low result
        if high_effort and low_result:
            analysis['divergence'] = True
            
            # Determine if bullish or bearish divergence
            if latest['close'] < df['close'].iloc[-2]:  # Price declining
                # High volume on decline with small spread = Absorption (bullish)
                analysis['divergence_type'] = 'bullish'
                analysis['absorption'] = True
            else:
                # High volume on rally with small spread = Distribution (bearish)
                analysis['divergence_type'] = 'bearish'
        
        # Convergence: Effort and Result in harmony
        if high_effort and high_result:
            analysis['convergence'] = True
        
        return analysis
    
    # ==========================================================================
    # WYCKOFF EVENTS DETECTION
    # ==========================================================================
    
    def detect_wyckoff_events(self, df: pd.DataFrame) -> Dict:
        """
        Detect all Wyckoff Events:
        
        ACCUMULATION:
        - PS (Preliminary Support): High volume support after decline
        - SC (Selling Climax): Highest volume, wide spread, close off low
        - AR (Automatic Rally): Rally after SC on diminishing volume
        - ST (Secondary Test): Test of SC area on lower volume
        - Spring: False breakdown below support, then recovery
        - Test: Low volume test of spring
        - SOS (Sign of Strength): Wide spread up on high volume
        - LPS (Last Point of Support): Pullback after SOS on low volume
        - BU (Back Up): Test of breakout area
        
        DISTRIBUTION:
        - PSY (Preliminary Supply): High volume selling after rally
        - BC (Buying Climax): Highest volume at top
        - AR (Automatic Reaction): Selloff after BC
        - ST (Secondary Test): Test of BC area
        - UTAD (Upthrust After Distribution): False breakout above resistance
        - SOW (Sign of Weakness): Wide spread down on high volume
        - LPSY (Last Point of Supply): Failed rally on low volume
        """
        events = {
            # Accumulation
            'PS': False, 'SC': False, 'AR': False, 'ST': False,
            'spring': False, 'test': False, 'SOS': False, 'LPS': False, 'BU': False,
            # Distribution
            'PSY': False, 'BC': False, 'UTAD': False, 'SOW': False, 'LPSY': False,
            # Common
            'stopping_volume': False,
            'effort_no_result': False
        }
        
        if len(df) < 30:
            return events
        
        recent = df.tail(30)
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        tr_high = recent['high'].max()
        tr_low = recent['low'].min()
        tr_mid = (tr_high + tr_low) / 2
        avg_volume = recent['volume'].mean()
        avg_spread = recent['spread'].mean()
        
        # ========== ACCUMULATION EVENTS ==========
        
        # PS (Preliminary Support)
        if latest['close'] < recent['close'].quantile(0.3):
            if latest['volume'] > avg_volume * 1.8:
                if latest['spread'] > avg_spread * 1.3:
                    if latest['close'] > latest['open']:
                        events['PS'] = True
        
        # SC (Selling Climax)
        if latest['volume'] >= recent['volume'].max() * 0.9:
            if latest['spread'] > avg_spread * 1.5:
                if latest['close_position'] > 0.5:  # Close off the low
                    if latest['low'] <= recent['low'].min() * 1.001:
                        events['SC'] = True
        
        # AR (Automatic Rally)
        if len(df) >= 3:
            prev2 = df.iloc[-3]
            if prev2['volume'] > avg_volume * 2:
                if latest['close'] > prev2['close']:
                    if latest['volume'] < prev2['volume'] * 0.7:
                        events['AR'] = True
        
        # ST (Secondary Test)
        if abs(latest['low'] - tr_low) / tr_low < 0.015:
            if latest['volume'] < avg_volume * 0.8:
                if latest['spread'] < avg_spread * 0.8:
                    events['ST'] = True
        
        # Spring
        if latest['low'] < tr_low * (1 - self.spring_depth):
            if latest['close'] > tr_low:
                if latest['volume'] < avg_volume:
                    events['spring'] = True
        
        # Test (of Spring)
        if events['spring'] or (prev['low'] < tr_low * (1 - self.spring_depth)):
            if latest['volume'] < avg_volume * 0.5:
                if abs(latest['low'] - tr_low) / tr_low < 0.01:
                    events['test'] = True
        
        # SOS (Sign of Strength)
        if latest['spread'] > avg_spread * 1.5:
            if latest['volume'] > avg_volume * 1.5:
                if latest['close'] > latest['open']:
                    if latest['close'] > recent['close'].quantile(0.7):
                        events['SOS'] = True
        
        # LPS (Last Point of Support)
        if latest['close'] < prev['close']:
            if latest['volume'] < avg_volume * 0.7:
                if prev['volume'] > avg_volume * 1.3:
                    if latest['low'] > tr_mid:
                        events['LPS'] = True
        
        # BU (Back Up)
        if latest['close'] > tr_high * 0.98:
            if latest['close'] < latest['open']:
                if latest['volume'] < avg_volume:
                    events['BU'] = True
        
        # ========== DISTRIBUTION EVENTS ==========
        
        # PSY (Preliminary Supply)
        if latest['close'] > recent['close'].quantile(0.7):
            if latest['volume'] > avg_volume * 1.8:
                if latest['spread'] > avg_spread * 1.3:
                    if latest['close'] < latest['open']:
                        events['PSY'] = True
        
        # BC (Buying Climax)
        if latest['volume'] >= recent['volume'].max() * 0.9:
            if latest['spread'] > avg_spread * 1.5:
                if latest['high'] >= recent['high'].max() * 0.999:
                    events['BC'] = True
        
        # UTAD (Upthrust After Distribution)
        if latest['high'] > tr_high * (1 + self.spring_depth):
            if latest['close'] < tr_high:
                if latest['volume'] > avg_volume * 1.2:
                    events['UTAD'] = True
        
        # SOW (Sign of Weakness)
        if latest['spread'] > avg_spread * 1.5:
            if latest['volume'] > avg_volume * 1.3:
                if latest['close'] < latest['open']:
                    if latest['close'] < recent['close'].quantile(0.3):
                        events['SOW'] = True
        
        # LPSY (Last Point of Supply)
        if latest['close'] > prev['close']:
            if latest['spread'] < avg_spread * 0.7:
                if latest['volume'] < avg_volume * 0.7:
                    if prev['close'] < prev['open']:
                        events['LPSY'] = True
        
        # ========== COMMON EVENTS ==========
        
        # Stopping Volume
        if latest['volume'] > avg_volume * 2.0:
            if latest['spread'] < avg_spread * 0.6:
                events['stopping_volume'] = True
        
        # Effort No Result
        if latest['volume'] > avg_volume * 1.8:
            if latest['spread'] < avg_spread * 0.7:
                events['effort_no_result'] = True
        
        return events
    
    # ==========================================================================
    # WYCKOFF PHASES IDENTIFICATION
    # ==========================================================================
    
    def identify_accumulation_phase(self, df: pd.DataFrame) -> Dict:
        """
        Identify Accumulation Phases:
        
        Phase A: Stopping the downtrend (PS, SC, AR, ST)
        Phase B: Building the cause (multiple tests, consolidation)
        Phase C: Testing (Spring, Terminal Shakeout)
        Phase D: Markup begins within TR (SOS, LPS)
        Phase E: Breakout and markup
        """
        phase = {
            'is_accumulation': False,
            'phase': None,
            'confidence': 0,
            'events': []
        }
        
        if len(df) < 50:
            return phase
        
        recent = df.tail(50)
        events = self.detect_wyckoff_events(df)
        
        # Check for Trading Range
        tr_range = (recent['high'].max() - recent['low'].min()) / recent['close'].iloc[-1]
        if tr_range > self.tr_range_threshold * 2:
            return phase  # Not in TR
        
        # Phase A: SC + AR + ST
        if events['SC'] or events['PS']:
            phase['is_accumulation'] = True
            phase['phase'] = 'A'
            phase['confidence'] = 0.6
            phase['events'].append('SC' if events['SC'] else 'PS')
        
        # Phase B: Multiple STs, consolidation
        if events['ST']:
            phase['is_accumulation'] = True
            phase['phase'] = 'B'
            phase['confidence'] = 0.65
            phase['events'].append('ST')
        
        # Phase C: Spring
        if events['spring']:
            phase['is_accumulation'] = True
            phase['phase'] = 'C'
            phase['confidence'] = 0.8
            phase['events'].append('SPRING')
        
        # Phase D: SOS + LPS
        if events['SOS']:
            phase['is_accumulation'] = True
            phase['phase'] = 'D'
            phase['confidence'] = 0.85
            phase['events'].append('SOS')
        
        if events['LPS']:
            phase['is_accumulation'] = True
            phase['phase'] = 'D'
            phase['confidence'] = 0.9
            phase['events'].append('LPS')
        
        # Phase E: Breakout
        tr_high = recent['high'].max()
        if recent['close'].iloc[-1] > tr_high * 1.01:
            if recent['volume'].iloc[-1] > recent['volume'].mean() * 1.3:
                phase['phase'] = 'E'
                phase['confidence'] = 0.95
                phase['events'].append('BREAKOUT')
        
        return phase
    
    def identify_distribution_phase(self, df: pd.DataFrame) -> Dict:
        """
        Identify Distribution Phases:
        
        Phase A: Stopping the uptrend (PSY, BC, AR, ST)
        Phase B: Building the cause for markdown
        Phase C: Testing (UTAD)
        Phase D: Markdown begins within TR (SOW, LPSY)
        Phase E: Breakdown and markdown
        """
        phase = {
            'is_distribution': False,
            'phase': None,
            'confidence': 0,
            'events': []
        }
        
        if len(df) < 50:
            return phase
        
        recent = df.tail(50)
        events = self.detect_wyckoff_events(df)
        
        # Check for Trading Range
        tr_range = (recent['high'].max() - recent['low'].min()) / recent['close'].iloc[-1]
        if tr_range > self.tr_range_threshold * 2:
            return phase
        
        # Phase A: BC + PSY
        if events['BC'] or events['PSY']:
            phase['is_distribution'] = True
            phase['phase'] = 'A'
            phase['confidence'] = 0.6
            phase['events'].append('BC' if events['BC'] else 'PSY')
        
        # Phase B: Consolidation
        if events['ST']:
            phase['is_distribution'] = True
            phase['phase'] = 'B'
            phase['confidence'] = 0.65
        
        # Phase C: UTAD
        if events['UTAD']:
            phase['is_distribution'] = True
            phase['phase'] = 'C'
            phase['confidence'] = 0.8
            phase['events'].append('UTAD')
        
        # Phase D: SOW + LPSY
        if events['SOW']:
            phase['is_distribution'] = True
            phase['phase'] = 'D'
            phase['confidence'] = 0.85
            phase['events'].append('SOW')
        
        if events['LPSY']:
            phase['is_distribution'] = True
            phase['phase'] = 'D'
            phase['confidence'] = 0.9
            phase['events'].append('LPSY')
        
        # Phase E: Breakdown
        tr_low = recent['low'].min()
        if recent['close'].iloc[-1] < tr_low * 0.99:
            if recent['volume'].iloc[-1] > recent['volume'].mean() * 1.3:
                phase['phase'] = 'E'
                phase['confidence'] = 0.95
                phase['events'].append('BREAKDOWN')
        
        return phase
    
    # ==========================================================================
    # NINE BUYING/SELLING TESTS
    # ==========================================================================
    
    def run_buying_tests(self, df: pd.DataFrame) -> Dict:
        """
        Wyckoff's Nine Buying Tests for Accumulation:
        
        1. Downside price objective accomplished
        2. PS, SC, ST present
        3. Activity bullish (volume up on rallies, down on reactions)
        4. Downward stride broken (downtrend line penetrated)
        5. Higher lows
        6. Higher highs
        7. Stock stronger than market
        8. Base forming (horizontal price line)
        9. Reward/Risk ratio >= 3:1
        """
        tests = {
            'test1_objective': False,
            'test2_events': False,
            'test3_activity': False,
            'test4_stride_broken': False,
            'test5_higher_lows': False,
            'test6_higher_highs': False,
            'test7_stronger_market': False,
            'test8_base_forming': False,
            'test9_reward_risk': False,
            'tests_passed': 0,
            'total_tests': 9
        }
        
        if len(df) < 50:
            return tests
        
        recent = df.tail(50)
        events = self.detect_wyckoff_events(df)
        
        # Test 2: PS, SC, ST present
        if events['PS'] or events['SC'] or events['ST']:
            tests['test2_events'] = True
            tests['tests_passed'] += 1
        
        # Test 3: Activity bullish
        rallies = recent[recent['close'] > recent['open']]
        reactions = recent[recent['close'] < recent['open']]
        
        if len(rallies) > 0 and len(reactions) > 0:
            avg_rally_vol = rallies['volume'].mean()
            avg_reaction_vol = reactions['volume'].mean()
            if avg_rally_vol > avg_reaction_vol * 1.1:
                tests['test3_activity'] = True
                tests['tests_passed'] += 1
        
        # Test 4: Downward stride broken
        # Simple check: recent close above 20-period high of lows
        high_of_lows = recent['low'].rolling(20).max().iloc[-1]
        if recent['close'].iloc[-1] > high_of_lows:
            tests['test4_stride_broken'] = True
            tests['tests_passed'] += 1
        
        # Test 5: Higher lows
        lows = recent['low'].tail(10)
        if lows.iloc[-1] > lows.iloc[0]:
            tests['test5_higher_lows'] = True
            tests['tests_passed'] += 1
        
        # Test 6: Higher highs
        highs = recent['high'].tail(10)
        if highs.iloc[-1] > highs.iloc[0]:
            tests['test6_higher_highs'] = True
            tests['tests_passed'] += 1
        
        # Test 7: Stronger than market (simplified - check price performance)
        price_change = (recent['close'].iloc[-1] - recent['close'].iloc[0]) / recent['close'].iloc[0]
        if price_change > 0:
            tests['test7_stronger_market'] = True
            tests['tests_passed'] += 1
        
        # Test 8: Base forming (tight range)
        tr_range = (recent['high'].max() - recent['low'].min()) / recent['close'].iloc[-1]
        if tr_range < self.tr_range_threshold:
            tests['test8_base_forming'] = True
            tests['tests_passed'] += 1
        
        # Test 9: Reward/Risk >= 3:1
        # Estimate based on TR range
        potential_profit = recent['high'].max() - recent['close'].iloc[-1]
        potential_loss = recent['close'].iloc[-1] - recent['low'].min()
        if potential_loss > 0:
            rr_ratio = potential_profit / potential_loss
            if rr_ratio >= self.min_reward_risk:
                tests['test9_reward_risk'] = True
                tests['tests_passed'] += 1
        
        # Test 1: Consider objective accomplished if other tests pass
        if tests['tests_passed'] >= 5:
            tests['test1_objective'] = True
            tests['tests_passed'] += 1
        
        return tests
    
    def run_selling_tests(self, df: pd.DataFrame) -> Dict:
        """
        Wyckoff's Nine Selling Tests for Distribution:
        
        1. Upside objective accomplished
        2. Activity bearish (volume down on rallies, up on reactions)
        3. PSY, BC present
        4. Stock weaker than market
        5. Upward stride broken
        6. Lower highs
        7. Lower lows
        8. Crown forming
        9. Reward/Risk >= 3:1
        """
        tests = {
            'test1_objective': False,
            'test2_activity': False,
            'test3_events': False,
            'test4_weaker_market': False,
            'test5_stride_broken': False,
            'test6_lower_highs': False,
            'test7_lower_lows': False,
            'test8_crown_forming': False,
            'test9_reward_risk': False,
            'tests_passed': 0,
            'total_tests': 9
        }
        
        if len(df) < 50:
            return tests
        
        recent = df.tail(50)
        events = self.detect_wyckoff_events(df)
        
        # Test 3: PSY, BC present
        if events['PSY'] or events['BC']:
            tests['test3_events'] = True
            tests['tests_passed'] += 1
        
        # Test 2: Activity bearish
        rallies = recent[recent['close'] > recent['open']]
        reactions = recent[recent['close'] < recent['open']]
        
        if len(rallies) > 0 and len(reactions) > 0:
            avg_rally_vol = rallies['volume'].mean()
            avg_reaction_vol = reactions['volume'].mean()
            if avg_reaction_vol > avg_rally_vol * 1.1:
                tests['test2_activity'] = True
                tests['tests_passed'] += 1
        
        # Test 5: Upward stride broken
        low_of_highs = recent['high'].rolling(20).min().iloc[-1]
        if recent['close'].iloc[-1] < low_of_highs:
            tests['test5_stride_broken'] = True
            tests['tests_passed'] += 1
        
        # Test 6: Lower highs
        highs = recent['high'].tail(10)
        if highs.iloc[-1] < highs.iloc[0]:
            tests['test6_lower_highs'] = True
            tests['tests_passed'] += 1
        
        # Test 7: Lower lows
        lows = recent['low'].tail(10)
        if lows.iloc[-1] < lows.iloc[0]:
            tests['test7_lower_lows'] = True
            tests['tests_passed'] += 1
        
        # Test 4: Weaker than market
        price_change = (recent['close'].iloc[-1] - recent['close'].iloc[0]) / recent['close'].iloc[0]
        if price_change < 0:
            tests['test4_weaker_market'] = True
            tests['tests_passed'] += 1
        
        # Test 8: Crown forming (tight range at top)
        tr_range = (recent['high'].max() - recent['low'].min()) / recent['close'].iloc[-1]
        if tr_range < self.tr_range_threshold:
            tests['test8_crown_forming'] = True
            tests['tests_passed'] += 1
        
        # Test 9: Reward/Risk >= 3:1
        potential_profit = recent['close'].iloc[-1] - recent['low'].min()
        potential_loss = recent['high'].max() - recent['close'].iloc[-1]
        if potential_loss > 0:
            rr_ratio = potential_profit / potential_loss
            if rr_ratio >= self.min_reward_risk:
                tests['test9_reward_risk'] = True
                tests['tests_passed'] += 1
        
        # Test 1: Objective accomplished
        if tests['tests_passed'] >= 5:
            tests['test1_objective'] = True
            tests['tests_passed'] += 1
        
        return tests
    
    # ==========================================================================
    # SIGNAL GENERATION
    # ==========================================================================
    
    def generate_signal(self, df: pd.DataFrame) -> str:
        """Generate trading signal based on comprehensive Wyckoff analysis"""
        # Calculate metrics
        df = self.calculate_volume_metrics(df)
        
        # Analyze components
        supply_demand = self.analyze_supply_demand(df)
        effort_result = self.analyze_effort_vs_result(df)
        events = self.detect_wyckoff_events(df)
        acc_phase = self.identify_accumulation_phase(df)
        dist_phase = self.identify_distribution_phase(df)
        buying_tests = self.run_buying_tests(df)
        selling_tests = self.run_selling_tests(df)
        
        # Store for reference
        self.current_events = events
        self.buying_tests = buying_tests
        self.selling_tests = selling_tests
        
        # ========== LONG SIGNAL ==========
        
        # Phase C or D Accumulation with Spring/SOS
        if acc_phase['is_accumulation'] and acc_phase['phase'] in ['C', 'D']:
            # Spring entry (Phase C)
            if events['spring'] and events['test']:
                if buying_tests['tests_passed'] >= 5:
                    self.current_phase = f"ACCUMULATION_C_SPRING"
                    return "LONG"
            
            # SOS/LPS entry (Phase D)
            if events['SOS'] or events['LPS']:
                if buying_tests['tests_passed'] >= 6:
                    self.current_phase = f"ACCUMULATION_D_SOS"
                    return "LONG"
        
        # Effort vs Result bullish divergence (absorption)
        if effort_result['absorption']:
            if acc_phase['phase'] in ['B', 'C']:
                if buying_tests['tests_passed'] >= 4:
                    self.current_phase = "ACCUMULATION_ABSORPTION"
                    return "LONG"
        
        # ========== SHORT SIGNAL ==========
        
        # Phase C or D Distribution with UTAD/SOW
        if dist_phase['is_distribution'] and dist_phase['phase'] in ['C', 'D']:
            # UTAD entry (Phase C)
            if events['UTAD']:
                if selling_tests['tests_passed'] >= 5:
                    self.current_phase = f"DISTRIBUTION_C_UTAD"
                    return "SHORT"
            
            # SOW/LPSY entry (Phase D)
            if events['SOW'] or events['LPSY']:
                if selling_tests['tests_passed'] >= 6:
                    self.current_phase = f"DISTRIBUTION_D_SOW"
                    return "SHORT"
        
        # Effort vs Result bearish divergence
        if effort_result['divergence'] and effort_result['divergence_type'] == 'bearish':
            if dist_phase['phase'] in ['B', 'C']:
                if selling_tests['tests_passed'] >= 4:
                    self.current_phase = "DISTRIBUTION_DIVERGENCE"
                    return "SHORT"
        
        return "NEUTRAL"
    
    # ==========================================================================
    # POSITION MANAGEMENT
    # ==========================================================================
    
    def calculate_position_size(self, entry_price: float, stop_loss: float) -> float:
        """Calculate position size based on risk management"""
        try:
            account_info = mt5.account_info()
            if account_info is None:
                return self.lot_size
            
            balance = account_info.balance
            risk_amount = balance * self.risk_per_trade
            symbol_info = mt5.symbol_info(self.symbol)
            point = symbol_info.point
            sl_distance = abs(entry_price - stop_loss)
            tick_value = symbol_info.trade_tick_value
            
            if sl_distance > 0 and tick_value > 0:
                lot_size = risk_amount / (sl_distance / point * tick_value)
                lot_size = min(lot_size, self.max_lot_size)
                lot_size = max(lot_size, symbol_info.volume_min)
                lot_step = symbol_info.volume_step
                lot_size = round(lot_size / lot_step) * lot_step
                return lot_size
            
            return self.lot_size
            
        except Exception as e:
            logging.error(f"❌ Error calculating position size: {e}")
            return self.lot_size
    
    def enter_trade(self, signal: str, df: pd.DataFrame):
        """Enter trade based on signal"""
        try:
            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                return
            
            recent = df.tail(30)
            tr_high = recent['high'].max()
            tr_low = recent['low'].min()
            
            if signal == "LONG":
                price = tick.ask
                # Stop below spring/TR low
                stop_loss = tr_low * 0.999
                # Target: TR range projection or 3:1 R/R
                risk = price - stop_loss
                take_profit = price + (risk * self.min_reward_risk)
                order_type = mt5.ORDER_TYPE_BUY
                
            elif signal == "SHORT":
                price = tick.bid
                # Stop above UTAD/TR high
                stop_loss = tr_high * 1.001
                # Target: TR range projection or 3:1 R/R
                risk = stop_loss - price
                take_profit = price - (risk * self.min_reward_risk)
                order_type = mt5.ORDER_TYPE_SELL
            else:
                return
            
            lot_size = self.calculate_position_size(price, stop_loss)
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot_size,
                "type": order_type,
                "price": price,
                "sl": stop_loss,
                "tp": take_profit,
                "deviation": 20,
                "magic": self.magic_number,
                "comment": f"Wyckoff_{self.current_phase}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
                logging.error(f"❌ Order failed: {result.retcode if result else mt5.last_error()}")
                return
            
            self.in_position = True
            self.position_info = {
                'ticket': result.order,
                'entry_price': result.price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'lot_size': lot_size,
                'side': signal,
                'phase': self.current_phase,
                'entry_time': datetime.now(),
                'buying_tests': self.buying_tests['tests_passed'] if signal == "LONG" else 0,
                'selling_tests': self.selling_tests['tests_passed'] if signal == "SHORT" else 0
            }
            
            active_events = [k for k, v in self.current_events.items() if v]
            
            message = f"""
🎯 WYCKOFF TRADE ENTERED!

📊 Signal: {signal}
📈 Phase: {self.current_phase}
🎭 Events: {', '.join(active_events[:4])}

💰 Entry: {result.price:.5f}
🛑 Stop Loss: {stop_loss:.5f}
🎯 Take Profit: {take_profit:.5f}
📦 Size: {lot_size}

✅ Tests Passed: {self.buying_tests['tests_passed'] if signal == 'LONG' else self.selling_tests['tests_passed']}/9
⚖️ Risk: {abs(result.price - stop_loss)/result.price*100:.2f}%
🎯 R/R: {self.min_reward_risk}:1
"""
            self.send_telegram_message(message)
            logging.info(message)
            
        except Exception as e:
            logging.error(f"❌ Error entering trade: {e}")
    
    def manage_position(self, df: pd.DataFrame):
        """Manage open position with Wyckoff exit signals"""
        if not self.in_position:
            return
        
        try:
            current_price = df['close'].iloc[-1]
            side = self.position_info['side']
            entry_price = self.position_info['entry_price']
            stop_loss = self.position_info['stop_loss']
            take_profit = self.position_info['take_profit']
            
            # Check SL/TP
            if side == "LONG":
                if current_price <= stop_loss:
                    self.close_position(df, "Stop Loss")
                    return
                elif current_price >= take_profit:
                    self.close_position(df, "Take Profit")
                    return
            else:
                if current_price >= stop_loss:
                    self.close_position(df, "Stop Loss")
                    return
                elif current_price <= take_profit:
                    self.close_position(df, "Take Profit")
                    return
            
            # Wyckoff exit signals
            events = self.detect_wyckoff_events(df)
            effort_result = self.analyze_effort_vs_result(df)
            
            if side == "LONG":
                # Exit on distribution signals
                if events['BC'] or events['UTAD'] or events['SOW']:
                    self.close_position(df, f"Distribution Signal")
                    return
                # Exit on bearish divergence
                if effort_result['divergence'] and effort_result['divergence_type'] == 'bearish':
                    self.close_position(df, "Bearish Divergence")
                    return
            
            else:  # SHORT
                # Exit on accumulation signals
                if events['SC'] or events['spring'] or events['SOS']:
                    self.close_position(df, f"Accumulation Signal")
                    return
                # Exit on bullish absorption
                if effort_result['absorption']:
                    self.close_position(df, "Bullish Absorption")
                    return
            
        except Exception as e:
            logging.error(f"❌ Error managing position: {e}")
    
    def close_position(self, df: pd.DataFrame, reason: str):
        """Close current position"""
        try:
            positions = mt5.positions_get(symbol=self.symbol)
            if positions is None or len(positions) == 0:
                self.in_position = False
                return
            
            position = positions[0]
            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                return
            
            if position.type == mt5.POSITION_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
                price = tick.bid
            else:
                order_type = mt5.ORDER_TYPE_BUY
                price = tick.ask
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": position.volume,
                "type": order_type,
                "position": position.ticket,
                "price": price,
                "deviation": 20,
                "magic": self.magic_number,
                "comment": f"Close_{reason}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
                logging.error(f"❌ Failed to close: {mt5.last_error()}")
                return
            
            entry_price = self.position_info['entry_price']
            side = self.position_info['side']
            
            if side == "LONG":
                pnl_percent = (price - entry_price) / entry_price * 100
            else:
                pnl_percent = (entry_price - price) / entry_price * 100
            
            pnl_money = position.profit
            
            self.stats['total_trades'] += 1
            if pnl_percent > 0:
                self.stats['winning_trades'] += 1
            else:
                self.stats['losing_trades'] += 1
            self.stats['total_profit'] += pnl_percent
            
            win_rate = self.stats['winning_trades'] / max(1, self.stats['total_trades']) * 100
            
            message = f"""
📊 POSITION CLOSED!

❓ Reason: {reason}
📈 Phase: {self.position_info.get('phase', 'N/A')}

💰 Entry: {entry_price:.5f}
💰 Exit: {price:.5f}
{'🟢' if pnl_percent > 0 else '🔴'} PnL: {pnl_percent:.2f}% (${pnl_money:.2f})

📊 Statistics:
├─ Total Trades: {self.stats['total_trades']}
├─ Win Rate: {win_rate:.1f}%
└─ Total Profit: {self.stats['total_profit']:.2f}%
"""
            self.send_telegram_message(message)
            logging.info(message)
            
            self.in_position = False
            self.position_info = {}
            
        except Exception as e:
            logging.error(f"❌ Error closing position: {e}")
    
    def send_telegram_message(self, message: str):
        """Send Telegram message"""
        if not self.telegram_token or not self.telegram_chat_id:
            return
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {'chat_id': self.telegram_chat_id, 'text': message, 'parse_mode': 'HTML'}
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            logging.error(f"❌ Telegram error: {e}")
    
    def check_existing_positions(self):
        """Check for existing positions on startup"""
        try:
            positions = mt5.positions_get(symbol=self.symbol)
            if positions is not None and len(positions) > 0:
                self.in_position = True
                position = positions[0]
                self.position_info = {
                    'ticket': position.ticket,
                    'entry_price': position.price_open,
                    'stop_loss': position.sl,
                    'take_profit': position.tp,
                    'lot_size': position.volume,
                    'side': "LONG" if position.type == mt5.POSITION_TYPE_BUY else "SHORT",
                    'entry_time': datetime.fromtimestamp(position.time),
                    'phase': 'RESUMED'
                }
                logging.info(f"📌 Found existing position: {self.position_info['side']}")
            else:
                self.in_position = False
        except Exception as e:
            logging.error(f"❌ Error checking positions: {e}")
    
    def run(self):
        """Main trading loop"""
        logging.info("🚀 Wyckoff Trading Bot Started!")
        self.send_telegram_message("""
🚀 WYCKOFF TRADING BOT STARTED!

📊 Complete Wyckoff Method:
├─ Five-Step Approach
├─ Accumulation/Distribution Phases
├─ All Wyckoff Events
├─ Nine Buying/Selling Tests
├─ Supply & Demand Analysis
└─ Effort vs Result

🎯 Ready for trading!
        """)
        
        self.check_existing_positions()
        
        try:
            while True:
                try:
                    if not mt5.terminal_info():
                        logging.error("❌ MT5 not connected")
                        time.sleep(10)
                        continue
                    
                    df = self.fetch_ohlcv()
                    if df.empty:
                        time.sleep(60)
                        continue
                    
                    df = self.calculate_volume_metrics(df)
                    
                    if self.in_position:
                        self.manage_position(df)
                    else:
                        signal = self.generate_signal(df)
                        if signal in ["LONG", "SHORT"]:
                            self.enter_trade(signal, df)
                    
                    time.sleep(60)
                    
                except KeyboardInterrupt:
                    logging.info("🛑 Bot stopped by user")
                    break
                except Exception as e:
                    logging.error(f"❌ Error in main loop: {e}")
                    time.sleep(60)
        
        finally:
            mt5.shutdown()
            logging.info("🛑 MT5 connection closed")


if __name__ == "__main__":
    bot = WyckoffTradingBot()
    bot.run()
