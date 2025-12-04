# /create-sprint Command Refactoring Plan

**Version:** 1.0
**Date:** 2025-11-05
**Status:** Ready for Implementation
**Priority:** 🟡 MEDIUM (84% of budget, approaching limit)

---

## Executive Summary

The `/create-sprint` command violates the lean orchestration pattern established in DevForgeAI by implementing all sprint planning logic directly in the command file. This refactoring extracts business logic to the `devforgeai-orchestration` skill and creates a specialized `sprint-planner` subagent for isolated context execution.

**Key Metrics:**
- **Current:** 497 lines, 12,525 chars (84% of 15K budget)
- **Target:** ~250 lines, ~8,000 chars (53% of budget)
- **Reduction:** 50% line reduction, 36% character reduction
- **Token Efficiency:** 44% improvement (native tools + context isolation)

---

## Current State Analysis

### File Statistics

```bash
# Current command file
File: .claude/commands/create-sprint.md
Lines: 497
Characters: 12,525
Budget Status: ⚠️ HIGH (84% of 15K limit)
```

### Current Architecture (Top-Heavy)

```
/create-sprint command (497 lines)
├─ Phase 1: Sprint Discovery (25 lines)
│   ├─ Glob existing sprints
│   ├─ Calculate next sprint number
│   └─ Load epic context
│
├─ Phase 2: Story Discovery & Selection (82 lines)
│   ├─ Find Backlog stories via Glob
│   ├─ Read story metadata
│   ├─ Present selection via AskUserQuestion
│   └─ Validate capacity
│
├─ Phase 3: Sprint Metadata Collection (32 lines)
│   ├─ Sprint name (AskUserQuestion)
│   ├─ Start date (AskUserQuestion)
│   ├─ Duration (AskUserQuestion)
│   ├─ Calculate end date
│   └─ Epic linkage (AskUserQuestion)
│
├─ Phase 4: Sprint File Creation (73 lines)
│   ├─ Generate YAML frontmatter
│   ├─ Generate markdown sections
│   └─ Write to .ai_docs/Sprints/
│
├─ Phase 5: Update Story Status (33 lines)
│   ├─ Edit each story file
│   ├─ Update status: Backlog → Ready for Dev
│   ├─ Add sprint reference
│   └─ Workflow history entries
│
├─ Phase 6: Success Report (28 lines)
│   └─ Display summary
│
└─ Error Handling (97 lines)
    ├─ No stories in Backlog (22 lines)
    ├─ Invalid story selection (19 lines)
    ├─ Sprint file creation failed (18 lines)
    └─ Story update failed (24 lines)
```

**Total business logic in command:** ~273 lines (55% of file)

### Issues Identified

1. **Business Logic in Command** (273 lines)
   - Sprint discovery algorithm
   - Story selection and validation
   - Capacity calculation
   - Sprint file generation
   - Story status updates

2. **No Skill Invocation**
   - Command doesn't invoke `devforgeai-orchestration` skill
   - Skill has entry point: `--plan-sprint` but unused
   - Complete reimplementation of logic

3. **Token Inefficiency**
   - All logic runs in main conversation (~12K tokens)
   - Should be in isolated skill/subagent context
   - No progressive disclosure

4. **Mixed Concerns**
   - User interaction (AskUserQuestion)
   - File operations (Glob, Read, Write, Edit)
   - Business logic (validation, calculation)
   - Display formatting

5. **Documentation Overhead** (97 lines)
   - Extensive error handling scenarios
   - Success criteria
   - Integration notes
   - Token efficiency targets

---

## Target Architecture (Lean Orchestration)

### Command Responsibilities (250 lines)

```
/create-sprint command (250 lines, 53% budget)
├─ Phase 0: Argument Validation (20 lines)
│   └─ Parse sprint name from $1
│
├─ Phase 1: User Interaction (80 lines)
│   ├─ Epic selection (AskUserQuestion)
│   ├─ Story selection (AskUserQuestion via orchestration skill)
│   ├─ Sprint metadata (AskUserQuestion)
│   └─ Confirmation
│
├─ Phase 2: Invoke Skill (15 lines)
│   ├─ Set context markers
│   └─ Skill(command="devforgeai-orchestration")
│
├─ Phase 3: Display Results (10 lines)
│   └─ Output skill result
│
└─ Integration Notes (125 lines)
    ├─ Usage examples
    ├─ Success criteria
    └─ Integration patterns
```

