#!/bin/bash
# Test: AC#3 - Proven Fix documents mechanical checkpoint solution
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

echo "=== AC#3: Proven Fix documents mechanical checkpoint solution ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file $TARGET_FILE does not exist"
    echo ""
    echo "Results: 0 passed, 3 failed"
    exit 1
fi

# Extract the Proven Fix section from within the pattern entry
PROVEN_FIX_SECTION=$(grep -A 50 "Prompt-Only Phase Enforcement Failure" "$TARGET_FILE" | grep -A 15 -i "Proven Fix")

# === Act & Assert ===

# Test 1: RCA-022 CLI gates referenced in Proven Fix
echo "$PROVEN_FIX_SECTION" | grep -q "RCA-022"
run_test "RCA-022 CLI gates referenced in Proven Fix" $?

# Test 2: RCA-040 Grep-based checkpoints referenced in Proven Fix
echo "$PROVEN_FIX_SECTION" | grep -q "RCA-040"
run_test "RCA-040 Grep-based checkpoints referenced in Proven Fix" $?

# Test 3: Statement that prompt-only enforcement is insufficient
echo "$PROVEN_FIX_SECTION" | grep -qi "prompt-only"
run_test "Statement about prompt-only enforcement insufficiency present" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
