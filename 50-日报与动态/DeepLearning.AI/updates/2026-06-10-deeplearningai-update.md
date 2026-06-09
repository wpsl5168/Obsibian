# DeepLearning.AI 课程同步 — 2026-06-10

**同步状态**: ❌ FAILED  
**尝试时间**: 2026-06-10 20:10:36 UTC  
**报告时间**: 2026-06-10 (Asia/Shanghai)

## 问题描述

本次同步尝试在 **Cloudflare WAF 阻挡** 导致失败。

### 阻挡详情
- **HTTP 状态**: 403 Forbidden
- **服务**: deeplearning.ai (所有子域)
- **原因**: IP 被 Cloudflare 识别为潜在 bot，或超过速率限制
- **Ray ID**: a092c84a2877a0d5 / a092c8ff3d6046c8

### 尝试方法（全部失败）
1. ❌ `curl` 带 User-Agent 模拟浏览器
2. ❌ `browser_navigate` via Browserbase  
3. ❌ Algolia 搜索 API (algolia.net)
4. ❌ Sitemap.xml 访问
5. ❌ 直接 HTTP HEAD 请求

## 上次成功同步

| 字段 | 值 |
|------|-----|
| **日期** | 2026-06-04 |
| **课程总数** | 124 |
| **快照文件** | `deeplearningai-courses-2026-06-04.json` |
| **变更** | 无 (vs 2026-06-01) |

## 建议行动

### 立即
- ⏳ 等待 1-12 小时，Cloudflare 可能自动解除阻挡
- 📍 考虑配置代理 IP 或 VPN 重试

### 长期
- 🔄 评估 Cloudflare 对自动化爬虫的持续阻挡政策
- 📡 寻找 DeepLearning.AI 数据的备选来源：
  - GitHub 上的课程列表镜像
  - RSS feed 或公开 API
  - 直接向 DeepLearning.AI 申请 API 访问

### 操作化
```bash
# 重试（当 Cloudflare 解除阻挡后）
cd ~/obsidian-vault && hermes cron run deeplearningai-sync

# 或手动触发
curl -s https://www.deeplearning.ai/courses/ | python3 parse_courses.py
```

## 日志

```
2026-06-10T20:10:36Z [INFO] Starting DeepLearning.AI sync...
2026-06-10T20:10:40Z [ERROR] Cloudflare 403 Forbidden - All endpoints blocked
2026-06-10T20:10:45Z [ERROR] Algolia API - No response
2026-06-10T20:10:50Z [WARN] Sync aborted - retry in 6-12 hours
```

---

**Next sync**: 2026-06-11 (自动)  
**Manual retry**: `hermes cron run deeplearningai-sync --force`
