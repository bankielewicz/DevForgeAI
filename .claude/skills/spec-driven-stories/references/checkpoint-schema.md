# Checkpoint Schema Reference

## Schema Version: 1.0

The checkpoint JSON file tracks story creation session state for resumability and anti-skip enforcement.

## File Location

```
devforgeai/workflows/checkpoints/${SESSION_ID}.checkpoint.json
```

## Schema

```json
{
  "checkpoint_version": "1.0",
  "session_id": "SC-YYYY-MM-DD-NNN",
  "workflow": "stories",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp",
  "status": "in_progress | completed | failed",
  "input": {
    "mode": "SINGLE_STORY | EPIC_BATCH",
    "epic_id": "EPIC-NNN | null",
    "feature_description": "string | null",
    "story_id": "STORY-NNN | null",
    "batch_mode": "boolean",
    "batch_index": "integer | null"
  },
  "progress": {
    "current_phase": "integer (0-8)",
    "phases_completed": ["01", "02", ...],
    "total_steps_completed": "integer"
  },
  "phases": {
    "01": { "status": "pending | in_progress | completed", "steps_completed": ["1.1", "1.2", ...] },
    "02": { "status": "...", "steps_completed": [...] },
    "03": { "status": "...", "steps_completed": [...] },
    "04": { "status": "...", "steps_completed": [...] },
    "05": { "status": "...", "steps_completed": [...] },
    "06": { "status": "...", "steps_completed": [...] },
    "07": { "status": "...", "steps_completed": [...] },
    "08": { "status": "...", "steps_completed": [...] }
  },
  "output": {
    "story_id": "STORY-NNN | null",
    "story_file_path": "devforgeai/specs/Stories/STORY-NNN-slug.story.md | null",
    "epic_linked": "boolean",
    "sprint_linked": "boolean",
    "validation_passed": "boolean",
    "error": "string | null"
  }
}
```

## State Transitions

```
status: in_progress -> completed  (all 8 phases done)
status: in_progress -> failed     (HALT on unrecoverable error)
```

## Phase Status Transitions

```
pending -> in_progress  (phase entry gate passed)
in_progress -> completed  (phase exit gate passed)
```

## Resume Protocol

1. Read checkpoint from disk
2. Find `progress.current_phase`
3. Verify phase status matches expected state
4. Resume from the phase that is `in_progress` or the next `pending` phase
5. Do NOT re-execute `completed` phases

## Verification

After every checkpoint write:
```
Glob(pattern="devforgeai/workflows/checkpoints/${SESSION_ID}.checkpoint.json")
IF not found: HALT -- "Checkpoint write verification failed"
```
