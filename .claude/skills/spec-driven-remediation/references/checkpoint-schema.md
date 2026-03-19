# Checkpoint Schema for Remediation Sessions

Defines the YAML structure for remediation session checkpoints. Checkpoints enable resume capability across context window clears and session interruptions.

---

## File Location

```
devforgeai/temp/.remediation-checkpoint-${SESSION_ID}.yaml
```

Where SESSION_ID is derived from the audit file name:
```
SESSION_ID = "FIX-" + basename(AUDIT_FILE).replace(".md", "")
Example: "FIX-custody-chain-audit-stories-413-424"
```

---

## Schema (v1.0)

```yaml
# Checkpoint metadata
checkpoint_version: "1.0"
session_id: "FIX-custody-chain-audit-stories-413-424"
timestamp: "2026-03-18T14:30:00Z"                    # ISO 8601, updated on each write
audit_file: "devforgeai/qa/audit/custody-chain-audit-stories-413-424.md"

# Execution mode (set once in Phase 00, immutable after)
mode:
  dry_run: false                                       # true = preview only
  auto_only: false                                     # true = skip interactive/ADR
  finding_filter: "all"                                # "all" or "F-NNN"

# Phase tracking
current_phase: 3                                       # 0-5, last phase entered
status: "in_progress"                                  # in_progress | completed | failed

# Phase completion map
phase_completion:
  phase_00: true
  phase_01: true
  phase_02: true
  phase_03: false                                      # Currently in progress
  phase_04: false
  phase_05: false

# Per-finding tracking (the core state that enables resume)
findings:
  - finding_id: "F-001"
    severity: "MEDIUM"
    type: "context/invalid_path"
    classification: "interactive"                      # automated | interactive | adr_required | advisory
    status: "applied"                                  # pending | applied | deferred | skipped | failed | previously_fixed
    verification: "passed"                             # pending | passed | failed | deferred
    retry_count: 0                                     # 0-2 (max 2 retries per finding)
    file_changed: "devforgeai/specs/context/source-tree.md"
    change_summary: "Added requirements/ to source-tree.md"

  - finding_id: "F-002"
    severity: "MEDIUM"
    type: "quality/broken_file_reference"
    classification: "automated"
    status: "pending"                                  # Not yet processed
    verification: "pending"
    retry_count: 0
    file_changed: null
    change_summary: null

# User decision log (persists interactive choices across sessions)
user_decisions:
  - timestamp: "2026-03-18T14:35:00Z"
    finding_id: "F-001"
    decision: "Add path to source-tree.md"
  - timestamp: "2026-03-18T14:36:00Z"
    phase_02_approval: "apply_all"                     # apply_all | review_each | skip_auto
```

---

## Field Descriptions

### Top-level Fields

| Field | Type | Description |
|-------|------|-------------|
| `checkpoint_version` | string | Schema version for forward compatibility |
| `session_id` | string | Unique session identifier derived from audit file |
| `timestamp` | string | ISO 8601 timestamp, updated on each checkpoint write |
| `audit_file` | string | Path to the source audit file |
| `current_phase` | integer | Last phase entered (0-5) |
| `status` | enum | Overall session status |

### Mode Fields

| Field | Type | Description |
|-------|------|-------------|
| `dry_run` | boolean | If true, no files are modified (preview only) |
| `auto_only` | boolean | If true, skip interactive and ADR-required fixes |
| `finding_filter` | string | "all" or specific finding ID (e.g., "F-002") |

### Finding Fields

| Field | Type | Description |
|-------|------|-------------|
| `finding_id` | string | Audit finding identifier (F-NNN) |
| `severity` | enum | CRITICAL, HIGH, MEDIUM, LOW |
| `type` | string | Finding type from audit (e.g., quality/broken_file_reference) |
| `classification` | enum | automated, interactive, adr_required, advisory |
| `status` | enum | pending, applied, deferred, skipped, failed, previously_fixed |
| `verification` | enum | pending, passed, failed, deferred |
| `retry_count` | integer | 0-2, number of retry attempts for this finding |
| `file_changed` | string/null | Path to the file that was modified (null if not yet applied) |
| `change_summary` | string/null | Brief description of the change made |

### User Decision Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | When the decision was recorded |
| `finding_id` | string | Which finding the decision applies to (optional) |
| `decision` | string | The user's choice (free text) |
| `phase_02_approval` | string | User's Phase 02 approval mode (optional) |

---

## Resume Logic

When resuming from a checkpoint:

1. Read the checkpoint file
2. Set `CURRENT_PHASE` from `current_phase` field
3. For each phase in `phase_completion`, skip completed phases
4. For each finding, respect existing `status` and `classification` — do not reclassify
5. For findings with `status == "applied"` and `verification == "pending"`, re-run verification
6. For user decisions, do NOT re-prompt — use the recorded decision
7. For `retry_count >= 2`, do not retry — mark as failed or deferred

---

## Write Protocol

- Write the checkpoint after EVERY step that changes state (not just at phase boundaries)
- Use atomic write: write to temp file first, then rename to avoid corruption
- Include the current timestamp on every write
- Never delete the checkpoint until Phase 05 completes successfully
