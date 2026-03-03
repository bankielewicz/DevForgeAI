# RCA-012 Phase 2 Test Validation
## Manual Testing Procedures for Phase 0.9

**Created:** 2025-01-21
**Status:** Ready for Manual Execution
**Test Scenarios:** 4 comprehensive scenarios

---

## Testing Approach

**Why Manual Testing:**
Phase 0.9 is integrated into the `/qa` command workflow. Testing requires running full `/qa` invocations, which:
- Execute complete QA skill (all 7+ phases)
- Require story context and validation infrastructure
- Are resource-intensive (65K+ tokens for deep mode)

**Recommended:** Execute these tests when ready to validate Phase 2, or defer to Phase 3 (when auditing stories).

---

## Test Scenario 1: STORY-007 (Perfect Traceability - Should PASS)

### Objective
Verify Phase 0.9 allows stories with 100% AC-to-DoD traceability to proceed to validation phases.

### Story Characteristics
- **File:** `devforgeai/specs/Stories/STORY-007-post-operation-retrospective-conversation.story.md`
- **Template:** v2.0 (AC headers: `### 1. [x]`)
- **AC Count:** 6
- **AC Requirements:** 16 granular requirements
- **DoD Items:** 22 total
- **DoD Completion:** 100% (22/22 checked)
- **Traceability:** 100% (all 16 requirements have DoD coverage)

### Test Procedure
```bash
/qa STORY-007 light
```

### Expected Phase 0.9 Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation (RCA-012)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Template version: v2.0
  • Total ACs: 6
  • Total requirements (granular): 16
  • DoD items: 22

Traceability Mapping:
  • AC#1 (3 requirements) → 6 DoD items ✓
  • AC#2 (3 requirements) → 4 DoD items ✓
  • AC#3 (2 requirements) → 2 DoD items ✓
  • AC#4 (3 requirements) → 4 DoD items ✓
  • AC#5 (2 requirements) → 3 DoD items ✓
  • AC#6 (3 requirements) → 3 DoD items ✓

Traceability Score: 100% ✅

DoD Completion Status:
  • Total items: 22
  • Complete [x]: 22
  • Incomplete [ ]: 0
  • Completion: 100%

✓ PASS - Traceability validated, story ready for QA validation

Proceeding to Phase 1 (Validation Mode Selection)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: Validation Mode = light
... (QA continues to coverage analysis, anti-patterns, etc.)
```

### Expected Behavior
- [ ] Phase 0.9 executes (output visible)
- [ ] Displays traceability analysis correctly
- [ ] Shows 100% traceability score
- [ ] Shows PASS status
- [ ] QA continues to Phase 1 (NOT halted)
- [ ] QA completes light validation normally
- [ ] No errors related to Phase 0.9

### If Test Fails
**Symptoms:**
- Phase 0.9 doesn't execute (no output)
- Traceability score incorrect (not 100%)
- QA halts unexpectedly
- Errors in algorithm execution

**Diagnosis:**
- Check if Phase 0.9 section exists in SKILL.md
- Verify reference files are loadable
- Check algorithm logic (Step 1-5 execution)
- Review display template population

**Fix:**
- Debug specific failure point
- Review algorithm.md for errors
- Test keyword matching with STORY-007 data
- Re-sync files if needed

---

## Test Scenario 2: Missing DoD Coverage (Should HALT)

### Objective
Verify Phase 0.9 halts QA when AC requirement has no corresponding DoD item.

### Test Story Creation
```bash
cat > devforgeai/specs/Stories/TEST-MISSING-COVERAGE.story.md << 'EOF'
---
id: TEST-MISSING-COVERAGE
title: Test Story for Phase 0.9 - Missing DoD Coverage
status: Dev Complete
format_version: "2.1"
---

# Story: Test Missing Coverage

## Acceptance Criteria

### AC#1: Feature Works Correctly and Performs Well

**Given** valid input data
**When** user submits request
**Then** system processes request successfully
**And** system completes processing in <100ms
**And** system logs transaction to audit trail

## Definition of Done

### Implementation
- [x] Feature implemented (processes request)

### Testing
- [x] Unit tests passing

# MISSING DoD coverage for:
# - AC#1: "completes in <100ms" (performance requirement)
# - AC#1: "logs transaction" (logging requirement)

## Implementation Notes

- [x] Feature implemented (processes request) - Completed: Phase 2
- [x] Unit tests passing - Completed: Phase 1

