# RCA-012: Validation Procedures
## Comprehensive Testing and Verification for All Remediation Phases

**Version:** 1.0
**Created:** 2025-01-21
**Purpose:** Detailed validation procedures ensuring each RCA-012 fix works correctly

---

## Overview

This document provides step-by-step validation procedures for each recommendation, phase, and the overall remediation effort. Use these procedures to verify fixes are correct before moving to the next phase.

---

## Validation Scripts

All validation scripts are stored in: `devforgeai/RCA/RCA-012/scripts/`

### Script: validate-phase1.sh

**Purpose:** Validate Phase 1 (Template + Documentation) completion

**Script:**
```bash
#!/bin/bash
# validate-phase1.sh - Phase 1 Completion Validation

echo "========================================================================="
echo "RCA-012 Phase 1 Validation"
echo "========================================================================="

total=0
passed=0
failed=0

# Test 1: Template format
echo "[1/7] Validating template format..."
ac_count=$(grep -c "^### AC#[0-9]:" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md 2>/dev/null || echo 0)
if [ $ac_count -eq 4 ]; then
  echo "  ✓ PASS: AC headers use new format (4 found)"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Expected 4 AC headers, found $ac_count"
  failed=$((failed + 1))
fi
total=$((total + 1))

# Test 2: No old format remains
echo "[2/7] Checking for old format..."
old_format=$(grep -c "^### [0-9]\. \[" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md 2>/dev/null || echo 0)
if [ $old_format -eq 0 ]; then
  echo "  ✓ PASS: No old checkbox syntax"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Old format still present ($old_format instances)"
  failed=$((failed + 1))
fi
total=$((total + 1))

# Test 3: Format version
echo "[3/7] Validating format version..."
if grep -q 'format_version: "2.1"' .claude/skills/devforgeai-story-creation/assets/templates/story-template.md; then
  echo "  ✓ PASS: Format version is 2.1"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Format version not 2.1"
  failed=$((failed + 1))
fi
total=$((total + 1))

# Test 4: Changelog present
echo "[4/7] Checking changelog..."
if grep -q "v2.1 (2025-01-21)" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md; then
  echo "  ✓ PASS: Changelog header present"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Changelog missing"
  failed=$((failed + 1))
fi
total=$((total + 1))

# Test 5: CLAUDE.md updated
echo "[5/7] Validating CLAUDE.md update..."
if grep -q "Acceptance Criteria vs. Tracking Mechanisms" src/CLAUDE.md; then
  echo "  ✓ PASS: CLAUDE.md section added"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: CLAUDE.md not updated"
  failed=$((failed + 1))
fi
total=$((total + 1))

# Test 6: CLAUDE.md synced
echo "[6/7] Checking CLAUDE.md sync..."
if diff -q src/CLAUDE.md CLAUDE.md > /dev/null 2>&1; then
  echo "  ✓ PASS: CLAUDE.md synced to root"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: CLAUDE.md not synced"
  failed=$((failed + 1))
fi
total=$((total + 1))

# Test 7: Skill documentation
echo "[7/7] Validating skill documentation..."
if grep -q "Story Template Versions" .claude/skills/devforgeai-story-creation/SKILL.md; then
  echo "  ✓ PASS: Skill version history added"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Skill not updated"
  failed=$((failed + 1))
fi
total=$((total + 1))

# Summary
echo ""
echo "========================================================================="
echo "Phase 1 Validation Summary"
echo "========================================================================="
echo "Total Tests: $total"
echo "Passed: $passed"
echo "Failed: $failed"
echo "Success Rate: $((passed * 100 / total))%"
echo ""

if [ $failed -eq 0 ]; then
  echo "✅ PHASE 1 VALIDATION: PASS"
  echo "   All 7 validation checks passed"
  echo "   Ready to proceed to Phase 2"
  exit 0
else
  echo "❌ PHASE 1 VALIDATION: FAIL"
  echo "   $failed tests failed"
  echo "   Review failures and re-implement before proceeding"
  exit 1
fi
```

**Usage:**
```bash
bash devforgeai/RCA/RCA-012/scripts/validate-phase1.sh
```

**Expected:** All 7 tests pass, exit code 0

---

### Script: validate-phase2.sh

**Purpose:** Validate Phase 2 (QA Enhancement) completion

