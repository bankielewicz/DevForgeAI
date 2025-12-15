# STORY-056 Test Execution Guide

## Overview

This document provides comprehensive guidance for executing the test suite for STORY-056: devforgeai-story-creation Skill Integration with User Input Guidance.

**Test Suite:** 45 total tests
- **Unit Tests:** 15 (bash)
- **Integration Tests:** 12 (bash + manual)
- **Regression Tests:** 10 (bash)
- **Performance Tests:** 8 (Python)

---

## Quick Start

### Prerequisites

1. Bash environment (Linux/macOS/WSL)
2. Python 3.8+ (for performance tests)
3. Optional: numpy (for advanced statistics)
   ```bash
   pip3 install numpy
   ```

### Run All Tests

```bash
# Navigate to repo root
cd /mnt/c/Projects/DevForgeAI2

# Make scripts executable
chmod +x .devforgeai/tests/skills/test-story-creation-*.sh

# Run test suites in sequence
echo "Running Unit Tests..."
bash .devforgeai/tests/skills/test-story-creation-guidance-unit.sh

echo "Running Integration Tests..."
bash .devforgeai/tests/skills/test-story-creation-guidance-integration.sh

echo "Running Regression Tests..."
bash .devforgeai/tests/skills/test-story-creation-regression.sh

echo "Running Performance Tests..."
python3 .devforgeai/tests/skills/test-story-creation-guidance-performance.py
```

---

## Test Suite Details

### Unit Tests (15 tests)

**File:** `.devforgeai/tests/skills/test-story-creation-guidance-unit.sh`

**Purpose:** Verify guidance file loading, pattern extraction, and mapping operations in isolation

**Tests:**
1. Step 0 loads guidance with valid file
2. Step 0 handles missing file gracefully
3. Step 0 handles corrupted markdown gracefully
4. Pattern extraction from valid content (≥4 patterns)
5. Pattern name normalization (hyphens, case insensitivity)
6. Pattern-to-question mapping lookup (Phase 1 Steps 3-5)
7. Pattern lookup miss handling (unknown question type)
8. Token measurement documentation
9. Baseline fallback behavior documented
10. Batch mode caching strategy documented
11. Epic selection pattern documented (Explicit Classification + Bounded Choice)
12. Sprint assignment pattern documented (Bounded Choice)
13. Priority selection pattern documented (Explicit Classification)
14. Story points pattern documented (Fibonacci Bounded Choice)
15. Reference file completeness (≥500 lines with all sections)

**Run:**
```bash
bash .devforgeai/tests/skills/test-story-creation-guidance-unit.sh
```

**Expected Output:**
```
Tests Passed: 15/15
✓ All unit tests PASSED
```

---

### Integration Tests (12 tests)

**File:** `.devforgeai/tests/skills/test-story-creation-guidance-integration.sh`

**Purpose:** Verify guidance integration with full Phase 1 workflow and measure subagent impact

**Automated Tests (3):**
1. Full Phase 1 execution with guidance enabled
2. Full Phase 1 execution without guidance (baseline)
3. Pattern conflict resolution

**Manual Verification Tests (9):**
4. Subagent re-invocation reduction (≥30% reduction)
5. Token overhead for Phase 1 (≤5% increase)
6. Backward compatibility (30+ existing tests pass)
7. Batch mode guidance caching (Read called 1x for 9 stories)
8. Mid-execution guidance changes (no mid-flight reload)
9. Concurrent skill invocations (5 parallel /create-story)
10. Phase 6 epic/sprint linking with enhanced metadata
11. End-to-end workflow (create story → dev → qa)
12. AC completeness measurement (85%+ on first attempt)

**Run:**
```bash
bash .devforgeai/tests/skills/test-story-creation-guidance-integration.sh
```

**Expected Output:**
```
Tests Completed: 12/12
✓ All integration tests PASSED/VERIFIED

Note: Some tests require manual execution. See output above for 'MANUAL VERIFICATION REQUIRED' sections.
```

**Manual Test Execution Examples:**

**Test 04: Subagent Re-invocation Reduction**
```bash
# Disable guidance
mv src/claude/skills/devforgeai-ideation/references/user-input-guidance.md \
   src/claude/skills/devforgeai-ideation/references/user-input-guidance.md.disabled

# Create 5 stories, count re-invocations
for i in {1..5}; do
  echo "Creating story $i (baseline)..."
  /create-story "Feature $i description"
done

# Re-enable guidance
mv src/claude/skills/devforgeai-ideation/references/user-input-guidance.md.disabled \
   src/claude/skills/devforgeai-ideation/references/user-input-guidance.md

# Create 5 more stories with guidance
for i in {6..10}; do
  echo "Creating story $i (with guidance)..."
  /create-story "Feature $i description"
done

# Calculate reduction percentage
# baseline_count = X, enhanced_count = Y
# reduction = (X - Y) / X * 100
```

