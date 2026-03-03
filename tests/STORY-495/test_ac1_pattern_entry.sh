#!/bin/bash
# Test: AC#1 - Pattern entry exists in PATTERNS.md
# Story: STORY-495
# Generated: 2026-02-23

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="devforgeai/RCA/PATTERNS.md"

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

echo "=== AC#1: Pattern entry exists in PATTERNS.md ==="
echo ""

# === Arrange ===
# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file $TARGET_FILE does not exist"
    echo ""
    echo "Results: 0 passed, 6 failed"
    exit 1
fi

# === Act & Assert ===

# Test 1: Section header present
grep -q "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE"
run_test "Section titled 'Prompt-Only Phase Enforcement Failure' exists" $?

# Test 2: Signature field present
grep -q "Signature" "$TARGET_FILE" | grep -q "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" 2>/dev/null
# Use a more targeted approach: find Signature field within the pattern section
grep -A 50 "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" | grep -qi "Signature"
run_test "Signature field present in pattern entry" $?

# Test 3: Occurrences field present
grep -A 50 "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" | grep -qi "Occurrences"
run_test "Occurrences field present in pattern entry" $?

# Test 4: Root Cause field present
grep -A 50 "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" | grep -qi "Root Cause"
run_test "Root Cause field present in pattern entry" $?

# Test 5: Proven Fix field present
grep -A 50 "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" | grep -qi "Proven Fix"
run_test "Proven Fix field present in pattern entry" $?

# Test 6: Detection field present
grep -A 50 "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" | grep -qi "Detection"
run_test "Detection field present in pattern entry" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