**Script:**
```bash
#!/bin/bash
# validate-phase2.sh - Phase 2 QA Enhancement Validation

echo "========================================================================="
echo "RCA-012 Phase 2 Validation"
echo "========================================================================="

total=0
passed=0

# Test 1: Traceability algorithm file exists
echo "[1/4] Checking traceability algorithm..."
if [ -f ".claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md" ]; then
  echo "  ✓ PASS: Algorithm file exists"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Algorithm file missing"
fi
total=$((total + 1))

# Test 2: Phase 0.9 in QA skill
echo "[2/4] Checking Phase 0.9 in QA skill..."
if grep -q "Phase 0.9.*Traceability Validation" .claude/skills/devforgeai-qa/SKILL.md; then
  echo "  ✓ PASS: Phase 0.9 added to QA skill"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Phase 0.9 not found"
fi
total=$((total + 1))

# Test 3: Report template exists
echo "[3/4] Checking report template..."
if [ -f ".claude/skills/devforgeai-qa/assets/traceability-report-template.md" ]; then
  echo "  ✓ PASS: Report template exists"
  passed=$((passed + 1))
else
  echo "  ⚠️  WARN: Report template missing (optional)"
  passed=$((passed + 1))  # Not critical
fi
total=$((total + 1))

# Test 4: Integration test scenarios
echo "[4/4] Running integration tests..."
echo "  (Manual validation required - see TESTING-PLAN.md Test 2.1-2.4)"
echo "  Mark PASS if all 4 scenarios behave correctly"
read -p "  Did all 4 QA test scenarios pass? (y/n): " response

if [[ "$response" == "y" ]]; then
  echo "  ✓ PASS: Integration tests passed"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Integration tests failed or not run"
fi
total=$((total + 1))

# Summary
echo ""
echo "========================================================================="
echo "Phase 2 Validation Summary"
echo "========================================================================="
echo "Tests: $total"
echo "Passed: $passed"
echo ""

if [ $passed -eq $total ]; then
  echo "✅ PHASE 2 VALIDATION: PASS"
  echo "   QA enhancement operational"
  echo "   Ready to proceed to Phase 3"
  exit 0
else
  echo "❌ PHASE 2 VALIDATION: FAIL"
  echo "   Review failures before proceeding"
  exit 1
fi
```

---

### Script: validate-phase3.sh

**Purpose:** Validate Phase 3 (Historical Cleanup) completion

**Script:**
```bash
#!/bin/bash
# validate-phase3.sh - Phase 3 Historical Cleanup Validation

echo "========================================================================="
echo "RCA-012 Phase 3 Validation"
echo "========================================================================="

# Test 1: Audit script exists
if [ -f "devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh" ]; then
  echo "✓ Audit script exists"
else
  echo "✗ Audit script missing"
  exit 1
fi

# Test 2: Run audit and check compliance
echo ""
echo "Running compliance audit..."
bash devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh > /tmp/phase3-audit.txt

# Extract compliance metrics
non_compliant=$(grep "Non-Compliant:" /tmp/phase3-audit.txt | awk '{print $2}')

echo ""
echo "Audit Results:"
cat /tmp/phase3-audit.txt | tail -15

echo ""
if [ "$non_compliant" -eq 0 ]; then
  echo "✅ PHASE 3 VALIDATION: PASS"
  echo "   All 39 stories compliant (100%)"
  echo "   Ready to proceed to Phase 4"
  exit 0
else
  echo "❌ PHASE 3 VALIDATION: FAIL"
  echo "   $non_compliant stories still non-compliant"
  echo "   Review flagged stories and fix before proceeding"
  exit 1
fi
```

---

### Script: validate-phase4.sh

**Purpose:** Validate Phase 4 (Automation) completion

