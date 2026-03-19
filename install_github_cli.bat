@echo off
echo ========================================
echo 🚀 GitHub CLI 安装脚本
echo ========================================
echo.

echo [1/4] 检查当前系统...
echo.

echo [2/4] 下载GitHub CLI安装程序...
echo 正在从GitHub Releases下载最新版本...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cli/cli/releases/download/v2.0.0/gh_2.0.0_windows_amd64.msi' -OutFile 'gh_installer.msi'"

if exist gh_installer.msi (
    echo ✅ 下载成功: gh_installer.msi
) else (
    echo ❌ 下载失败，请手动下载
    echo 手动下载地址: https://github.com/cli/cli/releases/latest
    echo 下载文件: gh_*_windows_amd64.msi
    pause
    exit /b 1
)

echo.
echo [3/4] 安装GitHub CLI...
echo 正在安装，请等待...
msiexec /i gh_installer.msi /quiet /norestart

echo.
echo [4/4] 验证安装...
echo.
where gh
if %errorlevel% equ 0 (
    echo ✅ GitHub CLI 安装成功!
    gh --version
) else (
    echo ❌ GitHub CLI 安装失败
    echo 请尝试手动安装:
    echo 1. 访问: https://cli.github.com/
    echo 2. 下载Windows安装程序
    echo 3. 运行安装程序
)

echo.
echo ========================================
echo 📋 下一步: 配置GitHub认证
echo ========================================
echo.
echo 安装完成后，需要配置GitHub认证:
echo.
echo 方法A: 使用GitHub PAT (推荐)
echo   1. 生成PAT: https://github.com/settings/tokens
echo   2. 运行: gh auth login --with-token < token.txt
echo.
echo 方法B: 交互式登录
echo   运行: gh auth login
echo.
echo 方法C: 使用现有认证
echo   运行: gh auth status
echo.
pause