#!/usr/bin/env node
/**
 * 🚀 最终推送脚本
 * 最简单的推送，确保网站更新
 */

const { execSync } = require('child_process');
const fs = require('fs');

console.log('🚀 最终推送脚本 - 修复网站更新问题');
console.log('='.repeat(50));

try {
    // 1. 检查核心文件
    console.log('📋 检查核心文件:');
    const essentialFiles = ['index.html', 'news-data.json', 'README.md'];
    essentialFiles.forEach(file => {
        if (fs.existsSync(file)) {
            const stats = fs.statSync(file);
            console.log(`  ✅ ${file}: ${stats.size} 字节 (${stats.mtime.toLocaleString('zh-CN')})`);
        } else {
            console.log(`  ❌ ${file}: 不存在`);
            process.exit(1);
        }
    });
    
    // 2. 检查news-data.json内容
    const newsData = JSON.parse(fs.readFileSync('news-data.json', 'utf8'));
    console.log(`📊 新闻数据: ${newsData.news.length} 条新闻`);
    console.log(`🕒 更新时间: ${newsData.metadata.generated_at}`);
    
    // 3. 添加文件到Git
    console.log('📁 添加文件到Git...');
    execSync('git add index.html news-data.json README.md', { stdio: 'inherit' });
    
    // 4. 提交更改
    const date = new Date().toISOString().split('T')[0];
    const commitMsg = `最终修复: ${date} 新闻网站更新 - 15条最新新闻`;
    console.log(`💾 提交更改: ${commitMsg}`);
    execSync(`git commit -m "${commitMsg}"`, { stdio: 'inherit' });
    
    // 5. 推送到GitHub
    console.log('🚀 推送到GitHub...');
    execSync('git push origin main', { stdio: 'inherit' });
    
    console.log('\n✅ 推送完成！');
    console.log('🌐 网站地址: https://alanwang0809.github.io/');
    console.log('⏰ 预计5-10分钟完成GitHub Pages部署');
    
    // 创建成功报告
    const report = {
        timestamp: new Date().toISOString(),
        success: true,
        files_pushed: essentialFiles.length,
        news_count: newsData.news.length,
        website_url: 'https://alanwang0809.github.io/',
        deployment_time: '5-10分钟'
    };
    
    fs.writeFileSync('push_final_report.json', JSON.stringify(report, null, 2));
    console.log('📝 推送报告: push_final_report.json');
    
} catch (error) {
    console.log(`❌ 推送失败: ${error.message}`);
    console.log('💡 建议: 检查网络连接或Git配置');
    process.exit(1);
}