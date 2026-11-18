---
name: lesson_软链脚本resolve导致真源静默落空
description: 2026-11-18 实证：计划任务跑一个 SYMLINK 脚本时，脚本内 Path(__file__).resolve() 会解到软链真身所在目录，使「相对本脚本定位真源」的路径整体偏移，真源读不到却不报错、任务退出码仍为 0（假绿）。Buddy2API_DailySyncDSH 因此丢了 27 条模型容量覆盖。修法：给任务 action 补显式 --overrides 绝对路径，保留从软链运行（因为依赖同目录的 gateway_model_ids.py）。
type: lesson
updated: 2026-11-18
kind: fact
status: active
---

# 软链脚本 `.resolve()` 导致真源静默落空（2026-11-18）

## 现象

计划任务 `Buddy2API_DailySyncDSH`（每日 06:10）`LastTaskResult = 0`，看起来一切正常，实际**容量覆盖表从未加载**。

## 根因

`D:\项目\ai-hub\buddy2api\scripts\sync_dsh_profile.py` 是 **SYMLINK** → `D:\主控编排\gateway\sync_dsh_profile.py`。

脚本 L62 `SCRIPT_DIR = Path(__file__).resolve().parent`，`.resolve()` 解析软链到真身，于是：

- `SCRIPT_DIR` = `D:\Work\主控编排\gateway`
- L138 `OVERRIDES_PATH = SCRIPT_DIR.parent / "dsh_model_overrides.json"` = **`D:\Work\主控编排\dsh_model_overrides.json`（不存在）**
- 真文件在 `D:\Work\主控编排\gateway\dsh_model_overrides.json`（27 条有效）

`D:\主控编排` 本身又是 Junction → `D:\Work\主控编排`，两层链接叠加，读代码时极易漏看。

## 判据：怎么确认它「静默」而不是「正常」

`--dry-run` 输出这一行是唯一线索：

```
容量覆盖表: 未发现（D:\Work\主控编排\dsh_model_overrides.json）
```

**它出现在正常输出流里、且不影响退出码** ⇒ 典型的假绿，与 `lesson_体检只握手必假绿_20261020`、`lesson_绿分两级_产出断言才是底线_20261022` 同源。

## 修法（已实施并验证）

**只能补显式参数，不能改跑真身。** 实测改跑 `D:\Work\主控编排\gateway\sync_dsh_profile.py` 会 `ModuleNotFoundError: No module named 'gateway_model_ids'` —— 该模块只存在于 `buddy2api\scripts\` 下，软链运行才能同时满足「依赖可达」与「路径可见」。

改动：任务 action 补 `--overrides "D:\Work\主控编排\gateway\dsh_model_overrides.json"`。

## 验证输出（2026-11-18 20:11）

- 手动 `Start-ScheduledTask` → `LastTaskResult = 0`，profile 于 20:11:18 被重写
- dry-run 输出：`容量覆盖表: ...（27 条）`
- 落盘核对 profile 实际值：`loomy/GLM-5.3-Flash` contextWindow=**1048576**、`loomy/spark-x2.6`=**262144**、`scnet/SCNet-Max`=**1048576** —— 与覆盖表一致
- 备份：任务 XML `D:\临时文件夹\Buddy2API_DailySyncDSH_bak_20261118.xml`、profile `D:\临时文件夹\cordis.patch.yml.bak-syncfix-20261118-2010`

## 通用教训

1. **看到 `Path(__file__).resolve()` 就要问一句：这个脚本是不是软链？** 是软链则所有「相对脚本定位」的路径都会偏移一级。
2. **退出码 0 不等于配置生效**。凡是「读外部配置」的脚本，验证必须落到「配置值有没有进产物」，不能只看退出码。
3. 修之前先确认**能不能改跑真身**——本例依赖同目录模块，改跑真身会炸，只有补参数一条路。
4. 历史遗留：该任务仍有 27 条覆盖中 20 条管着停用渠道（workbuddy/qwenwork/raccoon/traework），现役只剩 loomy×2 + scnet。覆盖表本身值得后续瘦身。
