#!/usr/bin/env bash
# =============================================================================
# STORY-391 AC#3: Before/After Comparison Demonstrates Quality Improvement
#
# Verifies:
# 1. Evaluation results file exists at devforgeai/specs/research/evaluation-results.md
# 2. Contains a structured comparison table with at least 5 dimensions
# 3. At least 3 of 5 dimensions show improvement
# 4. No dimension shows regression
# 5. Required dimensions: section completeness, prompt clarity,
#    example coverage, constraint explicitness, I/O specification
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
EVAL_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-results.md"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

# --- Test Helper ---
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
echo "STORY-391 AC#3: Before/After Comparison Tests"
echo "Evaluation: ${EVAL_FILE}"
echo "================================================================"
echo ""

# =============================================================================
# Test 1: Evaluation results file exists
# =============================================================================
echo "--- File Existence ---"

if [ -f "$EVAL_FILE" ]; then
    run_test "Evaluation results file exists" "0"
else
    run_test "Evaluation results file exists" "1"
    echo ""
    echo "FATAL: Evaluation file not found. Remaining tests will fail."
    echo "================================================================"
    echo "AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
    echo "================================================================"
    exit 1
fi

# =============================================================================
# Test 2: Contains comparison table
# =============================================================================
echo ""
echo "--- Comparison Table Structure ---"

# Check for markdown table markers (pipe-delimited rows)
TABLE_ROWS=$(grep -cE '^\|.*\|.*\|' "$EVAL_FILE" || true)
run_test "Evaluation file contains a markdown table (rows found: ${TABLE_ROWS})" "$( [ "$TABLE_ROWS" -ge 6 ] && echo 0 || echo 1 )"

# Check for table header separator (|---|---|)
TABLE_SEPARATOR=$(grep -cE '^\|[-: ]+\|' "$EVAL_FILE" || true)
run_test "Table has header separator row" "$( [ "$TABLE_SEPARATOR" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Contains at least 5 comparison dimensions
# =============================================================================
echo ""
echo "--- Required Dimensions ---"

# Dimension 1: Section completeness
DIM_SECTIONS=$(grep -ciE 'section completeness|sections present|required sections' "$EVAL_FILE" || true)
run_test "Dimension 1: Section completeness documented" "$( [ "$DIM_SECTIONS" -ge 1 ] && echo 0 || echo 1 )"

# Dimension 2: Prompt clarity
DIM_CLARITY=$(grep -ciE 'prompt clarity|explicit.*instructions|implicit.*instructions|instruction clarity' "$EVAL_FILE" || true)
run_test "Dimension 2: Prompt clarity documented" "$( [ "$DIM_CLARITY" -ge 1 ] && echo 0 || echo 1 )"

# Dimension 3: Example coverage
DIM_EXAMPLES=$(grep -ciE 'example coverage|worked examples|number of.*examples' "$EVAL_FILE" || true)
run_test "Dimension 3: Example coverage documented" "$( [ "$DIM_EXAMPLES" -ge 1 ] && echo 0 || echo 1 )"

# Dimension 4: Constraint explicitness
DIM_CONSTRAINTS=$(grep -ciE 'constraint explicit|DO.*DO NOT|explicit constraints|constraint.*lists' "$EVAL_FILE" || true)
run_test "Dimension 4: Constraint explicitness documented" "$( [ "$DIM_CONSTRAINTS" -ge 1 ] && echo 0 || echo 1 )"

# Dimension 5: Input/Output specification
DIM_IO=$(grep -ciE 'input.*output|I/O specification|defined.*undefined|input/output' "$EVAL_FILE" || true)
run_test "Dimension 5: Input/Output specification documented" "$( [ "$DIM_IO" -ge 1 ] && echo 0 || echo 1 )"

# Count total dimensions present (must be at least 5)
TOTAL_DIMENSIONS=0
[ "$DIM_SECTIONS" -ge 1 ] && TOTAL_DIMENSIONS=$((TOTAL_DIMENSIONS + 1))
[ "$DIM_CLARITY" -ge 1 ] && TOTAL_DIMENSIONS=$((TOTAL_DIMENSIONS + 1))
[ "$DIM_EXAMPLES" -ge 1 ] && TOTAL_DIMENSIONS=$((TOTAL_DIMENSIONS + 1))
[ "$DIM_CONSTRAINTS" -ge 1 ] && TOTAL_DIMENSIONS=$((TOTAL_DIMENSIONS + 1))
[ "$DIM_IO" -ge 1 ] && TOTAL_DIMENSIONS=$((TOTAL_DIMENSIONS + 1))

run_test "At least 5 dimensions documented (found: ${TOTAL_DIMENSIONS})" "$( [ "$TOTAL_DIMENSIONS" -ge 5 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: At least 3 dimensions show improvement
# =============================================================================
echo ""
echo "--- Improvement Verification ---"

# Look for improvement markers in table (Improved, Better, Added, Enhanced, +, upgrade)
IMPROVED_COUNT=$(grep -ciE 'improved|better|added|enhanced|upgrade' "$EVAL_FILE" || true)
run_test "At least 3 dimensions show improvement markers (found: ${IMPROVED_COUNT})" "$( [ "$IMPROVED_COUNT" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: No dimension shows regression
# =============================================================================
echo ""
echo "--- Regression Check ---"

# Look for regression markers (Regressed, Worse, Degraded, Removed, -)
REGRESSED_COUNT=$(grep -ciE 'regressed|worse|degraded|regression' "$EVAL_FILE" || true)
run_test "No dimensions show regression (regression markers found: ${REGRESSED_COUNT})" "$( [ "$REGRESSED_COUNT" -eq 0 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Before/After columns present
# =============================================================================
echo ""
echo "--- Before/After Structure ---"

HAS_BEFORE=$(grep -ciE '\bbefore\b' "$EVAL_FILE" || true)
run_test "Table contains 'Before' column/reference" "$( [ "$HAS_BEFORE" -ge 1 ] && echo 0 || echo 1 )"

HAS_AFTER=$(grep -ciE '\bafter\b' "$EVAL_FILE" || true)
run_test "Table contains 'After' column/reference" "$( [ "$HAS_AFTER" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 7: References test-automator specifically
# =============================================================================
echo ""
echo "--- Agent Reference ---"

HAS_AGENT_REF=$(grep -ciE 'test-automator|test.automator' "$EVAL_FILE" || true)
run_test "Evaluation references test-automator agent" "$( [ "$HAS_AGENT_REF" -ge 1 ] && echo 0 || echo 1 )"

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
