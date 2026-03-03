#!/bin/bash
# Test: AC#2 - HALT message includes expected path and text
# Story: STORY-514
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/implementing-stories/phases/phase-02-test-first.md"

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

echo "=== AC#2: HALT Message Content ==="

# === Test 1: HALT message contains exact required text ===
grep -q 'Snapshot file not created.*cannot complete Phase 02' "$TARGET_FILE"
run_test "HALT message contains exact text: Snapshot file not created - cannot complete Phase 02" $?

# === Test 2: HALT message includes the expected file path ===
grep -q 'red-phase-checksums\.json' "$TARGET_FILE" && \
grep -q 'HALT.*Snapshot file not created' "$TARGET_FILE"
run_test "HALT context includes snapshot file path reference" $?

# === Test 3: Exact HALT phrasing matches spec ===
grep -qF 'Snapshot file not created — cannot complete Phase 02' "$TARGET_FILE"
run_test "HALT uses exact phrasing with em-dash: Snapshot file not created — cannot complete Phase 02" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
