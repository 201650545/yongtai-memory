---
name: lesson_多行消息只发第一行_告警静默失效
description: Windows shell=True 传多行正文会在第一个换行处截断——飞书只收到标题、看起来发送成功，实际告警内容全被吞；修法是绕过 shell 直接调 node 入口
type: lesson
updated: 2026-10-21
kind: rule
status: active
---

# 教训：多行消息只发出第一行，而且**看起来完全成功**

> 2026-10-21 11:13 郭老师反馈：「我的飞书只收到了这样一条消息」（只一行标题）。

## 一、症状

飞书收到的是**消息的第一行**（标题），**正文全部消失**。
而发送脚本返回的是 `ok=true` ＋ 正常的 `message_id` ⇒ **没有任何报错**。

## 二、根因

```python
subprocess.run([LARK_CLI] + args, shell=True, ...)   # ← 错
```
- `shell=True` ⇒ 参数交给 **cmd.exe 解析**；
- **Windows 命令行解析在第一个换行处截断** ⇒ `--text "标题\n正文1\n正文2"` 只有标题被送出；
- 后面的行被 cmd 当成**新命令**（通常报"不是内部或外部命令"并丢弃）。

⇒ **凡是多行告警都只显示标题**：能力体检告警、契约自检 FAIL 告警、每日本质精选。
**告警内容一直在被吞，而"发送成功"的假象让它没被发现。**

## 三、修法（已落）

**绕过 shell**，直接用 node 跑 lark-cli 的真实入口，参数以 list 原样传：

```python
entry = os.path.join(os.path.dirname(LARK_CLI), "node_modules",
                     "@larksuite", "cli", "scripts", "run.js")
subprocess.run([node, entry] + args, capture_output=True, text=True, ...)  # 无 shell
```
验证方式（别只信返回码）：`--dry-run` 打请求体，看 `content` 字段里 **`\n` 是否齐全**。

> 顺带：`LARK_CLI` 是 `.cmd` 包装器，Windows 下 `shell=False` 直接 CreateProcess 会报 WinError 193 ⇒ **必须调 `.cmd` 里的真实 node 入口**。
> 本机**早就有这条教训**（归档 `ai-resource-hub\feishu\build_v03.py` 头注：「直接调 node run.js（绕开坏掉的 .bashrc lark-cli 函数）」）—— **同一个坑的老版本，我这次踩的是 shell 那条腿。**

## 四、更重要的两条（从"告警静默失效"抽象出来的）

1. **告警的成功判据不能只有"返回了 message_id"** ⇒ 必须**校验内容长度/行数**：
   "发成功了但内容没了"比"发失败"更危险，因为**它让告警看起来在岗**。
2. **凡是把多行正文当命令行参数传的地方，都要查一遍**（`shell=True` 尤其）。
   本机这次全局扫过：`D:\Work\元智能` 只有 `notify_capability.py` 一处 `shell=True`，其余 lark-cli 调用都在归档目录。

## 五、相关

- `D:\Work\元智能\10_AI自成长引擎\scripts\notify_capability.py`（已修；新增 `markdown=True` 参数走 `--markdown` 渲染富文本）
- `D:\记忆\流程\workflow_daily_essence_brief.md`（每日精选流水线）
- `D:\记忆\反馈\feedback-默认不主动汇报只在出错或待拍板时喊你.md`（"该喊的时候没喊"的实例）
