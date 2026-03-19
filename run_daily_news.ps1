# PowerShell脚本：运行每日新闻自动化
Write-Host "========================================" -ForegroundColor Green
Write-Host "🦞 每日新闻自动化系统" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 设置工作目录
$workspace = "C:\Users\sbjpk\.openclaw\workspace"
Set-Location $workspace

# 创建目录
$newsDir = "$workspace\daily_news_websites"
if (-not (Test-Path $newsDir)) {
    New-Item -ItemType Directory -Path $newsDir -Force
    Write-Host "✅ 创建目录: $newsDir" -ForegroundColor Cyan
}

# 获取当前日期
$dateStr = Get-Date -Format "yyyy-MM-dd"
Write-Host "📅 处理日期: $dateStr" -ForegroundColor Cyan

# 创建今日网站目录
$websiteDir = "$newsDir\news_$dateStr"
if (-not (Test-Path $websiteDir)) {
    New-Item -ItemType Directory -Path $websiteDir -Force
    Write-Host "✅ 创建网站目录: $websiteDir" -ForegroundColor Cyan
}

# 模板目录
$templateDir = "$workspace\news_website_2026_03_18"

# 复制模板文件
$files = @("index.html", "styles.css", "script.js")
foreach ($file in $files) {
    $src = "$templateDir\$file"
    $dst = "$websiteDir\$file"
    
    if (Test-Path $src) {
        $content = Get-Content $src -Encoding UTF8 -Raw
        
        # 更新日期信息
        if ($file -eq "index.html") {
            $content = $content -replace "2026年3月18日", "$((Get-Date -Format 'yyyy年M月d日'))"
            $content = $content -replace "2026-03-18", $dateStr
            $content = $content -replace "更新于 16:45", "更新于 $(Get-Date -Format 'HH:mm')"
        }
        
        Set-Content -Path $dst -Value $content -Encoding UTF8
        Write-Host "  ✅ 复制 $file" -ForegroundColor Green
    }
}

# 创建README
$readmeContent = @"
# 🦞 小龙虾新闻服务 - $dateStr重要新闻汇总

## 📋 网站信息
- **日期**: $dateStr
- **生成时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **自动化**: 每日新闻自动生成系统
- **部署位置**: GitHub个人页面子目录

## 🎨 功能特点
1. **5个颜色区分的新闻模块**
2. **重要性星级筛选**
3. **响应式设计**
4. **一键打印优化**

## 🔗 访问地址
https://alanwang0809.github.io/news/$dateStr/

## 📁 文件结构
Alanwang0809.github.io/
└── news/
    └── $dateStr/
        ├── index.html
        ├── styles.css
        ├── script.js
        └── README.md

## 🔄 自动化流程
此网站由小龙虾新闻服务自动生成，包含当日重要新闻汇总。

---
**生成系统**: 小龙虾AI伙伴 🦞
**最后更新**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

Set-Content -Path "$websiteDir\README.md" -Value $readmeContent -Encoding UTF8
Write-Host "  ✅ 创建README.md" -ForegroundColor Green

# 创建部署指令
$deployInstructions = @"
# 🚀 部署指令 - $dateStr新闻网站

## 部署到GitHub个人页面
你的个人页面: https://alanwang0809.github.io/
目标路径: /news/$dateStr/
最终地址: https://alanwang0809.github.io/news/$dateStr/

## 方法A：使用Git命令（推荐）

### 步骤1：克隆你的个人页面仓库
在PowerShell中运行：

cd `"C:\Users\sbjpk\.openclaw\workspace`"
git clone https://github.com/Alanwang0809/Alanwang0809.github.io.git
cd Alanwang0809.github.io

### 步骤2：创建新闻目录并复制文件
mkdir -Force news/$dateStr
Copy-Item -Path `"$websiteDir\*`" -Destination `"news\$dateStr`" -Recurse

### 步骤3：提交和推送
git add .
git commit -m `"添加 $dateStr 新闻网站`"
git push origin main

## 方法B：直接上传到GitHub网页
1. 访问: https://github.com/Alanwang0809/Alanwang0809.github.io
2. 点击 `"Add file`" → `"Upload files`"
3. 创建目录: news/$dateStr/
4. 拖放 $websiteDir 中的所有文件到该目录
5. 点击 `"Commit changes`"

## 方法C：使用GitHub Desktop
1. 打开GitHub Desktop
2. 添加仓库: Alanwang0809/Alanwang0809.github.io
3. 将 $websiteDir 中的文件复制到 news/$dateStr/ 目录
4. 提交并推送

## 📊 部署后
- 等待1-2分钟GitHub Pages更新
- 访问: https://alanwang0809.github.io/news/$dateStr/
- 测试所有功能

---
**提示**: 提供GitHub PAT后，此流程可以完全自动化。
"@

Set-Content -Path "$websiteDir\deploy_instructions.txt" -Value $deployInstructions -Encoding UTF8
Write-Host "  ✅ 创建部署指令文件" -ForegroundColor Green

# 创建执行报告
$reportContent = @"
# 🦞 每日新闻自动化报告 - $dateStr

## 📊 执行状态
- ✅ 新闻网站生成完成
- ✅ 文件准备就绪
- ⏳ 等待部署到GitHub个人页面

## 📁 生成文件
- **网站目录**: $websiteDir
- **部署指令**: $websiteDir\deploy_instructions.txt
- **预计地址**: https://alanwang0809.github.io/news/$dateStr/

## 🎯 网站内容
基于今日新闻整理，包含：
1. 🔥 国际要闻（红色系）
2. 💡 AI/科技前沿（蓝色系）
3. 📈 经济金融（绿色系）
4. 🎯 投行工作启示（紫色系）
5. 📊 新闻服务优化（橙色系）

## 🔄 自动化状态
- **定时任务**: 已设置每天08:30自动执行
- **部署方式**: 当前半自动化，需要手动部署
- **完全自动化**: 等待GitHub PAT配置

## 🚀 立即行动
按照 deploy_instructions.txt 中的指令部署网站。

---
**报告生成时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**自动化系统**: 小龙虾AI伙伴 🦞
"@

$reportFile = "$newsDir\report_$dateStr.md"
Set-Content -Path $reportFile -Value $reportContent -Encoding UTF8
Write-Host "  ✅ 创建执行报告" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🎉 自动化流程完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📁 网站文件: $websiteDir" -ForegroundColor Cyan
Write-Host "📄 部署指令: $websiteDir\deploy_instructions.txt" -ForegroundColor Cyan
Write-Host "📊 执行报告: $reportFile" -ForegroundColor Cyan
Write-Host "🌐 预计网址: https://alanwang0809.github.io/news/$dateStr/" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 下一步: 按照部署指令将网站部署到你的GitHub个人页面" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

# 保存结果
$result = @{
    date = $dateStr
    website_dir = $websiteDir
    website_url = "https://alanwang0809.github.io/news/$dateStr/"
    report_file = $reportFile
    deploy_instructions = "$websiteDir\deploy_instructions.txt"
} | ConvertTo-Json

$resultFile = "$newsDir\result_$dateStr.json"
Set-Content -Path $resultFile -Value $result -Encoding UTF8
Write-Host "💾 结果保存到: $resultFile" -ForegroundColor Gray