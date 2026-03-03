#!/bin/bash
# Test: AC#5 - Orchestration reference file audit completed
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - audit not yet performed)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

AUDIT_FILE="${PROJECT_ROOT}/devforgeai/specs/analysis/STORY-458-orchestration-reference-audit.md"

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=============================================="
echo "  AC#5: Orchestration Reference Audit"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# === Test 1: Audit file exists ===
test_result=0
if [ -f "$AUDIT_FILE" ]; then
    test_result=0
else
    test_result=1
fi
run_test "Audit report exists at expected path" "$test_result"

# === Test 2: Contains merge candidates section ===
test_result=0
if [ -f "$AUDIT_FILE" ] && grep -qi 'merge candidate' "$AUDIT_FILE"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains merge candidates section" "$test_result"

# === Test 3: Contains archive candidates section ===
test_result=0
if [ -f "$AUDIT_FILE" ] && grep -qi 'archive candidate' "$AUDIT_FILE"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains archive candidates section" "$test_result"

# === Test 4: Contains retain-as-is section ===
test_result=0
if [ -f "$AUDIT_FILE" ] && grep -qi 'retain.as.is\|retain as.is\|retain-as-is' "$AUDIT_FILE"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains retain-as-is section" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