**Test 06: Batch Mode Guidance Caching**
```bash
# Create epic with 9 features (in batch mode markers)
/create-story EPIC-TEST

# Monitor Read tool calls in transcript
# Expected: Read called EXACTLY 1 time for guidance file
# Verify: All 9 story files created in devforgeai/specs/Stories/
```

---

### Regression Tests (10 tests)

**File:** `.devforgeai/tests/skills/test-story-creation-regression.sh`

**Purpose:** Ensure guidance integration doesn't break existing functionality

**Tests:**
1. All existing Phase 1 questions still work
2. All existing Phase 2-8 phases unaffected
3. Story output format preserved (YAML + sections)
4. AskUserQuestion call signature unchanged
5. Baseline question logic preserved
6. Phase execution order unchanged (Phases 1-8 sequential)
7. Epic/sprint linking (Phase 6) behavior unchanged
8. Self-validation (Phase 7) logic unaffected
9. Skill output format unchanged (completion report)
10. Story file creation unchanged (Phase 5 file writing)

**Run:**
```bash
bash .devforgeai/tests/skills/test-story-creation-regression.sh
```

**Expected Output:**
```
Tests Passed: 10/10
✓ All regression tests PASSED

Next Step: Run existing 30+ test cases to ensure no regressions
Command: bash .devforgeai/tests/skills/test-story-creation-existing.sh
```

**Full Regression with Guidance Disabled:**
```bash
# Disable guidance file
mv src/claude/skills/devforgeai-ideation/references/user-input-guidance.md \
   src/claude/skills/devforgeai-ideation/references/user-input-guidance.md.disabled

# Run regression tests (should pass identically)
bash .devforgeai/tests/skills/test-story-creation-regression.sh

# Re-enable guidance
mv src/claude/skills/devforgeai-ideation/references/user-input-guidance.md.disabled \
   src/claude/skills/devforgeai-ideation/references/user-input-guidance.md

# Run regression tests again (should pass identically)
bash .devforgeai/tests/skills/test-story-creation-regression.sh

# Results should be identical (same PASS count)
```

---

### Performance Tests (8 tests)

**File:** `.devforgeai/tests/skills/test-story-creation-guidance-performance.py`

**Purpose:** Measure execution time, token overhead, and memory footprint

**Tests:**
1. Step 0 execution time (p95): target <2 seconds
2. Step 0 execution time (p99): target <3 seconds (stress test)
3. Pattern extraction time: target <500ms for 20 patterns
4. Pattern lookup time: target <50ms per question (10 lookups)
5. Phase 1 execution time increase: target ≤5% vs baseline
6. Token overhead for Step 0: target ≤1,000 tokens
7. Phase 1 total token increase: target ≤5% vs baseline
8. Memory footprint for cache: target <5 MB

**Run:**
```bash
python3 .devforgeai/tests/skills/test-story-creation-guidance-performance.py
```

**Expected Output:**
```
✓ TEST 01: Step 0 execution time (p95) - PASS
  Measurement: 0.1234 s
  Target:      2.0000 s

✓ TEST 02: Step 0 execution time (p99 - stress test) - PASS
  ...

Results: 8/8 tests PASSED

✓ All performance tests within targets!
```

**Performance Test Interpretation:**

| Test | Metric | Target | Status | Meaning |
|------|--------|--------|--------|---------|
| Test 01 | p95 latency | <2s | If PASS | Step 0 loads quickly for most users |
| Test 02 | p99 latency | <3s | If PASS | Even worst-case loads within 3s |
| Test 03 | Extract time | <500ms | If PASS | Pattern parsing is fast |
| Test 04 | Lookup time | <50ms | If PASS | Pattern matching is O(1) |
| Test 05 | Phase 1 increase | ≤5% | If PASS | Minimal user-visible delay |
| Test 06 | Step 0 tokens | ≤1000 | If PASS | Within token budget |
| Test 07 | Phase 1 tokens | ≤5% | If PASS | Minimal token increase |
| Test 08 | Memory | <5MB | If PASS | Cache is lightweight |

---

## Success Criteria

### Unit Tests (15/15 must pass)
```bash
Tests Passed: 15/15
✓ All unit tests PASSED
```

### Integration Tests (12/12 must complete)
```bash
Tests Completed: 12/12
✓ All integration tests PASSED/VERIFIED
```

### Regression Tests (10/10 + 30+ existing)
```bash
Tests Passed: 10/10
✓ All regression tests PASSED

Plus: 30+ existing tests must pass with guidance disabled
Plus: 30+ existing tests must pass with guidance enabled
```

### Performance Tests (8/8 within targets)
```bash
Results: 8/8 tests PASSED
✓ All performance tests within targets!
```

### Overall Success (45 tests)
```
✓ All 15 unit tests PASSED
✓ All 12 integration tests VERIFIED
✓ All 10 regression tests PASSED
✓ All 8 performance tests PASSED
✓ 30+ existing tests PASSED (baseline)
✓ 30+ existing tests PASSED (with guidance)
```

**Success Threshold:** 45/45 tests (100%)

---

## Test Fixtures

