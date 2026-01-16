# TEST-SPECIFICATION: STORY-262

**Story:** STORY-262 - Add early coverage threshold check to /dev Phase 04
**Test Type:** Structural Validation (Markdown Specification)
**Target File:** `.claude/skills/devforgeai-development/phases/phase-04-refactoring.md`
**Status:** RED (Failing) - Step 2a does not exist yet

---

## Test Summary

| Test ID | AC Coverage | Expected Result | Current Result |
|---------|-------------|-----------------|----------------|
| T-001 | AC#1 | Step 2a exists between Step 1 and Step 3 | FAIL |
| T-002 | AC#1 | Coverage thresholds documented (95/85/80) | FAIL |
| T-003 | AC#2 | test-automator remediation invocation documented | FAIL |
| T-004 | AC#2 | REMEDIATION_MODE flag reference present | FAIL |
| T-005 | AC#3 | Normal flow bypass documented | FAIL |
| T-006 | AC#4 | Validation checkpoint includes coverage check | FAIL |
| T-007 | AC#4 | phase-state.json observation schema documented | FAIL |
| T-008 | AC#5 | Step 2a has entry/exit gates | FAIL |
| T-009 | COMP-001 | Coverage percentage parsing documented | FAIL |
| T-010 | COMP-003 | >= operator threshold comparison documented | FAIL |
| T-011 | COMP-005 | Graceful fallback on tool failure documented | FAIL |
| T-012 | BR-005 | 2-cycle remediation limit documented | FAIL |

---

## Test Cases

### T-001: Step 2a Exists Between Step 1 and Step 3

**AC Coverage:** AC#1 (Coverage Check Executes After Refactoring-Specialist)
**Validates:** Step 2a documented in workflow

```bash
# Test: Step 2a header exists in phase-04-refactoring.md
grep -qE "^[0-9]+[a-z]?\.\s+.*[Ee]arly\s+[Cc]overage|Step\s+2a" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** Match found for "Step 2a" or "Early Coverage" step header
**Current:** FAIL (Step 2a not present in current file)

---

### T-002: Coverage Thresholds Documented

**AC Coverage:** AC#1 (Validates thresholds 95%/85%/80%)
**Validates:** ADR-010 threshold values present

```bash
# Test: All three threshold values present
grep -q "95" .claude/skills/devforgeai-development/phases/phase-04-refactoring.md && \
grep -q "85" .claude/skills/devforgeai-development/phases/phase-04-refactoring.md && \
grep -q "80" .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** All three threshold percentages documented
**Current:** FAIL (No coverage thresholds in current file)

---

### T-003: test-automator Remediation Invocation

**AC Coverage:** AC#2 (test-automator invoked with coverage gaps)
**Validates:** Task invocation template for remediation

```bash
# Test: test-automator Task() invocation with remediation context
grep -qE "Task\(.*subagent_type.*test-automator" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** Task() call to test-automator subagent present
**Current:** FAIL (No test-automator invocation in Phase 04)

---

### T-004: REMEDIATION_MODE Flag Reference

**AC Coverage:** AC#2 (COMP-004)
**Validates:** REMEDIATION_MODE=true parameter documented

```bash
# Test: REMEDIATION_MODE flag present
grep -qiE "remediation.?mode|REMEDIATION_MODE" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** REMEDIATION_MODE flag or equivalent documented
**Current:** FAIL (No remediation mode reference)

---

### T-005: Normal Flow Bypass Documented

**AC Coverage:** AC#3 (Coverage meeting thresholds proceeds normally)
**Validates:** Skip remediation when thresholds met

```bash
# Test: Conditional logic for threshold pass
grep -qiE "(proceed|skip|bypass).*(threshold|coverage|normal)" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** Documentation of normal flow when coverage passes
**Current:** FAIL (No conditional bypass documented)

---

### T-006: Validation Checkpoint Includes Coverage Check

**AC Coverage:** AC#4 (Checkpoint includes coverage verification)
**Validates:** Coverage check in validation checkpoint section

```bash
# Test: Coverage mentioned in validation checkpoint
grep -A20 "Validation Checkpoint" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md | \
  grep -qiE "coverage"
```

**Expected:** Coverage verification in checkpoint checklist
**Current:** FAIL (Checkpoint exists but no coverage item)

---

### T-007: phase-state.json Observation Schema

**AC Coverage:** AC#4 (phase-state.json reflects coverage result)
**Validates:** JSON schema for coverage observations

```bash
# Test: Observation schema includes coverage fields
grep -qiE "coverage.*(percentage|threshold|result)" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** Coverage observation schema documented
**Current:** FAIL (No coverage observation schema)

---

### T-008: Step 2a Entry/Exit Gates

**AC Coverage:** AC#5 (Clear entry/exit gates)
**Validates:** Gate documentation for Step 2a

```bash
# Test: Entry and exit gate markers for coverage step
grep -ciE "(entry|exit).*(gate|condition)" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
# Expected: >= 4 (existing Phase 04 gates + new Step 2a gates)
```

