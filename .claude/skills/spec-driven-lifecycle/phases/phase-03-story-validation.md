# Phase 03: Story Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=02 --to=03
```

## Contract

PURPOSE: Load and validate story file before skill invocation. Verify story status, prerequisites, and quality gate requirements. Story Management mode only.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Validated story file with status confirmed
STEP COUNT: 5 mandatory steps

---

## Mandatory Steps

### Step 1: Load Story Document

EXECUTE: Load the story file and extract YAML frontmatter.
```
story_files = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
Read(file_path=story_files[0])
```

Extract from frontmatter:
- `status` - Current workflow state
- `points` - Story point estimate
- `priority` - High/Medium/Low
- `epic` - Parent epic (if any)
- `sprint` - Sprint assignment (if any)

VERIFY: Story file loads successfully and contains required frontmatter fields.
```
Grep(pattern="^status:", path=story_files[0])
IF no match: HALT -- "Story file missing status field."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=1`

### Step 2: Validate Story Status

EXECUTE: Check that story status is valid for orchestration.
```
Valid statuses for orchestration:
- "Backlog" -> needs Architecture
- "Architecture" -> needs /create-context completion
- "Ready for Dev" -> ready for spec-driven-dev
- "In Development" -> may be resuming
- "Dev Complete" -> ready for spec-driven-qa
- "QA In Progress" -> QA running
- "QA Approved" -> ready for spec-driven-release
- "QA Failed" -> needs retry
- "Releasing" -> release in progress
- "Released" -> already done (HALT gracefully)
```

VERIFY: Status is one of the 11 valid states.
```
IF status == "Released":
  Display: "Story ${STORY_ID} already released."
  HALT (graceful - return already_released)

IF status not in valid_statuses:
  HALT -- "Invalid story status: {status}. Expected one of 11 valid states."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=2`

### Step 3: Check Prerequisites

EXECUTE: Verify prerequisites are met for the current status transition.
```
# Check story has required sections
Grep(pattern="## Acceptance Criteria", path=story_files[0])
Grep(pattern="## Technical Specification", path=story_files[0])

# Check dependencies if any
Grep(pattern="depends_on:", path=story_files[0])
IF dependencies found:
  FOR each dependency_id:
    dep_files = Glob(pattern="devforgeai/specs/Stories/${dependency_id}*.story.md")
    IF dep_files found:
      Read dep file, check status
      IF dep status != "Released" AND dep status != "QA Approved":
        Display: "Dependency ${dependency_id} not complete (status: {dep_status})"
        AskUserQuestion:
          Question: "Dependency ${dependency_id} is not complete. Proceed anyway?"
          Header: "Dependency"
          Options:
            - label: "Proceed (skip dependency check)"
              description: "Continue despite incomplete dependency"
            - label: "HALT"
              description: "Stop and resolve dependency first"
          multiSelect: false
```

VERIFY: All required sections present. Dependencies resolved or user-approved skip.
```
IF missing "## Acceptance Criteria": HALT -- "Story missing Acceptance Criteria section."
IF missing "## Technical Specification": HALT -- "Story missing Technical Specification section."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=3`

### Step 4: Determine Target Skill

EXECUTE: Based on story status, determine which skill should be invoked next.
```
IF status == "Backlog" OR status == "Architecture":
  target_skill = "spec-driven-architecture"
  target_action = "Create/update context files"

ELSE IF status == "Ready for Dev" OR status == "In Development":
  target_skill = "spec-driven-dev"
  target_action = "TDD implementation (Red-Green-Refactor)"

ELSE IF status == "Dev Complete" OR status == "QA Failed":
  target_skill = "spec-driven-qa"
  target_action = "Quality validation (deep mode)"

ELSE IF status == "QA Approved":
  target_skill = "spec-driven-release"
  target_action = "Release to staging/production"

ELSE IF status == "QA In Progress" OR status == "Releasing":
  target_skill = "WAIT"
  target_action = "Operation already in progress"
  Display: "Story ${STORY_ID} has an operation in progress (status: {status}). Waiting."
```

VERIFY: target_skill is set and corresponds to a valid skill name.
```
IF target_skill is not set: HALT -- "Cannot determine target skill for status: {status}"
IF target_skill == "WAIT":
  AskUserQuestion:
    Question: "Story is in '{status}' state. Force re-run?"
    Header: "In Progress"
    Options:
      - label: "Force re-run"
        description: "Override and re-invoke the appropriate skill"
      - label: "HALT"
        description: "Stop and wait for current operation to complete"
    multiSelect: false
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=4`

### Step 5: Quality Gate Pre-Check

EXECUTE: Verify the relevant quality gate allows the transition.
```
Read(file_path="references/quality-gates.md")  # Load from skill references

# Check gate requirements based on status transition
IF status == "Architecture" -> needs Gate 1 (Context Validation)
  Glob(pattern="devforgeai/specs/context/*.md")
  IF count != 6: HALT -- "Gate 1 FAILED: Missing context files ({count}/6)"

IF status == "Dev Complete" -> needs Gate 2 (Test Passing)
  # Gate 2 is enforced by spec-driven-qa, just verify entry conditions
  Display: "Gate 2 will be enforced by spec-driven-qa"

IF status == "QA Approved" -> needs Gate 3 (QA Approval)
  Grep(pattern="QA.*(APPROVED|Approved|approved)", path=story_files[0])
  IF no match: HALT -- "Gate 3 FAILED: Story not QA Approved"
```

VERIFY: Relevant quality gate pre-check passes.
```
Display: "Quality gate pre-check: PASSED for status '{status}'"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=5`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03 --checkpoint-passed
```
