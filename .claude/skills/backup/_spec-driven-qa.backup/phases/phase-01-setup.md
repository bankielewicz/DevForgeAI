# Phase 01: Setup

## Entry Gate

```bash
devforgeai-validate phase-init ${STORY_ID} --workflow=qa --project-root=.
# Exit 0: new workflow | Exit 1: resume | Exit 2: invalid | Exit 127: CLI not installed
```

## Contract

PURPOSE: Initialize QA environment -- validate CWD, create test isolation, acquire locks, detect story type and deliverable type.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Story-scoped directories, lock file, $STORY_TYPE, $DELIVERABLE_TYPE, $MODE
STEP COUNT: 8 mandatory steps

---

## Mandatory Steps

### Step 1.1: Session Checkpoint Detection

EXECUTE: Check for interrupted QA session and offer resume capability.
```
checkpoint_path = "devforgeai/qa/reports/${STORY_ID}/.qa-session-checkpoint.json"
Glob(pattern=checkpoint_path)

IF checkpoint found:
    Read(file_path=checkpoint_path)
    AskUserQuestion:
        Question: "Found interrupted QA session. Resume or start fresh?"
        Header: "Resume"
        Options:
            - label: "Resume from last checkpoint"
              description: "Continue from last completed phase"
            - label: "Start fresh"
              description: "Delete checkpoint and run complete QA validation"
        multiSelect: false

    IF user chooses "Resume":
        $RESUME_MODE = true
        $RESUME_PHASE = checkpoint.current_phase
    ELSE:
        $RESUME_MODE = false

ELSE:
    $RESUME_MODE = false
```
VERIFY: Either checkpoint processed (resume variables set) or fresh start confirmed ($RESUME_MODE = false).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.1 --project-root=.`

---

### Step 1.2: Validate Project Root

EXECUTE: Read CLAUDE.md to confirm we are in the project root directory.
```
Read(file_path="CLAUDE.md")

IF Read succeeds AND content contains "DevForgeAI" or "devforgeai":
    CWD_VALID = true
    Display: "Project root validated"
ELSE:
    # Try secondary markers
    Glob(pattern=".claude/skills/*.md")
    IF results found:
        CWD_VALID = true
    ELSE:
        CWD_VALID = false
        HALT: AskUserQuestion("Provide correct project root path?")
```
VERIFY: CWD_VALID = true. If false, workflow HALTED via AskUserQuestion.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.2 --project-root=.`

---

### Step 1.3: Load Test Isolation Configuration

EXECUTE: Read test isolation config file. Use defaults if not found.
```
Read(file_path=".claude/skills/devforgeai-qa/references/test-isolation-service.md")
Read(file_path="devforgeai/config/test-isolation.yaml")

IF file not found:
    config = {
        enabled: true,
        paths: {
            results_base: "tests/results",
            coverage_base: "tests/coverage",
            logs_base: "tests/logs"
        },
        directory: { auto_create: true, permissions: 755 },
        concurrency: { locking_enabled: true, lock_timeout_seconds: 300 }
    }
    Display: "Test isolation config not found, using defaults"
ELSE:
    config = parsed YAML content
    Display: "Test isolation config loaded"
```
VERIFY: config variable is populated (either from file or defaults).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.3 --project-root=.`

---

### Step 1.4: Create Story-Scoped Directories

EXECUTE: Create results, coverage, and logs directories for this story.
```
story_paths = {
    results_dir: "{config.paths.results_base}/${STORY_ID}",
    coverage_dir: "{config.paths.coverage_base}/${STORY_ID}",
    logs_dir: "{config.paths.logs_base}/${STORY_ID}"
}

