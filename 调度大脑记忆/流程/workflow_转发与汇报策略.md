---
name: workflow-转发与汇报策略
description: 郭老师定的转发/汇报规矩：结尾转发块格式、只报待决策事项、交付必回写、交接带简短汇报
metadata:
  node_type: memory
  type: workflow
  created: 2026-09-22
---

# 转发与汇报策略（郭老师历次口令汇总）

## 一、结尾转发块（每次任务收尾时）

- **什么时候写**：任务产出需要郭老师转发给别的工具/Agent/人时，当次回复结尾固定附一条。
- **格式要求**：约 50 字、一句话说清「做了什么 + 怎么用（调用方式/端点）+ 文件路径（真源文档）」，方便直接复制转发。
- **示例**：
  > 方舟额度每日自动盘点已上线（ArkQuotaScan 每天10:17，opencli抓控制台→快照→回写警戒闸门→破线写警报日志），首扫45模型已入档。真源：D:\项目\ai-hub\search_gateway\渠道编排规则.md
- **不要**写成流水账；不写「我做了 ABC 三个步骤」；只写接收方需要知道的事实。

## 二、汇报纪律

| 规矩 | 内容 | 来源 |
|---|---|---|
| **只汇报待决策事项** | 已完成的工作不反复汇报；被问时只给「需要决策的选项」让他拍板，用 AskUserQuestion 或紧凑选项 | feedback_decision_only_reporting |
| **做完即完结** | 正在做的任务一定要完结再进下一个，不留历史问题；多任务按顺序推进 | feedback_task_completion |
| **别反复问** | 小决策自己办或问 GPT 镜像商量；除非非常重大/破坏共享运行时才停手问郭老师 | feedback-stop-nagging-route-to-gpt |
| **汇报接收即回写** | 子 Agent 交付汇报当日，调度大脑必须回写 STATE/CHANGELOG（9-3 漏读反例） | feedback_report_receive_rule |
| **交接需简短汇报** | 派任务给外部执行 AI 时，须要求其完成后写简短汇报（模块×验收项/变更清单/验证/已知偏差） | handoff_require_brief_report |

## 三、给郭老师的选项格式

- 紧凑选项（A/B/C），每项一句话说清代价与收益；
- 推荐项放第一个并标注「(Recommended)」；
- 技术细节不进选项，进正文或文档。

## 四、任务完结时的档案四写（收尾清单）

1. `search_gateway\渠道编排规则.md`（渠道规则唯一真源）
2. `ai-hub-memory\projects\ai-resources\CHANGELOG.md`（当日流水）
3. Obsidian 本库（项目时间线 + 策略文章）
4. Claude 内部记忆（~/.claude .../memory/）

关联 [[workflow_调度大脑交接手册]] [[workflow_网关安全防扣费策略]]
