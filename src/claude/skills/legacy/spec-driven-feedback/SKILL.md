---
name: spec-driven-feedback
description: >
  Retrospective feedback system with Execute-Verify-Gate structural anti-skip
  enforcement for DevForgeAI operations. Captures feedback after /dev, /qa,
  /release, sprint planning, or manual triggers. Handles 5 feedback types:
  conversation, summary, metrics, checklist, and ai_analysis. Prevents
  token optimization bias through lean orchestration, per-phase reference
  loading, checkpoint persistence, and binary CLI gate enforcement. Use when
  feedback needs to be captured, when the user mentions retrospectives, lessons
  learned, workflow improvements, process feedback, or wants to review what
  went well or poorly. Also handles AI architectural analysis, feedback search,
  export/import, and configuration management.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Skill
  - Bash(python3:*)
model: opus
effort: High
version: "1.0.0"
topics: feedback, retrospective, anti-skip, spec-driven, hooks, ai-analysis
---

# Spec-Driven Feedback

Capture retrospective feedback from development workflows to improve processes, identify patterns, and enable continuous improvement — with structural anti-skip enforcement.

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Anti-Skip Enforcement

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow: the `devforgeai-validate` phase gates, the `settings.json`-registered `.claude/hooks/` scripts, and `.claude/hooks/phase-steps-registry.json` (ADR-076).

---

## Feedback Types

| Type | When Used | What Happens | Reference |
|------|-----------|--------------|-----------|
| **conversation** | After /dev, /qa, /release | Present context-aware questions via AskUserQuestion, persist responses | `references/adaptive-questioning.md` |
| **summary** | After any operation | Auto-generate markdown summary of results | `references/feedback-persistence-guide.md` |
| **metrics** | After any operation | Collect quantitative data (time, tokens, coverage) | `references/feedback-export-formats.md` |
| **checklist** | Sprint retrospectives | Interactive checklist via AskUserQuestion | `references/feedback-question-templates.md` |
| **ai_analysis** | After /dev, /qa (via hooks) | AI-generated framework improvement recommendations | `references/context-extraction.md` |

All references above are located at `references/` (relative to this skill directory).

---

## Parameter Extraction

Extract from conversation context markers set by invoking command:

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$FEEDBACK_MODE` | `/feedback`, hooks | conversation, summary, metrics, checklist, ai_analysis |
| `$FEEDBACK_CONTEXT` | `/feedback`, hooks | Story ID, operation details |
| `$FEEDBACK_SOURCE` | `/feedback`, hooks | manual, hook, auto |
| `$SEARCH_QUERY` | `/feedback-search` | Text search query |
| `$SEVERITY` | `/feedback-search` | low, medium, high, critical |
| `$STATUS` | `/feedback-search` | open, resolved, archived |
| `$LIMIT` | `/feedback-search` | Result count (default 10, max 1000) |
| `$PAGE` | `/feedback-search` | Pagination page number |
| `$FORMAT` | `/DF:feedback export-data` | json, csv, markdown |
| `$DATE_RANGE` | `/DF:feedback export-data`, `/export-feedback` | Date range filter |
| `$STORY_IDS` | `/DF:feedback export-data` | Comma-separated story IDs |
| `$SUBCOMMAND` | `/feedback-config` | view, edit, reset |
| `$SANITIZE` | `/export-feedback` | true/false for PII scrubbing |
| `$OUTPUT_PATH` | `/export-feedback` | ZIP output path |
| `$ARCHIVE_PATH` | `/import-feedback` | ZIP input path |

---

## Command Integration

These commands delegate to this skill. When invoked via a command, context markers are already set.

| Command | Purpose | Markers Set |
|---------|---------|-------------|
| `/DF:feedback` | Manual feedback capture (default) OR `export-data` subcommand for filtered single-file export | Feedback Mode (context: conversation; subcommand: export), Feedback Context, Feedback Source: manual, Format, Date Range, Story IDs, Severity, Status |
| `/feedback-config` | View/edit/reset config | Subcommand: view, edit, reset |
| `/feedback-search` | Search feedback history | Search Query, Severity, Status, Limit, Page |
| `/feedback-reindex` | Rebuild index from all sources | (invokes CLI directly: `devforgeai-validate feedback-reindex`) |
| `/export-feedback` | Export ZIP package with sanitization | Date Range, Sanitize, Output path |
| `/import-feedback` | Import ZIP package | Archive path |

---

## Hook Integration

This skill is auto-invoked by the event-driven hook system (STORY-018):

| Hook ID | Trigger | Feedback Type |
|---------|---------|---------------|
| `post-dev-feedback` | After /dev completes | conversation |
| `post-qa-retrospective` | After /qa completes | conversation |
| `post-release-monitoring` | After /release completes | conversation |
| `sprint-retrospective` | After sprint planning | checklist |
| `post-dev-ai-analysis` | After /dev completes | ai_analysis |
| `post-qa-ai-analysis` | After /qa completes | ai_analysis |

**Hook configuration:** `devforgeai/config/hooks.yaml`
**Hook system reference:** `HOOK-SYSTEM.md` (relative to this skill directory)

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
Extract from conversation context markers:
  $FEEDBACK_MODE     — from "**Feedback Mode:**" marker or default "conversation"
  $FEEDBACK_CONTEXT  — from "**Feedback Context:**" marker or extract from conversation
  $FEEDBACK_SOURCE   — from "**Feedback Source:**" marker or default "manual"
  $SEARCH_QUERY      — from "**Search Query:**" marker (search operations)
  $SEVERITY          — from "**Severity:**" marker (search/export)
  $STATUS            — from "**Status:**" marker (search)
  $FORMAT            — from "**Format:**" marker (export)
  $DATE_RANGE        — from "**Date Range:**" marker (export)
  $STORY_IDS         — from "**Story IDs:**" marker (export)
  $SUBCOMMAND        — from "**Subcommand:**" marker (config)
  $SANITIZE          — from "**Sanitize:**" marker (export ZIP)
  $OUTPUT_PATH       — from "**Output:**" marker (export ZIP)
  $ARCHIVE_PATH      — from "**Archive:**" marker (import ZIP)
```

