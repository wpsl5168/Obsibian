#!/usr/bin/env python3
import os
import shutil
import re
from datetime import datetime

vault = '/home/wpsl5168/.openclaw/workspace/obsidian-vault'

def ensure_dirs():
    dirs = ['01-新闻速递', '02-AI知识星球', '03-日常灵感', '04-项目开发', '05-日常笔记', '00-Index']
    for d in dirs:
        os.makedirs(os.path.join(vault, d), exist_ok=True)

def process_file(filepath, filename):
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already processed or is an index/readme
    if content.startswith('---') or 'README' in filename or '00-Overview' in filename:
        return

    # Determine category and destination
    dest_dir = '05-日常笔记'
    category = 'Notes'
    tags = ['daily']

    content_lower = content.lower()
    
    if 'brief' in filename.lower() or '简报' in content_lower or 'ai圈每日简报' in content:
        dest_dir = '01-新闻速递'
        category = 'News'
        tags = ['news', 'ai-agent', 'brief']
    elif '研究报告' in content_lower or 'mcp' in content_lower or 'agent' in content_lower:
        dest_dir = '02-AI知识星球'
        category = 'AI-Architecture'
        tags = ['ai', 'architecture']
    elif 'sql' in content_lower or 'dacpac' in content_lower or 'encryption' in content_lower:
        dest_dir = '03-日常灵感'
        category = 'SQL-Server'
        tags = ['sql', 'database', 'security']

    # Generate frontmatter
    date_str = datetime.now().strftime('%Y-%m-%d')
    frontmatter = f"""---
title: "{filename.replace('.md', '')}"
date: {date_str}
category: {category}
tags: [{', '.join(tags)}]
---
"""
    
    # Very basic bi-directional link injection for SQL Server concepts (Mock logic for Xiaobei)
    if 'SQL Server' in content and '[[SQL Server]]' not in content:
         content = content.replace('SQL Server', '[[SQL Server]]')
    if 'MCP' in content and '[[MCP]]' not in content:
         content = content.replace('MCP', '[[MCP]]')
    if 'Agent' in content and '[[AI Agent]]' not in content:
         content = content.replace('Agent', '[[AI Agent]]')

    new_content = frontmatter + '\n' + content
    
    dest_path = os.path.join(vault, dest_dir, filename)
    with open(dest_path, 'w') as f:
        f.write(new_content)
    
    if dest_path != filepath:
         os.remove(filepath)
         print(f"Moved and formatted: {filename} -> {dest_dir}/")
    else:
         print(f"Formatted: {filename}")

def main():
    ensure_dirs()
    # Find root and specific directory files to migrate
    for root, dirs, files in os.walk(vault):
        if '.git' in root or any(d in root for d in ['01-', '02-', '03-', '04-', '05-', '00-']):
            continue
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file), file)
    print("Migration complete. Generating index...")
    
    # Generate Index
    index_path = os.path.join(vault, '00-Index', '00-全局知识索引.md')
    with open(index_path, 'w') as f:
        f.write("---\ntitle: 全局知识索引\ndate: 2026-04-08\ncategory: Index\ntags: [index]\n---\n# 老王的知识网络库\n\n- [[01-新闻速递]]\n- [[02-AI知识星球]]\n- [[03-日常灵感]]\n- [[04-项目开发]]\n- [[05-日常笔记]]\n")

if __name__ == '__main__':
    main()