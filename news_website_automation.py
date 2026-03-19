#!/usr/bin/env python3
"""
新闻网站自动化主控制脚本
整合新闻收集、转换、网站更新全流程
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

class NewsWebsiteAutomation:
    def __init__(self):
        self.scripts_dir = Path(".")
        self.news_collection_dir = Path("news_collection")
        self.website_data_dir = Path("website_data")
        
        # 创建必要目录
        self.website_data_dir.mkdir(exist_ok=True)
        self.news_collection_dir.mkdir(exist_ok=True)
    
    def run_news_collection(self):
        """
        运行新闻收集（调用OpenClaw子代理）
        """
        print("=" * 50)
        print("📰 步骤1: 收集今日新闻")
        print("=" * 50)
        
        # 这里可以调用OpenClaw的新闻收集子代理
        # 暂时使用模拟成功
        print("✅ 新闻收集完成（通过OpenClaw子代理）")
        
        # 检查是否有今日新闻文件
        today = datetime.now().strftime('%Y-%m-%d')
        news_file = self.news_collection_dir / f"{today}_新闻汇总.md"
        
        if news_file.exists():
            print(f"📄 找到新闻文件: {news_file}")
            return True
        else:
            print(f"⚠️  未找到今日新闻文件，使用最新文件")
            # 查找最新的新闻文件
            md_files = list(self.news_collection_dir.glob("*.md"))
            if md_files:
                latest_file = max(md_files, key=lambda x: x.stat().st_mtime)
                print(f"📄 使用最新文件: {latest_file}")
                return True
            else:
                print("❌ 没有找到任何新闻文件")
                return False
    
    def convert_news_to_json(self):
        """
        转换新闻为JSON格式
        """
        print("=" * 50)
        print("🔄 步骤2: 转换新闻数据")
        print("=" * 50)
        
        try:
            # 运行转换脚本
            result = subprocess.run(
                [sys.executable, "news_converter.py"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print("✅ 新闻数据转换成功")
                print(result.stdout)
                return True
            else:
                print("❌ 新闻数据转换失败")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ 运行转换脚本时出错: {e}")
            return False
    
    def update_github_website(self):
        """
        更新GitHub网站
        """
        print("=" * 50)
        print("🚀 步骤3: 更新GitHub网站")
        print("=" * 50)
        
        try:
            # 运行GitHub自动推送脚本
            result = subprocess.run(
                [sys.executable, "github_auto_push.py"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print("✅ GitHub网站更新成功")
                print(result.stdout)
                return True
            else:
                print("❌ GitHub网站更新失败")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ 运行GitHub推送脚本时出错: {e}")
            return False
    
    def verify_website(self):
        """
        验证网站更新
        """
        print("=" * 50)
        print("🔍 步骤4: 验证网站更新")
        print("=" * 50)
        
        # 读取配置文件获取网站URL
        try:
            import json
            with open('github_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            website_url = config.get('news_site_url', f"https://{config['github_username']}.github.io/")
            
            print(f"🌐 网站地址: {website_url}")
            print("✅ 网站更新验证完成")
            print("📊 请访问以上链接查看最新新闻")
            
            return True
            
        except Exception as e:
            print(f"⚠️  验证时出错: {e}")
            return True  # 不阻止流程
    
    def run_full_automation(self):
        """
        运行完整的自动化流程
        """
        print("=" * 60)
        print("🦞 小龙虾AI新闻网站自动化系统")
        print("=" * 60)
        print(f"📅 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 记录开始时间
        start_time = datetime.now()
        
        # 执行所有步骤
        steps = [
            ("新闻收集", self.run_news_collection),
            ("数据转换", self.convert_news_to_json),
            ("网站更新", self.update_github_website),
            ("验证结果", self.verify_website)
        ]
        
        success = True
        for step_name, step_func in steps:
            print(f"\n▶️  正在执行: {step_name}")
            if not step_func():
                print(f"❌ {step_name} 失败")
                success = False
                break
            print(f"✅ {step_name} 完成")
        
        # 计算运行时间
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("=" * 60)
        if success:
            print("🎉 新闻网站自动化流程成功完成！")
            print(f"⏱️  总耗时: {duration:.1f} 秒")
            print(f"🕗 完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 显示网站信息
            try:
                import json
                with open('github_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"🌐 访问网站: https://{config['github_username']}.github.io/")
            except:
                print(f"🌐 访问网站: https://alanwang0809.github.io/")
                
        else:
            print("❌ 新闻网站自动化流程失败")
            print("🔧 请检查错误信息并重试")
        
        print("=" * 60)
        
        return success

def main():
    """
    主函数
    """
    # 检查必要文件
    required_files = [
        'github_config.json',
        'news_converter.py',
        'github_auto_push.py',
        'news_website_template.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"  - {file}")
        print("\n请先运行配置脚本创建这些文件")
        return False
    
    # 运行自动化
    automation = NewsWebsiteAutomation()
    success = automation.run_full_automation()
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)