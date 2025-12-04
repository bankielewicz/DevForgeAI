# `/create-sprint` Command Refactoring Guide

Guide for refactoring the `/create-sprint` command to use lean orchestration pattern with sprint-planner subagent.

---

## Overview

**Current Status:** Command is 497 lines, 84% of 15K character budget (top-heavy)

**Target Status:** Command is ~250 lines, 50% of 15K character budget (lean)

**Pattern:** Follow `/dev` and `/qa` refactoring pattern - delegate heavy logic to subagent

---

## Current Architecture (497 lines)

```
/create-sprint command
├─ Phase 1: Sprint Discovery (Glob, parse)
├─ Phase 2: Story Discovery & Selection (AskUserQuestion, Glob)
├─ Phase 3: Sprint Metadata Collection (AskUserQuestion x3)
├─ Phase 4: Sprint File Creation (Write + template logic)
├─ Phase 5: Update Story Status (Edit x N)
└─ Phase 6: Success Report (display)

All logic in command = 497 lines
```

## Target Architecture (250 lines)

```
/create-sprint command (refactored)
├─ Parse arguments (sprint-name if provided)
├─ Validate context (stories exist)
├─ Present story selection (AskUserQuestion)
│   └─ User selects: STORY-001, STORY-002, STORY-003
├─ Gather sprint metadata (AskUserQuestion)
│   └─ User provides: duration 14, epic EPIC-001
└─ Invoke sprint-planner subagent (Task)
    └─ Subagent handles: Phases 1-6 (discovery, generation, updates)
    └─ Returns: Structured JSON summary

Command size: ~250 lines (50% of budget)
Subagent size: 467 lines (isolated context, no token impact on main)
```

---

## Refactoring Steps

### Step 1: Keep User Interaction in Command

**What stays in `/create-sprint` command:**

```markdown
## Workflow

### Phase 1: Validate Context

Check for backlog stories:
```bash
Glob(pattern=".ai_docs/Stories/*.story.md")
```

If no stories exist:
```
AskUserQuestion:
  Question: "No stories found in Backlog. What would you like to do?"
  Options:
    - Create new stories first (exit, use /create-story)
    - Proceed anyway (skip sprint)
```

### Phase 2: Story Selection

Present available backlog stories:
```
AskUserQuestion:
  Question: "Found N stories in Backlog. Select stories for sprint:"

  Stories Available:
    [List all backlog stories with points, priority, epic]

  Options:
    - Select specific stories (provide IDs)
    - Select by priority (all HIGH, all HIGH+MEDIUM)
    - Select by epic
    - Custom selection
```

User response → List of story IDs

### Phase 3: Sprint Metadata

Gather sprint details via AskUserQuestion:
- Sprint name (if not provided in $1 argument)
- Duration (1/2/3 weeks, default 2)
- Start date (default today)
- Epic linkage

### Phase 4: Invoke Sprint Planner

```
Task(
  subagent_type="sprint-planner",
  description="Create Sprint-{N} with selected stories",
  prompt="Create sprint with:
    - Sprint name: {sprint_name}
    - Selected stories: {story_ids_comma_separated}
    - Duration: {duration_days} days
    - Epic: {epic_id}
    - Start date: {start_date}

    Execute complete sprint planning workflow and return summary."
)
```

### Phase 5: Report Results

Display results from subagent response:
```
✅ Sprint Created Successfully

Sprint Details:
  📋 {sprint_name}
  📅 {start_date} to {end_date}
  🎯 Epic: {epic_name}
  📊 Capacity: {total_points} points
  📝 Stories: {total_stories}

Stories Added:
  ✓ STORY-001: {title} ({points} points)
  ✓ STORY-002: {title} ({points} points)
  [...]

Next Steps:
  1. Review sprint goals
  2. Start first story: /dev STORY-001
  3. Track progress daily
```
```

### Step 2: Extract Constants and Helpers

**Before (inline):**
```
Each phase has hardcoded prompts, calculations, logic
```

