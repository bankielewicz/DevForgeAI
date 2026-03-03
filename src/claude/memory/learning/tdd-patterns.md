---
last_updated: 2026-02-02T10:00:00Z
total_patterns: 1
version: 1.0
---

# TDD Patterns Learned

Cross-story pattern learning for TDD workflow optimization. Patterns with >=3 occurrences are surfaced; <3 are "emerging" and not displayed.

## Confidence Levels

| Level | Occurrences | Description |
|-------|-------------|-------------|
| high | >=10 | Pattern validated across many stories |
| medium | >=5 | Pattern gaining confidence |
| low | >=3 | Pattern detected, monitoring |
| emerging | <3 | Not surfaced until threshold met |

---

## Pattern: clean-tdd-cycle

**Occurrences:** 5
**Confidence:** medium (>=5 occurrences)
**Last Seen:** STORY-341

**Description:** TDD cycle completes with single iteration per phase when story has clear acceptance criteria.

**When to Apply:**
- Story has clear, unambiguous AC
- No external dependencies
- Well-defined input/output contracts
- All prerequisite stories completed

**Examples:**
- STORY-339: ADR story completed in single iteration
- STORY-341: Session memory layer completed cleanly
- STORY-340: Framework insights added efficiently
- STORY-337: Observation capture phases added
- STORY-353: Token reduction validation passed

---

## Pattern Schema Reference

```yaml
pattern_entry:
  pattern_id: "string (hash of category + keywords)"
  occurrences: "integer >= 1"
  confidence: "enum: emerging|low|medium|high"
  last_seen: "STORY-NNN"
  description: "string"
  when_to_apply: "array of conditions"
  examples: "array (max 5 story IDs)"
```
