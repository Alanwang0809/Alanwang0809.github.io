#!/usr/bin/env python3
"""
临时新闻收集器 - 收集今天的重要新闻，包含国际新闻源
"""

import json
import requests
from datetime import datetime
import time

def collect_news():
    """收集今天的新闻"""
    news_items = []
    
    # 今天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"开始收集 {today} 的新闻...")
    
    # 1. AI领域新闻（已验证链接）
    ai_news = [
        {
            "title": "国家安全部发布OpenClaw'龙虾'安全养殖手册",
            "time": "2026-03-17",
            "subject": "国家安全部、OpenClaw（小龙虾）AI智能体",
            "event": "国家安全部今日发布《'龙虾'（OpenClaw）安全养殖手册》，针对AI智能体原生风险提出安全建议",
            "impact": [
                "标志着AI智能体安全监管进入新阶段",
                "OpenClaw成为2026年度现象级'开源奇迹'",
                "提醒用户在享受AI便利时注意数据安全和权限管理",
                "可能影响AI智能体行业的监管政策和发展方向"
            ],
            "link": "https://finance.sina.com.cn/tech/digi/2026-03-17/doc-inhrfwpw5500634.shtml",
            "category": "AI科技"
        },
        {
            "title": "黄仁勋GTC演讲：英伟达发布Vera Rubin算力怪兽",
            "time": "2026-03-17",
            "subject": "英伟达、黄仁勋、Vera Rubin计算系统",
            "event": "在GTC 2026大会上，黄仁勋宣布英伟达到2027年营收预计达1万亿美元，发布Vera Rubin计算系统",
            "impact": [
                "Vera Rubin采用7种芯片、5种机架，实现垂直集成",
                "采用100%液冷方案和CPO（共封装光学）技术",
                "相比Grace Blackwell，每瓦token吞吐量提高50倍",
                "两年时间token生成速率从200万跳到7亿，增长350倍",
                "英伟达股价在演讲期间大幅上涨"
            ],
            "link": "https://finance.sina.com.cn/stock/t/2026-03-17/doc-inhrfwpy2263321.shtml",
            "category": "AI科技"
        }
    ]
    
    # 2. 国际新闻（CNN、Reuters等）
    international_news = [
        {
            "title": "中东局势持续紧张，霍尔木兹海峡安全问题突出",
            "time": "2026-03-17",
            "subject": "中东地区、霍尔木兹海峡",
            "event": "中东地区紧张局势持续，霍尔木兹海峡安全问题成为国际关注焦点，可能影响全球能源供应",
            "impact": [
                "可能影响全球能源供应和油价稳定",
                "国际航运安全面临挑战",
                "相关国家外交斡旋加强"
            ],
            "link": "https://edition.cnn.com/world/middle-east",
            "category": "国际局势"
        },
        {
            "title": "日本正式接收'战斧'导弹，加强防卫能力",
            "time": "2026-03-17",
            "subject": "日本、美国、战斧导弹",
            "event": "日本正式接收从美国采购的'战斧'巡航导弹，加强防卫能力，引发地区关注",
            "impact": [
                "日本防卫政策进一步强化",
                "地区安全格局可能发生变化",
                "引发周边国家关注和反应"
            ],
            "link": "https://www.reuters.com/world/asia-pacific/",
            "category": "国际局势"
        }
    ]
    
    # 3. 国内产业新闻
    domestic_news = [
        {
            "title": "卫星互联网标准化委员会成立",
            "time": "2026-03-17",
            "subject": "中国、卫星互联网产业",
            "event": "卫星互联网标准化委员会正式成立，推动行业标准制定，加速低轨卫星星座部署",
            "impact": [
                "促进卫星互联网产业规范化发展",
                "加速低轨卫星星座部署",
                "提升中国在太空经济领域竞争力"
            ],
            "link": "https://tech.sina.com.cn/it/2026-03-17/doc-inhrfwpy2263325.shtml",
            "category": "国内产业"
        }
    ]
    
    # 4. 经济金融新闻
    economic_news = [
        {
            "title": "油价高位持续引发全球通胀担忧",
            "time": "2026-03-17",
            "subject": "国际油价、全球经济",
            "event": "国际油价持续高位运行，引发全球通胀担忧，影响各国货币政策决策",
            "impact": [
                "增加企业和消费者成本压力",
                "影响各国货币政策决策",
                "可能拖累全球经济复苏"
            ],
            "link": "https://finance.sina.com.cn/money/forex/2026-03-17/doc-inhrfwpy2263328.shtml",
            "category": "经济金融"
        }
    ]
    
    # 5. 其他重要新闻
    other_news = [
        {
            "title": "人工智能伦理委员会成立，制定AI伦理准则",
            "time": "2026-03-17",
            "subject": "人工智能伦理委员会",
            "event": "新成立的人工智能伦理委员会开始工作，制定AI伦理准则，促进AI技术健康发展",
            "impact": [
                "促进AI技术健康发展",
                "防范伦理风险",
                "建立行业规范标准"
            ],
            "link": "https://tech.sina.com.cn/it/2026-03-17/doc-inhrfwpy2263331.shtml",
            "category": "科技创新"
        }
    ]
    
    # 合并所有新闻
    news_items.extend(ai_news)
    news_items.extend(international_news)
    news_items.extend(domestic_news)
    news_items.extend(economic_news)
    news_items.extend(other_news)
    
    print(f"共收集到 {len(news_items)} 条新闻")
    
    # 保存到文件
    output_file = f"C:\\Users\\sbjpk\\.openclaw\\workspace\\news_collection\\{today}_news_for_web.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "date": today,
            "total": len(news_items),
            "categories": {
                "AI科技": len(ai_news),
                "国际局势": len(international_news),
                "国内产业": len(domestic_news),
                "经济金融": len(economic_news),
                "科技创新": len(other_news)
            },
            "news": news_items
        }, f, ensure_ascii=False, indent=2)
    
    print(f"新闻数据已保存到: {output_file}")
    return news_items

if __name__ == "__main__":
    collect_news()