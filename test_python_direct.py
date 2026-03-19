#!/usr/bin/env python3
"""
直接测试Python环境
"""

import sys
import subprocess
import os

print("Python Environment Test")
print("=" * 50)

# 1. Python信息
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"Platform: {sys.platform}")

# 2. 检查必要模块
required_modules = ["sys", "os", "json", "datetime", "math"]

print("\nChecking required modules:")
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module}")

# 3. 尝试导入交易相关模块
trading_modules = ["yfinance", "pandas", "numpy", "matplotlib"]

print("\nChecking trading modules:")
for module in trading_modules:
    try:
        __import__(module)
        version = eval(f"{module}.__version__")
        print(f"  ✓ {module} {version}")
    except ImportError:
        print(f"  ✗ {module} (not installed)")

# 4. 测试基本功能
print("\nTesting basic functionality:")

# 创建测试数据
import datetime
test_data = {
    "timestamp": datetime.datetime.now().isoformat(),
    "test_passed": True,
    "python_version": sys.version,
    "modules_installed": len([m for m in trading_modules if m in sys.modules])
}

print(f"  Current time: {test_data['timestamp']}")
print(f"  Trading modules installed: {test_data['modules_installed']}/{len(trading_modules)}")

# 5. 建议
print("\n" + "=" * 50)
print("Recommendations:")

if test_data['modules_installed'] < 2:
    print("1. Install required libraries:")
    print("   pip install yfinance pandas numpy matplotlib")
    
if "win" in sys.platform:
    print("2. On Windows, you may need to run as administrator")
    
print("3. Or use: python -m pip install --user <package>")

print("\nTest completed successfully!")

# 保存测试结果
with open("python_test_result.json", "w") as f:
    import json
    json.dump(test_data, f, indent=2, default=str)