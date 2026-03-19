@echo off
echo 纳析光电研究文件打开工具
echo ============================
echo.
echo 1. 纳析光电投资价值分析报告（Word文档）
echo 2. 纳析光电信息收集（Markdown文档）
echo 3. 研究总结与建议（Markdown文档）
echo 4. 打开所有文件
echo 5. 退出
echo.
set /p choice="请选择要打开的文件（1-5）："

if "%choice%"=="1" (
    start "" "纳析光电投资价值分析报告.docx"
    goto end
)

if "%choice%"=="2" (
    start "" "纳析光电信息收集.md"
    goto end
)

if "%choice%"=="3" (
    start "" "研究总结与建议.md"
    goto end
)

if "%choice%"=="4" (
    start "" "纳析光电投资价值分析报告.docx"
    start "" "纳析光电信息收集.md"
    start "" "研究总结与建议.md"
    goto end
)

if "%choice%"=="5" (
    exit
)

:end
echo.
echo 文件已打开，按任意键退出...
pause >nul