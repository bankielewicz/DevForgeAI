# STORY-129: CLI Availability Check - Implementation Plan

**Objective:** Implement Phase 01.0.5 in preflight-validation.md to check CLI availability before running CLI-dependent validations.

**Status:** Ready for execution

**Date Created:** 2025-12-23

---

## Executive Summary

Implement a new preflight validation step (Phase 01.0.5) that gracefully handles the case where the devforgeai CLI is not installed. This prevents cryptic "Unknown command" errors and allows the workflow to fall back to grep-based validation patterns.

**Test Coverage:** 5 acceptance criteria tests (all currently failing)
- test-ac1-step-exists.sh
- test-ac2-warning-format.sh
- test-ac3-version-display.sh
- test-ac4-skip-gracefully.sh
- test-ac5-fallback-docs.sh

---

## Requirements Analysis

### What Tests Expect

**Test AC#1 (Step Exists):**
- Header: "## Phase 01.0.5: CLI Availability Check"
- Contains: `command -v devforgeai`
- Contains: `CLI_AVAILABLE` variable

**Test AC#2 (Warning Format):**
- Warning: "WARN: devforgeai CLI not installed"
- Message: "Hook checks will be skipped"
- Message: "Manual validation required"

**Test AC#3 (Version Display):**
- Success pattern: "✓ devforgeai CLI:"
- Version retrieval: `devforgeai --version` or `--version`

**Test AC#4 (Skip Gracefully):**
- Skip pattern: "Skipping:"
- Message: "CLI not available"
- Lists skipped commands: check-hooks, validate-dod, validate-context (at least 2)

**Test AC#5 (Fallback Documentation):**
- Section: "Manual Validation" or "Fallback Validation"
- Documents: grep-based hook validation
- Documents: read-based context validation
- Documents: risks/limitations/skip scenarios

### Story File Requirements (STORY-129)

**Functional Requirements:**
1. Check if `devforgeai` command is available using `command -v`
2. Set `CLI_AVAILABLE` variable (true/false) for downstream use
3. Display warning if CLI not installed (non-fatal)
4. Display version if CLI is installed
5. Document fallback validation patterns
6. Document risks of CLI unavailability

**Implementation Details from Story:**
- Bash code block shows: `if ! command -v devforgeai &> /dev/null; then ... fi`
- Success message format: "✓ devforgeai CLI: {version}"
- Version retrieval: `devforgeai --version 2>/dev/null || echo "unknown"`
- Token cost: ~100 tokens
- Fallback validation patterns for: hooks, DoD checkboxes, context files

---

## File Structure Analysis

### Target File
**File:** `.claude/skills/devforgeai-development/references/preflight-validation.md`

**Current Structure:**
- Line 43-105: Phase 01.0 (Validate Project Root)
- Line 104-105: Separator and CRITICAL note
- Line 108+: Phase 01.1 (Validate Git Repository Status)

**Insertion Point:**
- **After Line 105:** Current line "---" separator after Phase 01.0
- **Before Line 108:** Before "## Phase 01.1" header
- **Insert before existing separator on line 106**

### Exact Line Numbers
- Phase 01.0 ends at line 105 with "---"
- Phase 01.1 starts at line 108 with "## Phase 01.1"
- **New section goes at line 106-107 (between the separator and Phase 01.1)**

### Format to Match

From Phase 01.0:
```
## Phase 01.0: Validate Project Root [MANDATORY - FIRST STEP]

**Purpose:** [description]

**Execute BEFORE Phase 01.1 (Git validation):**

```
[code block with pseudocode]
```

**On Failure:**

```
[error messages]
```

**CRITICAL:** [important note]

---
```

### Pattern Applied to Phase 01.0.5

The new section should follow the same structure:
1. Header with phase number, title, and attributes
2. **Purpose:** section
3. **Execute BEFORE** section noting where it fits
4. Implementation code block (bash-like pseudocode)
5. **Token Cost:** line
6. Downstream Impact section
7. Fallback Validation section (replaces "On Failure")
8. Risks documentation
9. Success/Failure criteria
10. Separator "---"

---

## Implementation Content

### Section to Insert

**Header:**
`## Phase 01.0.5: CLI Availability Check [MANDATORY] (STORY-129)`

**Content Structure:**
1. Purpose statement
2. When to execute (after Phase 01.0, before Phase 01.1)
3. Token cost: ~100 tokens
4. Bash implementation code block:
   - `command -v devforgeai` check
   - Setting `CLI_AVAILABLE` variable
   - Warning messages for CLI not available
   - Success message with version
   - Version retrieval: `devforgeai --version`

5. Downstream Impact section:
   - Commands to skip when `CLI_AVAILABLE=false`
   - List: devforgeai check-hooks, validate-dod, validate-context
   - Fallback: grep-based validation patterns

6. Fallback Validation section:
   - Hook Eligibility (grep pattern)
   - DoD Validation (grep pattern)
   - Context Validation (Read checks)

7. Risks section:
   - CLI fallback may miss validations
   - Grep-based fallback needs testing
   - CLI version check can fail silently

8. Success/Failure criteria:
   - Success: `CLI_AVAILABLE` variable set
   - Failure: N/A (always succeeds, warning only)

---

## Implementation Steps

### Step 1: Read Current File Structure
- Read preflight-validation.md to understand exact format
- Identify insertion line (should be around line 105-107)
- Note the exact formatting of Phase 01.0

