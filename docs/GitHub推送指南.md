# GitHub 推送指南（含 Token 获取教程）

> 本地仓库已就绪（60 文件已提交）。推送需要 GitHub 认证，推荐方案 A：Personal Access Token。

---

## 第一步：生成 Personal Access Token（约 2 分钟）

1. 浏览器打开 GitHub 并登录：https://github.com/login
2. 点击右上角你的**头像** → 选择 **Settings**（设置）
3. 在左侧设置菜单**最底部**，点击 **Developer settings**（开发者设置）
4. 左侧选择 **Personal access tokens** → 点击 **Tokens (classic)**
5. 点击右上角绿色按钮 **Generate new token** → 选择 **Generate new token (classic)**
6. 填写表单：
   - Note（备注）：随便填，如 aicrispr-push
   - Expiration（有效期）：建议选 30 天 或 90 天（够用）
   - Select scopes（权限）**只勾选第一个**：repo（完整仓库权限）
     - 展开后默认包含 repo:status / repo_deployment / public_repo / repo:invite / security_events，不用单独勾
7. 拉到页面底部，点击 **Generate token**（绿色）
8. **立即复制**出现的 token（形如 ghp_xxxxxxxxxxxx，只显示这一次！）

⚠️ 重要：
- token 等同密码，只显示一次，关页面就没了（丢了只能重新生成）
- 不要把 token 粘贴到聊天窗口/文档/代码里（会被泄露）
- 用完可在同一页面点 Revoke 撤销

---

## 第二步：用 token 推送（两种方式任选）

### 方式 1：配置凭据存储（推荐，一次配置永久免密）

在 PowerShell 执行（先建远程仓库，再存 token）：

    cd <你的AI-CRISPR-Design仓库路径>
    # 1) 创建远程仓库（把 <TOKEN> 换成你的 token）
    curl.exe -X POST -H "Authorization: token <TOKEN>" https://api.github.com/user/repos -H "Content-Type: application/json" -d "{\"name\":\"AI-CRISPR-Design\",\"private\":false,\"description\":\"AI-driven CRISPR design system for E. coli cell factories\"}"
    # 2) 推送（首次会弹出窗口/提示输入密码，粘贴 token 即可；之后 Windows 会记住）
    git push -u origin master

### 方式 2：临时用（不存储，每次都要输入）

    cd <你的AI-CRISPR-Design仓库路径>
    git push -u origin master
    # 用户名填 laitygreen
    # 密码粘贴 token（不是登录密码！）

---

## 第三步：验证推送成功

1. 打开 https://github.com/laitygreen/AI-CRISPR-Design 能看到仓库内容
2. 本地执行 git log --oneline 应看到 2 个提交
3. 后续更新：git add -A && git commit -m "说明" && git push

---

## 常见问题

| 问题 | 解决 |
|---|---|
| 提示 Repository not found | 远程仓库还没创建，先执行第二步方式1的第1步 |
| 提示认证失败 401 | token 权限不足或已过期，重新生成并勾选 repo |
| 提示 403 rate limit | API 调用超限，等几分钟或检查 token |
| 忘了 token | 重新生成一个（旧的自动失效） |
| 不想用 token 了 | 网页里 Revoke；Windows 凭据管理器删除 git 条目 |

---

## 备选：不生成 token 的其他方案

- 方案 B：网页手动建仓库（https://github.com/new 建 AI-CRISPR-Design）→ 本地 git push（浏览器自动授权）
- 方案 C：winget install GitHub.cli → gh auth login → gh repo create --source . --push

