---
description: Prompt versioning system for template migration safety - captures before/after snapshots of agent, skill, and command prompt files, enables rollback with SHA-256 integrity verification
argument-hint: <capture|finalize|rollback|history> <component-path-or-id> [--reason "change description"] [--version N|previous]
---

# /prompt-version

Versioning system for DevForgeAI prompt templates (agents, skills, commands). Captures before/after snapshots, maintains VERSION-HISTORY.md audit trail per component, enables rollback within minutes.

## Arguments

Parse `$ARGUMENTS` to extract:
1. **Subcommand** (required): `capture`, `finalize`, `rollback`, or `history`
2. **Component path or ID**: File path (`.claude/agents/test-automator.md`) or component_id (`test-automator`). For history: component_id or `"all"` for full audit
3. **Options**: `--reason "description"` (5-200 chars), `--version N` or `--version previous`

---

## Component ID Auto-Detection

When a file path is provided, auto-detect component_type and derive the component_id.

### Detection Rules

| Path Pattern | component_type | component_id Derivation |
|---|---|---|
| `.claude/agents/{name}.md` | agent | filename without .md (e.g., `test-automator` from `test-automator.md`) |
| `.claude/skills/{name}/SKILL.md` | skill | directory name (e.g., `implementing-stories` from `implementing-stories/SKILL.md`) |
| `.claude/commands/{name}.md` | command | filename without .md (e.g., `dev` from `dev.md`) |

**Path Validation (BR-003):** Must start with `.claude/` prefix and end with `.md` extension. Paths with `../` are forbidden (path traversal rejection). Reject absolute path outside project root.

**File Existence:** Validate file exists via `Read(file_path="{path}")`. If file does not exist, HALT missing component.

**Unknown Paths:** If path does not match any pattern, reject path with error listing valid path patterns (expected path formats): `.claude/agents/`, `.claude/skills/`, `.claude/commands/`.

**BR-001:** Component ID must be lowercase, hyphen-separated: `^[a-z][a-z0-9-]{1,63}$`. Start with `[a-z]`, max 64 chars.

**BR-002:** Component type must be one of: `agent`, `skill`, `command`.

**Edge Cases:** Handles nested directory paths (`skills/implementing-stories/SKILL.md`). Handles `.claude/agents/`, `.claude/skills/`, `.claude/commands/` path formats. Component renamed or moved between versions detected via PATH_CHANGED event and path_mismatch logging.

---

## Capture Subcommand

Read current component file, compute SHA-256 hash, store version snapshot in `devforgeai/specs/prompt-versions/{component_id}/`.

**Step 1:** `Read(file_path="{component_path}")` - If file not found or does not exist: HALT missing component.

**Step 2:** Compute SHA-256 via `Bash(command="sha256sum {path} | cut -d' ' -f1")`. Fallback: `Bash(command="python3 -c \"import hashlib; print(hashlib.sha256(open('{path}','rb').read()).hexdigest())\"")`. Hash must match `^[0-9a-f]{64}$` (BR-004).

**Step 3 (BR-008):** New components use sentinel `NEW_COMPONENT` as before_hash, type "creation".

**Step 4 (BR-005):** Check for concurrent captures via `Glob(pattern="devforgeai/specs/prompt-versions/{id}/*.snapshot.md")`. If pending capture (unfinalized) exists: HALT "already captured pending state".

**Step 5:** Write snapshot with naming `{timestamp}-{short_hash}.snapshot.md`:
```
Write(file_path="devforgeai/specs/prompt-versions/{component_id}/{timestamp}-{short_hash}.snapshot.md", content=snapshot)
```

### Snapshot Structure

```yaml
---
component_id: "{id}"
component_type: "{agent|skill|command}"
file_path: "{path}"
before_hash: "{hash_or_NEW_COMPONENT}"
after_hash: null
capture_timestamp: "{ISO-8601 YYYY-MM-DDTHH:MM:SS+00:00}"
finalized_timestamp: null
change_reason: null
---
```

Followed by `## Before Content` section with full before_content of the component file.

### Confirmation Output

Display component_id/component_type, before_hash (SHA-256), and snapshot path:
```
Capture complete:
  Component: {component_id} ({component_type})
  Before Hash: {before_hash}
  Snapshot: devforgeai/specs/prompt-versions/{component_id}/{filename}
```

---

## Finalize Subcommand

Record after-state, update snapshot, append to VERSION-HISTORY.md.

**Prerequisite:** A prior capture must exist. If no prior capture: HALT "capture first, pending snapshot not found."

**Step 1 (BR-007):** change_reason is required, 5-200 chars. Reject with "Change reason required - must be 5-200 chars. Min 5 chars, reason length validated."

**Step 2:** Read modified file, compute after_hash via sha256sum. Records after_content.

**Step 3:** If unchanged (identical hash, same hash, no modification): warn operator.

**Step 4:** Update existing snapshot via `Edit(file_path=..., old_string="after_hash: null", new_string=...)`. Set after_hash, after_content, change_reason, finalized_timestamp.

**Step 5:** Read or create VERSION-HISTORY.md. Auto-increment version_number (initial version starts at 1, next version = last + 1).

Append row to Markdown table:

| Version | Date | Before Hash | After Hash | Type | Reason | Snapshot |
| ------- | ---- | ----------- | ---------- | ---- | ------ | -------- |
| {version_number} | {YYYY-MM-DD} | {before_hash[:8]} | {after_hash[:8]} | migration | {change_reason} | {snapshot_file} |

Table columns: Version column, Date column, Before Hash column, After Hash column, Type column, Reason column, Snapshot column (snapshot reference/snapshot_file).

