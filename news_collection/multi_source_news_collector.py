#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多源新闻收集器 - 支持中文和英文新闻源
版本: 1.0
创建时间: 2026-03-16
作者: 小龙虾 🦞
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MultiSourceNewsCollector:
    """多源新闻收集器"""
    
    def __init__(self):
        self.news_sources = {
            # 中文新闻源
            'chinese': {
                'sina': {
                    'name': '新浪新闻',
                    'url': 'https://news.sina.com.cn',
                    'category': '综合',
                    'language': 'zh'
                },
                'caixin': {
                    'name': '财新网',
                    'url': 'https://www.caixin.com',
                    'category': '财经',
                    'language': 'zh'
                },
                'thepaper': {
                    'name': '澎湃新闻',
                    'url': 'https://www.thepaper.cn',
                    'category': '综合',
                    'language': 'zh'
                },
                '36kr': {
                    'name': '36氪',
                    'url': 'https://36kr.com',
                    'category': '科技',
                    'language': 'zh'
                },
                'huxiu': {
                    'name': '虎嗅',
                    'url': 'https://www.huxiu.com',
                    'category': '科技',
                    'language': 'zh'
                }
            },
            # 英文新闻源
            'english': {
                'bbc': {
                    'name': 'BBC News',
                    'url': 'https://www.bbc.com/news',
                    'category': '国际',
                    'language': 'en'
                },
                'reuters': {
                    'name': 'Reuters',
                    'url': 'https://www.reuters.com',
                    'category': '财经',
                    'language': 'en'
                },
                'bloomberg': {
                    'name': 'Bloomberg',
                    'url': 'https://www.bloomberg.com',
                    'category': '财经',
                    'language': 'en'
                },
                'ft': {
                    'name': 'Financial Times',
                    'url': 'https://www.ft.com',
                    'category': '财经',
                    'language': 'en'
                }
            }
        }
        
        # 用户兴趣关键词（根据Alan的投行工作定制）
        self.interest_keywords = [
            # AI相关
            'AI', 'artificial intelligence', 'machine learning', '大模型', '人工智能',
            # 新能源
            '新能源', 'new energy', 'electric vehicle', 'EV', 'battery', '储能',
            # 商业航天
            '商业航天', 'commercial space', 'satellite', 'rocket', 'SpaceX',
            # 金融经济
            'economy', 'finance', 'investment', 'stock', '市场', '经济',
            # 国际关系
            'China', 'US', 'trade', '外交', '国际关系'
        ]
        
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    
    def fetch_news_from_source(self, source_id: str, source_info: Dict) -> List[Dict]:
        """从单个新闻源获取新闻"""
        news_list = []
        
        try:
            logger.info(f"开始从 {source_info['name']} 获取新闻...")
            
            # 这里应该根据不同的新闻源实现具体的爬取逻辑
            # 由于时间关系，这里先返回模拟数据
            # 实际实现需要针对每个网站编写具体的解析逻辑
            
            if source_info['language'] == 'zh':
                # 中文新闻模拟数据
                news_list = self._get_chinese_mock_news(source_info)
            else:
                # 英文新闻模拟数据
                news_list = self._get_english_mock_news(source_info)
                
            logger.info(f"从 {source_info['name']} 获取到 {len(news_list)} 条新闻")
            
        except Exception as e:
            logger.error(f"从 {source_info['name']} 获取新闻失败: {e}")
            
        return news_list
    
    def _get_chinese_mock_news(self, source_info: Dict) -> List[Dict]:
        """获取中文模拟新闻（实际应该从网站爬取）"""
        mock_news = []
        
        # 根据不同的新闻源返回不同的模拟数据
        if source_info['name'] == '新浪新闻':
            mock_news = [
                {
                    'title': '中国商务部回应美国301调查',
                    'summary': '美国对包括中国在内的60个经济体发起301调查，中国商务部回应称此举"严重扰乱国际经贸秩序"',
                    'url': 'https://finance.sina.com.cn/jjxw/2026-03-16/doc-inhrcpie9922556.shtml',
                    'publish_time': '2026-03-16 10:30:00',
                    'source': '新浪新闻',
                    'category': '财经',
                    'language': 'zh'
                },
                {
                    'title': '全国卫星互联网标准化委员会成立',
                    'summary': '国家标准化管理委员会正式批准成立"全国卫星互联网系统与服务标准化技术委员会"',
                    'url': 'https://finance.sina.com.cn/stock/2026-03-16/doc-inhrcxwx8922497.shtml',
                    'publish_time': '2026-03-16 09:15:00',
                    'source': '新浪新闻',
                    'category': '科技',
                    'language': 'zh'
                }
            ]
        elif source_info['name'] == '财新网':
            mock_news = [
                {
                    'title': '央行继续实施适度宽松货币政策',
                    'summary': '中国人民银行召开货币政策委员会例会，决定继续实施好适度宽松的货币政策',
                    'url': 'https://economy.caixin.com/2026-03-16/101234567.html',
                    'publish_time': '2026-03-16 11:20:00',
                    'source': '财新网',
                    'category': '财经',
                    'language': 'zh'
                }
            ]
            
        return mock_news
    
    def _get_english_mock_news(self, source_info: Dict) -> List[Dict]:
        """获取英文模拟新闻（实际应该从网站爬取）"""
        mock_news = []
        
        if source_info['name'] == 'BBC News':
            mock_news = [
                {
                    'title': 'Middle East tensions rise over Strait of Hormuz',
                    'summary': 'Growing concerns about security in the Strait of Hormuz as tensions escalate in the Middle East',
                    'url': 'https://www.bbc.com/news/world-middle-east-12345678',
                    'publish_time': '2026-03-16 03:30:00',
                    'source': 'BBC News',
                    'category': 'International',
                    'language': 'en'
                },
                {
                    'title': 'AI regulation debate intensifies in Europe',
                    'summary': 'European Parliament discusses stricter AI regulations amid growing concerns about technology risks',
                    'url': 'https://www.bbc.com/news/technology-12345679',
                    'publish_time': '2026-03-16 05:45:00',
                    'source': 'BBC News',
                    'category': 'Technology',
                    'language': 'en'
                }
            ]
        elif source_info['name'] == 'Reuters':
            mock_news = [
                {
                    'title': 'Oil prices remain high amid supply concerns',
                    'summary': 'Crude oil prices hold near $90 a barrel as geopolitical tensions threaten supply',
                    'url': 'https://www.reuters.com/markets/commodities/oil-prices-remain-high-2026-03-16/',
                    'publish_time': '2026-03-16 04:15:00',
                    'source': 'Reuters',
                    'category': 'Commodities',
                    'language': 'en'
                }
            ]
            
        return mock_news
    
    def filter_by_interest(self, news_list: List[Dict]) -> List[Dict]:
        """根据兴趣关键词过滤新闻"""
        filtered_news = []
        
        for news in news_list:
            # 检查标题和摘要中是否包含兴趣关键词
            text_to_check = f"{news.get('title', '')} {news.get('summary', '')}".lower()
            
            for keyword in self.interest_keywords:
                if keyword.lower() in text_to_check:
                    filtered_news.append(news)
                    break  # 找到一个关键词就足够
        
        logger.info(f"兴趣过滤: 从 {len(news_list)} 条中筛选出 {len(filtered_news)} 条相关新闻")
        return filtered_news
    
    def translate_english_news(self, news_list: List[Dict]) -> List[Dict]:
        """为英文新闻添加中文摘要（模拟翻译）"""
        translated_news = []
        
        for news in news_list:
            if news['language'] == 'en':
                # 这里应该调用翻译API，现在先用模拟翻译
                news['chinese_summary'] = self._mock_translate(news['summary'])
                news['chinese_title'] = self._mock_translate(news['title'])
            else:
                news['chinese_summary'] = news['summary']
                news['chinese_title'] = news['title']
            
            translated_news.append(news)
        
        return translated_news
    
    def _mock_translate(self, text: str) -> str:
        """模拟翻译函数（实际应该调用翻译API）"""
        # 简单的关键词替换模拟翻译
        translation_map = {
            'Middle East': '中东',
            'Strait of Hormuz': '霍尔木兹海峡',
            'tensions': '紧张局势',
            'AI regulation': 'AI监管',
            'Europe': '欧洲',
            'Oil prices': '油价',
            'supply concerns': '供应担忧',
            'geopolitical tensions': '地缘政治紧张'
        }
        
        translated = text
        for eng, chi in translation_map.items():
            translated = translated.replace(eng, chi)
        
        return translated
    
    def format_news_for_output(self, news_list: List[Dict]) -> str:
        """将新闻格式化为标准输出格式"""
        output_lines = []
        
        # 按语言分类
        chinese_news = [n for n in news_list if n['language'] == 'zh']
        english_news = [n for n in news_list if n['language'] == 'en']
        
        # 添加标题
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_lines.append(f"# 📰 多源新闻汇总 - {current_time}")
        output_lines.append("")
        
        # 中文新闻部分
        if chinese_news:
            output_lines.append("## 🇨🇳 中文新闻")
            output_lines.append("")
            
            for i, news in enumerate(chinese_news[:10], 1):  # 最多10条
                output_lines.append(f"### {i}. {news['title']}")
                output_lines.append(f"**时间**：{news['publish_time']}")
                output_lines.append(f"**来源**：{news['source']}")
                output_lines.append(f"**分类**：{news['category']}")
                output_lines.append(f"**摘要**：{news['summary']}")
                output_lines.append(f"**原文链接**：{news['url']}")
                output_lines.append("")
        
        # 英文新闻部分
        if english_news:
            output_lines.append("## 🌍 英文新闻（附中文摘要）")
            output_lines.append("")
            
            for i, news in enumerate(english_news[:10], 1):  # 最多10条
                output_lines.append(f"### {i}. {news['title']}")
                output_lines.append(f"**时间**：{news['publish_time']}")
                output_lines.append(f"**来源**：{news['source']} ({news['language'].upper()})")
                output_lines.append(f"**分类**：{news['category']}")
                output_lines.append(f"**英文摘要**：{news['summary']}")
                output_lines.append(f"**中文摘要**：{news.get('chinese_summary', '暂无翻译')}")
                output_lines.append(f"**原文链接**：{news['url']}")
                output_lines.append("")
        
        # 统计信息
        output_lines.append("## 📊 统计信息")
        output_lines.append("")
        output_lines.append(f"- **总新闻数**：{len(news_list)} 条")
        output_lines.append(f"- **中文新闻**：{len(chinese_news)} 条")
        output_lines.append(f"- **英文新闻**：{len(english_news)} 条")
        output_lines.append(f"- **新闻源**：{len(set(n['source'] for n in news_list))} 个")
        output_lines.append(f"- **收集时间**：{current_time}")
        
        return "\n".join(output_lines)
    
    def collect_news(self, max_news_per_source: int = 5) -> Dict[str, Any]:
        """主收集函数"""
        all_news = []
        
        logger.info("开始多源新闻收集...")
        
        # 收集中文新闻
        for source_id, source_info in self.news_sources['chinese'].items():
            try:
                news = self.fetch_news_from_source(source_id, source_info)
                all_news.extend(news[:max_news_per_source])
                time.sleep(1)  # 礼貌延迟
            except Exception as e:
                logger.error(f"收集 {source_info['name']} 失败: {e}")
        
        # 收集英文新闻
        for source_id, source_info in self.news_sources['english'].items():
            try:
                news = self.fetch_news_from_source(source_id, source_info)
                all_news.extend(news[:max_news_per_source])
                time.sleep(1)  # 礼貌延迟
            except Exception as e:
                logger.error(f"收集 {source_info['name']} 失败: {e}")
        
        # 兴趣过滤
        filtered_news = self.filter_by_interest(all_news)
        
        # 翻译英文新闻
        translated_news = self.translate_english_news(filtered_news)
        
        # 按时间排序（最新的在前）
        sorted_news = sorted(
            translated_news,
            key=lambda x: x.get('publish_time', ''),
            reverse=True
        )
        
        # 格式化输出
        formatted_output = self.format_news_for_output(sorted_news)
        
        # 保存结果
        result = {
            'total_news': len(sorted_news),
            'chinese_news': len([n for n in sorted_news if n['language'] == 'zh']),
            'english_news': len([n for n in sorted_news if n['language'] == 'en']),
            'sources': list(set(n['source'] for n in sorted_news)),
            'formatted_output': formatted_output,
            'raw_news': sorted_news
        }
        
        logger.info(f"新闻收集完成: 总共 {result['total_news']} 条新闻")
        
        return result

def main():
    """主函数"""
    collector = MultiSourceNewsCollector()
    
    try:
        # 收集新闻
        result = collector.collect_news(max_news_per_source=3)
        
        # 保存到文件
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        output_file = f"news_collection/multi_source_news_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['formatted_output'])
        
        logger.info(f"新闻已保存到: {output_file}")
        
        # 打印统计信息
        print("\n" + "="*50)
        print("新闻收集统计:")
        print(f"总新闻数: {result['total_news']}")
        print(f"中文新闻: {result['chinese_news']}")
        print(f"英文新闻: {result['english_news']}")
        print(f"新闻源: {', '.join(result['sources'])}")
        print("="*50)
        
        return result
        
    except Exception as e:
        logger.error(f"新闻收集主程序失败: {e}")
        return None

if __name__ == "__main__":
    main()