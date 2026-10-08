# project.yaml 模板

> 机器可读项目元数据：AI / 脚本 / 未来的 workspace-index 自动汇总读这个；人类读 README。
> 复制到项目根 `project.yaml`，替换 {} 占位。

```yaml
id: {repo-name}
name: {中文名}
type: {game|tool|infra|notes}
status: {active|paused|done}
visibility: {public|private}

sources:
  overview: docs/00-项目总览.md
  tasks: docs/01-任务看板.md
  assets: docs/02-资产清单.md
  spec: docs/03-规格与规范.md

handbook:
  version: v1.0
  overrides: docs/03-规格与规范.md

updated_at: {YYYY-MM-DD}
```
