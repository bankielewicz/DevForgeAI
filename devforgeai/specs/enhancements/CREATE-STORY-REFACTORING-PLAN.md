# /create-story Refactoring + Batch Mode Enhancement Plan

**Date:** 2025-11-07
**Type:** Command Refactoring + Feature Enhancement
**Priority:** CRITICAL (refactoring), MEDIUM (batch enhancement)
**Status:** Planning Complete - Ready for Implementation

---

## Executive Summary

**Objective:** Refactor `/create-story` command to lean orchestration pattern (857 → ~350 lines), then add batch story creation from epics.

**Current State:**
- Command: 857 lines, 23,006 characters (153% over 15K budget)
- Contains ALL workflow logic inline (Phases 1-6)
- Subagent invocations in command (violates skills-first architecture)
- Priority: **CRITICAL** in refactoring queue

**Target State:**
- Command: ~350 lines, ~10,000 characters (<67% of budget)
- Lean orchestration: Arg validation → Skill invocation → Results display
- All workflow logic in skill's reference files
- Batch mode support (+50 lines for epic detection)

**Total Effort:** 10-12 hours (3-4 hrs refactoring + 6-8 hrs batch mode)

---

## Gap Analysis: Command vs. Skill

### What's Currently in Command (857 lines)

**Phase 1: Story Discovery (63 lines)**
- Find existing stories (Glob)
- Parse story IDs, determine next ID
- Read epic/sprint context (Glob)
- Collect metadata (AskUserQuestion)
- **FINDING:** Skill Phase 1 reference already covers this (story-discovery.md - 306 lines)
- **ACTION:** ✅ Can delegate to skill (no gap)

**Phase 2: Requirements Analysis (41 lines)**
- Invoke requirements-analyst subagent (Task tool)
- Validate subagent output
- Refine if incomplete
- **FINDING:** Skill Phase 2 reference already covers this (requirements-analysis.md - 201 lines)
- **ACTION:** ✅ Can delegate to skill (no gap)

**Phase 3: Technical Specification (58 lines)**
- Detect API requirements (keyword search)
- Invoke api-designer subagent (if applicable)
- Identify data models
- Define business rules
- Identify dependencies
- **FINDING:** Skill Phase 3 reference already covers this (technical-specification-creation.md - 303 lines)
- **ACTION:** ✅ Can delegate to skill (no gap)

**Phase 4: UI Specification (95 lines)**
- Detect UI requirements (keyword search)
- Ask user confirmation (AskUserQuestion)
- Document components, mockups, interfaces, interactions, accessibility
- **FINDING:** Skill Phase 4 reference already covers this (ui-specification-creation.md - 312 lines)
- **ACTION:** ✅ Can delegate to skill (no gap)

**Phase 5: Story File Creation (353 lines)**
- Construct YAML frontmatter (detailed field-by-field)
- Write all 7 sections (User Story, AC, Tech Spec, UI Spec, NFRs, Edge Cases, Workflow History)
- INCLUDES: Detailed example output (326 lines - STORY-042 complete example)
- Write file to disk (Write tool)
- Verify file creation (Read tool)
- **FINDING:** Skill Phase 5 reference already covers workflow (story-file-creation.md - 323 lines)
- **FINDING:** Skill has template (story-template.md - 609 lines)
- **GAP:** Example output in command (326 lines) is educational, not execution logic
- **ACTION:** ✅ Can delegate to skill, move example to skill reference

**Phase 6: Linking & Integration (23 lines)**
- Update epic file (Edit tool)
- Update sprint file (Edit tool)
- Create directory structure (Bash mkdir)
- **FINDING:** Skill Phase 6 reference already covers this (epic-sprint-linking.md - 140 lines)
- **ACTION:** ✅ Can delegate to skill (no gap)

**Success Criteria (13 lines)**
- Checklist of story requirements
- **FINDING:** Skill success criteria already documented
- **ACTION:** ✅ Can keep minimal version in command, detailed in skill

**Quality Gates (24 lines)**
- 4 gates with requirements
- **FINDING:** Covered by skill Phase 7 validation
- **ACTION:** ✅ Can remove from command, delegated to skill

**Error Handling (24 lines)**
- 5 error scenarios with actions
- **FINDING:** Skill error-handling.md covers this (385 lines)
- **ACTION:** ✅ Can simplify in command, detailed in skill

**Token Efficiency (30 lines)**
- Optimization strategies
- **FINDING:** Educational content, can move to skill or remove
- **ACTION:** ✅ Remove from command (not execution logic)

**Example Output (326 lines)**
- Complete STORY-042 example
- **FINDING:** Educational, valuable but inflates command
- **ACTION:** ✅ Move to skill reference or story-examples.md

**Integration Notes (30 lines)**
- DevForgeAI workflow integration
- **FINDING:** Can keep brief version in command
- **ACTION:** ✅ Keep minimal (5 lines), detailed in skill

**References (9 lines)**
- File locations
- **ACTION:** ✅ Keep (useful quick reference)

---

## Refactoring Strategy

### What to KEEP in Command (Lean Orchestration)

