---
name: lesson_小红书发布_标签要active_正文用pmViewDesc_草稿在本地
description: 小红书图文笔记自动化的三个硬坑：标签非active时键盘事件全丢（正文断行、话题下拉都失效）、ProseMirror要用pmViewDesc的tr.split拆段、草稿存在浏览器本地IndexedDB而非服务端。
type: lesson
updated: 2026-10-21
kind: rule
status: active
---

# 小红书发布三坑（2026-10-21 实测）

## 1. 标签不是 active ⇒ 键盘事件全部丢失

`opencli browser <S> tab list` 会给出每个标签的 `active` 标记。**非 active 的标签
`document.visibilityState === 'hidden'`**，Chrome 直接丢弃键盘事件：

- `opencli browser <S> keys Enter` 在 ProseMirror 编辑器里**不产生段落**（实测插入后 HTML 仍是 `<p>AAABBB</p>`，行粘在一起）；
- 话题联想下拉不出现（合成 `keyup` 没人接）。

**正解**：每次操作前先 `tab select <pageId>` 把自己的标签置 active，之后
`document.hasFocus()` 才是 true。opencli v1.8.8 的 `eval` **没有 `--tab` 定向**，
只能打活跃标签 ⇒ 抢标签的根因就在这里。

## 2. 正文断行要走 ProseMirror 自己的 API

`document.execCommand('insertText')` 能插字，但断行要靠：

```js
const el = document.querySelector('.ProseMirror');
const view = el.pmViewDesc;                     // ProseMirror 把 view 挂在 DOM 上
view.dispatch(view.state.tr.split(view.state.selection.from));   // 拆段
view.dispatch(view.state.tr.insertText(txt, view.state.selection.from)); // 插字
```

兜底顺序：`pmViewDesc` → `execCommand('insertParagraph')` → 物理 Enter。

## 3. 草稿存在浏览器本地，不在服务端

页面原文：「草稿存储于当前使用的浏览器本地，在清除浏览器数据时会被删除」。
实际落在 **IndexedDB `draft-database-v1`**，图文笔记在 store `image-draft`，
每条记录对应页面上的 `div.draft-item[data-draft-id][data-draft-type]`。

- UI 的「删除」按钮：派发完整指针序列（pointerdown→mouseup→click）仍不稳；
  直接 `indexedDB` 删记录 + 刷新最干脆。
- ⚠️ **删之前必须先验证标题字段**：标题在**嵌套字段**里（顶层 `v.title` 取不到），
  白名单匹配会全部落空 ⇒ **一条没留、删光**。批量删前先打印计划删除/保留清单并核对数量。

## 附：编辑器与组件区的出现时机

- **文字编辑器、标题栏、「添加组件」区，只有在图片上传成功之后才出现**。
  没传图就找 `.ProseMirror` 会得到 `no-editor`。
- **PDF 附件的 file input 要先点开「添加组件」区**才存在（`accept` 含 `.pdf`）。
  挂好后校验页面文本里出现了 PDF 文件名（读 `input.files.length` 不可靠，
  站点重渲染后拿到的是已脱离文档的旧节点，会读出 0）。

## 相关

- 完整流程与实现：`<技能库>\xhs-ops\components\xhs-note-publish\SKILL.md`
- 本轮实操脚本：`D:\Work\English-Content-Factory\02_Projects\HN-ENGLISH-666\06_templates\_publish_note.py`
