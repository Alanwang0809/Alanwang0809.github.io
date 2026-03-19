import json
import re
import os
from datetime import datetime
from pathlib import Path

def parse_news_markdown(markdown_content):
    news_items = []
    current_news = {}
    
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('### '):
            if current_news:
                news_items.append(current_news)
                current_news = {}
            
            title = line[4:].strip()
            current_news['title'] = title
            current_news['category'] = 'general'
            
        elif line.startswith('**时间**：'):
            time_str = line.replace('**时间**：', '').strip()
            current_news['time'] = time_str
            
        elif line.startswith('**主体**：'):
            subject = line.replace('**主体**：', '').strip()
            current_news['subject'] = subject
            
        elif line.startswith('**事件**：'):
            event = line.replace('**事件**：', '').strip()
            current_news['event'] = event
            
        elif line.startswith('**影响**：'):
            current_news['impact'] = []
            
        elif line.startswith('- ') and 'impact' in current_news:
            impact_item = line[2:].strip()
            current_news['impact'].append(impact_item)
            
        elif line.startswith('**原文链接**：'):
            link = line.replace('**原文链接**：', '').strip()
            current_news['link'] = link
            
        elif line == '' and current_news:
            if 'title' in current_news:
                current_news.setdefault('time', '')
                current_news.setdefault('subject', '')
                current_news.setdefault('event', '')
                current_news.setdefault('impact', [])
                current_news.setdefault('link', '')
                current_news.setdefault('category', 'general')
                
                news_items.append(current_news)
                current_news = {}
    
    if current_news and 'title' in current_news:
        current_news.setdefault('time', '')
        current_news.setdefault('subject', '')
        current_news.setdefault('event', '')
        current_news.setdefault('impact', [])
        current_news.setdefault('link', '')
        current_news.setdefault('category', 'general')
        
        news_items.append(current_news)
    
    return news_items

# 读取测试文件
with open('news_collection/2026-03-18_测试新闻.md', 'r', encoding='utf-8') as f:
    content = f.read()

news_items = parse_news_markdown(content)

# 添加ID和分类
for i, news in enumerate(news_items):
    news['id'] = i + 1
    news['order'] = i
    
    # 简单分类
    title_lower = news['title'].lower()
    if 'ai' in title_lower or '人工智能' in title_lower:
        news['category'] = 'ai'
    elif '新能源' in title_lower or '汽车' in title_lower:
        news['category'] = 'energy'
    elif '航天' in title_lower or '太空' in title_lower:
        news['category'] = 'space'

# 创建输出数据
output_data = {
    'metadata': {
        'generated_at': datetime.now().isoformat(),
        'source_file': '2026-03-18_测试新闻.md',
        'total_news': len(news_items),
        'categories': list(set([news['category'] for news in news_items]))
    },
    'news': news_items
}

# 保存JSON
os.makedirs('website_data', exist_ok=True)
with open('website_data/news-data.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"✅ 成功转换 {len(news_items)} 条新闻")
print("📊 分类统计:")
categories = {}
for news in news_items:
    cat = news['category']
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in categories.items():
    print(f"  {cat}: {count} 条")

print("📁 文件已保存: website_data/news-data.json")