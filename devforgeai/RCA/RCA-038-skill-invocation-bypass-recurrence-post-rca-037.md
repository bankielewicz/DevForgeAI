# RCA-038: Skill Invocation Bypass Recurrence Post-RCA-037

**Date:** 2026-02-13
**Reported By:** User
**Affected Component:** /create-story command + devforgeai-story-creation skill invocation
**Severity:** HIGH

---

## Issue Description

In session `7fe24492-10e5-44d4-8f9a-f51119e5d8ae`, despite RCA-037 fixes being implemented, Claude failed to properly invoke the devforgeai-story-creation skill after the /create-story command was invoked:

1. **First story (STORY-399):** Claude spent ~3 minutes executing the command's documented Epic Batch Workflow Steps 1-3 manually (Extract features, Multi-select, Batch metadata) BEFORE invoking the skill at Step 4.3. The skill was eventually invoked but only after extensive manual orchestration work.

2. **Second story:** When user asked "are you using devforgeai-story-creation skill?", Claude admitted: **"No — I was about to write the story file directly without invoking the skill."** Claude then corrected and invoked the skill only after user intervention.

**Expected behavior:** Command should immediately delegate to skill after minimal argument validation and context marker setting.

**Actual behavior:** Claude either delayed skill invocation (3 min manual work first) or attempted to bypass skill entirely.

**Impact:**
- User had to manually verify skill was being used
- Tokens wasted on manual orchestration work
- Framework workflow bypassed despite RCA-037 fixes
- User confidence in framework compliance reduced

---

## 5 Whys Analysis

**Issue:** Skill invocation delayed/bypassed in /create-story despite RCA-037 MANDATORY markers and WORKFLOW DISCIPLINE REMINDER

### Why #1: Why did Claude delay/bypass skill invocation despite RCA-037 fixes?

**Answer:** Claude executed the command's documented Steps 1-5 (Extract features, Multi-select, Batch metadata, Loop) as a manual workflow checklist BEFORE recognizing that skill invocation should happen in Step 4.3. The command's detailed step-by-step documentation was interpreted as "work to do" rather than "invoke skill which handles this."

**Evidence:**
- Session file line 3 shows Claude echoed entire `/create-story` command documentation
- Session file lines 3-50 show manual execution (Glob, Read, AskUserQuestion, TaskCreate) before skill invocation
- Session file line 52: First `Skill(skill="devforgeai-story-creation")` call

### Why #2: Why did Claude interpret documented steps as manual work instead of recognizing skill delegation?

**Answer:** The `/create-story` command file has **550 lines** documenting a detailed Epic Batch Workflow (Steps 1-5) and Single Story Workflow (Phase 1-4.5). Despite the `⚠️ INVOKE SKILL NOW (MANDATORY)` marker at Step 4.3, the sheer volume of documented workflow steps before that point caused Claude to enter "checklist execution mode" - treating each step as work to perform manually.

**Evidence:**
- `.claude/commands/create-story.md` lines 46-156: **110 lines** of Epic Batch Workflow
- Steps 1-3 contain explicit code blocks: `Grep(pattern=...)`, `AskUserQuestion(...)`
- Step 4.3 (line 135) has MANDATORY marker but is buried after extensive step documentation

### Why #3: Why does having detailed workflow documentation before skill invocation cause Claude to execute manually?

**Answer:** Claude's instruction-following prioritizes explicit step-by-step documentation over implicit architectural principles. When Claude sees "### Step 1: Extract Features from Epic" followed by code blocks showing `Grep(pattern=...)`, it executes that step. The lean orchestration principle ("Commands orchestrate. Skills validate.") is stated elsewhere but is not reinforced at the point where steps are documented.

**Evidence:**
- CLAUDE.md lines 551-560 state skill execution model
- Command file Steps 1-3 don't reference lean orchestration
- RCA-037 REC-4 reminder at lines 50-54 gets overshadowed by detailed step documentation

### Why #4: Why isn't the lean orchestration principle reinforced at each workflow step?

