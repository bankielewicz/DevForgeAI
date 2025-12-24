# STORY-087: /validate-epic-coverage Implementation Plan

**Status:** Planning
**Created:** 2025-12-23
**Target:** STORY-087 (Slash Command Interface - Currently In Development)
**Context:** Implementing the complete `/validate-epic-coverage` command workflow

---

## Overview

STORY-087 defines the slash command interface for epic coverage validation. The framework spec is complete and detailed (.claude/commands/validate-epic-coverage.md), but the actual command implementation is incomplete. This plan details implementing the full command workflow following the TDD methodology.

---

## Current State Assessment

### What Exists ✅
- **Specification:** Complete 463-line command spec with all phases and workflows
- **Gap Detection:** gap-detector.sh (STORY-085, QA Approved) - working, detected 99 orphaned stories
- **Coverage Reporting:** generate-report.sh (STORY-086, QA Approved) - working, generates JSON/markdown reports
- **Epic Files:** 30 epics with feature definitions in devforgeai/specs/Epics/
- **Story Files:** 136+ stories with epic linking in devforgeai/specs/Stories/

### What's Missing ❌
1. **Command Implementation:** No bash/shell script executing the workflow phases
2. **Argument Parsing:** Phase 0 & 0.1 (epic ID validation, mode detection)
3. **Report Parsing:** Extracting structured data from gap-detector.sh and generate-report.sh outputs
4. **Result Display:** Phase 2 (formatting and displaying results with color coding)
5. **Interactive Prompts:** Phase 2.1 (AskUserQuestion for gap resolution - depends on STORY-088)
6. **Tests:** No test coverage for command workflow

### Consistency Issues ⚠️
- Gap detection report shows 27.2% consistency score
- 99 orphaned stories claiming epics not listed in those epics' Stories tables
- Impact: Features may not have accurate coverage counts

---

## Implementation Strategy

### TDD Workflow (Mandatory)

```
Phase 1 (Red):     Write failing tests for each command phase
Phase 2 (Green):   Implement minimal code to pass tests
Phase 3 (Refactor): Clean up, optimize, extract helpers
```

### Architecture Approach

**Pattern:** Lean Orchestration Command (from CLAUDE.md pattern)
- **Thin wrapper:** Parse arguments, validate inputs
- **Service delegation:** Call existing gap-detector.sh and generate-report.sh
- **Output formatting:** Transform service output into user-friendly display

**File Structure:**
```
Command implementation options:
  Option A: Shell script wrapper (preferred for Claude Code native execution)
             Location: devforgeai/commands/validate-epic-coverage.sh

  Option B: Bash function in .claude/hooks/
             (not recommended - command spec expects executable)
```

**Data Flow:**
```
User Input (EPIC-015 --interactive)
    ↓
Phase 0: Argument Parsing
    - Parse epic ID, flags
    - Validate format (EPIC-NNN)
    - Normalize case
    ↓
Phase 0.1: Mode Detection
    - Detect interactive vs quiet
    - Detect CI environment
    ↓
Phase 1: Execute Validation
    - Glob epic files
    - Execute gap-detector.sh
    - Execute generate-report.sh
    - Parse JSON outputs
    ↓
Phase 2: Display Results
    - Format color-coded output (✅ ⚠️ ❌)
    - Show coverage percentages
    - List actionable gaps (top 10)
    ↓
Phase 2.1: Interactive Gap Resolution
    - AskUserQuestion for single gap
    - AskUserQuestion for multiple gaps
    - Invoke devforgeai-story-creation skill
    ↓
Output → User
```

---

## Implementation Phases

### Phase 1: Test Infrastructure
**Objective:** Create test suite for command phases

