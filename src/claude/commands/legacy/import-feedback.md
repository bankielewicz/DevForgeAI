---
description: Import feedback sessions from exported ZIP package
argument-hint: "<archive-path>"
model: opus
allowed-tools: Skill
---

# /import-feedback - Import Feedback Sessions

Import feedback sessions from a shared ZIP package exported by another DevForgeAI project or maintainer.

## Quick Reference

```bash
# Import from current directory
/import-feedback feedback-export.zip

# Import from absolute path
/import-feedback ~/Downloads/feedback-export-2025-11-11.zip

# Import from relative path
/import-feedback ../shared-feedback/export.zip
```

---

## Command Workflow

### Phase 0: Parse Arguments

```
ARCHIVE_PATH = First positional argument (required)
  - Must end with .zip
  - Must be a valid file path (relative or absolute)
  - If missing → Error: "Archive path is required. Usage: /import-feedback <path-to-zip>"
```

**Validate:**
```
IF ARCHIVE_PATH is empty: HALT "Archive path is required"
IF ARCHIVE_PATH does not end with ".zip": HALT "Archive must be a .zip file"
```

### Phase 1: Invoke Skill

**Set context markers:**
```
**Feedback Mode:** import
**Archive:** ${ARCHIVE_PATH}
**Feedback Source:** manual
```

**Invoke skill:**
```
Skill(command="spec-driven-feedback")
```

### Phase 2: Display Results

Display import confirmation from skill (sessions imported, duplicates resolved, next steps).

---

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT extract ZIP archives manually
- ❌ DO NOT validate ZIP contents manually
- ❌ DO NOT read/write feedback files directly
- ❌ DO NOT update index files directly
- ❌ DO NOT invoke Python scripts directly

**DO (command responsibilities only):**
- ✅ MUST validate archive path is provided
- ✅ MUST validate .zip extension
- ✅ MUST set context markers
- ✅ MUST invoke skill immediately after validation

All import logic lives in: `src/claude/skills/spec-driven-feedback/phases/phase-03-feedback-execution.md` (import sub-workflow)

---

## Error Handling

| Error | Resolution |
|-------|------------|
| File not found | Check file path (use absolute path if needed) |
| Not a valid ZIP | Re-export or request re-export from source |
| Framework version incompatible | Check manifest.json for min_framework_version |
| Permission denied | Check write permissions for devforgeai/feedback/ |

---

## Integration

**Invokes:** spec-driven-feedback skill (import sub-workflow)
**Related:** `/export-feedback` (create packages to share), `/feedback-reindex` (rebuild index after import)
**Python Backend:** `src/feedback_export_import.py` (invoked by skill, not by command)

---

**Token Budget:** ~800 tokens (lean orchestrator)
**Status:** Production Ready — Migrated to spec-driven-feedback