**Answer:** RCA-037 REC-1 focused on making Step 4.3 explicit but didn't address the fundamental structural issue: Steps 1-3 (Extract features, Multi-select, Batch metadata) are documented with detailed implementation code blocks that Claude follows. The fix added a "DO NOT proceed with manual analysis" warning at Step 4.3, but Steps 1-3 still look like work Claude should perform.

**Evidence:**
- RCA-037 REC-1 added explicit `Skill()` at Step 4.3 ✓ (verified at lines 130-138)
- RCA-037 REC-4 added WORKFLOW DISCIPLINE REMINDER ✓ (verified at lines 50-54)
- Steps 1-3 (lines 58-107) still have detailed code blocks for manual execution
- Second story bypass shows even Phase 1/2 warnings insufficient

### Why #5 (ROOT CAUSE):

**ROOT CAUSE:** The `/create-story` command's architecture fundamentally conflicts with lean orchestration. It documents **Steps 1-3 as manual work with implementation code blocks**, then says "invoke skill" at Step 4.3. This creates a **hybrid command/skill workflow** where Claude executes command-documented steps AND skill phases.

The RCA-037 fix made skill invocation at Step 4.3 explicit but didn't resolve the structural conflict where **110+ lines of "manual steps" precede the skill invocation point**. Claude interprets these documented steps as work to perform, not as documentation of what the skill will do.

The correct architecture per lean-orchestration-pattern.md:
1. Command validates arguments (minimal, ~20 lines)
2. Command sets context markers (minimal, ~10 lines)
3. Command invokes skill IMMEDIATELY (line ~30)
4. Skill handles ALL workflow (extraction, selection, metadata, creation)

Current architecture:
1. Command validates arguments (~20 lines)
2. Command documents 110+ lines of manual workflow steps
3. Command says "invoke skill" at Step 4.3 (line ~135)
4. Skill ALSO has 8 phases

This hybrid model causes confusion: Claude either executes Steps 1-3 then skill, or skips skill entirely thinking command already handled the work.

---

## Evidence Collected

### Files Examined

#### Session File: `/home/bryan/.claude/projects/-mnt-c-Projects-DevForgeAI2/7fe24492-10e5-44d4-8f9a-f51119e5d8ae.jsonl`
- **Finding:** Clear evidence of delayed and bypassed skill invocation
- **Lines examined:** 1-400
- **Excerpts:**
  - Line 3: Claude echoes entire command documentation
  - Lines 3-50: Manual execution of Steps 1-3 (Glob, Read, AskUserQuestion, TaskCreate)
  - Line 52: First Skill() invocation after ~3 min delay
  - Lines 307-309: User asks "are you using devforgeai-story-creation skill?" - Claude admits "No"
- **Significance:** CRITICAL - Direct evidence of recurrence

#### `.claude/commands/create-story.md`
- **Finding:** Command contains 550 lines, with 110+ lines of manual workflow before skill invocation
- **Lines examined:** 46-156 (Epic Batch Workflow)
- **Excerpts:**
  ```markdown
  ### Step 1: Extract Features from Epic
  Grep(pattern="### Feature", path="devforgeai/specs/Epics/${EPIC_ID}*.epic.md")

  ### Step 2: Multi-Select Features
  AskUserQuestion(questions=[{...}])

  ### Step 3: Batch Metadata Collection
  AskUserQuestion(questions=[{...}])

  ### Step 4.3: ⚠️ INVOKE SKILL NOW (MANDATORY)
  Skill(command="devforgeai-story-creation")
  DO NOT proceed with manual analysis.
  ```
- **Significance:** HIGH - Shows structural conflict (Steps 1-3 with code blocks before skill invocation)

#### `devforgeai/RCA/RCA-037-skill-invocation-skipped-despite-orchestrator-instructions.md`
- **Finding:** Previous RCA addressed same issue but fix was insufficient
- **Excerpts:**
  - REC-1: Added explicit Skill() at Step 4.3 ✓
  - REC-2: Documented Skill Invocation Checkpoint Pattern ✓
  - REC-4: Added WORKFLOW DISCIPLINE REMINDER ✓
