---
name: project-github-sync
description: GitHub 仓库 english-teaching-production 定位 = 规范/工具/命令/汇报镜像（非成品库），一键双发 publish_all.py 已首次启用
metadata: 
  node_type: memory
  type: project
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-08-11T12:52:12.162Z
---

GitHub 仓库 `github.com/201650545/english-teaching-production`（本地 staging 在 `C:\Users\郭永涛\AppData\Local\Temp\eng-teaching-up`）定位：**生产方法库镜像**——00_格式规范/00_工具/00_总规划（命令+05_汇报）/样例课件/README。学生课件体积大不入库；飞书看板是状态镜像。两者是互补出口，本地 `D:\英语教学` 才是唯一真源。

**一键双发**：`D:\英语教学\00_工具\publish_all.py`（同步三目录 → git commit+push → feishu_sync.py 刷飞书）。2026-08-10 首次启用，推送 71 项积压变更（提交 d918636）。此后交付收尾跑一次即可。过滤规则：00_工具 只入正式工具+词库 JSON，一次性验收脚本（verify_guard_v1.py / verify_LMX_L06_L10.py 等）列入 ONEOFF_TOOLS 排除，`_`/`fix_`/`check_` 前缀不入。

**2026-08-11 本地清理影响**：外部 Agent 清掉了本地 `D:\英语教学\README.md`、`00_工具\analyze_answers.py`、`样例课件\` 整目录（3 件 L01 HTML）。教师决策=**仓库保留、本地不恢复**。`00_工具` 目录结构完整（`ops\publish_all.py`/`feishu_sync.py`、`engine\verify_v2.py` 等子目录均在）。publish_all.py 只增不删，本地清理不传播；README/样例课件无本地源后不会更新，但仓库里仍是 d918636 的旧版，需要时可从 staging 找回。

**给 AI 的前提**：问 GPT/外部 AI 前先 `git pull` 拉最新规范（已写入 README「同步机制」节）。相关：[[project-ai-gateway]] [[workflow-gpt-repo-sync]]
