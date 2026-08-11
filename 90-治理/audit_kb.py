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
    """提取所有wiki链接"""
    return re.findall(r'\[\[([^\]]+)\]\]', content)

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
    dead_links = []
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
        
        try:
            content = md.read_text(encoding='utf-8')
        except Exception as e:
            print(f"⚠️  无法读取: {rel_path} - {e}")
            continue
        
        # 检查frontmatter
        if not has_frontmatter(content):
            missing_fm.append(str(rel_path))
        
        # 检查死链
        links = extract_links(content)
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

            # 支持相对当前文档目录的链接
            if not exists:
                relative_candidate = (md.parent / normalized).with_suffix('.md')
                exists = relative_candidate.exists()

            if not exists:
                dead_links.append((str(rel_path), target))
        
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
    
    print(f"\n🔗 死链: {len(dead_links)} 处")
    for src, target in dead_links[:15]:
        print(f"   - {src} → [[{target}]]")
    if len(dead_links) > 15:
        print(f"   ... 还有 {len(dead_links)-15} 处")
    
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
        'dead_links': dead_links,
        'hollow_files': hollow_files
    }

if __name__ == '__main__':
    results = scan_vault()