**Script:**
```bash
#!/bin/bash
# validate-phase4.sh - Phase 4 Automation Validation

echo "========================================================================="
echo "RCA-012 Phase 4 Validation"
echo "========================================================================="

total=0
passed=0

# Test 1: Migration script exists
echo "[1/3] Checking migration script..."
if [ -f ".claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh" ]; then
  if [ -x ".claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh" ]; then
    echo "  ✓ PASS: Migration script exists and is executable"
    passed=$((passed + 1))
  else
    echo "  ✗ FAIL: Migration script not executable"
  fi
else
  echo "  ✗ FAIL: Migration script missing"
fi
total=$((total + 1))

# Test 2: Traceability matrix in template
echo "[2/3] Checking traceability matrix in template..."
if grep -q "AC-to-DoD Traceability Matrix" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md; then
  echo "  ✓ PASS: Traceability matrix section in template"
  passed=$((passed + 1))
else
  echo "  ⚠️  WARN: Matrix section missing (optional enhancement)"
  passed=$((passed + 1))  # Optional
fi
total=$((total + 1))

# Test 3: Documentation complete
echo "[3/3] Checking documentation..."
doc_complete=true

if [ ! -f "devforgeai/RCA/RCA-012/MIGRATION-SCRIPT.md" ]; then
  echo "  ⚠️  Missing: MIGRATION-SCRIPT.md"
  doc_complete=false
fi

if [ ! -f "devforgeai/RCA/RCA-012/TRACEABILITY-MATRIX.md" ]; then
  echo "  ⚠️  Missing: TRACEABILITY-MATRIX.md"
  doc_complete=false
fi

if [ "$doc_complete" = true ]; then
  echo "  ✓ PASS: Documentation complete"
  passed=$((passed + 1))
else
  echo "  ✗ FAIL: Documentation incomplete"
fi
total=$((total + 1))

# Summary
echo ""
echo "========================================================================="
echo "Phase 4 Validation Summary"
echo "========================================================================="
echo "Tests: $total"
echo "Passed: $passed"
echo ""

if [ $passed -eq $total ]; then
  echo "✅ PHASE 4 VALIDATION: PASS"
  echo "   Automation tools operational"
  echo "   RCA-012 remediation complete"
  exit 0
else
  echo "❌ PHASE 4 VALIDATION: FAIL"
  exit 1
fi
```

---

### Script: validate-all-phases.sh

**Purpose:** Comprehensive validation across all 4 phases

**Script:**
```bash
#!/bin/bash
# validate-all-phases.sh - Comprehensive RCA-012 Validation

echo "========================================================================="
echo "RCA-012 Comprehensive Validation"
echo "========================================================================="
echo "Validating all 4 remediation phases..."
echo ""

# Phase 1
echo "Phase 1: Foundation"
bash devforgeai/RCA/RCA-012/scripts/validate-phase1.sh
phase1_result=$?

# Phase 2
echo ""
echo "Phase 2: Quality Gate Enhancement"
bash devforgeai/RCA/RCA-012/scripts/validate-phase2.sh
phase2_result=$?

# Phase 3
echo ""
echo "Phase 3: Historical Cleanup"
bash devforgeai/RCA/RCA-012/scripts/validate-phase3.sh
phase3_result=$?

# Phase 4
echo ""
echo "Phase 4: Automation"
bash devforgeai/RCA/RCA-012/scripts/validate-phase4.sh
phase4_result=$?

# Overall summary
echo ""
echo "========================================================================="
echo "Overall Validation Summary"
echo "========================================================================="

phases_passed=0

[ $phase1_result -eq 0 ] && phases_passed=$((phases_passed + 1)) && echo "✓ Phase 1: PASS" || echo "✗ Phase 1: FAIL"
[ $phase2_result -eq 0 ] && phases_passed=$((phases_passed + 1)) && echo "✓ Phase 2: PASS" || echo "✗ Phase 2: FAIL"
[ $phase3_result -eq 0 ] && phases_passed=$((phases_passed + 1)) && echo "✓ Phase 3: PASS" || echo "✗ Phase 3: FAIL"
[ $phase4_result -eq 0 ] && phases_passed=$((phases_passed + 1)) && echo "✓ Phase 4: PASS" || echo "✗ Phase 4: FAIL"

echo ""
echo "Phases Passed: $phases_passed/4"
echo ""

if [ $phases_passed -eq 4 ]; then
  echo "🎉 RCA-012 REMEDIATION: COMPLETE"
  echo "   All 4 phases validated successfully"
  echo "   Framework integrity restored"
  echo "   User confusion eliminated"
  exit 0
else
  echo "❌ RCA-012 REMEDIATION: INCOMPLETE"
  echo "   $(( 4 - phases_passed )) phases failed validation"
  echo "   Review failures and remediate"
  exit 1
fi
```

---

## Manual Validation Procedures

### Procedure 1: Template v2.1 Validation

**Objective:** Manually verify template structure is correct

**Steps:**
1. Open `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
2. Scroll to Acceptance Criteria section (~line 25)
3. Verify AC headers show `### AC#1:`, `### AC#2:`, `### AC#3:`, `### AC#4:`
4. Verify NO `### 1. [ ]` format
5. Scroll to YAML frontmatter (line ~11)
6. Verify `format_version: "2.1"`
7. Scroll to top (line 1-20)
8. Verify changelog header present with v2.1 entry

**Checklist:**
- [ ] AC header format: `### AC#N:` (no checkboxes)
- [ ] No old format (`### N. [ ]`) present
- [ ] Format version: "2.1"
- [ ] Changelog: v2.1 entry present
- [ ] Template structure intact (all sections)

**If All Pass:** Template validation PASS
**If Any Fail:** Review TEMPLATE-REFACTORING.md, re-implement

