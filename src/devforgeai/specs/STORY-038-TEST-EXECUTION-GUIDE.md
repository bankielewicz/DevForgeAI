# STORY-038: Test Execution Guide
## Red Phase - Verify All Tests Fail Initially

**Date:** 2025-11-18
**Purpose:** Validate test suite is comprehensive and fails initially (TDD Red phase)
**Status:** Ready for execution

---

## Quick Start

### Run Full Test Suite (67 tests)
```bash
cd /mnt/c/Projects/DevForgeAI2

# All tests - should show ~67 FAILED
pytest tests/unit/test_release_command_refactoring.py \
        tests/integration/test_release_scenarios.py -v
```

### Expected Output (RED Phase)
```
tests/unit/test_release_command_refactoring.py::TestCommandSizeReduction::test_command_character_count_under_15k_hard_limit FAILED
tests/unit/test_release_command_refactoring.py::TestCommandSizeReduction::test_command_character_count_under_12k_target FAILED
tests/unit/test_release_command_refactoring.py::TestCommandSizeReduction::test_command_line_count_under_350_lines FAILED
...
============================== 67 failed in X.XXs ==============================
```

---

## Test Suite Breakdown

### Unit Tests (38 tests)

```bash
pytest tests/unit/test_release_command_refactoring.py -v
```

**Classes:**
1. `TestCommandSizeReduction` (4 tests)
   - AC-1: Size reduction validation

2. `TestBusinessLogicExtraction` (6 tests)
   - AC-2: Logic extraction to skill

3. `TestFunctionalEquivalence` (6 tests)
   - AC-3: Scenario preservation

4. `TestSkillEnhancement` (9 tests)
   - AC-4: Skill enhancement

5. `TestTokenEfficiency` (3 tests)
   - AC-5: Token savings

6. `TestPatternCompliance` (7 tests)
   - AC-6: Pattern compliance

7. `TestSubagentCreation` (3 tests)
   - AC-7: Subagent decision

### Integration Tests (29 tests)

```bash
pytest tests/integration/test_release_scenarios.py -v
```

**Classes:**
1. `TestScenario3aSuccessfulStagingDeployment` (4 tests)
2. `TestScenario3bProductionDeploymentConfirmation` (4 tests)
3. `TestScenario3cDeploymentFailureRollback` (4 tests)
4. `TestScenario3dMissingQaApprovalGate` (4 tests)
5. `TestScenario3eDefaultEnvironmentStaging` (3 tests)
6. `TestScenario3fPostReleaseHooksIntegration` (3 tests)
7. `TestRegressionTests` (5 tests)
8. `TestHookNonBlockingBehavior` (2 tests)

---

## Test Execution Scenarios

### Scenario 1: Quick Validation (2 minutes)
```bash
# Run only size reduction tests (most critical)
pytest tests/unit/test_release_command_refactoring.py::TestCommandSizeReduction -v

# Expected: 4 FAILED
# Message: Command exceeds 15K hard limit: 18,166 chars
```

### Scenario 2: Pattern Compliance Check (3 minutes)
```bash
# Validate pattern compliance
pytest tests/unit/test_release_command_refactoring.py::TestPatternCompliance -v

# Expected: 7 FAILED
# Message: Command must invoke skill, have 3-5 phases, etc.
```

### Scenario 3: Full Unit Tests (5 minutes)
```bash
# All unit tests
pytest tests/unit/test_release_command_refactoring.py -v

# Expected: 38 FAILED
# Coverage: All AC-1 through AC-7
```

### Scenario 4: Full Integration Tests (5 minutes)
```bash
# All integration tests
pytest tests/integration/test_release_scenarios.py -v

# Expected: 29 FAILED
# Coverage: All 6 scenarios + regression + hooks
```

### Scenario 5: Complete Suite (10 minutes)
```bash
# All 67 tests
pytest tests/unit/test_release_command_refactoring.py \
        tests/integration/test_release_scenarios.py -v

# Expected: 67 FAILED (with detailed assertion messages)
```

---

## Test Output Analysis

