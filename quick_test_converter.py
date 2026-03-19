#!/usr/bin/env python3
"""
快速测试转换脚本
"""

import json
import os
from datetime import datetime

def convert_test_news():
    """转换测试新闻为JSON格式"""
    
    # 测试新闻数据
    test_news = [
        {
            "id": 1,
            "order": 0,
            "title": "新闻网站自动化系统测试成功",
            "category": "tech",
            "time": "2026-03-18 21:30",
            "subject": "小龙虾AI",
            "event": "新闻网站自动化系统测试运行成功。系统包含：1.GitHub自动推送 2.新闻数据转换 3.网站模板渲染 4.定时任务管理。测试验证了完整的工作流程。",
            "impact": [
                "从明天开始，网站将每天08:30自动更新",
                "无需手动操作，全自动化运行",
                "任何人都可以访问 https://alanwang0809.github.io/ 查看最新新闻",
                "为Alan节省每日新闻整理时间"
            ],
            "link": "https://github.com/alanwang0809/alanwang0809.github.io"
        },
        {
            "id": 2,
            "order": 1,
            "title": "AI大模型竞争进入新阶段",
            "category": "ai",
            "time": "2026-03-18",
            "subject": "全球AI公司",
            "event": "随着GPT-5、文心4.0、GLM-5等新一代大模型的发布，AI竞争进入新阶段。各公司不仅在模型规模上竞争，更在应用场景、商业化落地方面展开激烈角逐。",
            "impact": [
                "AI应用加速普及，各行各业都在探索AI转型",
                "算力需求持续增长，带动芯片产业发展",
                "AI人才竞争加剧，相关岗位薪资上涨",
                "投资机会集中在AI基础设施和行业解决方案"
            ],
            "link": "https://example.com/ai-competition"
        },
        {
            "id": 3,
            "order": 2,
            "title": "新能源汽车快充技术突破",
            "category": "energy",
            "time": "2026-03-18",
            "subject": "新能源汽车行业",
            "event": "多家车企宣布快充技术取得突破，充电时间从1小时缩短到15分钟。同时，充电网络建设加速，高速公路服务区充电桩覆盖率超过90%。",
            "impact": [
                "缓解电动汽车续航焦虑，促进销量增长",
                "充电基础设施投资机会增加",
                "电池技术进步推动成本下降",
                "绿色出行接受度进一步提高"
            ],
            "link": "https://example.com/ev-charging"
        },
        {
            "id": 4,
            "order": 3,
            "title": "商业航天发射成本大幅降低",
            "category": "space",
            "time": "2026-03-18",
            "subject": "商业航天公司",
            "event": "SpaceX、蓝色起源等公司通过火箭回收技术，将发射成本降低到原来的十分之一。中国商业航天公司也在积极跟进，计划今年进行多次商业发射。",
            "impact": [
                "卫星发射需求大幅增加",
                "太空旅游商业化进程加速",
                "空间资源开发成为可能",
                "带动相关产业链发展"
            ],
            "link": "https://example.com/space-launch"
        }
    ]
    
    # 创建输出数据
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'source': '晚间测试新闻',
            'total_news': len(test_news),
            'categories': list(set([news['category'] for news in test_news])),
            'purpose': '新闻网站自动化系统测试 - 2026-03-18 21:30'
        },
        'news': test_news
    }
    
    # 确保目录存在
    os.makedirs('website_data', exist_ok=True)
    
    # 保存JSON文件
    output_file = 'website_data/news-data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试新闻数据已生成: {output_file}")
    print(f"📊 包含 {len(test_news)} 条新闻")
    
    # 显示分类统计
    categories = {}
    for news in test_news:
        cat = news['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("📈 分类统计:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} 条")
    
    return True

if __name__ == "__main__":
    convert_test_news()