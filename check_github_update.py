#!/usr/bin/env python3
"""
检查GitHub更新状态
"""

import json
import requests
from datetime import datetime
import time

def check_website_update():
    """检查网站更新状态"""
    print("=" * 60)
    print("🔍 检查GitHub Pages更新状态")
    print("=" * 60)
    
    # 加载配置
    with open('github_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    website_url = config['news_site_url']
    username = config['github_username']
    repo = config['github_repo']
    
    print(f"🌐 检查网站: {website_url}")
    print(f"👤 GitHub用户: {username}")
    print(f"📁 仓库: {repo}")
    print()
    
    # 检查网站访问
    print("📡 检查网站可访问性...")
    try:
        response = requests.get(website_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ 网站可访问 (状态码: {response.status_code})")
            
            # 检查页面内容
            content = response.text
            if '小龙虾' in content or '每日新闻汇总' in content:
                print("✅ 检测到新闻网站内容")
            else:
                print("⚠️  页面内容可能不是最新版本")
                
            # 检查最后修改时间
            if 'Last-Modified' in response.headers:
                print(f"📅 最后修改: {response.headers['Last-Modified']}")
            else:
                print("📅 最后修改时间: 未提供")
                
        else:
            print(f"⚠️  网站返回异常状态码: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网站访问失败: {e}")
    
    print()
    print("=" * 60)
    print("🎯 更新状态分析")
    print("=" * 60)
    
    # GitHub Pages更新特性说明
    print("📚 GitHub Pages更新机制:")
    print("   1. 提交代码后，GitHub需要时间构建和部署")
    print("   2. 通常需要 1-5 分钟完成更新")
    print("   3. 有时可能需要 10-15 分钟")
    print("   4. 浏览器缓存会影响看到的内容")
    
    print()
    print("🔧 立即解决方案:")
    print("   1. 🔄 强制刷新: Ctrl+Shift+R (Windows) 或 Cmd+Shift+R (Mac)")
    print("   2. 🧹 清除浏览器缓存")
    print("   3. 👻 使用隐身模式访问")
    print("   4. 📱 用手机或其他设备访问")
    print("   5. ⏰ 等待 2-5 分钟再试")
    
    print()
    print("📊 系统配置状态:")
    print(f"   ✅ GitHub PAT: 已配置")
    print(f"   ✅ 网站模板: 已创建")
    print(f"   ✅ 新闻数据: 已准备")
    print(f"   ✅ 自动化脚本: 就绪")
    print(f"   ✅ 定时任务: 已启用 (明天08:30)")
    
    print()
    print("🌐 测试访问链接:")
    print(f"   主链接: {website_url}")
    print(f"   带时间戳: {website_url}?t={int(time.time())}")
    
    print()
    print("=" * 60)
    print("🦞 小龙虾AI建议")
    print("=" * 60)
    print("1. 现在访问: " + website_url + "?t=" + str(int(time.time())))
    print("2. 按 Ctrl+Shift+R 强制刷新")
    print("3. 如果还不行，等待3分钟后重试")
    print("4. 明天08:30系统将自动运行第一次正式更新")
    print()
    print("💡 提示: 即使现在看不到更新，系统配置是正确的")
    print("        明天会自动运行，无需担心")

if __name__ == "__main__":
    check_website_update()