#!/bin/bash
# Test: AC#1 - Post-Write Cross-Reference Update Step Exists
# Story: STORY-510
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/designing-systems/references/artifact-generation.md"

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

echo "=== AC#1: Post-Write Cross-Reference Update Step Exists ==="
echo ""

# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: A cross-reference update step exists
grep -q "EPIC-NNN" "$TARGET_FILE" && grep -q "EPIC-XXX" "$TARGET_FILE"
run_test "Step references EPIC-NNN to EPIC-XXX replacement" $?

# Test 2: Step references ADR-NNN replacement
grep -q "ADR-NNN" "$TARGET_FILE" && grep -q "ADR-XXX" "$TARGET_FILE"
run_test "Step references ADR-NNN to ADR-XXX replacement" $?

# Test 3: A step number exists for cross-reference update (e.g., Step 6.7.5 or similar)
grep -qi "cross-reference\|cross.reference" "$TARGET_FILE"
run_test "Cross-reference update step heading exists" $?

# Test 4: Step instructs reading the source requirements document
grep -qi "read.*requirements\|source.*requirements.*document\|requirements.*doc" "$TARGET_FILE"
run_test "Step instructs reading source requirements document" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
