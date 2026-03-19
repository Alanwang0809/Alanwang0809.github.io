@echo off
echo ========================================
echo 🔧 404错误诊断工具
echo ========================================
echo.

echo [1/4] 检查GitHub Pages配置...
echo.
echo 请访问: https://github.com/Alanwang0809/Alanwang0809.github.io/settings/pages
echo.
echo 需要确认:
echo 1. Source: Deploy from a branch
echo 2. Branch: main
echo 3. Folder: / (root)
echo 4. 状态: Your site is published at...
echo.

echo [2/4] 检查文件位置...
echo.
echo 正确位置:
echo Alanwang0809.github.io/
echo └── news/
echo     └── 2026-03-18/
echo         ├── index.html
echo         ├── styles.css
echo         └── script.js
echo.
echo 访问地址: https://alanwang0809.github.io/news/2026-03-18/
echo.

echo [3/4] 测试访问...
echo.
echo 测试方法:
echo 1. 等待2-3分钟
echo 2. 浏览器按 Ctrl+F5 强制刷新
echo 3. 访问: https://alanwang0809.github.io/news/2026-03-18/
echo 4. 如果还是404，尝试: https://alanwang0809.github.io/news/2026-03-18/index.html
echo.

echo [4/4] 常见解决方案...
echo.
echo 方案A: 启用GitHub Pages
echo   1. 访问上面的Pages设置链接
echo   2. 按照提示启用
echo   3. 等待5分钟
echo.
echo 方案B: 检查文件路径
echo   1. 确认文件在 news/2026-03-18/ 目录
echo   2. 确认文件名正确
echo   3. 确认文件内容不为空
echo.
echo 方案C: 清除缓存
echo   1. 浏览器开发者工具 (F12)
echo   2. Network标签 → Disable cache
echo   3. 刷新页面
echo.

echo ========================================
echo 🎯 诊断步骤
echo ========================================
echo.
echo 1. 先检查GitHub Pages是否启用
echo 2. 再检查文件位置是否正确
echo 3. 等待几分钟后测试
echo 4. 如果还是404，截图错误页面发给我
echo ========================================
pause