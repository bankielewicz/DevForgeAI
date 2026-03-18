# Phase 01: Setup & Classification

## Entry Gate

```bash
devforgeai-validate phase-init ${STORY_ID} --workflow=release --project-root=.
# Exit 0: new workflow | Exit 1: resume | Exit 2: invalid | Exit 127: CLI not installed
```

## Contract

PURPOSE: Initialize release environment -- validate CWD, detect tech stack, classify project type, set phase applicability, clean stale markers.
REQUIRED SUBAGENTS: tech-stack-detector (BLOCKING)
REQUIRED ARTIFACTS: $STORY_ID, $ENVIRONMENT, $PROJECT_TYPE, $SKIP_PHASES, $TECH_STACK_INFO, $BUILD_CONFIG
STEP COUNT: 12 mandatory steps

---

## Mandatory Steps

### Step 1.1: Session Checkpoint Detection

EXECUTE: Check for interrupted release session and offer resume capability.
```
checkpoint_path = "devforgeai/workflows/${STORY_ID}-release-phase-state.json"
Glob(pattern=checkpoint_path)

IF checkpoint found:
    Read(file_path=checkpoint_path)
    AskUserQuestion:
        Question: "Found interrupted release session for ${STORY_ID}. Resume or start fresh?"
        Header: "Resume"
        Options:
            - label: "Resume from last checkpoint"
              description: "Continue from last completed phase"
            - label: "Start fresh"
              description: "Delete checkpoint and run complete release workflow"
        multiSelect: false

    IF user chooses "Resume":
        $RESUME_MODE = true
        $RESUME_PHASE = checkpoint.progress.current_phase
    ELSE:
        $RESUME_MODE = false

ELSE:
    $RESUME_MODE = false
```
VERIFY: Either checkpoint processed (resume variables set) or fresh start confirmed ($RESUME_MODE = false).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.1 --project-root=.`

---

### Step 1.2: Validate Project Root

EXECUTE: Read CLAUDE.md to confirm we are in the project root directory.
```
Read(file_path="CLAUDE.md")

IF Read succeeds AND content contains "DevForgeAI" or "devforgeai":
    CWD_VALID = true
    Display: "Project root validated"
ELSE:
    Glob(pattern=".claude/skills/*.md")
    IF results found:
        CWD_VALID = true
    ELSE:
        CWD_VALID = false
        HALT: AskUserQuestion("Cannot confirm project root. Provide correct project root path?")
```
VERIFY: CWD_VALID = true. If false, workflow HALTED via AskUserQuestion.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.2 --project-root=.`

---

### Step 1.3: Load Parameter Extraction Reference

EXECUTE: Load the parameter extraction reference to guide context extraction.
```
Read(file_path=".claude/skills/spec-driven-release/references/parameter-extraction.md")
```
VERIFY: File content loaded successfully (non-empty response from Read).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.3 --project-root=.`

---

### Step 1.4: Extract Story ID and Environment

EXECUTE: Extract story ID and target environment from conversation context.
```
# Method 1: YAML frontmatter in conversation
Look for: id: STORY-XXX

# Method 2: Explicit statement
Look for: "Story ID: STORY-XXX" or "Environment: staging/production"

# Method 3: File reference
Look for: @devforgeai/specs/Stories/STORY-XXX.story.md

# Method 4: /release command arguments
$1 = story ID, $2 = environment

$STORY_ID = extracted story ID (must match STORY-[0-9]+ pattern)
$ENVIRONMENT = extracted environment (default: "staging" if not specified)

IF $STORY_ID not found:
    HALT: AskUserQuestion("Unable to determine story ID. Which story should be released?")

IF $ENVIRONMENT not in ["staging", "production", "test"]:
    HALT: AskUserQuestion("Invalid environment. Choose staging or production.")

Display: "Story: ${STORY_ID} | Environment: ${ENVIRONMENT}"
```
VERIFY: $STORY_ID matches STORY-[0-9]+ pattern AND $ENVIRONMENT is set.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.4 --project-root=.`

---

### Step 1.5: Read Story File and Validate QA Status

