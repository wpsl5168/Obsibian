#!/usr/bin/env python3
"""知识库审计脚本 - 检查Frontmatter、死链、空洞内容"""
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

VAULT_ROOT = Path.home() / "obsidian-vault"
MIN_SUBSTANTIAL_CHARS = 500

def has_frontmatter(content: str) -> bool:
    """检查是否有YAML frontmatter"""
    return content.strip().startswith('---') and '\n---' in content[3:]

def extract_links(content: str) -> List[str]:
    """提取正文 WikiLink，忽略 fenced code 与 inline code 中的示例。"""
    without_fences = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    without_code = re.sub(r'`[^`\n]*`', '', without_fences)
    return re.findall(r'\[\[([^\]]+)\]\]', without_code)

def is_hollow(filepath: Path, content: str) -> Tuple[bool, str]:
    """判断文件是否空洞，返回(是否空洞, 原因)"""
    # 移除frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]
        else:
            body = content
    else:
        body = content
    
    # 统计实质内容长度
    body_clean = re.sub(r'#+ .*\n', '', body)  # 移除标题
    body_clean = re.sub(r'^\s*[-*]\s+.*\n', '', body_clean, flags=re.MULTILINE)  # 移除空列表项
    body_clean = body_clean.strip()
    
    if len(body_clean) < MIN_SUBSTANTIAL_CHARS:
        # 检查是否包含待完善标记
        if any(x in content.lower() for x in ['待完善', '待补充', 'todo', 'tbd', '占位']):
            return True, f"短内容({len(body_clean)}字)且含待完善标记"
        if len(body_clean) < 200:
            return True, f"内容过短({len(body_clean)}字)"
    
    return False, ""

def scan_vault():
    """扫描知识库"""
    print("=" * 80)
    print("知识库审计报告")
    print("=" * 80)
    
    missing_fm = []
    missing_fm_governed = []
    dead_links = []
    dead_links_governed = []
    hollow_files = []
    
    # 构建文件映射：同时支持 [[文件名]]、[[目录/文件]]、相对路径链接
    all_files_by_stem = {}
    all_paths_no_ext = set()
    for md in VAULT_ROOT.rglob("*.md"):
        if '.trash' in str(md) or '.obsidian' in str(md):
            continue
        all_files_by_stem.setdefault(md.stem, []).append(md)
        all_paths_no_ext.add(md.relative_to(VAULT_ROOT).with_suffix('').as_posix())
    
    # 扫描文件
    for md in VAULT_ROOT.rglob("*.md"):
        if '.trash' in str(md) or '.obsidian' in str(md):
            continue
        
        rel_path = md.relative_to(VAULT_ROOT)
        governed = rel_path.parts and rel_path.parts[0] in {
            '10-知识库', '20-项目', '40-调研报告'
        }
        
        try:
            content = md.read_text(encoding='utf-8')
        except Exception as e:
            print(f"⚠️  无法读取: {rel_path} - {e}")
            continue
        
        # 检查frontmatter
        if not has_frontmatter(content):
            missing_fm.append(str(rel_path))
            if governed:
                missing_fm_governed.append(str(rel_path))
        
        # 检查死链
        # 根目录 log.md 是 append-only 治理历史，其中保留旧链接映射示例，
        # 不是可点击知识正文，不能据此制造死链告警。
        links = [] if rel_path.as_posix() == 'log.md' else extract_links(content)
        for link in links:
            # 处理别名 [[target|alias]] 与锚点 [[target#section]]
            target = link.split('|')[0].split('#')[0].strip().replace('\\', '/')
            if not target:
                continue

            normalized = target[:-3] if target.endswith('.md') else target
            exists = normalized in all_paths_no_ext

            # Obsidian 的短链接按文件名解析
            if not exists and '/' not in normalized:
                exists = normalized in all_files_by_stem

            # 支持相对当前文档目录的链接。不能直接对无扩展名目标
            # 调用 with_suffix('.md')：如 `4.1-标题` 会被 Path 误判为
            # 带 `.1-标题` 后缀并截断，制造假死链。
            if not exists:
                target_path = md.parent / normalized
                relative_candidate = (
                    target_path if target_path.suffix == '.md'
                    else Path(f"{target_path}.md")
                )
                exists = relative_candidate.exists()

            if not exists:
                dead_links.append((str(rel_path), target))
                if governed:
                    dead_links_governed.append((str(rel_path), target))
        
        # 检查空洞内容（仅限知识库核心区域）
        if '10-知识库' in str(rel_path) and not any(x in str(rel_path) for x in ['archive', 'Topics-archive', 'README']):
            is_h, reason = is_hollow(md, content)
            if is_h:
                hollow_files.append((str(rel_path), reason))
    
    # 输出结果
    print(f"\n📋 总计扫描: {len(list(VAULT_ROOT.rglob('*.md')))} 个文件")
    print(f"\n❌ 缺少Frontmatter: {len(missing_fm)} 个")
    for f in missing_fm[:20]:
        print(f"   - {f}")
    if len(missing_fm) > 20:
        print(f"   ... 还有 {len(missing_fm)-20} 个")
    print(f"   其中 Schema 治理区: {len(missing_fm_governed)} 个")
    
    print(f"\n🔗 死链: {len(dead_links)} 处")
    for src, target in dead_links[:15]:
        print(f"   - {src} → [[{target}]]")
    if len(dead_links) > 15:
        print(f"   ... 还有 {len(dead_links)-15} 处")
    print(f"   其中 Schema 治理区: {len(dead_links_governed)} 处")
    
    print(f"\n📄 空洞/骨架文件: {len(hollow_files)} 个")
    for f, reason in hollow_files[:20]:
        print(f"   - {f}")
        print(f"     理由: {reason}")
    if len(hollow_files) > 20:
        print(f"   ... 还有 {len(hollow_files)-20} 个")
    
    print("\n" + "=" * 80)
    
    # 返回详细数据供后续使用
    return {
        'missing_fm': missing_fm,
        'missing_fm_governed': missing_fm_governed,
        'dead_links': dead_links,
        'dead_links_governed': dead_links_governed,
        'hollow_files': hollow_files
    }

if __name__ == '__main__':
    results = scan_vault()
