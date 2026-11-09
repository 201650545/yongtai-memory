#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子库活跃度扫描工具 - scan_subrepo_activity.py (简化版)
========================
用途：分析各子库的最近活动情况，识别活跃/中等/僵尸目录
执行：python scan_subrepo_activity.py --workspace "D:\记忆" --days 30
"""

import argparse
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


def run_cmd(cmd: str, cwd: str = None) -> tuple:
    """执行 shell 命令并返回 (exit_code, output)"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, "Command timed out"


def get_git_commits(workspace: Path, days: int = 30) -> int:
    """获取指定天数内的 Git 提交数"""
    cmd = 'git log --since="{} days ago" --oneline | wc -l'.format(days)
    code, output = run_cmd(cmd, cwd=str(workspace))
    
    if code != 0 or not output.strip():
        return 0
    
    try:
        return int(output.strip())
    except ValueError:
        return 0


def get_file_count(workspace: Path) -> int:
    """统计 Markdown 文件数量"""
    cmd = 'find "{}" -name "*.md" -type f 2>/dev/null | wc -l'.format(str(workspace))
    code, output = run_cmd(cmd)
    
    if code != 0 or not output.strip():
        return 0
    
    try:
        return int(output.strip())
    except ValueError:
        return 0


def get_last_modified_time(workspace: Path) -> float:
    """获取最近修改的文件时间戳"""
    # 先尝试 git
    cmd = 'git log -1 --format=%ct'
    code, output = run_cmd(cmd, cwd=str(workspace))
    
    if code == 0 and output.strip():
        try:
            timestamp = float(output.strip())
            return timestamp
        except ValueError:
            pass
    
    # 回退到文件系统
    cmd = r'find "{}" -maxdepth 1 -name "*.md" -type f -printf "%T@\n" 2>/dev/null | sort -n | tail -1'.format(str(workspace))
    code, output = run_cmd(cmd)
    
    if code == 0 and output.strip():
        try:
            return float(output.strip())
        except ValueError:
            pass
    
    return datetime.now().timestamp() - 365 * 24 * 3600


def check_has_readme(workspace: Path) -> bool:
    """检查是否有 README.md"""
    readme_path = workspace / "README.md"
    return readme_path.exists()


def calculate_score(commits: int, files: int, last_active_days: int, has_readme: bool) -> float:
    """计算活跃度分数 (0-100)"""
    score = 0.0
    
    # 提交权重 (50 分)
    if commits >= 10:
        score += 50
    elif commits >= 5:
        score += 40
    elif commits >= 1:
        score += 20
    else:
        score += 0
    
    # 文件数量权重 (20 分)
    if files >= 50:
        score += 20
    elif files >= 20:
        score += 15
    elif files >= 5:
        score += 10
    elif files >= 1:
        score += 5
    
    # 新鲜度权重 (20 分)
    if last_active_days <= 1:
        score += 20
    elif last_active_days <= 7:
        score += 15
    elif last_active_days <= 30:
        score += 10
    elif last_active_days <= 90:
        score += 5
    else:
        score += 0
    
    # README 权重 (10 分)
    if has_readme:
        score += 10
    
    return min(100, round(score, 1))


def classify_status(score: float, commits: int, last_active_days: int) -> str:
    """根据分数分类状态"""
    if score >= 80 and commits > 0:
        return "✅ Active"
    elif score >= 60:
        return "⚠️ Moderate"
    elif score >= 40:
        return "🟡 Low Activity"
    else:
        return "❌ Zombie?"


def find_subrepos(workspace: Path) -> list:
    """查找所有有效的子仓库"""
    subrepos = []
    
    for item in workspace.iterdir():
        if not item.is_dir() or item.name.startswith('.'):
            continue
        
        git_dir = item / ".git"
        if git_dir.is_dir():
            subrepos.append(item)
    
    return subrepos


