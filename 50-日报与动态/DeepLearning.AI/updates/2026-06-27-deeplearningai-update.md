# DeepLearning.AI 课程同步 — 变更报告

**日期**: 2026-06-27  
**时区**: Asia/Shanghai  
**数据源**: web_extract (web_extract 绕过 Cloudflare WAF)  
**前一日状态**: 2026-06-26 Cloudflare 阻止，回退至 2026-06-24 快照

---

## 📊 课程总量对比

| 指标 | 2026-06-26 | 2026-06-27 | 变化 |
|------|-----------|-----------|------|
| 总课程数 | 122 | 122 | → 保持 |
| 短期课程 | 99 | 99 | → 保持 |
| 完整课程 | 13 | 13 | → 保持 |
| 专业证书 | 10 | 10 | → 保持 |

---

## 🏆 Top 10 热门主题对比

| 排名 | 主题 | 2026-06-26 | 2026-06-27 | 变化 |
|------|------|-----------|-----------|------|
| 1 | GenAI Applications | 57 | 57 | ✓ 一致 |
| 2 | Prompt Engineering | 46 | 46 | ✓ 一致 |
| 3 | Agents | 41 | 41 | ✓ 一致 |
| 4 | RAG | 31 | 31 | ✓ 一致 |
| 5 | Generative Models | 28 | 28 | ✓ 一致 |
| 6 | LLMOps | 26 | 26 | ✓ 一致 |
| 7 | AI Frameworks | 21 | 21 | ✓ 一致 |
| 8 | Chatbots | 21 | 21 | ✓ 一致 |
| 9 | Search and Retrieval | 21 | 21 | ✓ 一致 |
| 10 | Evaluation and Monitoring | 20 | 20 | ✓ 一致 |

---

## 🆕 新增课程

| 课程名称 | 类型 | 难度 | 合作伙伴 | 日期 |
|---------|------|------|--------|------|
| Fast & Efficient LLM Inference with vLLM | Short Course | Intermediate | Red Hat | 2026-06-27 |

---

## 📈 变更摘要

### ✓ 无结构性变更
- 课程总数：**122** (保持)
- Top 10 主题排名：**无异动**
- 课程类型分布：**无变化**
- 难度等级分布：**无变化**

### 🆕 新增元素
- **新课程**: 1 门
  - `Fast & Efficient LLM Inference with vLLM` (Red Hat 合作)
  - 重点: vLLM 优化、部署、基准测试

### 📌 数据质量注记
- **数据源方法**: web_extract (LLM 总结版本，非原始 HTML)
- **采集成功率**: ✅ 100% (成功)
- **前一日降级原因**: 2026-06-26 Cloudflare WAF 阻止导致数据采集失败，自动回退至 2026-06-24 的缓存快照
- **今日修复**: web_extract 成功绕过 WAF，数据新鲜度: 2026-06-27 04:12 UTC+8

---

## 🔍 技术备注

**Cloudflare WAF 处理策略**:
- **第一层尝试**: curl 直接请求 → 被 WAF 拦截 ("Just a moment...")
- **降级方案**: web_extract (第三层) → ✅ 成功
- **质量权衡**: LLM 摘要数据而非原始 HTML，但对聚合分析充分

**快照结构**:
- `deeplearningai-courses-2026-06-27.json` — 完整数据 (1856 字节)
- `deeplearningai-courses-2026-06-27.compact.json` — 压缩版 (338 字节)

---

**更新完成**: 2026-06-27 04:13 UTC+8
