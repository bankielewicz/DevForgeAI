# DevForgeAI-Development Skill Refactoring Plan

**Date:** 2025-11-14
**Issue:** Progressive disclosure files not loading after Phase 1 completion
**Root Cause:** Missing explicit `Read()` instructions in SKILL.md Phases 1-5
**Solution:** Add explicit loading instructions following Phase 0 pattern

---

## Problem Analysis

### Current Behavior (BROKEN)

After Phase 1 (Red phase) completes, Claude proceeds to Phase 2 (Green phase) but does NOT load `tdd-green-phase.md`, resulting in incomplete implementation.

**Why it fails:**

```markdown
### Phase 2: Implementation (Green Phase)
Minimal code to pass tests → backend-architect/frontend-developer → Tests GREEN
**Reference:** `tdd-green-phase.md`
```

Claude interprets this as:
- ✅ "Invoke backend-architect/frontend-developer subagent"
- ❌ "Load tdd-green-phase.md file" (NOT INFERRED)

### Expected Behavior (FIXED)

```markdown
### Phase 2: Implementation (Green Phase)

**⚠️ NOW EXECUTE PHASE 2 - Load the reference file and follow its instructions:**

Read(file_path=".claude/skills/devforgeai-development/references/tdd-green-phase.md")

**After loading tdd-green-phase.md, execute its step-by-step workflow.**
```

Claude executes:
1. ✅ Loads tdd-green-phase.md via Read()
2. ✅ Sees detailed step-by-step instructions
3. ✅ Executes all steps in sequence
4. ✅ Completes Phase 2 correctly

---

## Refactoring Strategy

### Pattern to Apply

**From Phase 0 (Working):**
- Has execution trigger: "⚠️ EXECUTION STARTS HERE"
- Has imperative: "Execute these steps now:"
- Has clear directive: "See `references/file.md` for complete workflow"

**Enhanced Pattern (Explicit Read):**
- Add execution trigger: "⚠️ NOW EXECUTE PHASE X"
- Add explicit Read(): `Read(file_path=".claude/skills/.../file.md")`
- Add follow-up instruction: "After loading, execute its step-by-step workflow"
- Keep summary for context

### Sections to Refactor

1. **Phase 0:** Enhance existing pattern (add explicit Read)
2. **Phase 1:** Add explicit Read() for tdd-red-phase.md
3. **Phase 2:** Add explicit Read() for tdd-green-phase.md
4. **Phase 3:** Add explicit Read() for tdd-refactor-phase.md
5. **Phase 4:** Add explicit Read() for integration-testing.md
6. **Phase 4.5:** Add explicit Read() for phase-4.5-deferral-challenge.md
7. **Phase 5:** Add explicit Read() for 3 reference files (sequential loading)
8. **Reference Files List:** Update to clarify progressive loading

---

## Implementation Plan

### Step 1: Backup Current SKILL.md ✅
```bash
cp .claude/skills/devforgeai-development/SKILL.md \
   .claude/skills/devforgeai-development/SKILL.md.backup-20251114
```

### Step 2: Refactor Phase 0 Section (Lines 79-98)

**Current:**
```markdown
**See `references/preflight-validation.md` for complete workflow.**
```

**Enhanced:**
```markdown
**⚠️ NOW LOAD AND EXECUTE Phase 0 workflow:**

Read(file_path=".claude/skills/devforgeai-development/references/preflight-validation.md")

**After loading preflight-validation.md, execute its 10-step validation workflow.**
```

### Step 3: Refactor Phase 1 Section (Lines 104-106)

**Current:**
```markdown
### Phase 1: Test-First Design (Red Phase)
Write failing tests from AC → test-automator subagent → Tests RED
**Reference:** `tdd-red-phase.md`
```

**Refactored:**
```markdown
### Phase 1: Test-First Design (Red Phase)

**⚠️ NOW EXECUTE PHASE 1 - Load the reference file and follow its instructions:**

Read(file_path=".claude/skills/devforgeai-development/references/tdd-red-phase.md")

**After loading tdd-red-phase.md, execute its step-by-step workflow.**

**Summary:** Write failing tests from AC → test-automator subagent → Tests RED
**Expected outcome:** All tests RED (failing), ready for implementation

---
```

### Step 4: Refactor Phase 2 Section (Lines 108-110)

**Current:**
```markdown
### Phase 2: Implementation (Green Phase)
Minimal code to pass tests → backend-architect/frontend-developer → Tests GREEN
**Reference:** `tdd-green-phase.md`
```