- **Significance:** HIGH - Shows attempted fixes that didn't prevent recurrence

#### `.claude/skills/devforgeai-story-creation/SKILL.md`
- **Finding:** Skill has comprehensive 8-phase workflow that duplicates what command documents
- **Lines examined:** 1-617
- **Excerpts:**
  - Line 22-36: Execution model states "YOU (Claude) execute these instructions phase by phase"
  - Lines 197-520: 8 phases including Discovery, Requirements, Tech Spec, UI Spec, File Creation
- **Significance:** MEDIUM - Skill is comprehensive, doesn't need command pre-work

#### `devforgeai/protocols/lean-orchestration-pattern.md`
- **Finding:** Pattern clearly states commands should invoke skill immediately
- **Lines examined:** 45-80
- **Excerpts:**
  ```markdown
  **What commands SHOULD do:**
  1. Parse arguments
  2. Load context
  3. Set markers
  4. Invoke skill - Single Skill(command="...") call
  5. Display results
  ```
- **Significance:** HIGH - Confirms architectural violation

#### `CLAUDE.md` Skills Execution Section
- **Finding:** Explains inline expansion model
- **Lines examined:** 548-590
- **Excerpts:**
  - "Skills are **INLINE PROMPT EXPANSIONS**, not background processes"
  - "After Skill(command="...")... YOU execute the skill's phases"
  - "NEVER wait passively after skill invocation"
- **Significance:** MEDIUM - Execution model is documented, but not preventing bypass

### Context Files Status

Not directly applicable (issue is architectural, not constraint violation)

### Workflow State

- Session: Active during story creation from EPIC-064
- Command mode: EPIC_BATCH
- Stories attempted: 2 (STORY-399, STORY-400)
- Skill invocation: Delayed for first, bypassed attempt for second

---

## Recommendations (Evidence-Based)

### CRITICAL Priority (Implement Immediately)

#### REC-1: Restructure /create-story Command to Invoke Skill Immediately
**Implemented in:** STORY-408

**Problem Addressed:** Command has 110+ lines of manual workflow documentation before skill invocation, causing hybrid execution

**File:** `.claude/commands/create-story.md`
**Location:** Lines 46-156 (Epic Batch Workflow) and 158-290 (Single Story Workflow)
**Change Type:** MAJOR REFACTOR

**Current Structure (WRONG):**
```
Phase 0: Mode Detection (40 lines)
## Epic Batch Workflow (110 lines)
  Step 1: Extract Features (20 lines with code blocks)
  Step 2: Multi-Select Features (25 lines with code blocks)
  Step 3: Batch Metadata (20 lines with code blocks)
  Step 4: Story Creation Loop (45 lines)
    Step 4.3: INVOKE SKILL (finally!)
## Phase 1: Single Story Workflow (90 lines)
## Phase 2: Invoke Story Creation Skill (50 lines)
```

**Proposed Structure (CORRECT):**
```
# /create-story - Create User Story

Transform feature → complete story. Delegates to devforgeai-story-creation skill.

---

## Quick Reference
/create-story epic-XXX     # Batch mode from epic
/create-story "description" # Single story mode

---

## Phase 0: Argument Validation (~30 lines)

Parse $1:
- If matches epic-XXX → MODE = "EPIC_BATCH", set epic_id
- If 10+ words → MODE = "SINGLE_STORY", set description
- Else → AskUserQuestion for mode

Validate:
- If EPIC_BATCH: Verify epic file exists via Glob
- If SINGLE_STORY: Verify description length ≥10 words

---

## Phase 1: Set Context Markers and Invoke Skill IMMEDIATELY (~20 lines)

**⚠️ INVOKE SKILL NOW (MANDATORY):**

**Mode:** ${MODE}
**Epic ID:** ${epic_id or "none"}
**Feature Description:** ${description or "batch from epic"}

Skill(command="devforgeai-story-creation")

**DO NOT execute workflow steps manually.**
**The skill handles: feature extraction, selection, metadata, creation.**

---

## Phase 2: Display Results (~20 lines)

Output: skill completion report
If batch: summary of created stories
If single: story details

---

## Error Handling (~30 lines)
[Minimal error handling as before]

---

Total: ~100-150 lines (vs current 550 lines)
```

