---
name: reference-traework-channel-experience-fix-20261020
description: TRAE Work（traework 渠道）上的 DeepSeek V4.1 Flash 工具调用与多轮体验修复记录：根因、改法、实测证据与已知边界。改的是 buddy2api 的 traework provider。
type: reference
updated: 2026-10-20
---

# TRAE Work 渠道体验修复（2026-10-20）

> 起因：郭老师反馈「TRAE Work 的 DeepSeek V4.1 Flash，工具调用和多轮对话体验不太好」。

## 一、这个渠道的底层事实

- `traework` 渠道走的是 **TRAE Work 的 agent 会话协议**（`AGENT_API` / `chat_sessions`），
  **没有 OpenAI 式 tools/tool_calls**；带 tools 直接会被上游拒。
- 所以 provider 采用**模拟工具调用**：把工具清单与协议写进 prompt，模型输出
  `<tool_call>{"name":...,"arguments":{...}}</tool_call>`，再由 provider 解析成 OpenAI `tool_calls`。
- 多轮也是模拟：每次调用新建上游会话，把整段历史折叠成一段文本 prompt（`_history_prompt`）。

## 二、查出来的四个根因（都在 `providers/traework/chat.py`）

1. **提示回显污染**：上游偶发把整段任务提示当成助手文本回传。后果：
   - 多轮时客户端收到的是一大段「【对话历史】…【要求】…」，不是回答；
   - 工具提示里自带示例标记，回显后被解析器当成真调用，正文残留 `</tool` 碎片。
2. **截断 JSON 解析失败**：模型偶尔输出 `<tool_call>{"name":"get_weather","arguments":{"city":"郴州"`（缺 `}}`），
   旧逻辑直接判失败，把未闭合标记当正文返回 ⇒ 工具调用「时好时坏」。
3. **长系统提示下模型“自己判断环境”**：系统提示很长时，模型会以「我在 Linux 沙箱、路径不存在」为由
   **拒绝调用工具**（明明工具是客户端执行的）。
4. **没有 tool_choice / 多轮约束**：`tool_choice=required` 不保证调用；历史里的工具调用可能被重复执行。

## 三、改法（commit `1a6c26e`，仅改 traework/chat.py）

- `_strip_prompt_echo()`：剥离整段 prompt 回显 + 按区块特征（【对话历史】/【要求】/【可用工具】）兜底。
- `_loads_repair()`：截断/缺括号/代码围栏的 JSON 自动补齐后解析。
- `_parse_tool_calls()`：标记不完整也能取到调用的兜底；清理 `</tool`、`</tool_call`（缺 `>`）残片；
  无标记但裸 JSON 带 name+arguments 也认。
- 工具协议移到 prompt **最末尾**，并写明：
  - 「工具由客户端在本机执行，不要判断路径/环境是否存在，不要回答无法访问/沙箱限制」；
  - 「用户请求需要工具时，必须先输出 tool_call，不能用自然语言代替」。
- 多轮规则：「历史里的工具调用与结果都已执行完，不要重复调用；只回复最后一条用户消息」。
- `tool_choice=required` / 指定函数时追加「本轮必须调用」。

## 四、实测（走 8787 网关，`traework/deepseek-v4.1-flash`）

| 场景 | 结果 |
|---|---|
| 工具调用连续 3 次 | 3/3 `finish=tool_calls`，`content=None` |
| 一句话要求查两个城市 | 2 个 tool_calls（并行 OK） |
| `tool_choice=required` + 闲聊 | 仍强制发起 1 次工具调用 |
| 大系统提示（约 3K 字符）+ 工具请求 | 正确发起 tool_call（改前会以“沙箱无法访问”拒绝） |
| 多轮：名字 + 截止日 + 工具结果 → 汇总 | 正确复述「项目 Alpha、周五、郴州 18~26℃」 |
| 闲聊但带 tools | 正常文本回答，不误触发工具 |
| 流式工具调用 | 正确输出 `delta.tool_calls` 与 `finish_reason=tool_calls` |

## 五、边界与注意

- 上游仍是 agent 协议：**极少数情况下它可能坚持用自然语言而不是调用工具**；提示已尽量约束，但不能 100% 保证。
- `_strip_prompt_echo` 会删掉回答里原样出现【对话历史】/【要求】等标记的片段（概率极低）。
- 本修复只影响 `traework` 渠道；`workbuddy` / `workbuddy-intl` 有原生 tools，不走这套模拟。
- 修改后需重启 8787 网关才生效（模块级常量与函数）。

## 关联

- 代码：`D:\项目\ai-hub\buddy2api\src\providers\traework\chat.py`
- 网关：`D:\项目\ai-hub\buddy2api`（8787，provider 列表含 traework）
- 测试脚本曾是临时脚本，不落库；复现方法：向 `/v1/chat/completions` 发 `model=traework/deepseek-v4.1-flash` + `tools`