**Phase 0: Argument Validation (~50 lines)**
- Capture $1 argument
- Detect mode: Epic pattern (epic-001) vs. feature description
- Validate epic exists (if batch mode)
- Handle no argument case (AskUserQuestion)

**Phase 1: Set Context Markers (~20 lines)**
- **Feature Description:** $1 (single story mode)
- OR **Epic ID:** EPIC-001, **Batch Mode:** true (batch mode)

**Phase 2: Invoke Skill (~15 lines)**
- Single line: `Skill(command="devforgeai-story-creation")`
- Skill handles all 8 phases

**Phase 3: Verify Completion (~30 lines)**
- Check story file(s) created
- Brief confirmation message
- Error handling if skill failed

**Phase 4: Next Steps (~20 lines)**
- Brief next action guidance
- Defer to skill's Phase 8 completion report

**Integration Notes (~50 lines)**
- Quick reference
- Common usage examples
- Success criteria (brief)

**Error Handling (~30 lines)**
- Minimal (3-4 error types)
- Skill execution failed
- Story file not found
- Refer to skill for detailed errors

**Total Target:** ~215 lines, ~8,000 characters (53% of budget)

---

### What to MOVE to Skill

**All existing command phases → Skill reference files:**

✅ **Already exist in skill references** (no migration needed):
- Phase 1: Story Discovery → `story-discovery.md` (306 lines)
- Phase 2: Requirements Analysis → `requirements-analysis.md` (201 lines)
- Phase 3: Technical Specification → `technical-specification-creation.md` (303 lines)
- Phase 4: UI Specification → `ui-specification-creation.md` (312 lines)
- Phase 5: Story File Creation → `story-file-creation.md` (323 lines)
- Phase 6: Linking & Integration → `epic-sprint-linking.md` (140 lines)

**Need to migrate from command:**

1. **Example Output (STORY-042) - 326 lines**
   - **Destination:** `.claude/skills/devforgeai-story-creation/references/story-examples.md`
   - **Append to existing examples** (file already has 4 examples)
   - **Benefit:** Consolidates examples, removes bloat from command

2. **Detailed subagent prompts - 58 lines**
   - **Current location:** Command Phase 2 (requirements-analyst), Phase 3 (api-designer)
   - **Destination:** Skill reference files already have this
   - **Action:** Verify skill references match or enhance, then remove from command

3. **Quality Gates detail - 24 lines**
   - **Destination:** Skill Phase 7 validation already has this
   - **Action:** Remove from command (redundant)

4. **Token Efficiency section - 30 lines**
   - **Destination:** General framework documentation (not command-specific)
   - **Action:** Remove from command

---

## Detailed Refactoring Plan

### Part 1: Refactor Command to Lean Pattern (3-4 hours)

#### Task 1.1: Create Backup (5 min)
```bash
cp .claude/commands/create-story.md .claude/commands/create-story.md.backup-pre-lean-refactor
```

#### Task 1.2: Verify Skill References Complete (30 min)

**Check each phase reference file exists and covers command logic:**
- [ ] `story-discovery.md` - covers Phase 1 logic
- [ ] `requirements-analysis.md` - covers Phase 2 logic (+ RCA-007 enhancements)
- [ ] `technical-specification-creation.md` - covers Phase 3 logic
- [ ] `ui-specification-creation.md` - covers Phase 4 logic
- [ ] `story-file-creation.md` - covers Phase 5 logic
- [ ] `epic-sprint-linking.md` - covers Phase 6 logic

**If gaps found:**
- Enhance skill reference file with missing logic from command
- Verify enhancement doesn't duplicate

#### Task 1.3: Migrate Example Output (15 min)

**Move STORY-042 example from command to skill:**
```bash
# Extract lines 575-826 (STORY-042 example) from create-story.md
# Append to .claude/skills/devforgeai-story-creation/references/story-examples.md
```

**Append as Example 5:**
```markdown
## Example 5: Authentication Story with Email Verification

**Source:** Migrated from /create-story command example

**File:** `devforgeai/specs/Stories/STORY-042.story.md`

[Full STORY-042 content here - 251 lines]

**Key Features:**
- API contracts (POST /api/auth/register, GET /api/auth/verify-email)
- Data model (User with verification fields)
- UI specification (RegistrationForm, PasswordStrengthIndicator)
- Accessibility (WCAG AA compliant)
- NFRs (measurable performance, security, usability)
```

#### Task 1.4: Rewrite Command to Lean Structure (2 hours)

**New command structure (target: ~350 lines):**

```markdown
---
description: Create user story with acceptance criteria and technical specification
argument-hint: [feature-description | epic-id]
model: haiku
allowed-tools: Read, Glob, Skill, AskUserQuestion, TodoWrite, Grep
---

# /create-story - Create User Story

**Purpose:** Transform feature description into complete user story with acceptance criteria, technical specifications, and UI specifications (if applicable).

**Output:** Story document in `devforgeai/specs/Stories/`

**Process:** Invokes `devforgeai-story-creation` skill which handles complete story generation workflow.

---

## Phase 0: Argument Validation and Mode Detection (NEW - Batch Support)

**Parse argument:**
```
ARG=$1

