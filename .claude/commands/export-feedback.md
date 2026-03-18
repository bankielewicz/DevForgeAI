---
description: Export feedback sessions to portable ZIP package
argument-hint: "[--date-range RANGE] [--sanitize true/false] [--output PATH]"
model: opus
allowed-tools: Skill
---

# /export-feedback - Export Feedback Sessions

Export feedback sessions into a portable, shareable ZIP package with optional sanitization for privacy.

## Quick Reference

```bash
# Export last 30 days (default, with sanitization)
/export-feedback

# Export specific date range
/export-feedback --date-range last-7-days
/export-feedback --date-range last-90-days
/export-feedback --date-range all

# Export without sanitization (maintainers only)
/export-feedback --sanitize false

# Export to custom location
/export-feedback --output ~/feedback-exports/
```

---

## Command Workflow

### Phase 0: Parse Arguments

```
DATE_RANGE = --date-range option (default: "last-30-days")
  Valid: "last-7-days", "last-30-days", "last-90-days", "all"
  Invalid → Error: "Invalid date range. Valid: last-7-days, last-30-days, last-90-days, all"

SANITIZE = --sanitize option (default: "true")
  Valid: "true", "false"
  Invalid → Error: "Invalid sanitize value. Valid: true, false"

OUTPUT = --output option (default: current directory)
```

### Phase 1: Invoke Skill

**Set context markers:**
```
**Feedback Mode:** export
**Date Range:** ${DATE_RANGE}
**Sanitize:** ${SANITIZE}
**Output:** ${OUTPUT}
**Feedback Source:** manual
```

**Invoke skill:**
```
Skill(command="spec-driven-feedback")
```

### Phase 2: Display Results

Display export confirmation from skill (archive path, size, session count, sanitization status).

---

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT read feedback session files directly
- ❌ DO NOT create ZIP archives manually
- ❌ DO NOT apply sanitization patterns manually
- ❌ DO NOT write export files directly
- ❌ DO NOT invoke Python scripts directly

**DO (command responsibilities only):**
- ✅ MUST validate argument format and ranges
- ✅ MUST set context markers
- ✅ MUST invoke skill immediately after validation

All export logic lives in: `src/claude/skills/spec-driven-feedback/phases/phase-03-feedback-execution.md` (export sub-workflow)

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No sessions match date range | Use broader range (e.g., `all`) |
| Permission denied | Check output directory write permissions |
| No feedback exists | Run `/feedback` or `/dev` to generate feedback first |

---

## Integration

**Invokes:** spec-driven-feedback skill (export sub-workflow)
**Related:** `/import-feedback` (import exported packages), `/feedback-export-data` (single-file export)
**Python Backend:** `src/feedback_export_import.py` (invoked by skill, not by command)

---

**Token Budget:** ~800 tokens (lean orchestrator)
**Status:** Production Ready — Migrated to spec-driven-feedback
