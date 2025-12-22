# STORY-050 Implementation Plan

**Story:** Refactor /audit-deferrals command for budget compliance
**Date Created:** 2025-11-17
**Phase:** Phase 1 Complete (Tests Generated)
**Next Phase:** Phase 2 (Implementation)
**Estimated Duration:** 5-6 hours

---

## Executive Summary

STORY-050 is about refactoring the `/audit-deferrals` command to follow the lean orchestration pattern. This requires extracting business logic from the command (currently 31,300 chars) to the devforgeai-orchestration skill, reducing the command to <12,000 chars while preserving 100% functionality.

**Key Metrics:**
- Current: 31,300 chars (208% over 15K limit)
- Target: 8-10K chars (53-67% of 15K)
- Reduction: 57% character reduction
- Reference: /qa command (295 lines, 7.2K chars) - primary template

---

## Refactoring Approach

### Phase Overview

```
Phase 1 (RED): ✅ COMPLETE
  - 35 tests generated (12 failing, 23 passing)
  - All 5 ACs + 13 tech spec requirements covered
  - Tests clearly show what needs to be implemented

Phase 2 (GREEN): Implementation
  - Analyze current command structure
  - Enhance devforgeai-orchestration skill with Phase 7
  - Refactor command to delegate Phase 6 to skill
  - Reduce command from 31K → <12K chars
  - Verify tests pass

Phase 3 (REFACTOR): Code Quality
  - Improve code organization
  - Add comprehensive documentation
  - Optimize for readability

Phase 4 (INTEGRATION): Validation
  - Run all 35 tests (expect 100% pass)
  - Verify STORY-033 tests identical (84 tests)
  - Performance benchmark (±10% baseline)

Phase 5 (GIT): Commit & Complete
  - Git commit implementation
  - Update story status to "Dev Complete"
  - Document workflow history
```

---

## Phase 2: Green Phase (Implementation)

### Step 1: Backup Current Command

```bash
cp .claude/commands/audit-deferrals.md .claude/commands/audit-deferrals.md.backup
git status  # Verify backup created
```

**Verification:** File exists and is readable

---

### Step 2: Analyze Current Command Structure

**Current File:** `.claude/commands/audit-deferrals.md` (31,300 chars)

**Analysis needed:**

1. **Count current phases:**
   ```bash
   grep "^### Phase " .claude/commands/audit-deferrals.md | wc -l
   # Expected: 6 phases (1-6)
   ```

2. **Identify Phase 6 logic:**
   ```bash
   sed -n '/^### Phase 6/,/^### Phase/p' .claude/commands/audit-deferrals.md | head -50
   # Extract: Hook eligibility, context prep, sanitization, invocation, logging, error handling, circular prevention
   ```

3. **Document Phase 6 structure:**
   - Substep 1: Eligibility check
   - Substep 2: Context preparation
   - Substep 3: Sanitization
   - Substep 4: Hook invocation
   - Substep 5: Logging
   - Substep 6: Error handling
   - Substep 7: Circular prevention

4. **Identify command vs skill responsibility:**
   - **Command should have:** Phase 0 (args), Phase 1 (context markers), Phase 2 (invoke skill), Phase 3 (display results)
   - **Skill should have:** All validation, orchestration, Phase 6 hook logic

---

### Step 3: Enhance devforgeai-orchestration Skill with Phase 7

**File:** `.claude/skills/devforgeai-orchestration/SKILL.md` (currently 3,249 lines)

**Add Phase 7: Hook Integration for Audit Deferrals**

Location: After Phase 6 in skill (after orchestration modes)

**Phase 7 Structure:**

```markdown
## Phase 7: Hook Integration for Audit Deferrals

**Purpose:** Execute hook eligibility check and conditional invocation for /audit-deferrals command

**Invoked by:** /audit-deferrals command Phase 2 → devforgeai-orchestration skill

**7 Substeps:**

### 7.1: Eligibility Check
- Check if deferral-audit mode enabled
- Check if hooks.yaml configured
- Determine if hooks eligible
- Return: eligible (true/false), reason

### 7.2: Context Preparation
- Extract STORY-IDs from audit
- Prepare audit metadata
- Gather hook context (operation, story, status)
- Return: context object

### 7.3: Sanitization
- Remove sensitive data
- Validate audit data integrity
- Prepare for hook consumption
- Return: sanitized context

### 7.4: Hook Invocation
- Call devforgeai invoke-hooks
- Pass prepared context
- Handle async completion
- Return: invocation result

### 7.5: Logging
- Log hook invocation (timestamp, result)
- Record hook response
- Append to devforgeai/feedback/logs/hook-invocations.log
- Return: log entry

### 7.6: Error Handling
- Catch hook failures gracefully
- Don't block audit workflow
- Log errors for diagnostics
- Return: error status (0 = success, 1 = graceful failure)

### 7.7: Circular Prevention
- Check for circular hook invocations
- Detect infinite loops
- Break circular dependency chains
- Return: circular prevention status
```

