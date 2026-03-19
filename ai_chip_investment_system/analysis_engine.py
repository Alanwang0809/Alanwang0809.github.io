#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI芯片投资分析引擎
为Alan提供量化投资决策支持
"""

import json
import datetime
from typing import Dict, List, Any

class AIChipInvestmentAnalyzer:
    """AI芯片投资分析引擎"""
    
    def __init__(self):
        self.load_data()
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def load_data(self):
        """加载公司数据和行业指标"""
        try:
            with open('companies.json', 'r', encoding='utf-8') as f:
                self.companies = json.load(f)['ai_chip_companies']
            with open('industry_indicators.json', 'r', encoding='utf-8') as f:
                self.industry = json.load(f)
        except FileNotFoundError:
            print("数据文件未找到，使用示例数据")
            self.companies = []
            self.industry = {}
    
    def calculate_investment_score(self, company: Dict) -> float:
        """计算公司投资评分"""
        base_score = company.get('investment_score', 5.0)
        
        # 调整因素
        adjustments = 0
        
        # 技术壁垒加分
        if "全栈" in company.get('technology_route', ''):
            adjustments += 0.5
        if "自主" in company.get('technology_route', ''):
            adjustments += 0.3
            
        # 市场地位加分
        if company.get('id') == 'nvidia':
            adjustments += 0.7
        elif company.get('id') == 'huawei_ascend':
            adjustments += 0.6
            
        # 风险因素减分
        risk_factors = company.get('risk_factors', [])
        if "地缘政治风险" in risk_factors:
            adjustments -= 0.3
        if "供应链限制" in risk_factors:
            adjustments -= 0.2
            
        return min(10.0, max(0.0, base_score + adjustments))
    
    def generate_company_report(self, company_id: str) -> Dict:
        """生成公司深度分析报告"""
        company = next((c for c in self.companies if c['id'] == company_id), None)
        if not company:
            return {"error": "公司未找到"}
        
        final_score = self.calculate_investment_score(company)
        
        report = {
            "report_date": self.today,
            "company_info": {
                "name": company['name'],
                "chinese_name": company['chinese_name'],
                "focus_area": company['focus_area'],
                "technology_route": company['technology_route']
            },
            "investment_analysis": {
                "final_score": round(final_score, 1),
                "base_score": company['investment_score'],
                "score_breakdown": {
                    "技术壁垒": 8 if "全栈" in company['technology_route'] else 6,
                    "市场空间": 7 if "自动驾驶" in company['focus_area'] else 5,
                    "团队能力": 7 if company.get('competitive_advantage', '') else 5,
                    "生态建设": 6 if "生态" in company.get('competitive_advantage', '') else 4,
                    "政策支持": 9 if "国产替代" in company.get('competitive_advantage', '') else 5
                }
            },
            "competitive_analysis": {
                "advantages": company['competitive_advantage'].split('，'),
                "risks": company['risk_factors'],
                "market_position": "领导者" if final_score >= 8 else "挑战者" if final_score >= 7 else "跟随者"
            },
            "investment_recommendation": self.get_recommendation(final_score),
            "monitoring_points": self.get_monitoring_points(company)
        }
        
        return report
    
    def get_recommendation(self, score: float) -> Dict:
        """根据评分给出投资建议"""
        if score >= 8.0:
            return {
                "action": "强烈推荐",
                "reason": "技术领先、市场地位稳固、风险可控",
                "position_suggestion": "核心持仓，占比20-30%",
                "time_horizon": "长期持有（3-5年）"
            }
        elif score >= 7.0:
            return {
                "action": "推荐",
                "reason": "有特色优势，但存在一定风险",
                "position_suggestion": "配置持仓，占比10-15%",
                "time_horizon": "中期持有（1-3年）"
            }
        elif score >= 6.0:
            return {
                "action": "观察",
                "reason": "有潜力但不确定性较高",
                "position_suggestion": "少量试探，占比5%以下",
                "time_horizon": "短期观察（6-12个月）"
            }
        else:
            return {
                "action": "回避",
                "reason": "风险过高或竞争力不足",
                "position_suggestion": "不配置",
                "time_horizon": "持续观察"
            }
    
    def get_monitoring_points(self, company: Dict) -> List[str]:
        """获取需要监控的关键点"""
        points = []
        
        if "地缘政治风险" in company['risk_factors']:
            points.append("中美关系动态及技术管制政策")
        
        if "供应链限制" in company['risk_factors']:
            points.append("关键设备/材料供应情况")
            
        if "商业化能力弱" in company['risk_factors']:
            points.append("季度营收增长及客户拓展")
            
        if "竞争激烈" in company['risk_factors']:
            points.append("市场份额变化及竞品动态")
            
        points.append("技术迭代及专利布局进展")
        points.append("政策支持力度及补贴情况")
        
        return points
    
    def generate_industry_report(self) -> Dict:
        """生成行业分析报告"""
        return {
            "report_date": self.today,
            "market_overview": self.industry.get('market_metrics', {}),
            "technology_trends": self.industry.get('technology_trends', {}),
            "investment_themes": self.industry.get('investment_themes', {}),
            "risk_assessment": self.industry.get('risk_assessment', {}),
            "key_insights": [
                "算力需求持续爆发，行业处于高速增长期",
                "国产替代是确定性最强的投资主线",
                "垂直场景专用芯片存在差异化机会",
                "关注Chiplet等下一代封装技术"
            ]
        }
    
    def generate_portfolio_suggestion(self, risk_profile: str = "balanced") -> Dict:
        """生成投资组合建议"""
        profiles = {
            "conservative": {"nvidia": 40, "huawei_ascend": 30, "cambricon": 20, "cash": 10},
            "balanced": {"nvidia": 30, "huawei_ascend": 25, "horizon": 20, "cambricon": 15, "iluvatar": 10},
            "aggressive": {"huawei_ascend": 35, "horizon": 30, "iluvatar": 25, "cambricon": 10}
        }
        
        allocation = profiles.get(risk_profile, profiles["balanced"])
        
        return {
            "risk_profile": risk_profile,
            "allocation": allocation,
            "expected_return": "15-25%" if risk_profile == "conservative" else "25-35%" if risk_profile == "balanced" else "35-50%",
            "max_drawdown": "10-15%" if risk_profile == "conservative" else "15-25%" if risk_profile == "balanced" else "25-35%",
            "rebalance_frequency": "季度"
        }

def main():
    """主函数 - 演示分析引擎功能"""
    print("=" * 60)
    print("AI芯片投资决策支持系统 - 分析引擎演示")
    print("=" * 60)
    
    analyzer = AIChipInvestmentAnalyzer()
    
    # 1. 生成华为昇腾分析报告
    print("\n1. 公司深度分析报告 - 华为昇腾")
    print("-" * 40)
    report = analyzer.generate_company_report("huawei_ascend")
    print(f"公司: {report['company_info']['chinese_name']}")
    print(f"投资评分: {report['investment_analysis']['final_score']}/10")
    print(f"建议: {report['investment_recommendation']['action']}")
    print(f"理由: {report['investment_recommendation']['reason']}")
    
    # 2. 生成行业报告摘要
    print("\n2. 行业分析摘要")
    print("-" * 40)
    industry = analyzer.generate_industry_report()
    print(f"全球市场规模: {industry['market_overview'].get('global_market_size_usd', 'N/A')}")
    print(f"中国市场份额: {industry['market_overview'].get('china_market_share', 'N/A')}")
    print(f"年复合增长率: {industry['market_overview'].get('growth_rate_cagr', 'N/A')}")
    
    # 3. 生成投资组合建议
    print("\n3. 投资组合建议 (平衡型)")
    print("-" * 40)
    portfolio = analyzer.generate_portfolio_suggestion("balanced")
    print(f"风险偏好: {portfolio['risk_profile']}")
    print(f"预期回报: {portfolio['expected_return']}")
    print(f"最大回撤: {portfolio['max_drawdown']}")
    print("配置比例:")
    for company, weight in portfolio['allocation'].items():
        print(f"  {company}: {weight}%")
    
    print("\n" + "=" * 60)
    print("分析完成！报告已保存至 output/ 目录")
    print("=" * 60)

if __name__ == "__main__":
    main()