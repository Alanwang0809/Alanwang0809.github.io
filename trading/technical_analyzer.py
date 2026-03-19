#!/usr/bin/env python3
"""
技术分析模块
包含各种技术指标计算和信号生成
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import talib
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignalType(Enum):
    """信号类型"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    NEUTRAL = "neutral"
    SELL = "sell"
    STRONG_SELL = "strong_sell"

@dataclass
class TradingSignal:
    """交易信号"""
    symbol: str
    signal_type: SignalType
    confidence: float  # 0-1 置信度
    price: float
    indicators: Dict
    timestamp: str
    reason: str

class TechnicalAnalyzer:
    """技术分析器"""
    
    def __init__(self):
        self.indicators = {}
        
    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算所有技术指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
        
        Returns:
            添加了技术指标的DataFrame
        """
        if df.empty:
            return df
        
        result = df.copy()
        
        # 价格转换
        close = result['Close'].values
        high = result['High'].values
        low = result['Low'].values
        volume = result['Volume'].values
        
        # 1. 趋势指标
        result['SMA_20'] = talib.SMA(close, timeperiod=20)
        result['SMA_50'] = talib.SMA(close, timeperiod=50)
        result['SMA_200'] = talib.SMA(close, timeperiod=200)
        result['EMA_12'] = talib.EMA(close, timeperiod=12)
        result['EMA_26'] = talib.EMA(close, timeperiod=26)
        
        # 2. 动量指标
        result['RSI'] = talib.RSI(close, timeperiod=14)
        result['MACD'], result['MACD_signal'], result['MACD_hist'] = talib.MACD(
            close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        result['Stoch_K'], result['Stoch_D'] = talib.STOCH(
            high, low, close, fastk_period=14, slowk_period=3, slowd_period=3
        )
        
        # 3. 波动率指标
        result['ATR'] = talib.ATR(high, low, close, timeperiod=14)
        result['BB_upper'], result['BB_middle'], result['BB_lower'] = talib.BBANDS(
            close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        
        # 4. 成交量指标
        result['OBV'] = talib.OBV(close, volume)
        
        # 5. 自定义指标
        result['Price_Change'] = result['Close'].pct_change()
        result['Volume_Change'] = result['Volume'].pct_change()
        result['Price_Volume_Ratio'] = result['Price_Change'] / (result['Volume_Change'].abs() + 1e-10)
        
        # 6. 衍生信号
        result['SMA_Crossover'] = self._calculate_crossover(result['SMA_20'], result['SMA_50'])
        result['MACD_Signal'] = self._calculate_macd_signal(result['MACD'], result['MACD_signal'])
        result['BB_Position'] = self._calculate_bb_position(close, result['BB_upper'], result['BB_lower'])
        
        return result
    
    def _calculate_crossover(self, fast_ma: pd.Series, slow_ma: pd.Series) -> pd.Series:
        """计算均线交叉"""
        crossover = pd.Series(0, index=fast_ma.index)
        crossover[(fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))] = 1  # 金叉
        crossover[(fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))] = -1  # 死叉
        return crossover
    
    def _calculate_macd_signal(self, macd: pd.Series, signal: pd.Series) -> pd.Series:
        """计算MACD信号"""
        macd_signal = pd.Series(0, index=macd.index)
        macd_signal[(macd > signal) & (macd.shift(1) <= signal.shift(1))] = 1  # MACD上穿信号线
        macd_signal[(macd < signal) & (macd.shift(1) >= signal.shift(1))] = -1  # MACD下穿信号线
        return macd_signal
    
    def _calculate_bb_position(self, price: np.ndarray, bb_upper: pd.Series, bb_lower: pd.Series) -> pd.Series:
        """计算布林带位置"""
        bb_position = pd.Series(0, index=bb_upper.index)
        bb_position[price > bb_upper] = 1  # 上轨上方
        bb_position[price < bb_lower] = -1  # 下轨下方
        return bb_position
    
    def generate_signals(self, df: pd.DataFrame, symbol: str) -> List[TradingSignal]:
        """
        生成交易信号
        
        Args:
            df: 包含技术指标的DataFrame
            symbol: 标的代码
        
        Returns:
            交易信号列表
        """
        if df.empty or len(df) < 50:
            return []
        
        signals = []
        latest = df.iloc[-1]
        
        # 1. 多重指标综合信号
        buy_signals = 0
        sell_signals = 0
        reasons = []
        
        # RSI信号
        if latest['RSI'] < 30:
            buy_signals += 1
            reasons.append("RSI超卖")
        elif latest['RSI'] > 70:
            sell_signals += 1
            reasons.append("RSI超买")
        
        # MACD信号
        if latest['MACD_Signal'] == 1:
            buy_signals += 1
            reasons.append("MACD金叉")
        elif latest['MACD_Signal'] == -1:
            sell_signals += 1
            reasons.append("MACD死叉")
        
        # 布林带信号
        if latest['BB_Position'] == -1:
            buy_signals += 1
            reasons.append("布林带下轨")
        elif latest['BB_Position'] == 1:
            sell_signals += 1
            reasons.append("布林带上轨")
        
        # 均线排列
        if latest['SMA_20'] > latest['SMA_50'] > latest['SMA_200']:
            buy_signals += 1
            reasons.append("均线多头排列")
        elif latest['SMA_20'] < latest['SMA_50'] < latest['SMA_200']:
            sell_signals += 1
            reasons.append("均线空头排列")
        
        # 成交量确认
        if latest['Volume_Change'] > 0.5 and latest['Price_Change'] > 0:
            buy_signals += 0.5
            reasons.append("放量上涨")
        elif latest['Volume_Change'] > 0.5 and latest['Price_Change'] < 0:
            sell_signals += 0.5
            reasons.append("放量下跌")
        
        # 确定最终信号
        total_signals = buy_signals + sell_signals
        if total_signals == 0:
            signal_type = SignalType.NEUTRAL
            confidence = 0.3
        else:
            signal_strength = (buy_signals - sell_signals) / total_signals
            
            if signal_strength > 0.6:
                signal_type = SignalType.STRONG_BUY
                confidence = min(0.9, 0.5 + abs(signal_strength) * 0.4)
            elif signal_strength > 0.2:
                signal_type = SignalType.BUY
                confidence = 0.5 + abs(signal_strength) * 0.3
            elif signal_strength < -0.6:
                signal_type = SignalType.STRONG_SELL
                confidence = min(0.9, 0.5 + abs(signal_strength) * 0.4)
            elif signal_strength < -0.2:
                signal_type = SignalType.SELL
                confidence = 0.5 + abs(signal_strength) * 0.3
            else:
                signal_type = SignalType.NEUTRAL
                confidence = 0.4
        
        # 创建信号对象
        signal = TradingSignal(
            symbol=symbol,
            signal_type=signal_type,
            confidence=confidence,
            price=latest['Close'],
            indicators={
                'rsi': float(latest['RSI']) if pd.notna(latest['RSI']) else None,
                'macd': float(latest['MACD']) if pd.notna(latest['MACD']) else None,
                'sma_20': float(latest['SMA_20']) if pd.notna(latest['SMA_20']) else None,
                'sma_50': float(latest['SMA_50']) if pd.notna(latest['SMA_50']) else None,
                'bb_position': int(latest['BB_Position']) if pd.notna(latest['BB_Position']) else None,
            },
            timestamp=df.index[-1].isoformat() if hasattr(df.index[-1], 'isoformat') else str(df.index[-1]),
            reason=", ".join(reasons) if reasons else "无明显信号"
        )
        
        signals.append(signal)
        
        # 2. 添加历史信号（可选）
        # 这里可以添加对历史数据的信号检测
        
        return signals
    
    def calculate_support_resistance(self, df: pd.DataFrame, window: int = 20) -> Dict:
        """
        计算支撑位和阻力位
        
        Args:
            df: 价格数据
            window: 窗口大小
        
        Returns:
            支撑阻力位字典
        """
        if len(df) < window:
            return {}
        
        highs = df['High'].rolling(window=window).max()
        lows = df['Low'].rolling(window=window).min()
        
        current_price = df['Close'].iloc[-1]
        
        # 寻找最近的支撑阻力位
        resistance_levels = highs[highs > current_price].tail(5).tolist()
        support_levels = lows[lows < current_price].tail(5).tolist()
        
        return {
            'current_price': float(current_price),
            'resistance_levels': sorted(set(resistance_levels)),
            'support_levels': sorted(set(support_levels), reverse=True),
            'nearest_resistance': min(resistance_levels) if resistance_levels else None,
            'nearest_support': max(support_levels) if support_levels else None,
        }

# 示例使用
if __name__ == "__main__":
    # 模拟数据
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    mock_data = pd.DataFrame({
        'Open': np.random.randn(100).cumsum() + 100,
        'High': np.random.randn(100).cumsum() + 105,
        'Low': np.random.randn(100).cumsum() + 95,
        'Close': np.random.randn(100).cumsum() + 100,
        'Volume': np.random.randint(1000000, 10000000, 100)
    }, index=dates)
    
    mock_data['High'] = mock_data[['Open', 'Close']].max(axis=1) + np.abs(np.random.randn(100))
    mock_data['Low'] = mock_data[['Open', 'Close']].min(axis=1) - np.abs(np.random.randn(100))
    
    # 测试技术分析
    analyzer = TechnicalAnalyzer()
    
    # 计算指标
    analyzed_data = analyzer.calculate_all_indicators(mock_data)
    print(f"数据形状: {analyzed_data.shape}")
    print(f"技术指标列: {list(analyzed_data.columns)}")
    
    # 生成信号
    signals = analyzer.generate_signals(analyzed_data, "TEST")
    if signals:
        signal = signals[0]
        print(f"\n交易信号:")
        print(f"  标的: {signal.symbol}")
        print(f"  信号: {signal.signal_type.value}")
        print(f"  置信度: {signal.confidence:.2%}")
        print(f"  价格: {signal.price:.2f}")
        print(f"  理由: {signal.reason}")
    
    # 计算支撑阻力
    sr_levels = analyzer.calculate_support_resistance(mock_data)
    print(f"\n支撑阻力位:")
    print(f"  当前价格: {sr_levels['current_price']:.2f}")
    print(f"  阻力位: {sr_levels['resistance_levels'][:3]}")
    print(f"  支撑位: {sr_levels['support_levels'][:3]}")