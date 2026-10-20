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

---

## 六、补充（2026-10-20 晚）：根因终于查到 + 两条根治路线被证伪

### 6.1 模型自己说出了为什么绕过协议

长系统提示 + 工具请求实测，模型原话：

> 「说明：我没有名为 `get_weather` 的工具，那段"必须输出 `<tool_call>`"的规约**也不是我的系统指令**，
> 所以我没有按它伪造调用。天气信息我用真实的联网搜索查到了。」

⇒ **根因**：上游 TRAE Work 走的是 **work 模式 agent 会话**（`AGENT_API/chat_sessions`），
agent 自带**真实**搜索/浏览/执行工具。我们只能把工具协议写进 user prompt，
模型因此把它当**不可信的提示注入**——凡是「我自己也能做」的请求（查天气这类），
它优先用自己的真工具，压根不配合模拟协议。

### 6.2 两条「根治」路线都被证伪（探针脚本可复跑）

| 尝试 | 结果 |
|---|---|
| 上游有系统指令字段？ | **没有**。`message.system_prompt` / `custom_instruction` / `agent_instruction` / `session.custom_system_prompt` 四个候选**全部被忽略**（模型照常答「1+1等于几」） |
| 会话 mode 能关掉自带工具？ | **不能**。接口对任何 mode 都返 200，但 `mode=chat` 发消息直接 **500 internal server error**；只有 `work` 可用 |
| 换更听话的上游模型？ | **能！** 见 6.4 |

### 6.3 实际做的两条兜底（commit `ab176d2`）

1. **A 方案 · 能力边界**：tools 请求且 `tool_choice != none` 时，prompt 末尾追加
   「你自带搜索/浏览/执行能力本轮不可用，动作一律交回客户端的 tool_call」
   （不改变 `tool_choice=auto` 的语义）。
2. **B 方案 · 兜底重试**：tools 请求但没解析出 tool_calls 时，**换账号 + 升级提示词再试一次**
   （复用原有账号轮换循环；重试轮允许复用同一账号，因为账号池可能只有 1 个）。

### 6.4 换上游模型 = 真正的杠杆（实测数据）

`scripts/probe_traework_model_compliance.py`（长系统提示 + 工具请求，各 4 次）：

| 上游模型 | 工具调用命中率 |
|---|---|
| **kimi-k3** | **3/4** ✅ |
| deepseek-v4.1-flash（原先默认） | **1/4** |
| qwen-3.7-plus | 1/2 |
| Doubao-Seed-2.1-Turbo | 0/2 |

⇒ 已把 `traework/kimi-k3` 加进网关选定模型（`/admin/selected-models`），
DSH profile 同步后两个 traework 模型都在，**需要工具调用时优先选 kimi-k3**。

### 6.5 另一个坑：上游并发上限

`429 {"code":991502,"reason":"solo_agent_parallel_limit","limit":2}` —— 上游同时只允许
**2 路 agent 会话**。调试/压测时容易撞上，看起来像"渠道挂了"。

## 七、关联

- 代码：`D:\项目\ai-hub\buddy2api\src\providers\traework\chat.py`（修复 `ab176d2`）
- 探针（可复跑）：`buddy2api\scripts\probe_traework_{tools,longsys,session_modes,system_field,system_field2,mode_behavior,model_compliance,kimi_e2e}.py`
- 网关：`D:\项目\ai-hub\buddy2api`（8787，provider 列表含 traework）
- 复现方法：向 `/v1/chat/completions` 发 `model=traework/kimi-k3` + `tools`
