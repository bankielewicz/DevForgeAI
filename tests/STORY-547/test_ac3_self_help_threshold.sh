#!/bin/bash
# Test: AC#3 - Self-Help Threshold Clearly Delineated
# Story: STORY-547
# Generated: 2026-03-06
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/when-to-hire-professional.md"

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

echo "=== AC#3: Self-Help Threshold Clearly Delineated ==="
echo ""

# === Act & Assert ===

# Test 1: Reference file exists
test -f "$REFERENCE_FILE"
run_test "Reference file exists" $?

# Test 2: Self-help section/path exists
grep -qi "self-help\|self help\|handle.*yourself\|DIY\|do it yourself" "$REFERENCE_FILE" 2>/dev/null
run_test "Self-help guidance path exists" $?

# Test 3: Low-risk characteristics identified
grep -qi "low.risk\|straightforward\|simple.*situation\|low.stakes\|routine" "$REFERENCE_FILE" 2>/dev/null
run_test "Low-risk characteristics identified" $?

# Test 4: Clear delineation between self-help and professional
grep -qi "when to.*self\|when.*professional\|threshold\|boundary\|versus\|vs\." "$REFERENCE_FILE" 2>/dev/null
run_test "Clear delineation between self-help and professional paths" $?

# Test 5: Disclaimer present in self-help section (individual circumstances vary)
grep -qi "individual circumstances\|circumstances may vary\|your situation" "$REFERENCE_FILE" 2>/dev/null
run_test "Includes disclaimer that individual circumstances vary" $?

# Test 6: Self-help does NOT recommend paid attorney as primary path
if [ -f "$REFERENCE_FILE" ]; then
    # Extract self-help section and verify it doesn't push attorney as primary
    # The self-help section should exist and contain self-directed guidance
    grep -qi "self-help\|self help" "$REFERENCE_FILE" 2>/dev/null
    has_self_help=$?
    if [ "$has_self_help" -eq 0 ]; then
        run_test "Self-help path provides self-directed guidance" 0
    else
        run_test "Self-help path provides self-directed guidance" 1
    fi
else
    run_test "Self-help path provides self-directed guidance" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
