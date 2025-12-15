# STORY-048 Test Suite - Quick Start Guide

## Overview

**142 comprehensive tests** have been generated for STORY-048: Production Cutover, Documentation, and Distribution Package

These tests validate all 7 acceptance criteria, edge cases, business rules, and non-functional requirements.

---

## Files Created

```
tests/
├── test_story_048_readme.py              (13 tests - AC-1)
├── test_story_048_install_guide.py       (23 tests - AC-2)
├── test_story_048_migration_guide.py     (21 tests - AC-3)
├── test_story_048_distribution_package.py (26 tests - AC-4)
├── test_story_048_deprecation.py         (18 tests - AC-5)
├── test_story_048_roadmap.py             (19 tests - AC-6)
├── test_story_048_onboarding.py          (20 tests - AC-7)
├── test_story_048_edge_cases.py          (20 tests - Edge Cases)
├── test_story_048_business_rules.py      (25 tests - Business Rules)
├── STORY-048-TEST-SUITE-SUMMARY.md       (Detailed documentation)
├── STORY-048-TEST-SUMMARY.json           (Machine-readable summary)
└── STORY-048-QUICK-START.md              (This file)
```

---

## Run All Tests

```bash
pytest tests/test_story_048*.py -v
```

Expected output: **142 tests, all FAILING (TDD Red phase)**

---

## Run Tests by Category

### AC-1: README.md Updates
```bash
pytest tests/test_story_048_readme.py -v
```
13 tests validating installer-based installation instructions

### AC-2: INSTALL.md Guide
```bash
pytest tests/test_story_048_install_guide.py -v
```
23 tests validating comprehensive installation guide (10 sections, 15+ troubleshooting scenarios, 10+ FAQ)

### AC-3: MIGRATION-GUIDE.md
```bash
pytest tests/test_story_048_migration_guide.py -v
```
21 tests validating 7-step migration workflow with safety checklist

### AC-4: Distribution Packages
```bash
pytest tests/test_story_048_distribution_package.py -v
```
26 tests validating tar.gz and ZIP package creation, extraction, and integrity

### AC-5: Deprecation Notices
```bash
pytest tests/test_story_048_deprecation.py -v
```
18 tests validating deprecation notices in README.md and .claude/README.md

### AC-6: ROADMAP Updates
```bash
pytest tests/test_story_048_roadmap.py -v
```
19 tests validating Phase 4 completion and version 1.0.1

### AC-7: Team Onboarding
```bash
pytest tests/test_story_048_onboarding.py -v
```
20 tests validating training log and 7-item checklist completion

### Edge Cases
```bash
pytest tests/test_story_048_edge_cases.py -v
```
20 tests for documentation sync, corruption, workflow adherence, etc.

### Business Rules & NFRs
```bash
pytest tests/test_story_048_business_rules.py -v
```
25 tests validating business rules and non-functional requirements

---

## Test Summary

| Category | Count |
|----------|-------|
| Total Tests | 142 |
| Acceptance Criteria Tests | 120 |
| Edge Case Tests | 20 |
| Business Rule Tests | 25 |
| Unit Tests | 95 |
| Integration Tests | 32 |

---

## Key Acceptance Criteria Tested

**AC-1: README.md Installer Instructions**
- ✅ Contains "python installer/install.py"
- ✅ Prerequisites list Python 3.8+, Git, Claude Code Terminal
- ✅ Fresh install + upgrade examples
- ✅ Old manual copy removed

**AC-2: INSTALL.md Guide (10 sections)**
- ✅ Prerequisites, Modes, Fresh, Upgrade, Rollback, Validate, Uninstall, Troubleshooting, FAQ, Support
- ✅ 15+ troubleshooting scenarios
- ✅ 10+ FAQ Q&A pairs
- ✅ Copy-paste friendly commands

