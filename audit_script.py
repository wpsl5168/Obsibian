#!/usr/bin/env python3
"""审计Obsidian知识库文件"""
import os
import re
from pathlib import Path

def check_frontmatter(content):
    """检查是否有frontmatter"""
    if content.startswith('---\n'):
        end = content.find('\n---\n', 4)
        return end > 0
    return False

def is_hollow(content, title):
    """检查是否是空洞文件"""
    # 移除frontmatter
    if content.startswith('---\n'):
        end = content.find('\n---\n', 4)
        if end > 0:
            content = content[end+5:]
    
    # 去除空白行
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # 计算实质内容（排除标题、TODO、占位符）
    real_content = []
    for line in lines:
        if line.startswith('#'):  # 标题
            continue
        if 'TODO' in line.upper() or '待完善' in line or '占位' in line:
            continue
        if re.match(r'^[>\-\*\s]+$', line):  # 只有符号
            continue
        real_content.append(line)
    
    real_text = '\n'.join(real_content)
    
    # 判断标准：实质内容<500字
    is_empty = len(real_text) < 500
    
    # 或标题包含"待完善"
    title_hollow = '待完善' in title or 'TODO' in title
    
    return is_empty or title_hollow, len(real_text)

def audit_files(base_dir):
    """审计文件"""
    base_path = Path(base_dir).expanduser()
    
    issues = {
        'no_frontmatter': [],
        'hollow': [],
        'dead_links': []  # 暂不实现，需要更复杂的逻辑
    }
    
    # 扫描AI模型与Agent目录
    target_dir = base_path / '10-知识库' / 'AI模型与Agent'
    if not target_dir.exists():
        print(f"目录不存在: {target_dir}")
        return issues
    
    for md_file in target_dir.rglob('*.md'):
        if md_file.name == 'README.md':
            continue
            
        try:
            content = md_file.read_text(encoding='utf-8')
            title = md_file.stem
            
            # 检查frontmatter
            if not check_frontmatter(content):
                issues['no_frontmatter'].append(str(md_file.relative_to(base_path)))
            
            # 检查空洞内容
            is_empty, char_count = is_hollow(content, title)
            if is_empty:
                issues['hollow'].append({
                    'path': str(md_file.relative_to(base_path)),
                    'chars': char_count,
                    'title': title
                })
        except Exception as e:
            print(f"处理文件出错 {md_file}: {e}")
    
    return issues

if __name__ == '__main__':
    issues = audit_files('~/obsidian-vault')
    
    print("=== 审计报告 ===\n")
    
    print(f"❌ 缺失Frontmatter: {len(issues['no_frontmatter'])}个")
    for f in issues['no_frontmatter']:
        print(f"  - {f}")
    
    print(f"\n⚠️  空洞文件: {len(issues['hollow'])}个")
    # 按字符数排序
    hollow_sorted = sorted(issues['hollow'], key=lambda x: x['chars'])
    for item in hollow_sorted:
        print(f"  - {item['path']} (实质内容{item['chars']}字)")
    
    print(f"\n总计问题: {len(issues['no_frontmatter']) + len(issues['hollow'])}个")
