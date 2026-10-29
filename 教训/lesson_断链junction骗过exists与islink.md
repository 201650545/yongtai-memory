---
name: lesson_断链junction骗过exists与islink
description: Windows 上指向已删除目录的 junction（断链联接）会让 os.path.exists 返回 False、os.path.islink 也返回 False，两头都判错——真在、说不在；是链接、说不是。唯一可靠判据是 os.path.lexists（是否还有这个目录项）+ pathlib.Path.is_junction（Python 3.12+），PowerShell 的 Get-Item 反而会把断链 junction 报成 Exists=True
metadata:
  node_type: memory
  type: 教训
  modified: 2026-10-29
  verified_on: Windows 11 + Python 3.12.10
type: lesson
updated: 2026-10-29
kind: rule
status: active
---

# 断链 junction：exists 与 islink 同时骗你

## 现象

`D:\Work\小红书点赞分析\.trae\skills\` 下有两个旧 Junction，目标目录已被删除。
清理脚本用 `os.path.exists()` 判断「链接还在不在」→ 全部返回 `False`，
于是判定「已经删干净了」，实际目录项还在、`git status` 也算它是脏的。

反过来，想用 `os.path.islink()` 识别「这是个链接、别当实体删」→ 同样 `False`，
于是把 junction 当成普通空目录 `rm -rf`，C 盘路径当场悬空，应用起不来。

## 实测（本机 2026-10-29，Python 3.12.10）

构造：`New-Item -ItemType Junction link -Target target` → 删掉 `target` → 量 `link`。

| 判据 | 结果 | 是否可信 |
|---|---|---|
| `os.path.exists(p)` | **False** | ❌ 它还在 |
| `os.path.lexists(p)` | **True** | ✅ 目录项仍在 |
| `os.path.islink(p)` | **False** | ❌ 它是 junction |
| `pathlib.Path(p).exists()` | False | ❌ |
| `pathlib.Path(p).is_symlink()` | False | ❌ |
| `pathlib.Path(p).is_junction()` | **True** | ✅（3.12+ 才有） |
| PowerShell `Get-Item p` 的 `Exists` | **True** | ⚠️ 与 Python 相反 |

两条互相矛盾的事实，一次搞清楚：

- **`exists` 走的是「能不能访问到目标」**。目标没了 ⇒ False。它回答的是「能不能用」，不是「在不在」。
- **`islink` 只认符号链接（symlink）**。Junction 是 reparse point 的另一种，`islink` 天生不认；Windows 上判断 junction 要用 `is_junction`（3.12 新增）或 `os.lstat().st_file_attributes & FILE_ATTRIBUTE_REPARSE_POINT`。
- PowerShell 的 `Get-Item` 看的是目录项本身，所以断链也报 `Exists=True`——**别拿 PS 的结果当反证**。

## 正确做法

```python
# 判断目录项是否还在（不管目标死活）
if os.path.lexists(path):
    ...
# 判断它是不是 junction（3.12+）
if pathlib.Path(path).is_junction():
    ...
```

清理顺序必须是：**先 `lexists` 确认目录项存在 → 判 `is_junction` 确认是链接 → 删链接本身（`os.rmdir` / `Remove-Item` 不带 `-Recurse`），不要 `rm -rf` 目标**。删完再 `New-Item -ItemType Directory` 重建空壳，避免路径悬空。

## 同类问题的共同点

「工具给的信号本身可能是错的」——`exists` 说不在、`islink` 说不是链接、PS 说在，
三个信号互相矛盾。**任何删除/迁移脚本，删除前必须至少用两种独立判据交叉验证**，
并且判据要选「描述对象本身」的（`lexists` / `is_junction`），而不是「描述对象可用性」的（`exists`）。
