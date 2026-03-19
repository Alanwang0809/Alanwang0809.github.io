# Python环境检查和安装脚本

Write-Host "🦞 小龙虾交易系统 - Python环境检查" -ForegroundColor Cyan
Write-Host "=" * 60

# 检查Python
$pythonPaths = @(
    "python",
    "python3", 
    "py",
    "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "C:\Python39\python.exe",
    "C:\Python310\python.exe",
    "C:\Python311\python.exe",
    "C:\Python312\python.exe"
)

Write-Host "`n🔍 检查Python安装..." -ForegroundColor Yellow

$foundPython = $null
foreach ($path in $pythonPaths) {
    try {
        if (Test-Path $path) {
            $fullPath = (Get-Command $path -ErrorAction Stop).Source
            $version = & $fullPath --version 2>&1
            Write-Host "✅ 找到Python: $fullPath" -ForegroundColor Green
            Write-Host "   版本: $version" -ForegroundColor Gray
            $foundPython = $fullPath
            break
        }
    } catch {
        # 继续检查下一个
    }
}

if (-not $foundPython) {
    Write-Host "❌ 未找到Python安装" -ForegroundColor Red
    Write-Host "`n📥 建议安装Python 3.8+:" -ForegroundColor Yellow
    Write-Host "1. 访问 https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. 下载Python 3.8+安装程序" -ForegroundColor White
    Write-Host "3. 安装时勾选 'Add Python to PATH'" -ForegroundColor White
    Write-Host "4. 重新运行此脚本" -ForegroundColor White
    exit 1
}

# 检查pip
Write-Host "`n🔍 检查pip安装..." -ForegroundColor Yellow
try {
    $pipVersion = & $foundPython -m pip --version 2>&1
    Write-Host "✅ pip已安装: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip未安装或有问题" -ForegroundColor Red
    Write-Host "尝试修复pip..." -ForegroundColor Yellow
    try {
        & $foundPython -m ensurepip --upgrade
        Write-Host "✅ pip修复完成" -ForegroundColor Green
    } catch {
        Write-Host "❌ pip修复失败" -ForegroundColor Red
    }
}

# 检查必要库
Write-Host "`n📦 检查必要Python库..." -ForegroundColor Yellow

$requiredLibs = @(
    "yfinance",
    "pandas", 
    "numpy",
    "matplotlib",
    "pandas-ta"
)

foreach ($lib in $requiredLibs) {
    try {
        & $foundPython -c "import $lib; print(f'✅ $lib {eval(`"$lib`".__version__)}')" 2>&1
    } catch {
        Write-Host "❌ $lib 未安装" -ForegroundColor Red
    }
}

# 安装缺失的库
Write-Host "`n📥 安装缺失的库..." -ForegroundColor Yellow
$missingLibs = @()
foreach ($lib in $requiredLibs) {
    try {
        & $foundPython -c "import $lib" 2>&1 | Out-Null
    } catch {
        $missingLibs += $lib
    }
}

if ($missingLibs.Count -gt 0) {
    Write-Host "需要安装: $($missingLibs -join ', ')" -ForegroundColor Yellow
    $installCmd = "& `"$foundPython`" -m pip install $($missingLibs -join ' ')"
    
    Write-Host "执行: $installCmd" -ForegroundColor Gray
    try {
        Invoke-Expression $installCmd
        Write-Host "✅ 库安装完成" -ForegroundColor Green
    } catch {
        Write-Host "❌ 库安装失败" -ForegroundColor Red
        Write-Host "错误: $_" -ForegroundColor Red
    }
} else {
    Write-Host "✅ 所有必要库已安装" -ForegroundColor Green
}

# 创建Python别名
Write-Host "`n🔧 创建Python快捷方式..." -ForegroundColor Yellow
$pythonAlias = "trading_python"
$aliasScript = @"
@echo off
"$foundPython" %*
"@

Set-Content -Path "trading\$pythonAlias.bat" -Value $aliasScript -Encoding ASCII
Write-Host "✅ 创建了 trading\$pythonAlias.bat" -ForegroundColor Green

# 测试交易系统
Write-Host "`n🧪 测试交易系统..." -ForegroundColor Yellow
try {
    & $foundPython "trading\test_system.py"
    Write-Host "✅ 交易系统测试通过" -ForegroundColor Green
} catch {
    Write-Host "❌ 交易系统测试失败" -ForegroundColor Red
    Write-Host "错误: $_" -ForegroundColor Red
}

Write-Host "`n" + "=" * 60
Write-Host "🎉 Python环境检查完成！" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host "`n下一步:"
Write-Host "1. 运行交易系统: trading\$pythonAlias.bat run_bot.py" -ForegroundColor White
Write-Host "2. 或直接运行: `"$foundPython`" trading\run_bot.py" -ForegroundColor White
Write-Host "`n按任意键继续..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")