#!/bin/bash
# Test: AC#2 - Reference File Accessible from advising-legal Skill
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

echo "=== AC#2: Reference File Accessible from advising-legal Skill ==="
echo ""

# === Act & Assert ===

# Test 1: Reference file exists
test -f "$REFERENCE_FILE"
run_test "Reference file exists" $?

# Test 2: Guidance on finding a qualified attorney
grep -qi "find.*attorney\|finding.*attorney\|locating.*attorney\|how to find" "$REFERENCE_FILE" 2>/dev/null
run_test "Contains guidance on finding a qualified attorney" $?

# Test 3: Guidance on preparing for a consultation
grep -qi "prepar.*consultation\|consultation prep\|before.*meeting\|prepare for" "$REFERENCE_FILE" 2>/dev/null
run_test "Contains guidance on preparing for a consultation" $?

# Test 4: Guidance on evaluating attorney fit
grep -qi "evaluat.*attorney\|attorney fit\|choosing.*attorney\|assess.*attorney\|right fit" "$REFERENCE_FILE" 2>/dev/null
run_test "Contains guidance on evaluating attorney fit" $?

# Test 5: Disclaimer is included
grep -qi "disclaimer" "$REFERENCE_FILE" 2>/dev/null
run_test "Contains disclaimer" $?

# Test 6: File is readable (not empty)
if [ -f "$REFERENCE_FILE" ]; then
    file_size=$(wc -c < "$REFERENCE_FILE")
    [ "$file_size" -gt 100 ]
    run_test "File is not empty (size: ${file_size} bytes)" $?
else
    run_test "File is not empty" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