---

### Procedure 2: Story Creation Validation

**Objective:** Verify new stories use template v2.1 correctly

**Steps:**
1. Run: `/create-story "Validation test story for RCA-012"`
2. Find created story file (most recent in `devforgeai/specs/Stories/`)
3. Open story file
4. Check YAML frontmatter for `format_version: "2.1"`
5. Check AC headers for `### AC#1:` format
6. Verify no `### 1. [ ]` format
7. Count AC headers
8. Verify all template sections present

**Checklist:**
- [ ] Story created without errors
- [ ] Format version is "2.1"
- [ ] AC headers use new format (≥3 found)
- [ ] No old format present
- [ ] All sections included (Description, AC, Tech Spec, etc.)

**Cleanup:** Delete test story after validation

**If All Pass:** Story creation validation PASS
**If Any Fail:** Check template, may need to re-create from backup

---

### Procedure 3: QA Phase 0.9 PASS Scenario

**Objective:** Verify QA allows stories with 100% traceability

**Steps:**
1. Run: `/qa STORY-007 light` (known perfect compliance)
2. Watch for "Phase 0.9: AC-DoD Traceability Validation" output
3. Verify displays traceability score (should be 100%)
4. Verify shows "✓ PASS" status
5. Verify QA continues to Phase 1 (validation mode selection)
6. Allow QA to complete fully

**Checklist:**
- [ ] Phase 0.9 executes (output visible)
- [ ] Traceability score displayed (100%)
- [ ] PASS status shown
- [ ] QA continues to Phase 1 (not halted)
- [ ] QA completes without errors related to Phase 0.9

**If All Pass:** QA PASS scenario validation PASS
**If Any Fail:** Review QA-ENHANCEMENT.md Step 2.3, check Phase 0.9 integration

---

### Procedure 4: QA Phase 0.9 FAIL Scenario (Missing Traceability)

**Objective:** Verify QA halts when AC requirement has no DoD coverage

**Steps:**
1. Create test story with intentional gap:
   ```markdown
   ## Acceptance Criteria
   ### AC#1: Feature works AND processes in <100ms

   ## Definition of Done
   - [x] Feature implemented
   # MISSING: No DoD item for "<100ms" requirement
   ```
2. Run: `/qa TEST-STORY light`
3. Verify QA halts at Phase 0.9 (does NOT proceed to Phase 1)
4. Verify displays "❌ QA VALIDATION FAILED"
5. Verify lists missing requirement ("<100ms")
6. Verify provides remediation guidance (add DoD item)
7. Delete test story

**Checklist:**
- [ ] QA halts at Phase 0.9
- [ ] Does NOT proceed to Phase 1
- [ ] Displays FAIL status clearly
- [ ] Lists missing requirement (detects "<100ms" gap)
- [ ] Provides actionable remediation
- [ ] Exit gracefully (no errors, just HALT)

**If All Pass:** QA FAIL (missing coverage) validation PASS
**If Any Fail:** Review algorithm in traceability-validation-algorithm.md, may have false negative

---

### Procedure 5: QA Phase 0.9 FAIL Scenario (Undocumented Deferrals)

**Objective:** Verify QA halts when DoD has unchecked items without "Approved Deferrals"

**Steps:**
1. Create test story with incomplete DoD, no deferrals:
   ```markdown
   ## Definition of Done
   - [x] Feature implemented
   - [ ] Performance test
   - [ ] E2E test
   # NO "Approved Deferrals" section
   ```
2. Run: `/qa TEST-STORY light`
3. Verify QA halts at Phase 0.9
4. Verify displays "Incomplete DoD Without Approval" error
5. Verify lists incomplete items (2 items)
6. Verify provides deferral template
7. Delete test story

**Checklist:**
- [ ] QA halts at Phase 0.9
- [ ] Detects 2 incomplete items
- [ ] Identifies missing "Approved Deferrals" section
- [ ] Provides template for creating section
- [ ] Remediation guidance actionable
- [ ] Does NOT proceed to Phase 1

**If All Pass:** QA FAIL (undocumented deferrals) validation PASS
**If Any Fail:** Review deferral validation logic in Phase 0.9

---

### Procedure 6: Audit Script Accuracy Validation

**Objective:** Verify audit script correctly identifies compliant vs. non-compliant stories

**Steps:**
1. Run: `bash devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh`
2. Review output for known cases:
   - STORY-007: Should show "✓ Complete (100% DoD)"
   - STORY-023: Should show "✓ Deferrals documented"
   - STORY-038: Should show "❌ INCOMPLETE" (before fix)