**Key Changes:**
1. REMOVE Steps 1-3 code blocks from Epic Batch Workflow
2. MOVE feature extraction, selection, metadata collection INTO skill
3. INVOKE SKILL in Phase 1, not Phase 2 or Step 4.3
4. Command does ONLY: argument validation, context markers, skill invocation, result display

**Rationale:**
- Eliminates hybrid architecture that causes confusion
- Skill already has Phase 1 (Story Discovery) that handles metadata collection
- Skill can handle batch mode internally (already has batch mode support per lines 156-192)
- Aligns with lean-orchestration-pattern.md prescription

**Testing Procedure:**
1. Run `/create-story epic-064`
2. Verify NO manual Grep/Read/AskUserQuestion before Skill() call
3. Verify Skill() invoked within first 10 seconds
4. Verify all feature selection/metadata happens inside skill
5. Run single mode: `/create-story "add data class detection"`
6. Verify immediate skill invocation

**Effort Estimate:** 3-4 hours (major refactor)

---

#### REC-2: Move Batch Workflow Logic into devforgeai-story-creation Skill
**Implemented in:** STORY-409

**Problem Addressed:** Batch workflow (feature extraction, multi-select) is currently documented in command

**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`
**Location:** Phase 1: Story Discovery
**Change Type:** ENHANCE

**Add to Phase 1 (Story Discovery):**

```markdown
### Step 0.1: Batch Mode Detection

IF conversation contains marker `**Mode:** EPIC_BATCH`:
  batch_mode = true
  epic_id = extract from `**Epic ID:**` marker

  # Step 0.2: Extract Features from Epic
  epic_file = Glob(pattern="devforgeai/specs/Epics/${epic_id}*.epic.md")
  epic_content = Read(file_path=epic_file)
  features = extract_features(epic_content)  # Parse ### Feature headers

  # Step 0.3: Multi-Select Features (if not already selected)
  IF features not already specified in context:
    AskUserQuestion(
      question: "Which features should have stories created?",
      header: "Feature Selection",
      options: [feature options with descriptions],
      multiSelect: true
    )

  # Step 0.4: Batch Metadata Collection
  AskUserQuestion for: sprint, priority, points approach

  # Step 0.5: Create Loop Context
  FOR each selected_feature:
    Generate next STORY-NNN ID
    Set batch context markers
    Execute Phases 2-7 for this story
    Track result

  # Step 0.6: Return Batch Summary
  Return: created stories list, failed count, next actions

ELSE (single story mode):
  Continue to standard Phase 1 workflow
```

**Rationale:**
- Skill already supports batch mode (lines 156-192) but expects command to do feature selection
- Moving selection INTO skill makes command truly lean
- Skill context isolation handles token-heavy batch work appropriately

**Testing Procedure:**
1. Invoke skill with `**Mode:** EPIC_BATCH` marker
2. Verify skill performs feature extraction
3. Verify skill asks for feature selection
4. Verify all stories created correctly

**Effort Estimate:** 2-3 hours

---

### HIGH Priority (Implement This Sprint)

#### REC-3: Add Pre-Invocation Guard to Command

**Problem Addressed:** Even with restructured command, Claude might still deviate

**File:** `.claude/commands/create-story.md`
**Location:** Top of file, after frontmatter
**Change Type:** ADD

**Add immediately after description:**

```markdown
---

## ⛔ CRITICAL: Lean Orchestration Enforcement

**This command follows lean orchestration pattern. Read these rules BEFORE executing:**