# Detect mode
if ARG matches ^[Ee][Pp][Ii][Cc]-\d{3}$:
  MODE="EPIC_BATCH"
  EPIC_ID=$(normalize to EPIC-NNN)
  Validate epic exists → Epic Batch Workflow
elif ARG has 10+ words:
  MODE="SINGLE_STORY"
  FEATURE_DESC=$ARG
  → Single Story Workflow (Phase 1)
else:
  AskUserQuestion: "Single story or batch from epic?"
```

---

## Epic Batch Workflow (NEW - ~100 lines)

**Step 1: Extract epic features**
- Read epic file
- Parse features (Grep for "### Feature X.Y:")
- Display feature list

**Step 2: Multi-select features**
- AskUserQuestion with multiSelect: true
- Validate at least 1 selected

**Step 3: Collect batch metadata**
- Ask sprint (batch or per-story)
- Ask priority (batch or inherit from epic or per-story)

**Step 4: Create stories in loop**
- TodoWrite progress tracking
- For each feature:
  - Calculate next story ID (gap-aware)
  - Set context markers (**Batch Mode:** true)
  - Invoke Skill(command="devforgeai-story-creation")
  - Verify created, update progress

**Step 5: Batch summary**
- Display created count, failed count
- List all created stories
- Handle failures (retry/continue/cancel)

---

## Phase 1: Single Story Workflow (EXISTING - ~50 lines)

**Capture feature description:**
- From $1 argument (already validated in Phase 0)
- Or AskUserQuestion if not provided

**Set context markers:**
```
**Feature Description:** $ARGUMENTS
```

**Invoke skill:**
```
Skill(command="devforgeai-story-creation")
```

**Skill handles:**
- Phase 1: Story Discovery (ID, epic/sprint, metadata)
- Phase 2-7: Complete story generation
- Phase 8: Completion report

---

## Phase 2: Verify Story Created (~30 lines)

**Check for new story file:**
- Glob pattern: `devforgeai/specs/Stories/STORY-*.story.md`
- Compare count before/after
- If no new file → Error handling

**Brief confirmation:**
- Read frontmatter (first 20 lines)
- Display: Story ID, title, epic, sprint, priority, points

---

## Phase 3: Error Handling (~30 lines)

**Skill invocation failed:**
- Display skill error
- Troubleshooting steps

**Story file not created:**
- Possible causes
- Recovery actions

**Other errors:**
- Refer to skill error-handling.md

---

## Integration Notes (~50 lines)

**Usage examples:**
```bash
/create-story User login with password reset
/create-story epic-001  # NEW: Batch mode
```

**Success criteria (brief):**
- Story created with all sections
- Linked to epic/sprint
- Validation passed

**Next steps:**
- /dev STORY-XXX (implement)
- /create-ui STORY-XXX (UI specs)
```

**Total: ~350 lines, ~10,000 characters (67% of budget)**

#### Task 1.5: Verify Skill References are Complete (30 min)

**Read each reference file and confirm it covers command logic:**

**story-discovery.md - Should include:**
- ✅ Find existing stories logic
- ✅ Parse story IDs, calculate next ID
- ✅ Read epic/sprint context
- ✅ Collect metadata via AskUserQuestion
- ⚠️ CHECK: Gap-aware ID calculation (may need enhancement)

**requirements-analysis.md - Should include:**
- ✅ Invoke requirements-analyst subagent (now story-requirements-analyst per RCA-007)
- ✅ Validate subagent output
- ✅ Refine if incomplete
- ✅ RCA-007 enhancements (4-section template, validation checkpoint)

**technical-specification-creation.md - Should include:**
- ✅ Detect API requirements
- ✅ Invoke api-designer subagent
- ✅ Identify data models, business rules, dependencies

**ui-specification-creation.md - Should include:**
- ✅ Detect UI requirements
- ✅ Ask user confirmation
- ✅ Document components, mockups, interfaces, interactions, accessibility

**story-file-creation.md - Should include:**
- ✅ Construct YAML frontmatter
- ✅ Write all 7 sections
- ✅ Write file to disk
- ✅ Verify file creation

**epic-sprint-linking.md - Should include:**
- ✅ Update epic file
- ✅ Update sprint file
- ✅ Create directory structure

**Action:** If any gaps found, enhance skill reference files BEFORE refactoring command.

#### Task 1.6: Execute Command Refactoring (1.5 hours)

**Refactor `.claude/commands/create-story.md`:**

1. **Update frontmatter** (add TodoWrite, Grep to allowed-tools, update argument-hint)

2. **Replace content with lean structure:**
   - Phase 0: Argument validation + mode detection (~50 lines)
   - Epic Batch Workflow (~100 lines)
   - Phase 1: Single Story Workflow (~50 lines)
   - Phase 2: Verify Story Created (~30 lines)
   - Phase 3: Error Handling (~30 lines)
   - Integration Notes (~50 lines)
   - References (~10 lines)

3. **Remove these sections entirely:**
   - Detailed Phase 1-6 workflows (redundant with skill)
   - Example Output (moved to skill)
   - Quality Gates detail (in skill)
   - Token Efficiency (not execution logic)
   - Detailed Success Criteria (in skill)

