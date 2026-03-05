#!/bin/bash
# Test: AC#2 - Copyright Section Explains Automatic Protection with Actionable Steps
# Story: STORY-545
# Generated: 2026-03-05
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/ip-protection-checklist.md"

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

echo "=== AC#2: Copyright Section Explains Automatic Protection ==="
echo ""

# === Arrange ===
# Reference file must exist

# === Act & Assert ===

# Test 1: Reference file exists (prerequisite)
test -f "$REFERENCE_FILE"
run_test "Reference file exists" $?

# Test 2: Copyright is automatic upon creation
grep -qi "automatic" "$REFERENCE_FILE" 2>/dev/null
run_test "Explains copyright is automatic upon creation" $?

# Test 3: Lists actionable steps - copyright notice
grep -qiE "copyright notice|notice.*copyright|\bcopyright.*\bnotice" "$REFERENCE_FILE" 2>/dev/null
run_test "Lists actionable step: copyright notices" $?

# Test 4: Lists actionable steps - registration
grep -qi "registration" "$REFERENCE_FILE" 2>/dev/null
run_test "Lists actionable step: registration" $?

# Test 5: Professional resource link present (copyright.gov or similar)
grep -qiE "copyright\.gov|https?://.*copyright" "$REFERENCE_FILE" 2>/dev/null
run_test "Includes professional resource link (e.g., copyright.gov)" $?

# Test 6: Clarifies registration is optional
grep -qiE "optional|not required|voluntary" "$REFERENCE_FILE" 2>/dev/null
run_test "Clarifies registration is optional" $?

# Test 7: Mentions registration strengthens remedies
grep -qiE "strengthen|statutory damages|remedies|enforcement" "$REFERENCE_FILE" 2>/dev/null
run_test "Explains registration strengthens remedies" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
