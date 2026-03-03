#!/bin/bash
# Test: AC#5 - Before/After Quality Comparison Shows Improvement
# Story: STORY-398
# Generated: 2026-02-13

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/devforgeai/specs/EPIC-062-migration-signoff.md"

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

echo "=== AC#5: Before/After Quality Comparison ==="
echo ""

# --- Arrange ---
# Target: Sign-off document contains comparison table

# --- Act & Assert ---

# Test 1: Sign-off document exists (prerequisite for AC5)
test -f "$TARGET_FILE"
run_test "Sign-off document exists (prerequisite)" $?

# Test 2: Contains comparison table (markdown table with pipes)
grep -qE '^\|.*\|.*\|' "$TARGET_FILE"
run_test "Contains markdown comparison table" $?

# Test 3: Comparison includes template conformance metric
grep -qi "template conformance" "$TARGET_FILE"
run_test "Comparison includes template conformance metric" $?

# Test 4: Comparison includes prompt pattern coverage metric
grep -qi "prompt pattern coverage" "$TARGET_FILE"
run_test "Comparison includes prompt pattern coverage metric" $?

# Test 5: Comparison includes structural consistency metric
grep -qi "structural consistency" "$TARGET_FILE"
run_test "Comparison includes structural consistency metric" $?

# Test 6: Comparison includes documentation completeness metric
grep -qi "documentation completeness" "$TARGET_FILE"
run_test "Comparison includes documentation completeness metric" $?

# Test 7: Comparison includes output format specification metric
grep -qi "output format specification" "$TARGET_FILE"
run_test "Comparison includes output format specification metric" $?

# Test 8: At least 5 metrics present in comparison (5+ table rows with data)
METRIC_COUNT=$(grep -ciE '(template conformance|prompt pattern|structural consistency|documentation completeness|output format)' "$TARGET_FILE")
[ "$METRIC_COUNT" -ge 5 ]
run_test "At least 5 metrics in comparison (found: $METRIC_COUNT)" $?

# Test 9: No quality dimension shows regression
# A regression would be indicated by words like "decreased", "worse", "regression", "declined"
! grep -qiE '(decreased|worse|regression|declined|degraded)' "$TARGET_FILE"
run_test "No quality dimension shows regression" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