**Status:** Dev Complete (but missing DoD items for performance and logging)
EOF
```

### Test Procedure
```bash
/qa TEST-MISSING-COVERAGE light
```

### Expected Phase 0.9 Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation (RCA-012)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Template version: v2.1
  • Total ACs: 1
  • Total requirements: 3
  • DoD items: 2

Traceability Mapping:
  • AC#1 (3 requirements) → 1 DoD item ⚠️ (2 missing)

Traceability Score: 33% ❌ (100% required)

Missing DoD Coverage for AC Requirements:
  • AC#1: completes processing in <100ms
  • AC#1: logs transaction to audit trail

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - AC-DoD Traceability Insufficient
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Missing Coverage: 2 AC requirements have no DoD validation

ACTION REQUIRED:

Add to Definition of Done:

### Quality
- [ ] Performance validated: Processing completes in <100ms (p95)

### Implementation
- [ ] Logging implemented: Transaction audit trail (all requests logged)

After fixing, re-run: /qa TEST-MISSING-COVERAGE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QA WORKFLOW HALTED - Fix traceability issues before proceeding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Expected Behavior
- [ ] Phase 0.9 executes
- [ ] Detects 3 AC requirements, 2 DoD items
- [ ] Calculates traceability: 33% (1/3 covered)
- [ ] Lists 2 missing requirements correctly
- [ ] Displays FAIL status with remediation
- [ ] QA HALTS at Phase 0.9 (does NOT proceed to Phase 1)
- [ ] Provides actionable fix (add 2 DoD items)

### Cleanup
```bash
rm devforgeai/specs/Stories/TEST-MISSING-COVERAGE.story.md
```

---

## Test Scenario 3: Undocumented Deferrals (Should HALT - STORY-038 Pattern)

### Objective
Verify Phase 0.9 halts when DoD has incomplete items without "Approved Deferrals" section (prevents STORY-038 bypass).

### Test Story Creation
```bash
cat > devforgeai/specs/Stories/TEST-UNDOCUMENTED-DEFERRALS.story.md << 'EOF'
---
id: TEST-UNDOCUMENTED-DEFERRALS
title: Test Story - Incomplete DoD Without Approval (STORY-038 Pattern)
status: Dev Complete
format_version: "2.1"
---

# Story: Test Undocumented Deferrals

## Acceptance Criteria

### AC#1: Quality Metrics Calculated

**Given** source code files
**When** quality analysis runs
**Then** system calculates complexity, duplication, and maintainability index

## Definition of Done

### Implementation
- [x] Complexity calculation implemented
- [x] Duplication detection implemented
- [x] Maintainability index calculated

### Testing
- [x] Unit test: Complexity calculation accuracy
- [x] Integration test: Full quality analysis workflow
- [ ] Performance test: 10K LOC analysis <30s
- [ ] Edge case test: Zero-line files
- [ ] Edge case test: Binary files
- [ ] Threshold violation test: Extreme values

### Documentation
- [x] Code quality metrics documented

# NO "Approved Deferrals" section
# Simulates STORY-038: 4 incomplete Testing items without documentation

## Implementation Notes

- [x] Complexity calculation implemented - Completed: Phase 2
- [x] Duplication detection implemented - Completed: Phase 2
- [x] Maintainability index calculated - Completed: Phase 2
- [x] Unit test: Complexity calculation accuracy - Completed: Phase 1
- [x] Integration test: Full quality analysis workflow - Completed: Phase 4
- [x] Code quality metrics documented - Completed: Phase 2