**File location:** Add after current Phase 6 (orchestration modes)

**Lines to add:** ~400 lines (including substep documentation)

**Expected skill size after Phase 7:** ~3,600 lines (currently 3,249 + ~350)
- Target: Stay <3,500 lines
- Mitigation: If >3,500, use progressive disclosure (extract Phase 7 to reference file)

---

### Step 4: Refactor /audit-deferrals Command

**Current file:** `.claude/commands/audit-deferrals.md` (31,300 chars, ~1,100 lines, 6 phases)

**Target:** <12,000 chars (~250-300 lines, 3-4 phases)

**Structure after refactoring:**

```markdown
# /audit-deferrals - Audit deferred work in stories

**Purpose:** Audit deferred work, identify circular chains, validate deferral justifications

---

## Phase 0: Argument Validation

**Step 1:** Validate optional arguments (none required for this command)

**Step 2:** Set context markers (optional: story filter, severity filter)

---

## Phase 1: Set Context and Invoke Skill

**Step 1:** Provide context markers for skill

```
**Command:** audit-deferrals
**Mode:** full-audit
```

**Step 2:** Invoke skill

```
Skill(command="devforgeai-orchestration")
```

---

## Phase 2: Display Results

Display skill output (audit report summary)

---

## Phase 3: Next Steps

Display recommendations from audit

---

[Integration notes, examples, etc.]
```

**Reduction strategy:**

1. **Remove Phase 1-5 implementation logic** (currently ~400 lines)
   - Move to skill
   - Command only delegates

2. **Remove display templates** (currently ~150 lines)
   - Skill generates appropriate display
   - Command just outputs result

3. **Remove error handling matrix** (currently ~100 lines)
   - Minimal error display (20-30 lines)
   - Skill communicates details

4. **Consolidate documentation** (currently ~300 lines)
   - Keep essential integration notes
   - External reference for detailed info

5. **Remove Phase 6 hook logic** (currently ~200 lines)
   - Move entirely to skill Phase 7
   - Command just invokes skill

**Expected result:** ~250-300 lines, ~8-10K chars

---

### Step 5: Create/Update Reference Files (if needed)

**If skill Phase 7 implementation >300 lines:**

Create: `.claude/skills/devforgeai-orchestration/references/audit-deferrals-hook-integration.md`

**Contents:**
- Phase 7 detailed workflow
- All 7 substeps with examples
- Error scenarios and handling
- Testing procedures

**Load on-demand:** Skill loads reference file only when Phase 7 executes (progressive disclosure)

---

### Step 6: Verify Tests Pass

**Run all tests:**

```bash
pytest tests/unit/test_story050_budget_compliance.py \
        tests/integration/test_story050_functionality.py -v
```

**Expected results after Phase 2:**

- ✅ `test_command_character_count_under_limit` - PASS (8-10K < 12K)
- ✅ `test_command_character_count_buffer` - PASS (8-10K < 15K)
- ✅ `test_command_has_three_phases` - PASS (3-4 phases)
- ✅ `test_command_delegates_to_skill` - PASS (Skill() call exists)
- ✅ `test_command_no_business_logic` - PASS (<100 lines logic)
- ✅ `test_no_hook_logic_in_command` - PASS (no hook code in command)
- ✅ `test_skill_phase_7_has_seven_substeps` - PASS (all 7 documented)
- ✅ `test_all_seven_phase_6_substeps_documented` - PASS (substeps present)
- ✅ All 35 tests PASS (23 currently passing + 12 after implementation)

**Failing tests → Passing tests:**

