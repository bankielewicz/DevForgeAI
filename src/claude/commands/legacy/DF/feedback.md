---
description: Manual feedback capture (default) or subcommand dispatch (export-data, ...)
argument-hint: "[export-data --format=... --date-range=... --story-ids=... --severity=... --status=...] | [free-form context]"
model: opus
allowed-tools: Skill
---

# /DF:feedback — Manual Feedback Trigger + Subcommand Dispatcher

Two invocation modes routed by the first argument:

1. **Subcommand mode** — first arg matches a known subcommand. Currently: `export-data` (folded in from the deleted `/feedback-export-data` slash command). Parses CLI flags and dispatches to the corresponding `spec-driven-feedback` sub-workflow.
2. **Free-form context mode** (default) — no recognized subcommand. All arguments are joined as a context string and a manual feedback entry is captured.

The slash command is a thin orchestrator. All filtering, indexing, export, and persistence logic lives in `spec-driven-feedback`.

---

## Quick Reference

### Subcommand mode

```bash
# Export filtered feedback data (folded in from /feedback-export-data)
/DF:feedback export-data
/DF:feedback export-data --format=csv
/DF:feedback export-data --format=markdown
/DF:feedback export-data --date-range=2026-05-01..2026-05-21
/DF:feedback export-data --story-ids=STORY-001,STORY-002
/DF:feedback export-data --severity=high --status=open
```

### Free-form context mode (default)

```bash
# Basic usage (no context)
/DF:feedback

# With story context
/DF:feedback STORY-001 after-dev-completion

# With operation context
/DF:feedback regression-testing phase-1

# With detailed context
/DF:feedback STORY-042 qa-validation performance-issue-detected
```

---

## Command Workflow

### Phase 0: Parse Arguments — Subcommand Routing

```
ARGS = command arguments (raw)

# Known subcommand registry. Extend by adding a branch here + matching
# context-marker block in Phase 1.
KNOWN_SUBCOMMANDS = {"export-data"}

IF len(ARGS) >= 1 AND ARGS[0] IN KNOWN_SUBCOMMANDS:
  SUBCOMMAND = ARGS[0]
  SUBARGS    = ARGS[1:]
  mode = "subcommand"
ELSE:
  SUBCOMMAND = null
  CONTEXT    = ARGS joined as string
  mode       = "context"
```

### Phase 0a: Subcommand-Mode Argument Parsing [CONDITIONAL]

**Triggered when:** `mode == "subcommand"` AND `SUBCOMMAND == "export-data"`

Parse CLI-style flags from `SUBARGS`:

```
FORMAT     = --format option (json | csv | markdown, default: json)
DATE_RANGE = --date-range option (YYYY-MM-DD..YYYY-MM-DD, default: empty)
STORY_IDS  = --story-ids option (comma-separated STORY-NNN, default: empty)
SEVERITY   = --severity option (low | medium | high | critical, default: empty)
STATUS     = --status option (open | resolved | archived, default: empty)
```

**Validation:**
- `FORMAT` must be one of `json`, `csv`, `markdown` — else error with guidance.
- `DATE_RANGE`, if present, must match `YYYY-MM-DD..YYYY-MM-DD`.
- `STORY_IDS`, if present, must be a comma-separated list of `STORY-NNN` IDs.
- `SEVERITY`, if present, must be one of `low`, `medium`, `high`, `critical`.
- `STATUS`, if present, must be one of `open`, `resolved`, `archived`.

### Phase 0b: Context-Mode Validation [CONDITIONAL]

**Triggered when:** `mode == "context"`

**Validate context:**
- Max length: 500 characters
- Allowed characters: alphanumeric, hyphens, underscores, spaces
- If exceeds limit or contains invalid characters → error with guidance

---

### Phase 1: Invoke spec-driven-feedback Skill

**Set context markers based on mode:**

```
IF mode == "subcommand" AND SUBCOMMAND == "export-data":
  **Feedback Mode:** export
  **Format:** ${FORMAT}
  **Date Range:** ${DATE_RANGE}
  **Story IDs:** ${STORY_IDS}
  **Severity:** ${SEVERITY}
  **Status:** ${STATUS}
ELSE:  # context mode
  **Feedback Context:** ${CONTEXT}
  **Feedback Source:** manual
```

**Invoke skill:**

```
Skill(command="spec-driven-feedback")
```

**What the skill does:**

