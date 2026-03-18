# Self-Contained Reference Inventory

## Overview

The `spec-driven-feedback` skill contains ALL reference files and templates locally. No external dependencies on other skills for reference material.

**Migration Note:** Absorbed from `devforgeai-feedback` per ADR-040. All references previously loaded from `.claude/skills/devforgeai-feedback/references/` are now self-contained within this skill's `references/` directory.

---

## Reference Files (13)

| Reference File | Purpose | Loaded In Phase |
|----------------|---------|-----------------|
| `context-extraction.md` | OperationContext data model, extraction patterns | Phase 01 |
| `context-sanitization.md` | Secret/PII removal patterns, redaction markers | Phase 01 |
| `adaptive-questioning.md` | Question selection algorithm, variable substitution | Phase 02 (conversation) |
| `feedback-question-templates.md` | Question library by operation type and status | Phase 02 (conversation, checklist, ai_analysis) |
| `template-format-specification.md` | Template YAML structure, field definitions | Phase 02 (base) |
| `template-examples.md` | Sample templates for all 7 types | Phase 02 |
| `feedback-analysis-patterns.md` | Trend analysis, pattern detection, temporal analysis | Phase 04 |
| `field-mapping-guide.md` | Template field mappings, response handling | Phase 04 |
| `feedback-persistence-guide.md` | File naming, session format, index structure | Phase 05 |
| `feedback-export-formats.md` | JSON, CSV, Markdown export schemas | Phase 02 (metrics, export, import), Phase 05 |
| `triage-workflow.md` | 6-phase triage workflow for recommendation conversion | Phase 02/03 (triage type) |
| `feedback-search-help.md` | Query syntax, filter options, pagination | Phase 02 (search type) |
| `user-customization-guide.md` | Configuration options, template customization | Phase 02 (config type) |

---

## Template Files (7)

| Template | Trigger Condition |
|----------|-------------------|
| `command-passed.yaml` | Command completed successfully |
| `command-failed.yaml` | Command failed |
| `skill-passed.yaml` | Skill completed successfully |
| `skill-failed.yaml` | Skill failed |
| `subagent-passed.yaml` | Subagent completed successfully |
| `subagent-failed.yaml` | Subagent failed |
| `generic.yaml` | Fallback for unknown operation types |

Templates are located at: `templates/` (relative to skill directory).

---

## Hook System Documentation

| File | Purpose |
|------|---------|
| `HOOK-SYSTEM.md` | Event-driven hook architecture documentation (STORY-018) |

Located at skill root: `HOOK-SYSTEM.md` (relative to skill directory).

---

## Loading Convention

Phase files use `Read()` with paths relative to the skill directory:

```
# CORRECT — relative to skill directory
Read(file_path="references/context-extraction.md")

# WRONG — do not use old shared paths
Read(file_path=".claude/skills/devforgeai-feedback/references/context-extraction.md")
```

Each phase loads its references FRESH. Do NOT rely on previous reads. This prevents the "already covered" rationalization that leads to token optimization bias.