### Feature Descriptions (for manual testing)

Create stories with these descriptions to verify guidance integration:

**1. Simple Feature (3 points)**
```
"Add user registration form with email validation. Allow users to create account with email/password."
```

**2. Moderate Feature (5 points)**
```
"Implement payment processing via Stripe. Support credit cards, invoicing, and subscription management."
```

**3. Complex Feature (8 points)**
```
"Build real-time notification system with WebSocket support, database persistence, and retry logic for failed delivery."
```

**4. Ambiguous Feature (needs AC clarification)**
```
"Improve system performance and make it more scalable."
```

**5. Edge Case Feature (needs error handling clarification)**
```
"Handle user uploads with validation and storage."
```

---

## Troubleshooting

### Test Failures

**"File not found: user-input-guidance.md"**
- Verify file exists: `ls src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`
- If missing: Ensure STORY-053 is completed first (creates guidance file)

**Unit tests fail on pattern count**
- Check guidance file has pattern definitions
- Verify patterns use `### Pattern` heading format
- Count patterns: `grep -c "^### Pattern" <file>`

**Integration tests don't read guidance**
- Guidance file might be temporarily disabled
- Run: `mv user-input-guidance.md.disabled user-input-guidance.md`
- Check Read tool call in skill output

**Performance tests slow**
- Test system may be under load
- Run tests in isolation on quiet system
- Expected: p95 <2s, but may vary by hardware

**Regression tests fail**
- Guidance integration may have broken baseline logic
- Check SKILL.md for syntax errors
- Verify AskUserQuestion parameters unchanged
- Restore from git if corrupted: `git checkout src/claude/skills/devforgeai-story-creation/`

---

## Test Maintenance

### Adding New Tests

When adding new test cases:

1. **Unit Tests:** Modify `test-story-creation-guidance-unit.sh`
   - Add `test_NN_name()` function
   - Update `TEST_TOTAL` in main()
   - Document assertion expectations

2. **Integration Tests:** Modify `test-story-creation-guidance-integration.sh`
   - Add manual verification section
   - Include step-by-step test instructions
   - Document expected manual actions

3. **Regression Tests:** Modify `test-story-creation-regression.sh`
   - Test existing functionality only (no guidance-specific tests)
   - Verify baseline behavior preserved
   - Compare with/without guidance

4. **Performance Tests:** Modify `test-story-creation-guidance-performance.py`
   - Update performance targets if needed
   - Add new measurement tests
   - Update summary report generation

### Updating Performance Targets

If performance targets need adjustment:

1. Run tests 20+ times on representative hardware
2. Calculate p95/p99 from results
3. Update `*_TARGET` constants in test file
4. Document rationale in AC#7 (Token Overhead Constraint)
5. Update STORY-056 if targets change

---

## CI/CD Integration

### Running Tests in CI Pipeline

```yaml
# Example GitHub Actions workflow
name: Test Story Creation Guidance

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Unit Tests
        run: bash .devforgeai/tests/skills/test-story-creation-guidance-unit.sh

      - name: Run Regression Tests
        run: bash .devforgeai/tests/skills/test-story-creation-regression.sh

      - name: Run Performance Tests
        run: |
          pip3 install numpy
          python3 .devforgeai/tests/skills/test-story-creation-guidance-performance.py

      - name: Report Results
        if: always()
        run: |
          echo "Unit Tests: ✓"
          echo "Regression Tests: ✓"
          echo "Performance Tests: ✓"
```

---

## Test Coverage Summary

| Category | Tests | Coverage |
|----------|-------|----------|
| **Unit** | 15 | File I/O, pattern extraction, mapping, fallback logic |
| **Integration** | 12 | Phase 1 workflow, subagent impact, token overhead, batch caching |
| **Regression** | 10 | Backward compatibility, phase order, output format, file creation |
| **Performance** | 8 | Timing (p95/p99), tokens, memory, extraction speed, lookup time |
| **Total** | 45 | Comprehensive coverage of AC#1-10 and NFRs |

---

## Final Checklist

Before marking STORY-056 complete:

- [ ] All 15 unit tests PASS
- [ ] All 12 integration tests VERIFIED (including manual tests)
- [ ] All 10 regression tests PASS
- [ ] All 8 performance tests within targets
- [ ] 30+ existing tests PASS with guidance disabled
- [ ] 30+ existing tests PASS with guidance enabled
- [ ] Integration guide created (≥500 lines with 10 sections)
- [ ] SKILL.md references integration guide in Phase 1 Step 0
- [ ] No AskUserQuestion signature changes
- [ ] Batch mode caching verified (Read called 1x per batch)
- [ ] Token overhead verified (≤1,000 for Step 0, ≤5% for Phase 1)
- [ ] Subagent re-invocation reduction verified (≥30%)
- [ ] AC completeness improvement verified (≥85% first-attempt)

**Success Criteria:** All items checked ✓

---

**Test Suite Version:** 1.0
**Last Updated:** 2025-01-21
**Status:** Ready for Phase 2 Implementation