**Step 6:** Report diff summary: lines added, lines removed, lines changed.

---

## Rollback Subcommand

Restore component to previous version. Must complete within 120 seconds (2 minutes).

**Step 1:** Accept version_number parameter or `"previous"` keyword (latest version before-state). If version does not exist: HALT "invalid version, version not found."

**Step 2:** `Read(file_path="devforgeai/specs/prompt-versions/{id}/VERSION-HISTORY.md")`. If no version history: HALT "no prior version, history empty."

**Step 3:** Locate snapshot_file from history. `Read(file_path=".../{snapshot}")`. If snapshot missing/not found: HALT "snapshot unavailable."

**Step 4 (BR-006):** Integrity verification before rollback (see Integrity Verification). Check integrity first.

**Step 5:** Read before_content from snapshot for restoration.

**Step 6 (BR-007):** rollback_reason required (5-200 chars). "Rollback reason required."

**Step 7:** Restore via `Write(file_path="{file_path}", content="{before_content}")`. Atomic rollback: no partial writes; if Write fails, original preserved.

**Step 8:** Append rollback version record: type `"rollback"`, restored_from (source version_number), rollback_reason.

**Step 9:** Compute verification hash of restored file.

### Confirmation

Display restored file path, version restored to, verification hash:
```
Rollback complete:
  Restored File Path: {file_path}
  Version Restored: v{N} (restored from version {source})
  Verification Hash: {hash}
  Duration: {s}s (limit: 120 seconds)
```

### Edge Cases

- **Deleted component:** File no longer exists at file_path. Use AskUserQuestion: recreate at original path, alternative path, or cancel.
- **Missing snapshot:** Snapshot not found - HALT.
- **Invalid version:** Version does not exist - HALT.
- **No history:** No prior version history, history empty.

---

## History Subcommand

Display version history from VERSION-HISTORY.md in Markdown table format.

**Single component:** `Read(file_path="devforgeai/specs/prompt-versions/{id}/VERSION-HISTORY.md")`

**"All" mode:** `Glob(pattern="devforgeai/specs/prompt-versions/*/VERSION-HISTORY.md")` to discover components. Groups by component with component_type header and file_path header per component.

### Display Table

| Version | Date | Before Hash | After Hash | Type | Reason |
| ------- | ---- | ----------- | ---------- | ---- | ------ |
| 3 | 2026-02-10 | a1b2c3d4 | e5f6g7h8 | migration | Updated prompt |
| 2 | 2026-02-08 | 12345678 | a1b2c3d4 | update | Added tools |
| 1 | 2026-02-05 | NEW_COMP | 12345678 | creation | Initial |

Hash truncated to first 8 characters (`[:8]`). Types: migration, rollback, update, creation.

**Counts:** Total version count per component. Overall total count across all components.

### Edge Cases

- **No entries:** "No version history, no entries, history empty."
- **Corrupted snapshot:** WARNING "Snapshot unavailable" - continue displaying other records.
- **Unknown component:** "Component not found, no such component, unknown component."

---

## Integrity Verification

SHA-256 hash integrity check before every rollback. Recompute SHA-256 from stored before_content, compare against recorded before_hash.

**Step 1:** Extract before_content and before_hash from snapshot. If missing before_content: HALT "incomplete snapshot, missing before_content." If missing before_hash: HALT "no before_hash, incomplete."

**Step 2:** If before_hash = `NEW_COMPONENT` sentinel, skip integrity (no content to verify). Sentinel NEW_COMPONENT = first-time capture.

**Step 3:** Recompute sha256 from stored_content: `Bash(command="echo -n '{content}' | sha256sum")`. Compute hash of before_content from snapshot.

**Step 4:** Compare computed hash against recorded before_hash.
- **Hash match:** Proceed with rollback.
- **Hash mismatch:** HALT immediately.

### INTEGRITY_VERIFICATION_FAILED

```
HALT: INTEGRITY_VERIFICATION_FAILED
  Expected hash (before_hash): {expected_hash}
  Actual hash (recomputed): {actual_hash}
Content may be tampered or corrupted. Refuse to restore corrupted content.
```

Displays expected vs actual hash for investigation.

### Recovery (AskUserQuestion)

```
AskUserQuestion(
  question="Integrity failed. Options:",
  options=[
    "Force restore - bypass check (WARNING: corrupted)",
    "Cancel rollback - keep current",
    "Restore from git history - use git fallback"
  ]
)
```

Force restore option, cancel option, git history fallback.

**NFR-005:** SHA-256 on every rollback. Always verify. HALT on mismatch.

**Edge Cases:** Corrupted snapshot (malformed snapshot, cannot parse). Missing before_content in snapshot. Missing before_hash in snapshot. Path traversal prevention via `.claude/` prefix validation (NFR-004).

---

## Error Handling

| Condition | Action |
|---|---|
| File does not exist | HALT missing |
| Invalid component_id | HALT invalid |
| Path outside .claude/ | HALT rejected |
| Path traversal `../` | HALT forbidden |
| INTEGRITY_VERIFICATION_FAILED | HALT mismatch |
| No pending capture for finalize | HALT capture first |
| Change reason < 5 chars | HALT too short |
| Absolute path outside project root | HALT rejected |

All timestamps: ISO-8601 `YYYY-MM-DDTHH:MM:SS+00:00`.

Native tools: `Read(file_path=...)`, `Write(file_path=...)`, `Edit(file_path=...)`, `Glob(pattern=...)`, `Grep(pattern=...)`, `Bash(command="sha256sum ...")`.
