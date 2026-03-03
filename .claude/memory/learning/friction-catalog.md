---
last_updated: 2026-02-02T10:00:00Z
total_frictions: 1
version: 1.0
---

# Friction Catalog

Cross-story friction point tracking for workflow improvement. Identifies recurring pain points and their solutions.

## Confidence Levels

| Level | Occurrences | Description |
|-------|-------------|-------------|
| high | >=10 | Friction well-understood, solution validated |
| medium | >=5 | Friction pattern confirmed |
| low | >=3 | Friction detected, monitoring |
| emerging | <3 | Not surfaced until threshold met |

---

## Friction: dependency-chain-verification

**Occurrences:** 3
**Confidence:** low (>=3 occurrences)
**Last Seen:** STORY-342

**Root Cause:** Story dependencies not verified before starting /dev workflow, causing mid-workflow discovery of blockers.

**Solution:**
1. Always check `depends_on` field in story frontmatter
2. Verify prerequisite stories are QA Approved before proceeding
3. Use dependency-graph-analyzer subagent for complex chains
4. HALT with clear message if dependencies incomplete

**Average Resolution Time:** 5-10 minutes (when caught early)

**Examples:**
- STORY-342: Verified STORY-339 and STORY-341 prerequisites
- STORY-341: Verified STORY-339 ADR prerequisite
- STORY-340: Verified prior observation stories

---

## Friction Schema Reference

```yaml
friction_entry:
  friction_id: "string (unique identifier)"
  occurrences: "integer >= 1"
  confidence: "enum: emerging|low|medium|high"
  last_seen: "STORY-NNN"
  root_cause: "string (why this friction occurs)"
  solution: "array (1-5 steps to prevent/resolve)"
  avg_resolution_time: "string (optional)"
  examples: "array (max 5 story IDs)"
```
