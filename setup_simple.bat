@echo off
echo ========================================
echo Trading System Setup
echo ========================================
echo.

echo Step 1: Check Python...
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

python --version
echo OK: Python found

echo.
echo Step 2: Check pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: pip not working, trying to fix...
    python -m ensurepip --upgrade
)

echo.
echo Step 3: Install required libraries...
echo Installing: yfinance pandas numpy matplotlib pandas-ta
python -m pip install yfinance pandas numpy matplotlib pandas-ta --user
if errorlevel 1 (
    echo ERROR: Failed to install libraries
    pause
    exit /b 1
)
echo OK: Libraries installed

echo.
echo Step 4: Test Python environment...
python -c "import yfinance, pandas, numpy; print('OK: Python environment test passed')"
if errorlevel 1 (
    echo ERROR: Python environment test failed
    pause
    exit /b 1
)

echo.
echo Step 5: Create run script...
(
echo @echo off
echo python "%%~dp0run_bot.py" %%*
) > trading\run.bat
echo OK: Created trading\run.bat

echo.
echo Step 6: Test trading system logic...
cd trading
python test_system.py
cd ..
if errorlevel 1 (
    echo WARNING: Trading system test had issues
) else (
    echo OK: Trading system logic test passed
)

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo To run trading system:
echo   1. cd trading
echo   2. python run_bot.py
echo   or run: trading\run.bat
echo.
echo Configuration:
echo   Edit trading\config.yaml for watchlist
echo   See trading\README.md for documentation
echo.
pause