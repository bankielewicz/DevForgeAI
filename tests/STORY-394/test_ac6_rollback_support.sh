#!/usr/bin/env bash
# =============================================================================
# STORY-394 AC#6: Rollback Decision Support
#
# Validates that the pipeline provides rollback decision support:
# - Identifies which specific dimensions regressed and by how much
# - ROLLBACK RECOMMENDED flag when composite delta below threshold
# - Specific agent file path for rollback target
# - Rollback exercise process documented
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PIPELINE_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-pipeline.md"
RESULTS_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-results.md"

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
echo "STORY-394 AC#6: Rollback Decision Support Tests"
echo "Target: ${PIPELINE_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: Pipeline file exists ---
echo "--- Pre-Check: File Exists ---"
if [ ! -f "$PIPELINE_FILE" ]; then
    echo "  FAIL: Pipeline file does not exist at ${PIPELINE_FILE}"
    echo ""
    echo "================================================================"
    echo "AC#6 Results: 0 passed, 1 failed out of 1 tests"
    echo "================================================================"
    exit 1
fi

# =============================================================================
# Test 1: Rollback section exists in pipeline
# =============================================================================
echo "--- Rollback Section ---"

HAS_ROLLBACK_SECTION=$(grep -ciE '(rollback|roll.back)' "$PIPELINE_FILE" || true)
run_test "Rollback section documented in pipeline (found: ${HAS_ROLLBACK_SECTION})" "$( [ "$HAS_ROLLBACK_SECTION" -ge 2 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Regression dimension identification documented
# =============================================================================
echo ""
echo "--- Regression Identification ---"

HAS_REGRESSION=$(grep -ciE '(regression|regress|dimension.*regress|negative.*delta)' "$PIPELINE_FILE" || true)
run_test "Regression identification documented (found: ${HAS_REGRESSION})" "$( [ "$HAS_REGRESSION" -ge 1 ] && echo 0 || echo 1 )"

HAS_WHICH_DIM=$(grep -ciE '(which.*dimension|dimension.*which|specific.*dimension|identify.*dimension)' "$PIPELINE_FILE" || true)
run_test "Specific dimension regression identification documented" "$( [ "$HAS_WHICH_DIM" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: ROLLBACK RECOMMENDED flag documented
# =============================================================================
echo ""
echo "--- Rollback Flag ---"

HAS_ROLLBACK_FLAG=$(grep -c 'ROLLBACK RECOMMENDED' "$PIPELINE_FILE" || true)
run_test "ROLLBACK RECOMMENDED flag documented (exact match)" "$( [ "$HAS_ROLLBACK_FLAG" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Threshold-based rollback trigger
# =============================================================================
echo ""
echo "--- Threshold Trigger ---"

HAS_THRESHOLD_TRIGGER=$(grep -ciE '(threshold.*rollback|rollback.*threshold|composite.*delta.*below|below.*threshold)' "$PIPELINE_FILE" || true)
run_test "Threshold-based rollback trigger documented" "$( [ "$HAS_THRESHOLD_TRIGGER" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Agent file path for rollback target
# =============================================================================
echo ""
echo "--- Rollback Target Path ---"

HAS_FILE_PATH=$(grep -ciE '(file.path|\.claude/agents/|agent.*path|rollback.*file|revert.*file)' "$PIPELINE_FILE" || true)
run_test "Agent file path for rollback documented" "$( [ "$HAS_FILE_PATH" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Rollback exercise process documented
# Per EPIC-062: "Rollback exercised for at least 1 component to verify capability"
# =============================================================================
echo ""
echo "--- Rollback Exercise Process ---"

HAS_EXERCISE=$(grep -ciE '(rollback.*exercise|exercise.*rollback|rollback.*process|rollback.*procedure|verify.*rollback)' "$PIPELINE_FILE" || true)
run_test "Rollback exercise process documented" "$( [ "$HAS_EXERCISE" -ge 1 ] && echo 0 || echo 1 )"

HAS_STEPS=$(grep -ciE '(step.*1|step.*2|step.*3|1\.\s|2\.\s|3\.\s)' "$PIPELINE_FILE" || true)
run_test "Rollback process includes numbered steps" "$( [ "$HAS_STEPS" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 7: Results file supports regression display
# =============================================================================
echo ""
echo "--- Results Regression Display ---"

if [ -f "$RESULTS_FILE" ]; then
    HAS_REGRESSION_DISPLAY=$(grep -ciE '(regression|ROLLBACK|negative)' "$RESULTS_FILE" || true)
    run_test "Results template supports regression display" "$( [ "$HAS_REGRESSION_DISPLAY" -ge 1 ] && echo 0 || echo 1 )"
else
    run_test "Results file exists for regression display check" "1"
fi

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
