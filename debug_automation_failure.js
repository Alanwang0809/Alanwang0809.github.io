#!/usr/bin/env node
/**
 * 🐛 调试自动化失败问题
 * 找出为什么昨天测试成功，今天失败
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔍 调试自动化失败问题');
console.log('='.repeat(50));

// 1. 检查当前网站状态
console.log('\n1. 📊 检查当前网站状态');
const websiteUrl = 'https://alanwang0809.github.io/';
console.log(`🌐 网站地址: ${websiteUrl}`);

// 2. 检查本地数据状态
console.log('\n2. 📁 检查本地数据状态');
const newsDataPath = path.join(__dirname, 'news-data.json');
if (fs.existsSync(newsDataPath)) {
    const newsData = JSON.parse(fs.readFileSync(newsDataPath, 'utf8'));
    console.log(`✅ 本地新闻数据: ${newsData.news.length} 条新闻`);
    console.log(`⏰ 更新时间: ${newsData.metadata.generated_at}`);
    console.log(`📋 数据来源: ${newsData.metadata.source}`);
} else {
    console.log('❌ 本地新闻数据文件不存在');
}

// 3. 检查Git状态
console.log('\n3. 🔧 检查Git状态');
try {
    const gitStatus = execSync('git status --porcelain', { encoding: 'utf8' }).trim();
    if (gitStatus) {
        console.log('⚠️ 有未提交的更改:');
        console.log(gitStatus.split('\n').map(line => `  ${line}`).join('\n'));
    } else {
        console.log('✅ 所有更改已提交');
    }
} catch (error) {
    console.log(`❌ Git状态检查失败: ${error.message}`);
}

// 4. 检查Git历史
console.log('\n4. 📜 检查Git历史');
try {
    const gitLog = execSync('git log --oneline -10', { encoding: 'utf8' }).trim();
    console.log('最近10次提交:');
    console.log(gitLog.split('\n').map(line => `  ${line}`).join('\n'));
} catch (error) {
    console.log(`❌ Git历史检查失败: ${error.message}`);
}

// 5. 检查远程仓库状态
console.log('\n5. 🌐 检查远程仓库状态');
try {
    const remoteUrl = execSync('git remote get-url origin', { encoding: 'utf8' }).trim();
    console.log(`✅ 远程仓库: ${remoteUrl}`);
    
    // 尝试获取远程状态
    try {
        execSync('git fetch origin', { stdio: 'ignore' });
        const diff = execSync('git log origin/main..main --oneline', { encoding: 'utf8' }).trim();
        if (diff) {
            console.log('🚀 有需要推送的提交:');
            console.log(diff.split('\n').map(line => `  ${line}`).join('\n'));
        } else {
            console.log('✅ 本地和远程已同步');
        }
    } catch (fetchError) {
        console.log('⚠️ 无法获取远程状态');
    }
} catch (error) {
    console.log(`❌ 远程仓库检查失败: ${error.message}`);
}

// 6. 检查自动化脚本
console.log('\n6. 🤖 检查自动化脚本');
const automationScripts = [
    'news_website_automation.py',
    'github_auto_push.py',
    'github_auto_push.js',
    'full_automation_system.js',
    'update_news_data.js'
];

automationScripts.forEach(script => {
    const scriptPath = path.join(__dirname, script);
    if (fs.existsSync(scriptPath)) {
        const stats = fs.statSync(scriptPath);
        console.log(`✅ ${script}: ${(stats.size / 1024).toFixed(1)} KB`);
    } else {
        console.log(`❌ ${script}: 不存在`);
    }
});

// 7. 检查定时任务配置
console.log('\n7. ⏰ 检查定时任务配置');
const cronFiles = [
    'AUTOMATION_SETUP_COMPLETE.md',
    'FULL_AUTOMATION_PLAN.md',
    'HEARTBEAT.md'
];

cronFiles.forEach(file => {
    const filePath = path.join(__dirname, file);
    if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        const hasSchedule = content.includes('08:30') || content.includes('定时');
        console.log(`✅ ${file}: ${hasSchedule ? '包含定时配置' : '无定时配置'}`);
    } else {
        console.log(`❌ ${file}: 不存在`);
    }
});

// 8. 分析失败原因
console.log('\n8. 🐛 分析失败原因');
console.log('='.repeat(50));

const issues = [];

// 检查可能的失败原因
if (fs.existsSync(newsDataPath)) {
    const newsData = JSON.parse(fs.readFileSync(newsDataPath, 'utf8'));
    const updateTime = new Date(newsData.metadata.generated_at);
    const now = new Date();
    const hoursDiff = (now - updateTime) / (1000 * 60 * 60);
    
    if (hoursDiff > 1) {
        issues.push(`新闻数据已过时 (${hoursDiff.toFixed(1)}小时前更新)`);
    }
}

try {
    const gitStatus = execSync('git status --porcelain', { encoding: 'utf8' }).trim();
    if (gitStatus) {
        issues.push('有未提交的Git更改');
    }
} catch (error) {
    issues.push('Git状态检查失败');
}

try {
    execSync('git fetch origin', { stdio: 'ignore' });
    const diff = execSync('git log origin/main..main --oneline', { encoding: 'utf8' }).trim();
    if (diff) {
        issues.push('有未推送的Git提交');
    }
} catch (error) {
    issues.push('无法连接远程仓库');
}

// 输出分析结果
if (issues.length > 0) {
    console.log('🔴 发现的问题:');
    issues.forEach((issue, i) => {
        console.log(`  ${i+1}. ${issue}`);
    });
} else {
    console.log('✅ 未发现明显问题');
}

console.log('\n' + '='.repeat(50));
console.log('🎯 建议的修复步骤:');
console.log('1. 立即手动推送当前更改到GitHub');
console.log('2. 验证网站是否更新');
console.log('3. 修复自动化脚本中的GitHub推送问题');
console.log('4. 设置监控确保明天08:30自动运行');
console.log('='.repeat(50));

// 生成调试报告
const debugReport = {
    timestamp: new Date().toISOString(),
    website_url: websiteUrl,
    local_news_count: fs.existsSync(newsDataPath) ? JSON.parse(fs.readFileSync(newsDataPath, 'utf8')).news.length : 0,
    git_status: 'checked',
    automation_scripts: automationScripts.filter(s => fs.existsSync(path.join(__dirname, s))).length,
    issues_found: issues,
    recommended_action: '手动推送 + 修复自动化'
};

const reportPath = path.join(__dirname, 'debug_report.json');
fs.writeFileSync(reportPath, JSON.stringify(debugReport, null, 2), 'utf8');
console.log(`📝 调试报告已保存: ${reportPath}`);