@echo off
echo ========================================
echo 🦞 简单Git推送测试
echo ========================================
echo.

echo 📋 步骤1: 显示当前目录
cd
echo.

echo 📋 步骤2: 显示Git配置
git config --list | findstr "user"
echo.

echo 📋 步骤3: 检查Git状态
if exist ".git" (
    echo ✅ Git仓库已初始化
    git status
) else (
    echo ❌ 当前目录不是Git仓库
)
echo.

echo 📋 步骤4: 显示重要文件
echo 网站模板文件:
if exist "news_website_template.html" (
    echo ✅ news_website_template.html (大小: %~z0 bytes)
) else (
    echo ❌ news_website_template.html 不存在
)

echo.
echo 新闻数据文件:
if exist "website_data/news-data.json" (
    echo ✅ website_data/news-data.json
) else (
    echo ❌ website_data/news-data.json 不存在
)
echo.

echo 📋 步骤5: GitHub配置信息
type github_config.json | findstr "username repo"
echo.

echo ========================================
echo 🎯 测试说明
echo ========================================
echo.
echo 这个测试将验证:
echo 1. Git命令行工具是否可用
echo 2. 当前环境是否适合Git操作
echo 3. 必要文件是否存在
echo.
echo 如果所有检查都通过，我们可以进行下一步:
echo 手动Git推送测试。
echo.
echo ========================================
pause