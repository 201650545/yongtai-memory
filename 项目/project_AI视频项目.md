---
name: project-AI视频项目
description: AI 视频项目入口页：用 Opus 5.5 + 浏览器乐谱渲染做视频；video-assembler 剪辑器已迁到 D:\Work\AI视频项目\video-assembler（2026-11-01）
type: project
updated: 2026-11-01
kind: fact
status: active
---
# AI 视频项目（入口页 · 2026-10-28 建）

> 郭老师 2026-10-27 指令：`D:\记忆\项目\` 下缺这个项目的入口页，Agent 找不到视频能力，补上。
> 口径：以下路径与文件数均为 **2026-10-27 实测**（`ds-work*` 清点 + 逐路径 Test-Path）。

## 一、现有资产（都在本机，不用重新找）

| 资产 | 路径 | 实测 |
|---|---|---|
| **AI 自动剪辑引擎**（主力） | `D:\Work\元智能\10_AI自成长引擎\草稿区\L3_Skill\video-assembler\` | 896 文件，含 `SKILL.md`、`AI_QUICKSTART.md`、`editor\README.md`(63KB) |
| 晨读 60 秒宣传片项目 | `D:\Work\AI视频项目\` | 561 文件，有 `AGENTS.md` + `README.md` |
| 30 秒知识点短视频 | 只有 `ds-work2\_inbox\知识视频\` 3 份查证文档(201KB) | **无项目目录** |
| B 站课件音画对齐 | `assemble.py` + `fetch_bilibili_lesson.py` | 已出过 1080×1440 成片（抽帧验收通过） |

## 二、注意事项（实测踩过的坑）

1. **`video-assembler` 已搬到 `D:\Work\AI视频项目\video-assembler\`（2026-11-01 郭老师定）**。本项目目录 `D:\Work\AI视频项目\` 是 AI 视频相关物的唯一归处（规矩见该项目 `AGENTS.md` §零）；**垃圾与测试文件不进本项目**（PoC、临时帧、废弃版本放 `_tmp\` 或删）。旧位置 `草稿区\L3_Skill\video-assembler\` 已清空（`out\` 730 文件 / 231.4 MB 试验产出已删），只剩一份迁移指针 `README_已迁移.md`。MCP 注册真源（`mcp_config.json`）与 Codex `config.toml` 的路径已同步改新。
2. 宣传片 README 里写的成片路径 `D:\Work\_inbox\宣传片_晨读60秒\v2_动效\final_v3\` **实测已不存在**（2026-10-24 按郭老师指示删除）。
3. 曾存在一个**名字多空格的误建目录** `L3_Skill\video-ass ***embler`；**2026-11-01 复核已不存在**（`Test-Path` 为 false）。
4. 本页 2026-10-28 之前**从未落盘**（只有 `ds-work2` 里的 `.pre_append.bak` 草稿）。

## 三、相关

- 画面形态升级（连环画 / 定格动画）：IDEA-030，见 `项目\project_想法池.md`
- 轻量剪辑工具清单：`_inbox\工具清单-20261027\工具清单.md`
- ffmpeg 不在 PATH，要走 `imageio_ffmpeg.get_ffmpeg_exe()`（实测路径见工具清单）
