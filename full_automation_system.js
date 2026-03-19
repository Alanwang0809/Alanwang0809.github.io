#!/usr/bin/env node
/**
 * 🦞 新闻网站全程自动化系统 - Node.js版本
 * 完全自动化，无需手动操作
 * 每天08:30自动运行
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
    // 时间配置
    runTime: '08:30', // 每天运行时间
    timezone: 'Asia/Shanghai', // 时区
    
    // 文件路径
    newsCollectionDir: path.join(__dirname, 'news_collection'),
    newsDataFile: path.join(__dirname, 'news-data.json'),
    indexHtmlFile: path.join(__dirname, 'index.html'),
    
    // GitHub配置
    githubRepo: 'https://github.com/alanwang0809/alanwang0809.github.io.git',
    githubBranch: 'main',
    
    // 日志配置
    logFile: path.join(__dirname, 'automation_log.json')
};

class FullAutomationSystem {
    constructor() {
        console.log('🚀 启动新闻网站全程自动化系统');
        console.log(`⏰ 运行时间: ${CONFIG.runTime} (${CONFIG.timezone})`);
        console.log(`📁 工作目录: ${__dirname}`);
    }
    
    // 步骤1: 检查系统状态
    checkSystemStatus() {
        console.log('\n🔍 步骤1: 检查系统状态');
        
        const checks = [
            { name: '工作目录', check: () => fs.existsSync(__dirname), required: true },
            { name: '新闻收集目录', check: () => fs.existsSync(CONFIG.newsCollectionDir), required: true },
            { name: '新闻数据文件', check: () => fs.existsSync(CONFIG.newsDataFile), required: true },
            { name: '网站HTML文件', check: () => fs.existsSync(CONFIG.indexHtmlFile), required: true },
            { name: 'Git安装', check: () => this.checkCommand('git --version'), required: true },
            { name: 'Node.js环境', check: () => this.checkCommand('node --version'), required: true }
        ];
        
        let allPassed = true;
        checks.forEach(check => {
            const passed = check.check();
            console.log(`  ${passed ? '✅' : '❌'} ${check.name}: ${passed ? '正常' : '异常'}`);
            if (!passed && check.required) {
                allPassed = false;
            }
        });
        
        return allPassed;
    }
    
    // 检查命令是否存在
    checkCommand(cmd) {
        try {
            execSync(cmd, { stdio: 'ignore' });
            return true;
        } catch (error) {
            return false;
        }
    }
    
    // 步骤2: 收集今日新闻
    collectTodayNews() {
        console.log('\n📰 步骤2: 收集今日新闻');
        
        try {
            // 检查是否有今日新闻文件
            const today = new Date();
            const dateStr = today.toISOString().split('T')[0];
            const todayNewsFile = path.join(CONFIG.newsCollectionDir, `${dateStr}_news_for_web.json`);
            
            if (fs.existsSync(todayNewsFile)) {
                console.log(`✅ 找到今日新闻文件: ${todayNewsFile}`);
                return true;
            }
            
            console.log('⚠️ 未找到今日新闻文件，需要运行新闻收集');
            // 这里可以调用新闻收集脚本
            return false;
        } catch (error) {
            console.log(`❌ 新闻收集失败: ${error.message}`);
            return false;
        }
    }
    
    // 步骤3: 更新新闻数据
    updateNewsData() {
        console.log('\n🔄 步骤3: 更新新闻数据');
        
        try {
            // 运行现有的Node.js更新脚本
            const updateScript = path.join(__dirname, 'update_news_data.js');
            if (fs.existsSync(updateScript)) {
                console.log('📝 运行新闻数据更新脚本...');
                execSync(`node "${updateScript}"`, { stdio: 'inherit' });
                console.log('✅ 新闻数据更新完成');
                return true;
            } else {
                console.log('❌ 未找到更新脚本');
                return false;
            }
        } catch (error) {
            console.log(`❌ 新闻数据更新失败: ${error.message}`);
            return false;
        }
    }
    
    // 步骤4: 更新GitHub网站
    updateGitHubWebsite() {
        console.log('\n🚀 步骤4: 更新GitHub网站');
        
        try {
            // 检查Git仓库状态
            const isGitRepo = this.checkCommand('git status');
            if (!isGitRepo) {
                console.log('⚠️ 未初始化Git仓库，正在初始化...');
                execSync('git init', { stdio: 'inherit' });
                execSync('git checkout -b main', { stdio: 'inherit' });
            }
            
            // 检查远程仓库
            try {
                execSync('git remote get-url origin', { stdio: 'ignore' });
            } catch (error) {
                console.log('⚠️ 未配置远程仓库，正在配置...');
                execSync(`git remote add origin ${CONFIG.githubRepo}`, { stdio: 'inherit' });
            }
            
            // 添加文件
            console.log('📁 添加文件到Git...');
            execSync('git add .', { stdio: 'inherit' });
            
            // 提交更改
            const now = new Date();
            const commitMessage = `自动更新: ${now.toISOString().split('T')[0]} 新闻 - 时间: ${now.toLocaleTimeString('zh-CN')}`;
            console.log(`💾 提交更改: ${commitMessage}`);
            execSync(`git commit -m "${commitMessage}"`, { stdio: 'inherit' });
            
            // 推送到GitHub
            console.log('🚀 推送到GitHub...');
            execSync('git push -u origin main --force', { stdio: 'inherit' });
            
            console.log('✅ GitHub网站更新完成');
            return true;
        } catch (error) {
            console.log(`❌ GitHub更新失败: ${error.message}`);
            return false;
        }
    }
    
    // 步骤5: 验证网站更新
    verifyWebsiteUpdate() {
        console.log('\n🔍 步骤5: 验证网站更新');
        
        try {
            // 检查本地文件是否更新
            const newsData = JSON.parse(fs.readFileSync(CONFIG.newsDataFile, 'utf8'));
            const now = new Date();
            const updateTime = new Date(newsData.metadata.generated_at);
            const timeDiff = Math.abs(now - updateTime) / (1000 * 60); // 分钟差
            
            console.log(`📊 新闻总数: ${newsData.news.length}`);
            console.log(`⏰ 更新时间: ${newsData.metadata.generated_at}`);
            console.log(`⏱️ 时间差: ${timeDiff.toFixed(1)} 分钟`);
            
            if (timeDiff < 60) { // 1小时内更新
                console.log('✅ 网站更新验证通过');
                return true;
            } else {
                console.log('⚠️ 网站可能未及时更新');
                return false;
            }
        } catch (error) {
            console.log(`❌ 验证失败: ${error.message}`);
            return false;
        }
    }
    
    // 步骤6: 记录日志
    logAutomationResult(results) {
        console.log('\n📝 步骤6: 记录自动化日志');
        
        try {
            const logEntry = {
                timestamp: new Date().toISOString(),
                beijing_time: new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString(),
                system: '新闻网站全程自动化系统',
                version: '2.0',
                results: results,
                status: results.every(r => r.success) ? 'success' : 'partial_failure',
                next_run: `明天 ${CONFIG.runTime}`
            };
            
            let logData = [];
            if (fs.existsSync(CONFIG.logFile)) {
                logData = JSON.parse(fs.readFileSync(CONFIG.logFile, 'utf8'));
            }
            
            logData.push(logEntry);
            
            // 只保留最近30天的日志
            if (logData.length > 30) {
                logData = logData.slice(-30);
            }
            
            fs.writeFileSync(CONFIG.logFile, JSON.stringify(logData, null, 2), 'utf8');
            console.log('✅ 自动化日志记录完成');
            
            return logEntry;
        } catch (error) {
            console.log(`❌ 日志记录失败: ${error.message}`);
            return null;
        }
    }
    
    // 主运行函数
    async run() {
        console.log('='.repeat(60));
        console.log('🦞 新闻网站全程自动化系统 - 开始执行');
        console.log('='.repeat(60));
        
        const startTime = Date.now();
        const results = [];
        
        // 执行所有步骤
        const steps = [
            { name: '系统状态检查', func: () => this.checkSystemStatus() },
            { name: '今日新闻收集', func: () => this.collectTodayNews() },
            { name: '新闻数据更新', func: () => this.updateNewsData() },
            { name: 'GitHub网站更新', func: () => this.updateGitHubWebsite() },
            { name: '网站更新验证', func: () => this.verifyWebsiteUpdate() }
        ];
        
        for (const step of steps) {
            console.log(`\n📋 执行: ${step.name}`);
            const stepStart = Date.now();
            
            try {
                const success = step.func();
                const stepTime = ((Date.now() - stepStart) / 1000).toFixed(1);
                
                results.push({
                    step: step.name,
                    success: success,
                    time_seconds: stepTime,
                    timestamp: new Date().toISOString()
                });
                
                console.log(`  ${success ? '✅' : '⚠️'} ${step.name} ${success ? '成功' : '失败'} (${stepTime}s)`);
                
                if (!success && step.name === '系统状态检查') {
                    console.log('❌ 系统状态检查失败，停止执行');
                    break;
                }
            } catch (error) {
                console.log(`❌ ${step.name} 执行异常: ${error.message}`);
                results.push({
                    step: step.name,
                    success: false,
                    error: error.message,
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        // 记录日志
        const logEntry = this.logAutomationResult(results);
        
        // 总结
        const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
        const successCount = results.filter(r => r.success).length;
        const totalSteps = steps.length;
        
        console.log('\n' + '='.repeat(60));
        console.log('📊 自动化执行总结');
        console.log('='.repeat(60));
        console.log(`⏱️ 总执行时间: ${totalTime} 秒`);
        console.log(`✅ 成功步骤: ${successCount}/${totalSteps}`);
        console.log(`📅 下次运行: 明天 ${CONFIG.runTime}`);
        console.log(`🌐 网站地址: https://alanwang0809.github.io/`);
        console.log('='.repeat(60));
        
        if (logEntry) {
            console.log(`📝 日志记录: ${CONFIG.logFile}`);
        }
        
        // 返回结果
        return {
            success: successCount === totalSteps,
            results: results,
            total_time_seconds: totalTime,
            next_run: `明天 ${CONFIG.runTime}`,
            website_url: 'https://alanwang0809.github.io/'
        };
    }
}

// 立即运行自动化系统
if (require.main === module) {
    const automation = new FullAutomationSystem();
    automation.run().then(result => {
        if (result.success) {
            console.log('\n🎉 新闻网站全程自动化执行完成！');
            console.log('🚀 网站已自动更新，无需手动操作');
            console.log('🦞 明天08:30将再次自动运行');
        } else {
            console.log('\n⚠️ 自动化执行部分失败，请检查日志');
            process.exit(1);
        }
    }).catch(error => {
        console.error(`❌ 自动化系统运行失败: ${error.message}`);
        process.exit(1);
    });
}

module.exports = FullAutomationSystem;