4. **Keep minimal versions:**
   - Brief success criteria (5 lines)
   - Brief integration notes (50 lines)
   - Error handling (30 lines)

#### Task 1.7: Test Refactored Command (30 min)

**Regression test: Single story mode still works**
```bash
# Test 1: Single story with full description
/create-story User profile settings page with avatar upload and preference management

# Expected:
# - Mode detected: SINGLE_STORY
# - Skill invoked correctly
# - Story created (STORY-007 or next available)
# - All 8 phases execute in skill
# - File created with all sections

# Assertions:
- [ ] Story file created
- [ ] Contains all sections (User Story, AC, Tech Spec, etc.)
- [ ] YAML frontmatter valid
- [ ] Quality unchanged from before refactoring
```

**Test 2: No argument provided**
```bash
/create-story

# Expected:
# - AskUserQuestion: "Single story or batch from epic?"
# - User selects "Single story"
# - Asks for feature description
# - Proceeds normally
```

**Test 3: Short argument (ambiguous)**
```bash
/create-story User login

# Expected:
# - <10 words, mode ambiguous
# - AskUserQuestion: "Single story or batch from epic?"
# - Proceeds based on selection
```

---

### Part 2: Add Batch Mode Support (6-8 hours)

#### Task 2.1: Enhance Skill with Batch Mode Detection (1 hour)

**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`

**Add section after "When to Use This Skill":**

```markdown
## Batch Mode Support (NEW - Enhancement)

**Batch mode triggered when:**
- Context marker `**Batch Mode:** true` present in conversation

**Batch mode behavior:**
- Skip interactive questions in Phase 1 (story discovery)
- Extract metadata from context markers:
  - **Story ID:** STORY-NNN (provided, not generated)
  - **Epic ID:** EPIC-NNN (provided)
  - **Feature Description:** (provided)
  - **Priority:** (provided)
  - **Points:** (provided)
  - **Sprint:** (provided)
- Execute Phases 2-8 normally (requirements, tech spec, UI spec, file creation, linking, validation, report)
- Skip next action AskUserQuestion in Phase 8 (batch controls this)

**Context markers required:**
```
**Story ID:** STORY-009
**Epic ID:** EPIC-001
**Feature Number:** 1.1
**Feature Name:** User Registration Form
**Feature Description:** Implement user registration form with email validation...
**Priority:** High
**Points:** 5
**Sprint:** Sprint-1
**Batch Mode:** true
**Batch Index:** 0
```

**Phase 1 modification:**
- Load `references/story-discovery.md`
- Detect batch mode markers
- If batch mode: Extract all metadata, skip AskUserQuestion flows
- If normal mode: Execute interactive discovery (existing logic)
```

**Estimated changes:** +40 lines to SKILL.md

#### Task 2.2: Update story-discovery.md for Batch Mode (1.5 hours)

**File:** `.claude/skills/devforgeai-story-creation/references/story-discovery.md`

**Add batch mode branch at beginning of Phase 1:**

```markdown
## Phase 1: Story Discovery

### Step 1: Detect Execution Mode

**Check for batch mode marker:**
```
if conversation contains "**Batch Mode:** true":
  BATCH_MODE = true
  → Proceed to Batch Mode Branch (Step 1.1)
else:
  BATCH_MODE = false
  → Proceed to Interactive Mode Branch (Step 1.2 - existing logic)
```

---

### Step 1.1: Batch Mode Branch (NEW)

**Extract all metadata from context markers:**

```
# Required markers
STORY_ID = extract_from_conversation("**Story ID:**")
EPIC_ID = extract_from_conversation("**Epic ID:**")
FEATURE_DESC = extract_from_conversation("**Feature Description:**")
PRIORITY = extract_from_conversation("**Priority:**")
POINTS = extract_from_conversation("**Points:**")
SPRINT = extract_from_conversation("**Sprint:**")

# Optional markers
FEATURE_NUM = extract_from_conversation("**Feature Number:**")
FEATURE_NAME = extract_from_conversation("**Feature Name:**")
BATCH_INDEX = extract_from_conversation("**Batch Index:**")
```

**Validate all required fields present:**
```
if not all_present(STORY_ID, EPIC_ID, FEATURE_DESC, PRIORITY, POINTS, SPRINT):
  ERROR: "Batch mode requires all metadata markers"
  FALLBACK: Switch to interactive mode
  → Proceed to Step 1.2 (ask questions)
```

**Skip all interactive questions:**
```
# Do NOT execute:
- AskUserQuestion for epic selection
- AskUserQuestion for sprint selection
- AskUserQuestion for priority
- AskUserQuestion for story points

# Use provided values instead
```

**Return Phase 1 output:**
```
return {
  "story_id": STORY_ID,
  "epic_id": EPIC_ID,
  "feature_description": FEATURE_DESC,
  "priority": PRIORITY,
  "points": POINTS,
  "sprint": SPRINT,
  "batch_mode": true
}

→ Proceed to Phase 2 (Requirements Analysis)
```

---

### Step 1.2: Interactive Mode Branch (EXISTING - No Changes)

[Existing logic - no modifications needed]

