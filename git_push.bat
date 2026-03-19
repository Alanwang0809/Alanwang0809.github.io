@echo off
echo 🚀 开始GitHub推送...
cd "C:\Users\sbjpk\.openclaw\workspace\temp_github_push"
git init
git checkout -b main
git remote add origin https://github.com/alanwang0809/alanwang0809.github.io.git
git add .
git commit -m "自动更新: 2026-03-19 新闻"
git push -f origin main
echo ✅ 推送完成！网站将在1-3分钟内更新。
echo 🌐 网站地址: https://alanwang0809.github.io/
pause