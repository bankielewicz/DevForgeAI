# RCA-037: Skill Invocation Skipped Despite Orchestrator Instructions

**Date:** 2026-02-02
**Reporter:** User
**Component:** /create-story command (Epic Batch Workflow)
**Severity:** HIGH

---

## Issue Description

When user invoked `/create-story epic-056`, Claude correctly detected EPIC_BATCH mode and validated the epic exists. However, Claude did NOT:
1. Present features via AskUserQuestion (Step 2 of Epic Batch Workflow)
2. Invoke `Skill(command="devforgeai-story-creation")` as required

Instead, Claude:
1. Read the epic file
2. Started manual analysis by checking for existing stories via Grep
3. Was interrupted by user who noticed the workflow deviation

**Expected behavior:** Command should follow Epic Batch Workflow steps: Extract features → Multi-select → Batch metadata → Loop with Skill invocation

**Actual behavior:** Claude deviated after epic validation to perform manual "preparation" analysis not prescribed by the command

**Impact:**
- User didn't get the interactive feature selection experience
- Skill workflow never executed
- Manual analysis wasted tokens and time
- Framework workflow bypassed

---

## 5 Whys Analysis

### Problem Statement
/create-story epic-056 invoked but devforgeai-story-creation skill NOT called. Claude started manual Grep analysis instead.

### Why #1: Why did Claude not invoke the devforgeai-story-creation skill?

**Answer:** Claude treated the Epic Batch Workflow as a research/preparation task rather than an immediate delegation to the skill. After validating the epic exists and reading its contents, Claude started checking for existing stories via Grep - treating this as "preparation before invoking the skill."

**Evidence:** After reading the epic, Claude immediately ran:
```
Grep(pattern="epic: EPIC-056", glob="devforgeai/specs/Stories/*.story.md")
```
This was NOT prescribed by the command's Epic Batch Workflow (lines 46-67).

### Why #2: Why did Claude add manual analysis steps not prescribed by the command?

**Answer:** The command contains extensive documentation that could be misinterpreted as "thorough analysis guidance" rather than "strict execution steps." The Epic Batch Workflow section (lines 46-67) is only 21 lines - brief compared to the 499-line command. Claude "filled in the gaps" with what seemed like reasonable preparation.

**Evidence:** The `/create-story` command at lines 50-51 says:
```
1. Extract features from epic (Grep: "### Feature X.Y:")
2. Multi-select features (AskUserQuestion, multiSelect: true)
```
But Claude deviated: Instead of immediately presenting features via AskUserQuestion (Step 2), Claude decided to "first check what stories already exist."

### Why #3: Why did Claude deviate from the prescribed workflow steps?

**Answer:** Claude interpreted the command's extensive documentation about the skill's 8-phase workflow (lines 165-204) as context/background information rather than as the clear delegation instruction. The command describes what the skill DOES but doesn't have an explicit "STOP HERE AND INVOKE SKILL" checkpoint in the batch workflow.

**Evidence:** From `/create-story.md` lines 185-196:
```markdown
**Invoke skill:**
Skill(command="devforgeai-story-creation")
```
This instruction is clear BUT it's in "Phase 2: Invoke Story Creation Skill" which is for SINGLE_STORY mode. The Epic Batch Workflow doesn't have an equally explicit "INVOKE SKILL NOW" marker.

### Why #4: Why does the Epic Batch Workflow lack explicit skill invocation instruction?

**Answer:** The Epic Batch Workflow section is a condensed summary (21 lines) that assumes Claude will follow Step 4: "Loop: Gap-aware ID → Markers → Skill → Track". The word "Skill" appears but without the explicit `Skill(command="devforgeai-story-creation")` tool invocation pattern shown in Single Story mode.

**Evidence:** Epic Batch Workflow (lines 50-54):
```
4. Loop: Gap-aware ID → Markers → Skill → Track
```
Compare to Single Story Workflow (line 188):
```
Skill(command="devforgeai-story-creation")
```
The batch workflow says "Skill" but doesn't show the explicit tool call syntax.

### Why #5 (ROOT CAUSE):

**ROOT CAUSE:** The `/create-story` command's Epic Batch Workflow section lacks explicit `Skill(command="devforgeai-story-creation")` invocation instruction with the same clarity as the Single Story Workflow. The batch workflow describes steps at a high level ("Markers → Skill → Track") without the explicit tool call format, creating ambiguity about WHEN and HOW to invoke the skill. Combined with Claude's tendency to "prepare" before execution, this gap allowed deviation from the prescribed workflow.

---

## Evidence Collected

### Files Examined

#### `.claude/commands/create-story.md` (Lines 46-67)
- **Finding:** Epic Batch Workflow uses summary language ("Markers → Skill") without explicit Skill() tool invocation
- **Excerpt (lines 50-54):**
```markdown
1. Extract features from epic (Grep: "### Feature X.Y:")
2. Multi-select features (AskUserQuestion, multiSelect: true)
3. Batch metadata: sprint, priority
4. Loop: Gap-aware ID → Markers → Skill → Track
5. Summary: Created/failed counts, story list
```
- **Significance:** CRITICAL - This is the gap that caused the deviation

