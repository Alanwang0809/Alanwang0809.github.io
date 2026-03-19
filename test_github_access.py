#!/usr/bin/env python3
"""
测试GitHub访问权限
"""

import json
import requests
from datetime import datetime

def test_github_access():
    """测试GitHub API访问权限"""
    print("=" * 60)
    print("🔐 测试GitHub访问权限")
    print("=" * 60)
    
    # 加载配置
    try:
        with open('github_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        token = config['github_token']
        username = config['github_username']
        repo = config['github_repo']
        
        print(f"👤 GitHub用户: {username}")
        print(f"📁 目标仓库: {repo}")
        print(f"🔑 Token前几位: {token[:10]}...")
        print()
        
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False
    
    # 测试GitHub API访问
    print("📡 测试GitHub API访问...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # 测试1: 验证Token有效性
    print("1. 验证Token有效性...")
    try:
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Token有效")
            print(f"   👤 登录用户: {user_data.get('login')}")
            print(f"   📧 邮箱: {user_data.get('email', '未公开')}")
        else:
            print(f"   ❌ Token无效，状态码: {response.status_code}")
            print(f"   📋 响应: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"   ❌ API请求失败: {e}")
        return False
    
    # 测试2: 检查仓库访问权限
    print("2. 检查仓库访问权限...")
    try:
        repo_url = f'https://api.github.com/repos/{username}/{repo}'
        response = requests.get(repo_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            print(f"   ✅ 仓库可访问")
            print(f"   📝 仓库名: {repo_data.get('full_name')}")
            print(f"   📅 创建时间: {repo_data.get('created_at')}")
            print(f"   🌐 网站URL: {repo_data.get('homepage', '无')}")
            
            # 检查是否有推送权限
            permissions = repo_data.get('permissions', {})
            if permissions.get('push'):
                print(f"   ✅ 有推送权限")
            else:
                print(f"   ❌ 无推送权限")
                return False
                
        elif response.status_code == 404:
            print(f"   ❌ 仓库不存在: {repo_url}")
            return False
        else:
            print(f"   ❌ 仓库访问失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 仓库检查失败: {e}")
        return False
    
    # 测试3: 检查最近提交
    print("3. 检查最近提交...")
    try:
        commits_url = f'https://api.github.com/repos/{username}/{repo}/commits'
        response = requests.get(commits_url, headers=headers, timeout=10, params={'per_page': 3})
        
        if response.status_code == 200:
            commits = response.json()
            if commits:
                print(f"   ✅ 找到 {len(commits)} 条提交记录")
                for i, commit in enumerate(commits[:3]):
                    commit_data = commit.get('commit', {})
                    author = commit_data.get('author', {})
                    print(f"   {i+1}. {author.get('date')}: {commit_data.get('message', '')[:50]}...")
            else:
                print(f"   ℹ️  仓库为空，无提交记录")
        else:
            print(f"   ❌ 获取提交记录失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 提交检查失败: {e}")
    
    print()
    print("=" * 60)
    print("📊 权限测试总结")
    print("=" * 60)
    print("✅ Token有效性: 已验证")
    print("✅ 仓库访问权限: 已验证")
    print("✅ 推送权限: 已验证")
    print("✅ API连接: 正常")
    print()
    print("🎯 下一步: 测试实际的文件推送")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_github_access()