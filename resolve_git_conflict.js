#!/usr/bin/env node
/**
 * 🔧 解决Git冲突脚本
 * 专门处理自动化系统中的Git冲突问题
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔧 解决Git冲突问题');
console.log('='.repeat(50));

// 检查当前Git状态
function checkGitStatus() {
    console.log('\n🔍 检查Git状态...');
    
    try {
        const status = execSync('git status --porcelain', { encoding: 'utf8' }).trim();
        if (status) {
            console.log('⚠️ 有未处理的更改:');
            console.log(status.split('\n').map(line => `  ${line}`).join('\n'));
            return status;
        } else {
            console.log('✅ Git状态干净');
            return '';
        }
    } catch (error) {
        console.log(`❌ Git状态检查失败: ${error.message}`);
        return null;
    }
}

// 检查冲突文件
function checkConflictFiles() {
    console.log('\n🔍 检查冲突文件...');
    
    const conflictFiles = [];
    
    // 检查README.md
    if (fs.existsSync('README.md')) {
        const content = fs.readFileSync('README.md', 'utf8');
        if (content.includes('<<<<<<<') || content.includes('=======') || content.includes('>>>>>>>')) {
            console.log('❌ README.md 有冲突标记');
            conflictFiles.push('README.md');
        } else {
            console.log('✅ README.md 无冲突');
        }
    }
    
    // 检查news-data.json
    if (fs.existsSync('news-data.json')) {
        const content = fs.readFileSync('news-data.json', 'utf8');
        if (content.includes('<<<<<<<') || content.includes('=======') || content.includes('>>>>>>>')) {
            console.log('❌ news-data.json 有冲突标记');
            conflictFiles.push('news-data.json');
        } else {
            console.log('✅ news-data.json 无冲突');
        }
    }
    
    return conflictFiles;
}

// 解决README.md冲突（保留我们的版本）
function resolveReadmeConflict() {
    console.log('\n🔧 解决README.md冲突...');
    
    if (!fs.existsSync('README.md')) {
        console.log('✅ README.md 不存在，无需解决');
        return true;
    }
    
    const content = fs.readFileSync('README.md', 'utf8');
    
    // 检查是否有冲突标记
    if (!content.includes('<<<<<<<')) {
        console.log('✅ README.md 无冲突标记');
        return true;
    }
    
    // 创建我们的版本
    const ourVersion = `# 新闻网站 - 自动更新

自动生成的新闻网站，每日08:30自动更新。

## 文件说明
- index.html: 主网站文件
- news-data.json: 新闻数据（15条最新新闻）
- news_preview.html: 新闻预览页面

## 自动化系统
由小龙虾AI自动维护，无需手动操作。

## 更新时间
- 数据更新时间: 2026-03-19T09:44:29+08:00
- 下次自动更新: 2026-03-20 08:30

## 主题
绿色护眼模式 (#4CAF50)

## 修复记录
- 2026-03-19: 修复GitHub推送保护问题，实现全程自动化`;

    fs.writeFileSync('README.md', ourVersion, 'utf8');
    console.log('✅ README.md 冲突已解决（使用我们的版本）');
    return true;
}

// 解决news-data.json冲突（保留我们的15条新闻）
function resolveNewsDataConflict() {
    console.log('\n🔧 解决news-data.json冲突...');
    
    if (!fs.existsSync('news-data.json')) {
        console.log('❌ news-data.json 不存在');
        return false;
    }
    
    const content = fs.readFileSync('news-data.json', 'utf8');
    
    // 检查是否有冲突标记
    if (!content.includes('<<<<<<<')) {
        console.log('✅ news-data.json 无冲突标记');
        return true;
    }
    
    // 读取我们本地的完整新闻数据
    const localNewsData = JSON.parse(fs.readFileSync('news-data.json', 'utf8'));
    
    // 确保我们有15条新闻
    if (localNewsData.news.length === 15) {
        console.log(`✅ 使用本地新闻数据: ${localNewsData.news.length} 条新闻`);
        
        // 更新元数据
        localNewsData.metadata = {
            generated_at: new Date().toISOString(),
            source: "自动更新系统 - 冲突修复版",
            total_news: localNewsData.news.length,
            categories: ["国际", "国内", "AI科技", "经济金融", "新能源", "商业航天"],
            version: "1.2",
            automation_ready: true,
            next_update: "2026-03-20 08:30",
            conflict_resolved: true
        };
        
        fs.writeFileSync('news-data.json', JSON.stringify(localNewsData, null, 2), 'utf8');
        console.log('✅ news-data.json 冲突已解决（使用我们的15条新闻）');
        return true;
    } else {
        console.log(`⚠️ 本地新闻数量异常: ${localNewsData.news.length} 条`);
        return false;
    }
}

// 完成Git操作
function completeGitOperations() {
    console.log('\n🚀 完成Git操作...');
    
    try {
        // 添加所有文件
        console.log('📁 添加所有文件...');
        execSync('git add .', { stdio: 'inherit' });
        
        // 如果有冲突，需要继续rebase
        const status = execSync('git status', { encoding: 'utf8' });
        if (status.includes('rebase in progress')) {
            console.log('⏳ 继续rebase操作...');
            execSync('git rebase --continue', { stdio: 'inherit' });
        }
        
        // 提交更改
        const commitMessage = `冲突修复: ${new Date().toISOString().split('T')[0]} - 解决Git冲突，保留15条新闻`;
        console.log(`💾 提交更改: ${commitMessage}`);
        execSync(`git commit -m "${commitMessage}"`, { stdio: 'inherit' });
        
        // 推送到main分支
        console.log('🚀 推送到main分支...');
        execSync('git push origin main', { stdio: 'inherit' });
        
        console.log('✅ Git操作完成！');
        return true;
    } catch (error) {
        console.log(`❌ Git操作失败: ${error.message}`);
        
        // 尝试放弃rebase
        try {
            console.log('🔄 尝试放弃rebase...');
            execSync('git rebase --abort', { stdio: 'inherit' });
            console.log('✅ 已放弃rebase');
        } catch (abortError) {
            console.log(`⚠️ 放弃rebase失败: ${abortError.message}`);
        }
        
        return false;
    }
}

// 创建简单的推送脚本（备用方案）
function createSimplePushScript() {
    console.log('\n📝 创建简单推送脚本（备用方案）...');
    
    const scriptContent = `#!/bin/bash
# 🚀 简单GitHub推送脚本
# 解决冲突后直接推送

echo "🔧 解决Git冲突并推送"
echo "======================"

# 1. 检查状态
git status

# 2. 添加所有文件
git add .

# 3. 提交更改
git commit -m "自动更新: $(date +'%Y-%m-%d') 新闻 - 冲突修复版"

# 4. 推送到GitHub
git push origin main

echo "✅ 推送完成！"
echo "🌐 网站地址: https://alanwang0809.github.io/"
echo "⏰ 预计1-3分钟内更新"`;

    fs.writeFileSync('simple_push.sh', scriptContent, 'utf8');
    
    // 创建Windows批处理文件
    const batchContent = `@echo off
echo 🚀 简单GitHub推送脚本
echo ======================

echo 1. 检查状态
git status

echo 2. 添加所有文件
git add .

echo 3. 提交更改
git commit -m "自动更新: %date% 新闻 - 冲突修复版"

echo 4. 推送到GitHub
git push origin main

echo ✅ 推送完成！
echo 🌐 网站地址: https://alanwang0809.github.io/
echo ⏰ 预计1-3分钟内更新
pause`;
    
    fs.writeFileSync('simple_push.bat', batchContent, 'utf8');
    
    console.log('✅ 创建推送脚本: simple_push.sh 和 simple_push.bat');
    return true;
}

// 主函数
async function main() {
    console.log('🦞 Git冲突解决方案');
    console.log('='.repeat(50));
    
    try {
        // 1. 检查当前状态
        const gitStatus = checkGitStatus();
        const conflictFiles = checkConflictFiles();
        
        if (conflictFiles.length === 0 && !gitStatus) {
            console.log('\n✅ 无Git冲突，无需解决');
            createSimplePushScript();
            return { success: true, action: 'no_conflict' };
        }
        
        // 2. 解决冲突
        console.log('\n🔧 开始解决冲突...');
        
        let allResolved = true;
        
        if (conflictFiles.includes('README.md')) {
            const resolved = resolveReadmeConflict();
            if (!resolved) allResolved = false;
        }
        
        if (conflictFiles.includes('news-data.json')) {
            const resolved = resolveNewsDataConflict();
            if (!resolved) allResolved = false;
        }
        
        if (!allResolved) {
            console.log('❌ 冲突解决失败');
            return { success: false, error: '冲突解决失败' };
        }
        
        // 3. 完成Git操作
        const gitSuccess = completeGitOperations();
        
        // 4. 创建备用脚本
        createSimplePushScript();
        
        // 5. 总结
        console.log('\n' + '='.repeat(50));
        console.log('🎯 Git冲突解决完成');
        console.log('='.repeat(50));
        
        const result = {
            success: gitSuccess,
            conflict_files_resolved: conflictFiles,
            git_operation: gitSuccess ? 'completed' : 'failed',
            backup_scripts_created: true,
            timestamp: new Date().toISOString(),
            next_steps: [
                '运行 simple_push.bat 完成推送',
                '等待GitHub Pages部署',
                '访问 https://alanwang0809.github.io/ 验证'
            ]
        };
        
        fs.writeFileSync('git_conflict_resolution_report.json', JSON.stringify(result, null, 2));
        console.log('📝 冲突解决报告已保存: git_conflict_resolution_report.json');
        
        return result;
        
    } catch (error) {
        console.log(`❌ 冲突解决失败: ${error.message}`);
        
        const errorReport = {
            success: false,
            error: error.message,
            timestamp: new Date().toISOString(),
            recommendation: '手动解决Git冲突或使用备用脚本'
        };
        
        fs.writeFileSync('git_conflict_error.json', JSON.stringify(errorReport, null, 2));
        
        return errorReport;
    }
}

// 执行
if (require.main === module) {
    main().then(result => {
        if (result.success) {
            console.log('\n✅ Git冲突解决方案执行成功！');
            console.log('🚀 现在可以运行 simple_push.bat 完成推送。');
        } else {
            console.log('\n⚠️ 冲突解决有部分问题');
            console.log('📋 请查看详细报告了解问题。');
        }
    });
}

module.exports = { main };