### Sample Output from RED Phase
```
collected 67 items

tests/unit/test_release_command_refactoring.py::TestCommandSizeReduction::test_command_character_count_under_15k_hard_limit FAILED [  1%]

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <test_release_command_refactoring.TestCommandSizeReduction object at 0x...>

    def test_command_character_count_under_15k_hard_limit(self):
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")
        assert command_path.exists(), f"Release command not found at {command_path}"
        with open(command_path, 'r') as f:
            content = f.read()
        char_count = len(content)
        assert char_count < 15000, (
            f"Command exceeds 15K hard limit: {char_count} chars. "
            f"Current: {char_count * 100 // 15000}% of limit. "
            f"Target: ≤15K (hard), ≤12K (target). Requires refactoring."
        )

E   AssertionError: Command exceeds 15K hard limit: 18,166 chars. Current: 121% of limit. Target: ≤15K (hard), ≤12K (target). Requires refactoring.

tests/unit/test_release_command_refactoring.py:41: AssertionError
============================== 1 failed in 0.03s ==============================
```

**What this tells us:**
- ✅ Test is correctly identifying the problem
- ✅ Current command size: 18,166 characters (121% of budget)
- ✅ Target: <12,000 characters (optimal)
- ✅ Hard limit: <15,000 characters
- ✅ Test will PASS once refactoring reduces size

---

## Interpreting Test Failures

### Type 1: Size Reduction Failures

```
AssertionError: Command has 655 lines (target: ≤350)
```

**Meaning:** Command too large (not refactored yet)
**Resolution:** Reduce lines from 655 → ≤350 in Phase 2

### Type 2: Business Logic Failures

```
AssertionError: Found deployment sequencing patterns in command
```

**Meaning:** Business logic still in command (not extracted)
**Resolution:** Move logic to skill in Phase 2

### Type 3: Pattern Compliance Failures

```
AssertionError: Command has 8 phases (expected 3-5)
```

**Meaning:** Command structure wrong
**Resolution:** Refactor to 3-5 phases (lean pattern) in Phase 2

### Type 4: Functional Equivalence Failures

```
AssertionError: Skill Phase 2 (Staging Deployment) not found
```

**Meaning:** Skill missing required phase
**Resolution:** Ensure skill has all phases in Phase 2

---

## Validating Test Quality

### Check 1: All Tests Fail
```bash
# Count failed tests
pytest tests/unit/test_release_command_refactoring.py \
        tests/integration/test_release_scenarios.py -v \
        | grep FAILED | wc -l

# Expected: 67 (all should fail)
```

### Check 2: No False Positives
```bash
# Verify tests fail for right reasons
pytest tests/unit/test_release_command_refactoring.py::TestCommandSizeReduction -v

# Check assertions contain useful messages about current vs expected
```

### Check 3: Tests Cover All AC
```bash
# Count tests per acceptance criteria
pytest tests/unit/test_release_command_refactoring.py -v | grep "AC-"

# Expected: Multiple tests for each AC (1-7)
```

### Check 4: Summary Statistics
```bash
# Get test summary
pytest tests/unit/test_release_command_refactoring.py \
        tests/integration/test_release_scenarios.py \
        -v --tb=no

# Expected output:
# ========================= 67 failed in X.XXs ==========================
```

---

## Next Steps (Phase 2 - Green)

### After RED Phase Validation Complete

1. **Verify all 67 tests fail** ✓
2. **Begin Phase 2 (Green - Implementation)**
   - Reduce command from 655 → ≤350 lines
   - Move business logic to skill
   - Implement lean pattern (5 responsibilities)
3. **Re-run tests during implementation**
   - After Phase 0: 4+ tests should pass (size/structure)
   - After Phase 1: More tests pass (pattern compliance)
   - After Phase 2: All tests pass (Green phase complete)

### Implementation Command
```bash
# During Phase 2, run frequently to track progress
pytest tests/unit/test_release_command_refactoring.py -v --tb=short

# Watch test count increase from 0 PASSED → 38 PASSED
```

---

## Troubleshooting

### Issue: "Release command not found"
```
AssertionError: Release command not found at /mnt/c/Projects/DevForgeAI2/.claude/commands/release.md
```

