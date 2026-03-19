#!/usr/bin/env python3
"""
快速GitHub推送测试
"""

import json
import subprocess
import os
import shutil
from datetime import datetime
from pathlib import Path

def load_config():
    """加载GitHub配置"""
    with open('github_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def run_command(command, cwd=None):
    """运行shell命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_github_push():
    """测试GitHub推送"""
    print("🚀 开始GitHub推送测试")
    print("=" * 50)
    
    # 加载配置
    config = load_config()
    token = config['github_token']
    username = config['github_username']
    repo = config['github_repo']
    
    repo_url = f"https://{token}@github.com/{username}/{repo}.git"
    local_path = "test_repo_temp"
    
    try:
        # 1. 克隆仓库
        print("📥 克隆GitHub仓库...")
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        
        success, stdout, stderr = run_command(f'git clone {repo_url} {local_path}')
        if not success:
            print(f"❌ 克隆失败: {stderr}")
            return False
        
        # 2. 准备网站文件
        print("📁 准备网站文件...")
        
        # 复制网站模板
        shutil.copy2('news_website_template.html', f'{local_path}/index.html')
        
        # 复制新闻数据
        shutil.copy2('website_data/news-data.json', f'{local_path}/news-data.json')
        
        # 创建README
        readme_content = f"""# 每日新闻网站 - 测试版本

这是一个自动更新的每日新闻网站测试版本。

## 测试信息
- **测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **测试目的**: 验证新闻网站自动化系统
- **测试状态**: 成功 ✅

## 新闻内容
本次测试包含4条新闻，涵盖：
- 🦞 系统测试新闻
- 🤖 AI人工智能
- 🔋 新能源
- 🚀 商业航天

## 自动化系统
从明天（2026-03-19）开始，网站将：
- 每天08:30自动更新
- 无需手动操作
- 包含当日最新新闻

## 访问地址
https://{username}.github.io/

---
*测试由小龙虾AI执行* 🦞
"""
        
        with open(f'{local_path}/README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 3. 提交更改
        print("📝 提交更改...")
        os.chdir(local_path)
        
        run_command('git add .')
        
        commit_msg = f"测试更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 新闻网站自动化系统测试"
        success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"')
        
        if not success and "nothing to commit" not in stderr:
            print(f"❌ 提交失败: {stderr}")
            os.chdir('..')
            return False
        
        # 4. 推送更改
        print("🚀 推送到GitHub...")
        success, stdout, stderr = run_command('git push origin main')
        if not success:
            print(f"❌ 推送失败: {stderr}")
            os.chdir('..')
            return False
        
        os.chdir('..')
        
        # 5. 清理
        shutil.rmtree(local_path)
        
        print("=" * 50)
        print("🎉 GitHub推送测试成功完成！")
        print(f"🌐 网站地址: https://{username}.github.io/")
        print(f"🕗 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        # 清理
        if os.path.exists(local_path):
            shutil.rmtree(local_path, ignore_errors=True)
        return False

if __name__ == "__main__":
    success = test_github_push()
    if success:
        print("\n✅ 测试完成！请访问 https://alanwang0809.github.io/ 查看更新")
    else:
        print("\n❌ 测试失败，请检查配置")
    exit(0 if success else 1)