**After (clean):**
```markdown
## Constants

SPRINT_CAPACITY_MIN = 20
SPRINT_CAPACITY_MAX = 40
SPRINT_CAPACITY_OPTIMAL_RANGE = "20-40 points"

## Helper Functions

validate_backlog_stories() → count
calculate_capacity_status(total_points) → "optimal"|"under"|"over"
```

### Step 3: Remove Phases 1-6 Logic Details

**What gets deleted from command:**

- Sprint discovery logic (already in subagent)
- Story validation logic (already in subagent)
- Capacity calculation code (already in subagent)
- Sprint document generation template (already in subagent)
- Story update loops (already in subagent)
- Success report formatting (subagent returns JSON)

**What stays:**

- Argument parsing (sprint-name)
- Story selection prompts
- Metadata gathering prompts
- Sprint planner invocation
- Result reporting

### Step 4: Update Command Structure

**New structure:**

```markdown
---
description: Create sprint plan with story selection
argument-hint: [sprint-name]
model: haiku
allowed-tools: Read, Glob, AskUserQuestion, Task
---

# Create Sprint Command

[Brief description]

## Arguments

[Keep current]

## Workflow

### Phase 1: Validate and Discover Stories
[Glob for backlog stories, count them]

### Phase 2: Story Selection
[AskUserQuestion - user selects stories]

### Phase 3: Sprint Metadata
[AskUserQuestion x 3 for duration, date, epic]

### Phase 4: Invoke Sprint Planner
[Task(subagent_type="sprint-planner", ...)]

### Phase 5: Report Results
[Display subagent response]

## Success Criteria
[Update to reference subagent success]

## Integration Points
[Update to show sprint-planner relationship]

## Error Handling
[Simplified - subagent handles most errors]
```

### Step 5: Remove Detailed Phase Documentation

**Before:**
```
### Phase 4: Sprint File Creation

**Generate sprint document:**

```bash
Write(
  file_path=".ai_docs/Sprints/Sprint-[N].md",
  content="[Sprint frontmatter + planning details]"
)
```

**Sprint file structure:**

```yaml
---
id: SPRINT-[N]
name: [Sprint Name]
...
[40 lines of YAML structure documentation]
```
[... 80+ more lines of template, examples, field descriptions ...]
```

**After:**
```
### Phase 4: Invoke Sprint Planner

Delegate sprint creation to specialized subagent:

```
Task(
  subagent_type="sprint-planner",
  description="Create Sprint-{N} with selected stories",
  prompt="Create sprint with selected stories, duration {duration}, epic {epic}"
)
```

Sprint planner handles:
- Discover next sprint number
- Validate stories
- Calculate capacity
- Generate sprint document
- Update story statuses
- Return structured summary

For sprint file format details: See `.claude/agents/sprint-planner.md`
```
```

### Step 6: Update Error Handling

**Before:**
```
### Error: Sprint File Creation Failed
[10 lines of specific error handling]

### Error: Story Update Failed
[10 lines of specific error handling]
```

**After:**
```
### Error: Story Selection Failed

**Condition:** No valid stories in Backlog

**Action:**
- Report no backlog stories
- Ask user to create stories first (/create-story)

### Error: Sprint Planner Failed

**Condition:** Subagent returns error

**Action:**
- Report specific error from subagent
- Suggest manual recovery steps
- Do not retry (subagent logic complete)

[Remove detailed file I/O errors - subagent handles those]
```

---

## Code Refactoring Example

### Phase 4 Comparison

**Current (In Command):**

```markdown
### Phase 4: Sprint File Creation

**Generate sprint document:**

```bash
Write(
  file_path=".ai_docs/Sprints/Sprint-[N].md",
  content="[Sprint frontmatter + planning details]"
)
```

**Sprint file structure:**

