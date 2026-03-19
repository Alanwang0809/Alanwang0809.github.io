#!/usr/bin/env python3
"""
市场数据获取模块
支持多市场、多时间框架数据获取
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional, Union
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketDataFetcher:
    """市场数据获取器"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        self.cache = {}
        
    def get_stock_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
        """
        获取股票数据
        
        Args:
            symbol: 股票代码 (如 "0700.HK", "AAPL")
            period: 时间周期 ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
            interval: 时间间隔 ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
        
        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume
        """
        try:
            logger.info(f"获取股票数据: {symbol}, 周期: {period}, 间隔: {interval}")
            
            # 使用yfinance获取数据
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                logger.warning(f"未获取到 {symbol} 的数据")
                return pd.DataFrame()
            
            # 添加技术分析常用列
            hist['Returns'] = hist['Close'].pct_change()
            hist['Log_Returns'] = np.log(hist['Close'] / hist['Close'].shift(1))
            
            logger.info(f"成功获取 {symbol} 数据，共 {len(hist)} 条记录")
            return hist
            
        except Exception as e:
            logger.error(f"获取股票数据失败: {symbol}, 错误: {e}")
            return pd.DataFrame()
    
    def get_crypto_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
        """
        获取加密货币数据
        
        Args:
            symbol: 加密货币代码 (如 "BTC-USD", "ETH-USD")
            period: 时间周期
            interval: 时间间隔
        
        Returns:
            DataFrame with crypto data
        """
        # yfinance也支持加密货币
        return self.get_stock_data(symbol, period, interval)
    
    def get_multiple_symbols(self, symbols: List[str], **kwargs) -> Dict[str, pd.DataFrame]:
        """
        批量获取多个标的的数据
        
        Args:
            symbols: 标的代码列表
            **kwargs: 传递给get_stock_data的参数
        
        Returns:
            字典: {symbol: DataFrame}
        """
        results = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol, **kwargs)
            if not data.empty:
                results[symbol] = data
            time.sleep(0.1)  # 避免请求过快
        
        return results
    
    def get_real_time_price(self, symbol: str) -> Dict:
        """
        获取实时价格
        
        Args:
            symbol: 标的代码
        
        Returns:
            实时价格信息字典
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'price': info.get('regularMarketPrice', info.get('currentPrice', 0)),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('regularMarketVolume', 0),
                'market_cap': info.get('marketCap', 0),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取实时价格失败: {symbol}, 错误: {e}")
            return {}
    
    def get_market_status(self) -> Dict:
        """
        获取市场状态
        
        Returns:
            各市场状态信息
        """
        # 这里可以扩展为获取各交易所状态
        return {
            'timestamp': datetime.now().isoformat(),
            'markets': {
                'US': 'open' if 9.5 <= datetime.now().hour < 16 else 'closed',
                'HK': 'open' if 9.5 <= datetime.now().hour < 16 else 'closed',
                'crypto': '24/7'
            }
        }

# 示例使用
if __name__ == "__main__":
    import numpy as np
    
    fetcher = MarketDataFetcher()
    
    # 测试获取腾讯股票数据
    tencent_data = fetcher.get_stock_data("0700.HK", period="1mo", interval="1d")
    if not tencent_data.empty:
        print(f"腾讯数据形状: {tencent_data.shape}")
        print(f"最新收盘价: {tencent_data['Close'].iloc[-1]:.2f}")
        print(f"最近5日收益率: {tencent_data['Returns'].tail().sum():.2%}")
    
    # 测试获取比特币数据
    btc_data = fetcher.get_crypto_data("BTC-USD", period="7d", interval="1h")
    if not btc_data.empty:
        print(f"\n比特币数据形状: {btc_data.shape}")
        print(f"最新价格: ${btc_data['Close'].iloc[-1]:.2f}")
    
    # 测试实时价格
    real_time = fetcher.get_real_time_price("AAPL")
    if real_time:
        print(f"\n苹果实时价格: ${real_time['price']:.2f}")
        print(f"涨跌幅: {real_time['change_percent']:.2%}")