| Test | Before | After |
|------|--------|-------|
| test_command_character_count_under_limit | ❌ FAIL (30K) | ✅ PASS (8-10K) |
| test_command_character_count_buffer | ❌ FAIL (30K > 15K) | ✅ PASS (<15K) |
| test_command_has_three_phases | ❌ FAIL (6 phases) | ✅ PASS (3-4 phases) |
| test_command_delegates_to_skill | ❌ FAIL (no Skill()) | ✅ PASS (Skill() added) |
| test_command_matches_qa_reference_structure | ❌ FAIL (not matching) | ✅ PASS (pattern matches) |
| test_command_no_business_logic | ❌ FAIL (22 patterns) | ✅ PASS (0 patterns) |
| test_no_hook_logic_in_command | ❌ FAIL (found logic) | ✅ PASS (logic in skill) |
| test_skill_phase_7_has_seven_substeps | ❌ FAIL (missing 2) | ✅ PASS (all 7 present) |
| test_skill_phase_7_preserves_functionality | ❌ FAIL (not documented) | ✅ PASS (fully documented) |
| test_all_seven_phase_6_substeps_documented | ❌ FAIL (5 of 7) | ✅ PASS (7 of 7) |
| test_refactored_command_pattern_matches_qa | ❌ FAIL (not matching) | ✅ PASS (matches /qa pattern) |
| test_command_no_direct_subagent_calls | ❌ FAIL (1 found) | ✅ PASS (0 found) |

---

## Phase 3: Refactoring (Code Quality)

After Phase 2 tests pass, refactor for quality:

### 3.1: Code Review

- Check command follows lean pattern
- Verify skill Phase 7 is well-documented
- Ensure no anti-patterns

### 3.2: Documentation

- Add docstrings to Phase 7 substeps
- Include workflow diagrams
- Add examples and error scenarios

### 3.3: Light QA Validation

```bash
# Run light QA to catch any issues
/qa STORY-050 light
```

---

## Phase 4: Integration Testing

### 4.1: Run All Tests

```bash
pytest tests/unit/test_story050_budget_compliance.py \
        tests/integration/test_story050_functionality.py -v
# Expected: 35/35 PASS
```

### 4.2: Verify STORY-033 Tests Still Pass

```bash
pytest tests/unit/test_story033_conf_requirements.py \
        tests/integration/test_hook_integration_story033.py -v
# Expected: 84 tests pass/fail/skip identically before/after
```

### 4.3: Performance Validation

```bash
# Record before refactoring
bash .claude/scripts/benchmark_audit_deferrals.sh baseline

# Measure after refactoring
bash .claude/scripts/benchmark_audit_deferrals.sh refactored

# Compare (assert difference <10%)
python .claude/scripts/compare_performance.py baseline refactored
```

---

## Phase 5: Git Workflow & Completion

### 5.1: Update Story DoD

Mark all Definition of Done items as complete:

```markdown
## Definition of Done

### Implementation
- [x] Backup original command file
- [x] Create Phase 7 in devforgeai-orchestration skill
- [x] Move 7 Phase 6 substeps from command to skill Phase 7
- [x] Refactor command Phase 6 to delegate to skill
- [x] Reduce command to ~250-300 lines, ~8-10K characters
- [x] Verify character count: 8000-12000 chars
- [x] Verify skill size: <3500 lines

### Quality
- [x] All 84 STORY-033 tests pass with identical results
- [x] Backward compatibility verified (reports byte-identical)
- [x] Performance verified (execution time within 10%)
- [x] Pattern consistency verified (code review vs /qa)
- [x] Budget compliance verified (command <12K chars)

### Testing
- [x] Test Case 1: Character count
- [x] Test Case 2: Test compatibility
- [x] Test Case 3: Functionality preservation
- [x] Test Case 4: Performance benchmark
- [x] Test Case 5: Pattern verification
- [x] Test Case 6: Skill size
- [x] Test Case 7: Hook integration
- [x] Test Case 8: Error handling
- [x] Test Case 9: Backward compatibility
- [x] Test Case 10: Regression testing

### Documentation
- [x] Refactoring documented in refactoring-case-studies.md (Case Study 6)
- [x] Command budget reference updated
- [x] Skill Phase 7 documented
- [x] Pattern consistency notes added
```

### 5.2: Git Commit

