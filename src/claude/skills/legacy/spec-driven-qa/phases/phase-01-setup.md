# Phase 01: Setup

## Entry Gate

```bash
devforgeai-validate phase-init ${STORY_ID} --workflow=qa --mode=${MODE} --project-root=.
# Exit 0: new workflow | Exit 1: resume | Exit 2: invalid | Exit 127: CLI not installed
```
**Fallback** (older CLI without `--mode`):
```bash
devforgeai-validate phase-init ${STORY_ID} --workflow=qa --project-root=.
```

## Contract

| | |
|---|---|
| **PURPOSE** | Initialize QA environment — validate CWD, create test isolation, acquire locks, detect story type and deliverable type. |
| **REQUIRED SUBAGENTS** | none |
| **REQUIRED ARTIFACTS** | Story-scoped directories, lock file, `$STORY_TYPE`, `$DELIVERABLE_TYPE`, `$MODE` |
| **STEP COUNT** | 7 mandatory steps |

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-qa/references/test-isolation-service.md")
Read(file_path=".claude/skills/spec-driven-qa/references/shared-protocols.md")
Read(file_path=".claude/skills/spec-driven-qa/references/parameter-extraction.md")
```

IF any Read fails: HALT -- "Phase 01 reference files not loaded."

**Note on CLI consolidation:** When the `qa-setup` CLI fast-path (next section) succeeds, the manual Steps 1.3/1.6 that perform these Reads are skipped. The CLI bundles equivalent setup internally; consumers that rely on the fast-path satisfy this contract via the CLI itself rather than direct Reads.

## CLI Consolidation (OPT-002)

The 7 manual steps below are deterministic and replaceable by one CLI call:
```bash
devforgeai-validate qa-setup ${STORY_ID} --workflow=qa --project-root=.
# Exit 0: fresh setup (JSON with story_type, deliverable_type, story_paths, lock_acquired)
# Exit 1: resume mode (JSON with resume_phase)
# Exit 2: invalid (CWD not project root or story not found)
```

On exit 0, extract values from JSON and skip to Exit Gate:
```
setup_result = JSON.parse(stdout)
$STORY_TYPE = setup_result.story_type
$DELIVERABLE_TYPE = setup_result.deliverable_type
story_paths = setup_result.story_paths
```

If CLI is unavailable (exit 127) or fails (exit 2), fall back to the manual steps below.

---

## Bootstrap: Initialize Iteration Log (Non-Blocking)

EXECUTE: Non-blocking — if the CLI fails, WARN and continue. Never HALT.
```bash
devforgeai-validate iteration-log-init ${STORY_ID} --project-root=.
```
VERIFY: If exit != 0, display "WARNING: Iteration log bootstrap failed — continuing workflow."
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=bootstrap --project-root=.`

---

## Mandatory Steps

### Step 1.1: Session Checkpoint Detection

EXECUTE: Check for interrupted QA session and offer resume.
```
checkpoint_path = "devforgeai/qa/reports/${STORY_ID}/.qa-session-checkpoint.json"
Glob(pattern=checkpoint_path)

IF checkpoint found:
    Read(file_path=checkpoint_path)
    AskUserQuestion: "Found interrupted QA session. Resume from last checkpoint, or Start fresh?"
    IF "Resume": $RESUME_MODE = true; $RESUME_PHASE = checkpoint.current_phase
    ELSE:        $RESUME_MODE = false
ELSE:
    $RESUME_MODE = false
```
VERIFY: $RESUME_MODE set (true with $RESUME_PHASE, or false).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.1 --project-root=.`

---

### Step 1.2: Validate Project Root

EXECUTE: Read CLAUDE.md to confirm CWD is project root.
```
Read(file_path="CLAUDE.md")

IF Read succeeds AND content contains "DevForgeAI" or "devforgeai":
    CWD_VALID = true
ELSE:
    Glob(pattern=".claude/skills/*.md")  # Secondary marker
    IF results found: CWD_VALID = true
    ELSE: CWD_VALID = false; HALT via AskUserQuestion("Provide correct project root path?")
```
VERIFY: CWD_VALID = true.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.2 --project-root=.`

---

### Step 1.3: Load Test Isolation Configuration