### Skill Responsibilities (devforgeai-orchestration)

**Add Phase 3: Sprint Planning Workflow**

```markdown
## Phase 3: Sprint Planning Workflow

When conversation contains "Operation: plan-sprint":

### Step 1: Validate Inputs
- Extract sprint name, epic, selected stories, duration from conversation
- Validate story IDs exist and status = Backlog

### Step 2: Invoke sprint-planner Subagent
Task(
  subagent_type="sprint-planner",
  description="Create Sprint-N with selected stories",
  prompt="Create sprint with:
    - Sprint name: {sprint_name}
    - Selected stories: {story_ids}
    - Duration: {duration_days} days
    - Epic: {epic_id}

    Execute complete sprint planning workflow and return summary."
)

### Step 3: Return Result
- Present subagent summary
- Provide next steps
```

### Subagent Responsibilities (sprint-planner)

**NEW: `.claude/agents/sprint-planner.md`** (467 lines)

```
Sprint Planner Subagent (isolated context)
├─ Phase 1: Sprint Discovery
│   ├─ Glob existing sprints
│   ├─ Parse sprint numbers
│   └─ Calculate next number
│
├─ Phase 2: Story Validation
│   ├─ Read story files
│   └─ Verify Backlog status
│
├─ Phase 3: Metrics Calculation
│   ├─ Sum story points
│   ├─ Calculate end date
│   └─ Validate capacity
│
├─ Phase 4: Document Generation
│   ├─ Generate YAML frontmatter
│   └─ Generate markdown sections
│
├─ Phase 5: Story Updates
│   ├─ Edit story status
│   ├─ Add sprint references
│   └─ Workflow history entries
│
└─ Phase 6: Summary Report
    └─ Return structured JSON
```

**Reference File:** `.claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md` (391 lines)

---

## Extraction Strategy

### Move to Skill (devforgeai-orchestration)

**Add Phase 3: Sprint Planning Workflow**
- Entry point detection: "Operation: plan-sprint"
- User interaction coordination (story selection)
- Subagent invocation
- Result presentation

**Lines added to skill:** ~150 lines (acceptable - skill is comprehensive)

### Move to Subagent (NEW: sprint-planner)

**Extract from command:**
- Phase 1: Sprint Discovery (25 lines) → Subagent Phase 1
- Phase 4: Sprint File Creation (73 lines) → Subagent Phase 4
- Phase 5: Update Story Status (33 lines) → Subagent Phase 5
- Capacity calculation logic (embedded in Phase 2) → Subagent Phase 3
- **Total extracted:** ~131 lines of business logic

**Create new subagent:** 467 lines (framework-aware, comprehensive)

### Move to Reference File (NEW: sprint-planning-guide.md)

**Extract from command:**
- Sprint capacity guidelines (20-40 points)
- Story selection criteria
- Status transition rules
- Sprint file structure specification
- Workflow history format

**Create reference file:** 391 lines

### Keep in Command

**User Interaction (80 lines):**
- Epic selection (AskUserQuestion)
- Story selection coordination
- Sprint metadata collection
- Confirmation dialogs

**Orchestration (35 lines):**
- Argument validation (20 lines)
- Skill invocation (15 lines)

**Documentation (125 lines):**
- Usage examples
- Success criteria
- Integration patterns

**Total kept:** 240 lines

### Delete/Consolidate

**Error Handling (97 lines):**
- Reduce to minimal (25 lines)
- Skill/subagent communicate errors
- Command displays them simply

**Token Efficiency Section (15 lines):**
- Move to integration notes

**Duplicate Guidance (20 lines):**
- Consolidate with integration patterns

**Total removed:** ~97 lines

---

## Implementation Steps

### Step 1: Create New Artifacts ✅ COMPLETE

**Files created by agent-generator:**
1. ✅ `.claude/agents/sprint-planner.md` (467 lines)
2. ✅ `.claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md` (391 lines)
3. ✅ Supporting documentation (7 files)

### Step 2: Update devforgeai-orchestration Skill

**File:** `.claude/skills/devforgeai-orchestration/SKILL.md`

**Add Phase 3: Sprint Planning Workflow**

Location: After Phase 2 (Story Creation), before Phase 4 (Story Lifecycle Management)

