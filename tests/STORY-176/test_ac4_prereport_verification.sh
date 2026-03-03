#!/bin/bash
###############################################################################
# Test Suite: STORY-176 - AC#4: Pre-Report Verification
# Purpose: Verify path exists in source-tree.md before flagging structure violation
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

echo "STORY-176 AC#4: Pre-Report Verification"
echo "Target: $SCANNER_FILE"

if [ ! -f "$SCANNER_FILE" ]; then
    echo ""
    echo "ERROR: Scanner file does not exist: $SCANNER_FILE"
    exit 1
fi

header "AC#4: Pre-Report Verification Section"

test_case "## Pre-Report Verification section exists"
if grep -q "^## Pre-Report Verification$" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found '## Pre-Report Verification' section header"
else
    fail_test "Missing '## Pre-Report Verification' section header"
fi

test_case "Pre-Report Verification mentions source-tree.md check"
if grep -qi "source-tree\|source_tree" "$SCANNER_FILE" 2>/dev/null && \
   grep -qi "verify\|check\|validate.*before.*report\|before.*flag" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Pre-Report Verification mentions source-tree.md check"
else
    fail_test "No mention of source-tree.md verification before flagging"
fi

test_case "Verification happens before flagging structure violations"
# Look for workflow that checks source-tree.md before reporting
if grep -qi "before.*flag\|verify.*before.*report\|check.*path.*exists" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Verification occurs before flagging violations"
else
    fail_test "No explicit 'verify before flag' workflow documented"
fi

test_case "Path existence check is documented"
if grep -qi "path.*exist\|exist.*path\|directory.*valid\|valid.*directory" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Path existence check is documented"
else
    fail_test "No path existence check documentation"
fi

test_case "False positive prevention rationale documented"
if grep -qi "false positive\|prevent.*incorrect\|avoid.*wrong\|reduce.*noise" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "False positive prevention rationale documented"
else
    fail_test "No rationale for why pre-report verification prevents false positives"
fi

test_case "Integration with Phase 3 (Structure Violations) documented"
# Pre-report verification should specifically apply to structure violations
if grep -qi "pre-report.*structure\|structure.*verify.*before\|phase 3.*verify" "$SCANNER_FILE" 2>/dev/null || \
   grep -qi "structure violation.*source-tree" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Pre-report verification linked to structure violation detection"
else
    fail_test "No explicit link between pre-report verification and Phase 3"
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
