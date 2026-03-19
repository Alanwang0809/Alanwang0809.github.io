@echo off
echo ========================================
echo Crayfish Trader - JavaScript Version
echo ========================================
echo.

echo Step 1: Check Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

node --version
echo OK: Node.js found

echo.
echo Step 2: Install dependencies...
if not exist "node_modules" (
    echo Installing axios...
    npm install axios
) else (
    echo Dependencies already installed
)

echo.
echo Step 3: Test the system...
node test_api.js
if errorlevel 1 (
    echo WARNING: Test had issues
) else (
    echo OK: System test passed
)

echo.
echo Step 4: Start monitoring...
echo.
echo To start monitoring:
echo   npm start
echo   or: node trading_api.js
echo.
echo The system will:
echo - Monitor prices every 5 minutes
echo - Generate buy/sell signals
echo - Save signals to trading_signals.json
echo.
echo Press Ctrl+C to stop
echo.
pause

echo.
echo Starting monitoring...
node trading_api.js