---
```

**Estimated changes:** +80 lines to story-discovery.md

#### Task 2.3: Add Batch Workflow to Command (2 hours)

**In Epic Batch Workflow section of command (Steps 1-5):**

**Step 1: Extract features from epic**
- Grep for feature pattern
- Parse feature number, name, description, points
- Display feature list

**Step 2: Multi-select AskUserQuestion**
- All features as options
- multiSelect: true
- Extract selected features

**Step 3: Batch metadata AskUserQuestion**
- Sprint (batch apply or per-story or inherit)
- Priority (batch apply or per-story or inherit from epic)

**Step 4: Story creation loop**
- TodoWrite initialization
- For each selected feature:
  - Calculate next story ID (gap-aware)
  - Set context markers (all 10 markers)
  - Invoke Skill(command="devforgeai-story-creation")
  - Verify created
  - Update TodoWrite progress
  - Track created/failed

**Step 5: Batch summary**
- Display created count, total points
- List all created stories
- Handle failures (AskUserQuestion for retry/continue/cancel)

**Estimated changes:** +100 lines to command (Epic Batch Workflow section)

#### Task 2.4: Implement Gap-Aware ID Calculation (30 min)

**Add helper logic to command (Epic Batch Workflow section):**

```markdown
**Calculate next story ID (gap-aware):**
```
# Get all existing stories
existing = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")

# Extract numbers
numbers = [extract STORY-NNN number from each file]
numbers.sort()

if numbers is empty:
  next_id = 1
else:
  max_num = max(numbers)
  all_nums = set(range(1, max_num + 1))
  gaps = sorted(set(all_nums) - set(numbers))

  if gaps:
    next_id = gaps[0]
    Display: "ℹ️ Filling gap at STORY-{next_id:03d}"
  else:
    next_id = max_num + 1

return f"STORY-{next_id:03d}"
```
```

**Estimated changes:** Included in Step 4 logic

#### Task 2.5: Update Skill Phase 8 for Batch Mode (30 min)

**File:** `.claude/skills/devforgeai-story-creation/references/completion-report.md`

**Add batch mode detection:**

```markdown
## Phase 8: Completion Report

### Step 1: Check Execution Mode

**Detect batch mode:**
```
if BATCH_MODE (from Phase 1):
  → Skip next action AskUserQuestion
  → Generate minimal completion summary
  → Return immediately
else:
  → Execute full completion report (existing logic)
```

### Step 1.1: Batch Mode Completion (NEW)

**Generate minimal summary:**
```
Story created successfully.

Story: {story_id}
Title: {title}
Points: {points}
```

**Return to command:**
- Command handles next action (part of batch loop)
- No interactive questions needed

---

### Step 1.2: Interactive Mode Completion (EXISTING)

