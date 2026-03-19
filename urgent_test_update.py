#!/usr/bin/env python3
"""
紧急测试更新 - 确保内容正确更新
"""

import json
import os
from datetime import datetime

def create_urgent_test_content():
    """创建紧急测试内容"""
    
    urgent_news = [
        {
            "id": 1,
            "order": 0,
            "title": "🦞【紧急测试】新闻网站自动化系统验证",
            "category": "test",
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "subject": "小龙虾AI紧急测试",
            "event": "这是2026年3月18日22:33的紧急测试更新。验证新闻网站自动化系统是否能正确更新内容。如果看到这条新闻，说明系统工作正常。",
            "impact": [
                "验证GitHub自动推送功能",
                "确认网站模板渲染正确",
                "测试新闻数据格式兼容性",
                "确保明天08:30自动更新能正常工作"
            ],
            "link": "https://github.com/alanwang0809/alanwang0809.github.io"
        },
        {
            "id": 2,
            "order": 1,
            "title": "🤖 AI大模型测试内容 - 系统验证",
            "category": "ai",
            "time": "2026-03-18 22:33",
            "subject": "测试AI公司",
            "event": "这是AI领域的测试内容，用于验证新闻分类和格式显示。如果看到这条新闻，说明分类系统工作正常。",
            "impact": [
                "验证AI新闻分类功能",
                "测试影响分析显示",
                "确认原文链接格式",
                "检查响应式设计适配"
            ],
            "link": "https://example.com/test-ai"
        },
        {
            "id": 3,
            "order": 2,
            "title": "🔋 新能源测试内容 - 系统验证",
            "category": "energy",
            "time": "2026-03-18 22:33",
            "subject": "测试新能源公司",
            "event": "这是新能源领域的测试内容，用于验证多分类新闻显示。如果看到这条新闻，说明网站能正确处理多个新闻类别。",
            "impact": [
                "验证新能源新闻分类",
                "测试多分类同时显示",
                "确认时间戳格式正确",
                "检查移动端适配效果"
            ],
            "link": "https://example.com/test-energy"
        }
    ]
    
    # 创建完整数据
    news_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source": "紧急测试更新",
            "total_news": len(urgent_news),
            "categories": ["test", "ai", "energy"],
            "test_purpose": "验证新闻网站自动化系统 - " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "user_feedback": "Alan反馈内容不正确，这是紧急修复测试"
        },
        "news": urgent_news
    }
    
    # 保存文件
    os.makedirs('website_data', exist_ok=True)
    with open('website_data/news-data.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 紧急测试内容已创建")
    print(f"📊 包含 {len(urgent_news)} 条测试新闻")
    print(f"🕗 生成时间: {datetime.now().strftime('%H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    print("🚨 紧急测试更新开始")
    print("=" * 50)
    create_urgent_test_content()
    print("=" * 50)
    print("📋 下一步: 需要手动运行GitHub推送")
    print("🌐 目标网站: https://alanwang0809.github.io/")
    print("=" * 50)