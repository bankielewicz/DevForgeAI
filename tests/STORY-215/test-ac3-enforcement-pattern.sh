#!/bin/bash
# STORY-215 AC-3: Enforcement Pattern Documented
# Tests that the enforcement pattern with HALT and AskUserQuestion is documented
# Expected: FAIL initially (file not yet modified)

# Note: Not using set -e to allow all tests to run even when some fail

CLAUDE_MD="/mnt/c/Projects/DevForgeAI2/CLAUDE.md"
TEST_NAME="AC-3: Enforcement Pattern Documented"
PASS_COUNT=0
FAIL_COUNT=0

echo "=================================================="
echo "STORY-215 Test: $TEST_NAME"
echo "=================================================="

# Test 3.1: Verify "HALT before invoking skill" text exists
echo -n "Test 3.1: Contains 'HALT before invoking skill' text... "
if grep -q "HALT before invoking skill" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing text: 'HALT before invoking skill'"
    ((FAIL_COUNT++))
fi

# Test 3.2: Verify "AskUserQuestion" tool is mentioned
echo -n "Test 3.2: Contains 'AskUserQuestion' tool reference... "
if grep -q "AskUserQuestion" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing reference to 'AskUserQuestion' tool"
    ((FAIL_COUNT++))
fi

# Test 3.3: Verify enforcement instruction is in the checklist section
echo -n "Test 3.3: Enforcement instruction appears in checklist section... "
# Get line number of checklist section
CHECKLIST_LINE=$(grep -n "^### Pre-Skill Execution Checklist" "$CLAUDE_MD" | head -1 | cut -d: -f1)
if [ -n "$CHECKLIST_LINE" ]; then
    # Search for enforcement text after the checklist header
    ENFORCEMENT_LINE=$(grep -n "HALT before invoking skill" "$CLAUDE_MD" | head -1 | cut -d: -f1)
    if [ -n "$ENFORCEMENT_LINE" ] && [ "$ENFORCEMENT_LINE" -gt "$CHECKLIST_LINE" ]; then
        echo "PASS (Enforcement at line $ENFORCEMENT_LINE, after checklist at line $CHECKLIST_LINE)"
        ((PASS_COUNT++))
    else
        echo "FAIL - Enforcement text not found after checklist section"
        ((FAIL_COUNT++))
    fi
else
    echo "FAIL - Checklist section not found"
    ((FAIL_COUNT++))
fi

# Test 3.4: Verify "Enforcement:" label exists
echo -n "Test 3.4: Contains 'Enforcement:' label... "
if grep -q "^\*\*Enforcement:\*\*" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing '**Enforcement:**' label"
    ((FAIL_COUNT++))
fi

# Test 3.5: Verify "ask for clarification" is mentioned
echo -n "Test 3.5: Contains 'ask for clarification' text... "
if grep -q "ask for clarification" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing text: 'ask for clarification'"
    ((FAIL_COUNT++))
fi

echo ""
echo "=================================================="
echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "=================================================="

if [ $FAIL_COUNT -gt 0 ]; then
    echo "AC-3 FAILED: Enforcement pattern not properly documented in CLAUDE.md"
    exit 1
else
    echo "AC-3 PASSED: Enforcement pattern properly documented in CLAUDE.md"
    exit 0
fi
