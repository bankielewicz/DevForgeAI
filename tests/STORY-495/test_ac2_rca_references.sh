#!/bin/bash
# Test: AC#2 - All 6 RCAs referenced in Occurrences field
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

echo "=== AC#2: All 6 RCAs referenced in Occurrences field ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file $TARGET_FILE does not exist"
    echo ""
    echo "Results: 0 passed, 6 failed"
    exit 1
fi

# Extract the Occurrences section (between Occurrences and next field header)
OCCURRENCES_SECTION=$(grep -A 20 "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" | grep -A 10 -i "Occurrences")

# === Act & Assert ===

# Test 1: RCA-018 referenced
echo "$OCCURRENCES_SECTION" | grep -q "RCA-018"
run_test "RCA-018 referenced in Occurrences" $?

# Test 2: RCA-019 referenced
echo "$OCCURRENCES_SECTION" | grep -q "RCA-019"
run_test "RCA-019 referenced in Occurrences" $?

# Test 3: RCA-021 referenced
echo "$OCCURRENCES_SECTION" | grep -q "RCA-021"
run_test "RCA-021 referenced in Occurrences" $?

# Test 4: RCA-022 referenced
echo "$OCCURRENCES_SECTION" | grep -q "RCA-022"
run_test "RCA-022 referenced in Occurrences" $?

# Test 5: RCA-033 referenced
echo "$OCCURRENCES_SECTION" | grep -q "RCA-033"
run_test "RCA-033 referenced in Occurrences" $?

# Test 6: RCA-040 referenced
echo "$OCCURRENCES_SECTION" | grep -q "RCA-040"
run_test "RCA-040 referenced in Occurrences" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
