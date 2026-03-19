# 🔐 GitHub Personal Access Token (PAT) 生成指南

## 🎯 目的
生成GitHub PAT用于实现**每日新闻完全自动化部署**

## 📋 PAT权限要求
- **仓库访问**: 所有仓库 或 仅Alanwang0809/Alanwang0809.github.io
- **权限**:
  - Contents: Read and write（读写内容）
  - Pages: Read and write（读写Pages）
  - Metadata: Read-only（只读元数据）

## 🚀 生成步骤

### 步骤1：访问GitHub Token设置
1. 打开浏览器
2. 访问: https://github.com/settings/tokens
3. 确保已登录你的GitHub账户 (alanwang0809)

### 步骤2：创建新Token
1. 点击 **"Generate new token"**
2. 选择 **"Fine-grained tokens"**（细粒度令牌）
3. 点击 **"Generate new token"** 按钮

### 步骤3：配置Token信息
#### 基本设置：
- **Token name**: `OpenClaw-News-Automation`
- **Expiration**: 建议选择 "90 days"（90天）或 "No expiration"（无期限）
- **Description**: "用于每日新闻自动生成和部署到GitHub Pages"

#### 仓库权限：
- **Repository access**: 选择 **"All repositories"** 或 **"Only select repositories"**
  - 如果选择后者，添加: `Alanwang0809/Alanwang0809.github.io`

#### 权限设置：
在 **Permissions** 部分，设置以下权限：

##### Repository permissions:
- **Contents**: ✅ Read and write
- **Pages**: ✅ Read and write
- **Metadata**: ✅ Read-only

##### Organization permissions:
- 保持默认（无需设置）

### 步骤4：生成和保存Token
1. 滚动到页面底部
2. 点击 **"Generate token"**
3. **重要**: 立即复制生成的token
4. **安全保存**: 保存在安全的地方，如密码管理器

## ⚠️ 安全注意事项

### 必须做：
1. ✅ 立即复制并保存token
2. ✅ 不要分享给任何人
3. ✅ 定期更新（建议90天）
4. ✅ 仅用于OpenClaw新闻自动化

### 不要做：
1. ❌ 不要将token提交到代码仓库
2. ❌ 不要分享截图包含token
3. ❌ 不要用于其他用途
4. ❌ 不要忘记过期时间

## 🔧 配置到OpenClaw

### 方法A：通过环境变量配置
```bash
# 设置环境变量
setx GITHUB_TOKEN "你的PAT令牌"
```

### 方法B：通过配置文件
创建配置文件：
```json
{
  "github": {
    "token": "你的PAT令牌",
    "username": "alanwang0809",
    "repository": "Alanwang0809.github.io"
  }
}
```

### 方法C：通过脚本参数
在自动化脚本中直接使用。

## 🛠️ 测试PAT有效性

### 测试命令：
```bash
# 测试仓库访问
curl -H "Authorization: token 你的PAT" https://api.github.com/user

# 测试仓库权限
curl -H "Authorization: token 你的PAT" https://api.github.com/repos/Alanwang0809/Alanwang0809.github.io
```

### 预期结果：
- 返回200状态码
- 显示你的用户信息
- 显示仓库信息

## 🔄 自动化流程集成

### 集成后流程：
```
每日08:30 → 收集新闻 → 生成网站 → 使用PAT自动部署 → 发送链接
```

### 自动化脚本使用PAT：
```python
import os
from github import Github

# 从环境变量获取PAT
github_token = os.getenv('GITHUB_TOKEN')

# 连接到GitHub
g = Github(github_token)
repo = g.get_repo("Alanwang0809/Alanwang0809.github.io")

# 自动上传文件
repo.create_file(
    path="news/2026-03-18/index.html",
    message="自动添加新闻网站",
    content=website_content,
    branch="main"
)
```

## 📊 PAT管理建议

### 定期检查：
1. **每月检查**：token是否仍然有效
2. **到期前更新**：提前7天生成新token
3. **权限审查**：确保权限最小化

### 多环境支持：
1. **开发环境**：测试用token
2. **生产环境**：正式用token
3. **备份token**：备用token

### 监控和告警：
1. **使用监控**：监控token使用情况
2. **异常告警**：异常访问告警
3. **使用日志**：记录所有使用记录

## 🚨 故障排除

### 问题1：Token无效
**症状**: 401 Unauthorized
**解决**:
1. 检查token是否过期
2. 检查token是否正确复制
3. 重新生成token

### 问题2：权限不足
**症状**: 403 Forbidden
**解决**:
1. 检查权限设置
2. 确保有Contents和Pages权限
3. 检查仓库访问权限

### 问题3：速率限制
**症状**: 429 Too Many Requests
**解决**:
1. 降低请求频率
2. 使用缓存
3. 优化代码

## 📞 支持

### 生成遇到问题：
1. 截图错误页面
2. 描述具体步骤
3. 发送给我分析

### 配置遇到问题：
1. 提供错误信息
2. 描述配置步骤
3. 发送日志信息

## 🎯 下一步

### 生成PAT后：
1. 发送token给我（通过安全方式）
2. 我配置自动化脚本
3. 测试完全自动化流程

### 完全自动化后：
1. 每日自动收到新闻链接
2. 无需任何手动操作
3. 享受自动化服务

---

**重要性**: 🔐 PAT是实现完全自动化的关键  
**安全性**: ⚠️ 妥善保管，不要泄露  
**用途**: 🚀 仅用于新闻自动化部署  
**支持**: 🦞 小龙虾AI伙伴全程技术支持