```yaml
---
id: SPRINT-[N]
name: [Sprint Name]
epic: [EPIC-ID or "Multiple" or "Standalone"]
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
duration_days: 14
status: Active
total_points: [Sum of story points]
completed_points: 0
stories:
  - STORY-001
  - STORY-002
  - STORY-003
created: YYYY-MM-DD HH:MM:SS
---

# Sprint [N]: [Sprint Name]

## Overview

**Duration:** [start_date] to [end_date] ([duration_days] days)
**Capacity:** [total_points] story points
**Epic:** [Epic name and link]

## Sprint Goals

[Generated from story themes - high-level objectives]

## Stories

### In Progress (0 points)
[Empty initially]

### Ready for Dev ([total_points] points)

#### STORY-001: [Story Title]
- **Points:** 5
- **Priority:** HIGH
- **Epic:** [Epic Name]
- **Acceptance Criteria:** [Count] criteria
- **Status:** Ready for Dev

[Repeat for each story]

### Completed (0 points)
[Empty initially]

## Sprint Metrics

- **Planned Velocity:** [total_points] points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** [count]
- **Stories Completed:** 0
- **Days Remaining:** [duration_days]

## Daily Progress

[Will be updated during sprint]

## Retrospective Notes

[To be filled at sprint end]

## Next Steps

1. Review and prioritize stories in sprint backlog
2. Begin implementation: `/implement STORY-[ID]`
3. Track progress daily
4. Update story statuses as work progresses
```

**Verify file written:**

```bash
Read(file_path=".ai_docs/Sprints/Sprint-[N].md")
```
```

**Lines:** 85 lines (just for Phase 4)

---

**Refactored (In Subagent):**

```markdown
### Phase 4: Invoke Sprint Planner

Delegate sprint creation to specialized subagent:

```
Task(
  subagent_type="sprint-planner",
  description="Create Sprint-{N} with {total_stories} selected stories",
  prompt="Create sprint with:
    - Sprint name: {sprint_name}
    - Selected stories: {story_ids}
    - Duration: {duration_days} days
    - Epic: {epic_id}
    - Start date: {start_date}

    Execute complete sprint planning workflow and return summary."
)
```

Sprint planner handles all document generation details. For format specification: See `.claude/agents/sprint-planner.md` or `references/sprint-planning-guide.md`.
```

**Lines:** 15 lines (just for Phase 4)

**Reduction:** 85 → 15 lines (82% reduction for this phase alone)

---

## Testing the Refactored Command

### Pre-Refactoring Test (Current)

```
> /create-sprint "User Authentication"
[Choose stories]
[Choose duration, epic]
→ Sprint created
→ Stories updated
→ Report displayed
```

### Post-Refactoring Test (New)

```
> /create-sprint "User Authentication"
[Choose stories via AskUserQuestion]
[Choose duration, epic via AskUserQuestion]
→ Task → sprint-planner subagent (isolated)
    ├─ Discover sprint number
    ├─ Validate stories
    ├─ Generate sprint file
    ├─ Update stories
    └─ Return JSON summary
→ Report displayed (from JSON)
```

**Expected behavior:** Identical from user perspective, but with:
- Faster token-to-value ratio (isolated context for heavy work)
- Clearer command structure (lean orchestration)
- Reusable subagent (can be invoked from skill or commands)

---

## Size Comparison

### Current `/create-sprint.md`

```
Total lines: 497
  - Workflow section: ~350 lines (6 phases)
  - Error handling: ~60 lines
  - Success criteria: ~15 lines
  - Integration: ~20 lines
  - Other: ~52 lines

Character count: ~12,525 (84% of 15K budget)
```

### Refactored `/create-sprint.md`

```
Total lines: ~250
  - Workflow section: ~120 lines (5 phases, subagent-delegated)
  - Error handling: ~20 lines
  - Success criteria: ~10 lines
  - Integration: ~30 lines (add sprint-planner reference)
  - Other: ~70 lines

Character count: ~6,500 (43% of 15K budget)
```

**Savings:** 497 → 250 lines (50% reduction), 12,525 → 6,500 chars (48% reduction)

**New capacity:** 50% → 43% budget = 7% headroom for future expansion

---

## Integration with Orchestration Skill

The orchestration skill can now delegate sprint planning:

```markdown
## Sprint Planning Phase

When orchestration needs to create sprint:

