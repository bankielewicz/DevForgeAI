#!/bin/bash
# Test: AC#5 - Skip Behavior When No Heuristics Trigger
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET="$PROJECT_ROOT/src/claude/skills/designing-systems/references/domain-reference-generation.md"
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

echo "=== AC#5: Skip Behavior When No Heuristics Trigger ==="

# Test 1: Documents skip behavior
grep -iq "skip" "$TARGET"
run_test "test_should_document_skip_behavior_when_reference_checked" $?

# Test 2: Contains "No domain references needed" message
grep -q "No domain references needed" "$TARGET"
run_test "test_should_contain_no_domain_refs_needed_message_when_checked" $?

# Test 3: Non-blocking, proceeds to Phase 6
grep -iq "Phase 6" "$TARGET" || grep -iq "non-blocking" "$TARGET"
run_test "test_should_be_nonblocking_proceed_to_phase6_when_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
