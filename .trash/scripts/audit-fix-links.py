#!/usr/bin/env python3
"""
小贝知识库审计修复 Part 3：补充双向链接
在有关联的文件之间添加 [[]] 链接
"""
import os
import re

VAULT = os.path.expanduser("~/obsidian-vault")

# 定义需要添加双向链接的映射
# (file_path, search_text, replace_text) 
# 用精确的文本查找替换来添加链接

LINK_FIXES = [
    # === 20260402-Claude Code架构分析.md ===
    # 链接到 MCP 规范
    ("20260402-Claude Code架构分析.md",
     "深度集成 **MCP (Model Context Protocol)**",
     "深度集成 **[[MCP规范|MCP]] (Model Context Protocol)**"),
    # 链接到 AI-Agent架构
    ("20260402-Claude Code架构分析.md",
     "更是一套成熟的 **Agent 操作系统**",
     "更是一套成熟的 **[[AI-Agent架构|Agent 操作系统]]**"),
    # 链接到 SWE-Agent
    ("20260402-Claude Code架构分析.md",
     "顶级 AI 工具的差距不在于模型本身",
     "顶级 AI 工具的差距不在于模型本身（另见 [[SWE-Agent实战]]）"),
    
    # === AI-Agent-Daily 系列 - 链接到知识星球 ===
    # 2026-04-13
    ("AI-Agent-Daily/2026-04-13.md",
     "## MCP（官方）",
     "## [[MCP规范|MCP]]（官方）"),
    ("AI-Agent-Daily/2026-04-13.md",
     "## Claude Code（官方）",
     "## [[20260402-Claude Code架构分析|Claude Code]]（官方）"),
    
    # 2026-04-12
    ("AI-Agent-Daily/2026-04-12.md",
     "## MCP（官方）",
     "## [[MCP规范|MCP]]（官方）"),
    ("AI-Agent-Daily/2026-04-12.md",
     "## Claude Code（官方）",
     "## [[20260402-Claude Code架构分析|Claude Code]]（官方）"),
    
    # 2026-04-11
    ("AI-Agent-Daily/2026-04-11.md",
     "## MCP（官方）",
     "## [[MCP规范|MCP]]（官方）"),
    ("AI-Agent-Daily/2026-04-11.md",
     "## Claude Code（官方）",
     "## [[20260402-Claude Code架构分析|Claude Code]]（官方）"),
    
    # 2026-04-10
    ("AI-Agent-Daily/2026-04-10.md",
     "## MCP（官方）",
     "## [[MCP规范|MCP]]（官方）"),
    ("AI-Agent-Daily/2026-04-10.md",
     "## Claude Code（官方）",
     "## [[20260402-Claude Code架构分析|Claude Code]]（官方）"),
    
    # 2026-04-09
    ("AI-Agent-Daily/2026-04-09.md",
     "## MCP（官方）",
     "## [[MCP规范|MCP]]（官方）"),
    ("AI-Agent-Daily/2026-04-09.md",
     "## Claude Code（官方）",
     "## [[20260402-Claude Code架构分析|Claude Code]]（官方）"),
    
    # === 04-项目开发/BrickHub 系列互相链接 ===
    ("04-项目开发/BrickHub/4.5-BrickHub_Architecture_Vision.md",
     "# BrickHub 项目总体架构与愿景",
     "# BrickHub 项目总体架构与愿景\n\n> 相关文档：[[4.6-BrickHub_Technical_Research|技术研究]] · [[4.7-BrickHub_LDraw_Standard_Assets|LDraw素材库]] · [[4.8-BrickHub_Interactive_Engine_Architecture|互动引擎]] · [[4.9-BrickHub_Engineering_Principles_and_Lessons|工程教训]]"),
    
    ("04-项目开发/BrickHub/4.6-BrickHub_Technical_Research.md",
     "# BrickHub 进阶技术研究蓝图",
     "# BrickHub 进阶技术研究蓝图\n\n> 相关文档：[[4.5-BrickHub_Architecture_Vision|架构愿景]] · [[4.8-BrickHub_Interactive_Engine_Architecture|互动引擎]] · [[4.9-BrickHub_Engineering_Principles_and_Lessons|工程教训]]"),
    
    ("04-项目开发/BrickHub/4.8-BrickHub_Interactive_Engine_Architecture.md",
     "# BrickHub 2.0 互动拼搭引擎架构选型与技术白皮书 (TDD)",
     "# BrickHub 2.0 互动拼搭引擎架构选型与技术白皮书 (TDD)\n\n> 相关文档：[[4.5-BrickHub_Architecture_Vision|架构愿景]] · [[4.6-BrickHub_Technical_Research|技术研究]] · [[4.9-BrickHub_Engineering_Principles_and_Lessons|工程教训]]"),
    
    ("04-项目开发/BrickHub/4.9-BrickHub_Engineering_Principles_and_Lessons.md",
     "# BrickHub 工程原则与血泪教训总结 (4.9)",
     "# BrickHub 工程原则与血泪教训总结 (4.9)\n\n> 相关文档：[[4.5-BrickHub_Architecture_Vision|架构愿景]] · [[4.6-BrickHub_Technical_Research|技术研究]] · [[4.8-BrickHub_Interactive_Engine_Architecture|互动引擎]]"),
    
    # === 05-日常笔记/ClaudeCode-工具 链接 ===
    ("05-日常笔记/ClaudeCode-工具/00-Overview.md",
     "# Claude Code 概览（落地导向）",
     "# Claude Code 概览（落地导向）\n\n> 深度架构分析见 [[20260402-Claude Code架构分析]] · MCP 协议见 [[MCP规范]]"),
    
    # === 03-日常灵感 SQL Server 系列互链 ===
    ("03-日常灵感/SQLServer_存储过程加密方案_WITH_ENCRYPTION.md",
     "# SQL Server 存储过程加密方案",
     "# SQL Server 存储过程加密方案\n\n> 系列文档：[[SQLServer_Dacpac包加密与自动化部署|Dacpac加密部署]] · [[SQLServer_高级加密方案_CLR_混淆|CLR高级混淆]]"),
    
    ("03-日常灵感/SQLServer_高级加密方案_CLR_混淆.md",
     "# SQL Server 高级加密方案",
     "# SQL Server 高级加密方案\n\n> 系列文档：[[SQLServer_存储过程加密方案_WITH_ENCRYPTION|WITH ENCRYPTION基础方案]] · [[SQLServer_Dacpac包加密与自动化部署|Dacpac加密部署]]"),
    
    # === 00-Inbox 研究报告 链接到知识星球子目录 ===
    ("00-Inbox/2026-04-11-AI-Agent-研究报告.md",
     "# AI Agent 研究报告（10 大主题｜偏一手来源）",
     "# AI Agent 研究报告（10 大主题｜偏一手来源）\n\n> 知识星球对应章节：[[4.1-AI_Agent核心心智模型|Agent心智模型]] · [[4.2-工作流编排模式|工作流编排]] · [[3.2-Model_Context_Protocol规范解析|MCP规范]] · [[3.3-RAG系统架构与演进|RAG系统]] · [[5.1-模型评测基准与Evals驱动开发|Evals评测]] · [[5.3-AI安全护栏与防御机制|安全护栏]]"),
]

count = 0
for rel_path, old_text, new_text in LINK_FIXES:
    full_path = os.path.join(VAULT, rel_path)
    if not os.path.exists(full_path):
        print(f"  ❌ 不存在: {rel_path}")
        continue
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_text not in content:
        print(f"  ⏭️ 未匹配: {rel_path} (可能已处理)")
        continue
    content = content.replace(old_text, new_text, 1)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    print(f"  🔗 已添加双向链接: {rel_path}")

print(f"\n共添加 {count} 处双向链接")
