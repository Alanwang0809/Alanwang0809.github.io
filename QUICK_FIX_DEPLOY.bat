@echo off
echo ========================================
echo 🚀 快速修复部署 - 今日新闻网站
echo ========================================
echo.

echo [1/4] 检查本地网站文件...
set "LOCAL_DIR=C:\Users\sbjpk\.openclaw\workspace\daily_news_websites\news_2026-03-18"
if not exist "%LOCAL_DIR%\index.html" (
    echo ❌ 错误: index.html 不存在
    echo 请先创建网站文件
    pause
    exit /b 1
)
echo ✅ 本地网站文件存在
echo.

echo [2/4] 最简单的部署方案...
echo.
echo 方案A：使用GitHub网页上传（推荐）
echo 1. 访问: https://github.com/Alanwang0809/Alanwang0809.github.io
echo 2. 点击 "Add file" → "Upload files"
echo 3. 在仓库中创建目录: news/2026-03-18/
echo 4. 拖放以下3个文件到该目录:
echo    - %LOCAL_DIR%\index.html
echo    - %LOCAL_DIR%\styles.css
echo    - %LOCAL_DIR%\script.js
echo 5. 点击 "Commit changes"
echo.
echo 方案B：检查是否已部署
echo 访问: https://alanwang0809.github.io/news/2026-03-18/
echo 如果显示404，说明未部署
echo.

echo [3/4] 启用GitHub Pages（如果未启用）...
echo 1. 访问: https://github.com/Alanwang0809/Alanwang0809.github.io/settings/pages
echo 2. Source选择: Deploy from a branch
echo 3. Branch选择: main
echo 4. Folder选择: / (root)
echo 5. 点击 Save
echo.

echo [4/4] 测试访问...
echo 部署后等待1-2分钟，然后访问:
echo https://alanwang0809.github.io/news/2026-03-18/
echo.
echo 如果仍然打不开，请:
echo 1. 截图错误页面
echo 2. 发送给我分析
echo.

echo ========================================
echo 🎯 你的目标：每日新闻自动生成网页并发送
echo ========================================
echo.
echo ✅ 已实现:
echo 1. 每日新闻自动收集（08:30）
echo 2. 网站模板系统
echo 3. 自动化脚本
echo 4. 定时任务设置
echo.
echo ⚠️ 待完成:
echo 1. 自动部署到GitHub（需要PAT）
echo 2. 自动发送链接
echo 3. 完全自动化
echo.
echo 🔧 完全自动化需要:
echo GitHub Personal Access Token (PAT)
echo 权限: repo, workflow, pages
echo ========================================
pause