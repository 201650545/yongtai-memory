# {项目名}（README 模板）

> 使用说明：复制本文件到新项目根 README.md，替换全部 {} 占位后删除本注释块。目标：空上下文的 AI 在 30~60 秒内知道去哪找答案。

## 这是什么

{一句话} + {2~3 段说明}

## 当前状态（As of {YYYY-MM-DD}）

- 阶段：{阶段}
- 当前重点：{重点}
- 最近重大变化：{变化}
- 详细任务状态：docs/01-任务看板.md

## Source of Truth

- 项目总览：docs/00-项目总览.md
- 任务状态：docs/01-任务看板.md
- 资产状态：docs/02-资产清单.md
- 项目规格：docs/03-规格与规范.md

## 依赖规范

- handbook v1.1：https://github.com/201650545/handbook
- 项目 override：docs/03-规格与规范.md

## 给 AI / Agent 的读取顺序

1. 本 README → 2. docs/00 总览 → 3. tasks / assets / spec → 4. 需要时查 handbook

## 不要假设

- GitHub 内容可能比本地晚，以文档内时间戳为准
- 成品资产不进仓库；资产清单之外的文件不视为正式资产
