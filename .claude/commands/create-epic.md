---
description: Create epic with feature breakdown
argument-hint: [epic-name]
model: opus
allowed-tools: AskUserQuestion, Skill
---

# /create-epic - Create Epic with Feature Breakdown

Creates a new epic with feature breakdown by delegating to the spec-driven-architecture skill.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT perform feature decomposition or technical assessment
- ❌ DO NOT generate display templates or next-steps guidance
- ❌ DO NOT invoke subagents directly (skill handles requirements-analyst, architect-reviewer)
- ❌ DO NOT validate against context files (skill handles framework validation)

**DO (command responsibilities only):**
- ✅ MUST validate epic name format (10-100 chars, alphanumeric/spaces/hyphens)
- ✅ MUST validate schema if ideation output provided (STORY-301)
- ✅ MUST set context markers (epic name, command mode)
- ✅ MUST invoke skill immediately after validation

---

## Quick Reference

```bash
/create-epic User Authentication System
/create-epic Payment Processing Overhaul
/create-epic Real-time Analytics Dashboard
```

---

## Phase 0: Argument Validation

```
epic_name = $ARGUMENTS

IF epic_name is empty:
    Display: "❌ Error: Epic name required"
    Display: "Usage: /create-epic [epic-name]"
    Display: "Example: /create-epic User Authentication System"
    HALT

IF length(epic_name) < 10 OR length(epic_name) > 100:
    Display: "❌ Invalid epic name length (must be 10-100 characters)"
    Display: "Current: '${epic_name}' (${length} characters)"
    HALT

Display: "✓ Epic name: ${epic_name}"
```

### Phase 0.5: Schema Validation (STORY-301)

```
IF ideation_output is provided:
    Read(file_path=".claude/skills/spec-driven-architecture/references/skill-output-schemas.yaml")
    validation_result = validate_ideation_schema(ideation_output)
    IF validation_result.status == "FAILED":
        Display: "❌ Schema validation failed for ideation output"
        HALT
    IF validation_result.status == "PASSED":
        Display: "✓ Schema validation passed"
```

---

## Phase 1: Set Context and Invoke Skill

**Epic name:** $epic_name
**Command:** create-epic
**Mode:** epic-creation

```
Skill(command="spec-driven-architecture")
```

**Skill handles ALL workflow** including discovery (4 AskUserQuestion flows for context gathering), feature decomposition (AskUserQuestion for review loop), technical assessment, epic file creation, context preservation validation (STORY-299), and completion summary.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Epic name empty | AskUserQuestion if interactive, else provide name: `/create-epic [epic-name]` |
| Name too short/long | Must be 10-100 characters |
| Schema validation failed | Fix ideation output format (see architecture skill schema) |
| Skill invocation failed | Verify `.claude/skills/spec-driven-architecture/SKILL.md` exists |
| Epic validation failed | Skill reports critical issues; resolve and retry |

---

## References

- Skill: `.claude/skills/spec-driven-architecture/SKILL.md` (Epic Creation Workflow, EVG-enforced)
- Help: `.claude/skills/spec-driven-architecture/references/create-epic-help.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`
- Guide: `.claude/memory/epic-creation-guide.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
