#!/usr/bin/env python3
"""
小贝知识库审计修复 Part 2：为 README 文件添加 Frontmatter
"""
import os

VAULT = os.path.expanduser("~/obsidian-vault")

README_META = {
    "01-新闻速递/README.md": ("01-新闻速递 索引", "2026-04-08", ["索引", "新闻"]),
    "02-AI知识星球/README.md": ("02-AI知识星球 索引", "2026-04-08", ["索引", "AI-Agent", "知识图谱"]),
    "03-日常灵感/README.md": ("03-日常灵感 索引", "2026-04-08", ["索引", "SQL-Server", "灵感"]),
    "04-项目开发/README.md": ("04-项目开发 索引", "2026-04-08", ["索引", "BrickHub", "项目"]),
    "05-日常笔记/README.md": ("05-日常笔记 索引", "2026-04-08", ["索引", "笔记"]),
    "assets/README.md": ("资源库 索引", "2026-04-08", ["索引", "资源"]),
    "99-Governance/OpenClaw-Memory/Daily/README.md": ("OpenClaw Memory 索引", "2026-04-08", ["索引", "OpenClaw", "Memory"]),
}

count = 0
for rel_path, (title, date, tags) in README_META.items():
    full_path = os.path.join(VAULT, rel_path)
    if not os.path.exists(full_path):
        continue
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.strip().startswith("---"):
        continue
    tags_str = ", ".join(tags)
    fm = f'---\ntitle: "{title}"\ndate: {date}\ntags: [{tags_str}]\n---\n\n'
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(fm + content)
    count += 1
    print(f"  ✅ README Frontmatter: {rel_path}")

print(f"\n共修复 {count} 个 README 的 Frontmatter")