Bash(command="mkdir -p {story_paths.results_dir} {story_paths.coverage_dir} {story_paths.logs_dir}")
```
VERIFY: Directories exist.
```
Glob(pattern="{story_paths.results_dir}")
IF not found: HALT -- "Failed to create story-scoped directories."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.4 --project-root=.`

---

### Step 1.5: Acquire Lock File

EXECUTE: Write lock file for concurrency control.
```
IF config.concurrency.locking_enabled:
    lock_file = "{story_paths.results_dir}/.qa-lock"

    # Check for existing lock
    Glob(pattern=lock_file)
    IF exists:
        AskUserQuestion: "QA lock exists. Wait, Force, or Cancel?"
        IF Force: delete and recreate
        IF Cancel: HALT

    Write(file_path=lock_file, content="timestamp: {ISO_8601}\nstory: ${STORY_ID}\nmode: ${MODE}")
    Display: "Lock acquired for ${STORY_ID}"
```
VERIFY: Lock file exists on disk.
```
Glob(pattern=lock_file)
IF not found AND locking_enabled: HALT -- "Failed to acquire lock."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.5 --project-root=.`

---

### Step 1.6: Load Mode-Specific References

EXECUTE: Load shared protocols and parameter extraction reference. In deep mode, load additional references needed for subsequent phases.
```
Read(file_path=".claude/skills/devforgeai-qa/references/shared-protocols.md")
Read(file_path=".claude/skills/devforgeai-qa/references/parameter-extraction.md")

IF $MODE == "deep":
    Display: "Deep mode: additional references will be loaded per-phase"
ELSE:
    Display: "Light mode: minimal reference loading"
```
VERIFY: shared-protocols.md content is in context (confirms Read succeeded).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.6 --project-root=.`

---

### Step 1.7: Extract Story Type for Adaptive Validation

EXECUTE: Read story file and extract type from YAML frontmatter for adaptive validator selection (STORY-183).
```
story_file = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
Read(file_path=story_file)

# Extract type: field from frontmatter
Grep(pattern="^type:", path=story_file, output_mode="content")

IF $STORY_TYPE is empty OR $STORY_TYPE not in ["feature", "bugfix", "refactor", "documentation"]:
    $STORY_TYPE = "feature"  # Conservative default
    Display: "Story type not specified -- defaulting to 'feature' (full validation)"
ELSE:
    Display: "Story type detected: {$STORY_TYPE}"

# Preview which validators will run
IF $STORY_TYPE == "documentation":
    Display: "  Validators: [code-reviewer] (1/1 threshold)"
ELIF $STORY_TYPE == "refactor":
    Display: "  Validators: [code-reviewer, security-auditor] (1/2 threshold)"
ELSE:
    Display: "  Validators: [test-automator, code-reviewer, security-auditor] (2/3 threshold)"
```
VERIFY: $STORY_TYPE is set to one of: feature, bugfix, refactor, documentation.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.7 --project-root=.`

---

### Step 1.8: Detect Deliverable Type

EXECUTE: Classify implementation files as code, non-code, or mixed. This affects coverage analysis (Phase 2) and code quality metrics (Phase 4).
```
# Read story's Implementation Notes or Files Created/Modified section
# Check file extensions of implementation deliverables

code_extensions = [".py", ".ts", ".js", ".cs", ".go", ".rs", ".java", ".cpp", ".c", ".rb"]
noncode_extensions = [".md", ".yaml", ".yml", ".json", ".xml", ".toml"]

# Extract files from story content
implementation_files = extract_files_from_story(story_content)

has_code = any file ends with code extension
has_noncode = any file ends with noncode extension

IF has_code AND has_noncode:
    $DELIVERABLE_TYPE = "mixed"
ELIF has_code:
    $DELIVERABLE_TYPE = "code"
ELIF has_noncode:
    $DELIVERABLE_TYPE = "non-code"
    Display: "Deliverable type: non-code -- coverage tooling and code quality metrics will be skipped"
ELSE:
    $DELIVERABLE_TYPE = "code"  # Conservative default

Display: "Deliverable type: {$DELIVERABLE_TYPE}"
```
VERIFY: $DELIVERABLE_TYPE is set to one of: code, non-code, mixed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=01 --step=1.8 --project-root=.`

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
