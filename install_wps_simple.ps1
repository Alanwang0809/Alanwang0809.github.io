Write-Host "=== WPS Office 安装程序 ===" -ForegroundColor Green
Write-Host ""

# 检查是否已安装WPS
Write-Host "检查是否已安装WPS Office..." -ForegroundColor Yellow
$wpsInstalled = $false

# 检查常见安装路径
$wpsPaths = @(
    "C:\Program Files (x86)\Kingsoft\WPS Office",
    "C:\Program Files\Kingsoft\WPS Office",
    "$env:ProgramFiles\Kingsoft\WPS Office",
    "$env:ProgramFiles(x86)\Kingsoft\WPS Office"
)

foreach ($path in $wpsPaths) {
    if (Test-Path $path) {
        Write-Host "发现WPS安装目录: $path" -ForegroundColor Green
        $wpsInstalled = $true
        break
    }
}

if ($wpsInstalled) {
    Write-Host "WPS Office 已经安装！" -ForegroundColor Green
    Write-Host "你可以直接打开.docx文件了。" -ForegroundColor Green
    Write-Host ""
    Write-Host "按任意键退出..." -ForegroundColor Gray
    $null = Read-Host
    exit
}

Write-Host "未找到WPS Office，开始安装..." -ForegroundColor Yellow
Write-Host ""

# 创建下载目录
$downloadDir = "$env:USERPROFILE\Downloads\WPS_Install"
if (-not (Test-Path $downloadDir)) {
    New-Item -ItemType Directory -Path $downloadDir -Force | Out-Null
    Write-Host "创建下载目录: $downloadDir" -ForegroundColor Cyan
}

# 尝试下载WPS
$wpsUrl = "https://wdl1.cache.wps.cn/wps/download/ep/WPS2019/WPSOffice_11.8.2.12195.exe"
$outputFile = "$downloadDir\WPSOffice_Setup.exe"

Write-Host "正在下载WPS Office..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Yellow

try {
    # 设置进度条不显示
    $ProgressPreference = 'SilentlyContinue'
    
    # 下载文件
    Invoke-WebRequest -Uri $wpsUrl -OutFile $outputFile
    
    if (Test-Path $outputFile) {
        $fileSize = (Get-Item $outputFile).Length / 1MB
        Write-Host "下载完成！文件大小: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "正在启动安装程序..." -ForegroundColor Yellow
        Write-Host "请按照安装向导完成安装。" -ForegroundColor Yellow
        Write-Host "建议选择默认安装选项。" -ForegroundColor Yellow
        
        # 启动安装
        Start-Process -FilePath $outputFile -Wait
        
        Write-Host ""
        Write-Host "安装完成！" -ForegroundColor Green
        Write-Host "现在你可以打开桌面上的.docx研究报告了。" -ForegroundColor Green
        
        # 验证安装
        Start-Sleep -Seconds 2
        $wpsExe = Get-ChildItem -Path "C:\" -Recurse -Filter "wps.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($wpsExe) {
            Write-Host "WPS Office 已成功安装到: $($wpsExe.FullName)" -ForegroundColor Green
        }
        
    } else {
        Write-Host "下载失败！" -ForegroundColor Red
    }
} catch {
    Write-Host "下载或安装过程中出错: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "请手动安装WPS Office:" -ForegroundColor Yellow
    Write-Host "1. 访问 https://www.wps.cn/" -ForegroundColor Cyan
    Write-Host "2. 点击'免费下载'" -ForegroundColor Cyan
    Write-Host "3. 运行下载的安装程序" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = Read-Host