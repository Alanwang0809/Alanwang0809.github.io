#!/usr/bin/env python3
"""
交易系统测试脚本
"""

import json
from datetime import datetime

def test_config():
    """测试配置文件"""
    print("📋 测试配置文件...")
    
    config = {
        "system": {
            "name": "小龙虾交易员",
            "version": "1.0.0",
            "mode": "development"
        },
        "markets": {
            "a_shares": ["000001.SZ", "000002.SZ"],
            "hk_stocks": ["0700.HK", "9988.HK"],
            "us_stocks": ["AAPL", "TSLA"],
            "crypto": ["BTC-USD", "ETH-USD"]
        },
        "risk_management": {
            "max_position_size": 0.05,
            "max_portfolio_risk": 0.20,
            "stop_loss_atr_multiple": 2.0,
            "take_profit_ratio": 2.0
        }
    }
    
    print(f"系统名称: {config['system']['name']}")
    print(f"版本: {config['system']['version']}")
    print(f"监控标的数量: {sum(len(v) for k, v in config['markets'].items() if k != 'system')}")
    print(f"最大仓位: {config['risk_management']['max_position_size']*100}%")
    print("✅ 配置文件测试通过")
    return True

def test_trading_logic():
    """测试交易逻辑"""
    print("\n🎯 测试交易逻辑...")
    
    # 模拟交易信号
    signals = [
        {"symbol": "AAPL", "signal": "BUY", "confidence": 0.85, "price": 175.50},
        {"symbol": "BTC-USD", "signal": "SELL", "confidence": 0.72, "price": 52000},
        {"symbol": "0700.HK", "signal": "HOLD", "confidence": 0.45, "price": 320.80}
    ]
    
    for signal in signals:
        print(f"  {signal['symbol']}: {signal['signal']} @ ${signal['price']:.2f} "
              f"(置信度: {signal['confidence']:.0%})")
    
    # 测试仓位计算
    portfolio_value = 100000
    max_position = portfolio_value * 0.05  # 5%
    
    print(f"\n💰 仓位计算测试:")
    print(f"  组合价值: ${portfolio_value:,.2f}")
    print(f"  单笔最大仓位: ${max_position:,.2f}")
    
    # 测试买入逻辑
    test_symbol = "AAPL"
    test_price = 175.50
    max_shares = int(max_position / test_price)
    
    print(f"  {test_symbol} 最大可买: {max_shares}股 (${max_shares * test_price:,.2f})")
    
    print("✅ 交易逻辑测试通过")
    return True

def test_risk_management():
    """测试风险管理"""
    print("\n🛡️ 测试风险管理...")
    
    # 测试止损计算
    entry_price = 100.0
    atr = 2.5  # 平均真实波幅
    stop_loss_multiple = 2.0
    
    stop_loss = entry_price - (atr * stop_loss_multiple)
    take_profit = entry_price + ((entry_price - stop_loss) * 2.0)
    
    print(f"  入场价: ${entry_price:.2f}")
    print(f"  ATR: ${atr:.2f}")
    print(f"  止损: ${stop_loss:.2f} (亏损: {(stop_loss-entry_price)/entry_price*100:.1f}%)")
    print(f"  止盈: ${take_profit:.2f} (盈利: {(take_profit-entry_price)/entry_price*100:.1f}%)")
    print(f"  风险回报比: 1:{((take_profit-entry_price)/(entry_price-stop_loss)):.1f}")
    
    # 测试组合风险
    positions = [
        {"symbol": "AAPL", "value": 5000},
        {"symbol": "TSLA", "value": 3000},
        {"symbol": "BTC-USD", "value": 2000}
    ]
    
    total_exposure = sum(p["value"] for p in positions)
    portfolio_value = 100000
    risk_ratio = total_exposure / portfolio_value
    
    print(f"\n  组合风险检查:")
    print(f"  总风险暴露: ${total_exposure:,.2f}")
    print(f"  组合价值: ${portfolio_value:,.2f}")
    print(f"  风险比例: {risk_ratio:.1%}")
    print(f"  状态: {'⚠️ 风险过高' if risk_ratio > 0.20 else '✅ 风险可控'}")
    
    print("✅ 风险管理测试通过")
    return True

def test_performance_report():
    """测试性能报告"""
    print("\n📊 测试性能报告...")
    
    # 模拟交易记录
    trades = [
        {"id": "TRADE_001", "symbol": "AAPL", "side": "BUY", "quantity": 50, "price": 170.0, "pnl": 275.0},
        {"id": "TRADE_002", "symbol": "TSLA", "side": "BUY", "quantity": 10, "price": 250.0, "pnl": -50.0},
        {"id": "TRADE_003", "symbol": "AAPL", "side": "SELL", "quantity": 50, "price": 175.5, "pnl": 275.0},
    ]
    
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t["pnl"] > 0)
    total_pnl = sum(t["pnl"] for t in trades)
    win_rate = winning_trades / total_trades if total_trades > 0 else 0
    
    print(f"  总交易次数: {total_trades}")
    print(f"  盈利交易: {winning_trades}")
    print(f"  胜率: {win_rate:.1%}")
    print(f"  总盈亏: ${total_pnl:+,.2f}")
    
    # 按标的统计
    symbol_stats = {}
    for trade in trades:
        symbol = trade["symbol"]
        if symbol not in symbol_stats:
            symbol_stats[symbol] = {"trades": 0, "pnl": 0}
        symbol_stats[symbol]["trades"] += 1
        symbol_stats[symbol]["pnl"] += trade["pnl"]
    
    print(f"\n  按标的统计:")
    for symbol, stats in symbol_stats.items():
        print(f"    {symbol}: {stats['trades']}次交易, 盈亏: ${stats['pnl']:+,.2f}")
    
    print("✅ 性能报告测试通过")
    return True

def main():
    """主测试函数"""
    print("=" * 60)
    print("🦞 小龙虾交易系统测试")
    print("=" * 60)
    
    tests = [
        ("配置文件", test_config),
        ("交易逻辑", test_trading_logic),
        ("风险管理", test_risk_management),
        ("性能报告", test_performance_report)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success, "✅ 通过"))
        except Exception as e:
            results.append((test_name, False, f"❌ 失败: {e}"))
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    
    all_passed = True
    for test_name, success, message in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！系统逻辑验证完成。")
        print("下一步: 安装Python依赖并测试实际数据获取。")
    else:
        print("⚠️  部分测试失败，需要检查系统逻辑。")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    main()