**Status:** Dev Complete
EOF
```

### Test Procedure
```bash
/qa TEST-UNDOCUMENTED-DEFERRALS light
```

### Expected Phase 0.9 Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation (RCA-012)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Total ACs: 1
  • Total requirements: 3

Traceability Mapping:
  • AC#1 (3 requirements) → 3 DoD items ✓

Traceability Score: 100% ✅

DoD Completion Status:
  • Total items: 10
  • Complete [x]: 6
  • Incomplete [ ]: 4
  • Completion: 60%

Deferral Documentation: INVALID (no Approved Deferrals section found)
  • Approved Deferrals section: MISSING ✗
  • Incomplete items: 4 (none documented)

Undocumented Incomplete DoD Items:
  • Testing: Performance test - 10K LOC analysis <30s
  • Testing: Edge case test - Zero-line files
  • Testing: Edge case test - Binary files
  • Testing: Threshold violation test - Extreme values

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - Incomplete DoD Without Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DoD Completion: 60% (6/10 items)

Incomplete Items: 4 (lack user approval documentation)

ACTION REQUIRED:

Add "Approved Deferrals" section to Implementation Notes:

## Approved Deferrals

**User Approval:** 2025-01-21 {time} UTC
**Approval Type:** Low-Priority Enhancement Deferral

**Deferred Items:**
1. **Performance test: 10K LOC analysis <30s**
   - Reason: {Blocker explanation}
   - Blocker Type: Artifact / Toolchain / Low-Priority
   - Follow-up: {Story ref or condition}

... (template for all 4 items)

After adding section, re-run: /qa TEST-UNDOCUMENTED-DEFERRALS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QA WORKFLOW HALTED - Add deferral documentation before proceeding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is the STORY-038 pattern. Phase 0.9 prevents this bypass.
```

### Expected Behavior
- [ ] Phase 0.9 executes
- [ ] Traceability: 100% (AC requirements covered)
- [ ] DoD completion: 60% (4/10 incomplete)
- [ ] Detects missing "Approved Deferrals" section
- [ ] Lists all 4 incomplete items
- [ ] Displays deferral template for user
- [ ] QA HALTS (does NOT proceed to Phase 1)
- [ ] Provides clear remediation guidance

### Success Criteria
✅ Phase 0.9 prevents STORY-038 pattern (primary goal)
✅ User sees exactly which items need deferral documentation
✅ Template provided is copy-paste ready
✅ QA does not bypass quality gate

### Cleanup
```bash
rm devforgeai/specs/Stories/TEST-UNDOCUMENTED-DEFERRALS.story.md
```

---

## Test Scenario 4: STORY-023 (Documented Deferrals - Should PASS)

### Objective
Verify Phase 0.9 allows stories with properly documented deferrals to proceed.

### Story Characteristics
- **File:** `devforgeai/specs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md`
- **Template:** v2.0
- **AC Count:** 7
- **DoD Items:** 22 total
- **DoD Completion:** 68% (15/22 checked, 7 deferred)
- **Deferrals:** VALID (all 7 documented in "Approved Deferrals" section)
- **User Approval:** 2025-11-14 14:30 UTC
- **Follow-up:** STORY-024 (implementation phase, now complete)

### Test Procedure
```bash
/qa STORY-023 light
```

### Expected Phase 0.9 Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation (RCA-012)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Template version: v2.0
  • Total ACs: 7
  • Total requirements: 18

Traceability Mapping:
  • AC#1 (3 requirements) → 3 DoD items ✓
  • AC#2 (2 requirements) → 2 DoD items ✓
  • AC#3 (3 requirements) → 3 DoD items ✓
  • AC#4 (2 requirements) → 2 DoD items ✓
  • AC#5 (3 requirements) → 3 DoD items ✓
  • AC#6 (2 requirements) → 2 DoD items ✓
  • AC#7 (3 requirements) → 3 DoD items ✓

Traceability Score: 100% ✅

DoD Completion Status:
  • Total items: 22
  • Complete [x]: 15
  • Incomplete [ ]: 7
  • Completion: 68%

Deferral Documentation: VALID (all 7 items user-approved)
  • Approved Deferrals section: EXISTS ✓
  • User approval timestamp: 2025-11-14 14:30 UTC ✓
  • Documented deferrals: 7/7 items (100%)
  • Follow-up story: STORY-024 (status: QA Approved, completed)

✓ PASS - Traceability validated, deferrals properly documented

Proceeding to Phase 1 (Validation Mode Selection)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: Design-phase story. Implementation deferred to STORY-024 with user approval.

