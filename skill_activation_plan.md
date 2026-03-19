# 🚀 技能安装与激活计划

## 📊 当前状态分析

### ✅ 已安装且正在运行的技能：
1. **Self-Improving Agent** - 自我改进机制
2. **Summarize** - 新闻摘要功能
3. **Cron/提醒系统** - 定时任务管理
4. **Feishu工具** - 消息发送和文件管理
5. **Web工具** - 新闻收集和网页访问

### ⚠️ 已安装但需要优化的技能：
1. **Agent Browser** - Chrome扩展不可达
2. **Weather** - 已添加到HEARTBEAT，但网络访问有问题

### ❌ 已安装但未激活的技能：
1. **GitHub** - 需要安装`gh`命令行工具
2. **GOG** - 需要Google OAuth配置

### 🔍 未安装的技能（Top 10列表）：
1. **Find Skills** - 技能发现/导航
2. **Ontology** - 知识图谱/结构化记忆  
3. **Skill Vetter** - 技能安全审查
4. **Proactive Agent** - 已通过cron实现功能

## 🎯 立即行动方案

### 阶段1：今天完成（最高优先级）

#### 1. 网页部署到GitHub Pages ✅ 进行中
- ✅ Git仓库初始化完成
- ✅ 代码提交完成
- ⏳ 需要创建GitHub仓库并推送
- ⏳ 需要启用GitHub Pages

**下一步**：运行 `push_to_github.ps1` 脚本完成部署

#### 2. 安装GitHub CLI工具
GitHub技能需要`gh`命令行工具。安装方法：

**Windows安装**：
1. 下载: https://github.com/cli/cli/releases
2. 运行安装程序
3. 验证: `gh --version`

**或使用winget**：
```powershell
winget install --id GitHub.cli
```

#### 3. 优化Weather技能
已添加到HEARTBEAT，但需要解决网络访问问题。替代方案：
- 使用其他天气API
- 或暂时跳过，等网络问题解决

### 阶段2：本周完成

#### 1. 解决Agent Browser连接问题
**问题**：Chrome扩展不可达
**解决方案**：
1. 检查Chrome扩展是否安装
2. 检查OpenClaw Browser Relay扩展状态
3. 检查本地服务端口(18792)

#### 2. 安装Find Skills技能
**当前问题**：clawdhub速率限制
**解决方案**：
1. 等待速率限制解除
2. 或直接从GitHub安装

#### 3. 安装Ontology技能
用于更好的知识管理，替代当前的文件系统。

### 阶段3：长期规划

#### 1. 配置GOG技能
需要Google OAuth配置，用于访问Gmail、Calendar、Drive等。

#### 2. 安装Skill Vetter技能
用于技能安全审查。

#### 3. 优化所有技能配置
定期评估和优化技能使用效率。

## 🔧 具体执行步骤

### 步骤1：完成网页部署
1. 运行 `push_to_github.ps1`
2. 按照脚本提示操作
3. 启用GitHub Pages
4. 测试网站: https://alanwang0809.github.io/news-2026-03-18/

### 步骤2：安装GitHub CLI
```powershell
# 方法1：使用winget
winget install --id GitHub.cli

# 方法2：手动下载安装
# 访问: https://github.com/cli/cli/releases
# 下载最新版 .msi 安装包
```

### 步骤3：测试GitHub技能
安装后测试：
```bash
gh auth login
gh repo view
```

### 步骤4：解决Agent Browser问题
检查步骤：
1. 打开Chrome浏览器
2. 访问: chrome://extensions/
3. 查找"OpenClaw Browser Relay"扩展
4. 确保已启用
5. 点击扩展图标，检查连接状态

### 步骤5：安装缺失技能
等clawdhub速率限制解除后：
```bash
clawdhub install find-skills
clawdhub install ontology
```

## 📋 技能激活检查清单

### 已完成：
- [x] Weather技能添加到HEARTBEAT
- [x] Git用户信息配置
- [x] 新闻网站代码提交

### 待完成：
- [ ] 创建GitHub仓库并推送代码
- [ ] 启用GitHub Pages
- [ ] 安装GitHub CLI工具
- [ ] 测试GitHub技能
- [ ] 解决Agent Browser连接
- [ ] 安装Find Skills技能
- [ ] 安装Ontology技能
- [ ] 配置GOG技能（可选）
- [ ] 安装Skill Vetter技能（可选）

## 🛠️ 故障排除

### 问题1：clawdhub速率限制
**症状**：`Rate limit exceeded`错误
**解决方案**：
1. 等待1-2小时再试
2. 或使用其他安装方法
3. 检查网络连接

### 问题2：Agent Browser不可达
**症状**：`Chrome extension relay is not reachable`
**解决方案**：
1. 检查Chrome扩展安装
2. 检查本地服务端口
3. 重启Chrome浏览器
4. 重启OpenClaw服务

### 问题3：Weather技能网络问题
**症状**：无法访问wttr.in
**解决方案**：
1. 检查网络连接
2. 尝试其他天气API
3. 或暂时禁用天气检查

## 📞 支持资源

### 文档：
- OpenClaw文档: C:\Users\sbjpk\AppData\Roaming\npm\node_modules\openclaw-cn\docs
- 技能文档: 各技能文件夹内的SKILL.md

### 社区：
- OpenClaw Discord: https://discord.com/invite/clawd
- GitHub Issues: https://github.com/openclaw/openclaw/issues

### 工具：
- clawdhub: 技能搜索和安装
- GitHub CLI: GitHub操作
- Chrome扩展: 浏览器自动化

## 🎯 成功标准

### 短期成功（今天）：
1. 新闻网站部署到GitHub Pages并可用
2. GitHub CLI工具安装完成
3. Weather技能在HEARTBEAT中激活

### 中期成功（本周）：
1. Agent Browser问题解决
2. Find Skills和Ontology技能安装
3. 所有Top 10技能状态明确

### 长期成功（本月）：
1. 所有重要技能正常运行
2. 技能使用效率优化
3. 新技能发现和安装流程建立

---

**计划创建时间**: 2026年3月18日  
**计划执行人**: 小龙虾AI伙伴 🦞  
**下次评估**: 2026年3月19日