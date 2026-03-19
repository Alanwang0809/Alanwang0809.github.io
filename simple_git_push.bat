@echo off
echo ========================================
echo 开始自动推送更新到GitHub
echo ========================================

REM 设置工作目录
cd /d "C:\Users\sbjpk\.openclaw\workspace"

REM 检查文件状态
echo.
echo 1. 检查文件状态...
git status

echo.
echo 2. 添加所有更改...
git add index.html
git add news-data.json

echo.
echo 3. 提交更改...
git commit -m "自动更新测试: 添加国际新闻 - 时间: %date% %time%"

echo.
echo 4. 推送到GitHub...
git push origin main

echo.
echo ========================================
echo 推送完成！
echo ========================================
pause