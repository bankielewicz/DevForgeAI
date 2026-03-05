# Setup Workflow (SKILL.md Phase 1)

> **Phase mapping:** This file uses legacy step numbering (0.0-0.6). In SKILL.md v3.0, Setup is **Phase 1** with steps 1.1-1.7. The step content is identical — only the numbering prefix differs.

Contains complete implementation for setup steps.

---

### Step 0.0: Session Checkpoint Detection [NEW - STORY-126]

**Purpose:** Detect interrupted QA sessions and offer resume capability.

**Constitution Alignment:** Skills MUST NOT assume state from previous invocations (architecture-constraints.md line 38)
    Read(file_path=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

```
checkpoint_path = "devforgeai/qa/reports/{STORY_ID}/.qa-session-checkpoint.json"
Glob(pattern=checkpoint_path)

IF checkpoint found:
    Read(file_path=checkpoint_path)
    checkpoint = parse_json(file_content)

    IF checkpoint.can_resume == true:
        Display: "Found interrupted QA session for {STORY_ID}"
        Display: "  Last phase: {checkpoint.current_phase}"
        Display: "  Completed phases: {checkpoint.completed_phases}"
        Display: "  Started: {checkpoint.started_at}"

        AskUserQuestion:
            Question: "Resume from Phase {checkpoint.current_phase} or start fresh?"
            Header: "Resume Session"
            Options:
                - label: "Resume from Phase {current_phase}"
                  description: "Continue from last checkpoint, skip completed phases"
                - label: "Start fresh (discard checkpoint)"
                  description: "Delete checkpoint and run complete QA validation"
            multiSelect: false

        IF user chooses "Resume":
            # Load checkpoint state
            $RESUME_MODE = true
            $RESUME_PHASE = checkpoint.current_phase
            $COMPLETED_PHASES = checkpoint.completed_phases
            Display: "✓ Resuming from Phase {checkpoint.current_phase}"
            # Skip to RESUME_PHASE (pre-flight will validate markers)
        ELSE:
            # Delete checkpoint and start fresh
            Bash(command="rm {checkpoint_path}")
            $RESUME_MODE = false
            Display: "✓ Starting fresh QA validation"

ELSE:
    $RESUME_MODE = false
    Display: "✓ No interrupted session found - starting fresh"
```

### Step 0.1: Validate Project Root [MANDATORY - FIRST STEP]

```
# Check project marker file
result = Read(file_path="CLAUDE.md")

IF result.success:
    content = result.content
    IF content_contains("DevForgeAI") OR content_contains("devforgeai"):
        CWD_VALID = true
        Display: "✓ Project root validated"
    ELSE:
        CWD_VALID = false
        HALT: Use AskUserQuestion to get correct path
ELSE:
    # Try secondary markers
    dir_check = Glob(pattern=".claude/skills/*.md")
    IF dir_check.has_results:
        CWD_VALID = true
        Display: "✓ Project root validated via .claude/skills/ structure"
    ELSE:
        CWD_VALID = false
        HALT: Use AskUserQuestion: "Provide project root path?"
```

**CRITICAL:** Do NOT proceed if CWD validation fails.

### Step 0.2: Load Test Isolation Configuration

**Reference:** `references/test-isolation-service.md`
    Read(file_path=".claude/skills/devforgeai-qa/references/test-isolation-service.md")

```
Read(file_path="devforgeai/config/test-isolation.yaml")

IF file not found:
    Display: "ℹ️ Test isolation config not found, using defaults"
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
ELSE:
    config = parsed YAML content
    Display: "✓ Test isolation config loaded"
```

### Step 0.3: Create Story-Scoped Directories

```
story_paths = {
    results_dir: "{config.paths.results_base}/{STORY_ID}",
    coverage_dir: "{config.paths.coverage_base}/{STORY_ID}",
    logs_dir: "{config.paths.logs_base}/{STORY_ID}"
}

IF config.directory.auto_create:
    Bash(command="mkdir -p {story_paths.results_dir} {story_paths.coverage_dir} {story_paths.logs_dir}")
    Write(file_path="{story_paths.results_dir}/timestamp.txt", content="{ISO_8601_TIMESTAMP}")
    Display: "✓ Story directories created: {STORY_ID}"
```

### Step 0.4: Acquire Lock File

```
IF config.concurrency.locking_enabled:
    lock_file = "{story_paths.results_dir}/.qa-lock"

    IF exists(lock_file):
        lock_age = now() - file_mtime(lock_file)
        IF lock_age > config.concurrency.stale_lock_threshold_seconds:
            Display: "⚠️ Removing stale lock file"
            Remove(file_path=lock_file)
        ELSE:
            AskUserQuestion: "Lock exists. Wait/Force/Cancel?"

    Write(file_path=lock_file, content="timestamp: {ISO_8601}\nstory: {STORY_ID}")
    Display: "✓ Lock acquired for {STORY_ID}"
```

### Step 0.5: Load Deep Mode Workflow (Deep Mode Only)

```
IF mode == "deep":
    Read(file_path=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")
    Display: "✓ Deep validation workflow loaded"
```

### Step 0.6: Extract Story Type for Adaptive Validation (STORY-183)

**Purpose:** Extract story type from YAML frontmatter to select appropriate validators.

This step detects story type in Phase 0 for adaptive validator selection.

```
# Read story file and extract type from frontmatter
story_content = Read(file_path="devforgeai/specs/Stories/{STORY_ID}*.story.md")

# Extract story_type from YAML frontmatter (type: field)
story_type = grep_extract("^type:\s*(.+)$", story_content)

IF $STORY_TYPE is empty OR $STORY_TYPE not in ["feature", "bugfix", "refactor", "documentation"]:
    # Default to feature for unknown/missing types (full validation)
    $STORY_TYPE = "feature"
    Display: "ℹ️ Story type not specified - defaulting to 'feature' (full validation)"
ELSE:
    Display: "✓ Story type detected: {$STORY_TYPE}"

# Display which validators will run (adaptive selection preview)
IF $STORY_TYPE == "documentation":
    Display: "  → Validators: [code-reviewer] (1/1 threshold)"
ELIF $STORY_TYPE == "refactor":
    Display: "  → Validators: [code-reviewer, security-auditor] (1/2 threshold)"
ELSE:
    Display: "  → Validators: [test-automator, code-reviewer, security-auditor] (2/3 threshold)"

# Store for Phase 2 adaptive validator selection
# See references/parallel-validation.md for validator mapping
    Read(file_path=".claude/skills/devforgeai-qa/references/parallel-validation.md")

```

**Validator Selection by Story Type:**

| Story Type | Validators | Threshold | Rationale |
|------------|------------|-----------|-----------|
| `documentation` | code-reviewer only | 1/1 | No code tests needed |
| `refactor` | code-reviewer, security-auditor | 1/2 | Tests already exist |
| `feature`/`bugfix` | all 3 validators | 2/3 | Full validation suite |
| (unknown/missing) | all 3 validators | 2/3 | Conservative default |

### Step 0.7: Detect Deliverable Type (Non-Code Handling)

**Purpose:** Determine if the story delivers executable code or non-code files (Markdown, YAML, JSON). This affects coverage analysis (Phase 2) and code quality metrics (Phase 4).

```
# Read story's Implementation Notes or Files Created/Modified section
# Check file extensions of implementation deliverables

implementation_files = extract_files_from_story(story_content)

code_extensions = [".py", ".ts", ".js", ".cs", ".go", ".rs", ".java", ".cpp", ".c", ".rb"]
noncode_extensions = [".md", ".yaml", ".yml", ".json", ".xml", ".toml"]

has_code = any(file.endswith(ext) for file in implementation_files for ext in code_extensions)
has_noncode = any(file.endswith(ext) for file in implementation_files for ext in noncode_extensions)

IF has_code AND has_noncode:
    $DELIVERABLE_TYPE = "mixed"
    Display: "Deliverable type: mixed (code + non-code files)"
ELIF has_code:
    $DELIVERABLE_TYPE = "code"
    Display: "Deliverable type: code"
ELIF has_noncode:
    $DELIVERABLE_TYPE = "non-code"
    Display: "Deliverable type: non-code (Markdown/config only)"
    Display: "  Coverage tooling and code quality metrics will be skipped"
    Display: "  Structural test coverage will be verified instead"
ELSE:
    $DELIVERABLE_TYPE = "code"  # Conservative default
    Display: "Deliverable type: unknown — defaulting to code"
```

**How $DELIVERABLE_TYPE affects later phases:**

| Phase | Step | If `non-code` | If `code` or `mixed` |
|-------|------|---------------|---------------------|
| 2 | 2.2 Coverage | Skip language-specific tooling. Verify structural test coverage instead. Report "N/A (non-code)." | Execute 7-step coverage workflow normally. |
| 3 | 3.3 Regression | Runs normally. Additive-only Markdown changes pass. | Runs normally with full pattern detection. |
| 4 | 4.1 Anti-patterns | Runs normally. Context violations apply to any file type. | Runs normally. |
| 4 | 4.4 Quality | Skip complexity, MI, duplication tools. Documentation coverage still applies. Report "N/A (non-code)." | Execute full quality metrics. |
