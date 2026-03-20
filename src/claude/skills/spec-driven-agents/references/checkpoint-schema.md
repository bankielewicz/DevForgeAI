# Checkpoint Schema Reference

**Purpose:** Define the checkpoint JSON structure used by spec-driven-agents for session persistence and resume

---

## Schema Definition

```json
{
  "checkpoint_version": "1.0",
  "session_id": "AGENT-{NNN}",
  "created_at": "ISO8601 timestamp",
  "status": "in_progress | completed | failed",
  "progress": {
    "current_phase": 0,
    "phases_completed": [],
    "completion_percentage": 0
  },
  "parameters": {
    "agent_name": "string | null",
    "creation_mode": "guided | template | domain | custom",
    "domain": "string | null",
    "template_name": "string | null",
    "spec_file": "string | null"
  },
  "framework_context": {
    "references_loaded": [],
    "context_files_required": []
  },
  "specification": {
    "name": "string | null",
    "purpose": "string | null",
    "domain": "string | null",
    "tools": [],
    "model": "string | null",
    "responsibilities": [],
    "integration_skills": [],
    "context_files": []
  },
  "generation": {
    "generated_files": {},
    "validation_results": "object | null",
    "reference_file_needed": "boolean"
  },
  "phases": {
    "01": { "status": "pending | in_progress | completed", "steps_completed": [] },
    "02": { "status": "pending | in_progress | completed", "steps_completed": [], "questions_answered": 0 },
    "03": { "status": "pending | in_progress | completed", "steps_completed": [] },
    "04": { "status": "pending | in_progress | completed", "steps_completed": [] },
    "05": { "status": "pending | in_progress | completed", "steps_completed": [] },
    "06": { "status": "pending | in_progress | completed", "steps_completed": [] }
  }
}
```

---

## Field Descriptions

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `checkpoint_version` | string | Schema version for forward compatibility |
| `session_id` | string | Unique session identifier (AGENT-NNN format) |
| `created_at` | string | ISO8601 timestamp of session creation |
| `status` | enum | Current session status |

### Progress Object

| Field | Type | Description |
|-------|------|-------------|
| `current_phase` | number | Current phase number (0-6) |
| `phases_completed` | array | List of completed phase IDs ("01"-"06") |
| `completion_percentage` | number | 0-100 percentage based on phases completed |

### Parameters Object

Captures the initial arguments from `/create-agent` command:

| Field | Type | Description |
|-------|------|-------------|
| `agent_name` | string/null | Name from command argument, null if not provided |
| `creation_mode` | enum | One of: guided, template, domain, custom |
| `domain` | string/null | Domain from `--domain=` flag |
| `template_name` | string/null | Template from `--template=` flag |
| `spec_file` | string/null | File path from `--spec=` flag |

### Specification Object

Populated during Phase 02 (Requirements Gathering):

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Validated agent name (kebab-case) |
| `purpose` | string | Agent purpose (2+ sentences) |
| `domain` | string | Agent domain (backend, frontend, qa, etc.) |
| `tools` | array | Selected tool set |
| `model` | string | Selected model (haiku, sonnet, opus, inherit) |
| `responsibilities` | array | Agent responsibilities |
| `integration_skills` | array | DevForgeAI skills this agent works with |
| `context_files` | array | Context files the agent should reference |

### Generation Object

Populated during Phases 04-05:

| Field | Type | Description |
|-------|------|-------------|
| `generated_files` | object | Paths to generated files (subagent, reference) |
| `validation_results` | object | 12-point validation check results |
| `reference_file_needed` | boolean | Whether a reference file should be generated |

---

## Resume Logic

When `--resume AGENT-NNN` is provided:

1. Construct path: `devforgeai/workflows/agent-creation/AGENT-NNN.checkpoint.json`
2. Glob for file existence
3. If found: Read, extract `current_phase`, jump to that phase in orchestration loop
4. If not found: Offer to start fresh or cancel

---

## Session ID Generation

```
1. Glob(pattern="devforgeai/workflows/agent-creation/AGENT-*.checkpoint.json")
2. Extract NNN from each match
3. Find maximum NNN
4. New session = AGENT-{max + 1} (zero-padded to 3 digits)
5. If no existing sessions: AGENT-001
```

---

## Checkpoint Location

```
devforgeai/workflows/agent-creation/{session_id}.checkpoint.json
```

This directory is created during Phase 00 if it does not exist.
