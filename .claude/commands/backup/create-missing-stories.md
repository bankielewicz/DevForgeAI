---
description: Create stories for all detected coverage gaps in an epic
argument-hint: "EPIC-NNN [--help]"
model: opus
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill
---

# /create-missing-stories - Batch Story Creation

Create stories for all detected gaps in an epic using batch mode.
## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- DO NOT run gap-detector.sh directly or iterate over features
- DO NOT create story files directly or format batch summaries
- NEVER perform gap detection, story creation, or display formatting

**DO (command responsibilities only):**
- MUST validate EPIC-NNN argument and verify epic exists
- MUST collect shared metadata via AskUserQuestion (supports "Set individually per story")
- MUST set context markers including Batch Index, Batch Total, Created From

## Phase 0: Argument Validation

```
ARG = $ARGUMENTS
IF ARG == "--help" OR ARG == "help": GOTO display_help
IF ARG empty: Display "Epic ID required. Usage: /create-missing-stories EPIC-NNN" -> HALT
IF NOT matches "^EPIC-[0-9]{3}$" (case-insensitive):
    Display "Invalid epic ID: ${ARG}. Expected: EPIC-NNN" -> HALT
EPIC_ID = normalize(ARG)
Verify: Glob("devforgeai/specs/Epics/${EPIC_ID}*.epic.md")
IF not found: Display "Epic not found: ${EPIC_ID}" + valid epics -> HALT
```

## Phase 1: Gap Detection + Metadata + Batch Creation

```
**Epic ID:** ${EPIC_ID}
**Mode:** detect
Skill(command="validating-epic-coverage")
```
After skill returns gap data, collect metadata via AskUserQuestion:
- **Sprint:** Backlog (default) / Current Sprint / Next Sprint
- **Priority:** Medium / High / Low / Set individually per story
- **Points:** 5 / 3 / 8 / Set individually per story

INDIVIDUAL_PRIORITY / INDIVIDUAL_POINTS = true if "Set individually" selected.
Invoke batch creation with context markers:

```
**Epic ID:** ${EPIC_ID}
**Mode:** create
**Sprint:** ${SPRINT}  **Priority:** ${PRIORITY}  **Points:** ${POINTS}
**Individual Priority:** ${INDIVIDUAL_PRIORITY}
**Individual Points:** ${INDIVIDUAL_POINTS}
**Batch Mode:** true  **Batch Total:** ${gap_count}
**Created From:** /create-missing-stories
Skill(command="validating-epic-coverage")
```

## Help Text

```
/create-missing-stories - Create stories for coverage gaps

USAGE:
    /create-missing-stories EPIC-NNN

ARGUMENTS:
    EPIC-NNN    Required. Epic ID (e.g., EPIC-015). Case-insensitive.

DESCRIPTION:
    Detects gaps, prompts for metadata, creates stories in batch
    with progress display and failure isolation per story.

EXAMPLES:
    /create-missing-stories EPIC-015

OUTPUT:
    - Gap count summary, progress display, success/failure report

ERROR HANDLING:
    - Invalid ID: format help. Not found: lists valid epics
    - No features: suggests /ideate. 100% coverage: success
    - Creation failure: continues to next (no rollback)

RELATED COMMANDS:
    /validate-epic-coverage  Check coverage first
    /create-story            Create individual story
    /dev                     Start story implementation

EXIT CODES:
    0  Success  1  Partial success  2  Error
```

## References

- Skill: `.claude/skills/validating-epic-coverage/SKILL.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`
