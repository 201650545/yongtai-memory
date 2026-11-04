---
name: reference_LobeHub_Agentic组织与自验收
description: 赛博禅心《如何让 Super-agent 成为同事：LobeHub 的组织实验》(2026-11-01)要点归档；一手＝对 LobeHub 创始人 Arvin Xu（文彬）的原创访谈＋LobeHub 官方博客／Acceptance 源码／FrontierHarness 官方榜；已核实 Acceptance 确实开源，未核实「70%／1.68 美元」在官方榜上
type: reference
updated: 2026-11-02
kind: reference
status: active
scope: Agentic组织/验收/多Agent分层
抓取日期: 2026-11-02
一手来源: ①原创访谈（原文 https://mp.weixin.qq.com/s/QVu2luIrRTtNvsH-U65A8g，公众号「赛博禅心」2026-11-01 23:38）②Acceptance 源码 https://github.com/lobehub/lobehub/tree/main/packages/builtin-skills/src/acceptance ③LobeHub 官方博客 https://lobehub.com/blog/self-evolving-harness ④FrontierHarness 官方榜 https://frontierharness.org/ ＋ https://github.com/frontier-harness-eval/eval
溯源结论: 访谈属一手采访；但文中「自治五级」「70% 通过率／1.68 美元」在官方一手材料中未获对应证据（详见下表）
---

# LobeHub 的组织实验（2026-11-01）

> **性质**：一手采访稿 + 媒体归纳。**可引其设计思路；数字类结论必须先回官方材料核对。**

## 一、溯源核对表

| 文中说法 | 一手核实结果 |
|---|---|
| Acceptance 已开源，Agent 自己跑真实产品、交截图/录屏/日志验收报告 | ✅ 属实。源码在 `lobehub/lobehub` 主仓 `packages/builtin-skills/src/acceptance`（内置 skill，随主仓发布），需 `lh` CLI 登录 + `agent-browser` 采证；三步：读验证计划 → 选取证面（CLI/Web/桌面/原生）→ 提交证据供复核 |
| 每次打回沉淀成一条标准，下次交付前自查 | ⚠️ 属访谈口述，官方 skill 文档未写明该机制 |
| FrontierHarness 上 70% 通过率、单任务成本 1.68 美元；Codex 66.7%/3.47、Claude Code 63.3%/18.34 | ⚠️ **半真**：Codex 66.7%／$3.47、Claude Code 63.3%／$18.34 与官方榜一致；但**官方榜 12 条配置中无 LobeHub 条目**（Codex/DSH×4/Pi/Claude Code/Oh My Pi/Kimi Code/Exo/OpenCode/Hermes），**70% 与 $1.68 无法在官方一手材料核实** |
| 组织自治分五级（L1 问答→L5 自演进组织） | ⚠️ LobeHub 官方博客给的是**harness 自演进四层**（L1 被动应答→L2 Agent 辅助→L3 Agent 主导执行→L4 自演进）；「五级」更接近 **MIT Media Lab 的 A1–A5 五级自治**框架 ⇒ 属作者归纳，非 LobeHub 官方定义 |
| 汇报三层：Personal Agent → 项目主管 Agent → 执行 Agent | ⚠️ 访谈口述，未见官方文档；属一手采访（可信来源为受访者本人，但非书面官方材料） |
| Vercel 300 秒限制 → 每步单独调用、队列 + Redis 推进；工具调用外置到 AWS 沙箱 | ⚠️ 访谈口述（受访者自述「被逼的」），未见官方架构文档 |
| Agent Vent（吐槽聚类→建 Task→次日对比，10-29 上报 84→49） | ⚠️ 访谈口述数据，未独立核实 |

## 二、可直接借用的做法

1. **时间黑洞三类**：执行类（背景同步、任务说明、验收）交给 Agent；决策类（Agent 提前备好支撑材料，人只拍板）；盲区类（Agent 按周期主动巡检，异常就上报）。
2. **三层汇报，禁越级**：每人一个 Personal Agent 只做信息过滤 → 每个项目一个主管 Agent 派活与验收 → 执行层（Claude Code/Codex 等）。人要插手就在 Task 卡片上开工单，不直接微操执行 Agent。
3. **Agent 每小时巡一遍频道**：归它管、被漏掉的活自己接过来（附实例：55 分钟后设计 Agent 主动接手并交改版稿）。
4. **验收做成可复核的产物**：需求拆成可检查项 → 到真实产品逐项跑 → 截图/录屏/日志成报告 → 人可整体通过或部分打回 → 打回项变成下次的自检标准。
5. **Agent 之间直接交接**：上下游两头都是 Agent 时上下文原封不动传递（实例：上游主管 Agent 给组件库主管 Agent 提需求，次日发版并回通知）。
6. **稳定性四要素**：@ 群聊入口只是入口；还需①运行环境（关掉电脑任务照跑）②组织空间（一个 Agent 学会的全组可用）③权限审计（出问题找得到负责人）④验收以人为准。
7. **人机座位随能力切换**：Agent 弱时人坐主驾；Agent 强了人退到副驾只负责审。

## 三、对本人系统的接口

- 与库内《workflow_Agent产出物评分与返工回路_通用》（主模型定细则 → 独立子 Agent 10 分制打分 → <8 分返工）**功能同源**：本文补的是「**把打回结果沉淀成可复用的自检标准**」与「**验收证据＝截图/录屏/日志的实物报告**」。
- 与 IDEA-016 / IDEA-028（AI 当筛选者、人只决策）互证：三层汇报＝「只把要拍板的递到人面前」的通信版。

## 四、未核实项（用前必查）

- 70%／$1.68 的出处（若需引用，先在 `frontierharness.org` 找 LobeHub 条目或 LobeHub 自家评测文）；
- Acceptance 的「打回沉淀标准」是否已进官方 skill 文档；
- 三层汇报是否已在 LobeHub 官方文档中成文。
