---
description: Generate and maintain project documentation automatically
argument-hint: "[STORY-ID | --type=TYPE | --mode=MODE | --audit=dryrun | --audit-fix --type=TYPE]"
model: sonnet
allowed-tools: Read, Glob, Skill, AskUserQuestion
---

# /document - Automated Documentation Generation

Generate project documentation from stories (greenfield), codebase analysis (brownfield), or audit existing documentation for DevEx quality.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT generate documentation content or templates
- ❌ DO NOT perform codebase analysis or discovery
- ❌ DO NOT perform audit scoring or fix classification
- ❌ DO NOT format or display multi-format output
- ❌ DO NOT list templates inline (skill handles --list-templates)

**DO (command responsibilities only):**
- ✅ MUST parse arguments (STORY-ID, --type, --mode, --export, --list-templates, --audit, --audit-fix, --finding)
- ✅ MUST validate story file exists (if STORY-ID provided)
- ✅ MUST validate audit file exists (if --audit-fix provided)
- ✅ MUST set context markers for skill
- ✅ MUST invoke skill immediately after validation

---

## Quick Reference

```bash
# Generation modes (existing)
/document STORY-040              # Generate docs for specific story
/document --type=readme          # Generate specific type
/document --mode=brownfield      # Analyze codebase
/document --export=html          # Export format
/document --list-templates       # Show available templates

# Audit modes (new)
/document --audit=dryrun                    # Score docs, generate findings file
/document --audit-fix --type=all            # Fix all findings
/document --audit-fix --type=license        # Fix license findings only
/document --audit-fix --type=tone           # Fix tone findings only
/document --audit-fix --type=formatting     # Fix formatting findings only
/document --audit-fix --type=architecture   # Fix architecture findings only
/document --audit-fix --type=onboarding     # Fix onboarding findings only
/document --audit-fix --type=community      # Fix community file findings only
/document --audit-fix --finding=F-003       # Fix single finding
```

---

## Phase 0: Argument Validation

```
STORY_ID = ""; TYPE = "readme"; MODE = "greenfield"; EXPORT = "markdown"
AUDIT_MODE = null; AUDIT_FIX = false; FINDING_FILTER = "all"

FOR arg in $ARGUMENTS:
    IF arg matches "STORY-[0-9]+":
        STORY_ID = arg
        @devforgeai/specs/Stories/${STORY_ID}*.story.md
        IF not found: Display "Story not found: ${STORY_ID}" → HALT

    ELIF arg == "--list-templates":
        Display: "Available templates: readme, developer-guide, api, troubleshooting, contributing, changelog, architecture"
        Display: ""
        Display: "Audit types: all, license, community, tone, architecture, formatting, onboarding"
        Display: ""
        Display: "Usage:"
        Display: "  /document --type=<template-name>        Generate docs"
        Display: "  /document --audit=dryrun                Audit docs"
        Display: "  /document --audit-fix --type=<audit-type>  Fix findings"
        EXIT

    ELIF arg starts with "--audit=":
        AUDIT_MODE = value   # Expected: "dryrun"
        IF AUDIT_MODE != "dryrun":
            Display: "Invalid audit mode: ${AUDIT_MODE}. Only 'dryrun' is supported."
            HALT

    ELIF arg == "--audit-fix":
        AUDIT_FIX = true

    ELIF arg starts with "--type=":
        TYPE = value

    ELIF arg starts with "--mode=":
        MODE = value

    ELIF arg starts with "--export=":
        EXPORT = value

    ELIF arg starts with "--finding=":
        FINDING_FILTER = value   # Expected: "F-NNN"
        IF FINDING_FILTER does not match "F-[0-9]+":
            Display: "Invalid finding ID: ${FINDING_FILTER}. Expected format: F-001"
            HALT

    ELIF arg not empty:
        Display: "Invalid argument: ${arg}"
        Display: "Usage: /document [STORY-ID | --type=TYPE | --mode=MODE | --audit=dryrun | --audit-fix --type=TYPE]"
        HALT

# Validate audit-fix has an audit file to consume
IF AUDIT_FIX == true:
    audit_file = "devforgeai/qa/audit/doc-audit.json"
    result = Read(file_path=audit_file)
    IF result fails:
        Display: "No audit file found at ${audit_file}."
        Display: "Run '/document --audit=dryrun' first to generate findings."
        HALT
```

---

## Phase 1: Invoke Skill

**Story ID:** ${STORY_ID}
**Documentation Type:** ${TYPE}
**Mode:** ${MODE}
**Export Format:** ${EXPORT}
**Audit Mode:** ${AUDIT_MODE}
**Audit Fix:** ${AUDIT_FIX}
**Finding Filter:** ${FINDING_FILTER}

```
Skill(command="devforgeai-documentation")
```

**Skill handles ALL workflow:**
- If AUDIT_MODE set → Phase A (audit scoring, findings generation)
- If AUDIT_FIX set → Phase B (fix classification, execution, verification)
- Otherwise → Phases 0-7 (existing generation workflow)

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Story not found | Verify STORY-NNN format, check devforgeai/specs/Stories/ |
| Context files missing | Run `/create-context` first |
| No completed stories | Use `--mode=brownfield` or wait for story completion |
| Export dependency missing | Install pandoc/wkhtmltopdf, or use markdown fallback |
| Coverage below 80% | Add docs for undocumented items, re-run |
| No audit file found | Run `/document --audit=dryrun` first |
| Invalid finding ID | Use format F-NNN (e.g., F-001) |
| Invalid audit mode | Only `dryrun` is supported |

---

## References

- Skill: `.claude/skills/devforgeai-documentation/SKILL.md`
- Help: `.claude/skills/devforgeai-documentation/references/document-help.md`
- Audit workflow: `.claude/skills/devforgeai-documentation/references/audit-workflow.md`
- Fix catalog: `.claude/skills/devforgeai-documentation/references/audit-fix-catalog.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
