# DeepLearning.AI 课程同步失败

**日期**: 2026-06-14  
**原因**: Cloudflare 防火墙阻止  

## 错误描述

无法访问 `https://www.deeplearning.ai/courses/`：

- ❌ curl 请求被 Cloudflare 拦截（HTTP 403 / Challenge）
- ❌ 浏览器访问同样被 Cloudflare bot detection 阻止
- ❌ Wayback Machine 快照加载被本地安全策略拦截

## 最后成功的快照

- **日期**: 2026-06-13
- **课程总数**: 24
- **主要变化**: 从 124 门课程大幅下降至 24 门（可能是网站页面版本更新或 API 返回格式变化）

## 建议

1. 等待 Cloudflare 放行（可能需要配置 User-Agent 或使用代理）
2. 考虑采用 Playwright/Puppeteer 完整浏览器模拟
3. 与 DeepLearning.AI 联系获取官方 API 访问权限

---

*自动同步失败日志*
