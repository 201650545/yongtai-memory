---
name: lesson-丢课根因是工具按文件名取id
description: 一课消失的根因是灌包工具按包文件名词干取 id 造出孤儿行，被按目录口径清理时删掉；id 真源只有包内 manifest 一处
type: lesson
updated: 2026-10-22
kind: rule
status: active
scope: 晨读
---

# 丢课根因：工具按文件名取 id

**结论**：App 侧按 `manifest['lessonId']` 建行，而**灌包工具曾按包文件名词干取 id**，
于是造出「孤儿行」（App 侧没有对应 lesson 的行），再被**按目录口径**的清理逻辑删掉——
表现为「一课消失」。现已统一为取 id 优先级：
**优先 `manifest['lessonId']` → 其次 `id` → 最后文件名词干**。

**判据**：

- **id 的真源只有一处 = 包内 manifest**；工具侧任何取 id 的代码都必须先读包内 manifest，
  **禁止用文件名推 id**。
- 清理「孤儿行」前必须先确认 App 侧确有对应 lesson，否则不要按目录口径批量删。
- 排查丢课先看：manifest 里的 `lessonId` 与 App 库里的行 id 是否**逐字相等**（大小写、前后缀都要比）。

**依据出处**：2026-10-22 晨读丢课排查。
相关但**根因不同**的既有条目（勿混为一谈）：`轮次记录/2026-10-15.md:39`
（catalog 里的 id 与 manifest 的 `lessonId` 不匹配导致「挂接是假的」）；
`项目/project_晨读.md:51-65`（课文数据口径裁定：目录为准、资产不能反定义目录）。