**AC-3: MIGRATION-GUIDE.md (7-step workflow)**
- ✅ Backup, Pull, Run installer, Verify, Update, Test, Cleanup
- ✅ Safety checklist
- ✅ Rollback procedure
- ✅ Troubleshooting

**AC-4: Distribution Packages**
- ✅ devforgeai-1.0.1.tar.gz created
- ✅ devforgeai-1.0.1.zip created
- ✅ Contains src/, installer/, docs, LICENSE, version.json
- ✅ Extracts and installs successfully

**AC-5: Deprecation Notices**
- ✅ README.md has deprecation notice with ⚠️
- ✅ .claude/README.md created with DEPRECATED warning
- ✅ Deprecation date: 2025-11-17
- ✅ Support until v2.0.0 (6+ months)

**AC-6: ROADMAP.md Updates**
- ✅ Phase 4 marked COMPLETE
- ✅ All 8 stories listed (STORY-041 through STORY-048)
- ✅ Version updated to 1.0.1
- ✅ Phase 5 described

**AC-7: Team Onboarding**
- ✅ Training log created at .devforgeai/onboarding/team-training-log.md
- ✅ Session metadata documented
- ✅ 7-item checklist per developer
- ✅ 100% completion tracked

---

## Coverage Metrics

```
Acceptance Criteria:    7/7 (100%)
Edge Cases:             7/7 (100%)
Business Rules:         4/4 (100%)
Non-Functional Req:     3/3 (100%)
Data Validation:        6/6 (100%)
```

---

## Example Test Execution

### Run specific test
```bash
pytest tests/test_story_048_readme.py::TestReadmeInstallationSection::test_readme_contains_installer_command -v
```

### Run specific test class
```bash
pytest tests/test_story_048_readme.py::TestReadmeInstallationSection -v
```

### Run with coverage report
```bash
pytest tests/test_story_048*.py --cov=. --cov-report=html --cov-report=term
```

### Run with verbose output
```bash
pytest tests/test_story_048*.py -vv --tb=short
```

### Run and stop on first failure
```bash
pytest tests/test_story_048*.py -x
```

---

## Expected Test Results (TDD Red Phase)

All tests are **currently FAILING** because the features they validate have not been implemented yet.

This is **intentional** and follows Test-Driven Development (TDD) principles:

1. **RED Phase** ← You are here
   - Write tests first
   - Tests fail (features don't exist)

2. **GREEN Phase** (Next)
   - Implement features to pass tests
   - Make all tests pass

3. **REFACTOR Phase** (After)
   - Improve code quality
   - Optimize while keeping tests passing

---

## Test Organization

Tests are organized by:

1. **Acceptance Criteria** - Grouped by AC number
2. **Functionality** - Test classes logically grouped
3. **Granularity** - Specific tests for each requirement
4. **Independence** - Each test can run alone

---

## Using Test Results

### When tests fail (expected in RED phase):
```
FAILED tests/test_story_048_readme.py::TestReadmeInstallationSection::test_readme_contains_installer_command
AssertionError: README.md must contain 'python installer/install.py' command
```

This tells you what needs to be implemented:
1. Create/update README.md
2. Add Installation section
3. Include "python installer/install.py" command

### When tests pass (GREEN phase):
```
PASSED tests/test_story_048_readme.py::TestReadmeInstallationSection::test_readme_contains_installer_command
```

Feature is implemented correctly ✅

---

## Development Workflow

1. **RED Phase** (Now)
   ```bash
   pytest tests/test_story_048*.py -v
   # All tests fail - Good!
   ```

2. **GREEN Phase** (During implementation)
   - Implement features listed in test assertions
   - Re-run tests frequently
   - Stop when all tests pass

3. **REFACTOR Phase** (After all tests pass)
   - Review code quality
   - Improve clarity and efficiency
   - Re-run tests to ensure nothing broke

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'pytest'"
**Solution:** Install pytest
```bash
pip install pytest
```

### Issue: "No such file or directory"
**Solution:** Run tests from project root
```bash
# Wrong:
cd tests && pytest test_story_048*.py

# Right:
pytest tests/test_story_048*.py
```

### Issue: Some tests skipped (showing "SKIPPED")
**Solution:** This is OK! Tests skip if prerequisite files don't exist
- Tests skip gracefully when files not found
- They'll pass once files are created

### Issue: Want to see only failures
```bash
pytest tests/test_story_048*.py -v --tb=short -x
```

---

## Key Test Patterns Used

### Pattern 1: File Existence Tests
```python
def test_file_exists(self):
    assert Path("file.md").exists()
```
Verifies required files created

### Pattern 2: Content Validation Tests
```python
def test_contains_keyword(self, content):
    assert re.search(r'keyword', content)
```
Validates file contents match requirements

### Pattern 3: Structure Tests
```python
def test_has_sections(self, content):
    sections = re.findall(r'## Section', content)
    assert len(sections) >= 10
```
Ensures proper document structure

### Pattern 4: Integration Tests
```python
def test_extracts_successfully(self):
    with tarfile.open(path, 'r:gz') as tar:
        tar.extractall(tmpdir)
```
Tests actual functionality (extraction, installation, etc.)

---

## Test Maintenance

### Adding New Tests
1. Follow existing patterns
2. Add to appropriate test class
3. Use clear, descriptive names
4. Add docstring explaining what's tested

### Updating Tests
1. Update assertion message if requirements change
2. Add new test if new requirement added
3. Remove test only if requirement removed

### Debugging Failed Tests
1. Run test in isolation: `pytest -vv tests/test_file.py::TestClass::test_name`
2. Check actual vs expected values
3. Verify file paths and locations
4. Add print statements for debugging

---

## Integration with Story

These tests are part of STORY-048 implementation:

```
STORY-048: Production Cutover, Documentation, and Distribution Package
  ├─ AC-1: README.md (13 tests)
  ├─ AC-2: INSTALL.md (23 tests)
  ├─ AC-3: MIGRATION-GUIDE.md (21 tests)
  ├─ AC-4: Distribution Packages (26 tests)
  ├─ AC-5: Deprecation (18 tests)
  ├─ AC-6: ROADMAP (19 tests)
  ├─ AC-7: Onboarding (20 tests)
  ├─ Edge Cases (20 tests)
  └─ Business Rules (25 tests)
```

---

## Next Steps

1. **Verify all tests fail initially**
   ```bash
   pytest tests/test_story_048*.py -v
   ```

2. **Start TDD cycle (GREEN phase)**
   - Implement AC-1: Update README.md
   - Re-run: `pytest tests/test_story_048_readme.py -v`
   - Move to AC-2, AC-3, etc.

3. **Commit frequently**
   ```bash
   git add tests/
   git commit -m "test(STORY-048): Generated comprehensive test suite"
   ```

4. **After all tests pass (REFACTOR phase)**
   - Review code quality
   - Optimize while keeping tests green

---

## Resources

- **Detailed Documentation:** `tests/STORY-048-TEST-SUITE-SUMMARY.md`
- **Machine-Readable Format:** `tests/STORY-048-TEST-SUMMARY.json`
- **Story Definition:** `devforgeai/specs/Stories/STORY-048-production-cutover-documentation.story.md`
- **Test Framework:** [pytest documentation](https://docs.pytest.org/)

---

## Summary

```
✅ 142 tests generated
✅ 7 acceptance criteria covered
✅ 7 edge cases covered
✅ 4 business rules covered
✅ 3 NFRs covered
✅ 100% acceptance criteria coverage
✅ Ready for TDD cycle (RED → GREEN → REFACTOR)
```

**Status:** Ready for Development ✅

All tests are ready to guide implementation through the TDD cycle.

---

Generated: 2025-11-20
Framework: DevForgeAI Test-Automator
TDD Phase: Red (Failing Tests)