**Solution:**
```bash
# Verify file exists
ls -la /mnt/c/Projects/DevForgeAI2/.claude/commands/release.md

# If missing, run this command to create with current content
touch /mnt/c/Projects/DevForgeAI2/.claude/commands/release.md
```

### Issue: "No such file or directory"
```
FileNotFoundError: [Errno 2] No such file or directory: 'tests/unit/test_release_command_refactoring.py'
```

**Solution:**
```bash
# Change to correct directory
cd /mnt/c/Projects/DevForgeAI2

# Verify test files exist
ls tests/unit/test_release_command_refactoring.py
ls tests/integration/test_release_scenarios.py
```

### Issue: "pytest not installed"
```
ModuleNotFoundError: No module named 'pytest'
```

**Solution:**
```bash
# Install pytest
pip install pytest

# Verify installation
pytest --version
```

---

## Test Coverage Validation

### Verify Test Coverage

```bash
# Unit tests coverage (should be 100% file coverage for command)
pytest tests/unit/test_release_command_refactoring.py \
        --cov=.claude/commands/release \
        --cov-report=term-missing
```

### Expected Coverage

- **Command file:** 100% coverage (all lines examined)
- **Skill file:** Partial coverage in unit tests (integration validates)
- **Reference files:** Checked for existence, not line coverage

---

## Continuous Integration

### Pre-Commit Validation
```bash
#!/bin/bash
# Run before committing test changes

cd /mnt/c/Projects/DevForgeAI2

# Run full test suite
pytest tests/unit/test_release_command_refactoring.py \
        tests/integration/test_release_scenarios.py \
        -q --tb=no

exit $?
```

### CI/CD Pipeline Integration
```yaml
# Example .github/workflows/test-story-038.yml

- name: Run STORY-038 Test Suite
  run: |
    pytest tests/unit/test_release_command_refactoring.py \
            tests/integration/test_release_scenarios.py \
            -v --junit-xml=junit.xml

- name: Upload Results
  uses: actions/upload-artifact@v2
  if: always()
  with:
    name: test-results
    path: junit.xml
```

---

## Performance Notes

### Test Execution Time

| Suite | Tests | Time | Notes |
|-------|-------|------|-------|
| **Unit** | 38 | ~2s | File I/O only |
| **Integration** | 29 | ~2s | File I/O only |
| **Total** | 67 | ~4s | Fast (no dependencies) |

### Resource Usage
- **CPU:** Minimal (file reading, regex matching)
- **Memory:** <50MB (test suite only)
- **Disk:** File reading only (no writes during RED phase)

---

## Success Criteria

### RED Phase Complete When:
```
✅ All 67 tests FAIL (not error, but FAIL with assertions)
✅ Each failure has clear assertion message
✅ No import errors or setup failures
✅ Test execution completes in <10 seconds
✅ Test output clearly shows:
   - Current state (18,166 chars, 655 lines, no pattern compliance)
   - Expected state (≤12,000 chars, ≤350 lines, 5-responsibility pattern)
   - Gap to close (>30% size reduction needed)
```

---

## Documentation Reference

**Related Files:**
- Test Summary: `.devforgeai/specs/STORY-038-TEST-GENERATION-SUMMARY.md`
- Story: `.ai_docs/Stories/STORY-038-refactor-release-command-lean-orchestration.story.md`
- Lean Pattern: `.devforgeai/protocols/lean-orchestration-pattern.md`

---

## Questions & Support

### Common Questions

**Q: Why do all tests fail?**
A: TDD Red phase. Tests are for functionality that doesn't exist yet. Tests should fail before implementation.

**Q: When will tests pass?**
A: After Phase 2 (Green) refactoring implementation completes, all 67 tests should pass.

**Q: Can I modify the tests?**
A: No. Tests represent acceptance criteria. Modify story requirements, not tests, if requirements change.

**Q: What if I can't reduce to ≤350 lines?**
A: Consider moving more logic to skill or creating subagent for specialized tasks.

---

**Generated:** 2025-11-18
**Status:** Ready for Phase 1 (Red Phase Validation)
**Next Phase:** Phase 2 (Green - Implementation)
