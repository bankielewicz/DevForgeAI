#!/bin/bash
###############################################################################
# Test Suite: STORY-176 - AC#5: Skip Security Scanning on Code Examples
# Purpose: Verify Markdown fenced code blocks are not scanned in Phase 6
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

echo "STORY-176 AC#5: Skip Security Scanning on Code Examples"
echo "Target: $SCANNER_FILE"

if [ ! -f "$SCANNER_FILE" ]; then
    echo ""
    echo "ERROR: Scanner file does not exist: $SCANNER_FILE"
    exit 1
fi

header "AC#5: Phase 6 Code Example Exclusion"

test_case "Phase 6 section exists"
if grep -q "^### Phase 6:" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found Phase 6 section"
else
    fail_test "Missing Phase 6 section header"
fi

test_case "Phase 6 is Security Vulnerabilities Scanning"
if grep -q "Phase 6.*Security\|Phase 6:.*Category 5" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Phase 6 is Security Vulnerabilities Scanning (Category 5)"
else
    fail_test "Phase 6 does not identify as Security Vulnerabilities Scanning"
fi

test_case "Phase 6 mentions fenced code block exclusion"
# Extract Phase 6 section content
phase6_content=$(sed -n '/^### Phase 6:/,/^### Phase [7-9]/p' "$SCANNER_FILE" 2>/dev/null || echo "")

if echo "$phase6_content" | grep -qi "fenced\|code block\|\`\`\`\|example" 2>/dev/null && \
   echo "$phase6_content" | grep -qi "skip\|exclude\|ignore" 2>/dev/null; then
    pass_test "Phase 6 mentions skipping fenced code blocks"
else
    fail_test "Phase 6 does not mention skipping fenced code blocks"
fi

test_case "Code examples in Markdown files are excluded from security scanning"
if grep -qi "markdown.*example.*skip\|example.*code.*exclude\|code.*block.*not.*scan" "$SCANNER_FILE" 2>/dev/null || \
   grep -qi "skip.*code.*example\|exclude.*fenced" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Code examples explicitly excluded from security scanning"
else
    fail_test "No explicit exclusion of code examples from security scanning"
fi

test_case "Rationale: Code examples demonstrate patterns, not production code"
if grep -qi "example\|demonstration\|illustration\|not.*production\|sample" "$SCANNER_FILE" 2>/dev/null && \
   grep -qi "exclude\|skip\|reason" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Rationale for skipping code examples documented"
else
    fail_test "No rationale for why code examples should be skipped"
fi

test_case "Exclusion applies to all Markdown files with code blocks"
# Check that exclusion covers .md files generally
if grep -qi "\.md.*code\|markdown.*fenced\|\.md.*example" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Exclusion applies to Markdown files with code blocks"
else
    fail_test "Exclusion not explicitly tied to Markdown file type"
fi

test_case "Code block detection mechanism documented"
# Should document how to detect fenced code blocks (``` markers)
if grep -q '\`\`\`' "$SCANNER_FILE" 2>/dev/null || \
   grep -qi "triple backtick\|fenced.*marker\|code.*fence" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Code block detection mechanism documented"
else
    fail_test "No mechanism for detecting fenced code blocks"
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
