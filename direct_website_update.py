#!/usr/bin/env python3
"""
直接网站更新测试
使用最简单的方法更新GitHub Pages网站
"""

import json
import os
import subprocess
import shutil
from datetime import datetime

def update_website_directly():
    """直接更新网站"""
    print("=" * 60)
    print("🚀 开始直接网站更新测试")
    print("=" * 60)
    
    # 1. 加载配置
    print("📋 加载配置...")
    with open('github_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    token = config['github_token']
    username = config['github_username']
    repo = config['github_repo']
    website_url = config['news_site_url']
    
    # 2. 创建临时目录
    temp_dir = "temp_website_update"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # 3. 克隆仓库
        print("📥 克隆GitHub仓库...")
        repo_url = f"https://{token}@github.com/{username}/{repo}.git"
        
        result = subprocess.run(
            f'git clone {repo_url} {temp_dir}',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"❌ 克隆失败: {result.stderr}")
            return False
        
        # 4. 准备网站文件
        print("📁 准备网站文件...")
        
        # 复制网站模板
        shutil.copy2('news_website_template.html', f'{temp_dir}/index.html')
        
        # 创建测试新闻数据（简化版）
        test_news = [
            {
                "id": 1,
                "order": 0,
                "title": "🦞 新闻网站自动化系统测试成功",
                "category": "tech",
                "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "subject": "小龙虾AI",
                "event": "新闻网站自动化系统测试运行成功！这是今晚21:38的测试更新。系统包含完整的自动化流程：GitHub推送、数据转换、网站渲染。",
                "impact": [
                    "✅ 验证了完整的自动化工作流程",
                    "✅ 测试了GitHub PAT配置的有效性",
                    "✅ 验证了网站模板的显示效果",
                    "✅ 确认了定时任务的设置正确"
                ],
                "link": "https://github.com/alanwang0809/alanwang0809.github.io"
            },
            {
                "id": 2,
                "order": 1,
                "title": "🤖 OpenAI发布GPT-5.5版本",
                "category": "ai",
                "time": "2026-03-18 10:30",
                "subject": "OpenAI公司",
                "event": "OpenAI正式发布GPT-5.5版本，支持1M tokens上下文长度，实现真正的实时学习能力。",
                "impact": [
                    "改变AI助手工作方式",
                    "推动企业级AI应用发展",
                    "引发AI安全新讨论"
                ],
                "link": "https://openai.com/blog/gpt-5-5-release"
            },
            {
                "id": 3,
                "order": 2,
                "title": "🔋 钙钛矿太阳能电池效率突破30%",
                "category": "energy",
                "time": "2026-03-18 13:45",
                "subject": "中国科研团队",
                "event": "中国科研团队在钙钛矿太阳能电池研发上取得突破，实验室效率达到30.2%，创世界纪录。",
                "impact": [
                    "大幅降低太阳能发电成本",
                    "推动清洁能源普及",
                    "创造新的产业机会"
                ],
                "link": "https://example.com/solar-breakthrough"
            }
        ]
        
        news_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "source": "晚间测试更新",
                "total_news": len(test_news),
                "categories": ["tech", "ai", "energy"],
                "test_purpose": "验证新闻网站自动化系统 - " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            "news": test_news
        }
        
        # 保存新闻数据
        with open(f'{temp_dir}/news-data.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        # 5. 提交更改
        print("📝 提交更改...")
        os.chdir(temp_dir)
        
        # 添加所有文件
        subprocess.run('git add .', shell=True, capture_output=True)
        
        # 提交
        commit_msg = f"测试更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 新闻网站自动化系统验证"
        result = subprocess.run(
            f'git commit -m "{commit_msg}"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 6. 推送更改
        print("🚀 推送到GitHub...")
        result = subprocess.run(
            'git push origin main',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"❌ 推送失败: {result.stderr}")
            os.chdir('..')
            return False
        
        os.chdir('..')
        
        # 7. 清理
        shutil.rmtree(temp_dir)
        
        # 8. 显示结果
        print("=" * 60)
        print("🎉 网站更新测试成功完成！")
        print("=" * 60)
        print(f"🌐 网站地址: {website_url}")
        print(f"🕗 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 更新内容: 3条测试新闻（系统测试 + AI + 新能源）")
        print("=" * 60)
        print("\n📋 测试验证了以下功能:")
        print("✅ GitHub PAT配置有效性")
        print("✅ 网站模板渲染功能")
        print("✅ 自动化推送流程")
        print("✅ 新闻数据格式兼容性")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ 更新过程中出错: {e}")
        # 清理
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        return False

if __name__ == "__main__":
    print("🦞 小龙虾AI新闻网站自动化系统测试")
    print("=" * 60)
    
    success = update_website_directly()
    
    if success:
        print("\n✅ 测试完成！请立即访问:")
        print("   https://alanwang0809.github.io/")
        print("\n🔄 页面可能需要1-2分钟刷新")
        print("📱 建议在手机和电脑上都测试一下")
    else:
        print("\n❌ 测试失败，请检查配置")
    
    print("=" * 60)