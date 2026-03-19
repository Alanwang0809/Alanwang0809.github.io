#!/usr/bin/env python3
"""
新闻数据转换脚本
将每日新闻Markdown文件转换为JSON格式，用于网站展示
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path

def parse_news_markdown(markdown_content):
    """
    解析Markdown格式的新闻内容，提取结构化数据
    """
    news_items = []
    current_news = {}
    
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 检测新闻标题（### 开头）
        if line.startswith('### '):
            if current_news:
                news_items.append(current_news)
                current_news = {}
            
            title = line[4:].strip()
            current_news['title'] = title
            
            # 从标题中提取分类
            current_news['category'] = extract_category(title)
            
        # 检测时间字段
        elif line.startswith('**时间**：'):
            time_str = line.replace('**时间**：', '').strip()
            current_news['time'] = time_str
            
        # 检测主体字段
        elif line.startswith('**主体**：'):
            subject = line.replace('**主体**：', '').strip()
            current_news['subject'] = subject
            
        # 检测事件字段
        elif line.startswith('**事件**：'):
            event = line.replace('**事件**：', '').strip()
            current_news['event'] = event
            
        # 检测影响字段
        elif line.startswith('**影响**：'):
            current_news['impact'] = []
            
        # 检测影响列表项
        elif line.startswith('- ') and 'impact' in current_news:
            impact_item = line[2:].strip()
            current_news['impact'].append(impact_item)
            
        # 检测链接字段
        elif line.startswith('**原文链接**：'):
            link = line.replace('**原文链接**：', '').strip()
            current_news['link'] = link
            
        # 检测空行，表示一条新闻结束
        elif line == '' and current_news:
            if 'title' in current_news:
                # 确保所有必要字段都存在
                current_news.setdefault('time', '')
                current_news.setdefault('subject', '')
                current_news.setdefault('event', '')
                current_news.setdefault('impact', [])
                current_news.setdefault('link', '')
                current_news.setdefault('category', 'general')
                
                news_items.append(current_news)
                current_news = {}
    
    # 添加最后一条新闻
    if current_news and 'title' in current_news:
        current_news.setdefault('time', '')
        current_news.setdefault('subject', '')
        current_news.setdefault('event', '')
        current_news.setdefault('impact', [])
        current_news.setdefault('link', '')
        current_news.setdefault('category', 'general')
        
        news_items.append(current_news)
    
    return news_items

def extract_category(title):
    """
    从新闻标题中提取分类
    """
    title_lower = title.lower()
    
    # AI相关关键词
    ai_keywords = ['ai', '人工智能', '大模型', '机器学习', '深度学习', 'chatgpt', 'gpt', '智谱', '腾讯混元', 'minimax']
    if any(keyword in title_lower for keyword in ai_keywords):
        return 'ai'
    
    # 新能源相关关键词
    energy_keywords = ['新能源', '电动车', '电动汽车', '电池', '充电', '光伏', '风电', '储能', '零跑', '宝马', '小牛', '蔚来']
    if any(keyword in title_lower for keyword in energy_keywords):
        return 'energy'
    
    # 商业航天相关关键词
    space_keywords = ['航天', '卫星', '火箭', '太空', 'spacex', '商业航天', '太空探索']
    if any(keyword in title_lower for keyword in space_keywords):
        return 'space'
    
    # 经济金融相关关键词
    economy_keywords = ['经济', '金融', '股市', '投资', '基金', '银行', '证券', '货币政策', '通胀']
    if any(keyword in title_lower for keyword in economy_keywords):
        return 'economy'
    
    # 科技相关关键词
    tech_keywords = ['科技', '技术', '互联网', '软件', '硬件', '芯片', '半导体', '5g', '6g', '物联网']
    if any(keyword in title_lower for keyword in tech_keywords):
        return 'tech'
    
    return 'general'

def convert_news_to_json(markdown_file, output_json_file):
    """
    将Markdown新闻文件转换为JSON格式
    """
    try:
        # 读取Markdown文件
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # 解析新闻
        news_items = parse_news_markdown(markdown_content)
        
        # 添加ID和排序
        for i, news in enumerate(news_items):
            news['id'] = i + 1
            news['order'] = i
        
        # 创建输出数据结构
        output_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'source_file': markdown_file,
                'total_news': len(news_items),
                'categories': list(set([news['category'] for news in news_items]))
            },
            'news': news_items
        }
        
        # 保存为JSON文件
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 成功转换 {len(news_items)} 条新闻到 {output_json_file}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return False

def create_news_data_json(news_markdown_dir, output_dir):
    """
    创建完整的新闻数据JSON文件
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找最新的新闻Markdown文件
    markdown_files = list(Path(news_markdown_dir).glob('*.md'))
    if not markdown_files:
        print(f"❌ 在 {news_markdown_dir} 中未找到Markdown文件")
        return False
    
    # 按日期排序，获取最新的文件
    latest_file = max(markdown_files, key=lambda x: x.stat().st_mtime)
    
    # 生成输出文件路径
    today = datetime.now().strftime('%Y-%m-%d')
    output_json = Path(output_dir) / 'news-data.json'
    
    # 转换新闻
    success = convert_news_to_json(str(latest_file), str(output_json))
    
    if success:
        print(f"📊 新闻统计:")
        with open(output_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            categories = {}
            for news in data['news']:
                cat = news['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in categories.items():
                print(f"  {cat}: {count} 条")
        
        return True
    else:
        return False

if __name__ == "__main__":
    # 配置路径
    NEWS_MARKDOWN_DIR = "news_collection"
    OUTPUT_DIR = "website_data"
    
    # 执行转换
    success = create_news_data_json(NEWS_MARKDOWN_DIR, OUTPUT_DIR)
    
    if success:
        print("🎉 新闻数据转换完成！")
    else:
        print("⚠️  新闻数据转换失败")
        exit(1)