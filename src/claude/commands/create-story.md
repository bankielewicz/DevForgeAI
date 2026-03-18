---
description: Create user story with acceptance criteria and technical specification
argument-hint: [feature-description | epic-id]
model: opus
allowed-tools: Glob, Skill, AskUserQuestion
---

# /create-story - Create User Story

Transform feature → story with AC, tech spec, UI spec. Single or batch mode.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT search epic files for feature lists
- ❌ DO NOT prompt user for feature selection or batch metadata
- ❌ DO NOT read epic content to analyze features
- ❌ DO NOT create manual task lists
- ❌ NEVER perform parsing, selection, or collection workflows

**DO (command responsibilities only):**
- ✅ MUST validate argument format (epic ID regex or 10+ word description)
- ✅ MUST set context markers (Mode, Epic ID or Feature Description)
- ✅ MUST invoke skill immediately after validation

## Phase 0: Argument Validation

```
ARG = $ARGUMENTS

IF ARG matches ^[Ee][Pp][Ii][Cc]-\d{3}$:
    epic_files = Glob(pattern="devforgeai/specs/Epics/${EPIC_ID}*.epic.md")
    IF not found: Display "Epic not found" → HALT
    MODE = "EPIC_BATCH"
    **Mode:** EPIC_BATCH
    **Epic ID:** ${EPIC_ID}

ELIF word_count(ARG) >= 10:
    MODE = "SINGLE_STORY"
    **Mode:** SINGLE_STORY
    **Feature Description:** ${ARG}

ELSE:
    AskUserQuestion(questions=[{
        question: "Create a single story or batch from epic?",
        header: "Mode",
        options: [{label: "Single story"}, {label: "Batch from epic"}]
    }])
```

## Phase 1: Invoke Skill

```
Skill(command="spec-driven-stories")
```

**Skill handles ALL workflow** including parsing, selection, creation, validation, and linking.

## Error Handling

| Error | Resolution |
|-------|------------|
| Epic not found | Verify EPIC-NNN format, check devforgeai/specs/Epics/ |
| Description too brief | Provide 10+ words describing user capability |
| Skill failed | Check .claude/skills/spec-driven-stories/SKILL.md exists |

## References

- Skill: `.claude/skills/spec-driven-stories/SKILL.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
