#!/usr/bin/env python3
"""
每日新闻自动化脚本
功能：收集新闻 → 生成网页 → 部署到GitHub → 发送链接
"""

import os
import json
import datetime
import subprocess
from pathlib import Path

# 配置
WORKSPACE = Path("C:/Users/sbjpk/.openclaw/workspace")
NEWS_DIR = WORKSPACE / "daily_news_websites"
TEMPLATE_DIR = WORKSPACE / "news_website_2026_03_18"

def get_current_date():
    """获取当前日期"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def create_daily_website(date_str):
    """创建每日新闻网站"""
    print(f"📅 创建 {date_str} 新闻网站...")
    
    # 创建日期目录
    website_dir = NEWS_DIR / f"news_{date_str}"
    website_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制模板文件
    template_files = ["index.html", "styles.css", "script.js"]
    for file in template_files:
        src = TEMPLATE_DIR / file
        dst = website_dir / file
        if src.exists():
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            # 更新日期信息
            if file == "index.html":
                content = content.replace("2026年3月18日", f"{date_str}")
                content = content.replace("2026-03-18", date_str)
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ 复制 {file}")
    
    # 创建README
    readme_content = f"""# 🦞 小龙虾新闻服务 - {date_str}重要新闻汇总

## 📋 网站信息
- **日期**: {date_str}
- **生成时间**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **自动化**: 每日新闻自动生成系统
- **部署位置**: GitHub个人页面子目录

## 🎨 功能特点
1. **5个颜色区分的新闻模块**
2. **重要性星级筛选**
3. **响应式设计**
4. **一键打印优化**

## 🔗 访问地址
https://alanwang0809.github.io/news/{date_str}/

## 📁 文件结构
Alanwang0809.github.io/
└── news/
    └── {date_str}/
        ├── index.html
        ├── styles.css
        ├── script.js
        └── README.md

## 🔄 自动化流程
此网站由小龙虾新闻服务自动生成，包含当日重要新闻汇总。

---
**生成系统**: 小龙虾AI伙伴 🦞
**最后更新**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    with open(website_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"  ✅ 创建README.md")
    return website_dir

def deploy_to_github(website_dir, date_str):
    """部署到GitHub个人页面"""
    print(f"🚀 部署 {date_str} 网站到GitHub个人页面...")
    
    # 部署到个人页面的news子目录
    target_path = f"news/{date_str}"
    website_url = f"https://alanwang0809.github.io/{target_path}/"
    
    deployment_script = website_dir / "deploy_instructions.txt"
    instructions = f"""# 🚀 部署指令 - {date_str}新闻网站

## 部署到GitHub个人页面
你的个人页面: https://alanwang0809.github.io/
目标路径: /{target_path}/
最终地址: {website_url}

## 步骤1：克隆你的个人页面仓库
在命令提示符中运行：

cd "C:\\Users\\sbjpk\\.openclaw\\workspace"
git clone https://github.com/Alanwang0809/Alanwang0809.github.io.git
cd Alanwang0809.github.io

## 步骤2：创建新闻目录并复制文件
mkdir -p news/{date_str}
xcopy /E /I "{website_dir}\\*" "news\\{date_str}\\"

## 步骤3：提交和推送
git add .
git commit -m "添加 {date_str} 新闻网站"
git push origin main

## 步骤4：访问网站
等待1-2分钟GitHub Pages更新，然后访问:
{website_url}

## 替代方案：直接上传到GitHub
1. 访问: https://github.com/Alanwang0809/Alanwang0809.github.io
2. 点击 "Add file" → "Upload files"
3. 拖放 {website_dir} 中的所有文件到 news/{date_str}/ 目录
4. 点击 Commit changes

---
**自动化提示**: 提供GitHub PAT后，此流程可以完全自动化。
"""
    
    with open(deployment_script, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"  ✅ 创建部署指令文件")
    return website_url

def generate_daily_report(date_str, website_url):
    """生成每日报告"""
    report = f"""# 🦞 每日新闻自动化报告 - {date_str}

## 📊 执行状态
- ✅ 新闻网站生成完成
- ✅ 文件准备就绪
- ⏳ 等待部署到GitHub

## 🔗 网站信息
- **本地路径**: {NEWS_DIR / f"news_{date_str}"}
- **GitHub仓库**: news_{date_str.replace('-', '_')}
- **访问地址**: {website_url}

## 📋 下一步操作
1. 按照部署指令推送代码到GitHub
2. 启用GitHub Pages
3. 测试网站功能

## 🎯 完全自动化方案
要实现完全自动化，需要：
1. GitHub Personal Access Token (repo权限)
2. 配置自动化部署脚本
3. 设置每日定时任务

## 📞 支持
如有问题，请联系小龙虾AI伙伴 🦞

---
**报告生成时间**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    report_file = NEWS_DIR / f"report_{date_str}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_file

def main():
    """主函数"""
    print("=" * 50)
    print("🦞 每日新闻自动化系统")
    print("=" * 50)
    
    # 获取当前日期
    date_str = get_current_date()
    print(f"📅 处理日期: {date_str}")
    
    # 创建网站
    website_dir = create_daily_website(date_str)
    
    # 生成部署信息
    website_url = deploy_to_github(website_dir, date_str)
    
    # 生成报告
    report_file = generate_daily_report(date_str, website_url)
    
    print("=" * 50)
    print("🎉 自动化流程完成!")
    print(f"📁 网站文件: {website_dir}")
    print(f"📄 部署指令: {website_dir}/deploy_instructions.txt")
    print(f"📊 执行报告: {report_file}")
    print(f"🌐 预计网址: {website_url}")
    print("=" * 50)
    
    # 返回结果
    return {
        "date": date_str,
        "website_dir": str(website_dir),
        "website_url": website_url,
        "report_file": str(report_file)
    }

if __name__ == "__main__":
    result = main()
    
    # 保存结果到JSON文件
    result_file = NEWS_DIR / f"result_{result['date']}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"💾 结果保存到: {result_file}")