Phase 1: Validation Mode = light
... (QA continues)
```

### Expected Behavior
- [ ] Phase 0.9 executes
- [ ] Traceability: 100%
- [ ] DoD completion: 68% (detected correctly)
- [ ] Finds "Approved Deferrals" section
- [ ] Validates user approval timestamp
- [ ] Matches 7/7 incomplete items to deferral list
- [ ] Shows PASS status (deferrals valid)
- [ ] QA continues to Phase 1 (NOT halted)
- [ ] Design-phase deferral pattern accepted

### Success Criteria
✅ Phase 0.9 accepts valid deferrals
✅ Design-phase stories can progress with incomplete implementation
✅ User approval requirement enforced
✅ Follow-up story reference validated

---

## Test Execution Summary

### Manual Test Execution Checklist

**When executing these tests:**

- [ ] **Before Testing:** Verify Phase 0.9 is in operational .claude/skills/devforgeai-qa/SKILL.md
- [ ] **Test 1:** Run `/qa STORY-007 light` → Verify PASS, continues
- [ ] **Test 2:** Create TEST-MISSING-COVERAGE.story.md, run `/qa`, verify HALT with remediation
- [ ] **Test 3:** Create TEST-UNDOCUMENTED-DEFERRALS.story.md, run `/qa`, verify HALT with template
- [ ] **Test 4:** Run `/qa STORY-023 light` → Verify PASS with deferrals, continues
- [ ] **After Testing:** Clean up test stories, document results

### Expected Test Results

| Test | Story | Expected Result | Validates |
|------|-------|----------------|-----------|
| 1 | STORY-007 | PASS, continue to Phase 1 | Perfect traceability handling |
| 2 | TEST-MISSING-COVERAGE | HALT at Phase 0.9 | Missing coverage detection |
| 3 | TEST-UNDOCUMENTED-DEFERRALS | HALT at Phase 0.9 | STORY-038 pattern prevention |
| 4 | STORY-023 | PASS, continue to Phase 1 | Valid deferral acceptance |

**Success:** All 4 tests behave as expected (100% pass rate)

---

## Alternative: Validation Without Full /qa Execution

**If you want to validate algorithm logic without running full QA:**

### Unit Test Approach

**Test Algorithm Components Independently:**

```python
# Pseudo-code for unit testing

# Test 1: AC Extraction
story_content = read_file("STORY-007-*.story.md")
ac_requirements = extract_ac_requirements(story_content)
assert len(ac_requirements) == 16  # Known count for STORY-007

# Test 2: DoD Extraction
dod_items = extract_dod_items(story_content)
assert len(dod_items) == 22  # Known count
assert all(item['checked'] for item in dod_items)  # All checked

# Test 3: Keyword Matching
ac_req = "Introduction explaining (≥200 words)"
dod_item = "Document includes introduction (648 words)"
score = calculate_match(ac_req, dod_item)
assert score >= 0.5  # Should match

# Test 4: Deferral Detection
story_with_deferrals = read_file("STORY-023-*.story.md")
deferral_status = validate_deferrals(story_with_deferrals)
assert deferral_status == "VALID"  # STORY-023 has documented deferrals
```

**Benefit:** Tests algorithm components without full QA overhead

**Limitation:** Doesn't test full integration, only individual functions

---

## Test Results Documentation Template

**After executing tests, document results:**

```markdown
# RCA-012 Phase 2 Test Results

**Test Date:** 2025-01-{XX}
**Tester:** {Name}
**QA Skill Version:** Phase 0.9 integrated

## Test Execution

| Test | Story | Expected | Actual | Status | Notes |
|------|-------|----------|--------|--------|-------|
| 1 | STORY-007 | PASS, continue | {actual} | {✅/❌} | {observations} |
| 2 | TEST-MISSING-COVERAGE | HALT at 0.9 | {actual} | {✅/❌} | {observations} |
| 3 | TEST-UNDOCUMENTED-DEFERRALS | HALT at 0.9 | {actual} | {✅/❌} | {observations} |
| 4 | STORY-023 | PASS, continue | {actual} | {✅/❌} | {observations} |

## Summary

**Tests Passed:** {count}/4
**Tests Failed:** {count}/4
**Pass Rate:** {percentage}%

## Issues Found

{IF any tests failed}:
- Issue 1: {description}
  - Symptom: {what happened}
  - Root cause: {why it happened}
  - Fix: {what needs to change}

## Validation

- [ ] All 4 tests passed
- [ ] No false positives (valid stories incorrectly halted)
- [ ] No false negatives (invalid stories incorrectly passed)
- [ ] Remediation guidance is clear and actionable
- [ ] Performance acceptable (<30s overhead, <2K tokens)

## Sign-Off

**Phase 2 Testing:** {COMPLETE / NEEDS REWORK}
**Tester:** {Name}
**Date:** {timestamp}
```

**Save to:** `devforgeai/RCA/RCA-012/test-results/phase2-test-results.md`

---

**Test Validation Documentation Complete**

**Status:** Tests designed and documented, ready for manual execution
**Recommended:** Execute tests when ready to validate Phase 0.9, or proceed to commit and validate in Phase 3