EXECUTE: Read test isolation config; use defaults if not found.
```
Read(file_path=".claude/skills/spec-driven-qa/references/test-isolation-service.md")
Read(file_path="devforgeai/config/test-isolation.yaml")

IF file not found:
    config = defaults: enabled=true, paths.{results,coverage,logs}_base=tests/{results,coverage,logs},
             directory.auto_create=true, permissions=755, concurrency.locking_enabled=true, lock_timeout=300s
    Display: "Test isolation config not found, using defaults"
ELSE:
    config = parsed YAML
    Display: "Test isolation config loaded"
```
VERIFY: `config` populated.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.3 --project-root=.`

---

### Step 1.4: Create Story-Scoped Directories

EXECUTE:
```
story_paths = {
    results_dir:  "{config.paths.results_base}/${STORY_ID}",
    coverage_dir: "{config.paths.coverage_base}/${STORY_ID}",
    logs_dir:     "{config.paths.logs_base}/${STORY_ID}"
}
Bash(command="mkdir -p {story_paths.results_dir} {story_paths.coverage_dir} {story_paths.logs_dir}")
```
VERIFY:
```
Glob(pattern="{story_paths.results_dir}")
IF not found: HALT — "Failed to create story-scoped directories."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.4 --project-root=.`

---

### Step 1.5: Acquire Lock File

EXECUTE:
```
IF config.concurrency.locking_enabled:
    lock_file = "{story_paths.results_dir}/.qa-lock"
    Glob(pattern=lock_file)
    IF exists:
        AskUserQuestion: "QA lock exists. Wait, Force, or Cancel?"
        IF Force: delete and recreate
        IF Cancel: HALT
    Write(file_path=lock_file, content="timestamp: {ISO_8601}\nstory: ${STORY_ID}\nmode: ${MODE}")
```
VERIFY:
```
Glob(pattern=lock_file)
IF not found AND locking_enabled: HALT — "Failed to acquire lock."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.5 --project-root=.`

---

### Step 1.6: Load Mode-Specific References

EXECUTE: Load shared protocols + parameter extraction. Deep mode loads additional references per-phase.
```
Read(file_path=".claude/skills/spec-driven-qa/references/shared-protocols.md")
Read(file_path=".claude/skills/spec-driven-qa/references/parameter-extraction.md")

IF $MODE == "deep": Display "Deep mode: additional references loaded per-phase"
ELSE:               Display "Light mode: minimal reference loading"
```
VERIFY: shared-protocols.md content in context (confirms Read succeeded).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.6 --project-root=.`

---

### Step 1.7: Extract Story Type and Deliverable Type

EXECUTE: Read story file once; extract type (for adaptive validator selection — STORY-183) and deliverable type (for Phase 2 coverage analysis and Phase 4 code quality).
```
story_file = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
story_content = Read(file_path=story_file)

# --- Story Type ---
Grep(pattern="^type:", path=story_file, output_mode="content")
IF $STORY_TYPE empty OR not in ["feature", "bugfix", "refactor", "documentation"]:
    $STORY_TYPE = "feature"  # Conservative default
    Display: "Story type not specified — defaulting to 'feature' (full validation)"
ELSE:
    Display: "Story type detected: {$STORY_TYPE}"

# Validator preview (drives Phase 04 parallel-validation threshold logic)
IF $STORY_TYPE == "documentation":  Display "  Validators: [code-reviewer] (1/1 threshold)"
ELIF $STORY_TYPE == "refactor":     Display "  Validators: [code-reviewer, security-auditor] (1/2 threshold)"
ELSE:                               Display "  Validators: [test-automator, code-reviewer, security-auditor] (2/3 threshold)"

# --- Deliverable Type ---
code_exts    = [".py", ".ts", ".js", ".cs", ".go", ".rs", ".java", ".cpp", ".c", ".rb"]
noncode_exts = [".md", ".yaml", ".yml", ".json", ".xml", ".toml"]
implementation_files = extract_files_from_story(story_content)

has_code    = any file ends in code_exts
has_noncode = any file ends in noncode_exts

IF has_code AND has_noncode: $DELIVERABLE_TYPE = "mixed"
ELIF has_code:               $DELIVERABLE_TYPE = "code"
ELIF has_noncode:            $DELIVERABLE_TYPE = "non-code"; Display "Deliverable type: non-code — coverage/quality skipped"
ELSE:                        $DELIVERABLE_TYPE = "code"  # Conservative default

Display: "Deliverable type: {$DELIVERABLE_TYPE}"
```
VERIFY: $STORY_TYPE ∈ {feature, bugfix, refactor, documentation}; $DELIVERABLE_TYPE ∈ {code, non-code, mixed}.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.7 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=01 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 02 | Exit 1: HALT
```

## Phase 01 Completion Display

```
Phase 01 Complete: Setup
  Project root: Validated
  Test isolation: Configured
  Lock: Acquired
  Mode: ${MODE}
  Story type: ${STORY_TYPE}
  Deliverable type: ${DELIVERABLE_TYPE}
```