```bash
git add .claude/commands/audit-deferrals.md \
        .claude/skills/devforgeai-orchestration/SKILL.md \
        [reference files if created]

git commit -m "$(cat <<'EOF'
refactor(STORY-050): Refactor /audit-deferrals for budget compliance

- Reduced command from 31.3K to ~9K chars (71% reduction)
- Extracted Phase 6 logic to devforgeai-orchestration skill Phase 7
- Added all 7 hook integration substeps (eligibility, context, sanitization, invocation, logging, error handling, circular prevention)
- Command now follows lean orchestration pattern (3 phases: validate → invoke skill → display)
- Achieved budget compliance: 9K chars (60% of 15K limit, target: 8-10K)
- Maintained 100% backward compatibility (all 84 STORY-033 tests pass identically)
- Performance maintained within 10% baseline (±10% threshold verified)
- Pattern consistency verified against /qa reference implementation

Technical changes:
  - .claude/commands/audit-deferrals.md: 31.3K → 9K chars (71% reduction)
  - .claude/skills/devforgeai-orchestration/SKILL.md: 3.2K → 3.6K lines (Phase 7 added)
  - All 12 failing tests now pass
  - All 23 previously passing tests still pass
  - 100% functionality preserved

References:
  - Lean Orchestration Pattern: devforgeai/protocols/lean-orchestration-pattern.md
  - Case Study 6: devforgeai/protocols/refactoring-case-studies.md
  - Command Budget: devforgeai/protocols/command-budget-reference.md
  - Reference Implementation (/qa): .claude/commands/qa.md
EOF
)"
```

### 5.3: Update Story Status

```bash
# Update story file YAML frontmatter
# status: Dev Complete
```

### 5.4: Document Workflow History

Add to story Workflow History section:

```markdown
## Workflow History

### 2025-11-17 Phase 1 (RED) - Test Generation Complete
- 35 tests generated (12 failing, 23 passing)
- All 5 ACs covered
- All 13 tech spec requirements covered
- Coverage gaps: 0
- Status: Ready for Phase 2 implementation

### 2025-11-17 Phase 2-5 (Implementation & Completion)
- Refactored command: 31.3K → 9K chars (71% reduction)
- Enhanced skill with Phase 7: 7 substeps fully documented
- All 35 tests passing (12 tests fixed)
- Performance: Within 10% baseline (verified)
- Backward compatibility: 100% (all 84 STORY-033 tests identical)
- Budget compliance: ✅ (9K < 12K target, 60% of 15K limit)
- Pattern consistency: ✅ (matches /qa reference)
- Status: Dev Complete

### 2025-11-17 Final Checklist
- [x] Phase 2: Implementation complete
- [x] Phase 3: Refactoring & code review complete
- [x] Phase 4: Integration testing complete (35/35 pass)
- [x] Phase 5: Git workflow & documentation complete
- [x] All DoD items checked
- [x] Story status: Dev Complete
```

---

## Detailed Tasks Breakdown

### Task 1: Command Refactoring (2-3 hours)

**Input file:** `.claude/commands/audit-deferrals.md` (31,300 chars)

**Output file:** `.claude/commands/audit-deferrals.md` (~8-10K chars)

**Specific actions:**

1. **Keep Phases 1-5 structure** (argument parsing, skill invocation framework)
   - Phase 0: Minimal validation (20-30 lines)
   - Phase 1: Context markers + skill invocation (40-50 lines)
   - Phase 2: Display results (20-30 lines)
   - Phase 3: Next steps guidance (20-30 lines)

2. **Remove all Phase 6 logic** (~200 lines)
   - All 7 substeps move to skill
   - Keep only brief note: "See devforgeai-orchestration skill Phase 7"

3. **Remove display templates** (~150 lines)
   - Delete all pass/fail/error template variants
   - Keep: minimal error display (5-10 lines)
   - Keep: reference to skill for detailed output

4. **Remove implementation notes** (~100 lines)
   - Keep only essential integration notes
   - Move detailed guidance to external reference

5. **Clean up documentation** (~300 lines)
   - Keep: High-level workflow description
   - Remove: Detailed step-by-step instructions
   - Reference: `.claude/memory/commands-reference.md` for complete details

**Verification steps:**

```bash
# Check size
wc -c .claude/commands/audit-deferrals.md
# Expected: 8000-12000

# Check structure
grep "^### Phase" .claude/commands/audit-deferrals.md | wc -l
# Expected: 3-4 phases

# Check delegation
grep "Skill(command=" .claude/commands/audit-deferrals.md
# Expected: 1 match with devforgeai-orchestration
```

---

### Task 2: Skill Enhancement (1.5-2 hours)

**Input file:** `.claude/skills/devforgeai-orchestration/SKILL.md` (3,249 lines)

**Output file:** `.claude/skills/devforgeai-orchestration/SKILL.md` (3,600-3,700 lines)

**Specific actions:**

1. **Add Phase 7 section** (~350-400 lines)
   - Location: After Phase 6 (orchestration modes)
   - 7 substeps, each documented
   - Include: Purpose, execution flow, error handling, special cases

