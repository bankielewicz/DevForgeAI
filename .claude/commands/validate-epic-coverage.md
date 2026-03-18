---
description: Validate epic coverage and report gaps
argument-hint: "[EPIC-ID] [--interactive | --quiet | --ci] [--help]"
model: opus
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill
---

# /validate-epic-coverage - Epic Coverage Validation

Validate epic-to-story coverage and report gaps with actionable commands.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT run gap-detector.sh or generate-report.sh directly
- ❌ DO NOT format coverage displays or tables
- ❌ DO NOT iterate over epic/story files or parse JSON output
- ❌ NEVER perform gap detection, coverage calculation, or display formatting

**DO (command responsibilities only):**
- ✅ MUST validate argument format (EPIC-ID regex or help flag)
- ✅ MUST detect prompt mode (interactive/quiet/ci) and set context markers
- ✅ MUST invoke skill immediately; MAY handle AskUserQuestion AFTER skill returns

## Phase 0: Argument Validation

```
ARG = $ARGUMENTS
IF ARG == "--help" OR ARG == "help": GOTO display_help
PROMPT_MODE = "interactive"
IF "--quiet" in ARGS OR "--ci" in ARGS: PROMPT_MODE = "quiet"
IF ARG provided AND NOT matches "^EPIC-[0-9]{3}$" (case-insensitive):
    Display: "❌ Invalid epic ID format: ${ARG}. Expected: EPIC-NNN" → HALT
MODE = "single" if EPIC-ID provided, else "all"
EPIC_ID = normalize(ARG) if provided
```

## Phase 1: Invoke Skill

```
**Epic ID:** ${EPIC_ID} (or "all")
**Mode:** validate
**Prompt Mode:** ${PROMPT_MODE}
Skill(command="validating-epic-coverage")
```

Skill runs gap detection, coverage analysis, and formats display via subagent.

## Phase 2: Interactive Gap Resolution

After skill returns, if `PROMPT_MODE == "interactive"` and gaps found:
- **Single gap:** AskUserQuestion "Create story for this gap?" → Yes/No/Later
  - If Yes: set context markers, invoke Skill(command="spec-driven-stories")
- **Multiple gaps:** AskUserQuestion "How to proceed?" → Batch/Select/Skip
  - Batch: "Run /create-missing-stories ${EPIC_ID}"
  - Select: multi-select AskUserQuestion, create via story-creation skill
If `PROMPT_MODE == "quiet"`: skip all interactive prompts.

## Help Text

```
/validate-epic-coverage - Validate epic coverage and report gaps

USAGE:
    /validate-epic-coverage [EPIC-ID] [OPTIONS]

ARGUMENTS:
    EPIC-ID     Optional. Validate specific epic (e.g., EPIC-015)
                If omitted, validates all epics in devforgeai/specs/Epics/

OPTIONS:
    --interactive   Enable gap-to-story prompts (default in terminal)
    --quiet         Suppress interactive prompts (for scripting)
    --ci            Same as --quiet, for CI/CD environments
    --help, help    Display this help message

EXAMPLES:
    /validate-epic-coverage
    /validate-epic-coverage EPIC-015
    /validate-epic-coverage EPIC-015 --quiet

OUTPUT:
    - Color-coded coverage indicators (✅ ⚠️ ❌)
    - Per-epic breakdown with feature coverage
    - Actionable /create-story commands for gaps
    - Framework-wide coverage percentage
    - Interactive gap resolution prompts (unless --quiet)

RELATED COMMANDS:
    /create-story           Create story to fill coverage gap
    /create-missing-stories Batch create stories for all gaps
    /create-epic            Create new epic with features

EXIT CODES:
    0    Success (validation completed)
    1    Error (invalid arguments or file system error)
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Invalid EPIC-ID | Expected EPIC-NNN format, case-insensitive |
| Epic not found | Lists valid epics from devforgeai/specs/Epics/ |
| No epics dir | "Run /create-epic to create epics" |

## References

- Skill: `.claude/skills/validating-epic-coverage/SKILL.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`
