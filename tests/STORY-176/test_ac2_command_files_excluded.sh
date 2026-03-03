#!/bin/bash
###############################################################################
# Test Suite: STORY-176 - AC#2: Command Files Excluded from Structure Validation
# Purpose: Verify files matching .claude/commands/*.md are skipped in Phase 3
# TDD Phase: RED (tests should FAIL until implementation)
###############################################################################

set -euo pipefail

SCANNER_FILE="src/claude/agents/anti-pattern-scanner.md"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

pass_test() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "  PASS: $1"
}

fail_test() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "  FAIL: $1"
}

test_case() {
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "Test $TEST_COUNT: $1"
}

header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

echo "STORY-176 AC#2: Command Files Excluded from Structure Validation"
echo "Target: $SCANNER_FILE"

if [ ! -f "$SCANNER_FILE" ]; then
    echo ""
    echo "ERROR: Scanner file does not exist: $SCANNER_FILE"
    exit 1
fi

header "AC#2: Phase 3 Command File Exclusion"

test_case "Phase 3 section exists"
if grep -q "^### Phase 3:" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found Phase 3 section"
else
    fail_test "Missing Phase 3 section header"
fi

test_case "Phase 3 mentions command file exclusion"
# Extract Phase 3 section content
phase3_content=$(sed -n '/^### Phase 3:/,/^### Phase [4-9]/p' "$SCANNER_FILE" 2>/dev/null || echo "")

if echo "$phase3_content" | grep -qi "skip\|exclude\|ignore" 2>/dev/null && \
   echo "$phase3_content" | grep -qi "command" 2>/dev/null; then
    pass_test "Phase 3 mentions skipping/excluding command files"
else
    fail_test "Phase 3 does not mention skipping command files"
fi

test_case "Phase 3 references .claude/commands pattern"
if echo "$phase3_content" | grep -q '\.claude/commands' 2>/dev/null; then
    pass_test "Phase 3 references .claude/commands pattern"
else
    fail_test "Phase 3 does not reference .claude/commands pattern"
fi

test_case "Phase 3 mentions logging when skipping files"
if echo "$phase3_content" | grep -qi "log\|message\|skip.*log\|exclude.*message" 2>/dev/null; then
    pass_test "Phase 3 mentions logging for skipped files"
else
    fail_test "Phase 3 does not mention logging when skipping files"
fi

test_case "Exclusion applies specifically to Structure Violations (Category 2)"
# Structure Violations is Category 2, mentioned in Phase 3
if grep -q "Structure Violations" "$SCANNER_FILE" 2>/dev/null && \
   grep -qi "exclude.*structure\|skip.*structure\|structure.*skip\|structure.*exclude" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Exclusion applies to Structure Violations scanning"
else
    fail_test "No explicit link between exclusion and Structure Violations"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    echo "STATUS: RED PHASE - Tests failing as expected (TDD)"
    exit 1
else
    echo "STATUS: GREEN PHASE - All tests passing"
    exit 0
fi