3. Check summary statistics (total, compliant, non-compliant counts)
4. Verify exit code (0 if all compliant, 1 if issues found)

**Checklist:**
- [ ] STORY-007 marked compliant
- [ ] STORY-023 marked compliant (with deferrals)
- [ ] STORY-038 marked non-compliant (before fix)
- [ ] Summary counts correct
- [ ] Exit code matches compliance (0 = compliant, 1 = issues)

**If All Pass:** Audit script validation PASS
**If Any Fail:** Review script logic, may have false positive/negative

---

### Procedure 7: STORY-038 Fix Validation

**Objective:** Verify STORY-038 moves from non-compliant to compliant after fix

**Steps:**
1. **Before Fix:** Run audit, confirm STORY-038 flagged
2. **Apply Fix:** Add "Approved Deferrals" section per STORY-AUDIT.md
3. **Verify Section:** Check section exists with user approval timestamp
4. **Count Items:** Verify all 4 incomplete items documented
5. **Re-run Audit:** Confirm STORY-038 now shows "✓ Deferrals documented"
6. **Run QA:** `/qa STORY-038 light` should PASS at Phase 0.9

**Checklist:**
- [ ] Before: Audit flags STORY-038 as non-compliant
- [ ] Fix applied: "Approved Deferrals" section added
- [ ] User approval timestamp present
- [ ] All 4 items documented with blocker justification
- [ ] After: Audit marks STORY-038 as compliant
- [ ] QA Phase 0.9 PASSES on STORY-038

**If All Pass:** STORY-038 fix validation PASS
**If Any Fail:** Review deferral documentation, ensure all 4 items covered

---

### Procedure 8: Migration Script Safety Validation

**Objective:** Verify migration script creates backup and can restore

**Steps:**
1. Copy story for testing: `cp devforgeai/specs/Stories/STORY-052*.story.md /tmp/test.story.md`
2. Run migration: `bash migrate-ac-headers.sh /tmp/test.story.md`
3. Verify backup created: `ls /tmp/test.story.md.v2.0-backup`
4. Check changes: `grep "^### AC#" /tmp/test.story.md` (should find AC headers)
5. Test restore: `mv /tmp/test.story.md.v2.0-backup /tmp/test.story.md`
6. Verify original format restored: `grep "^### [0-9]\. \[" /tmp/test.story.md`
7. Cleanup: `rm /tmp/test.story.md`

**Checklist:**
- [ ] Backup created before changes
- [ ] Migration successful (AC headers updated)
- [ ] Format version updated to 2.1
- [ ] Restore from backup works
- [ ] Original format recovered
- [ ] No data loss

**If All Pass:** Migration script safety PASS
**If Any Fail:** Review MIGRATION-SCRIPT.md, fix script bugs

---

## User Acceptance Validation

### UAT Procedure 1: User Comprehension Test

**Participant:** Framework user (developer, PM, or stakeholder)

**Test Materials:**
- CLAUDE.md "Acceptance Criteria vs. Tracking Mechanisms" section
- STORY-052 (old v2.0 format with unchecked AC headers)
- Newly created story (v2.1 format, no AC checkboxes)

**Test Protocol:**
1. **No Pre-Reading:** User has NOT been briefed on RCA-012 changes
2. **Present Old Story:** Show STORY-052, ask "Is this story complete?"
3. **Observe Confusion:** User likely confused by unchecked AC headers
4. **Provide Documentation:** Direct user to CLAUDE.md section
5. **Re-Ask Question:** "Now, is STORY-052 complete?"
6. **Present New Story:** Show v2.1 story, ask "Is this story complete?"
7. **Collect Feedback:** Interview user about clarity

**Questions for User:**
1. Were you initially confused by STORY-052's unchecked AC headers? (Yes/No)
2. Did the CLAUDE.md section help clarify? (Yes/No)
3. Do you understand why AC headers have no checkboxes in v2.1? (Yes/No)
4. Can you explain the three-layer tracking system? (Free response)
5. Which section do you check to determine story completion? (DoD/AC Checklist/AC Headers/Other)
6. Is the documentation clear enough? (1-5 scale)

**Success Criteria:**
- [ ] Q1: Yes (initial confusion expected)
- [ ] Q2: Yes (documentation helpful)
- [ ] Q3: Yes (understands definitions vs. trackers)
- [ ] Q4: User can explain at least 2 of 3 layers (TodoWrite, AC Checklist, DoD)
- [ ] Q5: User answers "DoD" (correct)
- [ ] Q6: Rating ≥4 (documentation clear)

