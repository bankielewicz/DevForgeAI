#!/bin/bash
###############################################################################
# Test Suite: STORY-176 - AC#3: Skill Files Excluded from Code Smell Detection
# Purpose: Verify files matching .claude/skills/**/*.md are skipped in Phase 5
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

echo "STORY-176 AC#3: Skill Files Excluded from Code Smell Detection"
echo "Target: $SCANNER_FILE"

if [ ! -f "$SCANNER_FILE" ]; then
    echo ""
    echo "ERROR: Scanner file does not exist: $SCANNER_FILE"
    exit 1
fi

header "AC#3: Phase 5 Skill File Exclusion"

test_case "Phase 5 section exists"
if grep -q "^### Phase 5:" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Found Phase 5 section"
else
    fail_test "Missing Phase 5 section header"
fi

test_case "Phase 5 is Code Smells Scanning"
# Verify Phase 5 is Category 4 - Code Smells
if grep -q "Phase 5.*Code Smells\|Phase 5:.*Category 4" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Phase 5 is Code Smells Scanning (Category 4)"
else
    fail_test "Phase 5 does not identify as Code Smells Scanning"
fi

test_case "Phase 5 mentions skill file exclusion"
# Extract Phase 5 section content
phase5_content=$(sed -n '/^### Phase 5:/,/^### Phase [6-9]/p' "$SCANNER_FILE" 2>/dev/null || echo "")

if echo "$phase5_content" | grep -qi "skip\|exclude\|ignore" 2>/dev/null && \
   echo "$phase5_content" | grep -qi "skill" 2>/dev/null; then
    pass_test "Phase 5 mentions skipping/excluding skill files"
else
    fail_test "Phase 5 does not mention skipping skill files"
fi

test_case "Phase 5 references .claude/skills pattern"
if echo "$phase5_content" | grep -q '\.claude/skills' 2>/dev/null; then
    pass_test "Phase 5 references .claude/skills pattern"
else
    fail_test "Phase 5 does not reference .claude/skills pattern"
fi

test_case "Agents (.claude/agents/*.md) also excluded from Phase 5"
if echo "$phase5_content" | grep -q '\.claude/agents' 2>/dev/null || \
   grep -q '\.claude/agents.*Phase 5\|Phase 5.*\.claude/agents' "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Agents also excluded from Phase 5"
else
    fail_test "Agents not explicitly excluded from Phase 5"
fi

test_case "Exclusion rationale documented (Markdown files are specifications, not code)"
if grep -qi "specification\|markdown.*not.*code\|documentation.*not.*executable" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Exclusion rationale documented"
else
    fail_test "No rationale for why Markdown files are excluded from code smell detection"
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
