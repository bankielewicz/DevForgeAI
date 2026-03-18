# Phase 07: DoD Update

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=06 --to=07
# Exit 0: proceed | Exit 1: Phase 06 incomplete
```

## Contract

PURPOSE: Update the story file's Definition of Done section, Implementation Notes, and workflow status to reflect completed work.
REQUIRED SUBAGENTS: None (file operations only)
REQUIRED ARTIFACTS: None
STEP COUNT: 5 mandatory steps

**CRITICAL FORMAT RULE:** Implementation Notes MUST use a FLAT LIST. NO ### subsections under ## Implementation Notes. The DoD validator parser stops at the first ### header, making items invisible. (Reference: `.claude/rules/workflow/commit-failure-recovery.md`)

---

## Mandatory Steps

### Step 1: Mark Completed Items in DoD

EXECUTE: Mark all completed Definition of Done items as [x] in the story file.
```
# For each completed DoD item:
Edit(file_path="${STORY_FILE}", old_string="- [ ] <DoD item text>", new_string="- [x] <DoD item text>")
```
VERIFY: Grep confirms completed items are marked.
```
Grep(pattern="- \\[x\\]", path="${STORY_FILE}")
```

### Step 2: Add DoD Items to Implementation Notes (FLAT LIST)

EXECUTE: Ensure `## Implementation Notes` section exists. Add completed DoD items as a flat list.
```
# Check if section exists:
Grep(pattern="^## Implementation Notes", path="${STORY_FILE}")
IF not found: Add section via Edit()

# Add items in CORRECT format (FLAT LIST, NO ### subsections):
# CORRECT:
#   ## Implementation Notes
#
#   **Developer:** DevForgeAI AI Agent
#   **Implemented:** ${CURRENT_DATE}
#
#   - [x] DoD item 1 - Completed: description
#   - [x] DoD item 2 - Completed: description
#
# WRONG (WILL FAIL VALIDATION):
#   ## Implementation Notes
#   ### Definition of Done Status    <-- NO! Parser stops here!
#   - [x] DoD item 1
```
VERIFY: Items are directly under `## Implementation Notes`, not under any ### subsection.
```
Grep(pattern="^### ", path="${STORY_FILE}")
# Verify no ### headers appear between "## Implementation Notes" and the DoD items
```

### Step 3: Validate DoD Format

EXECUTE: Run the DoD format validator.
```bash
source .venv/bin/activate && devforgeai-validate validate-dod ${STORY_FILE}
```
VERIFY: Exit code 0 = format valid.
```
IF exit code != 0:
  Read(file_path=".claude/rules/workflow/commit-failure-recovery.md")
  # Follow recovery workflow to fix format
  # Re-run validator until exit code 0
  HALT if cannot achieve exit code 0.
```

### Step 4: Update Workflow Status

EXECUTE: Update the story file's workflow status to "Dev Complete".
```
Edit(file_path="${STORY_FILE}", old_string="status: In Development", new_string="status: Dev Complete")
```
VERIFY: Status updated in story file.
```
Grep(pattern="status: Dev Complete", path="${STORY_FILE}")
IF not found: HALT — "Workflow status not updated."
```

### Step 5: Populate TDD Workflow Summary Table

EXECUTE: Read phase-state.json and populate the TDD Workflow Summary and Files Created/Modified tables in the story file.
```
Read(file_path="devforgeai/workflows/${STORY_ID}-phase-state.json")
# Extract phase list, status, timing
# Populate TDD Workflow Summary table
# Populate Files Created/Modified table
# Skip guard: Only populate if tables are empty (no data rows after header)
```
VERIFY: Tables contain data rows.
```
Grep(pattern="\\| 01 |\\| 02 |\\| Phase", path="${STORY_FILE}")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=07 --checkpoint-passed
# Exit 0: proceed to Phase 08 | Exit 1: DoD format invalid
```