#### `.claude/commands/create-story.md` (Lines 185-204)
- **Finding:** Single Story mode has explicit Skill() invocation
- **Excerpt (lines 187-188):**
```markdown
**Invoke skill:**
Skill(command="devforgeai-story-creation")
```
- **Significance:** HIGH - Shows correct pattern that batch mode is missing

#### `.claude/skills/devforgeai-story-creation/SKILL.md` (Lines 22-36)
- **Finding:** Skill has clear execution model stating "YOU execute these instructions phase by phase"
- **Excerpt (lines 22-27):**
```markdown
## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
```
- **Significance:** HIGH - Skill was never invoked so this execution model never applied

#### `devforgeai/protocols/lean-orchestration-pattern.md` (Lines 43-55)
- **Finding:** Commands should "Invoke skill - Single Skill(command="...") call"
- **Excerpt (lines 49-55):**
```markdown
**What commands SHOULD do:**
1. **Parse arguments** - Extract and validate user input
2. **Load context** - Load story/epic files
3. **Set markers** - Provide explicit context statements
4. **Invoke skill** - Single Skill(command="...") call
5. **Display results** - Output what skill returns
```
- **Significance:** MEDIUM - Confirms pattern that commands should have explicit skill invocation

### Related RCAs

- **RCA-029:** Brainstorm Skill Bypass During Plan Mode - Similar pattern of skill invocation not occurring
- **RCA-022:** Mandatory TDD Phases Skipped - Similar workflow deviation pattern

---

## Recommendations

### CRITICAL Priority

#### REC-1: Add Explicit Skill Invocation to Epic Batch Workflow
**Implemented in:** STORY-354

**Problem Addressed:** Epic Batch Workflow lacks explicit `Skill(command="devforgeai-story-creation")` tool call format

**File:** `.claude/commands/create-story.md`
**Location:** Lines 46-67 (Epic Batch Workflow section)
**Change Type:** MODIFY

**Current Text (lines 46-67):**
```markdown
## Epic Batch Workflow (NEW)

**Triggered:** MODE="EPIC_BATCH"

1. Extract features from epic (Grep: "### Feature X.Y:")
2. Multi-select features (AskUserQuestion, multiSelect: true)
3. Batch metadata: sprint, priority
4. Loop: Gap-aware ID → Markers → Skill → Track
5. Summary: Created/failed counts, story list

**Context markers per story:**
...
```

**Proposed Replacement:**
```markdown
## Epic Batch Workflow (NEW)

**Triggered:** MODE="EPIC_BATCH"

### Step 1: Extract Features from Epic
```
Grep(pattern="### Feature", path="${epic_file}", output_mode="content")
Extract feature list: [Feature 1.1, Feature 1.2, ...]
```

### Step 2: Multi-Select Features
```
AskUserQuestion(
  questions=[{
    question: "Select features to create stories for:",
    header: "Feature Selection",
    options: [extracted features with descriptions],
    multiSelect: true
  }]
)
```

### Step 3: Batch Metadata
```
AskUserQuestion for:
- Sprint assignment (multiSelect: false)
- Default priority (multiSelect: false)
```

### Step 4: Story Creation Loop

**FOR each selected feature:**

4.1. Generate gap-aware Story ID (Glob existing stories, find next number)

4.2. Set context markers:
```
**Story ID:** STORY-{NNN}
**Epic ID:** ${EPIC_ID}
**Feature Description:** {feature.description}
**Priority:** {priority}
**Points:** {feature.points}
**Sprint:** {sprint}
**Batch Mode:** true
```

4.3. **⚠️ INVOKE SKILL NOW (MANDATORY):**
```
Skill(command="devforgeai-story-creation")
```
DO NOT proceed with manual analysis. The skill handles all subsequent workflow.

4.4. Track result: success/failure

**END FOR**

### Step 5: Summary
Display: Created/failed counts, story list, next action

**Context markers per story:**
```

**Rationale:**
- The explicit `Skill(command="devforgeai-story-creation")` in Step 4.3 matches the pattern from Single Story mode
- Step numbering makes the workflow unambiguous
- [MANDATORY] and warning markers emphasize this is not optional
- "DO NOT proceed with manual analysis" explicitly prevents the observed deviation

**Testing Procedure:**
1. Run `/create-story epic-056`
2. Verify AskUserQuestion presented for feature selection (Step 2)
3. Verify Skill() invoked for each selected feature (Step 4.3)
4. Verify stories created in devforgeai/specs/Stories/

**Effort Estimate:** 30 minutes

---

### HIGH Priority

#### REC-2: Document Skill Invocation Checkpoint Pattern in Lean Orchestration Protocol
**Implemented in:** STORY-355

