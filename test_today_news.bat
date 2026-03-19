@echo off
echo ========================================
echo 🦞 今日新闻网站测试脚本
echo ========================================
echo.

echo [1/5] 检查文件...
set "WEBSITE_DIR=C:\Users\sbjpk\.openclaw\workspace\daily_news_websites\news_2026-03-18"
if exist "%WEBSITE_DIR%\index.html" (
    echo ✅ index.html 存在
) else (
    echo ❌ index.html 不存在
    goto :error
)

if exist "%WEBSITE_DIR%\styles.css" (
    echo ✅ styles.css 存在
) else (
    echo ❌ styles.css 不存在
    goto :error
)

if exist "%WEBSITE_DIR%\script.js" (
    echo ✅ script.js 存在
) else (
    echo ❌ script.js 不存在
    goto :error
)
echo.

echo [2/5] 文件大小检查...
for %%F in ("%WEBSITE_DIR%\index.html") do set index_size=%%~zF
for %%F in ("%WEBSITE_DIR%\styles.css") do set css_size=%%~zF
for %%F in ("%WEBSITE_DIR%\script.js") do set js_size=%%~zF
echo index.html: %index_size% 字节
echo styles.css: %css_size% 字节
echo script.js: %js_size% 字节
echo.

echo [3/5] 本地测试建议...
echo 请手动执行以下测试：
echo 1. 打开文件资源管理器
echo 2. 导航到: %WEBSITE_DIR%
echo 3. 双击 index.html 在浏览器中打开
echo 4. 测试所有功能
echo.

echo [4/5] 部署测试建议...
echo 部署地址: https://alanwang0809.github.io/news/2026-03-18/
echo.
echo 部署方法A（Git命令）:
echo   1. cd "C:\Users\sbjpk\.openclaw\workspace"
echo   2. git clone https://github.com/Alanwang0809/Alanwang0809.github.io.git
echo   3. cd Alanwang0809.github.io
echo   4. mkdir news\2026-03-18
echo   5. xcopy /E /I "%WEBSITE_DIR%\*" "news\2026-03-18\"
echo   6. git add .
echo   7. git commit -m "测试：添加2026-03-18新闻网站"
echo   8. git push origin main
echo.
echo 部署方法B（GitHub网页）:
echo   1. 访问: https://github.com/Alanwang0809/Alanwang0809.github.io
echo   2. 点击 "Add file" → "Upload files"
echo   3. 创建目录: news/2026-03-18/
echo   4. 拖放3个文件到该目录
echo   5. 点击 "Commit changes"
echo.

echo [5/5] 在线测试...
echo 部署后等待1-2分钟，然后访问：
echo https://alanwang0809.github.io/news/2026-03-18/
echo.
echo 测试所有功能，确保与本地版本一致。
echo.

echo ========================================
echo 🎉 测试指南完成！
echo ========================================
echo.
echo 📄 详细测试指南: TODAY_TEST_GUIDE.md
echo 📁 网站文件: %WEBSITE_DIR%
echo 🌐 目标地址: https://alanwang0809.github.io/news/2026-03-18/
echo.
echo 🚀 建议先进行本地测试，确认功能正常后再部署。
echo ========================================
pause
exit /b 0

:error
echo.
echo ❌ 测试文件检查失败，请检查文件是否存在。
echo ========================================
pause
exit /b 1