EXECUTE: Read the story file and verify it has QA Approved status.
```
Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")

IF no story file found:
    HALT: "Story file not found for ${STORY_ID}"

Read(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md")

Grep(pattern="QA Approved", path="devforgeai/specs/Stories/${STORY_ID}.story.md", output_mode="content")

IF "QA Approved" NOT found in story status:
    HALT: "Story ${STORY_ID} is not QA Approved. Current status must be 'QA Approved' before release."

Display: "Story ${STORY_ID} - QA Approved confirmed"
```
VERIFY: Story file exists AND contains "QA Approved" in status section.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.5 --project-root=.`

---

### Step 1.6: Stale Marker Cleanup

EXECUTE: Check for stale release markers from previous runs and clean up if approved.
```
Glob(pattern="devforgeai/workflows/.release-phase-*.marker")

IF stale markers found:
    Display: "Found ${count} stale release markers from a previous run."
    AskUserQuestion:
        Question: "Stale release markers detected from a previous release attempt. Clean up before proceeding?"
        Header: "Cleanup"
        Options:
            - label: "Yes, delete stale markers and proceed"
              description: "Remove old markers and start fresh release"
            - label: "No, abort release"
              description: "Stop release workflow to investigate"
        multiSelect: false

    IF user selects cleanup:
        FOR marker in stale_markers:
            Write(file_path=marker, content="")  # Overwrite then delete handled by workflow
        Display: "Stale markers cleaned up"
    ELSE:
        HALT: "Release aborted - stale markers not cleaned"

ELSE:
    Display: "No stale markers found - clean starting state"
```
VERIFY: Either no stale markers existed OR user approved cleanup AND markers removed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.6 --project-root=.`

---

### Step 1.7: Tech Stack Detection

EXECUTE: Detect project technology stack using tech-stack-detector subagent.
```
Read(file_path=".claude/skills/spec-driven-release/references/tech-stack-detection.md")

# Invoke tech-stack-detector subagent (BLOCKING)
Agent(subagent_type="tech-stack-detector", prompt="Detect technology stack for project at current working directory. Report: languages, frameworks, build tools, package managers, test frameworks. Check for: package.json, Cargo.toml, pyproject.toml, *.csproj, go.mod, pom.xml, build.gradle.")

$TECH_STACK_INFO = {
    stack_type: detected stack (e.g., "nodejs", "python", "rust", "dotnet"),
    build_command: appropriate build command,
    output_directory: build output path,
    test_command: test execution command,
    package_manager: detected package manager
}

Display: "Tech Stack: ${TECH_STACK_INFO.stack_type} | Build: ${TECH_STACK_INFO.build_command}"
```
VERIFY: $TECH_STACK_INFO is populated with stack_type, build_command, and output_directory.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.7 --project-root=.`

---

### Step 1.8: Project Type Classification

EXECUTE: Classify project as library, cli, or api based on build configuration.
```
# Detect ecosystem from build config
Glob(pattern="Cargo.toml")
Glob(pattern="package.json")
Glob(pattern="pyproject.toml")

IF no config file found:
    AskUserQuestion:
        Question: "Unable to determine project type automatically. What type is this project?"
        Header: "Project Type"
        Options:
            - label: "library (no deployment target, publish only)"
              description: "Package/library that gets published to a registry"
            - label: "cli (deployable binary/executable)"
              description: "Command-line tool that gets installed or deployed"
            - label: "api (deployable HTTP service)"
              description: "Web API or service that runs on a server"
        multiSelect: false

# Read config and classify
IF Cargo.toml found:
    Read(file_path="Cargo.toml")
    IF has [lib] AND NOT has [[bin]] AND NOT exists src/main.rs: $PROJECT_TYPE = "library"
    ELIF has [[bin]]: $PROJECT_TYPE = "cli"
    ELIF has actix-web OR rocket OR axum dependency: $PROJECT_TYPE = "api"
    ELSE: AskUserQuestion (ambiguous)

IF package.json found:
    Read(file_path="package.json")
    IF NOT has "bin" field AND NOT has express/fastify/koa: $PROJECT_TYPE = "library"
    ELIF has "bin" field: $PROJECT_TYPE = "cli"
    ELIF has express OR fastify OR koa OR hapi: $PROJECT_TYPE = "api"
    ELSE: AskUserQuestion (ambiguous)

IF pyproject.toml found:
    Read(file_path="pyproject.toml")
    IF NOT has [project.scripts] AND NOT has uvicorn/gunicorn: $PROJECT_TYPE = "library"
    ELIF has [project.scripts]: $PROJECT_TYPE = "cli"
    ELIF has uvicorn OR gunicorn OR flask: $PROJECT_TYPE = "api"
    ELSE: AskUserQuestion (ambiguous)

