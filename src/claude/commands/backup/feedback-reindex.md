---
description: Rebuild feedback index from all feedback sources (AI analysis, code reviews, reports, sessions)
argument-hint:
model: opus
allowed-tools: Bash, Read, Glob
---

# /feedback-reindex - Rebuild Unified Feedback Index

Rebuild `devforgeai/feedback/index.json` from ALL feedback sources.

**Invoke CLI:**
```bash
devforgeai-validate feedback-reindex --project-root=. --format=text
```

---

**BACKUP** - Original command before spec-driven-feedback migration
**Backed up:** 2026-03-16
