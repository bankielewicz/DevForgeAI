#!/bin/bash
# Test: AC#3 - Before/After Comparison Demonstrates Quality Improvement
# Story: STORY-393
# Generated: 2026-02-12
# Target: devforgeai/specs/research/evaluation-results.md

set -uo pipefail

PASSED=0
FAILED=0
EVAL_FILE="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/research/evaluation-results.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#3: Before/After Comparison ==="
echo ""

# === Test 1: Evaluation results file exists ===
if [ -f "$EVAL_FILE" ]; then
    run_test "Evaluation results file exists" 0
else
    run_test "Evaluation results file exists" 1
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# === Test 2: Contains requirements-analyst evaluation ===
grep -qi "requirements-analyst" "$EVAL_FILE" && run_test "Evaluation file references requirements-analyst" 0 || run_test "Evaluation file references requirements-analyst" 1

# === Test 3: Contains comparison table ===
grep -qE "\|.*\|.*\|" "$EVAL_FILE" && run_test "Evaluation file contains markdown table" 0 || run_test "Evaluation file contains markdown table" 1

# === Test 4: Dimension 1 - Section completeness evaluated ===
grep -qi "section completeness" "$EVAL_FILE" && run_test "Dimension evaluated: Section completeness" 0 || run_test "Dimension evaluated: Section completeness" 1

# === Test 5: Dimension 2 - Prompt clarity evaluated ===
grep -qi "prompt clarity" "$EVAL_FILE" && run_test "Dimension evaluated: Prompt clarity" 0 || run_test "Dimension evaluated: Prompt clarity" 1

# === Test 6: Dimension 3 - Example coverage evaluated ===
grep -qi "example coverage" "$EVAL_FILE" && run_test "Dimension evaluated: Example coverage" 0 || run_test "Dimension evaluated: Example coverage" 1

# === Test 7: Dimension 4 - Constraint explicitness evaluated ===
grep -qi "constraint explicitness" "$EVAL_FILE" && run_test "Dimension evaluated: Constraint explicitness" 0 || run_test "Dimension evaluated: Constraint explicitness" 1

# === Test 8: Dimension 5 - Input/Output specification evaluated ===
grep -qiE "input.output specification" "$EVAL_FILE" && run_test "Dimension evaluated: Input/Output specification" 0 || run_test "Dimension evaluated: Input/Output specification" 1

# === Test 9: At least 5 dimensions present ===
DIM_COUNT=0
grep -qi "section completeness" "$EVAL_FILE" && DIM_COUNT=$((DIM_COUNT + 1)) || true
grep -qi "prompt clarity" "$EVAL_FILE" && DIM_COUNT=$((DIM_COUNT + 1)) || true
grep -qi "example coverage" "$EVAL_FILE" && DIM_COUNT=$((DIM_COUNT + 1)) || true
grep -qi "constraint explicitness" "$EVAL_FILE" && DIM_COUNT=$((DIM_COUNT + 1)) || true
grep -qiE "input.output specification" "$EVAL_FILE" && DIM_COUNT=$((DIM_COUNT + 1)) || true
[ "$DIM_COUNT" -ge 5 ] && run_test "At least 5 evaluation dimensions present (count=$DIM_COUNT)" 0 || run_test "At least 5 evaluation dimensions present (count=$DIM_COUNT)" 1

# === Test 10: At least 3 dimensions show improvement ===
IMPROVED_COUNT=$(grep -ciE "improved|better|enhanced|increased" "$EVAL_FILE" || echo "0")
[ "$IMPROVED_COUNT" -ge 3 ] && run_test "At least 3 dimensions show improvement (count=$IMPROVED_COUNT)" 0 || run_test "At least 3 dimensions show improvement (count=$IMPROVED_COUNT)" 1

# === Test 11: No dimension shows regression ===
if grep -qiE "regressed|worse|degraded|decreased" "$EVAL_FILE" 2>/dev/null; then
    REGRESSED_COUNT=$(grep -ciE "regressed|worse|degraded|decreased" "$EVAL_FILE")
    run_test "No dimensions show regression (count=$REGRESSED_COUNT)" 1
else
    run_test "No dimensions show regression (count=0)" 0
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