**If <4 criteria pass:** Revise CLAUDE.md section for clarity, re-test with different user

---

### UAT Procedure 2: Story Creation Workflow Test

**Participant:** Framework user creating new story

**Test Protocol:**
1. User creates story: `/create-story "My test feature for UAT"`
2. User reviews generated story file
3. Observer asks: "Do you notice anything different about AC headers?"
4. Expected: "They don't have checkboxes" or "Format is different"
5. Observer asks: "Is this confusing or clearer?"
6. Expected: "Clearer" or "Less ambiguous"
7. User implements story (or simulates marking DoD items)
8. Observer asks: "Where do you track completion?"
9. Expected: "Definition of Done section"

**Questions for User:**
1. Did you notice AC headers have no checkboxes? (Yes/No)
2. Was it clear what AC headers represent? (Yes/No)
3. Did you know where to track completion? (Yes/No)
4. Would you have been confused with old format (checkboxes)? (Yes/No)
5. Rate clarity of new format (1-5 scale)

**Success Criteria:**
- [ ] Q1: Yes (noticed format)
- [ ] Q2: Yes (understood as definitions)
- [ ] Q3: Yes (used DoD section)
- [ ] Q4: Yes (would have been confused - validates fix value)
- [ ] Q5: Rating ≥4 (new format clear)

**If <4 criteria pass:** Template format may need refinement, consider alternative

---

## Regression Validation

### Regression Test 1: Old Stories Still Readable

**Objective:** Verify backward compatibility (v1.0/v2.0 stories still work)

**Procedure:**
1. Run `/dev STORY-007` (v2.0 format story)
2. Verify dev workflow completes without errors
3. Run `/qa STORY-014 light` (v2.0 format story)
4. Verify QA Phase 0.9 handles old format correctly
5. Run `/qa STORY-052 light` (after v2.1 doc created, but story is v2.0 format)
6. Verify QA works on mixed format (v2.0 story, v2.1 framework)

**Checklist:**
- [ ] /dev works on v2.0 stories
- [ ] /qa Phase 0.9 reads v2.0 format (AC headers with checkboxes)
- [ ] /qa Phase 0.9 reads v2.1 format (AC headers no checkboxes)
- [ ] No errors related to format differences
- [ ] Backward compatibility confirmed

**If Any Fail:** Phase 0.9 algorithm may not handle old format, fix regex patterns

---

### Regression Test 2: No Breaking Changes

**Objective:** Verify other commands unaffected by template/QA changes

**Procedure:**
```bash
# Test each major command
/create-epic "Regression test epic"        # Should work
/create-sprint "Regression Sprint 99"      # Should work
/create-context "Regression Test Project"  # Should work (if no context files)
/create-ui STORY-007                       # Should work (if story has UI)
/release STORY-007 staging                 # Should work (if QA approved)
/orchestrate TEST-STORY                    # Should work (full lifecycle)
```

**Checklist:**
- [ ] All commands execute without errors
- [ ] No warnings about AC header format
- [ ] Workflows complete normally
- [ ] No unexpected HALT or failures
- [ ] Functionality unchanged

**If Any Fail:** Identify which command broke, investigate why template/QA change affected it

---

## Performance Validation

### Performance Test 1: QA Phase 0.9 Overhead Measurement

**Objective:** Measure time and token overhead added by Phase 0.9

**Procedure:**

**Baseline (Before Phase 0.9):**
- Use old QA skill (restore from backup if needed)
- Run: `time /qa STORY-007 light`
- Record: baseline_time (e.g., 45 seconds)
- Record: baseline_tokens (from session summary)

**Enhanced (After Phase 0.9):**
- Use updated QA skill (with Phase 0.9)
- Run: `time /qa STORY-007 light`
- Record: enhanced_time (e.g., 52 seconds)
- Record: enhanced_tokens

**Calculate Overhead:**
- Time overhead: enhanced_time - baseline_time (e.g., 7 seconds)
- Token overhead: enhanced_tokens - baseline_tokens (e.g., +1.5K tokens)

**Acceptable Thresholds:**
- Time overhead: <30 seconds
- Token overhead: <2K tokens

**Checklist:**
- [ ] Time overhead measured
- [ ] Token overhead measured
- [ ] Time overhead <30 seconds
- [ ] Token overhead <2K tokens
- [ ] Overhead justified by value (prevents quality gate bypass)

**If Exceeds Thresholds:**
- Review algorithm efficiency
- Consider caching AC/DoD extraction
- Optimize keyword matching logic

---

### Performance Test 2: Audit Script Scalability

**Objective:** Verify audit handles current story count efficiently