1. ❌ DO NOT execute Grep() to extract features - skill handles this
2. ❌ DO NOT execute AskUserQuestion for metadata - skill handles this
3. ❌ DO NOT manually analyze epic content - skill handles this
4. ❌ DO NOT create story files directly - skill handles this

5. ✅ DO validate arguments (epic-XXX format or description length)
6. ✅ DO set context markers (Mode, Epic ID, Description)
7. ✅ DO invoke Skill(command="devforgeai-story-creation") IMMEDIATELY
8. ✅ DO display skill results

**If you find yourself executing Grep/Read/Write before Skill(), HALT and invoke skill.**

---
```

**Rationale:**
- Explicit "don't do" list counters tendency to interpret step documentation as work
- Placed at top of file to be seen before any workflow documentation
- Reinforces lean orchestration at point of execution

**Testing Procedure:**
1. Manually inspect Claude's tool calls after `/create-story`
2. First substantive call should be Skill() (after at most Glob for validation)

**Effort Estimate:** 30 minutes

---

#### REC-4: Create Automated Audit for Command/Skill Hybrid Violations
**Implemented in:** STORY-410

**Problem Addressed:** Need systematic detection of commands that document skill work

**File:** New: `.claude/scripts/audit-command-skill-overlap.sh`
**Change Type:** ADD

**Script Logic:**

```bash
#!/bin/bash
# Audit commands for potential lean orchestration violations

