---
name: lesson-channel-blame-needs-two-side-reconciliation
description: 判"某渠道一直失败"必须两侧对账（自家 route_log × 渠道官网日志），并搞清超时参数的真实语义；只看自家日志会把链路卡死、上游 200-带错误、守卫过严三类病因混成一个"渠道坏了"
metadata:
  node_type: memory
  type: 教训
  created: 2026-09-30
---

# 说某渠道老失败之前，先做两侧对账

2026-09-30 查 openrouter 起因：自家日志只有 outcome 标签，读起来像"OR 一直失败"。进 `openrouter.ai/logs` 对账后，同一个现象被拆成**三种不同病因**，处理方式完全不同：

| 病因 | 判据（两侧各看一眼才分得出来） | 该怎么办 |
|---|---|---|
| **请求根本没出境** | 自家有失败行、渠道侧**该分钟无任何记录** | 修出海链路（代理/节点），调超时参数无用 |
| **上游用 200 回错误** | 渠道侧 `Status=200 / Attempts=1` 但延迟极短（153–243ms），自家记成"空壳/错误事件" | 渠道官网永远看不到失败，别再去它的控制台找"错误率" |
| **自家守卫过严** | 渠道侧 **TTFT 分布**跨过守卫线（本次 0.87–3.6s vs 3.0s 线），且大 prompt 更慢 | 按实测分布调阈值，或按 prompt 体量分级 |

## 三条会反复咬人的技术事实

1. **`urllib`/socket 的 `timeout` 是"单次 socket 操作"上限，不是请求总时长。** 实测 8 发 ×512KB 全 200、耗时 13.6–38.8s，一次都没 trip。所以 `write operation timed out` ＝对端**完全停读**超预算（真卡死），不是"预算不够大"。**推论：想靠调大超时来消写超时，方向就是错的。**
2. **自家日志的"成功/选中"字段不可信。** `api_gateway.py:822` 在**发起请求之前**就写 `resolved_channel`，前端又用 `!!resolved_channel` 当成功（`api_page.html:2896`）⇒ 全链失败的行照样标绿。任何按这张表做的判断都要改读 `failures`/`errors` 数组。
3. **滚动日志的窗口只能按字节偏移切。** `route_log.jsonl` 的 `ts` 只有时分秒、跨天 append；我两次用 `ts>=` 字符串切窗口，都把**昨天**的行圈进"今天"，得出 3324 条／76 条两个假数字，均作废重算。
4. 附带一条：**语义缓存会吞掉你的验证请求**（0.04–0.12s 返回、route_log 零新增）。验链路必须先确认没命中缓存——用高熵随机前缀，别用重复 prompt＋填充字符。

## 渠道官网日志的作用域陷阱（本次未证完）

自家 27 条 OR 成功 vs OR `/logs`（Default Workspace，1d）同期 ~13 行。疑该视图按 **workspace/账号** 过滤，而网关在 **4 把 key** 轮换（`data/rate_limit_day.json` 当日见 3 个 key 指纹）。**没做完就不写进结论**；要逐条对齐只能靠 **trace-id 配对埋点**（把渠道返回的 `gen-…` id 记进 route_log）。

相关：[[调度大脑记忆/项目/project_ai_gateway]]、[[调度大脑记忆/反馈/feedback_round_close_triple_writeback]]、[[调度大脑记忆/教训/lesson_gateway_restart_privilege_trap]]