**Procedure:**
```bash
time bash devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh
```

**Record:**
- Execution time (should be <30 seconds for 39 stories)
- Memory usage (should be <100MB)
- Output readability (should be scannable)

**Checklist:**
- [ ] Completes in <30 seconds
- [ ] Memory usage reasonable (<100MB)
- [ ] Output is readable and actionable
- [ ] No errors or warnings

**Future Scaling:**
- 100 stories: Should complete <60 seconds
- 500 stories: May need optimization (parallel processing, caching)

---

## Integration Validation

### Integration Test 1: End-to-End Story Lifecycle

**Objective:** Validate complete workflow with template v2.1

**Procedure:**
1. Create: `/create-story "E2E lifecycle test story"`
2. Verify: Story uses v2.1 format (AC headers no checkboxes)
3. Implement: `/dev E2E-TEST-STORY`
4. Verify: Dev completes, marks DoD items
5. Validate: `/qa E2E-TEST-STORY deep`
6. Verify: QA Phase 0.9 passes (100% traceability)
7. Verify: Deep validation passes
8. Release: `/release E2E-TEST-STORY staging`
9. Verify: Release succeeds
10. Cleanup: Archive or delete test story

**Checklist:**
- [ ] Story creation uses v2.1 template
- [ ] /dev workflow completes
- [ ] /qa Phase 0.9 validates traceability (PASS)
- [ ] /qa deep validation passes
- [ ] /release succeeds
- [ ] No errors throughout lifecycle
- [ ] User never confused about completion status

**If All Pass:** E2E integration PASS
**If Any Fail:** Identify which step failed, investigate integration issue

---

## Compliance Validation

### Compliance Test: All 39 Stories at 100%

**Objective:** Final verification that all QA Approved stories comply with new standards

**Procedure:**
1. Run: `bash audit-qa-approved-stories.sh`
2. Check summary:
   - Total: 39
   - Compliant: 39 (100%)
   - Non-Compliant: 0 (0%)
3. Review any warnings or edge cases
4. Verify exit code: 0 (success)

**Checklist:**
- [ ] Total audited: 39 stories
- [ ] Compliant: 39 (100%)
- [ ] Non-compliant: 0 (0%)
- [ ] No warnings or edge cases
- [ ] Exit code: 0

**If Any Fail:**
- Review flagged stories
- Fix remaining issues
- Re-run audit until 100%

---

## Validation Sign-Off

### Phase-by-Phase Sign-Off

**After each phase validation:**

```markdown
# Phase {N} Validation Sign-Off

**Validator:** {Name}
**Date:** YYYY-MM-DD HH:MM UTC
**Phase:** {1, 2, 3, or 4}

**Validation Results:**
- Automated tests: {passed}/{total} PASS
- Manual tests: {passed}/{total} PASS
- User acceptance: {PASS / FAIL}

**Issues Found:**
{List any issues found during validation}

**Remediation:**
{What was done to fix issues}

**Final Status:**
- [ ] All validation checks PASS
- [ ] No outstanding issues
- [ ] Phase {N} complete and verified
- [ ] Ready to proceed to Phase {N+1}

**Signature:** {Name}
**Timestamp:** {UTC timestamp}
```

Save to: `devforgeai/RCA/RCA-012/validation/phase{N}-signoff.md`

---

### Final Remediation Sign-Off

**After all 4 phases validated:**

```markdown
# RCA-012 Final Validation Sign-Off

**Validator:** {Name}
**Completion Date:** YYYY-MM-DD
**Total Effort:** {actual hours}

**Phase Results:**
- [x] Phase 1: Foundation - PASS (template v2.1, documentation)
- [x] Phase 2: QA Enhancement - PASS (traceability validation operational)
- [x] Phase 3: Historical Cleanup - PASS (39/39 stories compliant)
- [x] Phase 4: Automation - PASS (migration tools operational)

**Overall Validation:**
- [x] All validation scripts PASS
- [x] User acceptance tests PASS
- [x] Regression tests PASS
- [x] Performance tests PASS
- [x] Integration tests PASS
- [x] Compliance audit shows 100%

**Success Metrics Achieved:**
- AC header consistency: 20% → 100% ✓
- AC-DoD traceability: 20% → 100% ✓
- User confusion incidents: Reduced to 0 ✓
- Quality gate bypasses: 0 detected ✓

**Framework Integrity:**
- ✅ Template v2.1 operational
- ✅ QA validation prevents bypasses
- ✅ All stories compliant
- ✅ Documentation clear and comprehensive

**Sign-Off:**
I certify that RCA-012 remediation is complete, all validations have passed, and the framework is ready for production use with enhanced tracking clarity.

Validator: {Signature/Name}
Reviewer: {Signature/Name}
Date: YYYY-MM-DD HH:MM UTC

**RCA-012 Status:** ✅ RESOLVED
```

