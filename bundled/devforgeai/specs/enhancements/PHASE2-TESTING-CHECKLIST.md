# Phase 2 Testing Checklist - Structured Technical Specifications

**Version:** 1.0
**Date:** 2025-11-07
**Phase:** Phase 2 (Structured Templates)
**Testing Duration:** Weeks 4-5 (10 days, ~40 hours)

---

## Test Coverage Summary

| Category | Test Cases | Est. Time | Status |
|----------|------------|-----------|--------|
| **Validator Unit Tests** | 12 | 4h | Pending |
| **Migration Unit Tests** | 10 | 4h | Pending |
| **Format Detection Tests** | 5 | 2h | Pending |
| **Integration Tests** | 8 | 8h | Pending |
| **Pilot Migration** | 10 stories | 12h | Pending |
| **Full Migration** | All stories | 16h | Pending |
| **Regression Tests** | 6 | 4h | Pending |
| **TOTAL** | **51 tests** | **50h** | **0% Complete** |

---

## Unit Tests: Validator (12 cases)

### TC-V1: Valid v2.0 Story (Success Case)

**Objective:** Verify validator accepts correctly formatted v2.0 story

**Test Story:** Create minimal v2.0 story with 1 component
```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Service"
      name: "TestService"
      file_path: "src/TestService.cs"
      requirements:
        - id: "SVC-001"
          description: "Test requirement"
          testable: true
          test_requirement: "Test: Verify service starts"
          priority: "High"
```

**Execute:**
```bash
python validate_tech_spec.py test-story.md
```

**Expected:**
- Exit code: 0
- Output: "✅ VALIDATION PASSED"
- Errors: 0
- Warnings: 0

---

### TC-V2: Missing format_version (Error)

**Objective:** Verify validator catches missing format_version field

**Test:** Remove `format_version` from YAML

**Expected:**
- Exit code: 1
- Error: "Missing 'format_version' field"

---

### TC-V3: Invalid Component Type (Error)

**Objective:** Verify validator rejects unknown component types

**Test:** Use `type: "InvalidType"`

**Expected:**
- Exit code: 1
- Error: "Unknown type 'InvalidType' (valid types: Service, Worker, ...)"

---

### TC-V4: Missing Required Field (Error)

**Objective:** Verify validator catches missing required fields per component type

**Test:** Service component without `requirements` field

**Expected:**
- Exit code: 1
- Error: "TestService (Service): Missing required field 'requirements'"

---

### TC-V5: Missing Test Requirement (Warning)

**Objective:** Verify validator warns if requirement lacks test_requirement

**Test:** Requirement without `test_requirement` field

