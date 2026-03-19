#!/usr/bin/env node
/**
 * 📡 监控网站更新状态
 * 实时检查GitHub Pages是否已更新
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 配置
const WEBSITE_URL = 'https://alanwang0809.github.io/news-data.json';
const CHECK_INTERVAL = 30000; // 30秒检查一次
const MAX_CHECKS = 20; // 最多检查20次（10分钟）

// 本地最新数据
const localDataPath = path.join(__dirname, 'news-data.json');
const localData = JSON.parse(fs.readFileSync(localDataPath, 'utf8'));
const LOCAL_NEWS_COUNT = localData.news.length;
const LOCAL_UPDATE_TIME = localData.metadata.generated_at;

console.log('📡 开始监控网站更新状态');
console.log('='.repeat(50));
console.log(`🌐 监控网址: ${WEBSITE_URL}`);
console.log(`📊 本地数据: ${LOCAL_NEWS_COUNT} 条新闻`);
console.log(`⏰ 本地更新时间: ${LOCAL_UPDATE_TIME}`);
console.log(`⏱️ 检查间隔: ${CHECK_INTERVAL/1000} 秒`);
console.log(`🕐 最长监控: ${(MAX_CHECKS * CHECK_INTERVAL / 1000 / 60).toFixed(1)} 分钟`);
console.log('='.repeat(50));

let checkCount = 0;
let updateDetected = false;

// 检查网站数据
function checkWebsiteUpdate() {
    checkCount++;
    
    console.log(`\n🔍 检查 #${checkCount} (${new Date().toLocaleTimeString('zh-CN')})`);
    
    const req = https.get(`${WEBSITE_URL}?t=${Date.now()}`, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
            data += chunk;
        });
        
        res.on('end', () => {
            try {
                // 尝试解析JSON
                const websiteData = JSON.parse(data);
                const websiteNewsCount = websiteData.news.length;
                const websiteUpdateTime = websiteData.metadata.generated_at;
                
                console.log(`📊 网站数据: ${websiteNewsCount} 条新闻`);
                console.log(`⏰ 网站更新时间: ${websiteUpdateTime}`);
                
                // 比较数据
                if (websiteNewsCount === LOCAL_NEWS_COUNT && 
                    websiteUpdateTime === LOCAL_UPDATE_TIME) {
                    console.log('✅ ✅ ✅ 网站已更新！数据匹配成功！');
                    console.log(`🎉 新闻数量: ${websiteNewsCount} 条`);
                    console.log(`🕒 更新时间: ${websiteUpdateTime}`);
                    updateDetected = true;
                    
                    // 生成更新确认报告
                    const updateReport = {
                        timestamp: new Date().toISOString(),
                        update_detected: true,
                        check_count: checkCount,
                        website_news_count: websiteNewsCount,
                        website_update_time: websiteUpdateTime,
                        local_news_count: LOCAL_NEWS_COUNT,
                        local_update_time: LOCAL_UPDATE_TIME,
                        match_status: '完全匹配',
                        website_url: 'https://alanwang0809.github.io/',
                        monitoring_duration: `${(checkCount * CHECK_INTERVAL / 1000).toFixed(0)} 秒`
                    };
                    
                    fs.writeFileSync('website_update_confirmed.json', JSON.stringify(updateReport, null, 2));
                    console.log('📝 更新确认报告已保存: website_update_confirmed.json');
                    
                    process.exit(0);
                } else {
                    console.log('⏳ 网站尚未更新或数据不匹配');
                    console.log(`📈 进度: ${checkCount}/${MAX_CHECKS} 次检查`);
                    
                    if (checkCount < MAX_CHECKS) {
                        setTimeout(checkWebsiteUpdate, CHECK_INTERVAL);
                    } else {
                        console.log('\n⚠️ 监控超时，网站可能尚未更新');
                        console.log('💡 可能原因:');
                        console.log('  1. GitHub Pages部署需要更长时间');
                        console.log('  2. 推送可能失败');
                        console.log('  3. 网络缓存问题');
                        
                        const timeoutReport = {
                            timestamp: new Date().toISOString(),
                            update_detected: false,
                            check_count: checkCount,
                            website_news_count: websiteNewsCount,
                            website_update_time: websiteUpdateTime,
                            local_news_count: LOCAL_NEWS_COUNT,
                            local_update_time: LOCAL_UPDATE_TIME,
                            match_status: '不匹配',
                            monitoring_duration: `${(checkCount * CHECK_INTERVAL / 1000).toFixed(0)} 秒`,
                            recommendations: [
                                '等待更长时间（GitHub Pages最多需要10分钟）',
                                '手动刷新浏览器缓存',
                                '检查GitHub仓库的提交状态'
                            ]
                        };
                        
                        fs.writeFileSync('website_update_timeout.json', JSON.stringify(timeoutReport, null, 2));
                        console.log('📝 超时报告已保存: website_update_timeout.json');
                        
                        process.exit(1);
                    }
                }
            } catch (error) {
                console.log(`❌ 解析网站数据失败: ${error.message}`);
                
                if (checkCount < MAX_CHECKS) {
                    setTimeout(checkWebsiteUpdate, CHECK_INTERVAL);
                } else {
                    console.log('\n⚠️ 监控超时，无法获取网站数据');
                    process.exit(1);
                }
            }
        });
    });
    
    req.on('error', (error) => {
        console.log(`❌ 请求失败: ${error.message}`);
        
        if (checkCount < MAX_CHECKS) {
            setTimeout(checkWebsiteUpdate, CHECK_INTERVAL);
        } else {
            console.log('\n⚠️ 监控超时，网络连接问题');
            process.exit(1);
        }
    });
    
    req.setTimeout(10000, () => {
        console.log('⏱️ 请求超时');
        req.destroy();
        
        if (checkCount < MAX_CHECKS) {
            setTimeout(checkWebsiteUpdate, CHECK_INTERVAL);
        }
    });
}

// 开始监控
console.log('\n🚀 开始实时监控...');
checkWebsiteUpdate();

// 添加退出处理
process.on('SIGINT', () => {
    console.log('\n\n🛑 监控被用户中断');
    console.log(`📊 已检查 ${checkCount} 次`);
    console.log(`🔍 更新状态: ${updateDetected ? '已检测到更新' : '未检测到更新'}`);
    process.exit(0);
});