---
description: Execute session data mining queries for workflow patterns, errors, and decisions
argument-hint: "[query-type] [options] | --help"
model: opus
allowed-tools: Read, Glob, Grep, Skill, AskUserQuestion
---

# /insights - Session Data Mining Query Interface

Execute insights queries to discover workflow patterns, errors, and decisions from session data.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT perform data mining or pattern analysis
- ❌ DO NOT format result displays or dashboards
- ❌ DO NOT invoke session-miner subagent directly (skill handles this)

**DO (command responsibilities only):**
- ✅ MUST parse query type (dashboard/workflows/errors/decisions/story)
- ✅ MUST validate query type and required parameters
- ✅ MUST handle --help flag display
- ✅ MUST invoke skill immediately after validation

---

## Phase 0: Argument Validation

```
QUERY_TYPE = "dashboard"; QUERY_PARAM = null; STORY_ID = null

IF "--help" in $ARGUMENTS:
    Read(file_path=".claude/skills/devforgeai-insights/references/insights-help.md")
    Display help content from reference file
    EXIT

FOR arg in $ARGUMENTS:
    IF arg in [workflows, errors, decisions, story, command-patterns]:
        QUERY_TYPE = arg
    ELIF arg matches "STORY-[0-9]+":
        STORY_ID = arg
    ELIF arg == "decisions":
        QUERY_PARAM = remaining args

IF QUERY_TYPE not in [dashboard, workflows, errors, decisions, story, command-patterns]:
    Display: "❌ Unknown query type: '${QUERY_TYPE}'"
    Display: "Valid: dashboard, workflows, errors, decisions, story, command-patterns"
    Display: "Usage: /insights [query-type] | /insights --help"
    HALT

IF QUERY_TYPE == "story" AND STORY_ID is empty:
    Display: "❌ Missing STORY-ID. Usage: /insights story STORY-XXX"
    HALT
```

---

## Phase 1: Invoke Skill

**Query Type:** ${QUERY_TYPE}
**Query:** ${QUERY_PARAM}
**Story:** ${STORY_ID}

```
Skill(command="devforgeai-insights", args="--type=${QUERY_TYPE} --query=${QUERY_PARAM} --story=${STORY_ID}")
```

**Skill handles ALL workflow** including session-miner orchestration, pattern analysis, and report generation.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Unknown query type | Valid: dashboard, workflows, errors, decisions, story |
| Missing STORY-ID | Usage: `/insights story STORY-XXX` |
| Skill not found | Verify `.claude/skills/devforgeai-insights/SKILL.md` exists |

---

## References

- Skill: `.claude/skills/devforgeai-insights/SKILL.md`
- Help: `.claude/skills/devforgeai-insights/references/insights-help.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