### Step 0.2: Resume Detection

```
IF conversation mentions "--resume" or resume context:
  Glob(pattern="devforgeai/feedback/checkpoints/FB-*.checkpoint.json")
  IF matching checkpoint found:
    Read the checkpoint file
    AskUserQuestion:
      Question: "Found existing feedback session. Resume or start fresh?"
      Header: "Resume"
      Options:
        - label: "Resume session"
          description: "Continue from last checkpoint"
        - label: "Start fresh"
          description: "Begin new feedback session"
    IF "Resume": Restore state, GOTO Phase Orchestration Loop at CURRENT_PHASE
ELSE:
  Continue to Step 0.3
```

### Step 0.3: Generate Session ID

```
# Scan for highest existing FB-YYYY-MM-DD-### in register
register_exists = Glob(pattern="devforgeai/feedback/feedback-register.md")

IF register_exists:
  Read(file_path="devforgeai/feedback/feedback-register.md")
  Extract highest ### for today's date
  SESSION_ID = "FB-{YYYY-MM-DD}-{###+1}" (zero-padded to 3 digits)
ELSE:
  SESSION_ID = "FB-{YYYY-MM-DD}-001"
```

### Step 0.4: CLI Initialization

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=feedback --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${SESSION_ID} --workflow=feedback` to get CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Must match FB-YYYY-MM-DD-NNN pattern. |
| 127 | CLI not installed | Continue without CLI enforcement (backward compatibility). |

### Step 0.5: Create Initial Checkpoint

```
checkpoint = {
  "checkpoint_version": "1.0",
  "session_id": SESSION_ID,
  "workflow": "feedback",
  "created_at": "current ISO 8601 timestamp",
  "updated_at": "current ISO 8601 timestamp",
  "status": "in_progress",
  "input": {
    "feedback_mode": $FEEDBACK_MODE,
    "feedback_source": $FEEDBACK_SOURCE,
    "feedback_context": $FEEDBACK_CONTEXT,
    "story_id": extracted story ID or null,
    "operation_type": extracted operation or null,
    "operation_status": extracted status or null,
    "search_query": $SEARCH_QUERY or null,
    "severity": $SEVERITY or null,
    "status_filter": $STATUS or null,
    "format": $FORMAT or null,
    "date_range": $DATE_RANGE or null,
    "subcommand": $SUBCOMMAND or null
  },
  "progress": {
    "current_phase": 0,
    "phases_completed": [],
    "total_steps_completed": 0
  },
  "phases": {
    "01": { "status": "pending", "steps_completed": [] },
    "02": { "status": "pending", "steps_completed": [] },
    "03": { "status": "pending", "steps_completed": [] },
    "04": { "status": "pending", "steps_completed": [] },
    "05": { "status": "pending", "steps_completed": [] },
    "06": { "status": "pending", "steps_completed": [] }
  },
  "output": {
    "feedback_id": null,
    "feedback_file_path": null,
    "feedback_type": null,
    "stories_created": [],
    "error": null
  }
}

Write(file_path="devforgeai/feedback/checkpoints/${SESSION_ID}.checkpoint.json", content=checkpoint)
```

**VERIFY:** `Glob(pattern="devforgeai/feedback/checkpoints/${SESSION_ID}.checkpoint.json")`
IF not found: HALT -- "Initial checkpoint was NOT created."

### Step 0.6: Display Session Banner

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Feedback Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: ${SESSION_ID}
Mode: ${FEEDBACK_MODE}
Source: ${FEEDBACK_SOURCE}
Context: ${FEEDBACK_CONTEXT || 'None provided'}
Story: ${story_id || 'N/A'}

Phases: 6 (Context Detection > Type Dispatch > Feedback Execution > Validation > Persistence > Completion)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 7):  # Phases 01-06

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=feedback --from={prev} --to={phase_id} --project-root=.
       IF exit != 0 AND exit != 127: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-feedback/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT rely on memory of previous reads.

    3. REFERENCE: Read the phase's reference files as specified in the phase Contract section.
       References are in references/ (self-contained within this skill).

    4. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.
       - Each step's EXECUTE tells you exactly what action to take
       - Each step's VERIFY tells you how to confirm the action happened
       - Each step's RECORD tells you how to update the checkpoint

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0 AND exit != 127: HALT

    6. CHECKPOINT: Update checkpoint JSON with phase completion.
       Write updated checkpoint to disk.
       Verify write via Glob().
```

