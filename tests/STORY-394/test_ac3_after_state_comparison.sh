#!/usr/bin/env bash
# =============================================================================
# STORY-394 AC#3: After-State Comparison with Numeric Scores
#
# Validates that the evaluation pipeline documents an after-state comparison
# process producing:
# - After-state scores for each rubric dimension
# - Delta (change) per dimension (before vs. after)
# - Weighted composite score for both states
# - Composite delta for overall improvement/regression
# - Pass/fail determination with configurable threshold (default >= 0)
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PIPELINE_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-pipeline.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

run_test() {
    local test_name="$1"
    local test_result="$2"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ "$test_result" -eq 0 ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "  PASS: ${test_name}"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo "  FAIL: ${test_name}"
    fi
}

echo "================================================================"
echo "STORY-394 AC#3: After-State Comparison Tests"
echo "Target: ${PIPELINE_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: Pipeline file exists ---
echo "--- Pre-Check: File Exists ---"
if [ ! -f "$PIPELINE_FILE" ]; then
    echo "  FAIL: Pipeline file does not exist at ${PIPELINE_FILE}"
    echo ""
    echo "================================================================"
    echo "AC#3 Results: 0 passed, 1 failed out of 1 tests"
    echo "================================================================"
    exit 1
fi

# =============================================================================
# Test 1: After-state section exists in pipeline
# =============================================================================
echo "--- After-State Section ---"

HAS_AFTER_SECTION=$(grep -ciE '(after.state|after state|post.migration)' "$PIPELINE_FILE" || true)
run_test "After-state evaluation section documented" "$( [ "$HAS_AFTER_SECTION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Delta calculation documented
# =============================================================================
echo ""
echo "--- Delta Calculation ---"

HAS_DELTA=$(grep -ciE '(delta|difference|change.*score|score.*change)' "$PIPELINE_FILE" || true)
run_test "Delta calculation documented (found: ${HAS_DELTA})" "$( [ "$HAS_DELTA" -ge 2 ] && echo 0 || echo 1 )"

# Delta formula documented (after - before)
HAS_FORMULA=$(grep -ciE '(after.*minus.*before|after.*-.*before|delta.*=.*after|score.*subtrac)' "$PIPELINE_FILE" || true)
run_test "Delta formula (after - before) documented" "$( [ "$HAS_FORMULA" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Weighted composite score documented
# =============================================================================
echo ""
echo "--- Composite Score ---"

HAS_COMPOSITE=$(grep -ciE '(composite.*score|weighted.*score|overall.*score|aggregate.*score)' "$PIPELINE_FILE" || true)
run_test "Weighted composite score documented (found: ${HAS_COMPOSITE})" "$( [ "$HAS_COMPOSITE" -ge 1 ] && echo 0 || echo 1 )"

HAS_WEIGHT_FORMULA=$(grep -ciE '(weight.*dimension|dimension.*weight|SUM.*weight|weighted.*sum)' "$PIPELINE_FILE" || true)
run_test "Composite calculation formula documented" "$( [ "$HAS_WEIGHT_FORMULA" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Pass/fail determination documented
# =============================================================================
echo ""
echo "--- Pass/Fail Determination ---"

HAS_PASS_FAIL=$(grep -ciE '(pass.fail|pass/fail|pass or fail|determination)' "$PIPELINE_FILE" || true)
run_test "Pass/fail determination documented" "$( [ "$HAS_PASS_FAIL" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Configurable threshold with default >= 0
# =============================================================================
echo ""
echo "--- Threshold Configuration ---"

HAS_THRESHOLD=$(grep -ciE '(threshold|configurable.*threshold|default.*threshold)' "$PIPELINE_FILE" || true)
run_test "Configurable threshold documented" "$( [ "$HAS_THRESHOLD" -ge 1 ] && echo 0 || echo 1 )"

HAS_DEFAULT_ZERO=$(grep -ciE '(default.*>=.*0|default.*no.*regression|>= 0)' "$PIPELINE_FILE" || true)
run_test "Default threshold >= 0 (no regression) specified" "$( [ "$HAS_DEFAULT_ZERO" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Per-dimension delta (not just composite)
# =============================================================================
echo ""
echo "--- Per-Dimension Delta ---"

HAS_PER_DIM=$(grep -ciE '(per.dimension|each dimension|dimension.level|dimension.*delta)' "$PIPELINE_FILE" || true)
run_test "Per-dimension delta documented" "$( [ "$HAS_PER_DIM" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