- In **export-data** mode: routes to the export sub-workflow, applies the filters, and writes a single-file export (JSON / CSV / Markdown) to `devforgeai/feedback/exports/`.
- In **context** mode: executes 6 EVG-enforced phases (Context Detection → Type Dispatch → Execution → Validation → Persistence → Completion), generates `FB-YYYY-MM-DD-###`, captures session metadata, records to `feedback-register.md` and `index.json`, returns confirmation with feedback ID.

---

### Phase 2: Display Results

**Context-mode success:**

```json
{
  "status": "success",
  "feedback_id": "FB-2026-05-21-001",
  "timestamp": "2026-05-21T14:30:00Z",
  "context": "STORY-001 after-dev-completion",
  "next_steps": "Feedback captured. View recent feedback with: /feedback-search --limit=5",
  "message": "Feedback captured successfully"
}
```

**Export-data success (delegated from skill):**

```json
{
  "status": "success",
  "export_id": "FBEXP-2026-05-21-001",
  "format": "csv",
  "file_path": "devforgeai/feedback/exports/FBEXP-2026-05-21-001.csv",
  "entry_count": 42,
  "filters_applied": {"date_range": "2026-05-01..2026-05-21"}
}
```

**Error response:**

```json
{
  "status": "error",
  "message": "Context exceeds maximum length of 500 characters (received: 537)",
  "suggested_action": "Reduce context length and retry"
}
```

---

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**

- ❌ DO NOT read feedback index files directly
- ❌ DO NOT parse, filter, or format feedback entries
- ❌ DO NOT write export files directly
- ❌ DO NOT write the feedback-register file directly

**DO (command responsibilities only):**

- ✅ MUST detect the subcommand from the first argument
- ✅ MUST validate argument format
- ✅ MUST set context markers
- ✅ MUST invoke `spec-driven-feedback` immediately after validation

All export, filter, and persistence logic lives in `spec-driven-feedback`'s phase files.

---

## Error Handling

### Context Mode

**Invalid Characters in Context**
```
Error: Context contains invalid characters
Constraint: Only alphanumeric, hyphens, underscores, and spaces allowed
Action: Remove special characters and retry
```

**Context Too Long**
```
Error: Context exceeds maximum length of 500 characters
Constraint: Max 500 characters
Action: Reduce context length and retry
```

**Feedback Directory Not Writable**
```
Error: Cannot write to devforgeai/feedback/ directory
Constraint: Requires write permissions
Action: Check directory permissions and retry
```

### Subcommand Mode (export-data)

**Invalid Format**
```
Error: --format must be one of json, csv, markdown (got: yaml)
Action: Use a supported format
```

**Invalid Date Range**
```
Error: --date-range must match YYYY-MM-DD..YYYY-MM-DD
Action: Use ISO dates separated by two dots (e.g. 2026-05-01..2026-05-21)
```

**Invalid Severity / Status**
```
Error: --severity must be one of low, medium, high, critical
Error: --status must be one of open, resolved, archived
```

---

## Success Criteria

### Context Mode

- [x] Feedback ID generated in format FB-YYYY-MM-DD-###
- [x] Timestamp in ISO8601 format
- [x] Context captured (if provided)
- [x] Entry written to feedback-register.md
- [x] Confirmation displayed with next steps
- [x] Validation prevents invalid inputs
- [x] Error messages are actionable
- [x] Exit code 0 (success) or 1 (error)

### Subcommand Mode (export-data)

- [x] Export to JSON, CSV, or Markdown formats
- [x] Selection criteria honored (date range, story IDs, severity, status)
- [x] File path generation with timestamps
- [x] Metadata included (export ID, timestamp, config snapshot)
- [x] Empty export handled (0 entries is valid)
- [x] Validation prevents unsupported formats
- [x] Exit code 0 (success) or 1 (error)

---

## Integration

**Invoked by:** User manually; `spec-driven-lifecycle` (after operation completion).

**Invokes:** `spec-driven-feedback` skill — captures feedback (context mode) or runs the export sub-workflow (subcommand mode).

**Updates:**
- Context mode: `devforgeai/feedback/feedback-register.md` (appends new entry).
- Subcommand mode: `devforgeai/feedback/exports/FBEXP-YYYY-MM-DD-NNN.{json|csv|md}` (new export file).

**Used with:**