```markdown
---

## Phase 3: Sprint Planning Workflow

### When to Execute

**Triggered when conversation contains:**
- "Operation: plan-sprint"
- "Sprint Name: {name}"
- "Selected Stories: {ids}"
- "Duration: {days} days"
- "Epic: {epic_id}"

**Prerequisites:**
- At least 1 story in Backlog status
- Valid epic (optional but recommended)
- Sprint name provided
- Duration specified (default: 14 days)

### Step 1: Validate User Context

Extract from conversation:
```
SPRINT_NAME = pattern match "Sprint Name: (.*)"
SELECTED_STORIES = pattern match "Selected Stories: (.*)"
DURATION_DAYS = pattern match "Duration: (\d+)"
EPIC_ID = pattern match "Epic: (.*)"
```

Validate:
- SELECTED_STORIES is comma-separated list of STORY-\d+ IDs
- DURATION_DAYS is 7, 14, or 21 (or custom)
- EPIC_ID matches existing epic (if provided)

### Step 2: Invoke sprint-planner Subagent

```
Task(
  subagent_type="sprint-planner",
  description="Create sprint with selected stories",
  prompt="Execute complete sprint planning workflow:

**Sprint Details:**
- Sprint Name: ${SPRINT_NAME}
- Selected Stories: ${SELECTED_STORIES}
- Duration: ${DURATION_DAYS} days
- Epic: ${EPIC_ID}

**Workflow:**
1. Discover next sprint number (Glob existing sprints)
2. Validate selected stories (Read files, check Backlog status)
3. Calculate capacity and dates (sum points, compute end date)
4. Generate sprint document (YAML + markdown)
5. Update story statuses (Backlog → Ready for Dev)
6. Return structured summary

**Reference Framework Constraints:**
Read(file_path=\".claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md\")

Execute and return JSON summary."
)
```

### Step 3: Process Subagent Result

**Expected result format:**
```json
{
  "sprint_id": "SPRINT-N",
  "file_path": ".ai_docs/Sprints/Sprint-N.md",
  "stories_updated": ["STORY-001", "STORY-002", ...],
  "total_points": 28,
  "capacity_status": "OPTIMAL",
  "start_date": "2025-11-05",
  "end_date": "2025-11-19",
  "next_steps": ["Review sprint goals", "Begin /dev STORY-001", ...]
}
```

### Step 4: Return Summary to Command

Present result:
```
✅ Sprint Created Successfully

Sprint Details:
  📋 ${sprint_id}: ${sprint_name}
  📅 ${start_date} to ${end_date} (${duration_days} days)
  🎯 Epic: ${epic_name}
  📊 Capacity: ${total_points} points (${capacity_status})
  📝 Stories: ${stories_updated.length} selected

Stories Added:
  ${stories_updated with titles and points}

Next Steps:
  ${next_steps from subagent}
```

### Error Handling

**Error: No stories in Backlog**
```
Subagent returns:
{
  "error": "NO_BACKLOG_STORIES",
  "available_statuses": {...breakdown...}
}

Command displays:
"⚠️ No stories available in Backlog.
 Create stories first: /create-story"
```

**Error: Invalid story selection**
```
Subagent returns:
{
  "error": "INVALID_STORIES",
  "invalid_ids": ["STORY-099"],
  "wrong_status": ["STORY-005: In Development"]
}

Command displays error details and valid options
```

---

## Success Criteria

- [ ] Phase 3 added to orchestration skill (150 lines)
- [ ] sprint-planner subagent invoked correctly
- [ ] Reference file loaded by subagent
- [ ] JSON result parsed and presented
- [ ] Error handling covers 4 scenarios
```

**Estimated addition to skill:** ~150 lines

**Why acceptable:** Skill is meant to be comprehensive coordinator. 150 lines for sprint planning workflow is appropriate.

### Step 3: Refactor /create-sprint Command

**File:** `.claude/commands/create-sprint.md`

**Create backup:**
```bash
cp .claude/commands/create-sprint.md .claude/commands/create-sprint.md.backup
```

**New command structure:**

```markdown
---
description: Create sprint plan with story selection
argument-hint: [sprint-name]
model: haiku
allowed-tools: Read, Glob, AskUserQuestion, Skill
---

# Create Sprint Command

Creates a new 2-week sprint with story selection and automatic status updates.

---

## Quick Reference

```bash
# Create sprint with name
/create-sprint "User Authentication Sprint"

# Create sprint (will prompt for name)
/create-sprint
```

---

## Command Workflow

### Phase 0: Argument Validation and Epic Selection

**Parse sprint name:**
```
SPRINT_NAME = $1 or ask user
```

**Select epic (AskUserQuestion):**
```
Question: "Link sprint to epic?"
Options:
  - [List of existing epics]
  - Multiple epics
  - No epic (standalone)
```

**Validate epic exists:**
```
IF epic selected:
  Glob(.ai_docs/Epics/${EPIC_ID}.epic.md)
  IF not found: Error + list available
```

---

### Phase 1: Story Selection

**Find available stories:**
```
Glob(pattern=".ai_docs/Stories/*.story.md")

FOR each story:
  Read YAML frontmatter
  IF status == "Backlog":
    Add to available list
```

**Present selection (AskUserQuestion):**
```
Question: "Select stories for sprint:"
Stories grouped by epic and priority:
  Epic: User Management
    🔴 HIGH   - STORY-001: User login (5 pts)
    🔴 HIGH   - STORY-002: Password reset (8 pts)
    🟡 MEDIUM - STORY-003: Profile page (3 pts)

Options:
  - Specific IDs: STORY-001, STORY-002
  - By priority: All HIGH
  - By epic: User Management
  - Custom selection
```

**Validate capacity:**
```
SUM story points
IF total > 40:
  AskUserQuestion: "Over capacity (${total} pts). Proceed?"
IF total < 20:
  AskUserQuestion: "Under capacity (${total} pts). Add more?"
```

---

### Phase 2: Sprint Metadata

**Collect details (AskUserQuestion):**
```
Start date: Default today
Duration: 2 weeks (14 days)
```

---

### Phase 3: Invoke Orchestration Skill

**Set context markers:**
```
**Operation:** plan-sprint
**Sprint Name:** ${SPRINT_NAME}
**Selected Stories:** ${STORY_IDS}
**Duration:** ${DURATION_DAYS} days
**Epic:** ${EPIC_ID}
```

**Invoke skill:**
```
Skill(command="devforgeai-orchestration")
```

**What skill does:**
- Invokes sprint-planner subagent (isolated context)
- Subagent creates sprint file
- Subagent updates story statuses
- Returns structured summary

---

### Phase 4: Display Results

**Output skill result:**
```
${result.display}

Next Steps:
${result.next_steps}
```

---

## Error Handling

### No Stories in Backlog
```
Error: No stories available
Action: Run /create-story first
```

### Invalid Story Selection
```
Error: Stories not found or wrong status
Action: Display valid options
```

### Sprint Creation Failed
```
Error: Subagent reported failure
Action: Display error details from skill
```

---

## Success Criteria

- [ ] Sprint file created in .ai_docs/Sprints/
- [ ] Stories updated to "Ready for Dev"
- [ ] Sprint references added to stories
- [ ] Workflow history updated
- [ ] Token usage ~3-5K (command overhead)
- [ ] Character count ~8K (53% of budget)

---

## Integration

**Invokes:** devforgeai-orchestration skill (Phase 3)
**Skill invokes:** sprint-planner subagent
**Updates:** Sprint files, story files
**Enables:** /dev command (stories now Ready for Dev)

---

## Performance

**Token Budget:**
- Command overhead: ~3K tokens
- User interaction: ~2K tokens
- Skill execution: ~40K tokens (isolated)
- Subagent: ~35K tokens (isolated)
- **Total main conversation:** ~5K tokens

**Execution Time:**
- User interaction: 2-5 minutes
- Sprint creation: 30-60 seconds
- **Total:** 3-6 minutes
```

**Target command file:** ~250 lines, ~8,000 characters

### Step 4: Update Memory References

**File:** `.claude/memory/subagents-reference.md`

Add sprint-planner to Available Subagents table:

```markdown
| **sprint-planner** | Sprint planning and story selection | sonnet | <40K | Sprint creation, story capacity validation |
```

Add to "Subagent Integration with Skills":

```markdown
**devforgeai-orchestration** uses:
- requirements-analyst (story creation)
- technical-debt-analyzer (sprint planning/retrospectives)
- **sprint-planner** (NEW - Phase 3 sprint planning workflow)
```

**File:** `.claude/memory/commands-reference.md`

Update /create-sprint entry:

```markdown
### /create-sprint [sprint-number]

**Purpose:** Plan 2-week sprint with story selection

**Invokes:** `devforgeai-orchestration` skill (Phase 3)

**Workflow:**
1. Epic selection (AskUserQuestion)
2. Story selection (AskUserQuestion)
3. Sprint metadata collection
4. Invoke orchestration skill → sprint-planner subagent
5. Display results

**Architecture (Post-Refactoring 2025-11-05):**

**Command (250 lines - Lean Orchestration):**
- User interaction (epic, stories, metadata)
- Skill invocation with context markers
- Result display

**Skill (devforgeai-orchestration - Phase 3):**
- Validate user inputs
- Invoke sprint-planner subagent
- Return summary

**Subagent (sprint-planner - NEW):**
- Sprint discovery (next number)
- Story validation and capacity
- Sprint file generation
- Story status updates
- Workflow history entries

**Token Efficiency:**
- Command: ~5K tokens
- Skill: ~40K tokens (isolated)
- Subagent: ~35K tokens (isolated)
- **Savings: 50% reduction in main conversation tokens**
- **Character budget: 8K (53% of limit) - COMPLIANT**
```

### Step 5: Update CLAUDE.md

**File:** `CLAUDE.md`

Update Component Summary:

```markdown
- **Subagents:** 20 (includes sprint-planner)
```

Update Project Structure:

```markdown
├── agents/              # 20 specialized subagents
│   └── [20 .md files including sprint-planner]
```

---

## Testing Strategy

### Unit Tests (10 cases)

**Test 1: Argument Validation**
```bash
/create-sprint
# Expected: Prompt for sprint name

/create-sprint "MVP Sprint"
# Expected: Proceed with name "MVP Sprint"
```

**Test 2: Epic Selection**
```
# Given: 3 epics exist
# When: Epic selection presented
# Then: User can select from 3 epics + "No epic" option
```

**Test 3: Story Selection**
```
# Given: 10 Backlog stories
# When: Story selection presented
# Then: Grouped by epic and priority, selectable
```

**Test 4: Capacity Validation (Over)**
```
# Given: Selected stories = 45 points
# When: Capacity checked
# Then: Warning "Over capacity (45 pts). Proceed?"
```

**Test 5: Capacity Validation (Under)**
```
# Given: Selected stories = 15 points
# When: Capacity checked
# Then: Warning "Under capacity (15 pts). Add more?"
```

**Test 6: Skill Invocation**
```
# Given: Valid inputs collected
# When: Phase 3 executes
# Then: Skill(command="devforgeai-orchestration") called with context markers
```

**Test 7: Subagent Result Parsing**
```
# Given: Subagent returns JSON
# When: Result received
# Then: Parse and display summary
```

**Test 8: Error Handling - No Backlog**
```
# Given: Zero Backlog stories
# When: Story selection attempted
# Then: Error displayed with guidance
```

**Test 9: Error Handling - Invalid Stories**
```
# Given: User selects STORY-999 (doesn't exist)
# When: Validation runs
# Then: Error with list of valid IDs
```

**Test 10: File Creation Verification**
```
# Given: Sprint created successfully
# When: Command completes
# Then: Sprint file exists at .ai_docs/Sprints/Sprint-N.md
```

### Integration Tests (8 cases)

**Test 1: Full Workflow - New Sprint**
```
# Given: Clean project with 5 Backlog stories
# When: /create-sprint "Sprint 1" executed
# Then:
#   - Sprint-1.md created
#   - 3 stories selected
#   - Stories status = Ready for Dev
#   - Sprint references added
#   - Workflow history updated
```

**Test 2: Multiple Sprints**
```
# Given: Sprint-1 exists
# When: /create-sprint "Sprint 2"
# Then: Sprint-2.md created (correct numbering)
```

**Test 3: Epic Linkage**
```
# Given: EPIC-001 exists
# When: Sprint linked to EPIC-001
# Then: Sprint file shows epic: EPIC-001
```

**Test 4: Cross-Epic Sprint**
```
# Given: Stories from EPIC-001 and EPIC-002
# When: Mixed stories selected
# Then: Sprint file shows epic: Multiple
```

**Test 5: Story Status Transition**
```
# Given: STORY-001 status = Backlog
# When: Added to sprint
# Then:
#   - STORY-001 status = Ready for Dev
#   - STORY-001 sprint = SPRINT-1
#   - Workflow history entry added
```

**Test 6: Capacity Calculation**
```
# Given: Stories with 5, 8, 3 points
# When: Sprint created
# Then: Sprint shows total_points: 16
```

**Test 7: Date Calculation**
```
# Given: Start date = 2025-11-05, Duration = 14 days
# When: Sprint created
# Then: End date = 2025-11-19
```

**Test 8: Next Steps Guidance**
```
# Given: Sprint created
# When: Results displayed
# Then: Next steps include "/dev STORY-001"
```

### Regression Tests (8 cases)

**Test 1: Backward Compatibility**
```
# Verify: /create-sprint behavior unchanged from user perspective
```

**Test 2: Sprint File Structure**
```
# Verify: YAML frontmatter matches original format
# Verify: Markdown sections match original
```

**Test 3: Story File Updates**
```
# Verify: Status transition same as original
# Verify: Sprint reference format same
# Verify: Workflow history format preserved
```

**Test 4: Error Messages**
```
# Verify: Error messages match original tone/content
```

**Test 5: Epic Linkage**
```
# Verify: Epic linking works as before
```

**Test 6: Capacity Warnings**
```
# Verify: Over/under capacity thresholds same (40/20 points)
```

**Test 7: Multi-Epic Sprints**
```
# Verify: Standalone and multi-epic sprints still supported
```

**Test 8: File Locations**
```
# Verify: Sprint files created in .ai_docs/Sprints/
# Verify: Story files updated in .ai_docs/Stories/
```

### Performance Tests

**Test 1: Token Budget**
```
# Verify: Command overhead <5K tokens
```

**Test 2: Character Budget**
```
# Verify: Command file <12K characters (target: ~8K)
```

**Test 3: Execution Time**
```
# Verify: Total time 3-6 minutes (within expected)
```

**Test 4: Subagent Token Usage**
```
# Verify: sprint-planner <40K tokens per invocation
```

---

## Implementation Timeline

### Phase 1: Preparation (15 minutes)
- [x] Create backup of original command
- [x] Review sprint-planner subagent (agent-generator output)
- [x] Review sprint-planning-guide.md reference
- [ ] Read refactoring plan in full

### Phase 2: Skill Update (20 minutes)
- [ ] Open devforgeai-orchestration/SKILL.md
- [ ] Add Phase 3: Sprint Planning Workflow (after Phase 2)
- [ ] Test skill can load reference file
- [ ] Verify subagent invocation pattern

### Phase 3: Command Refactoring (25 minutes)
- [ ] Create new command file from template
- [ ] Implement Phase 0: User Interaction (epic, stories, metadata)
- [ ] Implement Phase 3: Skill Invocation
- [ ] Implement Phase 4: Result Display
- [ ] Add error handling (minimal)
- [ ] Add integration notes

### Phase 4: Memory Updates (10 minutes)
- [ ] Update subagents-reference.md
- [ ] Update commands-reference.md
- [ ] Update CLAUDE.md Component Summary

### Phase 5: Testing (30 minutes)
- [ ] Unit tests (10 cases)
- [ ] Integration tests (8 cases)
- [ ] Regression tests (8 cases)
- [ ] Performance validation

### Phase 6: Deployment (10 minutes)
- [ ] Git commit with descriptive message
- [ ] Restart terminal
- [ ] Smoke tests (3 runs)
- [ ] Monitor for issues

**Total Estimated Time:** 110 minutes (~2 hours)

---

## Rollback Procedure

If refactoring causes issues:

```bash
# 1. Restore original command
cp .claude/commands/create-sprint.md.backup .claude/commands/create-sprint.md

# 2. Remove skill Phase 3 (if issues traced to skill)
# Edit devforgeai-orchestration/SKILL.md manually

# 3. Remove subagent (if not working)
rm .claude/agents/sprint-planner.md
rm .claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md

# 4. Restore memory files
git checkout HEAD~ .claude/memory/*.md

# 5. Restart terminal
# Reload original command

# 6. Document rollback reason
# Create .devforgeai/specs/enhancements/CREATE-SPRINT-ROLLBACK-REPORT.md
```

---

## Success Metrics

### Command Quality

| Metric | Before | After | Target | Status |
|--------|--------|-------|--------|--------|
| **Lines** | 497 | 250 | 150-300 | ✅ Within range |
| **Characters** | 12,525 | 8,000 | 6K-12K | ✅ Within range |
| **Budget %** | 84% | 53% | <70% | ✅ Compliant |
| **Phases** | 6 | 4 | 3-5 | ✅ Optimal |
| **Token Overhead** | ~12K | ~5K | <5K | ✅ Target met |

### Framework Compliance

- [x] Lean orchestration pattern applied
- [x] Skill invocation for business logic
- [x] Subagent for isolated context work
- [x] Reference file provides framework guardrails
- [x] No duplication (command/skill/subagent separation)
- [ ] Token efficiency >40% improvement (pending testing)

### Behavioral Preservation

- [ ] All original features preserved
- [ ] User experience unchanged
- [ ] Sprint file format identical
- [ ] Story update behavior same
- [ ] Error messages consistent

---

## Risk Assessment

### Low Risk ✅

- **Subagent created by agent-generator:** Follows proven templates
- **Reference file comprehensive:** 391 lines of explicit guidelines
- **Pattern proven:** /dev and /qa refactorings successful
- **Backup exists:** Original command preserved

### Medium Risk ⚠️

- **Skill modification:** Adding Phase 3 to orchestration skill (150 lines)
  - *Mitigation:* Test Phase 3 independently before integration
- **User interaction flow:** AskUserQuestion sequence changes
  - *Mitigation:* Preserve original dialog structure

### Managed Risk 🟡

- **Context extraction:** Skill must parse user inputs correctly
  - *Mitigation:* Explicit context markers, pattern matching validation
- **JSON parsing:** Command must parse subagent result
  - *Mitigation:* Structured format, error handling

---

## Related Documentation

**Core Principles:**
- `.devforgeai/protocols/lean-orchestration-pattern.md` - Refactoring methodology
- `.ai_docs/claude-skills.md` - Skills architecture
- `.ai_docs/Terminal/slash-commands-best-practices.md` - Command design

**Implementation Examples:**
- `.claude/commands/dev.md` - Lean orchestration reference (513 lines)
- `.claude/commands/qa.md` - Lean orchestration reference (295 lines)
- `.claude/agents/qa-result-interpreter.md` - Subagent example

**Subagent Generation:**
- `.devforgeai/SPRINT-PLANNER-GENERATION-SUMMARY.md` - Architecture overview
- `.devforgeai/COMMAND-REFACTORING-GUIDE-CREATE-SPRINT.md` - Step-by-step guide
- `.devforgeai/SPRINT-PLANNER-VERIFICATION.md` - Verification checklist

---

## Appendix A: Before/After Comparison

### Command Size

| Aspect | Before | After | Reduction |
|--------|--------|-------|-----------|
| Lines | 497 | 250 | 247 (50%) |
| Characters | 12,525 | 8,000 | 4,525 (36%) |
| Budget % | 84% | 53% | 31% improvement |

### Token Usage

| Context | Before | After | Savings |
|---------|--------|-------|---------|
| Command overhead | ~12K | ~5K | 7K (58%) |
| User interaction | ~2K | ~2K | 0 (same) |
| Business logic | In main | Isolated | ~35K moved |
| **Total main** | **~14K** | **~7K** | **7K (50%)** |

### Architecture

**Before:**
```
Command (497 lines)
└─ All 6 phases inline
```

**After:**
```
Command (250 lines)
└─ User interaction + orchestration
    └─ Skill (Phase 3)
        └─ Subagent (467 lines, isolated)
```

---

## Appendix B: File Manifest

### Files Modified

1. `.claude/commands/create-sprint.md` (497 → 250 lines)
2. `.claude/skills/devforgeai-orchestration/SKILL.md` (+150 lines for Phase 3)
3. `.claude/memory/subagents-reference.md` (+3 lines)
4. `.claude/memory/commands-reference.md` (~20 lines updated)
5. `CLAUDE.md` (subagent count updated)

### Files Created

1. `.claude/agents/sprint-planner.md` (467 lines) ✅ EXISTS
2. `.claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md` (391 lines) ✅ EXISTS
3. `.devforgeai/specs/enhancements/CREATE-SPRINT-REFACTORING-PLAN.md` (this file)

### Files for Backup

1. `.claude/commands/create-sprint.md.backup` (original preserved)

---

## Status: READY FOR IMPLEMENTATION

**Prerequisites:** ✅ All complete
- [x] sprint-planner subagent created
- [x] sprint-planning-guide.md reference created
- [x] Refactoring plan documented
- [x] Testing strategy defined
- [x] Rollback procedure prepared

**Next Action:** Begin Phase 2 - Update devforgeai-orchestration skill

**Estimated Completion:** 110 minutes (~2 hours)

**Confidence:** 🟢 HIGH (pattern proven, templates ready, comprehensive plan)