2. **Document 7 substeps** (~50 lines each):
   - 7.1 Eligibility check (validate hook conditions)
   - 7.2 Context preparation (extract audit metadata)
   - 7.3 Sanitization (remove sensitive data)
   - 7.4 Hook invocation (call devforgeai invoke-hooks)
   - 7.5 Logging (record invocation results)
   - 7.6 Error handling (graceful degradation)
   - 7.7 Circular prevention (detect infinite loops)

3. **Reference file consideration**:
   - If Phase 7 >300 lines: Create `.claude/skills/devforgeai-orchestration/references/audit-deferrals-hook-integration.md`
   - Reduces skill entry point (keep <200 lines per Reddit pattern)
   - Load on-demand when Phase 7 executes

**Verification steps:**

```bash
# Check skill size
wc -l .claude/skills/devforgeai-orchestration/SKILL.md
# Expected: <3500

# Check Phase 7 exists
grep -c "### Phase 7:" .claude/skills/devforgeai-orchestration/SKILL.md
# Expected: 1

# Check all 7 substeps present
grep -c "^#### 7\.[1-7]:" .claude/skills/devforgeai-orchestration/SKILL.md
# Expected: 7
```

---

### Task 3: Testing & Validation (1-1.5 hours)

**Run test suites:**

```bash
# Phase 2 completion verification
pytest tests/unit/test_story050_budget_compliance.py \
        tests/integration/test_story050_functionality.py -v --tb=short

# Expected: 35 PASS (currently 12 FAIL → 0 FAIL after implementation)
```

**Validate backward compatibility:**

```bash
pytest tests/unit/test_story033_conf_requirements.py \
        tests/integration/test_hook_integration_story033.py -v

# Expected: 84 tests pass/fail/skip identically (no regressions)
```

**Performance validation:**

```bash
# Baseline (before refactoring)
time /audit-deferrals > /tmp/baseline.json

# After refactoring
time /audit-deferrals > /tmp/refactored.json

# Compare outputs (should be byte-identical except timestamp)
diff <(jq 'del(.timestamp)' /tmp/baseline.json) \
     <(jq 'del(.timestamp)' /tmp/refactored.json)
# Expected: identical output (no changes except timing)
```

---

### Task 4: Documentation & Commit (1 hour)

**Files to update:**

1. **Story file:** `devforgeai/specs/Stories/STORY-050-refactor-audit-deferrals-budget-compliance.story.md`
   - Mark all DoD items as complete
   - Add Workflow History entries
   - Update Implementation Notes

2. **Refactoring documentation:** `devforgeai/protocols/refactoring-case-studies.md`
   - Add Case Study 6 (STORY-050 refactoring)
   - Include Before/After metrics
   - Document lessons learned

3. **Budget reference:** `devforgeai/protocols/command-budget-reference.md`
   - Update audit-deferrals from 31.3K (208%) to ~9K (60%)
   - Update priority queue (one less over-budget command)
   - Update compliance summary table

4. **Memory references:** `.claude/memory/commands-reference.md`
   - Note refactoring completion
   - Update audit-deferrals command description

**Git commit:**

```bash
git add .claude/commands/audit-deferrals.md \
        .claude/skills/devforgeai-orchestration/SKILL.md \
        devforgeai/specs/Stories/STORY-050-refactor-audit-deferrals-budget-compliance.story.md \
        devforgeai/protocols/refactoring-case-studies.md \
        devforgeai/protocols/command-budget-reference.md

git commit -m "refactor(STORY-050): Refactor /audit-deferrals for budget compliance..."
```

---

## Risk Analysis & Mitigation

### Risk 1: Skill Size Exceeds 3,500 Lines

**Risk:** Phase 7 implementation too large, skill exceeds target size

**Mitigation:**
- Use progressive disclosure: Extract Phase 7 to reference file
- Load reference file on-demand in skill
- Keep skill entry point <200 lines per Reddit article pattern

**Verification:** `wc -l .claude/skills/devforgeai-orchestration/SKILL.md` <3500

---

### Risk 2: Backward Compatibility Breaks

**Risk:** STORY-033 tests fail or audit report format changes

**Mitigation:**
- Keep Phase 1-5 command logic identical
- Only change Phase 6 (move to skill)
- Run STORY-033 tests before/after comparison

**Verification:** 84 STORY-033 tests pass/fail/skip identically before/after

---

### Risk 3: Performance Regression

**Risk:** Refactored command executes slower due to skill invocation overhead

**Mitigation:**
- Measure baseline before refactoring
- Compare P95 execution time before/after
- Threshold: <10% increase acceptable

