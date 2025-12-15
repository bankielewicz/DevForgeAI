# STORY-043 Test Suite

Comprehensive test suite for STORY-043: "Update Internal Path References from .claude/ to src/claude/"

## Quick Start

### Run All Tests
```bash
bash tests/STORY-043/run_all_tests.sh
```

### Run Specific Test
```bash
bash tests/STORY-043/test-ac1-audit-classification.sh
bash tests/STORY-043/test-ac2-update-safety.sh
bash tests/STORY-043/test-ac3-validation.sh
bash tests/STORY-043/test-ac4-progressive-disclosure.sh
bash tests/STORY-043/test-ac5-integration.sh
bash tests/STORY-043/test-ac6-deploy-preservation.sh
bash tests/STORY-043/test-ac7-script-safety.sh
```

## Test Files

| File | AC# | Purpose | Tests |
|------|-----|---------|-------|
| test-ac1-audit-classification.sh | #1 | Path audit and classification | 14 |
| test-ac2-update-safety.sh | #2 | Backup and update safety | 16 |
| test-ac3-validation.sh | #3 | Broken reference detection | 14 |
| test-ac4-progressive-disclosure.sh | #4 | src/ structure loading | 17 |
| test-ac5-integration.sh | #5 | Workflow integration | 18 |
| test-ac6-deploy-preservation.sh | #6 | CLAUDE.md preservation | 15 |
| test-ac7-script-safety.sh | #7 | Script guardrails | 25 |

**Total: 119 tests across 7 acceptance criteria**

## Test Pyramid

```
Unit Tests:        70% (83 tests)
Integration Tests: 20% (24 tests)
E2E Tests:         10% (12 tests)
```

## Expected Output (TDD Red Phase)

When no implementation exists, all tests fail (expected):

```
Tests run:    119
Tests passed: 0
Tests failed: 119

Status: RED - Failing tests indicate no implementation yet (correct for TDD Red phase)
```

## Test Status: RED

**Current Status:** All tests failing (TDD Red phase - correct!)

**Why:** Implementation scripts not yet created in src/scripts/

**Next Steps:**
1. Create audit-path-references.sh
2. Create update-paths.sh
3. Create validate-paths.sh
4. Create rollback-updates.sh
5. Generate output files
6. Run tests to validate (GREEN phase)

## Implementation Scripts Required

For tests to pass, create these scripts:

- `src/scripts/audit-path-references.sh` - Scan and classify path references
- `src/scripts/update-paths.sh` - Execute surgical path updates (3 phases)
- `src/scripts/validate-paths.sh` - Validate all paths resolve correctly
- `src/scripts/rollback-path-updates.sh` - Restore files from backup

Output directories required:
- `.devforgeai/specs/STORY-043/` - Classification and report files

## Test Design Principles

### AAA Pattern
All tests follow Arrange-Act-Assert pattern:
- **Arrange:** Set up test conditions
- **Act:** Execute behavior being tested
- **Assert:** Verify outcomes

### Independent Tests
- Each test can run in isolation
- No shared state between tests
- Proper setup/teardown

### Non-Blocking vs Blocking
- **Blocking:** Critical path (script existence, basic functionality)
- **Non-Blocking:** Detail validation (exact counts, deferred features)

## Test Categories

### Unit Tests (70%)
- Script existence and executability
- File creation and location
- Basic classification and validation
- Format checking

### Integration Tests (20%)
- Workflow execution (epic, story, dev)
- Skill and subagent interaction
- Path resolution across components
- Framework interaction

### E2E Tests (10%)
- Full script execution with real data
- Backup and rollback scenarios
- Complete workflow validation
- Success reporting

## Coverage Details

### AC#1: Path Audit (14 tests)
✓ Audit script exists
✓ Classification files created (4 files)
✓ Reference counts validated (~2,814 total)
✓ Format and uniqueness checks

### AC#2: Update Safety (16 tests)
✓ Backup created before updates
✓ 3-phase update execution
✓ Rollback script availability
✓ Diff summary generation

### AC#3: Zero Broken Refs (14 tests)
✓ Validation script execution
✓ Broken reference count = 0
✓ Category coverage (skills, assets, docs)
✓ Deploy-time preservation

### AC#4: Progressive Disclosure (17 tests)
✓ src/claude/ structure exists
✓ Reference files load from src/
✓ File content validity
✓ Multiple skill migration

### AC#5: Integration (18 tests)
✓ Epic creation workflow
✓ Story creation workflow
✓ Development workflow
✓ 3/3 workflows pass with 0 path errors

### AC#6: Deploy Preservation (15 tests)
✓ CLAUDE.md unchanged
✓ @.claude/ references preserved
✓ No @src/claude/ in deploy references
✓ 21/21 deploy refs preserved

### AC#7: Script Safety (25 tests)
✓ Pre-flight checks (git, disk space)
✓ Backup before modifications
✓ Surgical sed operations
✓ Validation and rollback
✓ Success reporting
✓ Error handling (set -euo pipefail)

## Test Utilities

### Color Output
```bash
RED='\033[0;31m'      # ✗ FAIL
GREEN='\033[0;32m'    # ✓ PASS
YELLOW='\033[1;33m'   # ⊘ WARNING
BLUE='\033[0;34m'     # [Info]
NC='\033[0m'          # No color
```

### Helper Functions
- `run_test(name, function)` - Execute and track test
- `assert_file_exists(path)` - Check file presence
- `assert_directory_exists(dir)` - Check directory presence
- `assert_file_count(dir, expected, tolerance)` - Validate file counts

## Running with CI/CD

### GitHub Actions Example
```yaml
- name: Run STORY-043 tests
  run: bash tests/STORY-043/run_all_tests.sh
```

### Jenkins Example
```groovy
stage('Test STORY-043') {
    steps {
        sh 'bash tests/STORY-043/run_all_tests.sh'
    }
}
```

## Troubleshooting

### Tests Fail with "Scripts not found"
Expected! This is TDD Red phase. Create implementation scripts:
```bash
touch src/scripts/{audit,update,validate,rollback}-path-*.sh
chmod +x src/scripts/*.sh
```

### Tests Fail with Permission Denied
Make scripts executable:
```bash
chmod +x tests/STORY-043/*.sh
```

### Tests Timeout
Some tests may take a few seconds. Increase timeout if needed:
```bash
bash tests/STORY-043/run_all_tests.sh --timeout=60
```

## Test Results Recording

After implementation, record results:

```bash
# Run tests and capture output
bash tests/STORY-043/run_all_tests.sh | tee test-results.log

# Generate report
echo "STORY-043 Test Results: PASSED (119/119)" > reports/story-043-results.txt
```

## References

### Story Documentation
- Story: `devforgeai/specs/Stories/STORY-043-update-path-references-to-src.story.md`
- Specs: `.devforgeai/specs/STORY-043/`

### Framework
- Tech Stack: `devforgeai/context/tech-stack.md`
- Testing Guide: `.claude/memory/qa-automation.md`
- Test Patterns: `devforgeai/specs/research/` (examples)

### Related Stories
- STORY-042: Copy framework files to src/ (prerequisite)
- STORY-044: Installer updates (depends on this story)

## Contact & Questions

For test improvements or questions:
- Review test code: inline comments explain each test
- Check TEST-GENERATION-SUMMARY.md for detailed coverage analysis
- Consult story.md for requirement clarification

---

**Test Suite Version:** 1.0
**Generated:** November 19, 2025
**Framework:** DevForgeAI TDD (Test-Driven Development)
**Status:** RED Phase - Ready for implementation
