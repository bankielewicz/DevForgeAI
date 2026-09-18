# QA Result Interpreter -- Display Templates

Reference content extracted from the core agent definition. Loaded on-demand during Step 5 (Generate Display Template).

---

## Template Selection Matrix

```
MODE: Light
  STATUS: PASSED → template="light_pass"
  STATUS: FAILED → template="light_fail_quick"

MODE: Deep
  STATUS: PASSED → template="deep_pass_full"

  STATUS: FAILED
    # Prioritize multiple violations template when >2 violations exist
    IF total_violation_count > 2:
      → template="deep_fail_multiple"
    ELSE IF deferral_violations present:
      → template="deep_fail_deferral"
    ELSE IF coverage_violations present:
      → template="deep_fail_coverage"
    ELSE IF compliance_violations present:
      → template="deep_fail_compliance"
    ELSE:
      → template="deep_fail_standard"

    # Note: deep_fail_multiple recommends /review-qa-reports workflow
```

**Template Generation (Haiku-optimized):**

Each template includes:
1. Title with status emoji
2. Summary section (1-2 sentences)
3. Key metrics (mode-specific)
4. Violation summary (by severity)
5. Recommended next steps (based on violations)
6. Link to detailed report

---

## Light Pass Template

```markdown
## ✅ Light QA Validation PASSED - {STORY_ID}

**Story:** {STORY_TITLE}
**Mode:** Light
**Status:** {CURRENT_STATUS} (unchanged)

### Quick Checks
✓ Build successful
✓ All tests passing ({PASS_COUNT}/{TOTAL_COUNT})
✓ No critical anti-patterns detected

**Note:** Light validation passed. Continue development or run deep validation when Dev Complete.

**Next Steps:**
- Continue implementation
- Run `/qa {STORY_ID} deep` when story is Dev Complete

---
```

## Deep Pass Template

```markdown
## ✅ Deep QA Validation PASSED - {STORY_ID}

**Story:** {STORY_TITLE}
**Mode:** Deep
**Status:** Dev Complete → QA Approved ✓

### Validation Results

**Test Coverage:**
- Business Logic: {BL_PCT}% (≥95% ✓)
- Application: {APP_PCT}% (≥85% ✓)
- Infrastructure: {INFRA_PCT}% (≥80% ✓)
- Overall: {OVERALL_PCT}%

**Code Quality:**
- Complexity: {AVG_CC} avg (max 10 ✓)
- Maintainability: {MI} (≥70 ✓)
- Duplication: {DUP_PCT}% (≤5% ✓)
- Documentation: {DOC_PCT}% (≥80% ✓)

**Violations:**
- CRITICAL: 0
- HIGH: 0
- MEDIUM: {MED_COUNT}
- LOW: {LOW_COUNT}

**Spec Compliance:**
✓ All acceptance criteria validated
✓ API contracts match specification
✓ Non-functional requirements met

### Recommendation
✅ **APPROVE** - Story meets all quality gates and is ready for release.

**Next Steps:**
1. Review detailed report: devforgeai/qa/reports/{STORY_ID}-qa-report.md
2. Deploy: `/release {STORY_ID}`

---
```

## Deferral Failure Template

