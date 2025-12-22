# STORY-100: Accuracy Tracking Log Setup - Quick Start Guide

## TDD Red Phase Test Suite

**File**: `tests/specs/STORY-100-accuracy-log.test.sh`
**Status**: ✅ RED Phase Complete (55 failing tests)
**Framework**: Bash/grep/wc (Native tools only)

---

## Quick Commands

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
bash tests/specs/STORY-100-accuracy-log.test.sh
```

### Run and Show Summary Only
```bash
bash tests/specs/STORY-100-accuracy-log.test.sh 2>&1 | tail -20
```

### Count Tests by Category
```bash
bash tests/specs/STORY-100-accuracy-log.test.sh 2>&1 | grep "✗ FAIL\|✓ PASS" | wc -l
```

### Show Failed Tests Only
```bash
bash tests/specs/STORY-100-accuracy-log.test.sh 2>&1 | grep "✗ FAIL"
```

---

## Test Suite Overview

**Total Tests**: 55 (all failing in RED phase)

| Category | Tests | Status |
|----------|-------|--------|
| **Acceptance Criteria** | **34** | ❌ FAIL |
| - AC#1: File & Markdown | 4 | ❌ FAIL |
| - AC#2: Categories & Severity | 8 | ❌ FAIL |
| - AC#3: 7 Required Fields | 10 | ❌ FAIL |
| - AC#4: Usage Guidance (300+ words) | 7 | ❌ FAIL |
| - AC#5: Baseline Reference | 5 | ❌ FAIL |
| **Non-Functional Requirements** | **4** | ❌ FAIL |
| - File size, permissions, format | 4 | ❌ FAIL |
| **Edge Cases** | **5** | ❌ FAIL |
| - Missing baseline, multi-category, backfill, etc. | 5 | ❌ FAIL |
| **Data Validation** | **6** | ❌ FAIL |
| - Date format, categories, severity, length, etc. | 6 | ❌ FAIL |
| **Integration** | **3** | ❌ FAIL |
| - STORY-099 linking, accuracy system | 3 | ❌ FAIL |
| **Metadata** | **3** | ❌ FAIL |
| - Version, docs, extensibility | 3 | ❌ FAIL |

---

## What Tests Validate

### AC#1: File Existence and Markdown Structure (4 tests)
✓ File exists at `devforgeai/metrics/accuracy-log.md`
✓ Content >= 500 characters
✓ Valid markdown headers (##, ###)
✓ Balanced backticks (no unclosed code blocks)

### AC#2: Three Categories with Severity Levels (8 tests)
✓ Rule Violations category
✓ Hallucinations category
✓ Missing Citations category
✓ Critical, High, Medium, Low severity levels
✓ Examples included for each category

### AC#3: Entry Template - 7 Required Fields (10 tests)
✓ Date field (ISO 8601: YYYY-MM-DD)
✓ Category field
✓ Severity field
✓ Command/Context field
✓ Description field (>=50 characters required)
✓ Evidence field
✓ Resolution Status field (Open, Resolved, Deferred)

### AC#4: Usage Guidance Section (7 tests)
✓ Usage Guidance section exists
✓ >= 300 words minimum
✓ Covers when to log issues
✓ Covers severity determination
✓ Covers effective descriptions
✓ Covers evidence/citation format
✓ Covers review cadence (recommended: weekly)

### AC#5: Baseline Reference Section (5 tests)
✓ Baseline Reference section present
✓ Links to STORY-099
✓ Includes comparison instructions
✓ Defines summary statistics format
✓ Handles missing baseline gracefully

### NFRs (4 tests)
✓ File size < 50KB
✓ File permissions 644
✓ Plain markdown only (no HTML/Mermaid)
✓ No hardcoded secrets

### Edge Cases (5 tests)
✓ Missing baseline handling
✓ Multi-category issue guidance
✓ High-volume logging format
✓ Historical backfill support
✓ Resolution tracking fields

### Data Validation (6 tests)
✓ ISO 8601 date format
✓ Category enumeration
✓ Severity enumeration
✓ Description length (50-500 chars)
✓ Evidence requirement
✓ Resolution status enumeration

### Integration (3 tests)
✓ STORY-099 reference
✓ Baseline metrics format
✓ EPIC-016 accuracy system integration

### Metadata (3 tests)
✓ Format version documented
✓ Inline documentation/comments
✓ Extensibility documented

---

## Expected Output

### RED Phase (Current - All Failing)

```
╔════════════════════════════════════════════════════════════════╗
║  STORY-100: Accuracy Tracking Log Setup - Test Suite           ║
║  TDD Red Phase - Failing Tests (No Implementation Yet)         ║
║  Framework: Bash/grep/wc - Native Tools (per tech-stack.md)    ║
╚════════════════════════════════════════════════════════════════╝

