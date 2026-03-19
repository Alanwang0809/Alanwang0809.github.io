@echo off
echo ========================================
echo 🦞 创建今日新闻网站
echo ========================================
echo.

echo [1/5] 设置环境...
cd /d "C:\Users\sbjpk\.openclaw\workspace"
if not exist "daily_news_websites" mkdir daily_news_websites
echo.

echo [2/5] 获取今日日期...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "DATE=%YYYY%-%MM%-%DD%"
echo 今日日期: %DATE%
echo.

echo [3/5] 创建网站目录...
set "WEBSITE_DIR=daily_news_websites\news_%DATE%"
if not exist "%WEBSITE_DIR%" mkdir "%WEBSITE_DIR%"
echo 网站目录: %WEBSITE_DIR%
echo.

echo [4/5] 复制模板文件...
set "TEMPLATE_DIR=news_website_2026_03_18"
copy "%TEMPLATE_DIR%\index.html" "%WEBSITE_DIR%\index.html" >nul
copy "%TEMPLATE_DIR%\styles.css" "%WEBSITE_DIR%\styles.css" >nul
copy "%TEMPLATE_DIR%\script.js" "%WEBSITE_DIR%\script.js" >nul
echo ✅ 复制模板文件完成
echo.

echo [5/5] 创建部署指令...
(
echo # 🚀 部署指令 - %DATE%新闻网站
echo.
echo ## 部署到GitHub个人页面
echo 你的个人页面: https://alanwang0809.github.io/
echo 目标路径: /news/%DATE%/
echo 最终地址: https://alanwang0809.github.io/news/%DATE%/
echo.
echo ## 方法A：使用Git命令（推荐）
echo.
echo ### 步骤1：克隆你的个人页面仓库
echo 在命令提示符中运行：
echo.
echo cd "C:\Users\sbjpk\.openclaw\workspace"
echo git clone https://github.com/Alanwang0809/Alanwang0809.github.io.git
echo cd Alanwang0809.github.io
echo.
echo ### 步骤2：创建新闻目录并复制文件
echo mkdir news\%DATE%
echo xcopy /E /I "%WEBSITE_DIR%\*" "news\%DATE%\" 
echo.
echo ### 步骤3：提交和推送
echo git add .
echo git commit -m "添加 %DATE% 新闻网站"
echo git push origin main
echo.
echo ## 方法B：直接上传到GitHub网页
echo 1. 访问: https://github.com/Alanwang0809/Alanwang0809.github.io
echo 2. 点击 "Add file" → "Upload files"
echo 3. 创建目录: news/%DATE%/
echo 4. 拖放 %WEBSITE_DIR% 中的所有文件到该目录
echo 5. 点击 "Commit changes"
echo.
echo ## 部署后
echo - 等待1-2分钟GitHub Pages更新
echo - 访问: https://alanwang0809.github.io/news/%DATE%/
echo - 测试所有功能
) > "%WEBSITE_DIR%\deploy_instructions.txt"

echo ✅ 创建部署指令文件
echo.

echo ========================================
echo 🎉 今日新闻网站创建完成！
echo ========================================
echo.
echo 📁 网站文件: %WEBSITE_DIR%
echo 📄 部署指令: %WEBSITE_DIR%\deploy_instructions.txt
echo 🌐 预计网址: https://alanwang0809.github.io/news/%DATE%/
echo.
echo 🚀 下一步: 按照部署指令将网站部署到你的GitHub个人页面
echo ========================================
pause