**Problem Addressed:** Other commands may have similar implicit skill invocation

**File:** `devforgeai/protocols/lean-orchestration-pattern.md`
**Location:** After line 55 (What commands SHOULD do)
**Change Type:** ADD

**Exact Text to Add:**
```markdown
### Skill Invocation Checkpoint Pattern

**For commands with multiple workflow modes (single vs batch):**

Each mode MUST have explicit `Skill(command="...")` invocation with:
1. Clear step number (e.g., "Step 4.3")
2. MANDATORY marker or warning emoji (⚠️)
3. Explicit tool call syntax (not summary like "→ Skill →")
4. "DO NOT proceed with manual analysis" statement

**Example (WRONG):**
```
Loop: ID → Markers → Skill → Track
```

**Example (CORRECT):**
```
### Step 4.3: ⚠️ INVOKE SKILL NOW (MANDATORY)
Skill(command="devforgeai-story-creation")
DO NOT proceed with manual analysis. The skill handles all subsequent workflow.
```

**Rationale:** Summary language creates ambiguity about WHEN to invoke skill. Explicit tool syntax with warning is unambiguous.
```

**Effort Estimate:** 15 minutes

---

#### REC-3: Audit Other Commands for Similar Pattern
**Implemented in:** STORY-356

**Problem Addressed:** Other commands may have similar implicit skill invocation gaps

**Priority:** HIGH

**Action:** Audit these commands for explicit Skill() invocation:
- `/ideate` - Check if skill invocation is explicit
- `/create-context` - Check if skill invocation is explicit
- `/create-epic` - Check if skill invocation is explicit
- `/brainstorm` - Check if skill invocation is explicit

**Testing:** For each command, verify Skill() appears with explicit syntax, not just "→ Skill →" summary.

**Effort Estimate:** 1 hour (15 min per command)

---

### MEDIUM Priority

#### REC-4: Add Pre-Flight Reminder to Epic Batch Workflow

**Problem Addressed:** Claude may still deviate even with explicit instructions

**File:** `.claude/commands/create-story.md`
**Location:** At start of Epic Batch Workflow section
**Change Type:** ADD

**Exact Text to Add:**
```markdown
**⚠️ WORKFLOW DISCIPLINE REMINDER:**
- Follow steps 1-5 IN ORDER
- DO NOT add preparatory analysis steps (like checking existing stories)
- DO NOT skip ahead or "optimize" the workflow
- The skill handles all complexity - your job is to invoke it
```

**Effort Estimate:** 10 minutes

---

## Implementation Checklist

- [ ] **REC-1 (CRITICAL):** Expand Epic Batch Workflow with explicit Skill() invocation: See STORY-354
  - [ ] Replace lines 46-67 with detailed step-by-step workflow
  - [ ] Add explicit `Skill(command="devforgeai-story-creation")` in Step 4.3
  - [ ] Add "DO NOT proceed with manual analysis" warning
  - [ ] Test with `/create-story epic-056`

- [ ] **REC-2 (HIGH):** Document Skill Invocation Checkpoint Pattern: See STORY-355
  - [ ] Add section to lean-orchestration-pattern.md
  - [ ] Include WRONG vs CORRECT examples

- [ ] **REC-3 (HIGH):** Audit other commands for similar pattern: See STORY-356
  - [ ] /ideate
  - [ ] /create-context
  - [ ] /create-epic
  - [ ] /brainstorm

- [ ] **REC-4 (MEDIUM):** Add workflow discipline reminder: Included in STORY-354
  - [ ] Add reminder box at start of Epic Batch Workflow

- [ ] Review this RCA for completeness
- [ ] Commit changes with reference to RCA-037
- [ ] Mark RCA as RESOLVED

---

## Prevention Strategy

### Short-term
- Add explicit `Skill(command="...")` invocations to all workflow modes in commands
- Use step numbering and MANDATORY markers consistently
- Add "DO NOT proceed with manual analysis" warnings

### Long-term
- Update lean-orchestration-pattern.md with explicit skill invocation pattern
- Create automated audit for commands to verify explicit skill invocation
- Consider adding pre-flight checkpoint that validates command understands it's delegating to skill

### Monitoring
- Watch for: Commands that describe skills but use summary language
- Audit for: Conversations where skill should have been invoked but wasn't
- Escalation: If skill invocation skipped, perform RCA to identify command gap

---

## Related RCAs

- **RCA-029:** Brainstorm Skill Bypass During Plan Mode - Similar pattern where skill was not invoked
- **RCA-022:** Mandatory TDD Phases Skipped - Similar workflow deviation pattern

---

## Status

**Status:** OPEN
**Resolution:** Pending implementation of recommendations

---

**RCA Created:** 2026-02-02
**RCA Number:** RCA-037
**RCA Title:** Skill Invocation Skipped Despite Orchestrator Instructions
