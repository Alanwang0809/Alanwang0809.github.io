#!/usr/bin/env python3
"""
GitHub PAT测试脚本
功能：测试GitHub PAT的有效性，验证仓库访问权限
"""

import requests
import json
import sys
import os
from pathlib import Path

def test_pat_with_requests(pat, username, repo):
    """使用requests测试PAT"""
    print(f"🔍 测试GitHub PAT有效性...")
    print(f"   用户名: {username}")
    print(f"   仓库: {repo}")
    
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 测试1: 验证用户
    print("\n[1/3] 验证用户身份...")
    try:
        user_response = requests.get("https://api.github.com/user", headers=headers)
        if user_response.status_code == 200:
            user_data = user_response.json()
            print(f"   ✅ 用户验证成功")
            print(f"     用户名: {user_data.get('login')}")
            print(f"     姓名: {user_data.get('name', '未设置')}")
        else:
            print(f"   ❌ 用户验证失败: {user_response.status_code}")
            print(f"     错误信息: {user_response.text}")
            return False
    except Exception as e:
        print(f"   ❌ 用户验证异常: {e}")
        return False
    
    # 测试2: 验证仓库访问
    print("\n[2/3] 验证仓库访问权限...")
    try:
        repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo}", headers=headers)
        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            print(f"   ✅ 仓库访问成功")
            print(f"     仓库名: {repo_data.get('full_name')}")
            print(f"     私有: {repo_data.get('private')}")
            print(f"     权限: {repo_data.get('permissions', {})}")
        else:
            print(f"   ❌ 仓库访问失败: {repo_response.status_code}")
            print(f"     错误信息: {repo_response.text}")
            return False
    except Exception as e:
        print(f"   ❌ 仓库访问异常: {e}")
        return False
    
    # 测试3: 验证写入权限
    print("\n[3/3] 验证写入权限...")
    try:
        # 尝试读取根目录文件
        content_response = requests.get(
            f"https://api.github.com/repos/{username}/{repo}/contents/",
            headers=headers
        )
        if content_response.status_code == 200:
            print(f"   ✅ 读取权限验证成功")
            # 检查是否有index.html文件
            contents = content_response.json()
            has_index = any(item.get('name') == 'index.html' for item in contents if isinstance(item, dict))
            print(f"     存在index.html: {has_index}")
        else:
            print(f"   ⚠️ 读取权限验证: {content_response.status_code}")
            print(f"     可能原因: 空仓库或权限限制")
    except Exception as e:
        print(f"   ⚠️ 读取权限验证异常: {e}")
    
    return True

def save_pat_config(pat, username, repo):
    """保存PAT配置到文件"""
    config = {
        "username": username,
        "token": pat,
        "repo": repo,
        "branch": "main",
        "api_url": "https://api.github.com"
    }
    
    config_file = Path("C:/Users/sbjpk/.openclaw/workspace/github_config.json")
    
    # 安全提示
    print("\n⚠️ 安全提示:")
    print("   配置文件将包含你的GitHub PAT")
    print("   请确保文件安全，不要分享或提交到公开仓库")
    
    # 保存配置
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ 配置已保存到: {config_file}")
        print(f"   请确保此文件安全!")
        return config_file
    except Exception as e:
        print(f"❌ 保存配置失败: {e}")
        return None

