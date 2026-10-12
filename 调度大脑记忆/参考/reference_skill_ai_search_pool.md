---
name: ai-search-pool Skill（多引擎 AI 搜索聚合）
description: 用户要「拓展搜索」时用的 skill。把 :3000 AI 搜索网关的逻辑改成了按需调用的 skill —— 无进程、无端口、无开机自启。指针 + 关键事实。
type: reference
---

# ai-search-pool skill —— 用户要「拓展搜索」时用它

## 一句话

原 `:3000` **AI 搜索网关**（聚合多个已登录的 AI 搜索引擎网页端）**已改为 skill 形态**。
用户要「**拓展搜索 / 扩展搜索 / 多引擎搜索 / 多方查证**」时，**直接用这个 skill，不要再启动 :3000 网关**。
（2026-10-11 郭老师裁定：「3000 网关那个逻辑就做成 skill 吧……用户需要拓展搜索时就用这个 skill」。）

## 位置

**真源（唯一可改处）** —— 按郭老师 2026-10-11 裁定「我自己做的 skill 必须放在元智能项目中」，
本体已归入技能库母仓（`技能库/README.md` §5 已登记）：

```
D:\Work\元智能\10_AI自成长引擎\技能库\ai-search-pool\
  SKILL.md    ← 完整用法 / 引擎表 / 常见坑（**正文在 skill 里，本文件只做指针**）
  run.py      ← 执行器：直接 import content_pool 调 run_search()
```

**宿主投影（Junction，勿直接改）**：

```
C:\Users\郭永涛\.workbuddy-ai\skills\ai-search-pool
    └─ Junction ─→ D:\Work\元智能\10_AI自成长引擎\技能库\ai-search-pool
```

（已实测 `LinkType=Junction`，透过链接可正常加载运行。**改动永远只改真源。**）

## 怎么用

```bash
PY="C:/Users/郭永涛/AppData/Roaming/uv/python/cpython-3.11.15-windows-x86_64-none/python.exe"
SK="C:/Users/郭永涛/.workbuddy-ai/skills/ai-search-pool/run.py"

"$PY" "$SK" "问题"                          # 默认 7 路（4 网页 + 3 资讯）
"$PY" "$SK" "问题" --engines metaso,perplexity   # 只问指定引擎（快）
"$PY" "$SK" --health                        # 先探活浏览器会话
"$PY" "$SK" --list-engines                  # 列引擎清单
```

产出 `<search_gateway>/services/runs/<run_id>/report.html`（＋ `summary.md` 综合结论）
→ 用 `present_files` 把 report.html 给用户看。

## 为什么不做成网关（2026-10-11 实测裁定）

`:3000` **只是一层 HTTP 壳**，底下真正干活的是两层：

| 层 | 文件 | 作用 |
|---|---|---|
| 调度层 | `search_gateway/services/content_pool.py` | 并发调度、汇总、出报告；**本就带 `if __name__=="__main__"` CLI** |
| 引擎层 | `search_gateway/services/engines.py` | 通过 `opencli browser <session>` 驱动已登录的搜索网页端 |

直接调库 ⇒ **无进程、无端口、无开机自启**。反例：该网关 **2026-09-25 → 10-11 静默死掉 6 周无人发现**
（日志停 09-25、健康记录停 09-28）—— 这就是不要常驻进程的理由。

实测对照：skill 形态 52.2s 出报告；网关形态 63.4s 出报告，**产出等价**，网关只多一个 HTTP 口。

## 关键事实（引用前必读）

- **引擎共 8 个**：`yuanbao` `doubao` `kimi` `qianwen` `metaso` `grok` `perplexity` `zai`。
  默认组合 = `metaso, perplexity, yuanbao, grok` ＋ 资讯兜底 `aihot, hackernews, rss`（共 7 路）。
  ⚠️ `kimi`/`qianwen` 常超时、`doubao` 回答过短，**2026-08-30 已降级**，非必要不选。
- **总结模型 = `free-high`**（回落 `free-flash`）。
  🔴 **不要换回 `deepseek-v4-flash`** —— 它是**推理模型**，真实长 prompt 下会把 `max_tokens` 全烧在
  reasoning 上、`content` 恒为空（HTTP 200 却什么都不吐，且旧代码静默 `return ""`，所以长期没人发现）。
- **鉴权**：`:3100` 已启用鉴权，key 从 `search_gateway/data/api_state.json` 的 `api_key` 读
  （环境变量 `SEARCH_GATEWAY_API_KEY` 优先）。🔴 **key 绝不写进代码，也不写进本记忆库**
  （本库会 git publish 到 GitHub 只读镜像）。`data/` 已被 `.gitignore` 忽略。
- **前置条件**：opencli 浏览器桥 ＋ 已登录的 Chrome（引擎就是"已登录的网页端"）；`:3100` 在跑（做总结用）。
- **引擎有随机性**：同一问题各轮会随机超时 1–2 路（实测 metaso / perplexity / grok 都出现过），
  **只要 ≥1 路答完就能出报告**，不影响交付。

## 关联

- 后台机制、渠道与路由：见 [[调度大脑记忆/参考/reference_免费中转站与聚合代理工具池]]、
  [[调度大脑记忆/参考/reference_全维度AI模型智力评分与推荐调度总则]]
- 网关本体：`D:\项目\ai-hub\search_gateway\`（`:3100` API 转发网关 ＋ `:3000` 搜索网关同仓不同系统）
