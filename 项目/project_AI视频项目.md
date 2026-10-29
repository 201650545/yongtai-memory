---
name: project-AI视频项目
type: project
updated: 2026-10-28
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
| 句读 60 秒宣传片项目 | `D:\Work\AI视频项目\` | 561 文件，有 `AGENTS.md` + `README.md` |
| 30 秒知识点短视频 | 只有 `ds-work2\_inbox\知识视频\` 3 份查证文档(201KB) | **无项目目录** |
| B 站课件音画对齐 | `assemble.py` + `fetch_bilibili_lesson.py` | 已出过 1080×1440 成片（抽帧验收通过） |

## 二、注意事项（实测踩过的坑）

1. `video-assembler` 在**草稿区**，不是正式项目目录；要长期用应提升到 `D:\Work\元智能\AI自动剪辑器\`（**尚未搬迁**）。
2. 宣传片 README 里写的成片路径 `D:\Work\_inbox\宣传片_句读60秒\v2_动效\final_v3\` **实测已不存在**（2026-10-24 按郭老师指示删除）。
3. 存在一个**名字多空格的误建目录** `L3_Skill\video-ass ***embler`，内部只有一份说明文件（写明"写错位置的副本、沙箱回收站删不掉"），**不要在该目录上工作**。
4. 本页 2026-10-28 之前**从未落盘**（只有 `ds-work2` 里的 `.pre_append.bak` 草稿）。

## 三、相关

- 画面形态升级（连环画 / 定格动画）：IDEA-030，见 `项目\project_想法池.md`
- 轻量剪辑工具清单：`_inbox\工具清单-20261027\工具清单.md`
- ffmpeg 不在 PATH，要走 `imageio_ffmpeg.get_ffmpeg_exe()`（实测路径见工具清单）