### Step 2: Prepare Content
- Create full Phase 01.0.5 section matching test expectations
- Ensure all 5 acceptance criteria are addressed
- Follow the style and format of Phase 01.0

### Step 3: Insert Section
- Use Edit tool to insert after Phase 01.0 separator
- Ensure proper formatting and line breaks
- Maintain YAML/Markdown consistency

### Step 4: Run Tests
- Execute all 5 test files
- Verify each test passes
- Check for any format violations

### Step 5: Validation
- Verify insertion location is correct
- Confirm downstream phases still accessible
- Check no markdown syntax errors

---

## Test Verification Checklist

- [ ] test-ac1-step-exists.sh: Header and variables exist
- [ ] test-ac2-warning-format.sh: Warning messages format correct
- [ ] test-ac3-version-display.sh: Version display pattern correct
- [ ] test-ac4-skip-gracefully.sh: Skip messages and command lists present
- [ ] test-ac5-fallback-docs.sh: Fallback documentation complete

---

## Content to Insert (Final Markdown)

Location: Insert between line 105 (after "---") and line 108 (before "## Phase 01.1")

```markdown
## Phase 01.0.5: CLI Availability Check [MANDATORY] (STORY-129)

**Purpose:** Verify devforgeai CLI is installed before attempting CLI-based validations. Prevent failures due to missing CLI by setting fallback mode and documenting manual validation patterns.

**When to execute:** After Phase 01.0 (Project Root validation), before Phase 01.1 (Git Repository validation)

**Token cost:** ~100 tokens

**Implementation:**

```bash
# Check if devforgeai CLI is available
if ! command -v devforgeai &> /dev/null; then
    CLI_AVAILABLE=false
    echo "WARN: devforgeai CLI not installed"
    echo "  - Hook checks will be skipped"
    echo "  - Manual validation required"
else
    CLI_AVAILABLE=true
    DEVFORGEAI_VERSION=$(devforgeai --version 2>/dev/null || echo "unknown")
    echo "✓ devforgeai CLI: $DEVFORGEAI_VERSION"
fi

# Store flag for downstream steps
$CLI_AVAILABLE = CLI_AVAILABLE
```

---

## Downstream Impact

**When `CLI_AVAILABLE=false`, the following CLI-based validations are SKIPPED:**
- `devforgeai check-hooks` - Hook eligibility verification
- `devforgeai validate-dod` - Definition of Done checkbox validation
- `devforgeai validate-context` - Context file existence validation

**Fallback:** Grep-based and Read-based validation patterns documented in "Manual Validation" section below.

**Message on skip:**
```
Skipping: CLI-based hook checks (CLI not available)
Skipping: CLI-based DoD validation (CLI not available)
Skipping: CLI-based context validation (CLI not available)
```

---

## Manual Validation When CLI Not Available

### Hook Eligibility (replaces devforgeai check-hooks)

**Grep-based fallback pattern:**
```
Grep(
  pattern="operation: dev",
  path="src/devforgeai/config/hooks.yaml",
  output_mode="count"
)
```

If count > 0: Hooks are eligible for dev operation.

### DoD Validation (replaces devforgeai validate-dod)

**Grep-based fallback pattern:**
```
Grep(
  pattern="^\\s*-\\s*\\[[ x]\\]",
  path="{STORY_FILE}",
  output_mode="count"
)
```

Count represents the number of Definition of Done checkbox items in the story file.

### Context Validation (replaces devforgeai validate-context)

**Read-based fallback pattern:**

For each context file, verify it exists and is readable:

```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

If ANY Read fails: Context is incomplete. Run `/create-context` to generate missing files.

---

## Risks

**Risk: CLI fallback may miss validations**
- Grep-based patterns are simpler than full CLI validation
- Some edge cases in hooks.yaml may not be detected
- Mitigation: Document what CLI checks catch that grep doesn't

**Risk: Grep-based fallback produces false positives**
- Pattern matching may match incorrect lines
- Yaml structure changes may break patterns
- Mitigation: Test fallback patterns against real story/hook files

**Risk: CLI version check can fail silently**
- `devforgeai --version` may not exist in early versions
- Fallback to "unknown" may mask version detection issues
- Mitigation: User can manually verify CLI version if needed

---

## Success Criteria

**Success:**
- `CLI_AVAILABLE` variable is set (true or false) based on CLI detection
- All warning messages display correctly when CLI not available
- Version displays correctly when CLI is available
- Downstream phases can skip CLI-based validations gracefully
- Fallback validation patterns documented

**Failure:**
- N/A - This step always succeeds (warning-only, never fails preflight)

---

## References

**Story File:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-129-cli-availability-check.story.md`

**Target File:** `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/references/preflight-validation.md`

**Test Files:**
- `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-129/test-ac1-step-exists.sh`
- `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-129/test-ac2-warning-format.sh`
- `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-129/test-ac3-version-display.sh`
- `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-129/test-ac4-skip-gracefully.sh`
- `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-129/test-ac5-fallback-docs.sh`

---

## Next Steps

1. **Execute:** Run this plan to implement Phase 01.0.5
2. **Validate:** Run all 5 test files to verify implementation
3. **Review:** Check formatting and markdown syntax
4. **Commit:** Create git commit for STORY-129 implementation
5. **QA:** Run full preflight-validation.md validation