```markdown
## ❌ QA Validation FAILED - Deferral Violations - {STORY_ID}

**Story:** {STORY_TITLE}
**Mode:** {MODE}
**Reason:** Deferred Definition of Done items require resolution

### Deferral Issues

**Summary:**
- Total deferred items: {COUNT}
- Validation violations: {VIOLATION_COUNT}
  - CRITICAL: {CRIT_COUNT} (blocks approval)
  - HIGH: {HIGH_COUNT} (blocks approval)
  - MEDIUM: {MED_COUNT}

**Violations Requiring Action:**

{FOR each CRITICAL/HIGH violation:}
**{SEVERITY}** - {ITEM_NAME}
- Current reason: "{CURRENT_REASON}"
- Issue: {VIOLATION_MESSAGE}
- Required action: {REMEDIATION}

### Resolution Required

Choose one approach:

**Option 1: Return to Development** (Recommended)
Run: `/dev {STORY_ID}`
- Dev skill will read this QA report
- Dev skill will help resolve deferral issues
- Options: complete work, create ADR, fix justifications

**Option 2: Review Detailed Report First**
See: devforgeai/qa/reports/{STORY_ID}-qa-report.md
- Review full deferral validation results
- Understand all violations and remediation options
- Then run `/dev {STORY_ID}` to fix

**Option 3: Fix Manually**
- Review violations above
- Fix justifications or complete deferred work
- Re-run: `/qa {STORY_ID}` to validate

**Option 4: Batch Remediation** (if multiple deferrals across stories)
Run: `/review-qa-reports --source local`
- Processes deferral issues systematically across all gap files
- Creates remediation stories with proper prioritization
- Links stories to source QA reports
- Tracks deferred items in technical debt register

---
```

## Coverage Failure Template

```markdown
## ⚠️ Coverage Thresholds Not Met - {STORY_ID}

**Story:** {STORY_TITLE}
**Mode:** Deep

### Coverage Results
- Business Logic: {PCT}% ❌ (required ≥95%, gap: {DELTA}%)
- Application: {PCT}% ❌ (required ≥85%, gap: {DELTA}%)
- Infrastructure: {PCT}% ✓ (required ≥80%)

### Uncovered Code
{List top 3-5 uncovered methods/files}

### Remediation Options

**Option A: Fix Immediately**
1. Add unit tests for uncovered business logic
2. Add integration tests for uncovered application code
3. Run: `/qa {STORY_ID}` to validate improvements

**Option B: Systematic Analysis** (Recommended for multiple gaps)
Run: `/review-qa-reports --source local`
- Analyzes all coverage gaps across your project
- Creates remediation stories in batch with proper prioritization
- Tracks progress in technical debt register
- Gap file: `devforgeai/qa/reports/{STORY_ID}-gaps.json`

---
```

## Spec Compliance Failure Template

```markdown
## ⚠️ Spec Compliance Issues - {STORY_ID}

**Story:** {STORY_TITLE}
**Mode:** Deep

### Failed Acceptance Criteria
{List AC without test coverage}

### API Contract Mismatches
{List endpoint mismatches}

### Missing Non-Functional Requirements
{List NFRs not validated}

### Required Actions
1. Add tests for missing acceptance criteria
2. Update implementation to match API contracts
3. Implement or validate NFRs
4. Re-run: `/qa {STORY_ID}` to validate

---
```

## Multiple Violations Template

```markdown
## ⚠️ QA Validation FAILED - Multiple Issues - {STORY_ID}

**Story:** {STORY_TITLE}
**Mode:** {MODE}
**Total Violations:** {VIOLATION_COUNT}

### Summary by Type
- Coverage gaps: {COVERAGE_COUNT}
- Anti-pattern violations: {AP_COUNT}
- Deferral issues: {DEFERRAL_COUNT}
- Compliance issues: {COMPLIANCE_COUNT}

### Recommended Approach

Given {VIOLATION_COUNT} violations detected, **systematic remediation** is recommended:

**Run:** `/review-qa-reports --source local`

This command will:
1. Parse gap file: `devforgeai/qa/reports/{STORY_ID}-gaps.json`
2. Aggregate and prioritize all violations by severity
3. Allow you to select which gaps to address
4. Create remediation stories in batch
5. Track deferred items in technical debt register

### Alternative Approaches

**Option A: Return to Development**
Run: `/dev {STORY_ID}`
- Fix issues one by one in TDD workflow
- Suitable for <3 violations

**Option B: Fix Manually**
- Review violations in detailed report
- Fix each issue directly
- Re-run: `/qa {STORY_ID}` to validate

**Detailed Report:** `devforgeai/qa/reports/{STORY_ID}-qa-report.md`

---
```