**Verification:** `P95_after < P95_baseline * 1.1`

---

### Risk 4: Test Failures After Refactoring

**Risk:** New tests fail unexpectedly during Phase 2

**Mitigation:**
- Implement command refactoring first (should fix 12 failing tests)
- Then implement skill Phase 7 (should fix remaining issues)
- If tests still fail, debug individually

**Verification:** All 35 tests PASS after Phase 2 complete

---

## Success Criteria

✅ **Phase 2 (Green) Complete when:**
- [ ] Command size: 8-10K chars (verified: `wc -c < .claude/commands/audit-deferrals.md`)
- [ ] Command phases: 3-4 (verified: `grep "^### Phase"`count)
- [ ] Skill size: <3,500 lines (verified: `wc -l`)
- [ ] Phase 7 substeps: All 7 documented (verified: `grep "#### 7\.[1-7]:"`count = 7)
- [ ] Tests passing: 35/35 (verified: `pytest ... -v`)
- [ ] STORY-033 tests: Identical results (verified: before/after comparison)
- [ ] Performance: Within 10% baseline (verified: P95 benchmark)

✅ **Phase 3 (Refactor) Complete when:**
- [ ] Code review passed
- [ ] Light QA validation passed
- [ ] Documentation complete

✅ **Phase 4 (Integration) Complete when:**
- [ ] All tests pass: 35/35
- [ ] Backward compatibility verified: 84/84 STORY-033 tests identical
- [ ] Performance validated: ±10% baseline

✅ **Phase 5 (Complete) Complete when:**
- [ ] Story DoD 100% complete
- [ ] Git committed
- [ ] Story status: Dev Complete
- [ ] Workflow history documented

---

## Timeline Estimate

| Phase | Task | Duration | Notes |
|-------|------|----------|-------|
| **Pre-Phase** | Test Generation | 30 min | ✅ COMPLETE |
| **Phase 2** | Command refactoring | 2-3 h | Reduce 31K → 9K chars |
| **Phase 2** | Skill enhancement | 1.5-2 h | Add Phase 7 (7 substeps) |
| **Phase 3** | Code review & refactor | 30 min | Quality improvements |
| **Phase 4** | Testing & validation | 1-1.5 h | Run all tests, verify compat |
| **Phase 5** | Documentation & commit | 1 h | Update story, commit |
| **TOTAL** | **Complete Implementation** | **5-6 hours** | Estimated total time |

---

## Reference Implementation (Template)

Use `/qa` command refactoring as primary template:

**Before refactoring:**
- 692 lines
- 31K chars (206% over budget)
- Multiple display templates
- Result parsing in command

**After refactoring:**
- 295 lines
- 7.2K chars (48% of budget)
- Skill generates templates via qa-result-interpreter subagent
- Command just displays result

**Pattern applied to STORY-050:**
- Before: 1,100 lines, 31.3K chars (208% over)
- After: 250-300 lines, 8-10K chars (53-67% of budget)
- Same lean orchestration pattern
- Extraction to skill (Phase 7)
- Subagent delegation (hook integration)

---

## Next Steps

**When ready to execute Phase 2-5:**

1. **Run Phase 2 implementation** (3-4 hours)
   ```bash
   /dev STORY-050  # Resume development with this plan as guide
   ```

2. **Execute Tasks 1-4** in sequence:
   - Task 1: Command refactoring
   - Task 2: Skill enhancement
   - Task 3: Testing & validation
   - Task 4: Documentation & commit

3. **Verify success criteria** at each phase

4. **Complete story** when all phases finish

---

## Related Documentation

- **Lean Orchestration Pattern:** `devforgeai/protocols/lean-orchestration-pattern.md`
- **Refactoring Case Studies:** `devforgeai/protocols/refactoring-case-studies.md`
- **Command Budget Reference:** `devforgeai/protocols/command-budget-reference.md`
- **/qa Reference Implementation:** `.claude/commands/qa.md` (295 lines, 7.2K chars)
- **/dev Reference Implementation:** `.claude/commands/dev.md` (513 lines, 12.6K chars)
- **Test Suite:** `tests/unit/test_story050_budget_compliance.py` (18 tests)
- **Test Suite:** `tests/integration/test_story050_functionality.py` (15 tests)

---

**Status:** Implementation plan complete. Ready for Phase 2-5 execution.

**Approved by:** Automated planning (Phase 1 complete, user confirmed detailed plan approach)

**Date prepared:** 2025-11-17
