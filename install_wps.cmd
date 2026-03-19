@echo off
echo ========================================
echo        WPS Office 安装程序
echo ========================================
echo.

echo 检查是否已安装WPS Office...
where wps >nul 2>nul
if %errorlevel% equ 0 (
    echo WPS Office 已经安装！
    echo 你可以直接打开.docx文件了。
    echo.
    pause
    exit /b 0
)

echo 未找到WPS Office，开始安装...
echo.

REM 创建下载目录
set "DOWNLOAD_DIR=%USERPROFILE%\Downloads\WPS_Install"
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"

echo 正在下载WPS Office...
echo 这可能需要几分钟，请耐心等待...
echo.

REM 使用curl下载（如果可用）
where curl >nul 2>nul
if %errorlevel% equ 0 (
    echo 使用curl下载...
    curl -L -o "%DOWNLOAD_DIR%\WPSOffice_Setup.exe" "https://wdl1.cache.wps.cn/wps/download/ep/WPS2019/WPSOffice_11.8.2.12195.exe"
) else (
    echo 使用bitsadmin下载...
    bitsadmin /transfer wpsdownload /download /priority normal "https://wdl1.cache.wps.cn/wps/download/ep/WPS2019/WPSOffice_11.8.2.12195.exe" "%DOWNLOAD_DIR%\WPSOffice_Setup.exe"
)

if exist "%DOWNLOAD_DIR%\WPSOffice_Setup.exe" (
    echo 下载完成！
    echo.
    echo 正在启动安装程序...
    echo 请按照安装向导完成安装。
    echo 建议选择默认安装选项。
    echo.
    
    start "" "%DOWNLOAD_DIR%\WPSOffice_Setup.exe"
    
    echo 安装程序已启动，请按照提示完成安装。
    echo 安装完成后，你就可以打开.docx研究报告了。
) else (
    echo 下载失败！
    echo.
    echo 请手动安装WPS Office：
    echo 1. 访问 https://www.wps.cn/
    echo 2. 点击"免费下载"
    echo 3. 运行下载的安装程序
)

echo.
pause