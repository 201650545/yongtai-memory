#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
死链检测工具 - detect_dead_links.py
========================
用途：扫描所有 Markdown 文件中的内部链接 [[xxx]]，验证目标是否存在
执行：python detect_dead_links.py --workspace "D:\记忆" --output dead_links_report.md

主要功能：
1. 🔍 提取所有 [[Link]] 格式的内部链接
2. ✅ 解析链接标题与实际文件名映射
3. ⚠️ 报告缺失的目标文件和断裂的链接
4. 📊 生成结构化的 Markdown 报告
"""

import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


def extract_links_from_file(filepath: Path) -> List[Tuple[str, str]]:
    """从单个文件中提取所有 [[Link]] 格式的链接"""
    content = filepath.read_text(encoding='utf-8', errors='ignore')
    
    # 匹配 [[...]] 格式的链接
    pattern = r'\[\[(.*?)\]\]'
    matches = re.findall(pattern, content)
    
    links = []
    for match in matches:
        # 去掉锚点部分 (例如 [[File#Section]])
        link_title = match.split('#')[0].strip()
        if link_title:
            links.append((link_title, str(filepath)))
    
    return links


def resolve_link_to_file(link_title: str, base_dir: Path, all_files: Set[Path]) -> Tuple[bool, str]:
    """
    尝试将链接解析为实际的文件路径
    返回：(是否找到，找到的路径或错误信息)
    """
    # 清理标题：移除可能的空格、下划线转义等
    clean_title = link_title.strip().replace('\\_', '_')
    
    # 常见扩展名列表（Obsidian 自动补全规则）
    extensions = ['.md', '', '.markdown', '.txt']
    
    # 尝试多种可能性
    candidates = [
        clean_title,                                    # 精确匹配
        f"{clean_title}.md",                            # 加 .md 扩展名
        f"{clean_title}.markdown",                      # 加 .markdown
        clean_title.lower(),                            # 小写版本
        f"{clean_title.lower()}.md",                    # 小写 + .md
    ]
    
    # 如果标题包含路径分隔符，优先在相对路径中查找
    if '/' in clean_title or '\\' in clean_title:
        for ext in extensions:
            candidate = f"{clean_title}{ext}"
            candidate_path = base_dir / candidate
            if candidate_path.exists():
                return True, str(candidate_path)
    
    # 在其他目录中搜索匹配的基名
    for file_path in all_files:
        filename = file_path.stem.lower()
        link_base = clean_title.lower().split('/')[-1].split('\\')[-1]
        
        if filename == link_base:
            return True, str(file_path)
    
    # 如果有任何变体匹配成功
    for candidate in candidates:
        candidate_path = base_dir / candidate
        if candidate_path.exists():
            return True, str(candidate_path)
    
    return False, None


def analyze_reference_patterns(files: List[Path], workspace: Path) -> Dict[str, Set[str]]:
    """分析文件的引用模式，找出被引用的频率"""
    references = defaultdict(set)  # source_file -> set of referenced_links
    
    for filepath in files:
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            links = re.findall(r'\[\[(.*?)\]\]', content)
            for link in links:
                references[str(filepath)].add(link.strip())
        except Exception as e:
            print(f"⚠️ 读取 {filepath} 失败：{e}")
    
    return references


def find_orphaned_files(all_files: Set[Path], references: Dict[str, Set[str]], workspace: Path) -> List[Path]:
    """找出从未被其他文件引用的孤立文件"""
    referenced_titles = set()
    for sources in references.values():
        referenced_titles.update(sources)
    
    orphaned = []
    for filepath in all_files:
        if filepath.name == 'Home.md' or filepath.name.startswith('README'):
            continue
        
        title = filepath.stem.lower().replace('_', '').replace('-', '')
        if title not in [t.lower().replace('_', '').replace('-', '') for t in referenced_titles]:
            orphaned.append(filepath)
    
    return orphaned[:10]  # 限制输出数量


def check_circular_references(references: Dict[str, Set[str]], max_depth: int = 5) -> List[List[str]]:
    """检测循环引用链"""
    graph = {}
    for src, targets in references.items():
        graph[src] = targets
    
    cycles = []
    visited_global = set()
    
    def dfs(current: str, path: List[str], depth: int):
        if depth > max_depth:
            return
        
        if current in path:
            cycle_start = path.index(current)
            cycle = path[cycle_start:] + [current]
            if len(cycle) > 2 and cycle not in cycles:
                cycles.append(cycle)
            return
        
        if current in graph:
            for target in graph[current]:
                dfs(target, path + [current], depth + 1)
    
    for start_node in list(graph.keys())[:20]:  # 限制搜索范围
        if start_node not in visited_global:
            dfs(start_node, [], 0)
            visited_global.add(start_node)
    
    return cycles[:5]  # 最多返回 5 个循环


def scan_workspace(workspace: Path) -> Dict:
    """扫描整个工作区的死链情况"""
    print(f"🔍 正在扫描工作区：{workspace}")
    
    # 收集所有 Markdown 文件
    md_files = list(workspace.rglob('*.md'))
    all_files_set = set(md_files)
    
    print(f"   📄 发现 {len(md_files)} 个 Markdown 文件")
    
    # 提取所有链接
    all_links = []
    for filepath in md_files:
        try:
            links = extract_links_from_file(filepath)
            for link_title, source_file in links:
                all_links.append({
                    'link': link_title,
                    'source': source_file,
                    'path': str(filepath.relative_to(workspace))
                })
        except Exception as e:
            print(f"   ⚠️ 处理 {filepath} 时出错：{e}")
    
    print(f"   🔗 共发现 {len(all_links)} 个内部链接")
    
    # 解析每个链接
    broken_links = []
    resolved_count = 0
    
    for item in all_links:
        found, resolved_path = resolve_link_to_file(
            item['link'], 
            workspace, 
            all_files_set
        )
        
        if found and resolved_path:
            resolved_count += 1
        else:
            broken_links.append({
                'link': item['link'],
                'source': item['source'],
                'relative_path': item['path'],
                'resolution': 'not_found'
            })
    
    # 分析孤立文件
    orphaned_files = find_orphaned_files(all_files_set, {}, workspace)
    
    # 检测循环引用
    references = analyze_reference_patterns(md_files, workspace)
    circular_refs = check_circular_references(references)
    
    return {
        'total_files': len(md_files),
        'total_links': len(all_links),
        'resolved_links': resolved_count,
        'broken_links_count': len(broken_links),
        'broken_links': sorted(broken_links, key=lambda x: x['source'])[:20],
        'orphaned_files': [str(f.relative_to(workspace)) for f in orphaned_files],
        'circular_references': circular_refs,
        'summary': {
            'link_coverage_rate': round(resolved_count / len(all_links) * 100, 1) if all_links else 100,
            'broken_rate': round(len(broken_links) / len(all_links) * 100, 1) if all_links else 0
        }
    }


def generate_markdown_report(stats: Dict, workspace: Path) -> str:
    """生成结构化的 Markdown 报告"""
    report = f"""# 🔗 死链检测报告

