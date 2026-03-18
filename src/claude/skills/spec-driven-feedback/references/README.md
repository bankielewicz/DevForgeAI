# Shared Reference Strategy

## Overview

The `spec-driven-feedback` skill shares ALL reference files and templates with the original `devforgeai-feedback` skill. No files are copied — they are loaded via explicit `Read()` paths during each phase.

## Why Shared References

Following the established pattern from `spec-driven-dev` (shares with `spec-driven-dev`), `spec-driven-qa` (shares with `devforgeai-qa`), and `spec-driven-ideation` (shares with `spec-driven-ideation`):

1. **No drift** — Single source of truth for reference content
2. **No maintenance burden** — Updates to `devforgeai-feedback` references automatically apply
3. **Lean skill** — `spec-driven-feedback` contains only its unique value: the EVG phase files
4. **Rollback safe** — If `spec-driven-feedback` is removed, `devforgeai-feedback` remains fully functional

## Reference File Locations

All references are loaded from: `.claude/skills/devforgeai-feedback/references/`

| Reference File | Loaded In Phase | Content |
|----------------|-----------------|---------|
| `context-extraction.md` | Phase 01 | OperationContext data model, extraction patterns |
| `context-sanitization.md` | Phase 01 | Secret/PII removal patterns, redaction markers |
| `adaptive-questioning.md` | Phase 02 (conversation/checklist) | Question selection algorithm, variable substitution |
| `feedback-question-templates.md` | Phase 02 | Question library by operation type and status |
| `template-format-specification.md` | Phase 02 | Template YAML structure, field definitions |
| `template-examples.md` | Phase 02 | Sample templates for all 7 types |
| `feedback-analysis-patterns.md` | Phase 04 | Trend analysis, pattern detection, temporal analysis |
| `field-mapping-guide.md` | Phase 04 | Template field mappings, response handling |
| `feedback-persistence-guide.md` | Phase 05 | File naming, session format, index structure |
| `feedback-export-formats.md` | Phase 05 | JSON, CSV, Markdown export schemas |
| `triage-workflow.md` | Phase 03 (triage type) | 6-phase triage workflow for recommendation conversion |
| `feedback-search-help.md` | Commands only | Query syntax, filter options, pagination |
| `user-customization-guide.md` | Commands only | Configuration options, template customization |

## Template Locations

All templates are loaded from: `.claude/skills/devforgeai-feedback/templates/`

| Template | When Used |
|----------|-----------|
| `command-passed.yaml` | Command completed successfully |
| `command-failed.yaml` | Command failed |
| `skill-passed.yaml` | Skill completed successfully |
| `skill-failed.yaml` | Skill failed |
| `subagent-passed.yaml` | Subagent completed successfully |
| `subagent-failed.yaml` | Subagent failed |
| `generic.yaml` | Fallback for unknown operation types |

## Other Shared Files

| File | Location | Purpose |
|------|----------|---------|
| `HOOK-SYSTEM.md` | `.claude/skills/devforgeai-feedback/HOOK-SYSTEM.md` | Event-driven hook architecture documentation |

## Loading Convention

Phase files use explicit, absolute `Read()` paths — NEVER relative paths:

```
# CORRECT
Read(file_path=".claude/skills/devforgeai-feedback/references/context-extraction.md")

# WRONG — do not use relative paths
Read(file_path="../../devforgeai-feedback/references/context-extraction.md")
```

Each phase loads its references FRESH. Do NOT rely on previous reads. This prevents the "already covered" rationalization that leads to token optimization bias.