**Refactored:**
```markdown
### Phase 2: Implementation (Green Phase)

**⚠️ NOW EXECUTE PHASE 2 - Load the reference file and follow its instructions:**

Read(file_path=".claude/skills/devforgeai-development/references/tdd-green-phase.md")

**After loading tdd-green-phase.md, execute its step-by-step workflow.**

**Summary:** Minimal code to pass tests → backend-architect/frontend-developer → Tests GREEN
**Expected outcome:** All tests GREEN (passing), ready for refactoring

---
```

### Step 5: Refactor Phase 3 Section (Lines 112-114)

**Current:**
```markdown
### Phase 3: Refactor (Refactor Phase)
Improve quality, keep tests green → refactoring-specialist, code-reviewer → Code improved
**Reference:** `tdd-refactor-phase.md`
```

**Refactored:**
```markdown
### Phase 3: Refactor (Refactor Phase)

**⚠️ NOW EXECUTE PHASE 3 - Load the reference file and follow its instructions:**

Read(file_path=".claude/skills/devforgeai-development/references/tdd-refactor-phase.md")

**After loading tdd-refactor-phase.md, execute its step-by-step workflow.**

**Summary:** Improve quality, keep tests green → refactoring-specialist, code-reviewer → Code improved
**Expected outcome:** Code improved, tests still GREEN, no anti-patterns

---
```

### Step 6: Refactor Phase 4 Section (Lines 116-118)

**Current:**
```markdown
### Phase 4: Integration & Validation
Cross-component testing, coverage validation → integration-tester → Thresholds met
**Reference:** `integration-testing.md`
```

**Refactored:**
```markdown
### Phase 4: Integration & Validation

**⚠️ NOW EXECUTE PHASE 4 - Load the reference file and follow its instructions:**

Read(file_path=".claude/skills/devforgeai-development/references/integration-testing.md")

**After loading integration-testing.md, execute its step-by-step workflow.**

**Summary:** Cross-component testing, coverage validation → integration-tester → Thresholds met
**Expected outcome:** Integration tests pass, coverage ≥ thresholds (95%/85%/80%)

---
```

### Step 7: Refactor Phase 4.5 Section (Lines 120-123)

**Current:**
```markdown
### Phase 4.5: Deferral Challenge Checkpoint (NEW - RCA-006)
Challenge ALL deferrals (pre-existing + new) → deferral-validator → User approval required
**Reference:** `phase-4.5-deferral-challenge.md`
**Purpose:** Prevent autonomous deferrals, enforce "Attempt First, Defer Only If Blocked" pattern
```

**Refactored:**
```markdown
### Phase 4.5: Deferral Challenge Checkpoint (NEW - RCA-006)

**⚠️ NOW EXECUTE PHASE 4.5 - Load the reference file and follow its instructions:**

Read(file_path=".claude/skills/devforgeai-development/references/phase-4.5-deferral-challenge.md")

**After loading phase-4.5-deferral-challenge.md, execute its step-by-step workflow.**

**Summary:** Challenge ALL deferrals (pre-existing + new) → deferral-validator → User approval required
**Purpose:** Prevent autonomous deferrals, enforce "Attempt First, Defer Only If Blocked" pattern
**Expected outcome:** Zero autonomous deferrals, all deferrals have user approval + valid references

---
```

### Step 8: Refactor Phase 5 Section (Lines 125-128)

**Current:**
```markdown
### Phase 5: Git Workflow & DoD Validation
Budget enforcement → Handle incomplete items → Git commit → Story complete
**References:** `deferral-budget-enforcement.md`, `git-workflow-conventions.md`, `dod-validation-checkpoint.md`
**Steps:** 1.6 Budget enforcement, 1.7 Handle new incomplete items, 2.0+ Git commit
```

**Refactored:**
```markdown
### Phase 5: Git Workflow & DoD Validation

**⚠️ NOW EXECUTE PHASE 5 - Load reference files in sequence:**

**Step 1: Load budget enforcement workflow:**

Read(file_path=".claude/skills/devforgeai-development/references/deferral-budget-enforcement.md")

**After loading, execute Phase 5 Step 1.6 (Budget Enforcement).**

**Step 2: Load DoD validation checkpoint:**

Read(file_path=".claude/skills/devforgeai-development/references/dod-validation-checkpoint.md")

**After loading, execute Phase 5 Step 1.7 (Handle New Incomplete Items).**

**Step 3: Load git workflow conventions:**

Read(file_path=".claude/skills/devforgeai-development/references/git-workflow-conventions.md")

**After loading, execute Phase 5 Step 2.0+ (Git Commit or File-Based Tracking).**

**Summary:** Budget enforcement → Handle incomplete items → Git commit → Story complete
**Expected outcome:** Changes committed (or file-tracked), story status = "Dev Complete"

---
```

