# DeepLearning.AI Course Index Update

**Date**: 2026-07-03  
**Fetch Method**: Jina Reader (Layer 3.5, after curl/browser failures)  
**Data Quality**: ✅ Success

## Summary

| Metric | Value |
|--------|-------|
| Total Courses | 124 |
| Regular Courses | 113 |
| Specializations | 11 |
| New Courses | 0 |
| Removed Courses | 0 |
| Status | No Changes |

## Details

### Comparison Base
- **Previous Snapshot**: 2026-07-02 (124 courses)
- **Current Snapshot**: 2026-07-03 (124 courses)

### Change Summary
- ✅ **No new courses added**
- ✅ **No courses removed**
- ✅ **Course catalog stable**

## Catalog Breakdown

### By Type
- **Regular Courses**: 113
- **Professional Certificates / Specializations**: 11

### Top Recent Additions (from catalog)
The course catalog includes recent additions in:
- AI Agents & Agentic Systems
- Inference Optimization (vLLM, SGLang)
- Multimodal Data Pipelines
- Coding Agents & Development Tools

## Data Source Notes

- **Collection Method**: Jina Reader (curl -sL to https://r.jina.ai/)
- **Fallback Chain Level**: 3.5
- **Prior Attempts**: curl + browser_navigate both blocked by Cloudflare WAF v2
- **Success Rate**: 100% (Jina Reader succeeded after primary methods failed)
- **Data Quality**: Structured markdown converted to JSON
- **URL Extraction**: Dual-path grep (courses + specializations), deduplicated

## Validation Checks

- [x] Both path types captured (/courses/ and /specializations/)
- [x] Empty slugs filtered
- [x] No duplicates
- [x] All URLs valid
- [x] JSON structure validated
- [x] Comparison logic verified

---

*Generated automatically by cron task at 2026-07-03 04:10 UTC+8*
