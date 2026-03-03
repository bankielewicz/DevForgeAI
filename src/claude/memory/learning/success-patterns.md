---
last_updated: 2026-02-02T10:00:00Z
total_patterns: 1
version: 1.0
---

# Success Patterns

Cross-story success pattern tracking for workflow optimization. Captures what works well for future stories.

## Confidence Levels

| Level | Occurrences | Description |
|-------|-------------|-------------|
| high | >=10 | Pattern highly successful, recommended |
| medium | >=5 | Pattern shows promise |
| low | >=3 | Pattern working, needs validation |
| emerging | <3 | Not surfaced until threshold met |

---

## Pattern: parallel-subagent-invocation

**Occurrences:** 8
**Confidence:** medium (>=5 occurrences)
**Last Seen:** STORY-342

**Description:** Invoking multiple independent subagents in parallel reduces total execution time by 30-40%.

**Success Indicators:**
- Reduced total phase time
- No cross-task dependencies
- Clean context isolation
- Consistent results

**When to Apply:**
- Tasks are completely independent
- No shared state between tasks
- Results can be merged afterward
- Maximum 4-6 parallel tasks recommended

**Examples:**
- STORY-342: git-validator + tech-stack-detector in parallel
- STORY-341: Multiple context file reads in parallel
- STORY-340: Validation checks parallelized
- STORY-339: ADR verification + source-tree check parallel
- STORY-337: Observation schema updates parallel

---

## Pattern Schema Reference

```yaml
success_entry:
  pattern_id: "string (unique identifier)"
  occurrences: "integer >= 1"
  confidence: "enum: emerging|low|medium|high"
  last_seen: "STORY-NNN"
  description: "string"
  success_indicators: "array of measurable outcomes"
  when_to_apply: "array of conditions"
  examples: "array (max 5 story IDs)"
```
