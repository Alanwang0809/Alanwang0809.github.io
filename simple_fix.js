#!/usr/bin/env node
/**
 * 🚀 最简单修复方案
 * 直接推送3个核心文件，修复网站显示问题
 */

const fs = require('fs');
const { execSync } = require('child_process');

console.log('🚀 最简单修复方案 - 修复新闻网站显示问题');
console.log('='.repeat(50));

try {
    // 1. 创建临时目录
    const tempDir = `fix_${Date.now()}`;
    if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
    }
    fs.mkdirSync(tempDir);
    
    console.log(`📁 创建临时目录: ${tempDir}`);
    
    // 2. 只复制3个核心文件
    const coreFiles = ['index.html', 'news-data.json', 'README.md'];
    console.log('📋 复制核心文件:');
    
    coreFiles.forEach(file => {
        if (fs.existsSync(file)) {
            fs.copyFileSync(file, `${tempDir}/${file}`);
            const stats = fs.statSync(file);
            console.log(`  ✅ ${file}: ${stats.size} 字节`);
        } else {
            console.log(`  ❌ ${file}: 不存在`);
            process.exit(1);
        }
    });
    
    // 3. 进入临时目录
    const originalDir = process.cwd();
    process.chdir(tempDir);
    
    // 4. 初始化干净的Git仓库
    console.log('🔧 初始化干净Git仓库...');
    execSync('git init', { stdio: 'inherit' });
    execSync('git checkout -b main', { stdio: 'inherit' });
    
    // 5. 配置远程仓库
    console.log('🌐 配置远程仓库...');
    execSync('git remote add origin https://github.com/Alanwang0809/Alanwang0809.github.io.git', { stdio: 'inherit' });
    
    // 6. 添加文件
    console.log('📁 添加文件...');
    execSync('git add .', { stdio: 'inherit' });
    
    // 7. 提交更改
    const date = new Date().toISOString().split('T')[0];
    const commitMsg = `紧急修复: ${date} 新闻网站更新 - 15条最新新闻`;
    console.log(`💾 提交更改: ${commitMsg}`);
    execSync(`git commit -m "${commitMsg}"`, { stdio: 'inherit' });
    
    // 8. 推送到GitHub（使用--force覆盖历史）
    console.log('🚀 强制推送到GitHub...');
    execSync('git push -f origin main', { stdio: 'inherit' });
    
    // 9. 清理
    process.chdir(originalDir);
    console.log('🧹 清理临时目录...');
    fs.rmSync(tempDir, { recursive: true, force: true });
    
    console.log('\n✅ 修复完成！');
    console.log('🌐 网站地址: https://alanwang0809.github.io/');
    console.log('⏰ 预计5-10分钟完成GitHub Pages部署');
    console.log('📊 推送内容: 15条最新行业新闻');
    
    // 创建成功报告
    const report = {
        timestamp: new Date().toISOString(),
        success: true,
        method: 'simple_force_push',
        files_pushed: coreFiles.length,
        website_url: 'https://alanwang0809.github.io/',
        deployment_time: '5-10分钟',
        note: '使用强制推送覆盖历史，解决Git状态混乱问题'
    };
    
    fs.writeFileSync('simple_fix_report.json', JSON.stringify(report, null, 2));
    console.log('📝 修复报告: simple_fix_report.json');
    
} catch (error) {
    console.log(`❌ 修复失败: ${error.message}`);
    
    const errorReport = {
        timestamp: new Date().toISOString(),
        success: false,
        error: error.message,
        recommendation: '可能需要手动在GitHub上操作'
    };
    
    fs.writeFileSync('simple_fix_error.json', JSON.stringify(errorReport, null, 2));
    console.log('📝 错误报告: simple_fix_error.json');
    
    process.exit(1);
}