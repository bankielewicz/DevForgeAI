#!/bin/bash
###############################################################################
# Test Suite: STORY-176 - AC#1: Exclusions Section Added
# Purpose: Verify anti-pattern-scanner.md includes ## Exclusions section
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

echo "STORY-176 AC#1: Exclusions Section Added"
echo "Target: $SCANNER_FILE"

# Check file exists
if [ ! -f "$SCANNER_FILE" ]; then
    echo ""
    echo "ERROR: Scanner file does not exist: $SCANNER_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "AC#1: Exclusions Section Validation"

test_case "## Exclusions section exists"
if grep -q "^## Exclusions$" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found '## Exclusions' section header"
else
    fail_test "Missing '## Exclusions' section header"
fi

test_case "Exclusions section has file pattern rules"
if grep -q "## Exclusions" "$SCANNER_FILE" 2>/dev/null; then
    # Check for pattern rules after Exclusions section
    exclusions_content=$(sed -n '/^## Exclusions$/,/^## /p' "$SCANNER_FILE" 2>/dev/null || echo "")

    if echo "$exclusions_content" | grep -q "pattern:" 2>/dev/null; then
        pass_test "Found pattern rules in Exclusions section"
    elif echo "$exclusions_content" | grep -q '\.claude/commands' 2>/dev/null; then
        pass_test "Found command file pattern in Exclusions section"
    else
        fail_test "No file pattern rules found in Exclusions section"
    fi
else
    fail_test "Cannot check pattern rules - Exclusions section missing"
fi

test_case "Exclusions section documents .claude/commands/*.md pattern"
if grep -q '\.claude/commands/\*\.md' "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found .claude/commands/*.md pattern"
else
    fail_test "Missing .claude/commands/*.md pattern"
fi

test_case "Exclusions section documents .claude/skills/**/*.md pattern"
if grep -q '\.claude/skills/\*\*/\*\.md' "$SCANNER_FILE" 2>/dev/null || \
   grep -q '\.claude/skills/\*\*' "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found .claude/skills/**/*.md pattern"
else
    fail_test "Missing .claude/skills/**/*.md pattern"
fi

test_case "Exclusions section documents .claude/agents/*.md pattern"
if grep -q '\.claude/agents/\*\.md' "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found .claude/agents/*.md pattern"
else
    fail_test "Missing .claude/agents/*.md pattern"
fi

test_case "Exclusions section specifies which phases each pattern excludes from"
if grep -q "excludes_from:\|Phase 3\|Phase 5\|Phase 6" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found phase exclusion specifications"
else
    fail_test "Missing phase exclusion specifications (excludes_from or Phase references)"
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
