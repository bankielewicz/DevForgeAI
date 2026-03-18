# Phase 03: Pre-Release Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=release --from=02 --to=03 --project-root=.
```

## Contract

PURPOSE: Validate all prerequisites before deployment -- QA approval, tests passing, dependencies released, environment ready, deployment strategy selected.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Validation status (PASS/FAIL), $DEPLOYMENT_STRATEGY
STEP COUNT: 7 mandatory steps

---

## Mandatory Steps

### Step 3.1: Load Pre-Release Validation References

EXECUTE: Load validation reference and release checklist.
```
Read(file_path=".claude/skills/spec-driven-release/references/pre-release-validation.md")
Read(file_path=".claude/skills/spec-driven-release/references/release-checklist.md")
```
VERIFY: Both files loaded successfully (non-empty Read responses).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=03 --step=3.1 --project-root=.`

---

### Step 3.2: Load Story File and QA Report

EXECUTE: Read story file and locate QA report.
```
Read(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md")

Glob(pattern="devforgeai/qa/reports/${STORY_ID}/*.md")

IF QA report found:
    Read(file_path=latest_qa_report)
    $QA_REPORT_AVAILABLE = true
    Display: "QA report loaded: ${qa_report_path}"
ELSE:
    $QA_REPORT_AVAILABLE = false
    Display: "Warning: No QA report found for ${STORY_ID}"
```
VERIFY: Story file loaded. QA report status known ($QA_REPORT_AVAILABLE set).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=03 --step=3.2 --project-root=.`

---

### Step 3.3: Validate QA Approval Gate

EXECUTE: Verify story has QA Approved status and QA report shows PASS.
```
Grep(pattern="Current Status.*QA Approved", path="devforgeai/specs/Stories/${STORY_ID}.story.md", output_mode="content")

IF "QA Approved" NOT found:
    HALT: "GATE FAILED: Story ${STORY_ID} status is not 'QA Approved'. Cannot release."

IF $QA_REPORT_AVAILABLE:
    Grep(pattern="PASS|APPROVED", path=latest_qa_report, output_mode="content")
    IF QA report does NOT show PASS:
        HALT: "GATE FAILED: QA report does not show PASS for ${STORY_ID}."

Display: "QA Approval Gate: PASSED"
```
VERIFY: Story status = "QA Approved" AND (QA report shows PASS OR no QA report but status is approved).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=03 --step=3.3 --project-root=.`

---

### Step 3.4: Validate Test Passing Gate

EXECUTE: Verify all tests pass for the story.
```
IF $QA_REPORT_AVAILABLE:
    Grep(pattern="tests? (pass|passing|100%)", path=latest_qa_report, output_mode="content", -i=true)
    IF test results indicate failure:
        HALT: "GATE FAILED: Tests not passing per QA report."
    Display: "Test Passing Gate: PASSED (from QA report)"
ELSE:
    Display: "No QA report - running tests to verify..."
    IF $TECH_STACK_INFO.stack_type == "nodejs":
        Bash(command="npm test", timeout=120000)
    ELIF $TECH_STACK_INFO.stack_type == "python":
        Bash(command="pytest", timeout=120000)
    ELIF $TECH_STACK_INFO.stack_type == "rust":
        Bash(command="cargo test", timeout=120000)

    IF exit_code != 0:
        HALT: "GATE FAILED: Tests failed. Fix tests before release."
    Display: "Test Passing Gate: PASSED (live test run)"
```
VERIFY: Tests confirmed passing (either from QA report or live execution).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=03 --step=3.4 --project-root=.`

---

### Step 3.5: Validate Dependency Gate

EXECUTE: Check if story has blocking dependencies.
```
Grep(pattern="depends[_ -]on|blocked[_ -]by|dependency", path="devforgeai/specs/Stories/${STORY_ID}.story.md", output_mode="content", -i=true)

IF dependencies found:
    FOR each dependency_story_id:
        Glob(pattern="devforgeai/specs/Stories/${dependency_story_id}*.story.md")
        IF story file found:
            Grep(pattern="Current Status.*Released", path=dependency_story_file, output_mode="content")
            IF NOT released:
                Display: "Warning: Dependency ${dependency_story_id} is not Released"
                $BLOCKING_DEPS[] = dependency_story_id

    IF $BLOCKING_DEPS.length > 0:
        AskUserQuestion:
            Question: "Blocking dependencies found: ${BLOCKING_DEPS.join(', ')}. Proceed anyway?"
            Header: "Dependencies"
            Options:
                - label: "Proceed despite blocking dependencies"
                  description: "Release anyway (dependencies may not affect this story)"
                - label: "Abort release"
                  description: "Wait for dependencies to be released first"
            multiSelect: false

        IF user selects abort:
            HALT: "Release aborted - blocking dependencies"

Display: "Dependency Gate: PASSED"
```
VERIFY: Either no blocking dependencies OR user acknowledged and chose to proceed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=03 --step=3.5 --project-root=.`

---

### Step 3.6: Validate Environment Readiness

EXECUTE: Check deployment configuration exists for target environment.
```
Glob(pattern="devforgeai/deployment/*.yaml")
Glob(pattern="devforgeai/deployment/*.yml")

IF $PROJECT_TYPE == "library":
    Display: "Environment check skipped (library project - no deployment target)"
ELIF deployment configs found:
    Display: "Deployment configuration available for ${ENVIRONMENT}"
    FOR each config_file:
        Display: "  Found: ${config_file}"
ELSE:
    Display: "Warning: No deployment configuration found"
    Read(file_path=".claude/skills/spec-driven-release/references/configuration-guide.md")

Display: "Environment Readiness Gate: PASSED"
```
VERIFY: Environment readiness assessed (configs found, library project, or user acknowledged).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=03 --step=3.6 --project-root=.`

---

### Step 3.7: Select Deployment Strategy

EXECUTE: Ask user to select deployment strategy (skip for library projects).
```
IF $PROJECT_TYPE == "library":
    $DEPLOYMENT_STRATEGY = "publish-only"
    Display: "Deployment strategy: publish-only (library project)"
ELSE:
    Read(file_path=".claude/skills/spec-driven-release/references/deployment-strategies.md")

    AskUserQuestion:
        Question: "Select deployment strategy for ${ENVIRONMENT}:"
        Header: "Strategy"
        Options:
            - label: "Blue-Green (Recommended)"
              description: "Zero-downtime deployment with instant rollback. Runs two identical environments."
            - label: "Canary"
              description: "Progressive rollout. Routes small percentage of traffic first, then increases."
            - label: "Rolling"
              description: "Gradual replacement of instances. Some downtime possible during transition."
            - label: "Recreate"
              description: "Stop old version, start new version. Simple but has downtime."
        multiSelect: false

    $DEPLOYMENT_STRATEGY = user_selection
    Display: "Deployment strategy selected: ${DEPLOYMENT_STRATEGY}"
```
VERIFY: $DEPLOYMENT_STRATEGY is set to a valid strategy name.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=03 --step=3.7 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=03 --checkpoint-passed --project-root=.
```

## Phase 03 Completion Display

```
Phase 03 Complete: Pre-Release Validation
  QA Approval: PASSED
  Tests: PASSED
  Dependencies: PASSED
  Environment: ${ENVIRONMENT} ready
  Strategy: ${DEPLOYMENT_STRATEGY}
  All gates passed - ready for deployment
```
