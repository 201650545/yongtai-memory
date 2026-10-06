---
name: workflow-xhs-daily-pipeline-three-tasks
description: 小红书点赞每日管线 A/B/C 的执行口径——入口是 skill 与脚本常量不是记忆；补跑要先冷却；落位即契约（_系统数据 11 个 JSON 勿改名移出）；排障按日志→webbridge→登录态→限流
metadata:
  node_type: memory
  type: 流程
  originSessionId: f969104b-ab73-4eac-a3ef-2a2649f10525
  modified: 2026-09-29
  关联批次: 2026-09-29 memory-work-inventory（本项目 32 份 .md／2 份 SKILL.md）
---

# 每日管线 A／B／C：怎么跑、什么时候别跑

**形状**（不是一个脚本，是三个任务共用一个调度器）：
- **A** 枚举全部点赞并取消旧赞（保留最近若干篇，连续失败 5 次主动终止防风控）
- **B** 对新点赞做点点 v3 深度分析、分析后取消赞，有每日上限，全文落 `b_answers/<note_id>.txt` 并写 `_lark_map.json`
- **C** 旧信息联网时效复核，每日 ≤3 篇，走独立子进程

**入口在 skill，不在记忆**：`D:\Work\小红书点赞分析\.trae\skills\xhs-like-daily\SKILL.md` 自己写着"本文件只是入口与红线，逐步操作以脚本和 docs 为唯一真相源，勿在本文件复制长 SOP（双写会腐烂）"——这条自律和 handbook 的 SSOT 法同源。**要常量就去 `scripts/xhs_like_manager.py` 顶部读，别信任何转述**（含本条）。

**三条最容易踩的执行口径**：
1. **A 跑完别立刻跑 B**：大枚举＋取消会让 B 的读接口被限流（`empty_response`，十几分钟后 bootstrap 失败中止）。补跑 B 前**冷却约 1 小时**，用一次性计划任务延后启动。
2. **登录态过期代码无法绕过**：症状＝个人主页没有"点赞"tab、出现登录遮罩。只能让他在真实 Chrome 扫码/手机重登，**任何脚本绕过尝试都是浪费时间**（这条与"能力问题≠权限问题"是同一类判定）。
3. **多数日子新增为 0 是常态**：比对后无新增就跳过总结与表格更新，直接走收尾清理，回复只写"本次无新增"。别为了有产出而扩大抓取。

**落位即契约**：管线 JSON 统一在 `_系统数据/`（11 个），读写位置常量已全部指向该目录（5 个 py ＋ 2 个 ps1）——**不要改名移出**，移出等于把定时任务的数据库搬走。日报 `reports/`、运行日志 `logs/mgr_YYYY-MM-DD.log`。

**定时任务本体**：`XHS_LikeManager_Daily` 每天 10:17（pythonw 无窗口，仅交互登录时运行、错过开机补跑）。改 `scripts/` 与 `_系统数据/` 必须保证它不断：先 `py_compile`，再用 `--only` ＋ `--quota` 小样本验证。灾备另有 `XHS_WorkBackup_Daily`（每日 11:37 递归镜像 `D:\Work` 到夸克网盘）。

**排障顺序**（固定，别跳）：当天日志末尾 traceback → `kimi-webbridge status`（502/`extension_connected:false` 见 [[调度大脑记忆/教训/lesson_browser_automation_anti_scrape]]）→ 登录态 → 限流冷却 → 点点 DOM/截断问题查 `docs/02 §5` 与 `docs/03`。

## 关联（Work 原文锚点）

| 原文 | sha16 | 位置 |
|---|---|---|
| `D:\Work\小红书点赞分析\.trae\skills\xhs-like-daily\SKILL.md` | `d293488c2a53bc2d` | 任务表 L12-16；怎么跑 L18-24；红线 9 条 L26-36；落位 L38-44；排查顺序 L46-53 |
| `D:\Work\小红书点赞分析\AGENTS.md` | `458097baed69ebc4` | 例外与常量 L17-23（uv Python、10:17 定时任务、lark-cli 路径、JSON 目录已归一） |
| `D:\Work\小红书点赞分析\README.md` | `ed168284dc928dfa` | 脚本工具链与数据资产 L33-34；灾备 L37；目录结构 L51-66 |