✗ FAIL: File does not exist at devforgeai/metrics/accuracy-log.md
✗ FAIL: Cannot check file size - file does not exist
... (55 tests all failing)

Total Tests Run:    55
Tests Passed:       0
Tests Failed:       55

Some tests FAILED (expected in RED phase - no implementation yet)
```

### GREEN Phase (After Implementation)

```
✓ PASS: File exists at devforgeai/metrics/accuracy-log.md
✓ PASS: File size (2540 bytes) >= 500 characters
✓ PASS: File contains 8 markdown headers
✓ PASS: Backticks balanced (42 total, 21 pairs)
... (55 tests all passing)

Total Tests Run:    55
Tests Passed:       55
Tests Failed:       0

All tests PASSED!
```

---

## TDD Workflow

### Phase 1: RED ✅ Complete
- [x] Write failing tests (55 tests)
- [x] Tests validate ALL acceptance criteria
- [x] Tests define specifications
- [x] Current status: All 55 tests FAIL as expected

### Phase 2: GREEN (Next - Implement)
- [ ] Create `devforgeai/metrics/accuracy-log.md`
- [ ] Add all required sections:
  - [ ] File header with version (v1.0)
  - [ ] AC#1: Valid markdown structure
  - [ ] AC#2: Three categories with severity levels
  - [ ] AC#3: Entry template with 7 fields
  - [ ] AC#4: Usage Guidance (>=300 words)
  - [ ] AC#5: Baseline Reference + STORY-099 link
- [ ] Ensure file < 50KB with 644 permissions
- [ ] Run tests until all 55 PASS

### Phase 3: REFACTOR (After GREEN)
- [ ] Improve clarity and organization
- [ ] Enhance documentation
- [ ] Ensure maintainability
- [ ] Verify all 55 tests still PASS

---

## Test File Structure

### Main Test Functions by Category

**AC#1 Tests** (File & Markdown):
- `test_ac1_file_exists()`
- `test_ac1_minimum_size()`
- `test_ac1_valid_markdown_headers()`
- `test_ac1_markdown_parsing()`

**AC#2 Tests** (Categories & Severity):
- `test_ac2_rule_violations_category()`
- `test_ac2_hallucinations_category()`
- `test_ac2_missing_citations_category()`
- `test_ac2_severity_critical/high/medium/low()`
- `test_ac2_category_examples()`

**AC#3 Tests** (7 Fields):
- `test_ac3_date_field()` through `test_ac3_resolution_status_field()`
- `test_ac3_all_seven_fields()` (composite check)
- `test_ac3_iso8601_format_documentation()`
- `test_ac3_description_character_requirement()`

**AC#4 Tests** (Usage Guidance):
- `test_ac4_usage_guidance_section_exists()`
- `test_ac4_word_count_minimum()`
- `test_ac4_when_to_log()`, `_severity_determination()`, `_description_guidance()`, `_evidence_format()`, `_review_cadence()`

**AC#5 Tests** (Baseline Reference):
- `test_ac5_baseline_section_exists()`
- `test_ac5_story099_link()`
- `test_ac5_comparison_instructions()`
- `test_ac5_summary_statistics_format()`
- `test_ac5_baseline_graceful_handling()`

**NFR Tests**:
- `test_nfr_file_size_limit()`
- `test_nfr_file_permissions()`
- `test_nfr_plain_markdown_only()`
- `test_nfr_no_hardcoded_secrets()`

**Edge Case Tests**:
- `test_edge_case_missing_baseline()`
- `test_edge_case_multi_category_guidance()`
- `test_edge_case_high_volume_logging()`
- `test_edge_case_historical_backfill()`
- `test_edge_case_issue_resolution_tracking()`

**Data Validation Tests**:
- `test_validation_date_format()`
- `test_validation_category_values()`
- `test_validation_severity_values()`
- `test_validation_description_length()`
- `test_validation_evidence_required()`
- `test_validation_resolution_status()`

**Integration Tests**:
- `test_integration_story099_reference()`
- `test_integration_baseline_metrics_format()`
- `test_integration_with_accuracy_system()`

**Metadata Tests**:
- `test_metadata_format_version()`
- `test_metadata_documentation_comments()`
- `test_metadata_extensibility_note()`

---

## Key Validation Points for Implementation

When creating `devforgeai/metrics/accuracy-log.md`, ensure:

### File Basics
- [ ] File path: `devforgeai/metrics/accuracy-log.md`
- [ ] File size: < 50KB
- [ ] Permissions: 644 (owner rw, group/other r)
- [ ] Format: Plain markdown (no HTML, Mermaid, custom extensions)
- [ ] Content size: >= 500 characters

### Content Requirements
- [ ] Valid markdown structure with headers (##, ###)
- [ ] Three issue categories: Rule Violations, Hallucinations, Missing Citations
- [ ] Four severity levels: Critical, High, Medium, Low (for each category)
- [ ] Entry template with all 7 fields:
  1. Date (YYYY-MM-DD format)
  2. Category (one of three)
  3. Severity (one of four)
  4. Command/Context
  5. Description (50-500 characters)
  6. Evidence (required, non-empty)
  7. Resolution Status (Open, Resolved, or Deferred)

### Documentation
- [ ] Usage Guidance section (>= 300 words) covering:
  - When to log
  - Severity determination
  - Effective descriptions
  - Evidence/citation format
  - Review cadence (weekly recommended)
- [ ] Baseline Reference section linking to STORY-099
- [ ] Graceful handling of missing baseline
- [ ] Format version documented (v1.0)
- [ ] Inline comments explaining sections

### Edge Cases Documented
- [ ] Multi-category issue guidance
- [ ] High-volume logging/daily summary format
- [ ] Historical backfill (Added Date vs Occurred Date)
- [ ] Resolution tracking (Date, Reference, Notes)

---

## Files Generated

| File | Purpose |
|------|---------|
| `tests/specs/STORY-100-accuracy-log.test.sh` | Main test suite (55 failing tests) |
| `tests/specs/STORY-100-TEST-GENERATION-SUMMARY.md` | Comprehensive documentation |
| `tests/specs/STORY-100-QUICK-START.md` | This quick reference guide |

---

## References

- **Story File**: `devforgeai/specs/Stories/STORY-100-accuracy-tracking-log-setup.story.md`
- **Prerequisite**: `devforgeai/specs/Stories/STORY-099-baseline-metrics-collection.story.md`
- **Tech Stack**: `devforgeai/specs/context/tech-stack.md`
- **Test Location**: `tests/specs/STORY-100-accuracy-log.test.sh`

---

## Notes

- All tests use bash native tools (grep, wc) per framework standards
- Tests are independent and can run in any order
- Tests follow AAA pattern (Arrange, Act, Assert)
- Failing output is expected in RED phase - indicates tests are working correctly
- No external dependencies required

**Generated**: 2025-12-18
**Status**: ✅ TDD Red Phase Complete
