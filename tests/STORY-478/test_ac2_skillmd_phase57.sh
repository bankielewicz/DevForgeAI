#!/bin/bash
# Test: AC#2 - SKILL.md Phase 5.7 Insertion
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET="$PROJECT_ROOT/src/claude/skills/designing-systems/SKILL.md"
PASSED=0
FAILED=0

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

echo "=== AC#2: SKILL.md Phase 5.7 Insertion ==="

# Test 1: Contains Phase 5.7 header
grep -q "Phase 5\.7" "$TARGET"
run_test "test_should_contain_phase57_header_when_skillmd_checked" $?

# Test 2: Phase 5.7 appears after Phase 5.5
PHASE55_LINE=$(grep -n "Phase 5\.5" "$TARGET" | head -1 | cut -d: -f1)
PHASE57_LINE=$(grep -n "Phase 5\.7" "$TARGET" | head -1 | cut -d: -f1)
[ -n "$PHASE57_LINE" ] && [ "$PHASE57_LINE" -gt "$PHASE55_LINE" ]
run_test "test_should_appear_after_phase55_when_order_checked" $?

# Test 3: Phase 5.7 appears before Phase 6 header
PHASE6_LINE=$(grep -n "^### Phase 6" "$TARGET" | head -1 | cut -d: -f1)
[ -n "$PHASE57_LINE" ] && [ "$PHASE57_LINE" -lt "$PHASE6_LINE" ]
run_test "test_should_appear_before_phase6_when_order_checked" $?

# Test 4: Contains Read() for on-demand reference loading
grep -A 30 "Phase 5\.7" "$TARGET" | grep -q "Read("
run_test "test_should_contain_read_instruction_when_phase57_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
