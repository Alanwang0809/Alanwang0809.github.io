/**
 * 小龙虾交易系统 - JavaScript API版本
 * 不需要本地Python环境，使用HTTP API获取数据
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

class TradingSystem {
    constructor(configPath = 'config.json') {
        this.config = this.loadConfig(configPath);
        this.watchlist = this.config.watchlist || [];
        this.positions = {};
        this.tradeHistory = [];
        
        console.log('🦞 小龙虾交易系统启动');
        console.log(`监控列表: ${this.watchlist.length} 个标的`);
    }
    
    loadConfig(configPath) {
        try {
            if (fs.existsSync(configPath)) {
                return JSON.parse(fs.readFileSync(configPath, 'utf8'));
            }
        } catch (error) {
            console.warn('配置文件加载失败，使用默认配置');
        }
        
        // 默认配置
        return {
            watchlist: ['AAPL', 'MSFT', 'GOOGL', 'BTC-USD'],
            api: {
                yahoo: 'https://query1.finance.yahoo.com/v8/finance/chart/',
                alphaVantage: 'https://www.alphavantage.co/query',
                coinGecko: 'https://api.coingecko.com/api/v3'
            },
            risk: {
                maxPosition: 0.05, // 5%
                stopLoss: 0.95,    // 5%止损
                takeProfit: 1.10   // 10%止盈
            }
        };
    }
    
    async getStockPrice(symbol) {
        try {
            // 使用Yahoo Finance API
            const url = `${this.config.api.yahoo}${symbol}`;
            const response = await axios.get(url, {
                params: {
                    range: '1d',
                    interval: '1m'
                },
                timeout: 5000
            });
            
            const data = response.data;
            if (data.chart && data.chart.result) {
                const result = data.chart.result[0];
                const quote = result.indicators.quote[0];
                const meta = result.meta;
                
                return {
                    symbol,
                    price: meta.regularMarketPrice,
                    change: meta.regularMarketChange,
                    changePercent: meta.regularMarketChangePercent,
                    high: meta.regularMarketDayHigh,
                    low: meta.regularMarketDayLow,
                    volume: meta.regularMarketVolume,
                    timestamp: new Date().toISOString()
                };
            }
        } catch (error) {
            console.error(`获取 ${symbol} 价格失败:`, error.message);
        }
        
        return null;
    }
    
    async getCryptoPrice(symbol) {
        try {
            // 简化处理，实际需要转换symbol
            const coinId = this.mapSymbolToCoinId(symbol);
            if (!coinId) return null;
            
            const url = `${this.config.api.coinGecko}/simple/price`;
            const response = await axios.get(url, {
                params: {
                    ids: coinId,
                    vs_currencies: 'usd',
                    include_24hr_change: true
                },
                timeout: 5000
            });
            
            const data = response.data[coinId];
            if (data) {
                return {
                    symbol,
                    price: data.usd,
                    changePercent: data.usd_24h_change,
                    timestamp: new Date().toISOString()
                };
            }
        } catch (error) {
            console.error(`获取 ${symbol} 价格失败:`, error.message);
        }
        
        return null;
    }
    
    mapSymbolToCoinId(symbol) {
        const mapping = {
            'BTC-USD': 'bitcoin',
            'ETH-USD': 'ethereum',
            'BNB-USD': 'binancecoin',
            'ADA-USD': 'cardano',
            'SOL-USD': 'solana'
        };
        return mapping[symbol] || null;
    }
    
    async monitorPrices() {
        console.log('\n📈 开始监控价格...');
        
        for (const symbol of this.watchlist) {
            let priceData;
            
            if (symbol.includes('-USD')) {
                priceData = await this.getCryptoPrice(symbol);
            } else {
                priceData = await this.getStockPrice(symbol);
            }
            
            if (priceData) {
                console.log(`${symbol}: $${priceData.price.toFixed(2)} ` +
                          `(${priceData.changePercent >= 0 ? '+' : ''}${priceData.changePercent?.toFixed(2) || '0.00'}%)`);
                
                // 检查交易信号
                await this.checkTradingSignal(symbol, priceData);
            }
            
            // 避免请求过快
            await this.sleep(100);
        }
    }
    
    async checkTradingSignal(symbol, priceData) {
        // 简化的交易信号逻辑
        const position = this.positions[symbol];
        
        if (!position) {
            // 没有持仓，检查买入信号
            if (priceData.changePercent < -3) {
                // 下跌超过3%，考虑买入
                console.log(`  📉 ${symbol} 下跌 ${priceData.changePercent.toFixed(2)}%，考虑买入`);
                await this.generateBuySignal(symbol, priceData);
            }
        } else {
            // 有持仓，检查卖出信号
            const profitPercent = (priceData.price / position.entryPrice - 1) * 100;
            
            if (profitPercent >= 10) {
                // 盈利超过10%，考虑止盈
                console.log(`  🎯 ${symbol} 盈利 ${profitPercent.toFixed(2)}%，考虑止盈`);
                await this.generateSellSignal(symbol, priceData, 'take_profit');
            } else if (profitPercent <= -5) {
                // 亏损超过5%，考虑止损
                console.log(`  ⚠️ ${symbol} 亏损 ${Math.abs(profitPercent).toFixed(2)}%，考虑止损`);
                await this.generateSellSignal(symbol, priceData, 'stop_loss');
            }
        }
    }
    
    async generateBuySignal(symbol, priceData) {
        const signal = {
            id: `SIGNAL_${Date.now()}`,
            symbol,
            type: 'BUY',
            price: priceData.price,
            timestamp: new Date().toISOString(),
            reason: `价格下跌 ${priceData.changePercent.toFixed(2)}%`,
            confidence: Math.min(0.8, Math.abs(priceData.changePercent) / 10)
        };
        
        console.log(`  ✅ 生成买入信号: ${signal.reason}`);
        this.saveSignal(signal);
        
        // 这里可以添加自动交易逻辑
        // await this.executeTrade(signal);
    }
    
    async generateSellSignal(symbol, priceData, reason) {
        const signal = {
            id: `SIGNAL_${Date.now()}`,
            symbol,
            type: 'SELL',
            price: priceData.price,
            timestamp: new Date().toISOString(),
            reason: reason === 'take_profit' ? '达到止盈目标' : '触发止损',
            confidence: 0.9
        };
        
        console.log(`  ✅ 生成卖出信号: ${signal.reason}`);
        this.saveSignal(signal);
    }
    
    saveSignal(signal) {
        const signalsFile = 'trading_signals.json';
        let signals = [];
        
        try {
            if (fs.existsSync(signalsFile)) {
                signals = JSON.parse(fs.readFileSync(signalsFile, 'utf8'));
            }
        } catch (error) {
            // 文件不存在或格式错误
        }
        
        signals.push(signal);
        
        // 只保留最近100个信号
        if (signals.length > 100) {
            signals = signals.slice(-100);
        }
        
        fs.writeFileSync(signalsFile, JSON.stringify(signals, null, 2));
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    async startMonitoring(intervalMinutes = 5) {
        console.log(`\n🔄 开始定时监控，间隔: ${intervalMinutes}分钟`);
        
        while (true) {
            await this.monitorPrices();
            console.log(`\n⏰ 下次检查: ${new Date(Date.now() + intervalMinutes * 60000).toLocaleTimeString()}`);
            await this.sleep(intervalMinutes * 60000);
        }
    }
}

// 使用示例
if (require.main === module) {
    const tradingSystem = new TradingSystem();
    
    // 处理Ctrl+C
    process.on('SIGINT', () => {
        console.log('\n\n🛑 收到停止信号，正在关闭...');
        process.exit(0);
    });
    
    // 开始监控
    tradingSystem.startMonitoring(5).catch(console.error);
}

module.exports = TradingSystem;