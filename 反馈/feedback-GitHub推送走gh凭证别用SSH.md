---
name: feedback-GitHub推送走gh凭证别用SSH
description: 本机推 GitHub 的正确通路是 gh CLI 的 HTTPS 凭证，不是 SSH 钥匙（SSH 钥匙在但 GitHub 侧没认，会 Permission denied publickey）
metadata:
  node_type: memory
  type: feedback
  created: 2026-10-20
type: feedback
updated: 2026-10-20
kind: fact
status: active
---

# GitHub 推送：走 `gh` 的 HTTPS 凭证，别走 SSH

## 症状

- `git push` 报 `git@github.com: Permission denied (publickey)`；
- 但本机 `~/.ssh/id_ed25519` **确实存在**（419 字节）⇒ 看起来"钥匙有了"，实际 GitHub 侧没认这把钥匙；
- 容易误判成"缺凭证，要去找用户要"。

## 真相（2026-10-20 实测）

**凭证早就有了，只是不在 SSH 那条路上。**

```powershell
gh auth status
# github.com
#   ✓ Logged in to github.com account 201650545 (keyring)
#   - Active account: true
#   - Git operations protocol: https
#   - Token scopes: 'delete_repo', 'gist', 'read:org', 'repo', 'workflow'
```

`gh` 的 token 存在 **Windows keyring**（不在 `hosts.yml` 明文），scope 含 `repo` ⇒ 读写都够。

## 正确推法（不改动仓库 remote 配置）

```powershell
git -C <repo> -c "credential.helper=!gh auth git-credential" push https://github.com/<owner>/<repo>.git <branch>:<branch>
```

一次实测：`8301009..7a0a686  main -> main`，exit=0。

## 配套坑

- `opencli browser` 打开 GitHub 会跳登录页 ⇒ **浏览器 profile 里没登录 GitHub**。
  这**不代表没有凭证** —— 先查 `gh auth status`，别急着让用户登录。
  浏览器没登录时，用 `gh` 这条路反而是通的。
- `gh` 的 token 在 keyring ⇒ **不能**从 `hosts.yml` 读出明文，脚本里要用就用 `gh auth git-credential`。
- 推之前先 `git ls-remote` 同一 URL 验证连通（只读，不改任何东西）。

## 关联

- 反馈机制见 `C:\Users\郭永涛\AGENTS.md` 第 12 条「拿 API key 这件事不要甩给郭老师」——
  本条是它的 **GitHub 专项落地**：凭证已在 `gh` 里，Agent 自己就能推。
- 2026-10-20 实例：经纬 public 仓 v3.2 推送（`D:\小浣熊\jingwei-public` → `201650545/jingwei-public`）。