def generate_report(data: list, days: int) -> str:
    """生成 Markdown 报告"""
    lines = [
        "# 📊 子库活跃度分析报告",
        "",
        "**分析时间**: {}  ".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "**统计周期**: 最近 {} 天".format(days),
        "",
        "---",
        "",
        "## 📈 活跃度总览",
        "",
        "| 状态 | 数量 | 占比 |",
        "|------|------|------|"
    ]
    
    total = len(data)
    active_cnt = sum(1 for d in data if 'Active' in d['status'])
    mod_cnt = sum(1 for d in data if 'Moderate' in d['status'])
    low_cnt = sum(1 for d in data if 'Low' in d['status'])
    zombie_cnt = sum(1 for d in data if 'Zombie' in d['status'])
    
    lines.extend([
        "| ✅ Active | {} | {:.1f}% |".format(active_cnt, active_cnt/total*100 if total else 0),
        "| ⚠️ Moderate | {} | {:.1f}% |".format(mod_cnt, mod_cnt/total*100 if total else 0),
        "| 🟡 Low Activity | {} | {:.1f}% |".format(low_cnt, low_cnt/total*100 if total else 0),
        "| ❌ Zombie? | {} | {:.1f}% |".format(zombie_cnt, zombie_cnt/total*100 if total else 0),
        "",
        "---",
        "",
        "## 📋 详细数据",
        "",
        "| 目录 | 提交数 | 文件数 | 最后活跃 | 有 README | 得分 | 状态 |",
        "|-----|--------|--------|----------|----------|------|------|"
    ])
    
    sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)
    for d in sorted_data:
        readme_icon = '✅' if d['has_readme'] else '❌'
        lines.append("| `{}` | {} | {} | {}天前 | {} | {} | {} |".format(
            d['path'], d['commits'], d['files'], d['last_active_days'], 
            readme_icon, d['score'], d['status']
        ))
    
    lines.extend([
        "",
        "---",
        "",
        "## 💡 行动建议",
        "",
        "### 🔄 归档建议"
    ])
    
    zombies = [d for d in sorted_data if 'Zombie' in d['status']]
    if zombies:
        for z in zombies[:5]:
            lines.append("- **{}**: 已 {} 天未更新，考虑归档或清理".format(z['path'], z['last_active_days']))
    else:
        lines.append("- 暂无僵尸目录需要归档")
    
    lines.extend([
        "",
        "### 📝 补充文档"
    ])
    
    no_readme = [d for d in sorted_data if not d['has_readme']]
    if no_readme:
        for nr in no_readme[:5]:
            lines.append("- **{}**: 缺少 README.md 文档".format(nr['path']))
    else:
        lines.append("- 所有目录都有 README 文档")
    
    lines.extend([
        "",
        "### 🚀 优先维护",
        "优先关注以下活跃项目："
    ])
    
    active = [d for d in sorted_data if 'Active' in d['status']]
    active_sorted = sorted(active, key=lambda x: x['commits'], reverse=True)[:3]
    for a in active_sorted:
        lines.append("- **{}**: 最近提交 {} 次，保持持续维护".format(a['path'], a['commits']))
    
    lines.extend([
        "",
        "---",
        "",
        "*本报告由 `scan_subrepo_activity.py` 自动生成*"
    ])
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="子库活跃度扫描工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python scan_subrepo_activity.py --workspace "D:\\记忆" --days 30
  python scan_subrepo_activity.py --workspace "D:\\记忆" --output activity_report.md
        """
    )
    parser.add_argument("--workspace", type=str, default=r"D:\记忆", help="工作空间路径")
    parser.add_argument("--days", type=int, default=30, help="统计周期天数")
    parser.add_argument("--output", type=str, help="输出 Markdown 报告路径")
    
    args = parser.parse_args()
    
    workspace = Path(args.workspace)
    if not workspace.exists():
        print("❌ 工作区不存在：{}".format(workspace))
        return 1
    
    print("🔍 开始分析工作区：{}".format(workspace))
    print("📅 统计周期：最近 {} 天".format(args.days))
    print("-" * 80)
    
    subrepos = find_subrepos(workspace)
    
    if not subrepos:
        print("⚠️ 未发现子仓库（没有 .git 的目录将被跳过）")
        return 0
    
    results = []
    for repo in subrepos:
        commits = get_git_commits(repo, days=args.days)
        files = get_file_count(repo)
        last_mtime = get_last_modified_time(repo)
        last_active_days = int((datetime.now().timestamp() - last_mtime) / 86400)
        has_readme = check_has_readme(repo)
        
        score = calculate_score(commits, files, last_active_days, has_readme)
        status = classify_status(score, commits, last_active_days)
        
        results.append({
            'path': str(repo.relative_to(workspace)),
            'commits': commits,
            'files': files,
            'last_active_days': last_active_days,
            'has_readme': has_readme,
            'score': score,
            'status': status
        })
    
    report_md = generate_report(results, args.days)
    
    print("\n📊 发现 {} 个子仓库:".format(len(results)))
    
    active_cnt = sum(1 for d in results if 'Active' in d['status'])
    zombie_cnt = sum(1 for d in results if 'Zombie' in d['status'])
    
    print("   ✅ 活跃项目：{}".format(active_cnt))
    print("   ⚠️  一般活动：{}".format(sum(1 for d in results if 'Moderate' in d['status'])))
    print("   🟡 低活动：{}".format(sum(1 for d in results if 'Low' in d['status'])))
    print("   ❌ 僵尸目录：{}".format(zombie_cnt))
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report_md, encoding='utf-8')
        print("\n💾 报告已保存到：{}".format(output_path))
    else:
        print("\n💡 使用 --output 参数可以保存完整 Markdown 报告")
    
    print("-" * 80)
    
    return 0 if zombie_cnt == 0 else 1


if __name__ == "__main__":
    exit(main())
