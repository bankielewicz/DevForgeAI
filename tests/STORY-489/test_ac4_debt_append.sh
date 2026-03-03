#!/bin/bash
# Test: AC#4 - Debt Register Append Works
# Story: STORY-489
# Generated: 2026-02-23

set -e

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/devforgeai-rca/SKILL.md"

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

echo "=== AC#4: Debt Register Append Works ==="

# Extract Phase 7.5 section for targeted testing
PHASE75_START=$(grep -n "Phase 7.5" "$TARGET_FILE" | head -1 | cut -d: -f1)

# Test 1: References technical-debt-register.md
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "technical-debt-register.md" 2>/dev/null
run_test "References technical-debt-register.md" $?

# Test 2: Mentions RCA number provenance
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "RCA-" 2>/dev/null
run_test "Mentions RCA number provenance" $?

# Test 3: Mentions recommendation ID provenance
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "REC-" 2>/dev/null
run_test "Mentions recommendation ID provenance" $?

# Test 4: Mentions Source provenance format
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "Source:" 2>/dev/null
run_test "Mentions Source provenance format" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
