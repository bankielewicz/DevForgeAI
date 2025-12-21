# RCA-016 REC-3 Implementation Plan: Pattern Recognition Guide

**Created:** 2025-12-01
**Purpose:** Executable plan for adding Progressive Disclosure Phase Skipping pattern to skill-execution-troubleshooting.md
**Related RCA:** RCA-016-qa-skill-phase-skipping-during-deep-validation.md
**Recommendation:** REC-3 (HIGH) - Create RCA-009 Pattern Recognition Guide
**Status:** READY FOR EXECUTION
**Prerequisites:**
- REC-1 (CRITICAL) - COMPLETE (Commit 3654474)
- REC-2 (HIGH) - COMPLETE (Commit 0d6744f)

---

## Executive Summary

This document provides a complete, context-rich implementation plan for REC-3 that can be executed in a fresh terminal session without requiring prior context.

**Problem Solved:** Progressive disclosure phase skipping pattern recurs across multiple skills (RCA-009, RCA-011, RCA-016) but no cross-skill documentation exists to help Claude recognize and prevent it.

**Solution:** Add new section to existing `.claude/memory/skill-execution-troubleshooting.md` documenting:
- Pattern symptoms
- Detection checklist
- Recovery procedure
- Prevention strategies
- Affected skills list
- Related RCAs

---

## Current State Analysis (As of 2025-12-01)

### Existing File: `.claude/memory/skill-execution-troubleshooting.md`

**Current content (355 lines):** Focuses on **Skill vs Task tool confusion** pattern:
- Symptom: Invoking skill then waiting passively
- Root cause: Confusing Skill tool (inline) with Task tool (isolated)
- Recovery: Resume execution immediately
- Prevention: Mental model correction

**What's Missing:** The **Progressive Disclosure Phase Skipping** pattern:
- Symptom: Executing skill but skipping phases (jumping from Phase 1 to Phase 5)
- Root cause: Reference files not loaded, Claude thinks phase names are self-explanatory
- Recovery: Load reference files, execute missing steps
- Prevention: Check for CHECKPOINT markers, verify reference loading

### Gap Analysis

| Pattern | Currently Documented | REC-3 Will Add |
|---------|---------------------|----------------|
| Skill vs Task confusion (wait after invoke) | ✅ Yes (lines 1-355) | N/A |
| Progressive Disclosure Phase Skipping | ❌ No | ✅ New section |
| Detection checklists | ✅ For waiting pattern | ✅ For skipping pattern |
| Recovery procedures | ✅ For waiting pattern | ✅ For skipping pattern |
| Related RCAs cross-reference | ❌ No | ✅ RCA-009, 011, 016 |

---

## Evidence Base: The Pattern

### Pattern Occurrences

**RCA-009 (2025-11-14):** devforgeai-development skill
- Skipped Tech Spec Coverage step in Phase 2
- Reference file mentioned but not loaded
- User caught issue

**RCA-011 (2025-11-19):** devforgeai-development skill
- Skipped mandatory TDD phases
- Progressive disclosure pattern identified as root cause
- Recommendations partially implemented