Display: "Project Type: ${PROJECT_TYPE}"
```
VERIFY: $PROJECT_TYPE is one of: "library", "cli", "api".
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.8 --project-root=.`

---

### Step 1.9: Set SKIP_PHASES Based on Project Type

EXECUTE: Configure which phases to skip based on project classification.
```
IF $PROJECT_TYPE == "library":
    $SKIP_PHASES = [04, 05, 06]
    # Library: no staging, no production, no post-deploy validation
    # Phase 08 monitoring steps skipped (but cleanup still runs)
ELIF $PROJECT_TYPE == "cli" OR $PROJECT_TYPE == "api":
    $SKIP_PHASES = []
    # All phases active for deployable projects

Display: "Skip phases: ${SKIP_PHASES} (${PROJECT_TYPE} project)"
```
VERIFY: $SKIP_PHASES is set (empty array for cli/api, [04, 05, 06] for library).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.9 --project-root=.`

---

### Step 1.10: Display Phase Plan

EXECUTE: Show the user which phases are active and which are skipped.
```
Display:
"
Phase Plan for ${STORY_ID} (${PROJECT_TYPE} project)

| Phase | Name                          | Status  |
|-------|-------------------------------|---------|
| 01    | Setup & Classification        | Active  |
| 02    | Build & Package               | Active  |
| 03    | Pre-Release Validation        | Active  |
| 04    | Staging Deployment            | ${04 in SKIP_PHASES ? 'Skipped' : 'Active'} |
| 05    | Production Deployment         | ${05 in SKIP_PHASES ? 'Skipped' : 'Active'} |
| 06    | Post-Deployment Validation    | ${06 in SKIP_PHASES ? 'Skipped' : 'Active'} |
| 07    | Release Documentation         | Active  |
| 08    | Monitoring, Cleanup & Closure | Active  |
"
```
VERIFY: Phase plan displayed to user with correct Active/Skipped status.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.10 --project-root=.`

---

### Step 1.11: Load Build Config

EXECUTE: Load build configuration. Use defaults if not found.
```
Read(file_path="devforgeai/deployment/build-config.yaml")

IF file not found:
    $BUILD_CONFIG = {
        enabled: true,
        fail_on_build_error: true,
        timeout_seconds: 300
    }
    Display: "Build config not found, using defaults (build enabled)"
ELSE:
    $BUILD_CONFIG = parsed YAML content
    Display: "Build config loaded: enabled=${BUILD_CONFIG.enabled}"
```
VERIFY: $BUILD_CONFIG is populated (either from file or defaults).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.11 --project-root=.`

---

### Step 1.12: Validate Deployment Config Exists

EXECUTE: Check for deployment configuration files.
```
Glob(pattern="devforgeai/deployment/*.yaml")
Glob(pattern="devforgeai/deployment/*.yml")

IF no deployment configs found:
    IF $PROJECT_TYPE == "library":
        Display: "No deployment config found (expected for library project)"
    ELSE:
        Display: "Warning: No deployment configuration found in devforgeai/deployment/"
        AskUserQuestion:
            Question: "No deployment configuration found. Proceed anyway or create config first?"
            Header: "Deploy Config"
            Options:
                - label: "Proceed without config"
                  description: "Continue with defaults (may fail at deployment phase)"
                - label: "Abort to create config"
                  description: "Stop release to set up deployment configuration first"
            multiSelect: false

        IF user selects abort:
            HALT: "Release aborted - deployment config needed"
ELSE:
    Display: "Deployment config found: ${config_count} file(s)"
```
VERIFY: Either deployment configs exist OR user acknowledged proceeding without OR library project (no config expected).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=01 --step=1.12 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=01 --checkpoint-passed --project-root=.
```

## Phase 01 Completion Display

```
Phase 01 Complete: Setup & Classification
  Story: ${STORY_ID}
  Environment: ${ENVIRONMENT}
  Tech Stack: ${TECH_STACK_INFO.stack_type}
  Project Type: ${PROJECT_TYPE}
  Skip Phases: ${SKIP_PHASES}
  Build Enabled: ${BUILD_CONFIG.enabled}
```