### Step 9: Update Reference Files List Section (Lines 164-189)

**Current:**
```markdown
## Reference Files

Load these on-demand during workflow execution:
```

**Refactored:**
```markdown
## Reference Files

**These files are loaded AUTOMATICALLY during workflow execution via explicit Read() instructions in each phase.**

You will load these files using Read() commands as you progress through the workflow:
```

### Step 10: Add TDD Patterns Reference Note (After Phase 5)

**Add:**
```markdown
---

### Additional Reference: Comprehensive TDD Patterns

**For overarching TDD guidance across all phases, optionally reference:**

Read(file_path=".claude/skills/devforgeai-development/references/tdd-patterns.md")

**Use this file when you need:**
- Cross-phase TDD patterns and best practices
- Deeper understanding of TDD principles
- Pattern recognition for code smells
- Test design patterns (AAA, Given/When/Then, etc.)
```

---

## Verification Steps

### 1. File Path Verification
```bash
# Verify all reference files exist
ls -la .claude/skills/devforgeai-development/references/
```

Expected files:
- ✅ preflight-validation.md
- ✅ tdd-red-phase.md
- ✅ tdd-green-phase.md
- ✅ tdd-refactor-phase.md
- ✅ integration-testing.md
- ✅ phase-4.5-deferral-challenge.md
- ✅ deferral-budget-enforcement.md
- ✅ dod-validation-checkpoint.md
- ✅ git-workflow-conventions.md
- ✅ tdd-patterns.md

### 2. Line Count Check
```bash
# Before refactoring
wc -l .claude/skills/devforgeai-development/SKILL.md

# After refactoring (should increase by ~50-70 lines)
wc -l .claude/skills/devforgeai-development/SKILL.md
```

### 3. Pattern Consistency Check

Verify each phase has:
- ✅ "⚠️ NOW EXECUTE PHASE X" heading
- ✅ `Read(file_path="...")` instruction
- ✅ "After loading...execute its workflow" directive
- ✅ Summary line (for context)
- ✅ Expected outcome statement
- ✅ Separator line (`---`)

---

## Success Criteria

### Functional Requirements
- [ ] Phase 0 has explicit Read() for preflight-validation.md
- [ ] Phase 1 has explicit Read() for tdd-red-phase.md
- [ ] Phase 2 has explicit Read() for tdd-green-phase.md
- [ ] Phase 3 has explicit Read() for tdd-refactor-phase.md
- [ ] Phase 4 has explicit Read() for integration-testing.md
- [ ] Phase 4.5 has explicit Read() for phase-4.5-deferral-challenge.md
- [ ] Phase 5 has explicit Read() for 3 sequential files
- [ ] All file paths are absolute and correct
- [ ] Pattern is consistent across all phases

### Quality Requirements
- [ ] No ambiguity in execution flow
- [ ] Clear imperative instructions ("NOW EXECUTE")
- [ ] Explicit tool calls (Read()) not implied
- [ ] Expected outcomes documented
- [ ] Summaries preserved for context

### Testing Requirements
- [ ] Test workflow execution with sample story
- [ ] Verify Phase 2 loads tdd-green-phase.md correctly
- [ ] Verify all 6 phases load their reference files
- [ ] Confirm no regression in Phase 0 behavior

---

## Rollback Plan

If refactoring causes issues:

```bash
# Restore original SKILL.md
cp .claude/skills/devforgeai-development/SKILL.md.backup-20251114 \
   .claude/skills/devforgeai-development/SKILL.md

# Restart Claude Code terminal
# Re-test workflow
```

---

## Timeline Estimate

- **Backup:** 1 minute
- **Refactor Phases 0-5:** 15 minutes
- **Update Reference Files section:** 3 minutes
- **Verification:** 5 minutes
- **Testing:** 10 minutes
- **Documentation:** 5 minutes

**Total:** ~40 minutes

---

## Related Documentation

- Root Cause Analysis: In-conversation analysis (2025-11-14)
- Anthropic Skills Documentation: https://www.claude.com/blog/skills
- Progressive Disclosure Pattern: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

---

**This refactoring eliminates inference requirements and makes progressive disclosure explicit and deterministic.**