**Expected:** At least 4 gate references (2 phase-level + 2 step-level)
**Current:** FAIL (Only 2 phase-level gates present)

---

### T-009: Coverage Percentage Parsing (COMP-001)

**AC Coverage:** COMP-001 (Parse coverage values 0.0-100.0)
**Validates:** Parsing logic documented

```bash
# Test: Coverage parsing documentation
grep -qiE "parse|extract.*coverage.*percent" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** Coverage percentage extraction documented
**Current:** FAIL (No parsing documentation)

---

### T-010: >= Operator Threshold Comparison (COMP-003)

**AC Coverage:** COMP-003, BR-002 (>= operator, boundary handling)
**Validates:** Comparison operator explicitly documented

```bash
# Test: >= operator documented for threshold comparison
grep -qE ">=|greater.*equal|at.*least" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** >= operator or equivalent documented
**Current:** FAIL (No threshold comparison operator)

---

### T-011: Graceful Fallback on Tool Failure (COMP-005)

**AC Coverage:** COMP-005, BR-004 (Graceful degradation)
**Validates:** Fallback behavior documented

```bash
# Test: Fallback/degradation path documented
grep -qiE "(fallback|graceful|fail.*safe|skip.*coverage)" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** Fallback to Phase 05 documented
**Current:** FAIL (No fallback documentation)

---

### T-012: 2-Cycle Remediation Limit (BR-005)

**AC Coverage:** BR-005 (HALT after 2 failed cycles)
**Validates:** Remediation cycle limit documented

```bash
# Test: Cycle limit documented
grep -qiE "(2|two).*(cycle|attempt|iteration).*limit|REMEDIATION_MAX_CYCLES" \
  .claude/skills/devforgeai-development/phases/phase-04-refactoring.md
```

**Expected:** 2-cycle remediation limit documented
**Current:** FAIL (No cycle limit documentation)

---

## Execution Script

```bash
#!/bin/bash
# tests/results/STORY-262/run-tests.sh

TARGET=".claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
PASS=0
FAIL=0

run_test() {
    local id="$1"
    local desc="$2"
    local cmd="$3"

    if eval "$cmd" 2>/dev/null; then
        echo "[PASS] $id: $desc"
        ((PASS++))
    else
        echo "[FAIL] $id: $desc"
        ((FAIL++))
    fi
}

echo "=== STORY-262 Test Specification Validation ==="
echo "Target: $TARGET"
echo ""

run_test "T-001" "Step 2a exists" \
    "grep -qE 'Step\s+2a|[0-9]+a\.' $TARGET"

run_test "T-002" "Coverage thresholds (95/85/80)" \
    "grep -q '95' $TARGET && grep -q '85' $TARGET && grep -q '80' $TARGET"

run_test "T-003" "test-automator remediation invocation" \
    "grep -qE 'Task.*test-automator' $TARGET"

run_test "T-004" "REMEDIATION_MODE flag" \
    "grep -qiE 'remediation.?mode' $TARGET"

run_test "T-005" "Normal flow bypass" \
    "grep -qiE 'proceed.*(threshold|coverage)' $TARGET"

run_test "T-006" "Validation checkpoint coverage" \
    "grep -A20 'Validation Checkpoint' $TARGET | grep -qiE 'coverage'"

run_test "T-007" "phase-state.json observation" \
    "grep -qiE 'coverage.*(observation|percentage)' $TARGET"

run_test "T-008" "Step 2a entry/exit gates" \
    "[ \$(grep -ciE 'entry.*(gate|condition)|exit.*(gate|condition)' $TARGET) -ge 4 ]"

run_test "T-009" "Coverage parsing (COMP-001)" \
    "grep -qiE 'parse.*coverage|extract.*percent' $TARGET"

run_test "T-010" ">= threshold comparison (COMP-003)" \
    "grep -qE '>=|greater.*equal' $TARGET"

run_test "T-011" "Graceful fallback (COMP-005)" \
    "grep -qiE 'fallback|graceful|fail.*safe' $TARGET"

run_test "T-012" "2-cycle remediation limit (BR-005)" \
    "grep -qiE '(2|two).*(cycle|attempt)' $TARGET"

echo ""
echo "=== Results ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
echo "Total: $((PASS + FAIL))"

exit $FAIL
```

---

## Verification Method

1. Run: `bash tests/results/STORY-262/run-tests.sh`
2. Expected TDD Red Phase: All 12 tests FAIL
3. After implementation: All 12 tests PASS

---

## Coverage Matrix

| AC/Requirement | Tests |
|----------------|-------|
| AC#1 | T-001, T-002 |
| AC#2 | T-003, T-004 |
| AC#3 | T-005 |
| AC#4 | T-006, T-007 |
| AC#5 | T-008 |
| COMP-001 | T-009 |
| COMP-003 | T-010 |
| COMP-005 | T-011 |
| BR-005 | T-012 |