---

## Phase Table

| Phase | Name | File | Steps | Required Subagents |
|-------|------|------|-------|--------------------|
| 00 | Initialization | (inline above) | 6 | none |
| 01 | Context Detection & Sanitization | `phases/phase-01-context-detection.md` | 5 | none |
| 02 | Type Dispatch & Preparation | `phases/phase-02-type-dispatch.md` | 4 | none |
| 03 | Feedback Execution | `phases/phase-03-feedback-execution.md` | 3-6 (varies by type) | framework-analyst (ai_analysis only) |
| 04 | Validation & Quality Gates | `phases/phase-04-validation.md` | 4 | none |
| 05 | Persistence & Indexing | `phases/phase-05-persistence.md` | 5 | none |
| 06 | Completion & Display | `phases/phase-06-completion.md` | 3 | none |

---

## Required Subagents Per Phase

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 03 | framework-analyst | CONDITIONAL (ai_analysis feedback type only) |

**All other phases:** No subagents required. Direct tool calls (Read, Write, Glob, Grep, AskUserQuestion).

---

## AI Analysis Output Schema

```json
{
  "story_id": "STORY-XXX",
  "timestamp": "ISO8601",
  "ai_analysis": {
    "what_worked_well": [{"observation": "...", "evidence": "...", "impact": "..."}],
    "areas_for_improvement": [{"issue": "...", "evidence": "...", "root_cause": "..."}],
    "recommendations": [{
      "title": "...",
      "description": "...",
      "affected_files": ["..."],
      "implementation_code": "...",
      "effort_estimate": "15 min|30 min|1 hour|2 hours|4 hours",
      "priority": "HIGH|MEDIUM|LOW",
      "feasible_in_claude_code": true
    }],
    "patterns_observed": ["..."],
    "anti_patterns_detected": ["..."],
    "constraint_analysis": "..."
  }
}
```

**Constraint:** All recommendations MUST be implementable within Claude Code Terminal. If a recommendation requires tools beyond Read, Write, Edit, Glob, Grep, Bash, TaskCreate, TaskUpdate, AskUserQuestion — flag it as `feasible_in_claude_code: false`.

---

## State Persistence

- **Checkpoint:** `devforgeai/feedback/checkpoints/${SESSION_ID}.checkpoint.json`
- **References:** `references/` (self-contained within this skill)
- **Templates:** `templates/` (self-contained within this skill)
- **Hook System:** `HOOK-SYSTEM.md` (self-contained within this skill)
- **Configuration:** `devforgeai/feedback/config.yaml`

---

## Workflow Completion Validation

```
IF phases_completed < 6: HALT "WORKFLOW INCOMPLETE - {completed_count}/6 phases"
IF feedback_file_path is null: HALT "Feedback file was not written"
IF feedback_id is null: HALT "Feedback ID was not generated"
IF checkpoint status != "complete": Update checkpoint status to "complete"
```

---

## Configuration

**File:** `devforgeai/feedback/config.yaml`

| Setting | Default | Description |
|---------|---------|-------------|
| `retention_days` | 90 | Days to keep feedback (1-3650) |
| `auto_trigger_enabled` | true | Auto-trigger on operation completion |
| `export_format` | json | Default export format (json/csv/markdown) |
| `include_metadata` | true | Include metadata in exports |
| `search_enabled` | true | Enable search functionality |

---

## Success Criteria

- All 6 phases executed (no skipping)
- Feedback file written to disk (verified via Glob)
- Index updated with new entry (verified via Grep)
- Register updated with new entry (verified via Grep)
- Checkpoint marked as complete
- Confirmation displayed to user with feedback ID
- Token usage < 40K (isolated context)

---

## Related Documentation

- **Origin ADR:** `devforgeai/specs/adrs/ADR-040-devforgeai-feedback-to-spec-driven-feedback-migration.md` (the `devforgeai-feedback` → `spec-driven-feedback` consolidation that produced this skill)
- **Hook System:** `HOOK-SYSTEM.md` (self-contained within this skill)
- **Hook Config:** `devforgeai/config/hooks.yaml`
- **Feedback Config:** `devforgeai/feedback/config.yaml`
- **Framework Analyst:** `.claude/agents/framework-analyst.md`
- **GH-issue posting for ai_analysis recs:** `.claude/skills/github-incident-from-feedback/SKILL.md` (ADR-077 — the direct-to-GitHub pathway for `ai_analysis` recommendations). Two slash commands consume it: `/create-incident-from-feedback` (per-entry ai-analysis files) and `/create-incident-from-queue` (aggregated recommendations-queue.json — replaces the retired `/recommendations-triage`).
