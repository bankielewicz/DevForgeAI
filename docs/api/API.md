# DevForgeAI API Reference

Version: 0.1.0 | Last Updated: 2026-03-03

---

## Table of Contents

1. [CLI Reference](#1-cli-reference)
2. [Skill Interface](#2-skill-interface)
3. [Subagent Interface](#3-subagent-interface)
4. [Hook System](#4-hook-system)
5. [Phase State JSON Schema](#5-phase-state-json-schema)

---

## 1. CLI Reference

The `devforgeai-validate` CLI provides workflow validation and phase state management commands.

**Installation:**

```bash
pip install -e .claude/scripts/
```

**Global Options:**

| Option | Description |
|--------|-------------|
| `--version` | Show version (0.1.0) |
| `--help` | Show help for any command |

---

### 1.1 phase-init

Initialize a phase state file for a story.

```
devforgeai-validate phase-init <story_id> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_id` | Yes | Story identifier (e.g., `STORY-527`) |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--project-root` | `.` | Project root directory |
| `--format` | `text` | Output format: `text` or `json` |
| `--workflow` | `dev` | Workflow type: `dev`, `qa`, or custom (via WORKFLOW_SCHEMAS) |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | State file created |
| 1 | State file already exists |
| 2 | Invalid story ID or invalid workflow type |

**Examples:**

```bash
# Initialize dev workflow
devforgeai-validate phase-init STORY-527 --project-root=.

# Initialize QA workflow
devforgeai-validate phase-init STORY-527 --workflow=qa --project-root=.

# JSON output
devforgeai-validate phase-init STORY-527 --format=json --project-root=.
```

**JSON Output (success):**

```json
{
  "success": true,
  "story_id": "STORY-527",
  "path": "devforgeai/workflows/STORY-527-phase-state.json",
  "current_phase": "01"
}
```

---

### 1.2 phase-status

Display current phase status for a story.

```
devforgeai-validate phase-status <story_id> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_id` | Yes | Story identifier |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--project-root` | `.` | Project root directory |
| `--format` | `text` | Output format: `text` or `json` |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Status displayed successfully |
| 1 | State file not found |

**Text Output Example:**

```
Story: STORY-527
Started: 2026-03-03T10:00:00Z
Current Phase: 03
Blocking: none

Phase Status:
  [x] Phase 01: completed
      Subagents: git-validator, tech-stack-detector, context-preservation-validator
  [x] Phase 02: completed
      Subagents: test-automator
  [ ] Phase 03: in_progress
  [ ] Phase 04: pending
  ...
```

---

### 1.3 phase-check

Validate whether a phase transition is allowed.

```
devforgeai-validate phase-check <story_id> --from=<phase> --to=<phase> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_id` | Yes | Story identifier |

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--from` | Yes | - | Source phase (e.g., `01`) |
| `--to` | Yes | - | Target phase (e.g., `02`) |
| `--project-root` | No | `.` | Project root directory |
| `--format` | No | `text` | Output format |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Transition allowed |
| 1 | Transition blocked (phase not completed or non-sequential) |
| 2 | Missing required subagents |

**Transition Rules:**
1. Source phase must have `status: "completed"`
2. Transitions must be sequential (no phase skipping)
3. All required subagents for the source phase must be invoked

**OR-group subagent logic:** Some phases accept alternative subagents. For example, Phase 03 requires `backend-architect` OR `frontend-developer`. If either has been invoked, the requirement is satisfied.

---

### 1.4 phase-complete

Mark a phase as complete.

```
devforgeai-validate phase-complete <story_id> --phase=<phase> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_id` | Yes | Story identifier |

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--phase` | Yes | - | Phase to complete (e.g., `02`) |
| `--checkpoint-passed` | No | `true` | Mark checkpoint as passed |
| `--checkpoint-failed` | No | `false` | Mark checkpoint as failed |
| `--project-root` | No | `.` | Project root directory |
| `--format` | No | `text` | Output format |
| `--workflow` | No | `dev` | Workflow type: `dev`, `qa` |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Phase completed successfully |
| 1 | Phase incomplete or error (e.g., step validation failure) |

---

### 1.5 phase-record

Record a subagent invocation for a phase. Idempotent -- duplicate invocations are ignored.

```
devforgeai-validate phase-record <story_id> --phase=<phase> --subagent=<name> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_id` | Yes | Story identifier |

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--phase` | Yes | - | Phase ID (`01` through `10`, including `4.5`, `5.5`) |
| `--subagent` | Yes | - | Subagent name (e.g., `test-automator`) |
| `--project-root` | No | `.` | Project root directory |
| `--format` | No | `text` | Output format |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Subagent recorded |
| 1 | State file not found |
| 2 | Error |

---

### 1.6 phase-record-step

Record a step completion for a phase. Validates the step ID against the phase-steps-registry.

```
devforgeai-validate phase-record-step <story_id> --phase=<phase> --step=<step_id> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_id` | Yes | Story identifier |

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--phase` | Yes | - | Phase ID (e.g., `02`) |
| `--step` | Yes | - | Step ID (e.g., `02.2`) |
| `--project-root` | No | `.` | Project root directory |
| `--format` | No | `text` | Output format |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Step recorded |
| 1 | Error (unknown step ID, registry not found, state file missing) |

**Validation:** The step ID is checked against `.claude/hooks/phase-steps-registry.json`. Unknown step IDs are rejected with exit code 1.

---

### 1.7 phase-observe

Record a workflow observation for a phase. Captures friction, gaps, successes, and patterns during TDD execution.

```
devforgeai-validate phase-observe <story_id> --phase=<phase> --category=<cat> --note="<text>" [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_id` | Yes | Story identifier |

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--phase` | Yes | - | Phase ID |
| `--category` | Yes | - | One of: `friction`, `gap`, `success`, `pattern` |
| `--note` | Yes | - | Observation description (non-empty) |
| `--severity` | No | `medium` | One of: `low`, `medium`, `high` |
| `--project-root` | No | `.` | Project root directory |
| `--format` | No | `text` | Output format |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Observation recorded |
| 1 | State file not found |
| 2 | Invalid input (bad category, severity, or empty note) |

---

### 1.8 validate-dod

Validate Definition of Done completion for a story file. Detects autonomous deferrals and validates user approval markers.

```
devforgeai-validate validate-dod <story_file> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `story_file` | Yes | Path to `.story.md` file |

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--format` | `text` | Output format: `text` or `json` |
| `--project-root` | `.` | Project root directory |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Validation passed |
| 1 | Validation failed (violations found) |

**Violation Severities:**

| Severity | Description |
|----------|-------------|
| CRITICAL | Autonomous deferral without user approval; DoD marked `[x]` but missing from Implementation Notes |
| HIGH | Referenced stories do not exist; missing Implementation Notes section |
| MEDIUM | Deferred items with incomplete justifications |

---

### 1.9 Other Commands

| Command | Description | Exit Codes |
|---------|-------------|------------|
| `check-git --directory=.` | Validate Git repository availability | 0=valid, 1=not a repo |
| `validate-context --directory=.` | Check all 6 context files exist and are non-empty | 0=valid, 1=missing files |
| `check-hooks --operation=dev --status=success` | Check if hooks should trigger | 0=should trigger, 1=no trigger |
| `invoke-hooks --operation=dev --story=STORY-XXX` | Invoke feedback skill for operation | 0=success |
| `validate-installation --project-root=.` | Run 6 installation checks (CLI, context, hooks, PYTHONPATH, Git, settings) | 0=pass, 1=fail |
| `ast-grep scan <path>` | Semantic code analysis with ast-grep or grep fallback | 0=clean, 1=violations |
| `feedback-reindex --project-root=.` | Rebuild feedback index from all sources | 0=success |

---

## 2. Skill Interface

Skills are inline prompt expansions invoked by the orchestrator (opus). They are not background processes -- the orchestrator executes all skill phases sequentially.

### Invocation Pattern

```
Skill(command="<skill-name>")
```

After invocation, the skill's `SKILL.md` content expands inline and the orchestrator executes each phase.

### Available Skills

| Skill | Command | Location | Purpose |
|-------|---------|----------|---------|
| Implementing Stories | `implementing-stories` | `.claude/skills/implementing-stories/SKILL.md` | TDD development (10 phases, Red-Green-Refactor) |
| QA Validation | `devforgeai-qa` | `.claude/skills/devforgeai-qa/SKILL.md` | Quality validation (deep/light modes) |
| Documentation | `devforgeai-documentation` | `.claude/skills/devforgeai-documentation/SKILL.md` | Documentation generation |
| Story Creation | `devforgeai-story-creation` | `.claude/skills/devforgeai-story-creation/SKILL.md` | Story file creation with validation |
| Root Cause Diagnosis | `root-cause-diagnosis` | `.claude/skills/root-cause-diagnosis/SKILL.md` | 4-phase failure diagnosis (Capture-Investigate-Hypothesize-Prescribe) |
| Designing Systems | `designing-systems` | `.claude/skills/designing-systems/SKILL.md` | Architecture design |
| DevForgeAI Release | `devforgeai-release` | `.claude/skills/devforgeai-release/SKILL.md` | Release management |

### Skill Execution Rules

1. ALL phases execute in sequence -- no skipping, no reordering
2. Each phase has mandatory validation checkpoints
3. Pre-flight checks verify previous phase completion
4. Only the user can authorize phase skipping via explicit instruction

### Example: Implementing Stories Phases

| Phase | Name | Entry Gate | Exit Gate |
|-------|------|------------|-----------|
| 01 | Pre-Flight Validation | `phase-init` | `phase-complete --phase=01` |
| 02 | Test-First (Red) | `phase-check --from=01 --to=02` | `phase-complete --phase=02` |
| 03 | Implementation (Green) | `phase-check --from=02 --to=03` | `phase-complete --phase=03` |
| 04 | Refactoring | `phase-check --from=03 --to=04` | `phase-complete --phase=04` |
| 4.5 | AC Compliance (Post-Refactor) | `phase-check --from=04 --to=4.5` | `phase-complete --phase=4.5` |
| 05 | Integration & Validation | `phase-check --from=4.5 --to=05` | `phase-complete --phase=05` |
| 5.5 | AC Compliance (Post-Integration) | `phase-check --from=05 --to=5.5` | `phase-complete --phase=5.5` |
| 06 | Deferral Challenge | `phase-check --from=5.5 --to=06` | `phase-complete --phase=06` |
| 07 | DoD Update | `phase-check --from=06 --to=07` | `phase-complete --phase=07` |
| 08 | Git Workflow | `phase-check --from=07 --to=08` | `phase-complete --phase=08` |
| 09 | Feedback Hook | `phase-check --from=08 --to=09` | `phase-complete --phase=09` |
| 10 | Result Interpretation | `phase-check --from=09 --to=10` | `phase-complete --phase=10` |

---

## 3. Subagent Interface

Subagents are specialized agents delegated to by the orchestrator. Each subagent handles a single responsibility within a workflow phase.

### Invocation Pattern

```
Agent(subagent_type="<agent-name>", prompt="<task-description>")
```

Alternatively, using the Task construct:

```
Task(
  subagent_type="<agent-name>",
  description="<brief description>",
  prompt="<detailed instructions>"
)
```

### Available Subagents

| Subagent | Phase(s) | Purpose |
|----------|----------|---------|
| `git-validator` | 01 | Validate Git repository state |
| `tech-stack-detector` | 01 | Detect and validate technology stack |
| `context-preservation-validator` | 01 | Validate context file integrity |
| `test-automator` | 02 | Generate failing tests (Red phase) |
| `backend-architect` | 03 | Implement backend code (Green phase) |
| `frontend-developer` | 03 | Implement frontend code (Green phase) |
| `context-validator` | 03 | Validate context compliance |
| `diagnostic-analyst` | 03 (conditional) | Root cause diagnosis on failures |
| `refactoring-specialist` | 04 | Refactor implementation |
| `code-reviewer` | 04 | Code quality review |
| `ac-compliance-verifier` | 4.5, 5.5 | Verify acceptance criteria compliance |
| `integration-tester` | 05 | Write and run integration tests |
| `deferral-validator` | 06 (conditional) | Validate deferral justifications |
| `framework-analyst` | 09 | Analyze workflow observations |
| `dev-result-interpreter` | 10 | Interpret and format dev results |

### OR-Group Subagents

Some phases accept alternative subagents. Phase 03 requires **either** `backend-architect` OR `frontend-developer` (not both). The phase-check command supports OR-group validation.

### Subagent Definition Files

All subagent definitions are located in `.claude/agents/`:

```
.claude/agents/
  backend-architect.md
  code-reviewer.md
  diagnostic-analyst.md
  frontend-developer.md
  integration-tester.md
  refactoring-specialist.md
  test-automator.md
  ...
```

---

## 4. Hook System

DevForgeAI uses Claude Code hooks for automatic phase enforcement. Hooks are configured in `.claude/settings.json` and execute shell scripts on specific events.

### 4.1 SubagentStop Hook

**File:** `.claude/hooks/track-subagent-invocation.sh`

**Trigger:** `SubagentStop` event (fires after every subagent completes)

**Behavior:**
1. Reads JSON from stdin containing `agent_type` field
2. Filters out built-in agents (`Explore`, `Plan`, `Bash`, `general-purpose`)
3. Validates `agent_type` format against `^[a-zA-Z0-9_-]+$` regex
4. Finds the active story from the most recently modified `STORY-*-phase-state.json`
5. Extracts `current_phase` from the state file
6. Calls `devforgeai-validate phase-record` to record the invocation

**Exit Code:** Always 0 (non-blocking). Failures are logged to stderr only.

**Input Schema:**

```json
{
  "agent_type": "test-automator"
}
```

### 4.2 TaskCompleted Hook

**File:** `.claude/hooks/validate-step-completion.sh`

**Trigger:** `TaskCompleted` event (fires when a task is marked complete)

**Behavior:**
1. Reads JSON from stdin containing `subject` field
2. Checks if subject matches step pattern (`^Step [0-9]`)
3. Extracts step ID (e.g., `"Step 02.2: test-automator invoked"` becomes `"02.2"`)
4. Looks up the step in `phase-steps-registry.json`
5. Skips conditional steps (`"conditional": true`)
6. For non-conditional steps with a `subagent` field, checks if that subagent was invoked in the phase state
7. Supports OR-logic for array subagent fields (any match passes)

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Pass (step valid, no subagent required, conditional step, or lookup failed gracefully) |
| 2 | Block (required subagent was not invoked) |

**Input Schema:**

```json
{
  "subject": "Step 02.2: test-automator invoked"
}
```

**Environment Variables:**

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Project root override |
| `REGISTRY_PATH` | Override path to phase-steps-registry.json |
| `PHASE_STATE_PATH` | Override path to phase-state.json |

### 4.3 Phase Steps Registry

**File:** `.claude/hooks/phase-steps-registry.json`

The registry defines all 72 steps across 12 phases (01-10, plus 4.5 and 5.5). Each step entry has:

```json
{
  "id": "02.2",
  "check": "test-automator invoked",
  "subagent": "test-automator",
  "conditional": false
}
```

**Step Entry Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique step identifier (e.g., `"02.2"`, `"4.5.1"`) |
| `check` | string | Human-readable description of what the step validates |
| `subagent` | string, array, or null | Required subagent(s). `null` = no subagent check. Array = OR-logic. |
| `conditional` | boolean | If `true`, the step is skipped by the TaskCompleted hook |

**Phase Summary:**

| Phase | Name | Steps |
|-------|------|-------|
| 01 | Pre-Flight Validation | 8 steps (01.1 - 01.8) |
| 02 | Test-First (Red) | 7 steps (02.1 - 02.7) |
| 03 | Implementation (Green) | 7 steps (03.1 - 03.7) |
| 04 | Refactoring | 7 steps (04.1 - 04.7) |
| 4.5 | AC Compliance (Post-Refactor) | 4 steps (4.5.1 - 4.5.4) |
| 05 | Integration & Validation | 5 steps (05.1 - 05.5) |
| 5.5 | AC Compliance (Post-Integration) | 4 steps (5.5.1 - 5.5.4) |
| 06 | Deferral Challenge | 7 steps (06.1 - 06.7) |
| 07 | DoD Update | 5 steps (07.1 - 07.5) |
| 08 | Git Workflow | 6 steps (08.1 - 08.6) |
| 09 | Feedback Hook | 8 steps (09.1 - 09.8) |
| 10 | Result Interpretation | 4 steps (10.1 - 10.4) |

---

## 5. Phase State JSON Schema

Phase state files are stored in `devforgeai/workflows/` with the naming convention `STORY-XXX-phase-state.json` (dev) or `STORY-XXX-qa-phase-state.json` (QA).

### Dev Workflow Schema

```json
{
  "story_id": "STORY-527",
  "workflow_started": "2026-03-03T10:00:00+00:00",
  "current_phase": "03",
  "blocking_status": "none",
  "phases": {
    "01": {
      "status": "completed",
      "started_at": "2026-03-03T10:00:00+00:00",
      "completed_at": "2026-03-03T10:05:00+00:00",
      "checkpoint_passed": true,
      "subagents_required": ["git-validator", "tech-stack-detector", "context-preservation-validator"],
      "subagents_invoked": ["git-validator", "tech-stack-detector", "context-preservation-validator"],
      "steps_completed": ["01.1", "01.2", "01.3", "01.4", "01.6", "01.7", "01.8"]
    },
    "02": {
      "status": "completed",
      "started_at": null,
      "completed_at": "2026-03-03T10:15:00+00:00",
      "checkpoint_passed": true,
      "subagents_required": ["test-automator"],
      "subagents_invoked": ["test-automator"],
      "steps_completed": ["02.1", "02.2", "02.3", "02.4", "02.5", "02.6", "02.7"]
    },
    "03": {
      "status": "in_progress",
      "started_at": null,
      "completed_at": null,
      "checkpoint_passed": null,
      "subagents_required": [["backend-architect", "frontend-developer"], "context-validator"],
      "subagents_invoked": [],
      "steps_completed": []
    }
  },
  "observations": []
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `story_id` | string | Story identifier (format: `STORY-NNN`) |
| `workflow_started` | string (ISO 8601) | Timestamp when workflow was initialized |
| `current_phase` | string | Current active phase ID |
| `blocking_status` | string | `"none"` or description of blocking issue |
| `phases` | object | Map of phase ID to phase data |
| `observations` | array | Workflow observations captured via `phase-observe` |

### Phase Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"pending"`, `"in_progress"`, or `"completed"` |
| `started_at` | string or null | ISO 8601 timestamp |
| `completed_at` | string or null | ISO 8601 timestamp |
| `checkpoint_passed` | boolean or null | Whether the phase checkpoint passed |
| `subagents_required` | array | Required subagents. Nested arrays denote OR-groups. |
| `subagents_invoked` | array of strings | Subagents that have been recorded for this phase |
| `steps_completed` | array of strings | Step IDs completed (validated against registry) |

### Valid Phase IDs

**Dev workflow:** `01`, `02`, `03`, `04`, `4.5`, `05`, `5.5`, `06`, `07`, `08`, `09`, `10`

**QA workflow:** `00`, `01`, `1.5`, `02`, `03`, `04`

### OR-Group Encoding

When a phase accepts alternative subagents, the `subagents_required` field uses a nested array:

```json
{
  "subagents_required": [["backend-architect", "frontend-developer"], "context-validator"]
}
```

This means: (`backend-architect` OR `frontend-developer`) AND `context-validator`.

### Observation Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique observation identifier |
| `phase` | string | Phase ID when observation was captured |
| `category` | string | `"friction"`, `"gap"`, `"success"`, or `"pattern"` |
| `note` | string | Description of the observation |
| `severity` | string | `"low"`, `"medium"`, or `"high"` |
| `timestamp` | string (ISO 8601) | When observation was recorded |

### File Locations

| Workflow | Path Pattern |
|----------|-------------|
| Dev | `devforgeai/workflows/STORY-XXX-phase-state.json` |
| QA | `devforgeai/workflows/STORY-XXX-qa-phase-state.json` |
| Custom | `devforgeai/workflows/STORY-XXX-{workflow}-phase-state.json` |

### Concurrency

Phase state files use platform-aware file locking:
- **POSIX** (Linux, macOS, WSL): `fcntl` advisory locks
- **Windows**: `msvcrt` locking

All writes are atomic (write to temp file, then rename).

---

## Source Files

| Component | File |
|-----------|------|
| CLI entry point | `.claude/scripts/devforgeai_cli/cli.py` |
| Phase commands | `.claude/scripts/devforgeai_cli/commands/phase_commands.py` |
| PhaseState module | `.claude/scripts/devforgeai_cli/phase_state.py` |
| DoD validator | `.claude/scripts/devforgeai_cli/validators/dod_validator.py` |
| SubagentStop hook | `.claude/hooks/track-subagent-invocation.sh` |
| TaskCompleted hook | `.claude/hooks/validate-step-completion.sh` |
| Steps registry | `.claude/hooks/phase-steps-registry.json` |

---

<!-- SECTION: assessing-entrepreneur START -->
## Assessing Entrepreneur

The `assessing-entrepreneur` skill collects self-reported work-style preferences across 6 dimensions and produces a structured adaptive profile at `devforgeai/specs/business/user-profile.yaml`.

**Source:** `src/claude/skills/assessing-entrepreneur/SKILL.md` (196 lines)
**Story:** STORY-465 (Guided Self-Assessment Skill)
**Execution model:** Inline expansion (9 phases, executed sequentially by the orchestrator)

### Skill Invocation

```
Skill(command="assessing-entrepreneur")
```

### Command Interface

```
/assess-me [--recalibrate]
```

| Argument | Description |
|----------|-------------|
| _(none)_ | Full assessment. Creates a new `user-profile.yaml`. |
| `--recalibrate` | Re-runs the full questionnaire. Overwrites `user-profile.yaml` only; coaching history is preserved (BR-002). |

### Workflow Phases

| Phase | Name | Description |
|-------|------|-------------|
| 1 | Disclaimer and Consent | Displays safety disclaimer; blocks data collection until user consents via AskUserQuestion |
| 2 | Work Style Preferences | Q1.1 (Daily Structure), Q1.2 (Environment), Q1.3 (Collaboration) |
| 3 | Task Completion Patterns | Q2.1 (Project Patterns), Q2.2 (Interruption Recovery) |
| 4 | Motivation Drivers | Q3.1 (Primary Drivers, multi-select), Q3.2 (Drop-off Points, multi-select) |
| 5 | Energy Management | Q4.1 (Peak Hours), Q4.2 (Recovery, multi-select) |
| 6 | Previous Attempts | Q5.1 (Experience), Q5.2 (Lessons, multi-select, conditional) |
| 7 | Self-Reported Challenges | Q6.1 (Primary, multi-select), Q6.2 (Support, multi-select) |
| 8 | Profile Generation | Invokes `entrepreneur-assessor` subagent to normalize responses |
| 9 | Results Summary | Displays profile, recommended adaptations, and next steps |

### Questionnaire Interface

All questions use the AskUserQuestion tool:

```
AskUserQuestion(
  question: string,
  header: string,
  options: string[],
  multiSelect?: boolean
)
```

**Question inventory:** 13 questions across 6 dimensions.

| ID | Dimension | Header | Multi-Select |
|----|-----------|--------|-------------|
| Q1.1 | Work Style | Work Style - Daily Structure | No |
| Q1.2 | Work Style | Work Style - Environment | No |
| Q1.3 | Work Style | Work Style - Collaboration | No |
| Q2.1 | Task Completion | Task Completion - Project Patterns | No |
| Q2.2 | Task Completion | Task Completion - Interruption Recovery | No |
| Q3.1 | Motivation | Motivation - Primary Drivers | Yes |
| Q3.2 | Motivation | Motivation - Drop-off Points | Yes |
| Q4.1 | Energy Management | Energy Management - Peak Hours | No |
| Q4.2 | Energy Management | Energy Management - Recovery | Yes |
| Q5.1 | Previous Attempts | Previous Attempts - Experience | No |
| Q5.2 | Previous Attempts | Previous Attempts - Lessons | Yes |
| Q6.1 | Self-Reported Challenges | Self-Reported Challenges - Primary | Yes |
| Q6.2 | Self-Reported Challenges | Self-Reported Challenges - Support | Yes |

Q5.2 is conditional: only asked when the user reports previous experience in Q5.1.

### Subagent Contract

**Invocation (Phase 8):**

```
Task(
  subagent_type="entrepreneur-assessor",
  description="Normalize assessment responses into structured user profile",
  prompt="Process the following self-reported assessment responses and generate
          a structured user-profile. Responses: [collected responses from Phases 2-7].
          Dimensions: Work Style, Task Completion, Motivation, Energy Management,
          Previous Attempts, Self-Reported Challenges."
)
```

**Source:** `src/claude/agents/entrepreneur-assessor.md` (128 lines)

**Tools:**

| Tool | Usage |
|------|-------|
| Read | Load reference files for adaptation frameworks |
| Glob | Discover existing profile files when updating |
| Grep | Search patterns in reference documentation |
| AskUserQuestion | Clarify ambiguous or missing responses only |

**Processing pipeline:**

1. **Validate** -- Check all 6 dimensions have responses
2. **Normalize** -- Map categorical to tags, multi-select to weighted lists, free-text to themes
3. **Generate** -- Produce structured YAML profile
4. **Cross-reference** -- Identify reinforcing or contradicting patterns across dimensions
5. **Output** -- Write profile and return summary

### Output Schema: Adaptive Profile

Written to `devforgeai/specs/business/user-profile.yaml`:

```yaml
schema_version: "1.0"
created: "2026-02-21"
last_calibrated: "2026-02-21"

adaptive_profile:
  task_chunk_size: micro        # micro | standard | extended
  session_length: short         # short | medium | long
  check_in_frequency: frequent  # frequent | moderate | minimal
  progress_visualization: per_task  # per_task | daily | weekly
  celebration_intensity: high   # high | medium | low
  reminder_style: specific      # specific | balanced | gentle
  overwhelm_prevention: strict  # strict | moderate | open
```

**Enum values:**

| Dimension | Values | Range |
|-----------|--------|-------|
| task_chunk_size | micro, standard, extended | 5-60 min per task |
| session_length | short, medium, long | 15-60 min per session |
| check_in_frequency | frequent, moderate, minimal | every 1-5 tasks |
| progress_visualization | per_task, daily, weekly | granularity of visual feedback |
| celebration_intensity | high, medium, low | every-completion to milestone-only |
| reminder_style | specific, balanced, gentle | specific-next-action to gentle-nudge |
| overwhelm_prevention | strict, moderate, open | next-3-tasks-only to full-roadmap |

### Business Rules

| ID | Rule | Enforcement |
|----|------|-------------|
| BR-001 | `assessing-entrepreneur` (via `entrepreneur-assessor`) is the sole writer of `user-profile.yaml`. All other components are read-only consumers. | Subagent tool restrictions; coaching skill has no Write tool. |
| BR-002 | Recalibration (`--recalibrate`) overwrites `user-profile.yaml` only. Coaching session history is never modified. | Recalibration flow writes profile file; session log is not in scope. |
| BR-003 | The skill never diagnoses mental health conditions. All questions capture self-reported preferences only. | Phase 1 disclaimer; no diagnostic language in skill or subagent files. |

### Reference Files

Loaded on demand during Phases 8-9:

| File | Purpose |
|------|---------|
| `references/work-style-questionnaire.md` | Detailed question sets for all 6 dimensions (Phases 2-7) |
| `references/adhd-adaptation-framework.md` | Neurodivergent-friendly coaching adaptations |
| `references/confidence-assessment-workflow.md` | Confidence calibration patterns |
| `references/plan-calibration-engine.md` | Plan complexity adjustment from profile data |

### Integration Points

| Direction | Component | Description |
|-----------|-----------|-------------|
| Invoked by | `/assess-me` command | Primary user-facing entry point |
| Invoked by | `/assess-me --recalibrate` | Recalibration entry point |
| Invoked by | `/ideate` command | Optional assessment before ideation |
| Produces | `user-profile.yaml` | Consumed by downstream planning (BR-001: sole writer) |
| Consumed by | Plan calibration engine | Adjusts plan parameters based on adaptive profile |
| Consumed by | Coaching adaptation workflows | Adjusts coaching style (read-only per BR-001) |
<!-- SECTION: assessing-entrepreneur END -->

<!-- SECTION: coaching-entrepreneur START -->
## Coaching Entrepreneur

The `coaching-entrepreneur` skill delivers adaptive business coaching by dynamically shifting between Coach mode (empathetic, encouraging) and Consultant mode (structured, deliverable-focused) based on user state and profile. The skill reads the adaptive profile from `user-profile.yaml` to calibrate persona blend intensity. It also reads a persistent session log to track emotional state across sessions and adapt tone at session start.

**Source:** `src/claude/skills/coaching-entrepreneur/SKILL.md` (target ≤1000 lines)
**Stories:** STORY-467 (Dynamic Persona Blend Engine), STORY-468 (Emotional State Tracking)
**Execution model:** Inline expansion (invoked via command interface)
**Dependency:** STORY-466 (Adaptive Profile Generation) — requires `user-profile.yaml` from `/assess-me`

### Skill Invocation

```
Skill(command="coaching-entrepreneur")
```

### Persona Definitions

#### Coach Mode
- **Activation:** User reports struggling, overwhelmed, or low confidence; or adaptive profile indicates high `celebration_intensity`
- **Language:** Empathetic, encouraging, validates effort, addresses self-doubt, celebrates incremental wins
- **Structure:** Narrative-driven, validates feelings first, then offers perspective

#### Consultant Mode
- **Activation:** User reports focused on deliverables; or adaptive profile indicates structured `reminder_style`; or topic requires technical framework
- **Language:** Structured, deliverable-focused, uses professional frameworks, numbered action lists
- **Structure:** Framework-first (e.g., SWOT, Lean Canvas), then concrete next steps

### Subagent Contract

**Invocation:**

```
Task(
  subagent_type="business-coach",
  description="Gather coaching context and deliver adaptive coaching",
  prompt="User topic: [topic]. User state: [emotional_state].
          Adaptive profile: [profile_dimensions].
          Persona mode: [coach|consultant|blend].
          Previous session emotional state: [prior_emotional_state|none]."
)
```

**Source:** `src/claude/agents/business-coach.md` (target ≤500 lines)

**Tools:**

| Tool | Usage |
|------|-------|
| Read | Load user profile, session log, and reference frameworks |
| Write | Persist session log entry after emotional state is captured |
| Glob | Discover coaching reference materials |
| Grep | Search for relevant frameworks in references |
| AskUserQuestion | Gather coaching context and emotional state |

**Restrictions:** Profile writes are reserved for `assessing-entrepreneur` skill (BR-001). Session log writes are the only Write operation permitted for `business-coach`.

### Profile Reading Integration

The skill reads `devforgeai/specs/business/user-profile.yaml` (if present) to determine:

| Profile Dimension | Influence on Coaching |
|-------------------|----------------------|
| `task_chunk_size` | Breaks goals into micro (Coach) or extended (Consultant) increments |
| `celebration_intensity` | High → Coach mode preferred; Low → Consultant mode preferred |
| `reminder_style` | Specific → Consultant; Gentle → Coach |
| `overwhelm_prevention` | Strict → Coach mode; Open → Consultant mode |
| `check_in_frequency` | Frequent → Coach mode; Minimal → Consultant mode |

**Fallback behavior:** If profile missing, defaults to Coach mode.

### Emotional State Tracking

**Story:** STORY-468 | **Epic:** EPIC-072

The skill persists a session log at `devforgeai/specs/business/coaching/session-log.yaml` across Claude Code sessions. Each session entry records the user's self-reported emotional state and the date. At session start, the skill reads the most recent prior entry to calibrate its opening tone before prompting the user for the current state.

#### Session Log Schema

```yaml
# devforgeai/specs/business/coaching/session-log.yaml
sessions:
  - date: "2026-03-01"
    emotional_state: energized
  - date: "2026-03-04"
    emotional_state: tired
    override: focused   # optional — user-supplied correction
```

**Emotional state enum values:** `energized` | `focused` | `neutral` | `tired` | `frustrated` | `anxious` | `overwhelmed`

The `override` field is present only when the user explicitly corrects the logged state mid-session. It takes effect immediately and replaces the active state for that session's tone calibration.

#### Session Start Tone Adaptation

On each invocation, the skill:

1. Reads `session-log.yaml` and extracts the most recent entry's `emotional_state` (or `override` if present).
2. Uses that state to select an opening tone before asking the user about the current session.
3. Asks the user to confirm or update their current emotional state via `AskUserQuestion`.
4. Writes a new session entry with today's date and the confirmed state.

**Example — prior state `tired`, current session opens in Coach mode:**
```
Last session you were tired. Let's check in — how are you feeling heading into today?
[ energized | focused | neutral | tired | frustrated | anxious | overwhelmed ]
```

**Example — prior state `energized`, current session opens in Consultant mode:**
```
Last session you were energized. Ready to dig into deliverables? What are we tackling today?
[ energized | focused | neutral | tired | frustrated | anxious | overwhelmed ]
```

If `session-log.yaml` does not exist (first session), no prior-state prompt is shown and the skill asks directly for current state.

#### User Override Support

A user may correct their emotional state at any point during a session. The skill:

1. Immediately adopts the new state for tone calibration.
2. Writes the override to the current session entry's `override` field.
3. Narrates the mode shift explicitly to the user.

Overrides are logged for continuity across sessions; the next session start reads `override` in preference to `emotional_state` when both are present.

#### Tone Mapping

| Emotional State | Default Opening Mode | Rationale |
|-----------------|---------------------|-----------|
| `energized` | Consultant | High-energy state suits structured, deliverable-focused work |
| `focused` | Consultant | User is in execution mindset |
| `neutral` | Blend | No strong signal; blend until user topic clarifies |
| `tired` | Coach | Lower energy requires encouragement and reduced cognitive load |
| `frustrated` | Coach | Validation before problem-solving |
| `anxious` | Coach | Address self-doubt and overwhelm first |
| `overwhelmed` | Coach | Strict micro-chunking; no frameworks until grounded |

### Business Rules

| ID | Rule | Enforcement |
|----|------|-------------|
| BR-001 | Coaching skill reads `user-profile.yaml` only. Never writes user profile. | No Write tool for `user-profile.yaml`; profile writes reserved for `assessing-entrepreneur`. |
| BR-002 | Persona mode transitions are explicit and visible to user. | Skill narrates persona shift. |
| BR-003 | If user profile unavailable, default to Coach mode. Never infer emotional state from topic keywords. | Read() on profile path returns not-found → immediate fallback, no inference. |
| BR-004 (STORY-468) | Emotional state is self-reported only. Never AI-inferred. | State captured exclusively via `AskUserQuestion`; no keyword scanning or sentiment analysis. |
| BR-005 (STORY-468) | User overrides are respected immediately without negotiation. | On override signal, mode shifts in the same turn and override is written to session log. |

### Reference Files

Loaded on demand during coaching sessions:

| File | Purpose |
|------|---------|
| `references/coach-persona-prompts.md` | Coach mode language templates |
| `references/consultant-frameworks.md` | Structured coaching frameworks |
| `references/persona-blend-rules.md` | Decision trees for mode selection |

### Integration Points

| Direction | Component | Description |
|-----------|-----------|-------------|
| Depends on | `user-profile.yaml` (via STORY-466) | Reads adaptive profile; missing profile triggers fallback |
| Depends on | `session-log.yaml` (STORY-468) | Reads prior emotional state for tone adaptation at session start |
| Produces | `session-log.yaml` (STORY-468) | Writes session entry with confirmed emotional state and any user override |
| Invoked by | Coaching commands | Primary user-facing entry point |
| Produces | Coaching narratives (ephemeral) | Coaching content delivered in-session only; not persisted |
<!-- SECTION: coaching-entrepreneur END -->
