---
name: end-turn-forward-block
description: 需转发时，每次结尾写约50字、含文件路径的转发块
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-08-05T01:06:23.860Z
---

当一轮结束时有需要郭老师转发给其他 AI 的交付（命令/说明/补充/问题包）时，在回复**最后**固定写一段约 50 字、**含文件路径**的转发块，让他直接复制转发，不用再翻上下文找路径。

**Why:** 郭老师 2026-08-04 明确要求。他做信息中继，需要一键拿到"转给谁、转什么文件"。

**How to apply:** 结尾格式：`**转发：**\`路径\` —— 一句话（发给谁、做什么）。` 只有真需转发时才写，闲聊/纯汇报不写。相关：[[handoff-require-brief-report]]、[[workflow-human-ai-research]]。
