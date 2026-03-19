#!/usr/bin/env python3
"""
小龙虾交易机器人核心引擎
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import yaml
import json
from dataclasses import dataclass, asdict
import schedule
import time

from data_fetcher import MarketDataFetcher
from technical_analyzer import TechnicalAnalyzer, TradingSignal, SignalType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Position:
    """持仓信息"""
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    entry_time: str
    stop_loss: float
    take_profit: float
    pnl: float = 0.0
    pnl_percent: float = 0.0

@dataclass
class Trade:
    """交易记录"""
    id: str
    symbol: str
    side: str  # "buy" or "sell"
    quantity: float
    price: float
    timestamp: str
    reason: str
    signal_confidence: float

class TradingBot:
    """交易机器人"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.fetcher = MarketDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        
        # 状态
        self.positions: Dict[str, Position] = {}
        self.trade_history: List[Trade] = []
        self.cash_balance: float = self.config.get('initial_capital', 100000.0)
        self.portfolio_value: float = self.cash_balance
        self.is_running: bool = False
        
        # 监控列表
        self.watchlist: List[str] = self.config['markets'].get('watchlist', [])
        
        logger.info(f"交易机器人初始化完成，初始资金: ${self.cash_balance:,.2f}")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"配置文件加载成功: {config_path}")
            return config
        except Exception as e:
            logger.error(f"配置文件加载失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'initial_capital': 100000.0,
            'max_position_size': 0.05,  # 单笔最大仓位 5%
            'max_portfolio_risk': 0.20,  # 组合最大风险 20%
            'stop_loss_atr_multiple': 2.0,
            'take_profit_ratio': 2.0,
            'markets': {
                'watchlist': ['AAPL', 'MSFT', 'GOOGL', 'BTC-USD', 'ETH-USD']
            },
            'trading_hours': {
                'start': '09:30',
                'end': '16:00'
            }
        }
    
    async def start(self):
        """启动交易机器人"""
        logger.info("🚀 启动小龙虾交易机器人...")
        self.is_running = True
        
        # 启动监控任务
        asyncio.create_task(self._monitoring_loop())
        
        # 启动定期分析任务
        asyncio.create_task(self._analysis_loop())
        
        # 启动风险检查任务
        asyncio.create_task(self._risk_management_loop())
        
        logger.info("交易机器人已启动，开始监控市场...")
    
    async def stop(self):
        """停止交易机器人"""
        logger.info("🛑 停止交易机器人...")
        self.is_running = False
        
        # 平仓所有头寸
        await self.close_all_positions()
        
        logger.info(f"交易机器人已停止，最终组合价值: ${self.portfolio_value:,.2f}")
    
    async def _monitoring_loop(self):
        """监控循环"""
        check_interval = self.config.get('monitoring', {}).get('check_interval', 60)
        
        while self.is_running:
            try:
                # 更新持仓市值
                await self._update_portfolio_value()
                
                # 检查价格警报
                await self._check_price_alerts()
                
                # 检查新闻警报
                await self._check_news_alerts()
                
                # 记录状态
                self._log_status()
                
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"监控循环错误: {e}")
                await asyncio.sleep(10)
    
    async def _analysis_loop(self):
        """分析循环"""
        analysis_interval = 300  # 5分钟
        
        while self.is_running:
            try:
                # 对监控列表中的标的进行分析
                for symbol in self.watchlist:
                    await self._analyze_symbol(symbol)
                
                await asyncio.sleep(analysis_interval)
                
            except Exception as e:
                logger.error(f"分析循环错误: {e}")
                await asyncio.sleep(30)
    
    async def _risk_management_loop(self):
        """风险管理循环"""
        risk_check_interval = 60  # 1分钟
        
        while self.is_running:
            try:
                # 检查止损止盈
                await self._check_stop_loss_take_profit()
                
                # 检查仓位风险
                await self._check_position_risk()
                
                # 检查组合风险
                await self._check_portfolio_risk()
                
                await asyncio.sleep(risk_check_interval)
                
            except Exception as e:
                logger.error(f"风险管理循环错误: {e}")
                await asyncio.sleep(10)
    
    async def _analyze_symbol(self, symbol: str):
        """分析单个标的"""
        try:
            # 获取数据
            data = self.fetcher.get_stock_data(
                symbol, 
                period="1mo", 
                interval="1d"
            )
            
            if data.empty:
                return
            
            # 技术分析
            analyzed_data = self.analyzer.calculate_all_indicators(data)
            
            # 生成信号
            signals = self.analyzer.generate_signals(analyzed_data, symbol)
            
            if signals:
                signal = signals[0]
                
                # 记录信号
                logger.info(f"📈 {symbol} 信号: {signal.signal_type.value} "
                          f"(置信度: {signal.confidence:.2%}, 理由: {signal.reason})")
                
                # 根据信号执行交易
                await self._execute_trade_signal(signal)
                
        except Exception as e:
            logger.error(f"分析标的 {symbol} 错误: {e}")
    
    async def _execute_trade_signal(self, signal: TradingSignal):
        """执行交易信号"""
        try:
            symbol = signal.symbol
            current_price = signal.price
            
            # 检查是否已有持仓
            existing_position = self.positions.get(symbol)
            
            if signal.signal_type in [SignalType.STRONG_BUY, SignalType.BUY]:
                # 买入信号
                if existing_position:
                    logger.info(f"{symbol} 已有持仓，跳过买入")
                    return
                
                # 计算买入数量
                position_size = self._calculate_position_size(symbol, current_price)
                
                if position_size > 0:
                    # 执行买入
                    await self._buy(symbol, position_size, current_price, signal)
                    
            elif signal.signal_type in [SignalType.STRONG_SELL, SignalType.SELL]:
                # 卖出信号
                if existing_position:
                    # 执行卖出
                    await self._sell(symbol, existing_position.quantity, current_price, signal)
                    
        except Exception as e:
            logger.error(f"执行交易信号错误: {e}")
    
    def _calculate_position_size(self, symbol: str, price: float) -> float:
        """计算仓位大小"""
        try:
            # 最大仓位比例
            max_position_pct = self.config.get('max_position_size', 0.05)
            
            # 可用资金
            available_cash = self.cash_balance * 0.95  # 保留5%现金
            
            # 计算最大可买金额
            max_position_value = self.portfolio_value * max_position_pct
            
            # 取较小值
            position_value = min(available_cash, max_position_value)
            
            # 计算数量
            quantity = position_value / price
            
            # 取整
            quantity = int(quantity)
            
            if quantity > 0:
                logger.info(f"{symbol} 计算仓位: {quantity}股，价值: ${quantity * price:,.2f}")
                return quantity
            else:
                return 0
                
        except Exception as e:
            logger.error(f"计算仓位大小错误: {e}")
            return 0
    
    async def _buy(self, symbol: str, quantity: float, price: float, signal: TradingSignal):
        """执行买入"""
        try:
            # 计算总成本
            cost = quantity * price
            
            if cost > self.cash_balance:
                logger.warning(f"资金不足，无法买入 {symbol}")
                return
            
            # 计算止损止盈
            atr = await self._get_atr(symbol)
            stop_loss = price - (atr * self.config.get('stop_loss_atr_multiple', 2.0))
            take_profit = price + ((price - stop_loss) * self.config.get('take_profit_ratio', 2.0))
            
            # 创建持仓
            position = Position(
                symbol=symbol,
                quantity=quantity,
                entry_price=price,
                current_price=price,
                entry_time=datetime.now().isoformat(),
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            # 更新状态
            self.positions[symbol] = position
            self.cash_balance -= cost
            
            # 记录交易
            trade = Trade(
                id=f"TRADE_{len(self.trade_history)+1:06d}",
                symbol=symbol,
                side="buy",
                quantity=quantity,
                price=price,
                timestamp=datetime.now().isoformat(),
                reason=signal.reason,
                signal_confidence=signal.confidence
            )
            self.trade_history.append(trade)
            
            logger.info(f"✅ 买入 {symbol}: {quantity}股 @ ${price:.2f}, "
                      f"成本: ${cost:,.2f}, 止损: ${stop_loss:.2f}, 止盈: ${take_profit:.2f}")
            
        except Exception as e:
            logger.error(f"买入执行错误: {e}")
    
    async def _sell(self, symbol: str, quantity: float, price: float, signal: TradingSignal):
        """执行卖出"""
        try:
            position = self.positions.get(symbol)
            if not position:
                logger.warning(f"没有 {symbol} 的持仓")
                return
            
            # 计算收益
            revenue = quantity * price
            cost = position.quantity * position.entry_price
            pnl = revenue - cost
            pnl_percent = (pnl / cost) * 100
            
            # 更新状态
            del self.positions[symbol]
            self.cash_balance += revenue
            
            # 记录交易
            trade = Trade(
                id=f"TRADE_{len(self.trade_history)+1:06d}",
                symbol=symbol,
                side="sell",
                quantity=quantity,
                price=price,
                timestamp=datetime.now().isoformat(),
                reason=signal.reason,
                signal_confidence=signal.confidence
            )
            self.trade_history.append(trade)
            
            logger.info(f"✅ 卖出 {symbol}: {quantity}股 @ ${price:.2f}, "
                      f"收益: ${pnl:+,.2f} ({pnl_percent:+.2f}%)")
            
        except Exception as e:
            logger.error(f"卖出执行错误: {e}")
    
    async def _get_atr(self, symbol: str) -> float:
        """获取ATR值"""
        try:
            data = self.fetcher.get_stock_data(symbol, period="1mo", interval="1d")
            if not data.empty:
                analyzed = self.analyzer.calculate_all_indicators(data)
                if not analyzed.empty and 'ATR' in analyzed.columns:
                    return float(analyzed['ATR'].iloc[-1])
        except:
            pass
        return 0.0
    
    async def _update_portfolio_value(self):
        """更新组合价值"""
        try:
            # 计算持仓市值
            positions_value = 0.0
            for symbol, position in self.positions.items():
                # 获取最新价格
                real_time = self.fetcher.get_real_time_price(symbol)
                if real_time and 'price' in real_time:
                    current_price = real_time['price']
                    position.current_price = current_price
                    position.pnl = (current_price - position.entry_price) * position.quantity
                    position.pnl_percent = (current_price / position.entry_price - 1) * 100
                    positions_value += current_price * position.quantity
            
            # 更新组合价值
            self.portfolio_value = self.cash_balance + positions_value
            
        except Exception as e:
            logger.error(f"更新组合价值错误: {e}")
    
    async def _check_stop_loss_take_profit(self):
        """检查止损止盈"""
        try:
            for symbol, position in list(self.positions.items()):
                current_price = position.current_price
                
                # 检查止损
                if current_price <= position.stop_loss:
                    logger.warning(f"⚠️ {symbol} 触发止损: ${current_price:.2f} <= ${position.stop_loss:.2f}")
                    await self._sell(symbol, position.quantity, current_price, 
                                   TradingSignal(symbol, SignalType.STRONG_SELL, 1.0, 
                                               current_price, {}, datetime.now().isoformat(), "止损触发"))
                
                # 检查止盈
                elif current_price >= position.take_profit:
                    logger.info(f"🎯 {symbol} 触发止盈: ${current_price:.2f} >= ${position.take_profit:.2f}")
                    await self._sell(symbol, position.quantity, current_price,
                                   TradingSignal(symbol, SignalType.STRONG_SELL, 1.0,
                                               current_price, {}, datetime.now().isoformat(), "止盈触发"))
                    
        except Exception as e:
            logger.error(f"检查止损止盈错误: {e}")
    
    async def _check_position_risk(self):
        """检查仓位风险"""
        # 这里可以添加更复杂的风险检查逻辑
        pass
    
    async def _check_portfolio_risk(self):
        """检查组合风险"""
        try:
            max_risk = self.config.get('max_portfolio_risk', 0.20)
            
            # 计算当前风险
            total_exposure = sum(p.quantity * p.current_price for p in self.positions.values())
            risk_ratio = total_exposure / self.portfolio_value if self.portfolio_value > 0 else 0
            
            if risk_ratio > max_risk:
                logger.warning(f"⚠️ 组合风险过高: {risk_ratio:.1%} > {max_risk:.1%}")
                # 这里可以添加自动减仓逻辑
                
        except Exception as e:
            logger.error(f"检查组合风险错误: {e}")
    
    async def _check_price_alerts(self):
        """检查价格警报"""
        # 这里可以添加价格突破警报逻辑
        pass
    
    async def _check_news_alerts(self):
        """检查新闻警报"""
        # 这里可以添加新闻监控逻辑
        pass
    
    def _log_status(self):
        """记录状态"""
        try:
            status = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_value': self.portfolio_value,
                'cash_balance': self.cash_balance,
                'positions_count': len(self.positions),
                'total_trades': len(self.trade_history),
                'positions': [
                    {
                        'symbol': p.symbol,
                        'quantity': p.quantity,
                        'entry_price': p.entry_price,
                        'current_price': p.current_price,
                        'pnl': p.pnl,
                        'pnl_percent': p.pnl_percent
                    }
                    for p in self.positions.values()
                ]
            }
            
            # 每10分钟记录一次详细状态
            if datetime.now().minute % 10 == 0:
                logger.info(f"📊 状态更新: 组合价值 ${self.portfolio_value:,.2f}, "
                          f"现金 ${self.cash_balance:,.2f}, 持仓 {len(self.positions)}个")
                
        except Exception as e:
            logger.error(f"记录状态错误: {e}")
    
    async def close_all_positions(self):
        """平仓所有头寸"""
        logger.info("开始平仓所有头寸...")
        
        for symbol, position in list(self.positions.items()):
            try:
                real_time = self.fetcher.get_real_time_price(symbol)
                if real_time and 'price' in real_time:
                    await self._sell(symbol, position.quantity, real_time['price'],
                                   TradingSignal(symbol, SignalType.STRONG_SELL, 1.0,
                                               real_time['price'], {}, datetime.now().isoformat(), "系统平仓"))
            except Exception as e:
                logger.error(f"平仓 {symbol} 错误: {e}")
        
        logger.info("所有头寸平仓完成")
    
    def get_performance_report(self) -> Dict:
        """获取性能报告"""
        try:
            total_trades = len(self.trade_history)
            winning_trades = 0
            total_pnl = 0
            
            # 分析交易记录
            trades_by_symbol = {}
            for trade in self.trade_history:
                symbol = trade.symbol
                if symbol not in trades_by_symbol:
                    trades_by_symbol[symbol] = []
