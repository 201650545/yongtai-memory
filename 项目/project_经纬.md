---
name: project-经纬
description: 经纬（Jingwei）＝DeepSeek Harness 的黑白无限画布插件（@local/jingwei）。把一次真跑的 DAG 画在右栏，节点/连线/耗时之外不显示别的；真跑由主 AI 发两路 subagent，画布只读 manifest。2026-10-19 深夜状态 active（MVP 可用），插件已装，最新 run 20261019-212601-a41f 验收 10/10。真源 D:\Work\经纬\docs\00-项目总览.md。
metadata:
  node_type: memory
  type: 项目
  created: 2026-10-19
  modified: 2026-10-19
type: project
updated: 2026-10-19
---

# 经纬 · 黑白无限画布插件

> **本条目只补记忆侧的状态与裁定，正文不复制**。项目真源：`D:\Work\经纬\docs\00-项目总览.md`。

## 一句话

DSH 右栏里只有一张黑白无限画布：一次真跑的 DAG（两条并行支路 + 汇总）画成可拖、可平移、可缩放的节点图。除此之外没有 header、没有时间轴、没有详情、没有产物面板。

## 三条原则（仍然钉死）

1. **图是唯一视图真相**：数据真源是 `artifacts/<runId>/` 与会话日志，画布只读 manifest。
2. **单点调度**：真跑只有主 AI 能发起，插件不自己调模型。
3. **视图只读**：画布不直接改运行状态。

## 现状（2026-10-19 22:10）

- `project.yaml` → `status: active`；插件 `@local/jingwei` 已装进 `desktop` profile（symlink 到 `plugin/jingwei`），右栏 tab「经纬」
- 最新真跑 `20261019-212601-a41f`：文案 169.27s ∥ 设计 222.65s，墙钟 222.65s，墙钟÷最慢 1.0000，验收 10/10，视觉自检 PASS
- 文档收敛为 `docs/00~06`（总览/当前状态/架构/画布规范/运行手册/决策/踩坑）
- v1 dashboard 与旧实验、旧脚本、旧文档全部进 `archive/`

## 形态转向（重要）

2026-10-19 深夜，郭老师否掉了 v1 的 dashboard：「只做黑白极简风，不要其他颜色」「直接只保留一个无限画布」「不是什么东西都拿给我看的」。
→ 所有 header / 时间轴 / 节点详情 / 产物 / 验收表删除；配色锁死 `#000`/`#fff`；交互只剩拖节点、拖空白、滚轮缩放、`F`/`0` 复位、`R` 刷新。
裁定见 `docs/05-决策记录.md` D-16~D-18；规范见 `docs/03-画布规范.md`。

## 边界（不做）

不做通用 DAG 编辑器（节点创建/连线编辑/属性面板）／不做实验报告界面／不做多模型调度后端／不做公网服务／不接主题色。

## 下一步

1. 人工确认真实 DSH 右栏观感
2. F3 单路重跑（未重跑那路 hash 不变）
3. token 计数进 manifest
4. 按钮触发真跑（Host 借 `ctx.agents`，交互与费用闸门未定）

## 关联

- 宿主：DeepSeek Harness（profile `desktop`）
- 插件：`@local/jingwei`（Host 路由 `/jingwei/**` + Client 右栏 tab）
- 模型来路：客户端凭据网关（`:8787`，buddy2api 零倍率）、API转发网关（`:3100`，仅补救）
- 项目登记：`D:\记忆\项目清单\projects.yaml` → `local_only` 段「经纬（Jingwei）」
- vault 登记：`D:\Work\元智能\machine\vault_registry.yaml` → 经纬
