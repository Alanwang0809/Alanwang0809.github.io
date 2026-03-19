# WPS Office 下载和安装脚本
Write-Host "正在准备下载WPS Office..." -ForegroundColor Green

# 创建下载目录
$downloadDir = "$env:USERPROFILE\Downloads\WPS_Install"
if (-not (Test-Path $downloadDir)) {
    New-Item -ItemType Directory -Path $downloadDir -Force | Out-Null
}

# WPS官方下载链接（备用链接）
$wpsUrl = "https://wdl1.cache.wps.cn/wps/download/ep/WPS2019/WPSOffice_11.8.2.12195.exe"
$outputFile = "$downloadDir\WPSOffice_Setup.exe"

Write-Host "正在从WPS官网下载安装程序..." -ForegroundColor Yellow
Write-Host "下载链接: $wpsUrl" -ForegroundColor Cyan
Write-Host "保存到: $outputFile" -ForegroundColor Cyan

try {
    # 尝试下载
    $progressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $wpsUrl -OutFile $outputFile -ErrorAction Stop
    
    if (Test-Path $outputFile) {
        $fileSize = (Get-Item $outputFile).Length / 1MB
        Write-Host "下载完成！文件大小: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Green
        
        Write-Host "`n正在启动安装程序..." -ForegroundColor Yellow
        Write-Host "请按照安装向导完成安装。" -ForegroundColor Yellow
        Write-Host "建议选择默认安装选项。" -ForegroundColor Yellow
        
        # 启动安装程序
        Start-Process -FilePath $outputFile -Wait
        
        Write-Host "`n安装完成！" -ForegroundColor Green
        Write-Host "现在你可以打开.docx研究报告了。" -ForegroundColor Green
        
        # 检查是否安装成功
        $wpsPath = "C:\Program Files (x86)\Kingsoft\WPS Office\11.8.2.12195\office6\wps.exe"
        if (Test-Path $wpsPath) {
            Write-Host "WPS Office已成功安装到: $wpsPath" -ForegroundColor Green
        } else {
            Write-Host "请检查WPS是否安装成功，可能需要重启电脑。" -ForegroundColor Yellow
        }
    } else {
        Write-Host "下载失败，文件不存在。" -ForegroundColor Red
    }
} catch {
    Write-Host "下载失败: $_" -ForegroundColor Red
    Write-Host "`n请手动下载WPS Office:" -ForegroundColor Yellow
    Write-Host "1. 访问 https://www.wps.cn/" -ForegroundColor Cyan
    Write-Host "2. 点击'立即下载'" -ForegroundColor Cyan
    Write-Host "3. 运行下载的安装程序" -ForegroundColor Cyan
}

Write-Host "`n按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")