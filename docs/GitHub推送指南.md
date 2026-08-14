# GitHub 推送指南

> 本地仓库已就绪（60 文件已提交）。推送需要 GitHub 认证。

## 方案 A：提供 Personal Access Token（推荐，可自动化）

1. 登录 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)，勾选权限：repo（完整仓库权限）
3. 把 token 发给我（或自行执行下方命令）

    cd C:/Users/lxj19/aaa_bioinfor/AI-CRISPR-Design
    git push -u origin master
    提示输入用户名时填 laitygreen，密码填 token

    或先用 API 创建远程仓库：
    curl -X POST -H 'Authorization: token <TOKEN>' https://api.github.com/user/repos -d '{ name: AI-CRISPR-Design, private: false }'

## 方案 B：网页手动创建（无需 token）

1. 打开 https://github.com/new
2. Repository name: AI-CRISPR-Design
3. 选 Public（或 Private），不要勾选 README/LICENSE/.gitignore（本地已有）
4. Create repository
5. 回到本地执行：

    cd C:/Users/lxj19/aaa_bioinfor/AI-CRISPR-Design
    git remote set-url origin https://github.com/laitygreen/AI-CRISPR-Design.git
    git push -u origin master
    推送时浏览器会弹出 GitHub 登录授权（Windows Credential Manager）

## 方案 C：安装 GitHub CLI（一劳永逸）

    winget install GitHub.cli
    gh auth login   # 浏览器授权
    gh repo create AI-CRISPR-Design --public --source . --push

---

## 推送后检查

- 确认仓库 https://github.com/laitygreen/AI-CRISPR-Design 可见
- 确认 docs/、src/、环境文件齐全
- 之后每次更新：git add -A && git commit -m 更新说明 && git push

