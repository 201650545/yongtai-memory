---
name: lesson-定时任务跑而不产出-占位符未替换
description: "定时任务'每天在跑但产出为 0'的静默故障（小红书每日管线实证）：脚本初始化时用了未替换的路径占位符 `<PROJECT_DIR>`，导致所有落盘路径含非法字符 `< >` 而 `OSError: Invalid argument`；任务 B 分析成功但路由/入库全丢，任务 C 从初始化就崩。诊断法＝先看日志是不是"跑满了但没落盘"，再 grep 占位符。"
metadata:
  node_type: memory
  type: 教训
  modified: 2026-10-20
type: lesson
updated: 2026-10-20
kind: rule
status: active
---

# 定时任务"每天跑但产出为 0"：先查占位符有没有被替换

现场是 `D:\Work\小红书点赞分析` 的每日管线（每天 01:00 跑任务 A/B/C）。**表面症状**：日志每天都有（`logs/mgr_YYYY-MM-DD.log`），用户却觉得"好像没天天在跑"——因为没有产出。这条教训不限于小红书，是所有"脚本模板生成后忘了替换占位符"的通用坑。

## 症状

1. **日志每天生成、流程每次都走到**，看似正常。
2. 但日志里大量出现 `[Errno 22] Invalid argument: '<PROJECT_DIR>\\_系统数据\\_routing.json'`。
3. 任务 B 明明打出 `分析完成 ✓ (2943 字)`，紧跟就是 `路由落盘失败` / `入库失败：[WinError 2]`。
4. 任务 C 从 `init_state` 第一步就崩，连续多天同一处 traceback。
5. 用户视角＝"任务没跑"，因为**分析结果一条都没落进盘**。

## 根因

脚本被初始化（可能是从模板/占位符脚手架生成）时，路径基址写成：
```python
BASE = r"<PROJECT_DIR>"
```
`<PROJECT_DIR>` 是**未替换的占位符**。Windows 路径里 `< >` 是非法字符，于是所有基于 `BASE` 拼出来的路径（`_系统数据\_routing.json`、`_review_state.json.tmp`、`b_answers/`）全部 `OSError: Invalid argument`。

而**同项目里另一个脚本** `xhs_like_manager.py` 用的是正确硬编码：
```python
BASE_DIR = r"D:\Work\小红书点赞分析"
```
所以任务 A 能跑、任务 B 的"拉取"能跑——只有落到 `route_sync.py`／`review_stale.py` 的那一步才炸。**同一个项目里一半对一半错，最容易骗过人。**

## 判据 / 诊断顺序

1. **先看日志末尾是不是"跑满了但没落盘"**：有 `分析完成 ✓` 却没有对应的入库/写库成功行 → 十有八九是落盘路径坏了，不是抓取失败。
2. **grep 占位符**：在项目里搜 `<PROJECT_DIR>`、`PROJECT_ROOT`、`__BASE__`、`{{BASE}}` 这类未替换标记。
   ```powershell
   Get-ChildItem <项目>\scripts -Filter *.py | ForEach-Object {
     Select-String -Path $_.FullName -Pattern 'PROJECT_DIR' -SimpleMatch
   }
   ```
3. **不要只看主脚本**：管线拆成多个模块时，`manager` 可能正确、被它 `import` 的 `route_sync`／`review_stale` 可能全错。**搜全项目，不只搜入口脚本。**
4. **修完必验证三件事**：① `py_compile` 语法通过；② 导入后 `print(BASE)` 指向真实存在的目录（`os.path.isdir`）；③ dry-run 一遍，确认不再报 `Invalid argument`。

## 修复（本次）

把 5 个文件里的 `BASE = r"<PROJECT_DIR>"` 替换为 `BASE = r"D:\Work\小红书点赞分析"`：

- `build_knowledge.py`（旧脚本，顺带修）
- `judge_gateway.py`（旧脚本，顺带修）
- `merge_verdicts.py`（旧脚本，顺带修）
- `route_sync.py`（**任务 B 落盘依赖，关键**）
- `review_stale.py`（**任务 C 本体，关键**）

改前已按"改前必存"铁律备份到 `scripts\.history\*.bak`。全部 `py_compile` 通过；`route_sync.DATA`、`review_stale.DATA`、`review_stale.STATE_FILE` 均 `os.path.isdir/isfile` 为 True；`review_stale.py --dry-run` 返回 `队列就绪：共 0 篇`，不再报 `Invalid argument`。

## 第二轮：同类占位符还有第二个，别只修一个就收工

2026-10-21 01:00 首跑验证：`Invalid argument` 已消失、任务 C 也正常了，但任务 B 冒出**新的**失败行：

```
分析完成 ✓ (1119 字)
入库失败：[WinError 2] 系统找不到指定的文件。
```

查下去是 `route_sync.py` 第 29 行的**另一个占位符**：

```python
CLI = r"C:\Users\<USER_NAME>\.trae-cn\plugins\trae-remote-official\lark\1.0.5\bin\lark-cli.exe"
```

`<USER_NAME>` 从未被替换 → lark-cli 找不到 → 每次入库都失败。修法与前者不同，用环境变量而非硬编码用户名：

```python
CLI = os.path.expandvars(r"%USERPROFILE%\.trae-cn\plugins\trae-remote-official\lark\1.0.5\bin\lark-cli.exe")
```

**这条教训的要点**：占位符往往是**成批出现**的（`<PROJECT_DIR>`、`<USER_NAME>`、`{{BASE}}`……）。修完一处必须**全项目再 grep 一遍所有尖括号/花括号占位符**，否则会出现"修好一个、暴露下一个"的挤牙膏，每轮都要等一次真实运行才发现。本次就是修了 5 个文件的 `BASE` 却漏了 `CLI`，多等了一整天才暴露。

**验证方式**：不要只看日志不报错，要**实际调用一次**。本次用修复后的 `write_lark()` 直接补写 3 篇历史分析，返回真实 `record_id`（如 `reczz28Pql8Ak3MS`）才算通。

## 关联

- 项目：`D:\记忆\项目\project_xhs_like_analysis.md`
- 流程：`D:\记忆\流程\workflow_xhs_daily_pipeline_three_tasks.md`（每日管线 A/B/C）
- 教训：`D:\记忆\教训\lesson_browser_automation_anti_scrape.md`（同项目的浏览器风控坑，也是"表面正常实则全错"一类）
- 脚本备份：`D:\Work\小红书点赞分析\scripts\.history\`