**Tests to Create:**
1. `test_phase0_help_flag.sh` - Tests --help flag displays help text
2. `test_phase0_valid_epic_id.sh` - Tests EPIC-015 format validation
3. `test_phase0_invalid_epic_id.sh` - Tests rejection of invalid formats
4. `test_phase0_epic_not_found.sh` - Tests error when epic doesn't exist
5. `test_phase01_mode_detection.sh` - Tests --interactive, --quiet, --ci flags
6. `test_phase1_single_epic.sh` - Tests validation for single epic
7. `test_phase1_all_epics.sh` - Tests validation for all epics
8. `test_phase2_output_format.sh` - Tests color-coded output formatting
9. `test_phase2_actionable_gaps.sh` - Tests /create-story command suggestions
10. `test_phase21_interactive_prompt.sh` - Tests AskUserQuestion flow (requires STORY-088)

**Test Location:** `devforgeai/tests/STORY-087/`

**Test Fixtures:**
- Sample epic files (existing in devforgeai/specs/Epics/)
- Sample story files (existing in devforgeai/specs/Stories/)
- Expected output files for comparison

### Phase 2: Argument Parsing (Phase 0 & 0.1)
**Objective:** Implement argument validation and mode detection

**Implementation:**
1. Create command wrapper script
2. Parse $1 (epic ID or flag)
3. Validate format: `^[Ee][Pp][Ii][Cc]-[0-9]{3}$`
4. Detect mode flags: --interactive, --quiet, --ci
5. Auto-detect CI environment: check CI env var or no TTY
6. Return normalized EPIC_ID and MODE for subsequent phases

**Functions to Implement:**
- `parse_arguments()` - Parse $1, $2, etc.
- `validate_epic_id()` - Check EPIC-NNN format
- `detect_mode()` - Determine interactive vs quiet
- `display_help()` - Show help text from spec
- `list_valid_epics()` - Extract epic IDs from Glob

**Acceptance Criteria:**
- ✅ `--help` displays help text
- ✅ `epic-015` normalizes to `EPIC-015`
- ✅ Invalid format `EPIC-99` rejected with error
- ✅ Epic not found shows valid epic list
- ✅ `--quiet` suppresses interactive prompts
- ✅ CI environment auto-detected

### Phase 3: Service Integration (Phase 1)
**Objective:** Execute existing services and parse outputs

**Implementation:**
1. Call `devforgeai/epic-coverage/generate-report.sh` → capture JSON output
2. Call `devforgeai/traceability/gap-detector.sh` → capture JSON output
3. Parse JSON using `jq` (standard in Claude Code)
4. Extract: coverage %, feature names, story IDs, gaps
5. Handle errors from services gracefully

**Functions to Implement:**
- `execute_gap_detector()` - Run gap-detector.sh, parse output
- `execute_report_generator()` - Run generate-report.sh, parse output
- `extract_coverage_percentage()` - Get % from report
- `extract_gaps()` - Get gap details from gap detector
- `merge_results()` - Combine service outputs into unified structure

**Acceptance Criteria:**
- ✅ Services run successfully (exit code 0)
- ✅ JSON output parsed correctly
- ✅ Coverage percentages extracted
- ✅ Gaps list populated
- ✅ Errors handled gracefully (missing files, parse errors)

### Phase 4: Output Formatting (Phase 2)
**Objective:** Display results with proper formatting and color coding

**Implementation:**
1. Format header with box drawing characters (━┃└─)
2. Color coding: ✅ (100%), ⚠️ (50-99%), ❌ (<50%)
3. For single-epic: feature-by-feature breakdown
4. For all-epics: summary table format
5. Display actionable gaps: /create-story suggestions (top 10)
6. Shell-safe escaping for feature names with special chars

**Functions to Implement:**
- `display_header()` - Draw title box
- `display_single_epic_report()` - Feature breakdown
- `display_all_epics_report()` - Summary table
- `display_actionable_gaps()` - /create-story suggestions
- `escape_shell_safe()` - Escape quotes, backticks, $
- `format_percentage()` - Return color-coded emoji + %

**Acceptance Criteria:**
- ✅ Header renders with box drawing characters
- ✅ Coverage > 100% → ✅, 50-99% → ⚠️, <50% → ❌
- ✅ Feature list shows coverage status
- ✅ Gaps list shows /create-story commands
- ✅ Special characters in names are escaped
- ✅ Output matches spec examples

