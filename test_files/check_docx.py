#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查python-docx库是否可用
"""

import sys

print("检查python-docx库...")

try:
    import docx
    print("✅ python-docx库可用")
    print(f"版本信息: {docx.__version__ if hasattr(docx, '__version__') else '未知'}")
except ImportError as e:
    print("❌ python-docx库未安装")
    print(f"错误信息: {e}")
    print("\n可能的解决方案:")
    print("1. 安装python-docx: pip install python-docx")
    print("2. 使用其他方式创建Word文件")
    print("3. 先创建.txt文件测试流程")

# 检查其他相关库
print("\n检查其他可能用到的库...")

try:
    import os
    print("✅ os库可用")
except ImportError:
    print("❌ os库不可用")

try:
    import datetime
    print("✅ datetime库可用")
except ImportError:
    print("❌ datetime库不可用")

print("\nPython版本:", sys.version)