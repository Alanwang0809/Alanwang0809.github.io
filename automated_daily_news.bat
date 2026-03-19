@echo off
echo ========================================
echo 🦞 每日新闻自动化系统
echo ========================================
echo.

echo [1/5] 设置环境...
cd /d "C:\Users\sbjpk\.openclaw\workspace"
if not exist "daily_news_websites" mkdir daily_news_websites
echo.

echo [2/5] 运行自动化脚本...
python daily_news_automation.py
echo.

echo [3/5] 检查生成结果...
for /f "tokens=2 delims=:" %%i in ('findstr /c:"处理日期:" daily_news_automation.py 2^>nul') do set DATE=%%i
set DATE=%DATE:~1%
echo 处理日期: %DATE%
echo.

echo [4/5] 文件位置...
echo 网站文件: daily_news_websites\news_%DATE%
echo 部署指令: daily_news_websites\news_%DATE%\deploy_instructions.txt
echo 执行报告: daily_news_websites\report_%DATE%.md
echo.

echo [5/5] 下一步操作:
echo.
echo 1. 查看部署指令文件
echo 2. 按照指令部署到GitHub
echo 3. 启用GitHub Pages
echo 4. 测试网站访问
echo.
echo ========================================
echo 🎉 自动化流程完成！
echo 每日新闻网站已生成，等待部署。
echo ========================================
pause