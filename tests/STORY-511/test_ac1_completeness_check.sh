#!/bin/bash
# Test: AC#1 - Decision Context Completeness Check Added
# Story: STORY-511
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE=".claude/agents/context-preservation-validator.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#1: Decision Context Completeness Check ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Decision Context Completeness Check section exists
grep -q "Decision Context Completeness Check" "$TARGET_FILE"
run_test "Decision Context Completeness Check section exists" $?

# Test 2: Validates Design Rationale is non-empty
grep -q "Design Rationale" "$TARGET_FILE" && grep -q "non-empty\|not empty\|is populated\|has content" "$TARGET_FILE"
run_test "Validates Design Rationale is non-empty" $?

# Test 3: Validates Rejected Alternatives has at least 1 entry
grep -q "Rejected Alternatives" "$TARGET_FILE" && grep -q "at least 1\|at least one\|minimum 1\|has entries" "$TARGET_FILE"
run_test "Validates Rejected Alternatives has at least 1 entry" $?

# Test 4: Validates Implementation Constraints is non-empty
grep -q "Implementation Constraints" "$TARGET_FILE" && grep -q "non-empty\|not empty\|is populated\|has content" "$TARGET_FILE"
run_test "Validates Implementation Constraints is non-empty" $?

# Test 5: All three validations appear together in a completeness check context
grep -A 20 "Decision Context Completeness Check" "$TARGET_FILE" | grep -q "Design Rationale"
run_test "Design Rationale referenced within completeness check section" $?

grep -A 20 "Decision Context Completeness Check" "$TARGET_FILE" | grep -q "Rejected Alternatives"
run_test "Rejected Alternatives referenced within completeness check section" $?

grep -A 20 "Decision Context Completeness Check" "$TARGET_FILE" | grep -q "Implementation Constraints"
run_test "Implementation Constraints referenced within completeness check section" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
