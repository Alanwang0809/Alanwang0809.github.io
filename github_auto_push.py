#!/usr/bin/env python3
"""
GitHub自动提交脚本
将新闻网站文件自动推送到GitHub仓库
"""

import os
import json
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

class GitHubAutoPush:
    def __init__(self, config_file='github_config.json'):
        """
        初始化GitHub配置
        """
        self.config = self.load_config(config_file)
        self.repo_url = f"https://{self.config['github_token']}@github.com/{self.config['github_username']}/{self.config['github_repo']}.git"
        self.local_repo_path = "temp_github_repo"
        
    def load_config(self, config_file):
        """
        加载配置文件
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证必要配置
            required_keys = ['github_token', 'github_username', 'github_repo']
            for key in required_keys:
                if key not in config:
                    raise ValueError(f"缺少必要配置: {key}")
            
            return config
            
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            raise
    
    def run_command(self, command, cwd=None):
        """
        运行shell命令
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                print(f"命令执行失败: {command}")
                print(f"错误输出: {result.stderr}")
                return False, result.stderr
            
            return True, result.stdout
            
        except Exception as e:
            print(f"执行命令时出错: {e}")
            return False, str(e)
    
    def clone_or_pull_repo(self):
        """
        克隆或拉取GitHub仓库
        """
        if os.path.exists(self.local_repo_path):
            print("📥 拉取最新代码...")
            success, output = self.run_command("git pull", cwd=self.local_repo_path)
            if not success:
                print(f"❌ 拉取失败: {output}")
                return False
        else:
            print("📥 克隆仓库...")
            success, output = self.run_command(f"git clone {self.repo_url} {self.local_repo_path}")
            if not success:
                print(f"❌ 克隆失败: {output}")
                return False
        
        return True
    
    def prepare_website_files(self):
        """
        准备网站文件
        """
        print("📁 准备网站文件...")
        
        # 源文件目录
        source_files = {
            'news_website_template.html': 'index.html',
            'website_data/news-data.json': 'news-data.json'
        }
        
        # 确保目标目录存在
        website_dir = Path(self.local_repo_path)
        
        # 复制文件
        for source, target in source_files.items():
            source_path = Path(source)
            target_path = website_dir / target
            
            if not source_path.exists():
                print(f"⚠️  源文件不存在: {source}")
                continue
            
            # 复制文件
            shutil.copy2(source_path, target_path)
            print(f"  ✅ 复制: {source} -> {target}")
        
        # 创建README文件
        readme_content = f"""# 每日新闻网站

这是一个自动更新的每日新闻网站，由小龙虾AI驱动。

## 功能特点
- 🕗 每日08:30自动更新新闻
- 🤖 AI自动收集和整理新闻
- 🎨 响应式设计，绿色护眼主题
- 📊 多分类筛选和统计
- 🔄 完全自动化更新流程

## 新闻来源
- 新浪新闻
- 澎湃新闻  
- 36氪
- 虎嗅
- 其他权威媒体

## 技术栈
- HTML/CSS/JavaScript
- Python自动化脚本
- GitHub Pages
- GitHub Actions (可选)

## 更新日志
- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: 网站初始化完成

## 维护者
- [Alan](https://github.com/alanwang0809)
- 🦞 小龙虾AI助手

访问网站: https://{self.config['github_username']}.github.io/
"""
        
        readme_path = website_dir / 'README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("  ✅ 创建README.md")
        
        return True
    
    def commit_and_push(self):
        """
        提交并推送到GitHub
        """
        print("📝 提交更改...")
        
        # 切换到仓库目录
        os.chdir(self.local_repo_path)
        
        # 添加所有文件
        success, output = self.run_command("git add .")
        if not success:
            return False
        
        # 提交
        commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 的新闻"
        success, output = self.run_command(f'git commit -m "{commit_message}"')
        if not success:
            # 如果没有更改，也继续
            if "nothing to commit" in output:
                print("ℹ️  没有需要提交的更改")
                return True
            return False
        
        # 推送
        print("🚀 推送到GitHub...")
        success, output = self.run_command("git push origin main")
        if not success:
            return False
        
        return True
    
    def cleanup(self):
        """
        清理临时文件
        """
        if os.path.exists(self.local_repo_path):
            try:
                shutil.rmtree(self.local_repo_path)
                print("🧹 清理临时文件...")
            except Exception as e:
                print(f"⚠️  清理临时文件时出错: {e}")
    
    def run(self):
        """
        执行完整的自动推送流程
        """
        print("=" * 50)
        print("🚀 开始GitHub自动推送流程")
        print("=" * 50)
        
        try:
            # 1. 克隆或拉取仓库
            if not self.clone_or_pull_repo():
                return False
            
            # 2. 准备网站文件
            if not self.prepare_website_files():
                return False
            
            # 3. 提交并推送
            if not self.commit_and_push():
                return False
            
            # 4. 显示成功信息
            print("=" * 50)
            print("🎉 GitHub自动推送成功完成！")
            print(f"🌐 网站地址: https://{self.config['github_username']}.github.io/")
            print(f"📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ 自动推送失败: {e}")
            return False
        
        finally:
            # 5. 清理
            self.cleanup()

def main():
    """
    主函数
    """
    # 检查必要文件
    required_files = [
        'github_config.json',
        'news_website_template.html', 
        'website_data/news-data.json'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    # 执行自动推送
    pusher = GitHubAutoPush()
    success = pusher.run()
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)