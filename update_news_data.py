#!/usr/bin/env python3
"""
更新新闻数据文件，将今日新闻添加到news-data.json
"""

import json
import os
from datetime import datetime

def update_news_data():
    # 读取今日新闻
    today_news_path = "news_collection/2026-03-19_news_for_web.json"
    
    if not os.path.exists(today_news_path):
        print(f"❌ 未找到今日新闻文件: {today_news_path}")
        return False
    
    with open(today_news_path, 'r', encoding='utf-8') as f:
        today_news = json.load(f)
    
    # 读取现有新闻数据
    news_data_path = "news-data.json"
    if not os.path.exists(news_data_path):
        print(f"❌ 未找到新闻数据文件: {news_data_path}")
        return False
    
    with open(news_data_path, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    # 更新元数据
    news_data['metadata']['generated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
    news_data['metadata']['source'] = "自动更新系统"
    news_data['metadata']['total_news'] = len(today_news['news'])
    news_data['metadata']['categories'] = today_news['categories']
    news_data['metadata']['version'] = "2.0"
    news_data['metadata']['next_update'] = "2026-03-20 08:30"
    news_data['metadata']['test_purpose'] = "正式自动更新 - 2026年3月19日"
    
    # 清空现有新闻，添加今日新闻
    news_data['news'] = []
    
    # 转换今日新闻格式
    category_map = {
        'AI科技': 'ai',
        '新能源': 'energy',
        '商业航天': 'space',
        '国际财经': 'international',
        '经济金融': 'finance'
    }
    
    for i, item in enumerate(today_news['news']):
        # 确定类别
        category = category_map.get(item['category'], 'general')
        
        # 创建新闻条目
        news_item = {
            'id': i + 1,
            'order': i,
            'title': item['title'],
            'category': category,
            'time': item['time'],
            'subject': item.get('source', '未指定'),
            'event': item['summary'],
            'impact': [
                f"来源: {item['source']}",
                f"类别: {item['category']}",
                f"发布时间: {item['time']}"
            ],
            'link': item['url']
        }
        news_data['news'].append(news_item)
    
    # 保存更新后的数据
    with open(news_data_path, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功更新新闻数据文件")
    print(f"📊 新闻总数: {len(news_data['news'])}")
    print(f"📁 类别: {', '.join(today_news['categories'])}")
    print(f"⏰ 更新时间: {news_data['metadata']['generated_at']}")
    
    return True

if __name__ == "__main__":
    if update_news_data():
        print("🎉 新闻数据更新完成！")
    else:
        print("❌ 新闻数据更新失败")