- `/feedback-search` — query captured feedback
- `/export-feedback` — ZIP-package export with sanitization (STORY-013, distinct from this subcommand's single-file export)
- `/feedback-config` — configure feedback system
- `/feedback-reindex` — rebuild index

**Distinct from `/export-feedback`:**

| Feature | `/DF:feedback export-data` (folded-in STORY-020) | `/export-feedback` (STORY-013) |
|---------|---------------------------------------------------|--------------------------------|
| **Output** | Single file (JSON / CSV / Markdown) | ZIP package with sessions |
| **Sanitization** | Raw data export | Always applied |
| **Use Case** | Data analysis, reporting | Share with maintainers |
| **Selection** | Date range + story IDs + filters | Date range only |

---

## Examples

### Example 1: Capture After Story Development (context mode)

```bash
/DF:feedback STORY-042 dev-complete all-tests-passing
```

```
Feedback captured: FB-2026-05-21-003
Timestamp: 2026-05-21T15:42:00Z
Context: STORY-042 dev-complete all-tests-passing

Next steps: View recent feedback with: /feedback-search --limit=5
```

### Example 2: Capture During Manual Testing (context mode)

```bash
/DF:feedback manual-testing found-edge-case-bug
```

```
Feedback captured: FB-2026-05-21-004
Timestamp: 2026-05-21T16:15:00Z
Context: manual-testing found-edge-case-bug
```

### Example 3: No Context (context mode)

```bash
/DF:feedback
```

```
Feedback captured: FB-2026-05-21-005
Timestamp: 2026-05-21T16:20:00Z
Context: N/A
```

### Example 4: Export Recent Feedback as CSV (subcommand mode)

```bash
/DF:feedback export-data --format=csv --date-range=2026-05-14..2026-05-21
```

```
Export complete: FBEXP-2026-05-21-001
File: devforgeai/feedback/exports/FBEXP-2026-05-21-001.csv
Entries: 17
Format: csv
Filters: date_range=2026-05-14..2026-05-21
```

### Example 5: Export Story-Filtered Feedback as Markdown (subcommand mode)

```bash
/DF:feedback export-data --format=markdown --story-ids=STORY-042,STORY-043
```

---

## Troubleshooting

### "Context contains invalid characters"

Context mode rejects special characters (allowed: alphanumeric, hyphens, underscores, spaces).

```bash
# ❌ Wrong
/DF:feedback STORY-001 (high-priority) #urgent @review!

# ✅ Correct
/DF:feedback STORY-001 high-priority urgent review
```

### "Context exceeds maximum length"

Context mode caps at 500 characters. Reduce length:

```bash
# ❌ Wrong
/DF:feedback STORY-001 This is a very long context with lots of details...

# ✅ Correct
/DF:feedback STORY-001 dev-phase performance-optimization
```

### "Cannot write to feedback directory"

```bash
# Check permissions
ls -la devforgeai/feedback/

# Fix permissions if needed
chmod 755 devforgeai/feedback/
```

### Subcommand not recognized

If you intended a subcommand (e.g. `export-data`) but it was treated as context, the first argument must match the subcommand name exactly. Check spelling: `export-data` (not `export_data`, `exportdata`, or `export data`).

### Feedback ID not incrementing (context mode)

```bash
# Check feedback register for duplicates
grep "^## FB-" devforgeai/feedback/feedback-register.md

# If duplicates found, manually edit to fix sequence numbers
```

---

## Related Commands

- `/feedback-search` — query feedback history
- `/feedback-config` — configure feedback system
- `/export-feedback` — ZIP-package export with sanitization (distinct from this subcommand's single-file export)
- `/feedback-reindex` — rebuild index
- `/qa` — QA validation (auto-triggers feedback)
- `/orchestrate` — full lifecycle (includes feedback capture)

---

## Migration Note

The standalone `/feedback-export-data` slash command (STORY-020) has been folded into this command as the `export-data` subcommand. Replace any prior invocations:

```bash
# Old (removed)
/feedback-export-data --format=csv

# New
/DF:feedback export-data --format=csv
```

The skill-level export sub-workflow and the context markers it reads are unchanged — only the entry point has moved.

---

## See Also

- `spec-driven-feedback` skill documentation
- STORY-013: Export Feedback ZIP Package (`/export-feedback`)
- STORY-020: Feedback CLI Commands (`export-data` subcommand origin)
- `devforgeai/feedback/feedback-register.md` (feedback storage)
- `devforgeai/feedback/config.yaml` (configuration file)
