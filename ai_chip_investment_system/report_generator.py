#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI芯片投资报告生成器
自动生成格式化的投资报告
"""

import json
import datetime
from analysis_engine import AIChipInvestmentAnalyzer

class ReportGenerator:
    """投资报告生成器"""
    
    def __init__(self):
        self.analyzer = AIChipInvestmentAnalyzer()
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.green_theme = {
            "primary": "#4CAF50",
            "dark": "#2E7D32",
            "light": "#81C784",
            "accent": "#A5D6A7"
        }
    
    def generate_daily_briefing(self) -> str:
        """生成每日简报"""
        industry = self.analyzer.generate_industry_report()
        
        briefing = f"""# 📊 AI芯片行业每日简报
**报告日期：{self.today}** | **生成：小龙虾投资分析系统**

---

## 🎯 今日要点

### 市场动态
- **全球市场规模**：{industry['market_overview'].get('global_market_size_usd', 'N/A')} (2026预测)
- **中国份额**：{industry['market_overview'].get('china_market_share', 'N/A')}
- **增长趋势**：年复合增长率 {industry['market_overview'].get('growth_rate_cagr', 'N/A')}

### 技术前沿
**当前主流**：{industry['technology_trends'].get('current_generation', 'N/A')}
**下一代技术**：{industry['technology_trends'].get('next_generation', 'N/A')}

### 投资主题
1. **国产替代** - EDA工具、IP核自主化
2. **垂直场景** - 自动驾驶、工业视觉专用芯片
3. **下一代封装** - Chiplet技术突破

---

## 📈 重点公司监控

"""
        
        # 添加公司摘要
        for company in self.analyzer.companies[:3]:  # 只显示前3家
            report = self.analyzer.generate_company_report(company['id'])
            briefing += f"### {company['chinese_name']} ({company['name']})\n"
            briefing += f"- **评分**：{report['investment_analysis']['final_score']}/10\n"
            briefing += f"- **建议**：{report['investment_recommendation']['action']}\n"
            briefing += f"- **关注点**：{', '.join(company['focus_area'][:2])}\n\n"
        
        briefing += """---

## ⚠️ 风险提示

"""
        risks = industry['risk_assessment']
        for risk, level in risks.items():
            briefing += f"- **{risk}**：{level}\n"
        
        briefing += f"""

---

## 🦞 分析师观点（小龙虾）

**核心判断**：AI芯片是数字经济的"发动机"，国产替代是确定性最强的主线。

**操作建议**：
1. **短期**：关注已上市龙头企业，把握政策红利
2. **中期**：布局垂直场景专精公司，寻找差异化机会
3. **长期**：押注下一代计算范式，提前卡位

**今日关注**：关注中美技术对话进展及国内产业政策动向。

---
*本报告由Alan的AI伙伴小龙虾自动生成，数据仅供参考，投资需谨慎。*
*绿色护眼主题：{self.green_theme['primary']}*
"""
        
        return briefing
    
    def generate_company_depth_report(self, company_id: str) -> str:
        """生成公司深度分析报告"""
        report = self.analyzer.generate_company_report(company_id)
        if "error" in report:
            return f"错误：{report['error']}"
        
        company = next((c for c in self.analyzer.companies if c['id'] == company_id))
        
        depth_report = f"""# 🔍 {company['chinese_name']}深度分析报告
**报告日期：{self.today}** | **生成：小龙虾投资分析系统**

---

## 📋 公司概况

**公司名称**：{company['chinese_name']} ({company['name']})
**专注领域**：{', '.join(company['focus_area'])}
**技术路线**：{company['technology_route']}
**竞争优势**：{company['competitive_advantage']}

---

## 📊 投资评分分析

**综合评分**：{report['investment_analysis']['final_score']}/10

### 评分明细
"""
        
        # 评分明细
        for factor, score in report['investment_analysis']['score_breakdown'].items():
            depth_report += f"- **{factor}**：{score}/10\n"
        
        depth_report += f"""

### 投资建议
**操作建议**：{report['investment_recommendation']['action']}
**建议理由**：{report['investment_recommendation']['reason']}
**持仓建议**：{report['investment_recommendation']['position_suggestion']}
**时间周期**：{report['investment_recommendation']['time_horizon']}

---

## ⚖️ 竞争优势与风险

### 核心优势
"""
        
        for advantage in report['competitive_analysis']['advantages']:
            depth_report += f"- ✅ {advantage}\n"
        
        depth_report += "\n### 主要风险\n"
        
        for risk in report['competitive_analysis']['risks']:
            depth_report += f"- ⚠️ {risk}\n"
        
        depth_report += f"""
**市场地位**：{report['competitive_analysis']['market_position']}

---

## 👁️ 监控要点

"""
        
        for i, point in enumerate(report['monitoring_points'], 1):
            depth_report += f"{i}. {point}\n"
        
        depth_report += f"""

---

## 🎯 小龙虾分析视角

### 投资逻辑
1. **技术壁垒**：{company['technology_route']}路线是否可持续？
2. **市场空间**：{', '.join(company['focus_area'][:2])}领域增长潜力如何？
3. **竞争格局**：在{report['competitive_analysis']['market_position']}位置上的护城河有多深？

