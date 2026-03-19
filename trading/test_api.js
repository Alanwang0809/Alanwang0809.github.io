/**
 * 测试交易系统API
 */

const TradingSystem = require('./trading_api.js');

async function testTradingSystem() {
    console.log('🧪 测试小龙虾交易系统API版本');
    console.log('=' .repeat(50));
    
    try {
        // 创建交易系统实例
        const trader = new TradingSystem();
        
        console.log('\n1. 测试配置加载:');
        console.log(`   监控列表: ${trader.watchlist.join(', ')}`);
        console.log(`   最大仓位: ${trader.config.risk.maxPosition * 100}%`);
        
        console.log('\n2. 测试价格获取 (前2个标的):');
        for (let i = 0; i < Math.min(2, trader.watchlist.length); i++) {
            const symbol = trader.watchlist[i];
            console.log(`   获取 ${symbol} 价格...`);
            
            let priceData;
            if (symbol.includes('-USD')) {
                priceData = await trader.getCryptoPrice(symbol);
            } else {
                priceData = await trader.getStockPrice(symbol);
            }
            
            if (priceData) {
                console.log(`     ✅ ${symbol}: $${priceData.price.toFixed(2)}`);
            } else {
                console.log(`     ❌ ${symbol}: 获取失败`);
            }
            
            await trader.sleep(100); // 避免请求过快
        }
        
        console.log('\n3. 测试交易信号生成:');
        
        // 模拟价格数据
        const testPriceData = {
            symbol: 'TEST',
            price: 100,
            changePercent: -5, // 下跌5%
            timestamp: new Date().toISOString()
        };
        
        console.log(`   模拟 ${testPriceData.symbol} 下跌 ${testPriceData.changePercent}%`);
        await trader.checkTradingSignal(testPriceData.symbol, testPriceData);
        
        console.log('\n4. 检查信号文件:');
        try {
            const fs = require('fs');
            if (fs.existsSync('trading_signals.json')) {
                const signals = JSON.parse(fs.readFileSync('trading_signals.json', 'utf8'));
                console.log(`   找到 ${signals.length} 个交易信号`);
                if (signals.length > 0) {
                    const latest = signals[signals.length - 1];
                    console.log(`   最新信号: ${latest.symbol} ${latest.type} @ $${latest.price}`);
                }
            } else {
                console.log('   信号文件不存在');
            }
        } catch (error) {
            console.log(`   读取信号文件失败: ${error.message}`);
        }
        
        console.log('\n' + '=' .repeat(50));
        console.log('✅ 测试完成！系统基本功能正常。');
        console.log('\n下一步:');
        console.log('1. 安装依赖: npm install');
        console.log('2. 运行系统: npm start');
        console.log('3. 或直接运行: node trading_api.js');
        
    } catch (error) {
        console.error('\n❌ 测试失败:', error.message);
        console.error(error.stack);
    }
}

// 运行测试
testTradingSystem().catch(console.error);