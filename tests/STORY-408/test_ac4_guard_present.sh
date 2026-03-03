#!/bin/bash
# Test: AC#4 - Pre-invocation guard section present at top of command
# Story: STORY-408
# Generated: 2026-02-16

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/create-story.md"

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

echo "=== AC#4: Pre-invocation guard section present ==="

# Test 1: Guard section header exists
grep -qi 'lean orchestration' "$TARGET_FILE"
run_test "Lean Orchestration guard section exists" $?

# Test 2: DO NOT list exists with at least 4 items
# Look for "DO NOT" header/marker followed by list items
DO_NOT_COUNT=$(grep -c 'DO NOT' "$TARGET_FILE")
[ "$DO_NOT_COUNT" -ge 1 ]
run_test "DO NOT section marker exists" $?

# Count prohibited action items (lines with DO NOT or bullet items after DO NOT header)
PROHIBIT_COUNT=$(grep -cE '^\s*[-*]\s+.*DO NOT|^\s*[-*]\s+.*NEVER|^\s*[-*]\s+.*FORBIDDEN' "$TARGET_FILE")
if [ "$PROHIBIT_COUNT" -lt 4 ]; then
    # Alternative: count bullet items in DO NOT section
    PROHIBIT_COUNT=$(sed -n '/DO NOT/,/^##\|^DO:/p' "$TARGET_FILE" | grep -cE '^\s*[-*]\s')
fi
echo "    INFO: Found $PROHIBIT_COUNT prohibited action items"
[ "$PROHIBIT_COUNT" -ge 4 ]
run_test "DO NOT list has 4+ prohibited actions (found $PROHIBIT_COUNT)" $?

# Test 3: DO list exists with at least 3 items
DO_COUNT=$(sed -n '/^.*DO:/,/^##\|^---/p' "$TARGET_FILE" | grep -cE '^\s*[-*]\s')
if [ "$DO_COUNT" -lt 3 ]; then
    # Alternative: look for permitted actions list
    DO_COUNT=$(grep -cE '^\s*[-*]\s+.*MUST\s|^\s*[-*]\s+.*ALWAYS\s|^\s*[-*]\s+.*DO:\s' "$TARGET_FILE")
fi
echo "    INFO: Found $DO_COUNT permitted action items"
[ "$DO_COUNT" -ge 3 ]
run_test "DO list has 3+ permitted actions (found $DO_COUNT)" $?

# Test 4: Guard section appears before any Phase documentation
GUARD_LINE=$(grep -n -i 'lean orchestration' "$TARGET_FILE" | head -1 | cut -d: -f1)
PHASE_LINE=$(grep -n -iE '^#+\s*(Phase|Step)\s+[0-9]' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$GUARD_LINE" ] && [ -n "$PHASE_LINE" ]; then
    [ "$GUARD_LINE" -lt "$PHASE_LINE" ]
    run_test "Guard section (line $GUARD_LINE) before Phase docs (line $PHASE_LINE)" $?
else
    run_test "Both guard section and phase docs found for position check" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