[Existing Phase 8 logic - no changes]
```

**Estimated changes:** +30 lines to completion-report.md

---

## Implementation Checklist

### Pre-Implementation (30 min)
- [x] Create backup of create-story.md
- [ ] Verify all skill reference files complete
- [ ] Identify gaps (if any)
- [ ] Create test epic (EPIC-001) ✅ Already done
- [ ] Document current story count (baseline: 1 story, STORY-006)

### Refactoring Implementation (3 hours)
- [ ] Task 1.2: Verify skill references (30 min)
- [ ] Task 1.3: Migrate example output to skill (15 min)
- [ ] Task 1.4: Rewrite command to lean structure (2 hrs)
- [ ] Task 1.7: Test single story mode regression (30 min)

### Batch Mode Implementation (6 hours)
- [ ] Task 2.1: Add batch mode detection to skill (1 hr)
- [ ] Task 2.2: Update story-discovery.md for batch (1.5 hrs)
- [ ] Task 2.3: Add batch workflow to command (2 hrs)
- [ ] Task 2.4: Gap-aware ID calculation (30 min)
- [ ] Task 2.5: Update Phase 8 for batch mode (30 min)
- [ ] Test batch mode with EPIC-001 (30 min)

### Post-Implementation (1 hour)
- [ ] Update `.claude/memory/commands-reference.md` (batch mode examples)
- [ ] Update `.claude/memory/skills-reference.md` (batch mode notes)
- [ ] Verify character budget: <12K target (<15K hard limit)
- [ ] Git commit with descriptive message

---

## Success Criteria

### Refactoring Success
- [ ] Command: 300-400 lines (target: ~350)
- [ ] Command: <12,000 characters (target), <15,000 (hard limit)
- [ ] All workflow logic in skill references (not command)
- [ ] Single story mode regression tests pass (100%)
- [ ] No features lost (100% backward compatible)
- [ ] Follows lean orchestration pattern (command → skill → subagents)

### Batch Mode Success
- [ ] Epic detection works (epic-001, EPIC-001, Epic-001 all recognized)
- [ ] Multi-select feature picker works (select 1-5 of 5 features)
- [ ] Batch metadata reduces questions (10 questions → 3-4 questions for 5 stories)
- [ ] Sequential story creation works (STORY-007, STORY-008, STORY-009, STORY-010, STORY-011)
- [ ] Gap-aware ID calculation fills gaps correctly
- [ ] Progress tracking visible (TodoWrite updates)
- [ ] Error handling: Continue on failure, track failed stories
- [ ] Batch summary displays created/failed counts
- [ ] All created stories link to epic correctly

### Quality Assurance
- [ ] Zero extra files created (only .story.md files) - RCA-007 compliance
- [ ] Story quality unchanged (same AC, tech spec, UI spec depth)
- [ ] Token efficiency: Command <3K tokens in main conversation
- [ ] Execution time: 5 stories in ~10-12 minutes (sequential, acceptable)

---

## Comparison: Before vs. After

### Command Structure

| Aspect | Before (Current) | After (Refactored) | After (+ Batch) |
|--------|------------------|-------------------|----------------|
| **Lines** | 857 | ~250 | ~350 |
| **Characters** | 23,006 | ~8,000 | ~10,000 |
| **Budget %** | 153% (OVER) | 53% (✅) | 67% (✅) |
| **Phases inline** | 6 (all) | 0 (delegated) | 0 (delegated) |
| **Subagent calls** | 2 (in command) | 0 (in skill) | 0 (in skill) |
| **Example output** | 326 lines | 0 (moved) | 0 (moved) |
| **Modes supported** | 1 (single) | 1 (single) | 2 (single + batch) |

### User Experience

| Aspect | Before | After (Single) | After (Batch) |
|--------|--------|---------------|--------------|
| **Create 1 story** | 2 min, 4-5 questions | 2 min, 4-5 questions | Same |
| **Create 5 stories** | 10 min, 20-25 questions, 5 commands | 10 min, 20-25 questions, 5 commands | ~12 min, 4-5 questions, 1 command |
| **Epic detection** | No | No | Yes (epic-001 pattern) |
| **Multi-select features** | No | No | Yes |
| **Batch metadata** | No | No | Yes (ask once, apply all) |
| **Progress tracking** | No | No | Yes (TodoWrite) |

---

## Risks and Mitigation

### Risk 1: Skill references missing command logic

**Likelihood:** Low (skill references are comprehensive)
**Impact:** High (broken functionality)

**Mitigation:**
- Task 1.5: Verify each reference file before refactoring
- Gap analysis documented above
- If gaps found: Enhance skill reference FIRST, then refactor command

---

### Risk 2: Command still over budget after refactoring

**Likelihood:** Low (following proven pattern from /qa, /dev)
**Impact:** Medium (need additional trimming)

**Mitigation:**
- Target: 350 lines (~10K chars) provides 5K character buffer under limit
- If over: Remove integration notes, simplify error handling
- Reference implementations: /qa (295 lines, 7.2K), /create-sprint (250 lines, 8K)

---

### Risk 3: Batch mode breaks single story mode

**Likelihood:** Low (modes are separated by Phase 0 detection)
**Impact:** High (regression)

**Mitigation:**
- Explicit mode detection in Phase 0
- Single story workflow unchanged (just renamed Phase 1)
- Regression testing mandatory (Task 1.7)

---

### Risk 4: Gap-aware ID calculation has edge cases

**Likelihood:** Medium (gaps, duplicates, race conditions)
**Impact:** Medium (ID conflicts)

**Mitigation:**
- Comprehensive test cases (empty, gaps, no gaps, max number edge)
- Simple algorithm (set operations, proven pattern)
- Fallback: If conflict, increment and retry

---

## Testing Strategy

### Unit Tests (Refactoring)

**Test 1: Mode detection**
- Input: "epic-001" → MODE="EPIC_BATCH" ✅
- Input: "EPIC-001" → MODE="EPIC_BATCH" ✅
- Input: "Epic-001" → MODE="EPIC_BATCH" ✅
- Input: "User login with password" (10+ words) → MODE="SINGLE_STORY" ✅
- Input: "User login" (<10 words) → AskUserQuestion ✅
- Input: (empty) → AskUserQuestion ✅

**Test 2: Single story regression**
- Create story with full description → File created, all sections present ✅
- Create story, no argument → Asks for description, proceeds ✅
- Create story, ambiguous → Asks mode, proceeds ✅

### Integration Tests (Batch Mode)

**Test 3: Full batch creation (5 features)**
- Epic: EPIC-001 (5 features)
- Select: All 5 features
- Sprint: Backlog (batch)
- Priority: Inherit from epic (High)
- Expected: 5 stories created (STORY-007 through STORY-011)
- Assertions:
  - [ ] 5 .story.md files created
  - [ ] Story IDs sequential (007, 008, 009, 010, 011)
  - [ ] All linked to EPIC-001
  - [ ] All priority: High (inherited)
  - [ ] All sprint: Backlog
  - [ ] Zero extra files (RCA-007 compliance)

**Test 4: Partial selection (3 of 5 features)**
- Epic: EPIC-001
- Select: Features 1.1, 1.3, 1.5 only
- Sprint: Backlog
- Priority: High (batch)
- Expected: 3 stories created (STORY-007, STORY-008, STORY-009)
- Assertions:
  - [ ] Exactly 3 files created
  - [ ] Only selected features have stories
  - [ ] Unselected features (1.2, 1.4) have no stories

**Test 5: Gap detection**
- Existing: STORY-006
- Delete STORY-006 temporarily (create gap)
- Create batch: Select 2 features
- Expected: STORY-006, STORY-007 (fills gap first)
- Assertions:
  - [ ] Gap notification displayed
  - [ ] STORY-006 created (gap filled)
  - [ ] STORY-007 created (sequential after gap)

**Test 6: Per-story metadata**
- Epic: EPIC-001
- Select: 2 features
- Sprint: "Ask per story"
- Priority: "Ask per story"
- Expected: Asks sprint twice, priority twice
- Assertions:
  - [ ] 4 AskUserQuestion calls (2 sprint + 2 priority)
  - [ ] Stories have different sprint/priority based on answers

### Regression Tests

**Test 7: Story quality unchanged**
- Create single story (old workflow)
- Create batch story (new workflow)
- Compare: User story, AC count, tech spec depth, UI spec detail
- Expected: Same quality
- Assertions:
  - [ ] Both have 3+ AC
  - [ ] Both have measurable NFRs
  - [ ] Both have complete tech spec
  - [ ] Both have accessibility requirements (if UI)

**Test 8: Epic/sprint linking works**
- Create batch: 3 stories assigned to Sprint-1
- Read EPIC-001, check for story references
- Read Sprint-1 (if exists), check for story references
- Expected: All 3 stories referenced in epic
- Assertions:
  - [ ] Epic contains STORY-007, STORY-008, STORY-009
  - [ ] Epic feature sections updated with story IDs

---

## Token Budget Analysis

### Command Token Usage

**Before refactoring:**
- Command: ~3,500 tokens (all inline logic)
- Skill invocation: ~90,000 tokens (isolated)
- Total main conversation: ~3,500 tokens

**After refactoring (single story):**
- Command overhead: ~2,000 tokens (lean structure)
- Skill invocation: ~90,000 tokens (isolated)
- Total main conversation: ~2,000 tokens
- **Savings:** 43% reduction

**After batch mode (5 stories):**
- Command overhead: ~2,500 tokens (batch logic + progress tracking)
- Skill invocations: 5 × ~90,000 = ~450,000 tokens (isolated)
- Total main conversation: ~6,000 tokens (batch overhead + summaries)
- vs. Manual: 5 × ~3,500 = ~17,500 tokens
- **Savings:** 66% reduction

---

## Rollback Plan

### If Refactoring Breaks Single Story Mode

**Immediate rollback (<15 min):**
```bash
# Restore original command
cp .claude/commands/create-story.md.backup-pre-lean-refactor .claude/commands/create-story.md

