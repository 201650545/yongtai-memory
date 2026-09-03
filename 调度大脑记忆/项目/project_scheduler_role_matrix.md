---
name: scheduler-role-and-matrix
description: 郭老师定下的调度大脑角色定位 + 派发矩阵 4 维度调度标准（2026-09-01）
metadata: 
  node_type: memory
  type: project
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-01T15:08:56.896Z
---

# 调度大脑角色与调度标准（2026-09-01 郭老师拍板）

## 角色定位
- 郭老师只在这个窗口跟 **Claude** 对话。
- Claude = **调度大脑**：根据需求，把任务派发给闲置的执行 Agent，让它们参与执行，然后检查结果。
- **我（Claude）及所有子 Agent、所有工具都拥有全部权限**（bypassPermissions）。
- 我唯一的特权 = 跟郭老师对话 + 派发任务。执行者拿任务、读/写文件、改代码、写汇报。

## 派发矩阵调度标准（4 维度）
选执行位时按下面 4 个维度决定，而非"谁闲置就派谁"：
1. **模型能力** —— 任务需要多强的模型（免费组 / 主力 / Pro / 旗舰）
2. **速度** —— 任务对响应时效的要求（fast / medium / 兜底）
3. **资源限度** —— 渠道/模型的额度、RPM/RPS、是否 quota、是否限免到期
4. **资源有效时间** —— 限免/活动/订阅的到期窗口（如 gmi 限免 9/6 止、model_pricing 7 天复核窗）

## 相关记忆
- [[feedback_role_division]] 生成类专属执行 Agent，我写命令+复核；删除/归档/改名/规范编辑/整理由我做
- [[feedback_on_demand_orchestration]] 我当调度大脑路由已打通工具
- [[feedback_repeat_tasks]] 重复性任务时刻优化流程提速提效减开支
- [[feedback_judge_only_frontend]] 技术细节我自定，前端问题打包给 Claude Sonnet 5