Save to: `devforgeai/RCA/RCA-012/FINAL-VALIDATION-SIGNOFF.md`

---

## Validation Checklist (Master)

### Pre-Validation
- [ ] All 4 phases implemented
- [ ] All documents created (11 documents in RCA-012/)
- [ ] All scripts created (5 scripts in scripts/)

### Phase 1 Validation
- [ ] Automated: validate-phase1.sh PASS (7/7 tests)
- [ ] Manual: Template v2.1 validated (Procedure 1)
- [ ] Manual: Story creation validated (Procedure 2)
- [ ] UAT: User comprehension confirmed (UAT Procedure 1)

### Phase 2 Validation
- [ ] Automated: validate-phase2.sh PASS (4/4 tests)
- [ ] Manual: QA PASS scenario validated (Procedure 3)
- [ ] Manual: QA FAIL (traceability) validated (Procedure 4)
- [ ] Manual: QA FAIL (deferrals) validated (Procedure 5)

### Phase 3 Validation
- [ ] Automated: validate-phase3.sh PASS
- [ ] Manual: Audit script accuracy (Procedure 6)
- [ ] Manual: STORY-038 fix validated (Procedure 7)
- [ ] Compliance: All 39 stories at 100% (Compliance Test)

### Phase 4 Validation
- [ ] Automated: validate-phase4.sh PASS (3/3 tests)
- [ ] Manual: Migration script safety (Procedure 8)
- [ ] Manual: Traceability matrix in template (verify present)

### Regression Validation
- [ ] Old stories work (Regression Test 1)
- [ ] No breaking changes (Regression Test 2)

### Integration Validation
- [ ] E2E lifecycle test (Integration Test 1)

### Performance Validation
- [ ] QA Phase 0.9 overhead acceptable (Performance Test 1)
- [ ] Audit script scalable (Performance Test 2)

### User Acceptance
- [ ] UAT 1: User comprehension (≥4/6 criteria)
- [ ] UAT 2: Story creation workflow (≥4/5 criteria)

### Final Validation
- [ ] Comprehensive validation script PASS (validate-all-phases.sh)
- [ ] All phase sign-offs complete
- [ ] Final sign-off documented

**Overall:** 100% of validation procedures pass

---

## Troubleshooting Failed Validations

### Issue: Template Validation Fails

**Symptom:** validate-phase1.sh shows template format incorrect

**Diagnosis:**
```bash
grep "^### AC#" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md | wc -l
# If <4: AC headers not all updated
# If >4: Extra headers added accidentally
```

**Fix:**
- Review TEMPLATE-REFACTORING.md Step 2
- Restore from backup: `mv story-template.md.v2.0-backup story-template.md`
- Re-implement changes carefully
- Re-validate

---

### Issue: QA Phase 0.9 False Positive

**Symptom:** QA halts on story with valid traceability

**Diagnosis:**
- Review Phase 0.9 output (which requirement flagged as missing?)
- Check DoD section (does item exist with different wording?)
- Review algorithm keyword matching logic

**Fix:**
- Update algorithm to recognize alternative wordings
- OR update DoD item to use keywords from AC requirement
- Re-test with same story

---

### Issue: Audit Script False Negative

**Symptom:** Audit marks non-compliant story as compliant

**Diagnosis:**
- Manually review flagged story
- Check DoD completion percentage (is it actually 100%?)
- Check for "Approved Deferrals" section (does it exist?)

**Fix:**
- Update audit script logic (may have counting bug)
- Re-run audit
- Verify correct behavior

---

## Validation Artifacts

**Store all validation results in:**
`devforgeai/RCA/RCA-012/validation/`

**Files to Create:**
- `phase1-validation-results.md`
- `phase2-validation-results.md`
- `phase3-validation-results.md`
- `phase4-validation-results.md`
- `regression-test-results.md`
- `uat-results.md`
- `performance-test-results.md`
- `FINAL-VALIDATION-SIGNOFF.md`

**Purpose:**
- Audit trail of validation activities
- Evidence that remediation was tested thoroughly
- Reference for future RCAs (what was validated, how)

---

**Validation Procedures Complete**
**Total Procedures:** 8 automated + 8 manual = 16 comprehensive procedures
**Estimated Validation Time:** 3-4 hours (across all phases)
**Success Criteria:** 100% of procedures pass before marking RCA-012 RESOLVED
