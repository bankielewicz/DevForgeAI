---
description: Search feedback history with filters and pagination
argument-hint: [query] [--severity] [--status] [--limit] [--page]
model: opus
allowed-tools: Skill
---

# /feedback-search - Search Feedback History

Search and filter feedback history with pagination support.
## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT read feedback index files directly
- ❌ DO NOT parse or filter feedback entries manually
- ❌ DO NOT build result sets or sort entries
- ❌ NEVER perform search or aggregation workflows

**DO (command responsibilities only):**
- ✅ MUST validate argument format and ranges
- ✅ MUST set context markers (Query, Severity, Status, Limit, Page)
- ✅ MUST invoke skill immediately after validation

## Phase 0: Parse Arguments

```
QUERY    = First positional argument (optional, default: "")
SEVERITY = --severity option (low | medium | high | critical)
STATUS   = --status option (open | resolved | archived)
LIMIT    = --limit option (default: 10)
PAGE     = --page option (default: 1)
```

**Validate inputs:**
```
Query Too Long: IF len(QUERY) > 200 → "Error: Query exceeds maximum length of 200 characters" → HALT
Invalid Limit:  IF LIMIT < 1 OR LIMIT > 1000 → "Error: Limit must be between 1 and 1000" → HALT
Invalid Page:   IF PAGE < 1 OR not integer → "Error: Page must be a positive integer" → HALT
Empty Feedback: IF feedback history empty → "No feedback collected. Run '/feedback' to start collecting" → HALT
```

## Phase 1: Invoke Skill

**Set context markers and invoke:**
```
**Search Query:** ${QUERY}  **Severity:** ${SEVERITY}  **Status:** ${STATUS}  **Limit:** ${LIMIT}  **Page:** ${PAGE}
Skill(command="devforgeai-feedback")
```

## Phase 2: Display Results

**Success response (with results):** Display feedback entries returned by skill including
feedback_id, timestamp, story_id, operation, severity, summary, status, and next_page_info.

**Success response (no results):**
```
No feedback found for query "${QUERY}".
Run '/feedback' to start collecting or check query format.
See: .claude/skills/devforgeai-feedback/references/feedback-search-help.md
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Query too long | Reduce query to under 200 characters |
| Invalid limit | Use --limit value between 1 and 1000 |
| Invalid page | Use --page=1 or higher positive integer |
| No feedback history | Run /feedback command to capture feedback first |

## References

- Skill: `.claude/skills/devforgeai-feedback/SKILL.md`
- Extended docs: `.claude/skills/devforgeai-feedback/references/feedback-search-help.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**

## Related Commands

- `/feedback` - Capture feedback (creates searchable entries)
- `/feedback-config` - Configure search behavior
- `/export-feedback` - Export search results
- `/orchestrate` - Auto-captures feedback during workflows

## See Also

- devforgeai-feedback skill (search implementation)
- STORY-016: Searchable Metadata Index
- devforgeai/feedback/feedback-index.json (search index)
- devforgeai/feedback/feedback-register.md (feedback storage)