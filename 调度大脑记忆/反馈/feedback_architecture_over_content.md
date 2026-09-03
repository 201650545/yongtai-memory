---
name: feedback-architecture-over-content
description: 郭老师的工作哲学——项目架构比内容重要，架构用最先进模型把关、内容用性价比模型执行，官网连接器读 GitHub 省 API 钱
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-10T16:12:41.722Z
---

郭老师设置飞书 DataHub 的根本目的：让 ChatGPT 官网 / Anthropic 官网通过 **GitHub 连接器** 直接读取飞书导出的公开数据，最先进模型帮他优化多维表格和项目——用官网订阅的现成连接器，避免为最先进模型的昂贵 API 每次调用烧钱。

**Why:** 普通人做项目，**架构安排比具体内容更重要**。架构（结构、数据流、字段设计、规范）错一点全盘重来，必须用最先进模型把关；具体内容（文字、填充、批量执行）量大且便宜，用性价比模型操作即可。

**How to apply:**
- 凡是**架构/规范/方案/结构**级工作 → 按最高标准认真做，不偷懒、不省成本（先进模型、仔细规划、可反复打磨）。
- 凡是**执行/内容/批量**级工作 → 交给执行 Agent + 性价比模型跑（见 [[feedback-role-division]] 分工边界）。
- 多利用 **GitHub 作为数据桥**：数据导到 GitHub Pages 公开 JSON，AI 工具（官网/镜像）经连接器读取即可介入，不必绕 API。
- 关联：[[project-ai-gateway]]（多引擎 AI 搜索/网关是"性价比模型"的载体）、[[workflow-human-ai-research]]（人机互查方法）。
