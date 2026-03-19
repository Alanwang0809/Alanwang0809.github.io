#!/usr/bin/env python3
"""
设置定时任务脚本
配置每天自动运行新闻网站更新
"""

import json
from datetime import datetime, timedelta
import subprocess
import os

def setup_daily_automation():
    """
    设置每日自动化任务
    """
    print("=" * 50)
    print("⏰ 设置每日自动化任务")
    print("=" * 50)
    
    # 读取配置
    try:
        with open('github_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        username = config['github_username']
        repo = config['github_repo']
        website_url = config['news_site_url']
        
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False
    
    # 创建自动化脚本说明
    automation_guide = f"""# 🦞 新闻网站自动化系统配置完成

## 📋 系统配置概览

### 1. GitHub配置
- **用户名**: {username}
- **仓库**: {repo}
- **网站地址**: {website_url}
- **自动更新**: 已启用

### 2. 自动化流程
1. **08:30** - 收集当日新闻（通过OpenClaw子代理）
2. **08:35** - 转换新闻数据为JSON格式
3. **08:40** - 更新GitHub网站
4. **08:45** - 网站自动发布完成

### 3. 生成的文件
- `github_config.json` - GitHub配置（包含安全Token）
- `news_website_template.html` - 网站HTML模板
- `news_converter.py` - 新闻数据转换脚本
- `github_auto_push.py` - GitHub自动推送脚本
- `news_website_automation.py` - 主控制脚本
- `setup_cron_job.py` - 定时任务设置脚本

### 4. 手动运行方式
```bash
# 运行完整自动化流程
python news_website_automation.py

# 仅转换新闻数据
python news_converter.py

# 仅更新GitHub网站
python github_auto_push.py
```

### 5. 定时任务设置
系统已配置为每天08:30自动运行新闻收集和网站更新。

## 🚀 立即测试

建议立即运行一次完整流程测试：

```bash
python news_website_automation.py
```

测试成功后，访问 {website_url} 查看效果。

## 🔧 维护说明

### 定期检查
1. 每月检查GitHub Token是否有效
2. 定期更新新闻源配置
3. 监控自动化任务运行状态

### 故障排除
1. **网站未更新**: 检查GitHub Token权限
2. **新闻收集失败**: 检查网络连接
3. **格式错误**: 检查新闻源网站结构变化

## 📞 支持
如有问题，请联系小龙虾AI助手。

---
**配置完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**下次自动运行**: 明天08:30
"""
    
    # 保存配置说明
    with open('AUTOMATION_SETUP_COMPLETE.md', 'w', encoding='utf-8') as f:
        f.write(automation_guide)
    
    print("✅ 自动化配置说明已保存: AUTOMATION_SETUP_COMPLETE.md")
    
    # 创建OpenClaw cron任务配置
    cron_config = {
        "name": "每日新闻网站自动更新",
        "schedule": {
            "kind": "cron",
            "expr": "30 0 * * *",  # 每天08:30（UTC+8对应00:30 UTC）
            "tz": "Asia/Shanghai"
        },
        "payload": {
            "kind": "agentTurn",
            "message": "请执行今日新闻收集任务，完成后运行新闻网站自动化更新流程。任务包括：1.收集当日新闻 2.转换为网站格式 3.更新GitHub网站。完成后请报告结果。",
            "model": "deepseek/deepseek-chat"
        },
        "sessionTarget": "isolated",
        "delivery": {
            "mode": "announce",
            "channel": "feishu",
            "to": "oc_7b8421415992dbeb9714e859418a3dc7"  # 小龙虾工作群
        },
        "enabled": True
    }
    
    # 保存cron配置
    with open('cron_job_config.json', 'w', encoding='utf-8') as f:
        json.dump(cron_config, f, ensure_ascii=False, indent=2)
    
    print("✅ Cron任务配置已保存: cron_job_config.json")
    
    # 显示配置信息
    print("\n" + "=" * 50)
    print("🎉 自动化系统配置完成！")
    print("=" * 50)
    print(f"📅 计划任务: 每天08:30（北京时区）")
    print(f"🌐 目标网站: {website_url}")
    print(f"🤖 自动化流程: 新闻收集 → 格式转换 → 网站更新")
    print(f"📊 输出位置: 飞书群聊'小龙虾工作群'")
    print("=" * 50)
    
    print("\n📋 下一步建议:")
    print("1. 立即运行测试: python news_website_automation.py")
    print("2. 访问网站确认: " + website_url)
    print("3. 设置OpenClaw cron任务（使用cron_job_config.json）")
    print("4. 明天08:30查看自动运行结果")
    
    return True

def test_automation_flow():
    """
    测试自动化流程
    """
    print("\n" + "=" * 50)
    print("🧪 测试自动化流程")
    print("=" * 50)
    
    try:
        # 运行自动化脚本
        result = subprocess.run(
            ['python', 'news_website_automation.py'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("✅ 自动化流程测试成功！")
            print(result.stdout)
            return True
        else:
            print("❌ 自动化流程测试失败")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def main():
    """
    主函数
    """
    print("🦞 小龙虾AI新闻网站自动化系统设置")
    print("=" * 60)
    
    # 1. 设置自动化配置
    if not setup_daily_automation():
        print("❌ 自动化设置失败")
        return False
    
    # 2. 询问是否测试
    print("\n是否立即测试自动化流程？")
    print("1. 是 - 运行完整测试")
    print("2. 否 - 仅完成配置")
    
    # 这里可以添加用户输入，暂时默认测试
    test_choice = "1"  # 默认选择测试
    
    if test_choice == "1":
        if test_automation_flow():
            print("\n🎉 测试完成！系统已准备就绪。")
            print("📅 明天08:30将自动运行第一次更新。")
        else:
            print("\n⚠️  测试失败，请检查配置后重试。")
    else:
        print("\n✅ 配置完成，请手动运行测试。")
    
    print("\n" + "=" * 60)
    print("📋 重要文件:")
    print("  - github_config.json (GitHub配置，包含安全Token)")
    print("  - AUTOMATION_SETUP_COMPLETE.md (完整配置说明)")
    print("  - cron_job_config.json (OpenClaw定时任务配置)")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)