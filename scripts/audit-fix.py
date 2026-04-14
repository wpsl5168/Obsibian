#!/usr/bin/env python3
"""
小贝知识库审计修复脚本
批量为缺失 Frontmatter 的文件补上标准格式
"""
import os
import re
from datetime import datetime

VAULT = os.path.expanduser("~/obsidian-vault")

# 文件 -> (title, date, tags) 映射
# 只处理没有 frontmatter 的文件
FILES_META = {
    # === AI-Agent-Daily ===
    "AI-Agent-Daily/2026-04-09.md": ("AI Agent Daily Brief 2026-04-09", "2026-04-09", ["AI-Agent", "Daily-Brief", "MCP", "Claude-Code"]),
    "AI-Agent-Daily/2026-04-10.md": ("AI Agent Daily Brief 2026-04-10", "2026-04-10", ["AI-Agent", "Daily-Brief", "MCP", "Claude-Code"]),
    "AI-Agent-Daily/2026-04-11.md": ("AI Agent Daily Brief 2026-04-11", "2026-04-11", ["AI-Agent", "Daily-Brief", "MCP", "Claude-Code"]),
    "AI-Agent-Daily/2026-04-12.md": ("AI Agent Daily Brief 2026-04-12", "2026-04-12", ["AI-Agent", "Daily-Brief", "MCP", "Claude-Code"]),
    "AI-Agent-Daily/2026-04-13.md": ("AI Agent Daily Brief 2026-04-13", "2026-04-13", ["AI-Agent", "Daily-Brief", "MCP", "Claude-Code"]),
    
    # === 00-Inbox ===
    "00-Inbox/2026-04-11-AI-Agent-研究报告.md": ("AI Agent 研究报告（10大主题）", "2026-03-28", ["AI-Agent", "LLM", "MCP", "RAG", "研究报告"]),
    "00-Inbox/2026-04-12-AI-Agent-研究报告.md": ("AI Agent 研究报告（10大主题）副本", "2026-03-28", ["AI-Agent", "LLM", "MCP", "RAG", "研究报告", "duplicate"]),
    
    # === 根目录散落文件 ===
    "20260402-Claude Code架构分析.md": ("Claude Code 架构深度解析与创新分析", "2026-04-02", ["AI-Agent", "Claude-Code", "MCP", "架构分析"]),
    "00-写作与排版规范.md": ("写作与排版规范", "2026-04-08", ["规范", "写作", "知识库"]),
    
    # === 04-项目开发/BrickHub ===
    "04-项目开发/BrickHub/4.5-BrickHub_Architecture_Vision.md": ("BrickHub 项目总体架构与愿景", "2026-04-08", ["BrickHub", "架构", "项目开发"]),
    "04-项目开发/BrickHub/4.6-BrickHub_Technical_Research.md": ("BrickHub 进阶技术研究蓝图", "2026-04-09", ["BrickHub", "Three.js", "PBR", "LDraw"]),
    "04-项目开发/BrickHub/4.7-BrickHub_LDraw_Standard_Assets.md": ("BrickHub 标准 LDraw 测试素材库", "2026-04-09", ["BrickHub", "LDraw", "测试素材"]),
    "04-项目开发/BrickHub/4.8-BrickHub_Interactive_Engine_Architecture.md": ("BrickHub 2.0 互动拼搭引擎架构白皮书", "2026-04-10", ["BrickHub", "TDD", "架构", "Three.js"]),
    "04-项目开发/BrickHub/4.9-BrickHub_Engineering_Principles_and_Lessons.md": ("BrickHub 工程原则与血泪教训总结", "2026-04-10", ["BrickHub", "工程原则", "教训"]),
    "04-项目开发/BrickHub/Gemini提示词.md": ("BrickHub Gemini/Copilot 提示词模板", "2026-04-08", ["BrickHub", "提示词", "Gemini", "Copilot"]),
    
    # === 05-日常笔记/ClaudeCode ===
    "05-日常笔记/ClaudeCode-工具/00-Overview.md": ("Claude Code 概览（落地导向）", "2026-04-07", ["Claude-Code", "Vibe-Coding", "AI-Agent"]),
    
    # === 10-Topics/Learning/DeepLearning.AI ===
    "10-Topics/Learning/DeepLearning.AI/updates/2026-04-09-deeplearningai-update.md": ("DeepLearning.AI 每日更新 2026-04-09", "2026-04-09", ["DeepLearning-AI", "学习", "课程"]),
    "10-Topics/Learning/DeepLearning.AI/updates/2026-04-10-deeplearningai-update.md": ("DeepLearning.AI 每日更新 2026-04-10", "2026-04-10", ["DeepLearning-AI", "学习", "课程"]),
    "10-Topics/Learning/DeepLearning.AI/updates/2026-04-11-deeplearningai-update.md": ("DeepLearning.AI 每日更新 2026-04-11", "2026-04-11", ["DeepLearning-AI", "学习", "课程"]),
    "10-Topics/Learning/DeepLearning.AI/updates/2026-04-12-deeplearningai-update.md": ("DeepLearning.AI 每日更新 2026-04-12", "2026-04-12", ["DeepLearning-AI", "学习", "课程"]),
    "10-Topics/Learning/DeepLearning.AI/updates/2026-04-13-deeplearningai-update.md": ("DeepLearning.AI 每日更新 2026-04-13", "2026-04-13", ["DeepLearning-AI", "学习", "课程"]),
    "10-Topics/Learning/DeepLearning.AI/digests/2026-04-09-digest.md": ("DeepLearning.AI 每日简报 2026-04-09", "2026-04-09", ["DeepLearning-AI", "学习", "摘要"]),
    "10-Topics/Learning/DeepLearning.AI/digests/2026-04-10-digest.md": ("DeepLearning.AI 每日观察 2026-04-10", "2026-04-10", ["DeepLearning-AI", "学习", "摘要"]),
    "10-Topics/Learning/DeepLearning.AI/digests/2026-04-11-digest.md": ("DeepLearning.AI 每日解读 2026-04-11", "2026-04-11", ["DeepLearning-AI", "学习", "摘要"]),
    "10-Topics/Learning/DeepLearning.AI/digests/2026-04-12-digest.md": ("DeepLearning.AI 每日简报 2026-04-12", "2026-04-12", ["DeepLearning-AI", "学习", "摘要"]),
    "10-Topics/Learning/DeepLearning.AI/digests/2026-04-13-digest.md": ("DeepLearning.AI 每日总结 2026-04-13", "2026-04-13", ["DeepLearning-AI", "学习", "摘要"]),
    
    # === 99-Governance (Agent Memory 日志) ===
    "99-Governance/OpenClaw-Memory/Daily/2026-03-28.md": ("OpenClaw Memory 2026-03-28", "2026-03-28", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-03-29.md": ("OpenClaw Memory 2026-03-29", "2026-03-29", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-03-30.md": ("OpenClaw Memory 2026-03-30", "2026-03-30", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-03-30-agent-connection.md": ("Agent 连接调试记录", "2026-03-30", ["OpenClaw", "Agent", "调试"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-02.md": ("OpenClaw Memory 2026-04-02", "2026-04-02", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-02-agent-security.md": ("Agent 安全策略讨论", "2026-04-02", ["OpenClaw", "安全", "AI-Agent"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-02-notebooklm-api.md": ("NotebookLM API 调研", "2026-04-02", ["NotebookLM", "API", "LLM"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-04-xiongan-travel.md": ("雄安出差记录", "2026-04-04", ["出差", "雄安", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-07.md": ("OpenClaw Memory 2026-04-07", "2026-04-07", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-07-summary.md": ("2026-04-07 压缩汇总", "2026-04-07", ["OpenClaw", "Memory", "汇总"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-07-email-debug.md": ("邮件调试记录", "2026-04-07", ["OpenClaw", "邮件", "调试"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-08.md": ("OpenClaw Memory 2026-04-08", "2026-04-08", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-08-daily-brief.md": ("Daily Brief 构建记录", "2026-04-08", ["OpenClaw", "Daily-Brief", "Pipeline"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-08-obsidian-migration.md": ("知识库全面重构总结", "2026-04-08", ["OpenClaw", "Obsidian", "知识库", "迁移"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-09.md": ("OpenClaw Memory 2026-04-09", "2026-04-09", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-09-brickhub-model.md": ("BrickHub 大模型检查记录", "2026-04-09", ["BrickHub", "LLM", "OpenClaw"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-10.md": ("OpenClaw Memory 2026-04-10", "2026-04-10", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-11.md": ("OpenClaw Memory 2026-04-11", "2026-04-11", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/2026-04-12.md": ("OpenClaw Memory 2026-04-12", "2026-04-12", ["OpenClaw", "Memory", "日志"]),
    "99-Governance/OpenClaw-Memory/Daily/SQLServer_Dacpac包加密与自动化部署.md": ("SQLServer Dacpac加密部署（Memory副本）", "2026-04-08", ["SQL-Server", "Dacpac", "安全", "duplicate"]),
}

def has_frontmatter(content):
    return content.strip().startswith("---")

def add_frontmatter(filepath, title, date, tags):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if has_frontmatter(content):
        return False
    
    tags_str = ", ".join(tags)
    fm = f'---\ntitle: "{title}"\ndate: {date}\ntags: [{tags_str}]\n---\n\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fm + content)
    
    return True

count = 0
for rel_path, (title, date, tags) in FILES_META.items():
    full_path = os.path.join(VAULT, rel_path)
    if os.path.exists(full_path):
        if add_frontmatter(full_path, title, date, tags):
            count += 1
            print(f"  ✅ 已添加 Frontmatter: {rel_path}")
        else:
            print(f"  ⏭️ 已有 Frontmatter: {rel_path}")
    else:
        print(f"  ❌ 文件不存在: {rel_path}")

print(f"\n共修复 {count} 个文件的 Frontmatter")
