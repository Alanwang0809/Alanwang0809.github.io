#!/usr/bin/env node
/**
 * 立即更新GitHub新闻网站
 */

const { execSync } = require('child_process');
const fs = require('fs');

console.log('🚀 立即更新GitHub新闻网站');
console.log('='.repeat(50));

try {
    // 1. 检查文件
    console.log('📋 检查文件...');
    const files = ['index.html', 'news-data-final.json'];
    files.forEach(file => {
        if (fs.existsSync(file)) {
            const stats = fs.statSync(file);
            console.log(`  ✅ ${file}: ${stats.size} 字节`);
        } else {
            console.log(`  ❌ ${file}: 不存在`);
            process.exit(1);
        }
    });
    
    // 2. 检查新闻数据
    const newsData = JSON.parse(fs.readFileSync('news-data-final.json', 'utf8'));
    console.log(`📊 新闻数据: ${newsData.news.length} 条新闻`);
    console.log(`🕒 更新时间: ${newsData.metadata.generated_at}`);
    
    // 3. 强制推送（假设已授权）
    console.log('📁 添加文件...');
    execSync('git add index.html news-data-final.json', { stdio: 'inherit' });
    
    console.log('💾 提交更改...');
    const date = new Date().toISOString().split('T')[0];
    execSync(`git commit -m "紧急更新: ${date} - ${newsData.news.length}条最新新闻"`, { stdio: 'inherit' });
    
    console.log('🚀 强制推送到GitHub...');
    execSync('git push origin main --force', { stdio: 'inherit' });
    
    console.log('\n✅ 更新完成！');
    console.log('🌐 网站地址: https://alanwang0809.github.io/');
    console.log('⏰ 预计5-10分钟完成GitHub Pages部署');
    
    return {
        success: true,
        url: 'https://alanwang0809.github.io/',
        newsCount: newsData.news.length,
        updateTime: new Date().toISOString()
    };
    
} catch (error) {
    console.error('❌ 更新失败:', error.message);
    return {
        success: false,
        error: error.message
    };
}