#!/usr/bin/env node
/**
 * GitHub自动推送脚本 (Node.js版本)
 * 将新闻网站文件自动推送到GitHub仓库
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class GitHubAutoPush {
    constructor(configFile = 'github_config.json') {
        this.config = this.loadConfig(configFile);
        this.repoUrl = `https://${this.config.github_token}@github.com/${this.config.github_username}/${this.config.github_repo}.git`;
        this.localRepoPath = "temp_github_repo";
    }

    loadConfig(configFile) {
        try {
            const configPath = path.join(__dirname, configFile);
            const configContent = fs.readFileSync(configPath, 'utf8');
            const config = JSON.parse(configContent);

            // 验证必要配置
            const requiredKeys = ['github_token', 'github_username', 'github_repo'];
            for (const key of requiredKeys) {
                if (!(key in config)) {
                    throw new Error(`缺少必要配置: ${key}`);
                }
            }

            return config;
        } catch (error) {
            console.error(`❌ 加载配置文件失败: ${error.message}`);
            throw error;
        }
    }

    runCommand(command, cwd = process.cwd()) {
        try {
            console.log(`📝 执行命令: ${command}`);
            const output = execSync(command, { 
                cwd, 
                encoding: 'utf8',
                stdio: ['pipe', 'pipe', 'pipe']
            });
            console.log(`✅ 命令输出: ${output.trim()}`);
            return { success: true, output };
        } catch (error) {
            console.error(`❌ 命令执行失败: ${error.message}`);
            if (error.stdout) console.log(`标准输出: ${error.stdout.toString()}`);
            if (error.stderr) console.log(`错误输出: ${error.stderr.toString()}`);
            return { success: false, error: error.message };
        }
    }

    prepareFiles() {
        console.log("📁 准备网站文件...");
        
        // 需要推送到GitHub的文件列表
        const filesToPush = [
            'index.html',
            'news-data.json',
            'compact_news_update.html',
            'news_website_template.html'
        ];

        // 检查文件是否存在
        const missingFiles = [];
        for (const file of filesToPush) {
            if (!fs.existsSync(file)) {
                missingFiles.push(file);
            }
        }

        if (missingFiles.length > 0) {
            console.warn(`⚠️  以下文件不存在: ${missingFiles.join(', ')}`);
        }

        return filesToPush.filter(file => !missingFiles.includes(file));
    }

    async pushToGitHub() {
        console.log("=".repeat(50));
        console.log("🚀 开始推送到GitHub");
        console.log("=".repeat(50));

        try {
            // 1. 检查当前Git状态
            console.log("\n1️⃣ 检查Git状态...");
            const gitStatus = this.runCommand('git status');
            if (!gitStatus.success) {
                console.log("⚠️  Git状态检查失败，尝试初始化...");
                this.runCommand('git init');
            }

            // 2. 配置Git用户信息
            console.log("\n2️⃣ 配置Git用户信息...");
            this.runCommand('git config user.name "alanwang0809"');
            this.runCommand('git config user.email "alanwang0809@users.noreply.github.com"');

            // 3. 添加远程仓库（如果不存在）
            console.log("\n3️⃣ 配置远程仓库...");
            const remotes = this.runCommand('git remote -v');
            if (!remotes.output || !remotes.output.includes('origin')) {
                console.log("添加远程仓库...");
                this.runCommand(`git remote add origin ${this.repoUrl}`);
            }

            // 4. 添加所有文件
            console.log("\n4️⃣ 添加文件到Git...");
            this.runCommand('git add .');

            // 5. 提交更改
            console.log("\n5️⃣ 提交更改...");
            const commitMessage = `自动更新新闻网站 - ${new Date().toISOString().split('T')[0]}`;
            this.runCommand(`git commit -m "${commitMessage}"`);

            // 6. 推送到GitHub
            console.log("\n6️⃣ 推送到GitHub...");
            const pushResult = this.runCommand('git push -u origin main --force');
            
            if (pushResult.success) {
                console.log("\n🎉 GitHub推送成功！");
                console.log(`🌐 网站地址: https://${this.config.github_username}.github.io/`);
                return true;
            } else {
                console.error("\n❌ GitHub推送失败");
                return false;
            }

        } catch (error) {
            console.error(`❌ 推送过程出错: ${error.message}`);
            return false;
        }
    }

    async run() {
        console.log("🦞 GitHub自动推送脚本启动");
        console.log(`📊 配置信息:`);
        console.log(`  - 用户名: ${this.config.github_username}`);
        console.log(`  - 仓库: ${this.config.github_repo}`);
        console.log(`  - Token: ${this.config.github_token ? '已配置' : '未配置'}`);

        // 准备文件
        const files = this.prepareFiles();
        console.log(`📁 将推送 ${files.length} 个文件: ${files.join(', ')}`);

        // 推送到GitHub
        const success = await this.pushToGitHub();

        if (success) {
            console.log("\n✅ 自动化流程完成！");
            console.log(`🌐 请访问: https://${this.config.github_username}.github.io/`);
            console.log(`⏰ 下次自动更新: 明天08:30`);
        } else {
            console.log("\n❌ 自动化流程失败，请检查错误信息");
        }

        return success;
    }
}

// 主执行函数
async function main() {
    try {
        const pusher = new GitHubAutoPush();
        await pusher.run();
    } catch (error) {
        console.error(`❌ 脚本执行失败: ${error.message}`);
        process.exit(1);
    }
}

// 执行脚本
if (require.main === module) {
    main();
}

module.exports = GitHubAutoPush;