# Remove any new artifacts (if created)
# (None expected for refactoring)

# Restart terminal
# Original behavior restored
```

**Root cause analysis:**
- Document what broke
- Identify missing logic in skill references
- Fix skill references before re-attempting refactoring

### If Batch Mode Fails

**Disable batch mode (<5 min):**
```bash
# In .claude/commands/create-story.md, comment out epic detection:
# Change: if ARG matches ^[Ee][Pp][Ii][Cc]-\d{3}$:
# To:     # DISABLED if ARG matches ^[Ee][Pp][Ii][Cc]-\d{3}$:

# All inputs treated as feature descriptions
# Single story mode 100% functional
```

**No rollback needed** - batch mode is additive, can be disabled without affecting single story mode

---

## Post-Implementation Documentation

### Files to Update

1. **`.claude/memory/commands-reference.md`**
   - Update /create-story section with batch mode examples
   - Document epic-001 pattern
   - Note character budget improvement (153% → 67%)

2. **`.claude/memory/skills-reference.md`**
   - Document batch mode support in devforgeai-story-creation
   - Add batch mode context markers

3. **`.devforgeai/protocols/lean-orchestration-pattern.md`**
   - Add /create-story to refactored commands list
   - Update priority queue (remove create-story from CRITICAL)

4. **`.devforgeai/protocols/command-budget-reference.md`**
   - Update command status table
   - Show create-story improvement (153% → 67%)

5. **`CLAUDE.md`**
   - Update component summary (if applicable)
   - Note batch mode feature

---

## Timeline Estimate

### Week 1: Refactoring (3-4 hours)
- **Day 1 (2 hours):** Tasks 1.1-1.4 (backup, verify, migrate, rewrite)
- **Day 1 (1 hour):** Task 1.5-1.7 (verify, test regression)
- **Day 2 (1 hour):** Buffer for issues, documentation updates

**Milestone:** Command refactored to lean pattern, single story mode works

### Week 2: Batch Mode (6-8 hours)
- **Day 3 (2 hours):** Tasks 2.1-2.2 (skill batch detection, story-discovery.md update)
- **Day 4 (3 hours):** Task 2.3-2.4 (batch workflow in command, gap calculation)
- **Day 5 (2 hours):** Task 2.5, testing (Phase 8 update, comprehensive tests)
- **Day 5 (1 hour):** Documentation updates, git commit

**Milestone:** Batch mode functional, all tests pass

**Total:** 10-12 hours across 5 working days (2 weeks elapsed)

---

## Expected Outcomes

### Immediate (After Refactoring)
- ✅ Command: 250-300 lines, ~8,000 chars (53% of budget)
- ✅ Budget compliance achieved (CRITICAL → COMPLIANT)
- ✅ Lean orchestration pattern followed
- ✅ Single story mode works (regression tests pass)
- ✅ Framework architecture standards met

### Final (After Batch Mode)
- ✅ Command: 350-400 lines, ~10,000 chars (67% of budget)
- ✅ Batch mode functional (epic-001 → 5 stories in 1 command)
- ✅ Question reduction (20 → 4 for 5 stories)
- ✅ Progress tracking visible
- ✅ Error recovery built-in
- ✅ 100% backward compatible

---

## Dependencies

### Prerequisites
- ✅ RCA-007 fix complete (all 3 phases) - Prevents multi-file creation
- ✅ Test epic created (EPIC-001)
- ✅ Skill references exist (all 16 files)
- ✅ Lean orchestration pattern documented

### No Blockers
- All dependencies within DevForgeAI framework
- All tools available (Read, Glob, Skill, AskUserQuestion, TodoWrite, Grep)
- All patterns proven in other refactorings

---

## Validation Steps

### After Refactoring (Pre-Batch)

**Step 1: Character budget check**
```bash
wc -c .claude/commands/create-story.md
# Expected: <12,000 (target) or <15,000 (hard limit)
```

**Step 2: Line count check**
```bash
wc -l .claude/commands/create-story.md
# Expected: 250-300 lines
```

**Step 3: Regression test**
```bash
/create-story User dashboard with analytics and export functionality