### 关键问题
- 公司如何应对{report['competitive_analysis']['risks'][0] if report['competitive_analysis']['risks'] else '行业竞争'}？
- 技术迭代对公司的影响有多大？
- 政策环境变化带来的机遇与挑战？

---

## 📅 后续跟踪计划

1. **每周**：监控公司新闻及行业动态
2. **每月**：更新财务数据及市场份额
3. **每季**：重新评估投资评分及建议
4. **重大事件**：实时分析并更新报告

---
*本报告由Alan的AI伙伴小龙虾自动生成，基于公开信息整理分析。*
*投资有风险，决策需谨慎。建议结合自身风险承受能力做出投资决定。*
*报告主题色：{self.green_theme['primary']}（绿色护眼模式）*
"""
        
        return depth_report
    
    def generate_portfolio_report(self, risk_profile: str = "balanced") -> str:
        """生成投资组合报告"""
        portfolio = self.analyzer.generate_portfolio_suggestion(risk_profile)
        
        portfolio_report = f"""# 💼 AI芯片投资组合建议
**风险偏好：{risk_profile}** | **报告日期：{self.today}** | **生成：小龙虾投资分析系统**

---

## 📈 组合概览

**预期回报**：{portfolio['expected_return']}
**最大回撤**：{portfolio['max_drawdown']}
**再平衡频率**：{portfolio['rebalance_frequency']}

---

## 🎯 资产配置

"""
        
        # 配置详情
        total_weight = sum(portfolio['allocation'].values())
        for company_id, weight in portfolio['allocation'].items():
            if company_id == "cash":
                portfolio_report += f"- **现金**：{weight}%\n"
            else:
                company = next((c for c in self.analyzer.companies if c['id'] == company_id), None)
                if company:
                    portfolio_report += f"- **{company['chinese_name']}**：{weight}%\n"
        
        portfolio_report += f"\n**总配置**：{total_weight}%\n"
        
        portfolio_report += """
---

## 🔄 再平衡策略

### 触发条件
1. 单一资产权重偏离目标±5%
2. 行业重大政策变化
3. 公司基本面重大变化
4. 定期季度再平衡

### 调整原则
- 上涨超配 → 适度减仓锁定收益
- 下跌低配 → 逢低加仓摊薄成本
- 风险变化 → 调整风险敞口

---

## ⚠️ 风险管理

### 风险控制措施
1. **仓位控制**：单一个股不超过30%
2. **止损纪律**：个股下跌15%触发止损检查
3. **分散投资**：覆盖不同技术路线和应用场景
4. **现金储备**：保持10-20%现金应对机会

### 压力测试
- **悲观情景**：行业增速放缓至20%，组合回撤25-30%
- **中性情景**：行业增速35%，组合回报25-35%
- **乐观情景**：行业增速50%，组合回报40-50%

---

## 📊 绩效跟踪指标

### 绝对指标
- 累计收益率
- 年化收益率
- 最大回撤
- 夏普比率

### 相对指标
- 相对于AI芯片指数的超额收益
- 相对于科技板块的相对强弱
- 风险调整后收益

---

## 🦞 组合经理观点

**当前市场判断**：
- AI芯片行业处于高速成长期
- 国产替代提供确定性机会
- 技术迭代带来结构性变化

**配置思路**：
1. **核心持仓**：技术领先、生态完善的龙头企业
2. **卫星持仓**：垂直场景、特色技术的成长公司
3. **机会持仓**：下一代技术的早期布局

**操作建议**：
- 坚持定投，平滑成本
- 关注政策动向，把握国产替代节奏
- 警惕技术迭代风险，保持组合灵活性

---
*本投资组合建议由Alan的AI伙伴小龙虾基于量化模型生成。*
*实际投资需结合个人风险承受能力、投资目标及市场情况。*
*过去表现不代表未来收益，投资有风险，入市需谨慎。*
*报告主题色：{self.green_theme['primary']}（绿色护眼模式）*
"""
        
        return portfolio_report
    
    def save_report(self, report_type: str, content: str, filename: str = None):
        """保存报告到文件"""
        if not filename:
            filename = f"{report_type}_{self.today}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"报告已保存：{filename}")
        return filename

def main():
    """主函数 - 演示报告生成功能"""
    print("=" * 60)
    print("AI芯片投资报告生成系统")
    print("=" * 60)
    
    generator = ReportGenerator()
    
    # 1. 生成每日简报
    print("\n1. 生成每日简报...")
    briefing = generator.generate_daily_briefing()
    generator.save_report("daily_briefing", briefing, "output/每日简报.md")
    print("✅ 每日简报生成完成")
    
    # 2. 生成华为昇腾深度报告
    print("\n2. 生成公司深度报告...")
    depth_report = generator.generate_company_depth_report("huawei_ascend")
    generator.save_report("company_depth", depth_report, "output/华为昇腾深度分析.md")
    print("✅ 公司深度报告生成完成")
    
    # 3. 生成投资组合报告
    print("\n3. 生成投资组合报告...")
    portfolio_report = generator.generate_portfolio_report("balanced")
    generator.save_report("portfolio", portfolio_report, "output/投资组合建议.md")
    print("✅ 投资组合报告生成完成")
    
    print("\n" + "=" * 60)
    print("所有报告已生成完毕！")
    print("查看 output/ 目录获取完整报告")
    print("=" * 60)

if __name__ == "__main__":
    main()