### Phase 5: Interactive Prompts (Phase 2.1)
**Objective:** Implement gap-to-story resolution workflow (DEPENDS ON STORY-088)

**Prerequisite:** STORY-088 must be QA Approved with:
- Context markers documented (Story ID, Epic ID, Feature #, Batch Mode flag)
- devforgeai-story-creation skill updated to accept context
- Batch mode support tested

**Implementation (if STORY-088 ready):**
1. Check if PROMPT_MODE == "quiet" → skip entire phase
2. For single gap: AskUserQuestion with 3 options
3. For multiple gaps: AskUserQuestion with 3 options + multi-select
4. Generate context markers based on gap data
5. Invoke devforgeai-story-creation skill
6. Display confirmation message

**Functions to Implement:**
- `should_show_prompts()` - Check mode and gap count
- `prompt_single_gap()` - Ask about single gap
- `prompt_multiple_gaps()` - Ask about multiple gaps
- `generate_context_markers()` - Build Story ID, Epic ID, Feature #, etc.
- `invoke_story_creation()` - Call skill with context
- `batch_create_stories()` - Loop through selected gaps

**Acceptance Criteria (IF STORY-088 approved):**
- ✅ Single gap shows "Create now / Skip / Later" prompt
- ✅ Multiple gaps show "Create all / Select specific / Skip" prompt
- ✅ Selected gaps create stories successfully
- ✅ Quiet mode suppresses all prompts
- ✅ Skill invocation passes correct context
- ✅ Error handling for story creation failures

---

## Key Dependencies

### Hard Dependencies (MUST exist)
1. ✅ **gap-detector.sh** (STORY-085) - QA Approved, working
2. ✅ **generate-report.sh** (STORY-086) - QA Approved, working
3. ✅ **devforgeai/specs/Epics/*.epic.md** - 30 epics existing
4. ✅ **devforgeai/specs/Stories/*.story.md** - 136+ stories existing

### Soft Dependencies (Can implement, will need later)
1. ⏳ **STORY-088** (Create-Story Integration) - For Phase 2.1 interactive prompts
   - Needed for: Skill invocation with context markers
   - Workaround: Phase 2.1 can be marked "pending STORY-088 approval"

2. ⏳ **STORY-089** (DevForgeAI Command Integration) - For quality gates
   - Not critical for Phase 0-2
   - Can be deferred to future story

### Technology Stack (from tech-stack.md)
- **Language:** Bash (Claude Code native ✅)
- **Parsing:** Grep patterns, jq for JSON (no Python/npm deps)
- **Tools:** Read, Glob, Grep, Bash, AskUserQuestion (all available ✅)

---

## Critical Issues to Resolve

### Issue 1: Epic-Story Bidirectional Consistency (27.2% score)
**Problem:** Many stories claim `epic: EPIC-002` but EPIC-002's Stories table doesn't list those stories.
**Example:** STORY-009 claims EPIC-002, but EPIC-002 has 0 stories in its table.

**Impact on Implementation:**
- Feature count may be inaccurate (counts features in Stories table, not claims)
- Gap detection may report features without assigned stories even if stories claim the epic

**Recommendation:**
- Document known inconsistency in command output
- Consider future maintenance story to sync epic tables with story claims
- For now: Use gap-detector.sh outputs as source of truth (it validates both directions)

### Issue 2: Story Status Tracking (Dev Complete threshold)
**Problem:** Business rule BR-002 states "Only stories with status >= 'Dev Complete' count toward coverage"

**Current Stories (EPIC-015):**
- STORY-083-089: Multiple stories with different statuses (QA Approved, In Development, Backlog)

**Implementation Approach:**
- Query story YAML `status:` field
- Compare against status threshold: Backlog < Architecture < Ready < In Dev < Dev Complete
- Test with actual story status values from codebase

---

## Implementation Order (TDD Green Phase)

1. **Tests First** - Write all test cases covering each phase
2. **Phase 0 implementation** - Argument parsing (easiest, foundation)
3. **Phase 0.1 implementation** - Mode detection
4. **Phase 1 implementation** - Service integration (depends on services)
5. **Phase 2 implementation** - Output formatting (depends on parsed data)
6. **Phase 2.1 implementation** - Interactive prompts (depends on STORY-088)
7. **Integration tests** - End-to-end command execution
8. **Refactoring** - Extract helper functions, optimize

---

## Success Criteria (Definition of Done)

### Functional Requirements ✅
- [ ] Command parses arguments (epic ID, flags)
- [ ] Validates epic ID format and existence
- [ ] Detects interactive vs quiet mode
- [ ] Calls gap-detector.sh and generate-report.sh
- [ ] Displays color-coded coverage report
- [ ] Shows actionable gaps (top 10)
- [ ] Interactive prompts work (if STORY-088 approved)
- [ ] Error messages clear and actionable

### Quality Requirements ✅
- [ ] All tests pass (95%+ coverage for business logic)
- [ ] No bash syntax errors (shellcheck clean)
- [ ] Handles edge cases (empty epics, no stories, special chars)
- [ ] Performance: Single epic <500ms, all epics <3s
- [ ] Exit codes: 0 (success), 1 (error)

### Documentation ✅
- [ ] Command spec matches implementation
- [ ] Tests document expected behavior
- [ ] Error messages match spec
- [ ] Integration with STORY-088 documented

---

## Potential Blockers

1. **STORY-088 not approved** → Phase 2.1 implementation blocked
   - Workaround: Implement Phase 0-2, mark Phase 2.1 as deferred

2. **Bidirectional consistency <30%** → May need to fix epic Stories tables first
   - Workaround: Document in output, create future maintenance story

3. **Performance >3s** → May need to optimize Bash loops
   - Solution: Parallelize service calls, cache results

4. **Special characters in feature names** → Shell escaping complexity
   - Solution: Use jq for data extraction, double-quote all substitutions

---

## Files to Modify/Create

### New Files
- `devforgeai/commands/validate-epic-coverage.sh` - Main command implementation (Phase 0-2)
- `devforgeai/tests/STORY-087/test_phase0_*.sh` - Test suite (Phase 1)
- `.claude/plans/STORY-087-validate-epic-coverage.md` - This plan file

### Existing Files to Reference
- `.claude/commands/validate-epic-coverage.md` - Spec (read-only, validate against)
- `devforgeai/epic-coverage/generate-report.sh` - Service (invoke, parse output)
- `devforgeai/traceability/gap-detector.sh` - Service (invoke, parse output)
- `.claude/skills/devforgeai-story-creation/SKILL.md` - Skill reference (for context markers)

---

## Checkpoints & Progress Tracking

| Phase | Checkpoint | Status | Date | Notes |
|-------|-----------|--------|------|-------|
| 1 | Test infrastructure created | Pending | | 10+ test files |
| 2 | Phase 0 implementation + tests pass | Pending | | Arg parsing working |
| 3 | Phase 0.1 implementation + tests pass | Pending | | Mode detection working |
| 4 | Phase 1 implementation + tests pass | Pending | | Services called, outputs parsed |
| 5 | Phase 2 implementation + tests pass | Pending | | Output formatting complete |
| 6 | Phase 2.1 ready (if STORY-088 approved) | Pending | | Interactive prompts wired |
| 7 | Integration tests + end-to-end | Pending | | Full workflow tested |
| 8 | Code review + QA validation | Pending | | Ready for QA Approved |

---

## Questions for User Clarification

1. **STORY-088 Status:** Should Phase 2.1 (interactive prompts) be deferred until STORY-088 is QA Approved, or implemented as skeleton with TODO comments?

2. **Epic Consistency:** Should command warn users about low consistency score (27.2%)? Or silently use gap-detector.sh outputs as source of truth?

3. **Performance vs Accuracy:** If consistency check adds >500ms latency, should it be skipped by default or always run?

---

**Plan Status:** Ready for user approval
**Next Step:** Await user feedback on questions above, then begin TDD implementation