**RCA-016 (2025-12-01):** devforgeai-qa skill
- Skipped Phases 2, 3, 4, 6, 7 (jumped from Phase 1 to Phase 5)
- Reference files mentioned but not loaded
- anti-pattern-scanner hallucinated violations (didn't read actual files)
- User asked "did you skip any phases?" to catch issue

### Common Symptoms

1. Skill phases listed but not fully executed
2. Reference files mentioned in SKILL.md but not Read()
3. Subagents documented as MANDATORY but not invoked
4. Workflow completes "too quickly" (Deep QA in 3 min instead of 10 min)
5. User asks "did you skip phases?" or "did you follow 100%?"
6. Results don't match expected detail level

### Root Cause (Validated)

Phase summaries in SKILL.md appear complete but actually require loading reference files to see full workflow. Claude sees phase name (e.g., "Phase 2: Anti-Pattern Detection") and thinks "I know what that means" without:
1. Loading the reference file
2. Executing the documented workflow steps
3. Invoking mandatory subagents with proper context

---

## Implementation Plan

### File to Modify

**File:** `.claude/memory/skill-execution-troubleshooting.md`
**Current lines:** 355
**Expected after:** ~480 lines (+125 lines)
**Action:** ADD new section (do not replace existing content)

### Section to Add

**Insert Location:** After line 355 (end of current file, before any closing content)

**New Section Title:** `## Pattern: Progressive Disclosure Phase Skipping`

---

## Content to Add (Copy-Paste Ready)

```markdown

---

## Pattern: Progressive Disclosure Phase Skipping

**Pattern ID:** RCA-009 / RCA-011 / RCA-016
**Severity:** HIGH
**Frequency:** Recurring across skills with progressive disclosure
**First Documented:** 2025-11-14
**Most Recent:** 2025-12-01

---

### What Is This Pattern?

**Problem:** You execute a skill's workflow but skip phases by not loading reference files.

**Example:**
```
Phase 0.9: AC-DoD Traceability ✅ Executed
Phase 1: Test Coverage ✅ Executed
Phase 2: Anti-Pattern Detection ❌ SKIPPED (jumped to Phase 5)
Phase 3: Spec Compliance ❌ SKIPPED
Phase 4: Code Quality ❌ SKIPPED
Phase 5: Report Generation ✅ Executed (but with incomplete data)
Phase 6: Feedback Hooks ❌ SKIPPED
Phase 7: Story Update ❌ SKIPPED
```

**Root Cause:** Phase summaries in SKILL.md appear self-explanatory, but the actual workflow steps are in reference files. You see "Phase 2: Anti-Pattern Detection" and think "I know what that means" without loading the 6-step workflow from the reference file.

---

### Symptoms (How to Detect)

**Watch for these warning signs:**

1. **Workflow completes too quickly**
   - Deep QA should take ~10-12 minutes, not 3 minutes
   - TDD cycle should take ~30 minutes, not 5 minutes
   - If you're "done" suspiciously fast, you likely skipped phases

2. **Reference files not loaded**
   - SKILL.md says "**Ref:** `references/workflow-name.md`"
   - But you didn't `Read(file_path="...")` that file
   - You executed based on phase title alone

3. **Subagents not invoked**
   - SKILL.md says "**Subagent:** agent-name (MANDATORY)"
   - But you didn't `Task(subagent_type="agent-name", ...)`
   - You made assumptions instead of following documented workflow

4. **Results lack expected detail**
   - Anti-pattern scan returns no violations (but you didn't read actual code files)
   - Coverage analysis has no layer breakdown (skipped classification step)
   - Spec compliance has no traceability matrix (skipped generation step)

5. **User questions completeness**
   - "Did you skip any phases?"
   - "Did you follow 100%?"
   - "Why didn't you invoke the subagent?"
   - If user has to ask, you likely skipped something

---

### Detection Checklist

**Run this checklist if you suspect phase skipping:**

- [ ] **Reference files:** Did I `Read()` every reference file mentioned in SKILL.md phases?
- [ ] **Subagent invocations:** Did I `Task()` every MANDATORY subagent listed?
- [ ] **Phase count:** Did I execute ALL phases (not just some)?
- [ ] **Execution time:** Is elapsed time reasonable for workflow complexity?
- [ ] **Result detail:** Do results have expected granularity (layer breakdown, violation counts, traceability matrix)?
- [ ] **Checkpoint markers:** Did I see and respond to every "⚠️ CHECKPOINT" in SKILL.md?
- [ ] **Completion checklists:** Did I verify every checkbox before proceeding to next phase?

**If ANY checkbox is unchecked:** You likely skipped phases. See Recovery Procedure below.

---

### Recovery Procedure

**If you catch yourself (or user points out) skipping phases:**

#### Step 1: Acknowledge the Gap

```
"You're right - I executed phases [X, Y] but skipped phases [A, B, C, D].
I proceeded based on phase titles without loading the reference files
that contain the actual workflow steps."
```

#### Step 2: Identify What Was Skipped

List specifically:
- Which phases were skipped
- Which reference files were not loaded
- Which subagents were not invoked

Example:
```
Skipped phases:
- Phase 2: Anti-Pattern Detection (did not load anti-pattern-detection-workflow.md)
- Phase 3: Spec Compliance (did not load spec-compliance-workflow.md, did not invoke deferral-validator)
- Phase 4: Code Quality (did not load code-quality-workflow.md)
- Phase 6: Feedback Hooks (did not load feedback-hooks-workflow.md)
- Phase 7: Story Update (did not load story-update-workflow.md)
```

#### Step 3: Load Missing Reference Files

```
Read(file_path=".claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/spec-compliance-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/code-quality-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/story-update-workflow.md")
```

#### Step 4: Execute Skipped Phases

For each skipped phase:
1. Read the reference file's workflow steps
2. Execute EACH step in order
3. Invoke any MANDATORY subagents
4. Verify completion checklist before proceeding
5. Display phase completion to user

#### Step 5: Update Results

Integrate newly collected data into final results:
- Add violation counts from anti-pattern scan
- Add compliance status from spec validation
- Add quality metrics from code analysis
- Update overall QA result based on all phases

#### Step 6: Verify Completeness

Display completion checklist showing ALL phases executed:
```
✓ Phase 0.9: AC-DoD Traceability (100% score)
✓ Phase 1: Test Coverage (85% overall)
✓ Phase 2: Anti-Pattern Detection (0 CRITICAL, 2 MEDIUM)
✓ Phase 3: Spec Compliance (8/8 AC validated)
✓ Phase 4: Code Quality (MI: 78, Complexity: avg 4.2)
✓ Phase 5: Report Generated
✓ Phase 6: Feedback Hooks (triggered)
✓ Phase 7: Story Updated to QA Approved
```

---

### Prevention Strategies

**Before executing any skill phase:**

#### Strategy 1: Check for CHECKPOINT Markers

Look for `⚠️ CHECKPOINT` in SKILL.md. These mark phases requiring reference loading.

Example:
```markdown
### Phase 2: Anti-Pattern Detection

**⚠️ CHECKPOINT: You MUST load the reference file and execute ALL steps before proceeding**

**Step 2.0: Load Workflow Reference (REQUIRED)**
Read(file_path=".claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md")
```

**If you see a CHECKPOINT:** You MUST load the reference file. No exceptions.

#### Strategy 2: Verify Reference Loading

Before claiming a phase complete, ask yourself:
- Did I `Read()` the reference file for this phase?
- Did I see the workflow steps from that file?
- Did I execute EACH step, not just the phase title?

#### Strategy 3: Use Phase Completion Checklists

Each phase should have a completion checklist. Verify EVERY checkbox before proceeding.

Example:
```markdown
**Phase 2 Completion Checklist:**
- [ ] Loaded anti-pattern-detection-workflow.md (Step 2.0)
- [ ] Step 1: Loaded ALL 6 context files
- [ ] Step 2: Invoked anti-pattern-scanner subagent
- [ ] Step 3: Parsed JSON response
- [ ] Step 4: Updated blocks_qa state
- [ ] Step 5: Displayed violations summary
- [ ] Step 6: Stored violations for report
```

**IF any checkbox is unchecked:** HALT and complete missing steps.

#### Strategy 4: Display Loading Confirmation

When you load a reference file, explicitly confirm:
```
Loading reference: anti-pattern-detection-workflow.md
Found 6 workflow steps. Executing steps 1-6...
```

This creates a visible trail showing reference files were actually loaded.

#### Strategy 5: Track Execution Time

Be suspicious if workflow completes very quickly:
- Deep QA: Expect ~10-12 minutes
- TDD Development: Expect ~30 minutes
- Light QA: Expect ~3-5 minutes

If done much faster, verify you didn't skip phases.

---

### Affected Skills

**Skills with progressive disclosure that may exhibit this pattern:**

| Skill | Reference Files | Risk Level |
|-------|-----------------|------------|
| devforgeai-development | 8 reference files | HIGH (RCA-009, RCA-011) |
| devforgeai-qa | 19 reference files | HIGH (RCA-016) |
| devforgeai-orchestration | 4 reference files | MEDIUM |
| devforgeai-release | 5 reference files | MEDIUM |
| devforgeai-architecture | 6 reference files | MEDIUM |
| devforgeai-ideation | 16 reference files | MEDIUM |
| devforgeai-story-creation | 6 reference files | MEDIUM |
| devforgeai-documentation | 7 reference files | LOW |

**High-risk indicators:**
- More reference files = more phases to potentially skip
- MANDATORY subagents = more invocations to potentially miss
- Complex workflows = more opportunities for shortcuts

---

### Related RCAs

**RCA-009: Incomplete Skill Workflow Execution (2025-11-14)**
- Skill: devforgeai-development
- Symptom: Skipped Tech Spec Coverage step in Phase 2
- Root cause: Progressive disclosure - reference file not loaded
- Status: Partially resolved

**RCA-011: Mandatory TDD Phase Skipping (2025-11-19)**
- Skill: devforgeai-development
- Symptom: Skipped mandatory TDD phases
- Root cause: Same as RCA-009 - progressive disclosure ambiguity
- Status: Recommendations pending

**RCA-016: QA Skill Phase Skipping During Deep Validation (2025-12-01)**
- Skill: devforgeai-qa
- Symptom: Skipped 5 phases (2, 3, 4, 6, 7), jumped from Phase 1 to Phase 5
- Root cause: Same pattern - reference files not loaded
- Status: REC-1 COMPLETE, REC-2 COMPLETE, REC-3 IN PROGRESS

**Pattern frequency:** 3 incidents in 3 weeks (HIGH recurrence rate)

---

### Success Criteria

After implementing prevention strategies, verify:

- ✅ All reference files loaded (visible `Read()` calls in conversation)
- ✅ All workflow steps executed (not just phase titles)
- ✅ All MANDATORY subagents invoked
- ✅ Completion checklists verified before phase transitions
- ✅ Expected execution time achieved
- ✅ User does NOT need to question completeness

---

### Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  PROGRESSIVE DISCLOSURE PHASE SKIPPING - QUICK CHECK        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BEFORE each phase:                                         │
│  □ Look for ⚠️ CHECKPOINT marker                            │
│  □ Read() the reference file if indicated                   │
│  □ Note the workflow step count (e.g., "6 steps")           │
│                                                             │
│  DURING phase execution:                                    │
│  □ Execute EACH step from reference file                    │
│  □ Invoke MANDATORY subagents with Task()                   │
│  □ Display step completion as you work                      │
│                                                             │
│  AFTER each phase:                                          │
│  □ Verify completion checklist (ALL boxes checked)          │
│  □ Display "Phase X Complete" summary                       │
│  □ Only THEN proceed to next phase                          │
│                                                             │
│  WARNING SIGNS:                                             │
│  ⚠ Workflow completing too fast                            │
│  ⚠ No Read() calls for reference files                     │
│  ⚠ No Task() calls for MANDATORY subagents                 │
│  ⚠ Results lacking expected detail                         │
│  ⚠ User asking "did you skip phases?"                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Difference from "Waiting After Invoke" Pattern

**Two distinct patterns exist. Don't confuse them:**

| Aspect | Waiting After Invoke | Phase Skipping |
|--------|---------------------|----------------|
| **When it occurs** | Immediately after `Skill()` | During skill execution |
| **Symptom** | Stop and wait passively | Execute but skip phases |
| **What you do wrong** | Nothing (waiting) | Partial execution |
| **Reference files** | N/A (never started) | Not loaded |
| **Recovery** | Start executing Phase 0 | Load refs, execute missing phases |
| **Related RCAs** | RCA-009 (original) | RCA-009, RCA-011, RCA-016 |

**Both patterns can occur in same session:**
1. First, you might wait after skill invocation (Pattern 1)
2. After resuming, you might skip phases (Pattern 2)

**Check for BOTH patterns when troubleshooting skill execution issues.**
```

---

## Execution Instructions

### Pre-Execution Checklist

```
- [ ] Read current file: Read(file_path=".claude/memory/skill-execution-troubleshooting.md")
- [ ] Verify file ends around line 355 with "## Remember" section
- [ ] Create backup: Bash(command="cp .claude/memory/skill-execution-troubleshooting.md .claude/memory/skill-execution-troubleshooting.md.rec3-backup")
- [ ] Note current line count for verification
```

### Execution Steps

**Step 1:** Read current file to confirm structure

**Step 2:** Create backup

**Step 3:** Append new section using Edit tool
- Find the last line of the file
- Add the new "Pattern: Progressive Disclosure Phase Skipping" section
- Preserve all existing content

**Step 4:** Verify the addition
- Count total lines (should be ~480)
- Grep for "Progressive Disclosure Phase Skipping" (should find 1 match)
- Grep for "RCA-016" in the file (should find multiple matches)

**Step 5:** Update CLAUDE.md references (if needed)
- Check if skill-execution-troubleshooting.md is already referenced
- If not, add reference in appropriate section

**Step 6:** Update RCA-016 status
- Mark REC-3 as COMPLETE in implementation checklist
- Add implementation record

### Post-Execution Verification

```bash
# Verify file size
wc -l .claude/memory/skill-execution-troubleshooting.md
# Expected: ~480 lines (was 355)

# Verify new section exists
grep -c "Progressive Disclosure Phase Skipping" .claude/memory/skill-execution-troubleshooting.md
# Expected: 1 (or more if mentioned in quick reference)

# Verify RCA cross-references
grep -c "RCA-016" .claude/memory/skill-execution-troubleshooting.md
# Expected: 3+ mentions

# Verify detection checklist exists
grep -c "Detection Checklist" .claude/memory/skill-execution-troubleshooting.md
# Expected: 1

# Verify recovery procedure exists
grep -c "Recovery Procedure" .claude/memory/skill-execution-troubleshooting.md
# Expected: 1
```

---

## Git Commit Message

```
docs(RCA-016): Add Progressive Disclosure Phase Skipping pattern guide (REC-3)

- Add new section to skill-execution-troubleshooting.md (~125 lines)
- Document pattern symptoms (5 warning signs)
- Add detection checklist (7 verification items)
- Add 6-step recovery procedure
- Add 5 prevention strategies
- List affected skills with risk levels (8 skills)
- Cross-reference RCA-009, RCA-011, RCA-016
- Add quick reference card for at-a-glance checking
- Differentiate from "Waiting After Invoke" pattern

RCA: RCA-016 (QA Skill Phase Skipping During Deep Validation)
Recommendation: REC-3 (HIGH) - Create Pattern Recognition Guide
Prerequisites: REC-1 (CRITICAL), REC-2 (HIGH) - Both COMPLETE

File modified: .claude/memory/skill-execution-troubleshooting.md
Lines added: ~125 (355 → ~480)
```

---

## Rollback Procedure

```bash
# If implementation fails, restore from backup
cp .claude/memory/skill-execution-troubleshooting.md.rec3-backup .claude/memory/skill-execution-troubleshooting.md

# Verify restoration
diff .claude/memory/skill-execution-troubleshooting.md .claude/memory/skill-execution-troubleshooting.md.rec3-backup
# Should show no differences
```

---

## Expected Outcomes

### Before REC-3
- 1 pattern documented (Waiting After Invoke)
- No cross-skill pattern recognition
- No detection checklist for phase skipping
- No recovery procedure for phase skipping
- File size: 355 lines

### After REC-3
- 2 patterns documented (Waiting + Phase Skipping)
- Cross-skill pattern recognition with 8 affected skills listed
- Detection checklist with 7 verification items
- 6-step recovery procedure
- 5 prevention strategies
- Quick reference card
- RCA cross-references (009, 011, 016)
- File size: ~480 lines

### Metrics
- **Patterns documented:** 1 → 2 (100% increase)
- **Detection checklist items:** 0 → 7 (new)
- **Recovery steps:** 0 → 6 (new for this pattern)
- **Prevention strategies:** 0 → 5 (new)
- **RCA cross-references:** 0 → 3 (new)
- **Skills coverage:** Framework-wide (8 skills listed)

---

## Session Resume Instructions

To resume this plan in a new terminal session:

1. **Read this plan:**
```
Read(file_path="devforgeai/RCA/RCA-016-REC3-PATTERN-RECOGNITION-GUIDE-PLAN.md")
```

2. **Read current troubleshooting file:**
```
Read(file_path=".claude/memory/skill-execution-troubleshooting.md")
```

3. **Create backup:**
```
Bash(command="cp .claude/memory/skill-execution-troubleshooting.md .claude/memory/skill-execution-troubleshooting.md.rec3-backup")
```

4. **Append new section** (content is in "Content to Add" section above)

5. **Run verification commands**

6. **Commit changes**

---

## Checkpoint Summary

| Checkpoint | Description | Verification |
|------------|-------------|--------------|
| CP-1 | Plan document created | File exists at `devforgeai/RCA/RCA-016-REC3-PATTERN-RECOGNITION-GUIDE-PLAN.md` |
| CP-2 | Backup created | File exists at `.claude/memory/skill-execution-troubleshooting.md.rec3-backup` |
| CP-3 | New section appended | `grep "Progressive Disclosure Phase Skipping"` returns match |
| CP-4 | Detection checklist added | `grep "Detection Checklist"` returns match |
| CP-5 | Recovery procedure added | `grep "Recovery Procedure"` returns match |
| CP-6 | Prevention strategies added | `grep "Prevention Strategies"` returns match |
| CP-7 | RCA cross-references added | `grep -c "RCA-016"` returns 3+ |
| CP-8 | Quick reference card added | `grep "QUICK CHECK"` returns match |
| CP-9 | File size verified | `wc -l` returns ~480 |
| CP-10 | Git commit successful | Commit hash recorded |

---

**Document Complete - Ready for Execution**