**生成时间**: {stats.get('_timestamp', 'N/A')}  
**工作区**: {workspace}  
**扫描文件数**: {stats['total_files']}  
**总链接数**: {stats['total_links']}  

---

## 📊 摘要统计

| 指标 | 数值 |
|------|------|
| ✅ 正常链接 | {stats['resolved_links']} |
| ❌ 断裂链接 | {stats['broken_links_count']} |
| 📈 覆盖率 | {stats['summary']['link_coverage_rate']}% |
| ⚠️ 破裂率 | {stats['summary']['broken_rate']}% |

---

## 🔴 关键问题 ({len(stats['broken_links'])} 个)

{''.join([f"""### 来源：`{os.path.basename(item['source'])}`
- **失效链接**: `[[{item['link']}]]`
- **相对路径**: `{item['relative_path']}`
- **状态**: 目标文件不存在

""" for item in stats['broken_links'][:10]])}
{'无' if len(stats['broken_links']) == 0 else ''}

---

## 🟡 警告项

### 孤立文件 (未被引用)

{'' if stats['orphaned_files'] else '暂无'}
{''.join([f'- `{os.path.basename(f)}`' for f in stats['orphaned_files'][:5]])}

### 循环引用

{'' if not stats['circular_references'] else ''}
{''.join([f"- {' → '.join(ref[:6])}" for ref in stats['circular_references'][:3]])}

---

## 💡 建议

1. **修复断裂链接**: 确认失效链接应指向的正确目标文件或删除该引用
2. **补充 README**: 孤立文件可能是独立模块，考虑添加说明文档
3. **打破循环**: 循环引用可能导致渲染问题，建议重构索引结构

---

*本报告由 `detect_dead_links.py` 自动生成*
"""
    return report


def main():
    parser = argparse.ArgumentParser(
        description="死链检测工具 - 扫描 Obsidian 知识库中的断裂内部链接",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python detect_dead_links.py --workspace "D:\\记忆"
  python detect_dead_links.py --workspace "D:\\记忆" --output report.md
  python detect_dead_links.py --workspace "D:\\记忆","D:\\Work" --parallel  # 并行扫描多个仓库
        """
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default="D:\\记忆",
        help="要扫描的工作空间路径 (默认：D:\\记忆)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出 Markdown 报告路径 (可选)"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="显示详细检查结果"
    )
    
    args = parser.parse_args()
    
    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"❌ 工作区不存在：{workspace}")
        return 1
    
    # 开始扫描
    stats = scan_workspace(workspace)
    stats['_timestamp'] = str(datetime.now())
    
    # 控制台摘要
    print(f"\n📊 扫描结果:")
    print(f"   总文件数：{stats['total_files']}")
    print(f"   总链接数：{stats['total_links']}")
    print(f"   ✅ 正常链接：{stats['resolved_links']}")
    print(f"   ❌ 断裂链接：{stats['broken_links_count']}")
    
    if stats['broken_links']:
        print(f"\n⚠️  发现 {stats['broken_links_count']} 个断裂链接:")
        for i, item in enumerate(stats['broken_links'][:5], 1):
            print(f"   {i}. `[[{item['link']}]]` ← `{os.path.basename(item['source'])}`")
        
        if len(stats['broken_links']) > 5:
            print(f"   ... 还有 {len(stats['broken_links']) - 5} 个")
    
    if stats['orphaned_files']:
        print(f"\n📁 发现 {len(stats['orphaned_files'])} 个孤立文件")
    
    if stats['circular_references']:
        print(f"\n🔄 发现 {len(stats['circular_references'])} 个循环引用")
    
    # 保存报告
    if args.output:
        report_md = generate_markdown_report(stats, workspace)
        output_path = Path(args.output)
        output_path.write_text(report_md, encoding='utf-8')
        print(f"\n💾 报告已保存到：{output_path}")
    
    # 返回非零退出码表示有断裂链接
    return 0 if stats['broken_links_count'] == 0 else 1


if __name__ == "__main__":
    exit(main())
