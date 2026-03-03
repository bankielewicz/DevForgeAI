---
description: Generate and maintain project documentation automatically
argument-hint: [STORY-ID | --type=TYPE | --mode=MODE]
model: opus
allowed-tools: Read, Glob, Skill, AskUserQuestion
---

# /document - Automated Documentation Generation

Generate project documentation from stories (greenfield) or codebase analysis (brownfield).

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT generate documentation content or templates
- ❌ DO NOT perform codebase analysis or discovery
- ❌ DO NOT format or display multi-format output
- ❌ DO NOT list templates inline (skill handles --list-templates)

**DO (command responsibilities only):**
- ✅ MUST parse arguments (STORY-ID, --type, --mode, --export, --list-templates)
- ✅ MUST validate story file exists (if STORY-ID provided)
- ✅ MUST set context markers for skill
- ✅ MUST invoke skill immediately after validation

---

## Phase 0: Argument Validation

```
STORY_ID = ""; TYPE = "readme"; MODE = "greenfield"; EXPORT = "markdown"

IF $1 matches "STORY-[0-9]+":
    STORY_ID = $1
    @devforgeai/specs/Stories/${STORY_ID}*.story.md
    IF not found: Display "Story not found: ${STORY_ID}" → HALT
ELIF $1 == "--list-templates":
    Display: "Available templates: readme, developer-guide, api, troubleshooting, contributing, changelog, architecture"
    Display: "Usage: /document --type=<template-name>"
    EXIT
ELIF $1 starts with "--type=": TYPE = value
ELIF $1 starts with "--mode=": MODE = value
ELIF $1 starts with "--export=": EXPORT = value
ELIF $1 not empty:
    Display: "Invalid argument: $1"
    Display: "Usage: /document [STORY-ID | --type=TYPE | --mode=MODE]"
    HALT
```

---

## Phase 1: Invoke Skill

**Story ID:** ${STORY_ID}
**Documentation Type:** ${TYPE}
**Mode:** ${MODE}
**Export Format:** ${EXPORT}

```
Skill(command="devforgeai-documentation")
```

**Skill handles ALL workflow** including mode detection, discovery, content generation, template application, validation, and export.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Story not found | Verify STORY-NNN format, check devforgeai/specs/Stories/ |
| Context files missing | Run `/create-context` first |
| No completed stories | Use `--mode=brownfield` or wait for story completion |
| Export dependency missing | Install pandoc/wkhtmltopdf, or use markdown fallback |
| Coverage below 80% | Add docs for undocumented items, re-run |

---

## References

- Skill: `.claude/skills/devforgeai-documentation/SKILL.md`
- Help: `.claude/skills/devforgeai-documentation/references/document-help.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