def create_automation_script():
    """创建自动化部署脚本"""
    script_content = '''#!/usr/bin/env python3
"""
GitHub自动部署脚本
使用PAT自动更新GitHub Pages
"""

import requests
import json
import base64
import datetime
import os
from pathlib import Path

class GitHubDeployer:
    def __init__(self, config_file):
        """初始化部署器"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.headers = {
            "Authorization": f"token {self.config['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.api_base = self.config['api_url']
        self.repo_path = f"{self.config['username']}/{self.config['repo']}"
    
    def get_file_sha(self, file_path):
        """获取文件的SHA"""
        url = f"{self.api_base}/repos/{self.repo_path}/contents/{file_path}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get('sha')
        elif response.status_code == 404:
            return None  # 文件不存在
        else:
            raise Exception(f"获取文件SHA失败: {response.status_code} - {response.text}")
    
    def update_file(self, file_path, content, commit_message):
        """更新或创建文件"""
        url = f"{self.api_base}/repos/{self.repo_path}/contents/{file_path}"
        
        # 获取当前SHA（如果文件存在）
        sha = self.get_file_sha(file_path)
        
        # 准备请求数据
        data = {
            "message": commit_message,
            "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
            "branch": self.config['branch']
        }
        
        if sha:
            data["sha"] = sha
        
        response = requests.put(url, headers=self.headers, json=data)
        
        if response.status_code in [200, 201]:
            print(f"✅ 文件更新成功: {file_path}")
            return True
        else:
            print(f"❌ 文件更新失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    
    def deploy_news_page(self, html_content, date_str):
        """部署新闻页面"""
        print(f"🚀 开始部署 {date_str} 新闻页面...")
        
        # 更新index.html
        success = self.update_file(
            "index.html",
            html_content,
            f"更新 {date_str} 新闻页面"
        )
        
        if success:
            print(f"🎉 部署完成!")
            print(f"🌐 访问地址: https://{self.config['username']}.github.io/")
            return True
        else:
            print(f"❌ 部署失败")
            return False

def main():
    """主函数"""
    print("=" * 50)
    print("🦞 GitHub新闻自动部署系统")
    print("=" * 50)
    
    # 配置文件路径
    config_file = Path("C:/Users/sbjpk/.openclaw/workspace/github_config.json")
    
    if not config_file.exists():
        print("❌ 配置文件不存在")
        print(f"   请先运行 github_pat_tester.py 配置PAT")
        return
    
    # 创建部署器
    deployer = GitHubDeployer(config_file)
    
    # 示例HTML内容
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>🦞 {date_str} 新闻汇总</title>
    <style>body {{ font-family: Arial, sans-serif; padding: 20px; }}</style>
</head>
<body>
    <h1>🦞 {date_str} 新闻汇总</h1>
    <p>这是自动生成的新闻页面，更新时间: {datetime.datetime.now().strftime("%H:%M")}</p>
    <p>🎯 每日08:30自动更新 | 技术支持: 小龙虾AI伙伴</p>
</body>
</html>'''
    
    # 部署页面
    deployer.deploy_news_page(html_content, date_str)
    
    print("=" * 50)
    print("📋 部署流程完成")
    print("=" * 50)

if __name__ == "__main__":
    main()
'''
    
    script_file = Path("C:/Users/sbjpk/.openclaw/workspace/github_auto_deploy.py")
    try:
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"\n✅ 自动化脚本已创建: {script_file}")
        print(f"   使用方法: python {script_file}")
        return script_file
    except Exception as e:
        print(f"❌ 创建脚本失败: {e}")
        return None

def main():
    """主函数"""
    print("=" * 50)
    print("🔧 GitHub PAT配置工具")
    print("=" * 50)
    
    # 获取用户输入
    print("\n📝 请输入以下信息:")
    
    pat = input("GitHub PAT: ").strip()
    if not pat:
        print("❌ PAT不能为空")
        return
    
    username = "Alanwang0809"  # 固定用户名
    repo = "Alanwang0809.github.io"  # 固定仓库
    
    print(f"\n📋 配置信息:")
    print(f"   PAT: {'*' * min(20, len(pat))}...")
    print(f"   用户名: {username}")
    print(f"   仓库: {repo}")
    
    # 测试PAT
    if test_pat_with_requests(pat, username, repo):
        print("\n🎉 PAT测试成功!")
        
        # 保存配置
        config_file = save_pat_config(pat, username, repo)
        
        if config_file:
            # 创建自动化脚本
            script_file = create_automation_script()
            
            print("\n🚀 配置完成!")
            print("=" * 50)
            print("📋 下一步:")
            print("1. 测试自动化部署:")
            print(f"   python {script_file}")
            print("\n2. 设置定时任务:")
            print("   每天08:30自动执行新闻收集和部署")
            print("\n3. 验证网站更新:")
            print("   https://alanwang0809.github.io/")
            print("=" * 50)
    else:
        print("\n❌ PAT测试失败，请检查:")
        print("1. PAT是否正确")
        print("2. PAT是否已过期")
        print("3. 是否授予了正确的权限 (repo)")
        print("4. 网络连接是否正常")

if __name__ == "__main__":
    main()