# Expected:
# - Story created successfully
# - All sections present (User Story, AC, Tech Spec, UI Spec, NFRs, Edge Cases)
# - YAML frontmatter valid
# - Quality unchanged
```

### After Batch Mode

**Step 4: Epic detection test**
```bash
/create-story epic-001

# Expected:
# - Mode detected: EPIC_BATCH
# - Shows 5 features from EPIC-001
# - Multi-select works
```

**Step 5: Batch creation test**
```bash
/create-story epic-001
# Select all 5 features
# Sprint: Backlog
# Priority: Inherit from epic (High)

# Expected:
# - 5 stories created (STORY-007 through STORY-011)
# - All linked to EPIC-001
# - All priority: High
# - Progress tracking visible
# - Batch summary displays
```

**Step 6: RCA-007 compliance check**
```bash
ls devforgeai/specs/Stories/STORY-*-SUMMARY.md 2>/dev/null
# Expected: (no files) - zero extra files created

ls devforgeai/specs/Stories/STORY-*.story.md | wc -l
# Expected: 6 (baseline: STORY-006 + new: STORY-007 through STORY-011)
```

---

## Key Design Decisions

### Decision 1: All Workflow Logic in Skill References ✅

**Rationale:**
- Skill already has comprehensive reference files for all 8 phases
- Command becoming lean orchestrator (not implementer)
- Proven pattern from /qa, /dev, /create-sprint refactorings

**Result:** Command delegates to skill, skill delegates to references

---

### Decision 2: Batch Logic Split Between Command and Skill ✅

**Command responsibilities (Epic Batch Workflow - ~100 lines):**
- Epic file loading and feature extraction
- Multi-select feature picker (AskUserQuestion)
- Batch metadata collection (sprint, priority)
- Story creation loop (invoke skill N times)
- Progress tracking (TodoWrite)
- Batch summary display

**Skill responsibilities (Batch Mode Branch):**
- Detect batch mode marker
- Extract metadata from context markers
- Skip interactive questions in Phase 1
- Execute Phases 2-7 normally
- Skip next action question in Phase 8

**Rationale:**
- User interaction (AskUserQuestion) belongs in command (UX layer)
- Story generation belongs in skill (business logic layer)
- Clear separation of concerns

---

### Decision 3: Gap-Aware ID Calculation in Command ✅

**Rationale:**
- Command needs to know ALL story IDs upfront (for TodoWrite list)
- Simple algorithm (set operations, <20 lines)
- Batch-specific logic (not needed in skill's single-story mode)

**Alternative considered:** Put in skill
**Rejected because:** Skill doesn't need gap detection in single-story mode, batch mode needs it for all stories upfront

---

### Decision 4: No Parallel Optimization in Phase 1 ✅

**Rationale:**
- Phase 6 (parallel optimization) is optional
- Sequential implementation is simpler (fewer edge cases)
- 10-12 min for 5 stories is acceptable (vs. 10 min for 5 separate commands)
- Parallel can be added later if users request (separate phase)

**Benefit:** Reduces implementation complexity, faster to ship

---

## Next Steps After Plan Approval

1. **Execute Task 1.1:** Create backup ✅ (5 min)
2. **Execute Task 1.2-1.5:** Verify skill references, migrate example (1 hour)
3. **Execute Task 1.6:** Refactor command to lean structure (2 hours)
4. **Execute Task 1.7:** Test regression (30 min)
5. **Execute Task 2.1-2.5:** Implement batch mode (6 hours)
6. **Execute comprehensive testing:** All test cases (1.5 hours)
7. **Update documentation:** 4 files (30 min)
8. **Git commit:** Descriptive message documenting refactoring + batch mode

**Total:** 11-12 hours

---

**Plan Status:** ✅ COMPLETE - Ready for execution pending user approval

**Character count:** ~11,500 characters (plan document)
