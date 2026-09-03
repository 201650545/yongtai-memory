---
name: claude-scheduler-brain
description: Claude Code 是 ai-resource-hub 的调度大脑（唯一窗口）；三项同步打通、分配链路验证、调度规范文档位置
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-31T07:15:27.452Z
  originSessionId: 8ee5c1ea-99c5-4cbe-bf2c-52824ee32254
---

**Claude Code = ai-resource-hub「AI 自助资源运营体系」的调度大脑（统一入口）**（用户 2026-08-30 托付：「我只在这个窗口跟你对话了，资源你来分配」）。

- **调度接入规范**：`D:\ai-resource-hub\docs\Claude调度大脑_接入规范_2026-08-30.md`（资源库地图/查库命令/分配规则/三端同步/验收）。
- **资源库（配置真源）**：飞书多维表格 Base `StmDbTXQWaujshs9NpIc3UFpnAc`（9 表）。读用 lark-cli：`LARK="node $HOME/AppData/Roaming/npm/node_modules/@larksuite/cli/scripts/run.js"`；模型资源总表 `tbl5ONs0gzE7I5xI`（唯一真表）/能力规格 `tbllAPtPd68uDTTj`/实例 `tbl8bKuwqP0Wl4d1`/账号 `tblsrXWXX8GQ9hx4`。
- **分配规则**：免费/低价优先（路由优先级升序）、同 routing_group 轮换不换模型、额度到点停、优先走 :3100 已编排组、测试用免费模型、quarantined（cap-aliyun-01）不选。
- **三项同步**：`cd /d/ai-resource-hub/sync && python sync_all.py`（GitHub↔本地 双向 + 飞书导出 CI 托管）。2026-08-30 修复 ai-hub-memory pre-commit 阻塞（5 项目 STATE 归档到 archive/projects/<p>/2026/ + ROUTER 登记 + CHANGELOG DROP），**三端同步全绿**。
- **分配链路已验证**：:3100 调 deepseek-free 成功路由到实际渠道返回。**真实委派已验证**（2026-08-30）：`subagent.py` 翻译任务→deepseek-free 返回准确译文；`--model fast` 兜底→正常返回。A 类可放心委派简单/重复任务。
- **统一派发入口 dispatch.py**（用户 2026-08-31 拍板「三级派发」，D-GLOBAL-20260831-01）：`python D:\项目\services\dispatch.py "任务" [--tier A|B|C] [--via trae|qoder] [--file ..] [--sys ..] [--cwd ..]`。**A 级·免费模型**（纯文本：总结/命名/翻译/分析→subagent.py→:3100 deepseek-free/fast，只读）；**B 级·程序 Agent**（写码/写文件/批处理→trae-solo 默认锁 DeepSeek V4 Flash 正式版、备选 qoder CLI，目录感知可读写）；**C 级·浏览器**（问诊/评审/网页操作→opencli）。**付费边界：默认全免费，绝不直呼付费模型；`--paid` 仅用户显式指定**。已实测：A 级两次真实调用通过（含附文件+sys）、TRAE status Connected + history 有任务。
- **子 Agent 委派机制**（用户 2026-08-30「网关模型作为子 Agent」）：`python D:\项目\services\subagent.py "任务" [--model fast] [--file 路径] [--sys 提示]`。**A 类只配两个模型名**：`deepseek-free`（DeepSeek 全链，网关排序=魔塔免费125次/天→免费快→慢→opencode 付费垫底）、`fast`（各渠道免费集合）。**测试禁忌：不乱测**（部分平台已充值，测到高级模型浪费钱，只走编排名）。去掉了 glm-5.2（用不了）/qwen3.8-flash（额度不明）。
- **B 类 Agent 程序配置**（用户 2026-08-30 拍板）：Trae Work=DeepSeek V4 Flash 正式版（锁）；豆包=**豆包 2.1 turbo** + 工作模式（已开）+ 思考低（2026-08-30 已调好）；Qoder=千问3.8 flash。
- **桌面执行器**：Trae 全自动对话（opencli trae-solo open-task/send）；**豆包已接入**（opencli doubao-app，CDP 9225，需 `OPENCLI_CDP_TARGET="doubao://doubao-chat/chat"`；2026-08-30 修 adapter——新版输入框是 contenteditable tiptap，utils.js injectTextScript 改 selection+execCommand 注入；**ask 提取截断已修**：新版 textEl 无 `div[dir]`、indicator 在 textEl 外，poll 中途误判完成——ask.js 改文本稳定检测（done 后连续 2 次相同才返回），实测完整回复）；**Qoder 走官方 CLI**（2026-08-30 用户提示有 CLI，查实 `@qodercn-ai/qoderclicn` 已装，但 `qoder` 命令因 `~/.real/.bin/node` 失效需用 system node 调 `bundle/qoderclicn.js`）：`python D:\项目\services\qoder_cli.py "任务" [--cwd 目录] [--sys 提示] [--model]`，底层 `qoderclicn -p` 非交互一次出结果，完整 agent 带工具/目录感知（实测翻译+读 git status 都准）。**取代旧 opencli qoder DOM adapter**（QODER_TURNS_JS 提取器/排队等待/会话清理都不再维护）。模型侧排队照旧（千问3.8-flash），超时默认 300s。Antigravity 接入通但 AI 报错（Google RemoteControl 代理 empty hostname）；QoderWork/WorkBuddy 未接入（QoderWork 强制随机 CDP 端口不兼容 opencli 固定端口；WorkBuddy 需 cmd 启动传参，iframe 结构复杂，均待定）。关联 [[trae-solo-opencli-control]] [[project-ai-resource-hub]]。

**How to apply:** 用户在本窗口给任务 → 查资源库自主分配资源执行 → 产出回写飞书/GitHub → 跑 sync_all.py 三端同步。关联 [[feedback-on-demand-orchestration]] [[feedback-model-policy]]。
