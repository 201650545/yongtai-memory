---
name: feedback-judge-only-frontend
description: 郭老师唯一验收标准=前端能用/转发API可调通/AI搜索可见结果；技术细节我自定；前端问题打包给 Claude Sonnet 5 回答
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-12T01:00:16.127Z
---

郭老师对这个项目的**唯一判断标准**：只看前端（Dashboard 页面）能不能用、只关心「同意转发的 API 能不能调通」「AI 搜索能不能看到结果」。AI 搜索的返回内容他自己不看（那是给 AI 用的）。除此之外的后端/架构技术细节（缓存策略、build 一致性、freshness 规则、失败策略等）都由我自行决策，不用反复拿去问他。

**Why:** 他不想被后端技术选择打扰，只以前端呈现与链路可用性作为验收，认为中间实现是执行层的事。

**How to apply:**
- 技术取舍先自定，倾向让「前端始终能显示、链路始终可用」；只有影响前端呈现、或必须 owner 拍板的业务语义，才用紧凑选项问（见 [[feedback-decision-only-reporting]]）。
- 前端相关问题（UI/渲染/页面 bug）优先打包给 **Claude Sonnet 5** 回答（他认可其前端能力），走高级 AI 问诊流程（见 [[feedback-proactive-improvement]]）。
- AI 搜索集成/网关的验收 = 「能不能返回结果」，不纠结结果内容质量。