```
# Load user preferences from conversation
**Sprint name:** {sprint_name}
**Selected stories:** {story_ids_csv}
**Duration:** {duration_days}
**Epic:** {epic_id}

# Invoke sprint planner
Task(
  subagent_type="sprint-planner",
  description="Create sprint with selected stories",
  prompt="Create sprint with:
    - Sprint name: {sprint_name}
    - Selected stories: {story_ids_csv}
    - Duration: {duration_days}
    - Epic: {epic_id}"
)

# Extract result and proceed
IF success:
    Mark sprint created
    Update context with sprint_id
    Proceed to development phase
ELSE
    Report error
    Ask user for recovery
```
```

---

## Timeline for Implementation

1. **Create subagent** ✅ (Done: sprint-planner.md)
2. **Create reference guide** ✅ (Done: sprint-planning-guide.md)
3. **Refactor command** (~30 min)
   - Remove phases 1-6 detailed logic
   - Keep user interaction prompts
   - Update Phase 4 to invoke subagent
   - Simplify error handling
4. **Test refactored command** (~15 min)
   - Create test sprint
   - Verify story updates
   - Check metrics
5. **Update documentation** (~20 min)
   - Update command reference
   - Update subagents reference
   - Add sprint-planner to list
6. **Terminal restart and verify** (~5 min)
   - Restart to load sprint-planner
   - Test `/create-sprint` command
   - Verify /agents shows sprint-planner

**Total time:** ~70 minutes (1 hour 10 min)

---

## Files to Modify

### Modify (Refactor)
- `.claude/commands/create-sprint.md` - Remove Phases 1-6 logic, keep user interaction

### Create (Already Done)
- `.claude/agents/sprint-planner.md` - New subagent (467 lines) ✅
- `.claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md` - New reference (391 lines) ✅

### Update (Documentation)
- `.claude/memory/subagents-reference.md` - Add sprint-planner to list
- `.claude/memory/commands-reference.md` - Update /create-sprint description

---

## Success Criteria for Refactoring

- [x] sprint-planner subagent created and tested
- [ ] /create-sprint command refactored (<250 lines)
- [ ] Command uses lean orchestration pattern
- [ ] Invokes sprint-planner subagent correctly
- [ ] Results displayed from subagent response
- [ ] Error handling simplified
- [ ] No functional change from user perspective
- [ ] Token budget improved (50% reduction in command size)
- [ ] All tests passing
- [ ] Documentation updated

---

## Rollback Plan (If Needed)

If refactoring causes issues:

1. Restore original `.claude/commands/create-sprint.md`
2. Sprint planner subagent can remain (unused, no harm)
3. No changes to other commands or skills required
4. Full functionality restored

**Risk:** Low - command is isolated, no dependencies on changes

---

## Next: Orchestration Skill Integration

After `/create-sprint` refactoring, update devforgeai-orchestration skill:

```markdown
## Sprint Planning Phase

Orchestration skill detects when sprint creation needed:

```
# Detect sprint creation request
IF workflow_intent == "create-sprint" OR story_count > 1:
    # Load sprint parameters from conversation

    # Invoke sprint-planner subagent
    Task(subagent_type="sprint-planner", ...)

    # Update story statuses in skill context
    # Transition to next workflow phase
```
```

This enables full orchestration of Epic → Sprint → Story → Development workflow.

---

## Questions and Answers

**Q: Won't delegating to subagent slow down the command?**
A: No, subagent runs in parallel. Command stays responsive while subagent works in isolated context.

**Q: What if sprint planner fails?**
A: Error is returned in JSON response. Command displays error and recovery steps.

**Q: Can sprint-planner be reused?**
A: Yes. Can be invoked from orchestration skill, direct Task calls, or other commands.

**Q: How does this compare to /dev refactoring?**
A: Identical pattern - lightweight command delegates to subagent via Task tool.

**Q: Do users need to know about the subagent?**
A: No. From user perspective, /create-sprint command works identically. Subagent is implementation detail.

---

## Conclusion

Refactoring `/create-sprint` to use lean orchestration with sprint-planner subagent:
- Reduces command complexity by 50%
- Improves token efficiency through isolation
- Enables subagent reuse across tools
- Follows established pattern from /dev and /qa
- Maintains perfect backward compatibility with user experience

**Ready to proceed with refactoring.**

---

**Document:** `/create-sprint` Command Refactoring Guide
**Status:** Ready for Implementation
**Estimated Time:** 70 minutes
**Generated:** 2025-11-05
