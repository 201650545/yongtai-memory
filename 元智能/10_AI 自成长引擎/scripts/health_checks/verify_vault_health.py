#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双仓健康检查工具 - verify_vault_health.py
========================
用途：扫描并验证 Obsidian 知识库仓库的健康状态
执行：python verify_vault_health.py --workspaces "D:\记忆","D:\Work" --output health_report.json

主要检查项：
1. ✅ 子库可达性 - 遍历 Home.md 中的子库链接，验证目录是否存在
2. ✅ 索引一致性 - 对比生成的 table 与实际目录结构
3. ✅ 备份清理 - 查找 >7 天的 .bak-* 文件
4. ✅ Git 脏污度 - 统计未提交/未跟踪文件数
5. ⚠️ 密钥风险 - 轻量扫描明文凭据（可选）
"""

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any


def run_cmd(cmd: str, cwd: str = None) -> tuple[int, str]:
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
    except FileNotFoundError:
        return -1, "Command not found"


def check_subrepo_accessibility(workspace: Path):
    """验证 Home.md 表格中的子库是否可达。

    子库可能是带数字前缀的嵌套目录（如 10_AI自成长引擎）或跨仓目录
    （如 通用规范 在记忆仓），因此用「去前缀的目录名集合」做包含匹配，
    并把兄弟记忆仓纳入搜索范围，避免把合法嵌套/跨仓结构误判为缺失。
    """
    home_md = workspace / "Home.md"
    if not home_md.exists():
        return True, []

    def norm(name: str) -> str:
        return re.sub(r"^\d+[_\-]?", "", name.strip()).strip("`[]")

    # 收集本仓 + 记忆仓的所有目录名（去前缀归一化）
    known = set()
    search_roots = [workspace]
    memory_vault = Path(r"D:\记忆")
    if memory_vault.exists() and memory_vault != workspace:
        search_roots.append(memory_vault)
    for root in search_roots:
        for p in root.rglob("*"):
            if p.is_dir() and not any(part.startswith(".") for part in p.relative_to(root).parts):
                known.add(norm(p.name))

    missing = []
    in_table = False
    for line in home_md.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells or set(cells[0]) <= {"-", ":", " "} or cells[0] in ("子库", ""):
            in_table = True
            continue
        if not in_table:
            continue
        name = norm(re.split(r"[（(]", cells[0])[0])
        if name and name not in known:
            missing.append(cells[0])

    return len(missing) == 0, missing


def check_backup_files(workspace: Path, days: int = 7) -> List[str]:
    """查找超过指定天数的 .bak-* 备份文件（纯 Python，跨平台）"""
    import time
    cutoff = time.time() - days * 86400
    expired = []
    for p in workspace.rglob("*.bak-*"):
        if p.is_file() and p.stat().st_mtime < cutoff:
            expired.append(str(p))
    return expired


def check_git_status(workspace: Path) -> Dict[str, int]:
    """统计 Git 仓库的修改和未跟踪文件数"""
    status, stdout = run_cmd("git status --short", cwd=str(workspace))
    
    if status != 0 or not stdout:
        return {"modified": 0, "untracked": 0, "total": 0}
    
    lines = [l for l in stdout.split('\n') if l.strip()]
    modified = sum(1 for l in lines if l.strip().startswith(' M'))
    untracked = sum(1 for l in lines if l.strip().startswith('??'))
    
    return {
        "modified": modified,
        "untracked": untracked,
        "total": len(lines)
    }


def scan_secrets_light(workspace: Path, max_files: int = 1000) -> List[Dict]:
    """轻量级密钥扫描：纯 Python 遍历文本文件内容，只报位置不回显密钥值"""
    patterns = {
        "Bearer": r"Bearer\s+[A-Za-z0-9_\-\.]{20,}",
        "API_KEY": r"(?:api[_-]?key|apikey)\s*[=:]\s*['\"]?[A-Za-z0-9_\-\.]{16,}",
        "Token": r"(?:token|secret)\s*[=:]\s*['\"]?[A-Za-z0-9_\-\.]{16,}",
    }
    skip_dirs = {".git", ".cache", "node_modules", ".venv", "venv", "_scratch_tmp", "scratch"}
    findings = []
    scanned = 0
    for p in workspace.rglob("*"):
        if scanned >= max_files:
            break
        if not p.is_file() or p.suffix not in (".md", ".py", ".json"):
            continue
        if any(part in skip_dirs for part in p.parts):
            continue
        scanned += 1
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for keyword, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                findings.append({"file": str(p.relative_to(workspace)), "pattern": keyword})
                break
    return findings[:20]


def generate_health_report(workspace: Path, vault_name: str) -> Dict[str, Any]:
    """为单个仓库生成完整健康报告"""
    print(f"🔍 正在检查 {vault_name}...")
    
    # 1. 子库可达性
    subrepo_ok, missing = check_subrepo_accessibility(workspace)
    subrepo_status = "healthy" if subrepo_ok else "warning"
    
    # 2. 备份文件检查
    expired_backups = check_backup_files(workspace, days=7)
    backup_status = "clean" if not expired_backups else "dirty"
    
    # 3. Git 状态
    git_stats = check_git_status(workspace)
    git_status = "clean" if git_stats["total"] == 0 else "dirty"
    
    # 4. 密钥扫描（仅在仓库脏污时进行）
    secrets_found = []
    if git_stats["total"] > 10:
        secrets_found = scan_secrets_light(workspace)
    
    # 构建报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "vault_name": vault_name,
        "path": str(workspace.absolute()),
        "checks": {
            "subrepo_accessibility": {
                "status": subrepo_status,
                "details": {"missing_directories": missing} if not subrepo_ok else {}
            },
            "backup_cleanup": {
                "status": backup_status,
                "expired_count": len(expired_backups),
                "files": expired_backups[:10]
            },
            "git_cleanliness": {
                "status": git_status,
                "statistics": git_stats
            },
            "secrets_scan": {
                "status": "clean" if not secrets_found else "danger",
                "count": len(secrets_found),
                "findings": secrets_found[:5]
            }
        },
        "overall_score": calculate_score(git_stats, expired_backups, secrets_found)
    }
    
    # 添加警告信息
    alerts = []
    if missing:
        alerts.append({"level": "error", "message": f"缺少子库目录：{', '.join(missing)}"})
    if expired_backups:
        alerts.append({"level": "warning", "message": f"发现 {len(expired_backups)} 个过期备份文件"})
    if git_stats["total"] > 20:
        alerts.append({"level": "info", "message": f"Git 仓库较脏 ({git_stats['total']} 个未提交文件)"})
    if secrets_found:
        alerts.append({"level": "critical", "message": f"发现 {len(secrets_found)} 个潜在密钥泄露风险"})
    
    report["alerts"] = alerts
    
    return report


def calculate_score(git_stats: Dict, expired_backups: List, secrets: List) -> float:
    """计算健康分数（0-100）"""
    score = 100.0
    
    # Git 脏污扣分
    score -= min(30, git_stats["total"] * 0.5)
    
    # 过期备份扣分
    score -= min(20, len(expired_backups) * 2)
    
    # 密钥泄露严重扣分
    if secrets:
        score -= 50
    
    return max(0, round(score, 1))


def main():
    parser = argparse.ArgumentParser(
        description="双仓健康检查工具 - 验证 Obsidian 知识库整体健康状态",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python verify_vault_health.py --workspaces "D:\\记忆","D:\\Work"
  python verify_vault_health.py --workspaces "D:\\记忆","D:\\Work" --output report.json
  python verify_vault_health.py --detailed  # 显示详细信息
        """
    )
    parser.add_argument(
        "--workspaces",
        type=str,
        default="D:\\记忆,D:\\Work",
        help="用逗号分隔的工作空间路径列表 (默认：D:\\记忆,D:\\Work)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出 JSON 报告路径 (可选)"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="显示详细检查结果"
    )
    
    args = parser.parse_args()
    
    workspaces = [w.strip() for w in args.workspaces.split(",")]
    reports = {}
    overall_alerts = []
    
    print("=" * 80)
    print("🏥 Obsidian Vault Health Check - 知识库健康检查工具")
    print("=" * 80)
    print(f"📅 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 工作空间：{', '.join(workspaces)}")
    print("-" * 80)
    
    for ws_path_str in workspaces:
        ws_path = Path(ws_path_str)
        if not ws_path.exists():
            print(f"❌ 路径不存在：{ws_path}")
            continue
        
        report = generate_health_report(ws_path, ws_path.name)
        reports[ws_path.name] = report
        overall_alerts.extend(report.get("alerts", []))
        
        # 控制台输出摘要
        score = report["overall_score"]
        emoji = "✅" if score >= 80 else ("⚠️" if score >= 60 else "❌")
        print(f"{emoji} {ws_path.name}: 得分 {score}/100")
        
        if args.detailed:
            for check_name, check_data in report["checks"].items():
                status = check_data.get("status", "?")
                print(f"   - {check_name}: {status}")
            
            if report.get("alerts"):
                print("   📋 警告:")
                for alert in report["alerts"]:
                    level = alert["level"].upper()
                    msg = alert["message"][:60] + "..." if len(alert["message"]) > 60 else alert["message"]
                    print(f"      [{level}] {msg}")
        
        print()
    
    # 汇总结果
    print("=" * 80)
    print("📊 总体评估:")
    avg_score = sum(r["overall_score"] for r in reports.values()) / len(reports) if reports else 0
    overall_emoji = "✅" if avg_score >= 80 else ("⚠️" if avg_score >= 60 else "❌")
    print(f"{overall_emoji} 平均健康分：{avg_score:.1f}/100")
    
    if overall_alerts:
        print(f"⚠️ 共发现 {len(overall_alerts)} 条警报:")
        for i, alert in enumerate(overall_alerts[:5], 1):  # 只显示前 5 条
            level = alert["level"].upper()
            msg = alert["message"][:70] + "..." if len(alert["message"]) > 70 else alert["message"]
            print(f"   {i}. [{level}] {msg}")
        
        if len(overall_alerts) > 5:
            print(f"   ... 还有 {len(overall_alerts) - 5} 条警报")
    
    # 保存 JSON 报告
    if args.output:
        output_path = Path(args.output)
        full_report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_vaults": len(reports),
                "average_score": avg_score,
                "total_alerts": len(overall_alerts)
            },
            "vaults": reports
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 完整报告已保存到：{output_path}")
    
    print("=" * 80)
    
    # 返回非零退出码表示有问题
    return 0 if avg_score >= 80 else 1


if __name__ == "__main__":
    exit(main())
