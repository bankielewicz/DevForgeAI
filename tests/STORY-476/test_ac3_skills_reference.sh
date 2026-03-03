#!/bin/bash
# Test: AC#3 - skills-reference.md Updated with Phase 5.5
# Story: STORY-476
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET="src/claude/memory/skills-reference.md"

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

echo "=== AC#3: skills-reference.md Updated with Phase 5.5 ==="

# Test 1: Phase 5.5 mentioned in designing-systems entry
grep -A 100 'designing-systems' "$TARGET" | grep -q 'Phase 5\.5'
run_test "Phase 5.5 mentioned in designing-systems entry" $?

# Test 2: Phase 5.5 listed between Phase 5 and Phase 6
PHASE5_LINE=$(grep -n 'Phase 5[^.]' "$TARGET" | head -1 | cut -d: -f1)
PHASE6_LINE=$(grep -n 'Phase 6' "$TARGET" | head -1 | cut -d: -f1)
PHASE55_LINE=$(grep -n 'Phase 5\.5' "$TARGET" | head -1 | cut -d: -f1)
if [ -n "$PHASE5_LINE" ] && [ -n "$PHASE6_LINE" ] && [ -n "$PHASE55_LINE" ]; then
    [ "$PHASE55_LINE" -gt "$PHASE5_LINE" ] && [ "$PHASE55_LINE" -lt "$PHASE6_LINE" ]
    run_test "Phase 5.5 listed between Phase 5 and Phase 6" $?
else
    run_test "Phase 5.5 listed between Phase 5 and Phase 6" 1
fi

# Test 3: prompt-alignment-workflow.md in reference files list
grep -q 'prompt-alignment-workflow\.md' "$TARGET"
run_test "prompt-alignment-workflow.md in reference files list" $?

# Test 4: alignment-auditor mentioned for Phase 5.5 subagent integration
grep -A 5 'Phase 5\.5' "$TARGET" | grep -q 'alignment-auditor'
run_test "alignment-auditor mentioned for Phase 5.5" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
