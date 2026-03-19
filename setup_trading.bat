@echo off
chcp 65001 >nul
echo ========================================
echo 🦞 小龙虾交易系统安装程序
echo ========================================
echo.

echo 步骤1: 检查Python环境...
where python >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo ✅ Python已安装
) else (
    echo ❌ Python未安装或不在PATH中
    echo.
    echo 请安装Python 3.8+:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装Python 3.8+
    echo 3. 安装时勾选"Add Python to PATH"
    echo 4. 重新运行此脚本
    pause
    exit /b 1
)

echo.
echo 步骤2: 检查pip...
python -m pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ pip已安装
) else (
    echo ❌ pip有问题，尝试修复...
    python -m ensurepip --upgrade
)

echo.
echo 步骤3: 安装必要库...
echo 安装: yfinance pandas numpy matplotlib pandas-ta

python -m pip install yfinance pandas numpy matplotlib pandas-ta --user
if %errorlevel% neq 0 (
    echo ❌ 库安装失败
    echo 尝试使用管理员权限运行
    pause
    exit /b 1
)
echo ✅ 库安装完成

echo.
echo 步骤4: 测试Python环境...
python -c "import yfinance, pandas, numpy; print('✅ Python环境测试通过')"
if %errorlevel% neq 0 (
    echo ❌ Python环境测试失败
    pause
    exit /b 1
)

echo.
echo 步骤5: 创建运行脚本...
(
echo @echo off
echo python "%%~dp0run_bot.py" %%*
) > trading\run_trading.bat

echo ✅ 创建了 trading\run_trading.bat

echo.
echo 步骤6: 测试交易系统逻辑...
cd trading
python test_system.py
cd ..

if %errorlevel% neq 0 (
    echo ❌ 交易系统测试失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 安装完成！
echo ========================================
echo.
echo 运行交易系统:
echo   1. cd trading
echo   2. python run_bot.py
echo   或直接运行: trading\run_trading.bat
echo.
echo 配置说明:
echo   编辑 trading\config.yaml 配置监控列表
echo   编辑 trading\README.md 查看系统文档
echo.
pause