for cmd in .claude/commands/*.md; do
  # Count lines between command start and Skill() invocation
  first_skill_line=$(grep -n "Skill(command=" "$cmd" | head -1 | cut -d: -f1)

  if [ -z "$first_skill_line" ]; then
    echo "⚠️ $cmd: No Skill() invocation found"
    continue
  fi

  # Count code blocks before Skill()
  code_blocks=$(head -n "$first_skill_line" "$cmd" | grep -c '```')

  if [ "$code_blocks" -gt 4 ]; then
    echo "❌ $cmd: $code_blocks code blocks before Skill() - potential hybrid violation"
  else
    echo "✅ $cmd: Clean ($code_blocks code blocks before Skill())"
  fi
done
```

**Rationale:**
- Automated detection prevents recurrence in other commands
- Codifies "commands should invoke skill quickly" as measurable metric

**Effort Estimate:** 1 hour

---

### MEDIUM Priority (Next Sprint)

#### REC-5: Update lean-orchestration-pattern.md with Hybrid Violation Pattern
**Implemented in:** STORY-411

**Problem Addressed:** Need to document this anti-pattern for future prevention

**File:** `devforgeai/protocols/lean-orchestration-pattern.md`
**Location:** Anti-Patterns section (after line 480)
**Change Type:** ADD

**Add Anti-Pattern 6:**

```markdown
### Anti-Pattern 6: Hybrid Command/Skill Workflow

**Problem:**
```markdown
# Command documents workflow steps that skill also performs
## Epic Batch Workflow
### Step 1: Extract Features ← Claude executes this
### Step 2: Multi-Select Features ← Claude executes this
### Step 3: Batch Metadata ← Claude executes this
### Step 4.3: INVOKE SKILL ← Then skill ALSO has these phases!
```

**Why This Fails:**
- Claude interprets documented steps as work to perform
- Skill invocation comes AFTER manual work, not BEFORE
- Results in duplicate work or skill bypass
- RCA-037 + RCA-038 documented this pattern's failure

**Solution:**
```markdown
# Command invokes skill IMMEDIATELY
## Phase 0: Validate Arguments
## Phase 1: Set Markers and Invoke Skill
Skill(command="devforgeai-story-creation")
# Skill handles all workflow (extraction, selection, creation)
```

**Rule:** If workflow step belongs in skill, don't document it in command with code blocks.
```

**Effort Estimate:** 30 minutes

---

#### REC-6: Add Skill Invocation Timing Metric to Framework Monitoring

**Problem Addressed:** No visibility into how quickly commands invoke skills

**Approach:** Add optional timing log to skill invocations

**File:** Could be hook-based or manual instrumentation

**Metric:** `time_to_skill_invocation_ms` - Time from command start to Skill() call

**Target:** <5 seconds for most commands (indicates no manual pre-work)

**Effort Estimate:** 2 hours

---

### LOW Priority (Backlog)

#### REC-7: Review All Commands for Similar Hybrid Patterns
**Implemented in:** STORY-412

**Problem Addressed:** Other commands may have same structural issue

**Action:** Audit these commands:
- `/ideate` - Check for manual work before skill
- `/dev` - Check for manual work before skill (already refactored per RCA history)
- `/qa` - Check for manual work before skill
- `/create-epic` - Check for manual work before skill

**Effort Estimate:** 2 hours

---

## Implementation Checklist

### Immediate (REC-1, REC-2, REC-3)
- [ ] Backup `/create-story.md`: `cp create-story.md create-story.md.backup-rca038`
- [ ] Restructure command to invoke skill in Phase 1 (REC-1): See STORY-408
- [ ] Move batch workflow logic into skill Phase 1 (REC-2): See STORY-409
- [ ] Add pre-invocation guard to command top (REC-3)
- [ ] Test: `/create-story epic-064` - verify immediate skill invocation
- [ ] Test: `/create-story "add data class detection"` - verify immediate skill invocation
- [ ] Test: Verify batch mode still works correctly
- [ ] Test: Verify single mode still works correctly

### This Sprint (REC-4)
- [ ] REC-4: Create audit script for command/skill overlap: See STORY-410
- [ ] Run audit on all commands
- [ ] Fix any other violations found

### Next Sprint (REC-5, REC-6, REC-7)
- [ ] REC-5: Update lean-orchestration-pattern.md with Anti-Pattern 6: See STORY-411
- [ ] Implement skill invocation timing metric
- [ ] REC-7: Review All Commands for Similar Hybrid Patterns: See STORY-412

### Documentation
- [ ] Update `CLAUDE.md` if lean orchestration guidance needs reinforcement
- [ ] Commit RCA-038 with reference to RCA-037
- [ ] Link to any stories created for substantial work

---

## Prevention Strategy

**Short-term (Immediate):**
- Restructure /create-story to invoke skill immediately (REC-1)
- Add explicit "don't do" guards at top of command (REC-3)
- Manual review of other commands for similar patterns

**Long-term (Framework Enhancement):**
- Automated audit script to detect hybrid violations (REC-4)
- Skill invocation timing metric (REC-6)
- Update lean orchestration protocol with explicit anti-pattern (REC-5)
- Establish "lines before Skill()" as measurable command health metric

**Monitoring:**
- Watch for: Commands with >50 lines before Skill() invocation
- Watch for: User reports of "Claude didn't use the skill"
- Audit trigger: After any command modification, run overlap audit
- Escalation: If hybrid pattern recurs, consider architectural enforcement (pre-commit check)

---

## Related RCAs

- **RCA-037:** Skill Invocation Skipped Despite Orchestrator Instructions - **DIRECT PREDECESSOR**
  - Same root issue (skill invocation not immediate)
  - RCA-037 fixes addressed Step 4.3 but not Steps 1-3
  - RCA-038 addresses structural architecture problem

- **RCA-029:** Brainstorm Skill Bypass During Plan Mode - Similar pattern where skill was not invoked

- **RCA-022:** Mandatory TDD Phases Skipped - Similar workflow deviation pattern

---

## Status

**Status:** IN_PROGRESS
**Resolution:** Stories created for REC-1 (STORY-408), REC-2 (STORY-409), REC-4 (STORY-410), REC-5 (STORY-411), REC-7 (STORY-412). REC-3 included in STORY-408 scope. REC-6 pending.
**Successor to:** RCA-037 (this RCA supersedes RCA-037 findings)

---

**RCA Created:** 2026-02-13
**RCA Number:** RCA-038
**RCA Title:** Skill Invocation Bypass Recurrence Post-RCA-037
