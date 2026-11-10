---
name: obsidian_optimization_plan
description: Obsidian 知识库优化方案（8.3→9.5+）：按评分标准逐项修复的优先级清单与可执行命令
type: reference
updated: 2026-11-11
kind: reference
status: active
---
# Obsidian 知识库优化方案（从 8.3 → 9.5+）

## 🔴 优先级 P0：立即修复（+0.5 分）

### 1. **清理未提交文件** (修复 -0.3 分)
```bash
# 检查未跟踪文件来源
cd "D:\Work"
git status --short | grep "^??"

# 决策：
# - 若是临时数据 → 加入 .gitignore
# - 若是重要工作 → git add 并提交
```

**执行步骤**:
1. `git stash` 保存当前所有修改
2. `git clean -n` 预览将要删除的文件
3. 将临时数据移动到 `_tmp/` 目录并忽略
4. 重要数据提交到分支

### 2. **移除备份文件** (修复 -0.2 分)
```bash
# 查找并清理 bak 文件
find "D:\记忆" -name "*.bak-*" -mtime +7 -delete
```

**规则**: `.bak-*` 文件超过 7 天自动删除

### 3. **密钥安全加固** (修复 -0.2 分)
- ✅ 已在 public-surface.json deny 中拦截
- ⚠️ **新增**: 在.gitignore 中添加 model_routes.json 的敏感字段检测
- 🔧 **工具**: 运行 `python D:\记忆\备份与安检\密钥扫描.py --strict`

---

## 🟡 优先级 P1：中期优化（+0.4 分）

### 4. **增强自动化覆盖率** (+0.4 分)
**现状**: 仅索引自动生成，缺少：
- 依赖图自动维护
- 死链检测
- 子库状态扫描

**实施方案**:
```python
# 新脚本：verify_vault_health.py
# 功能：
# 1. 检测所有子库是否可访问
# 2. 检查 Home.md 表格是否最新
# 3. 扫描过期备份文件
# 4. 输出健康报告 JSON
```

**cron 任务**: 每天 02:30 运行，失败时飞书告警

---

## 🟢 优先级 P2：长期演进（+0.3 分）

### 5. **引入冲突解决机制** (+0.3 分)
**问题**: 当记忆仓与工作库冲突时，谁优先？

**解决方案**:
```yaml
# 新增文件：D:\记忆\通用规范\conflict_resolution.yaml
resolution_priority:
  - work_live_code: 代码仓优先（ai-hub, listenloop）
  - knowledge_doc: 记忆仓优先（AGENTS.md, SOP）
  - shared_config: 以主仓为准（标注在文件头）
```

### 6. **建立架构审计机制** (+0.3 分)
**每月一次**:
```bash
# 脚本：audit_structure.py
# - 统计子库活跃度（最近 30 天提交）
# - 识别僵尸目录（无 README 或文档过期）
# - 生成改进建议报告
```

---

## 📊 预期效果

| 优化阶段 | 当前分数 | 预期分数 | 耗时 |
|---------|---------|---------|------|
| **P0 紧急修复** | 8.3 | 8.8 | 30 分钟 |
| **P1 自动化增强** | 8.8 | 9.2 | 2 小时 |
| **P2 长期演进** | 9.2 | 9.6 | 持续迭代 |

---

## 🚀 立即可执行命令

```bash
# 1. 快速体检
cd "D:\记忆" && python scripts/query_evidence.py "git status 未提交文件数量"

# 2. 清理备份
find "D:\记忆" -name "*.bak-*" -mtime +7 -ls

# 3. 检查密钥泄漏
python "D:\记忆\备份与安检\密钥扫描.py" --workspace "D:\Work"
```

---

## 💬 下一步行动建议

1. **今天**: 执行 P0 清理（30 分钟）
2. **本周**: 制定自动化脚本优先级
3. **本月**: 完成首次架构审计

**是否需要我帮你执行这些优化操作？**
