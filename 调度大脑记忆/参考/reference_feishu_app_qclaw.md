---
name: feishu-app-qclaw
description: ai-resource-hub 公开数据桥用的飞书应用 = qclaw(cli_a933ead8cdf85ccc)，2026-08-11 实测确认有 base 权限
metadata: 
  node_type: memory
  type: reference
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-11T14:24:56.822Z
---

**ai-resource-hub 公开数据桥的飞书应用（已确认，2026-08-11）：**

- 应用名 **qclaw**，App ID `cli_a933ead8cdf85ccc`，品牌 feishu，飞书个人版 Production app，状态 Enabled。
- 应用 owner 用户 郭樂（ou_1efa2e5bb895820a8db4e8c6ba0d7232）。
- **实测有 base 权限**：`lark-cli base +table-list --base-token "StmDbTXQWaujshs9NpIc3UFpnAc" --as bot` 列出全部 6 表（工具资产明细表/资源能力规格表 21 条/资源实例表 21 条等）。
- 凭据在 GitHub Actions Secrets：`FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_BASE_TOKEN`（**值绝不写入文件/仓库/聊天**）。
- 开发者后台「凭证与基础信息」页：https://open.feishu.cn/app/cli_a933ead8cdf85ccc/baseinfo（显示密钥需点眼睛图标，勿点「重置」）。
- 注意：旧记忆/文件曾误记 cli_a923220b38f89cb1（龙虾1号）——那是另一个应用，**数据桥用的是 qclaw**。

相关：[[feedback-browser-session]] [[project-ai-gateway]]