**Expected:**
- Exit code: 0 (warnings don't fail)
- Warning: "SVC-001: Missing 'test_requirement' field"

---

### TC-V6: Test Requirement Format (Warning)

**Objective:** Verify validator checks test_requirement format

**Test:** test_requirement: "Should work" (doesn't start with "Test: ")

**Expected:**
- Exit code: 0
- Warning: "test_requirement should start with 'Test: ' prefix"

---

### TC-V7: Duplicate IDs (Error)

**Objective:** Verify validator detects duplicate IDs within scope

**Test:** Two requirements with same ID "SVC-001"

**Expected:**
- Exit code: 1
- Error: "Duplicate ID 'SVC-001' in component_requirements"

---

### TC-V8: All Component Types (Success)

**Objective:** Verify validator accepts all 7 component types

**Test:** Story with Service, Worker, Configuration, Logging, Repository, API, DataModel

**Expected:**
- Exit code: 0
- No errors for any component type

---

### TC-V9: Empty Components Array (Error)

**Objective:** Verify validator requires at least one component

**Test:** `components: []`

**Expected:**
- Exit code: 1
- Error: "No components defined (components array is empty)"

---

### TC-V10: Invalid YAML Syntax (Error)

**Objective:** Verify validator catches YAML syntax errors

**Test:** Malformed YAML (missing colon, bad indentation)

**Expected:**
- Exit code: 1
- Error: "Invalid YAML in tech spec: ..."

---

### TC-V11: NFR Metric Validation (Warning)

**Objective:** Verify validator checks NFR metrics are measurable

**Test:** NFR with vague metric "should be fast"

**Expected:**
- Exit code: 0
- Warning: "NFR-001: metric should be measurable (contain number or threshold)"

---

### TC-V12: v1.0 Story (Warning)

**Objective:** Verify validator detects v1.0 freeform format

**Test:** Story with freeform markdown tech spec (no YAML block)

**Expected:**
- Exit code: 0 (v1.0 is valid, just not v2.0)
- Warning: "Story uses v1.0 freeform format (not structured YAML)"

---

## Unit Tests: Migration Script (10 cases)

### TC-M1: Simple Story Migration (Success)

**Objective:** Migrate simple story (2-3 components)

**Test Story:** CRUD story with basic tech spec

**Execute:**
```bash
python migrate_story_v1_to_v2.py STORY-TEST-001.md --dry-run
```

**Expected:**
- Detects components (configuration, repository, api)
- Generates valid YAML
- No errors

---

### TC-M2: Already v2.0 (Skip)

**Objective:** Verify script detects and skips v2.0 stories

**Test:** v2.0 story

**Expected:**
- Output: "✓ Already v2.0 format (no migration needed)"
- Exit code: 0
- No changes

---

### TC-M3: Backup Creation (Success)

**Objective:** Verify backup created before migration

**Test:** Migrate story with `--backup`

**Expected:**
- Backup file created in `devforgeai/backups/phase2-migration/`
- Original file preserved

---

### TC-M4: Dry Run Mode (No Changes)

**Objective:** Verify --dry-run doesn't modify files

**Test:** Migrate with `--dry-run`

**Expected:**
- Preview shown
- Original file unchanged
- Exit code: 0

---

### TC-M5: Missing Tech Spec Section (Error)

**Objective:** Verify script handles missing tech spec gracefully

**Test:** Story without Technical Specification section

**Expected:**
- Exit code: 1
- Error: "No Technical Specification section found"

---

### TC-M6: Complex Story (7+ components)

**Objective:** Migrate complex story with multiple component types

**Test:** Story with Service + Worker + Configuration + Logging + Repository + API + DataModel

**Expected:**
- All 7 component types detected
- Valid YAML generated
- No data loss

---

### TC-M7: Validation After Migration

**Objective:** Verify `--validate` flag runs validator

**Test:** Migrate with `--validate`

**Expected:**
- Migration completes
- Validator automatically runs
- Exit code matches validation result

---

### TC-M8: Business Rules Extraction

**Objective:** Verify business rules extracted from freeform

**Test:** Story mentioning "Business Rule: Alert severity must be Info, Warning, or Error"

**Expected:**
- business_rules array populated
- Rule text extracted

---

### TC-M9: NFR Extraction

**Objective:** Verify NFRs extracted (especially performance metrics)

**Test:** Story mentioning "< 5 seconds startup time"

**Expected:**
- NFR created with metric "< 5 seconds"
- Category: "Performance"

---

### TC-M10: Batch Migration

**Objective:** Verify batch migration of multiple stories

**Test:** Migrate 3 stories in sequence

**Execute:**
```bash
for story in STORY-001 STORY-002 STORY-003; do
  python migrate_story_v1_to_v2.py devforgeai/specs/Stories/$story.story.md
done
```

**Expected:**
- All 3 migrate successfully
- No file conflicts
- All validated

---

## Integration Tests (8 cases)

### TC-I1: /dev with v2.0 Story

**Objective:** Verify /dev command works with v2.0 stories

**Test:** Run `/dev STORY-V2-TEST`

**Expected:**
- Phase 1 Step 4 detects v2.0 format
- Components extracted via YAML parsing
- Coverage gap detection works (95%+ accuracy)
- Workflow completes successfully

---

### TC-I2: /dev with v1.0 Story (Backward Compat)

**Objective:** Verify /dev still works with v1.0 freeform stories

**Test:** Run `/dev STORY-V1-TEST`

**Expected:**
- Phase 1 Step 4 detects v1.0 format
- Falls back to freeform parsing
- Coverage gap detection works (85% accuracy)
- Workflow completes successfully

---

### TC-I3: Story Creation Generates v2.0

**Objective:** Verify `/create-story` generates v2.0 format by default

**Test:** Run `/create-story "Test feature with API and database"`

**Execute:**
```bash
/create-story "Create user registration API with email validation"
```

**Expected:**
- Generated story has `format_version: "2.0"` in frontmatter
- Tech spec section uses YAML code block
- All components have test requirements
- Validates with validate_tech_spec.py

---

### TC-I4: Migration + Validation Pipeline

**Objective:** End-to-end migration and validation

**Test:** Migrate story then validate

**Execute:**
```bash
python migrate_story_v1_to_v2.py STORY-001.md --validate
```

**Expected:**
- Migration completes
- Validation runs automatically
- Both succeed
- Exit code: 0

---

### TC-I5: Format Detection in Step 4

**Objective:** Verify Step 4.1 format detection works

**Test:** Prepare one v1.0 and one v2.0 story, run /dev on each

**Expected:**
- v1.0: "Detected story format: v1.0"
- v2.0: "Detected story format: v2.0"
- Different parsing paths used
- Both complete successfully

---

### TC-I6: Coverage Analysis Accuracy (v1.0 vs v2.0)

**Objective:** Compare gap detection accuracy between formats

**Test:** Create identical story in both formats, run /dev

**Expected:**
- v1.0: ~85% component detection (some missed)
- v2.0: 95%+ component detection (all found)
- v2.0 detects more gaps (better coverage)

---

### TC-I7: Rollback and Recovery

**Objective:** Verify rollback restores original functionality

**Test:**
1. Migrate 3 stories
2. Rollback all
3. Run /dev on rolled-back stories

**Expected:**
- Rollback completes in <15 min
- Stories restored to v1.0
- /dev works with restored stories

---

### TC-I8: Mixed Format Project

**Objective:** Verify project with both v1.0 and v2.0 stories works

**Test:** Project with 5 v1.0 and 5 v2.0 stories

**Execute:**
```bash
/dev STORY-V1-001  # v1.0 story
/dev STORY-V2-001  # v2.0 story
```

**Expected:**
- Both workflows complete
- Format detection works for each
- No conflicts or errors

---

## Pilot Migration Tests (10 stories)

### Pilot Story Selection Criteria

**Simple stories (3):**
- 2-3 components total
- Basic CRUD operations
- Minimal business rules
- Examples: User registration, basic API

**Medium stories (4):**
- 4-6 components
- Multiple services or workers
- Configuration + logging
- Examples: Background workers, service integration

**Complex stories (3):**
- 8+ components
- Full-stack (API + Service + Worker + Repository + Config + Logging + DataModel)
- Complex business rules
- Examples: Complete feature implementations

---

### Per-Story Pilot Test

**For each of 10 pilot stories:**

**Step 1: Pre-migration checks**
- [ ] Story file exists
- [ ] Backup created
- [ ] Original validated (can run /dev successfully)

**Step 2: Execute migration**
```bash
python migrate_story_v1_to_v2.py devforgeai/specs/Stories/STORY-XXX.md --validate
```

**Step 3: Validate migration**
- [ ] Migration completes (exit code 0)
- [ ] Validation passes (exit code 0)
- [ ] Manual review: YAML quality ≥4/5

**Step 4: Test with /dev**
```bash
/dev STORY-XXX
```
- [ ] Phase 1 completes
- [ ] Step 4 detects v2.0 format
- [ ] Coverage analysis works
- [ ] Workflow completes to end

**Step 5: Comparison**
- [ ] Component count: v1.0 detected vs v2.0 detected
- [ ] Accuracy: v2.0 should detect ≥ v1.0 components
- [ ] No data loss (all requirements preserved)

---

### Pilot Success Criteria

**Technical:**
- [ ] Migration success rate: 100% (10/10 stories)
- [ ] Validation pass rate: ≥90% (9/10 stories)
- [ ] /dev success rate: 100% (10/10 workflows)
- [ ] Parsing accuracy: ≥95% (component detection)

**Quality:**
- [ ] Manual review average: ≥4/5
- [ ] Zero data loss
- [ ] No critical bugs
- [ ] All test requirements preserved

**Performance:**
- [ ] Migration time: <30 min per story
- [ ] Validation time: <30 sec per story
- [ ] /dev time: Unchanged from v1.0 baseline

---

## Regression Tests (6 cases)

### TC-R1: v1.0 Stories Still Work

**Objective:** Ensure v1.0 stories unaffected by Phase 2 changes

**Test:** Run /dev on 3 unmigrated v1.0 stories

**Expected:**
- All workflows complete
- No errors from format detection
- Backward compatibility maintained

---

### TC-R2: Story Creation Unchanged (UX)

**Objective:** Verify story creation user experience unchanged

**Test:** Time `/create-story` before and after Phase 2

**Expected:**
- Time difference: <10% (should be similar)
- User answers same questions
- No new friction

---

### TC-R3: QA Validation Unchanged

**Objective:** Verify /qa works with both v1.0 and v2.0

**Test:** Run /qa on v1.0 and v2.0 stories

**Expected:**
- Both complete successfully
- No format-related errors

---

### TC-R4: Orchestration Workflow

**Objective:** Verify /orchestrate works with v2.0

**Test:** Run `/orchestrate STORY-V2-TEST`

**Expected:**
- Dev → QA → Release pipeline completes
- No failures due to format

---

### TC-R5: Template Backward Compatibility

**Objective:** Verify old stories can still be edited

**Test:** Edit v1.0 story (add AC), save, validate

**Expected:**
- Story remains v1.0 (no forced migration)
- Edit successful
- /dev still works

---

### TC-R6: No Breaking Changes

**Objective:** Comprehensive regression across all commands

**Test:** Run all 11 slash commands

**Expected:**
- All commands functional
- No format-related errors
- Backward compatibility 100%

---

## Performance Benchmarks

### Validator Performance

**Test:** Validate 100 v2.0 stories

**Metrics:**
- Average time per story: Target <500ms
- Memory usage: Target <50MB
- CPU usage: Target <25%

---

### Migration Performance

**Test:** Migrate 50 stories (batch)

**Metrics:**
- Average time per story: Target <15 min (with AI-assisted)
- Success rate: Target ≥95%
- Accuracy: Target ≥95% (component detection)

---

### Format Detection Performance

**Test:** Run /dev on 20 stories (mixed v1.0 and v2.0)

**Metrics:**
- Format detection overhead: Target <100ms
- No impact on overall /dev time: Target <5% difference

---

## Acceptance Criteria (Phase 2 Complete)

### Must Meet ALL (Critical)

- [ ] Structured format specification complete (STRUCTURED-FORMAT-SPECIFICATION.md)
- [ ] Validator functional (validate_tech_spec.py passes all 12 unit tests)
- [ ] Migration script reliable (≥95% success rate on pilot)
- [ ] Dual format support working (/dev works with v1.0 and v2.0)
- [ ] Story template updated (generates v2.0 by default)
- [ ] Pilot migration successful (10/10 stories, 100% success)
- [ ] Zero data loss during migration
- [ ] All validation tests pass (51/51)

### Should Meet 4 of 5 (High Priority)

- [ ] Parsing accuracy ≥95% (v2.0 format)
- [ ] Manual review quality ≥4/5 average
- [ ] Migration time <30 min per story
- [ ] User satisfaction ≥80%
- [ ] Documentation complete (guides, FAQ, examples)

### Nice to Have (Medium Priority)

- [ ] AI-assisted migration with LLM (95%+ accuracy)
- [ ] Batch migration tooling
- [ ] Migration progress dashboard
- [ ] Automated quality scoring

---

## Test Execution Plan

### Week 4 Day 1-2: Validator Testing (10 hours)

**Execute:**
1. TC-V1 through TC-V12 (12 validator tests)
2. Document results
3. Fix any validator bugs
4. Re-test until 100% pass

**Deliverable:** All validator tests passing

---

### Week 4 Day 3: Migration Testing (6 hours)

**Execute:**
1. TC-M1 through TC-M10 (10 migration tests)
2. Document results
3. Note migration accuracy (likely <95% without AI)
4. Identify improvement areas

**Deliverable:** Migration tests results, enhancement recommendations

---

### Week 4 Day 4: Integration Testing (8 hours)

**Execute:**
1. TC-I1 through TC-I8 (8 integration tests)
2. Test /dev, /create-story, /qa with v2.0
3. Verify dual format support
4. Test rollback procedures

**Deliverable:** Integration test results

---

### Week 4 Day 5: Pilot Migration (12 hours)

**Execute:**
1. Select 10 pilot stories (simple, medium, complex)
2. Migrate each story
3. Validate each migration
4. Test each with /dev
5. Manual review (quality scoring)

**Deliverable:** 10 migrated stories, quality metrics

---

### Week 5 Day 1: Pilot Review & Decision (4 hours)

**Analyze pilot results:**
- Migration success rate: __/10
- Validation pass rate: __/10
- /dev success rate: __/10
- Average quality score: __/5
- Parsing accuracy: __%

**Make GO/NO-GO decision:**
- ✅ GO: All criteria met → Full migration (Week 5 Day 2-4)
- ⚠️ ITERATE: Issues found → Fix and re-pilot
- 🛑 NO-GO: Critical failures → Rollback Phase 2

---

### Week 5 Day 2-4: Full Migration (If GO) (16 hours)

**Execute:**
1. Backup all stories
2. Count total stories
3. Batch migrate (10 at a time)
4. Validate each batch
5. Manual spot-check (20%)

**Deliverable:** All stories migrated to v2.0

---

### Week 5 Day 5: Regression Testing (4 hours)

**Execute:**
1. TC-R1 through TC-R6 (6 regression tests)
2. Run performance benchmarks
3. Test all 11 slash commands
4. Verify no breaking changes

**Deliverable:** Regression test results, Phase 2 complete

---

## Bug Tracking Template

**For each bug found during testing:**

```markdown
### Bug #[N]: [Brief Description]

**Severity:** Critical / High / Medium / Low
**Component:** Validator / Migration Script / Format Detection / Other
**Discovered In:** [Test case ID]

**Reproduction:**
1. [Step 1]
2. [Step 2]
3. [Expected vs Actual]

**Root Cause:** [Analysis]

**Fix:** [Solution]

**Verification:**
- [ ] Fix implemented
- [ ] Test case re-run (passes)
- [ ] Regression tests (no new issues)
```

---

## Success Metrics

### Phase 2 Success Dashboard

**Technical Metrics:**
- Migration success rate: Target 100%, Actual: ___%
- Validation pass rate: Target ≥90%, Actual: ___%
- Parsing accuracy: Target ≥95%, Actual: ___%
- /dev success rate: Target 100%, Actual: ___%

**Quality Metrics:**
- Manual review average: Target ≥4/5, Actual: ___/5
- Data loss: Target 0%, Actual: ___%
- Bug count: Target <5 critical, Actual: ___

**Performance Metrics:**
- Migration time: Target <30 min, Actual: ___ min avg
- Validator time: Target <500ms, Actual: ___ ms avg
- /dev time impact: Target <5%, Actual: ___%

**User Metrics:**
- User satisfaction: Target ≥80%, Actual: ___%
- Time to migrate story: Target <1.5h, Actual: ___ h avg
- Story creation time: Target <10 min, Actual: ___ min

---

## Decision Point 2 (End of Week 5)

### GO Criteria (Proceed to Phase 3)

**All technical criteria met:**
- ✅ Migration success 100%
- ✅ Parsing accuracy ≥95%
- ✅ Validation passing ≥90%
- ✅ /dev works 100%
- ✅ No critical bugs
- ✅ User satisfaction ≥80%

**Action:** Create Phase 3 implementation plan, proceed to automated validation

---

### ITERATE Criteria

**Some criteria missed:**
- ⚠️ Parsing accuracy 85-95%
- ⚠️ User satisfaction 60-80%
- ⚠️ Minor bugs (5-10)
- ⚠️ Performance slower than expected

**Action:** Week 6 optimization, re-test, re-evaluate

---

### NO-GO Criteria

**Critical failures:**
- 🛑 Migration success <90%
- 🛑 Parsing accuracy <85%
- 🛑 Data loss occurred
- 🛑 Critical bugs (>5)
- 🛑 User rejection

**Action:** Rollback Phase 2, document issues, reassess approach

---

## Test Results Log Template

```markdown
# Phase 2 Testing Results

**Date:** YYYY-MM-DD
**Tester:** [Name]
**Duration:** [Hours]

## Summary

- Total tests: 51
- Passed: __
- Failed: __
- Skipped: __
- Pass rate: __%

## Unit Tests: Validator (12 tests)

| Test ID | Description | Result | Notes |
|---------|-------------|--------|-------|
| TC-V1 | Valid v2.0 story | ✅ PASS | |
| TC-V2 | Missing format_version | ✅ PASS | Error caught correctly |
| ... | ... | ... | ... |

## Pilot Migration (10 stories)

| Story ID | Components | Migration | Validation | /dev | Quality | Notes |
|----------|------------|-----------|------------|------|---------|-------|
| STORY-001 | 3 | ✅ PASS | ✅ PASS | ✅ PASS | 4/5 | Minor YAML formatting |
| STORY-002 | 5 | ✅ PASS | ✅ PASS | ✅ PASS | 5/5 | Perfect |
| ... | ... | ... | ... | ... | ... | ... |

## Decision

**Based on results:** GO / ITERATE / NO-GO

**Rationale:** [Explain decision based on metrics]

**Next Steps:** [What happens next]
```

---

**Complete this checklist during Weeks 4-5. All 51 tests must pass for Phase 2 success.**
