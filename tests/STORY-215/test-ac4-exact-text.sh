#!/bin/bash
# STORY-215 AC-4: Exact Text Added Per RCA-021
# Tests that the exact text from RCA-021 REC-1 specification is present
# Expected: FAIL initially (file not yet modified)

# Note: Not using set -e to allow all tests to run even when some fail

CLAUDE_MD="/mnt/c/Projects/DevForgeAI2/CLAUDE.md"
TEST_NAME="AC-4: Exact Text Added Per RCA-021"
PASS_COUNT=0
FAIL_COUNT=0

echo "=================================================="
echo "STORY-215 Test: $TEST_NAME"
echo "=================================================="

# Test 4.1: Exact header text
echo -n "Test 4.1: Exact header '### Pre-Skill Execution Checklist'... "
if grep -q "^### Pre-Skill Execution Checklist$" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact header: '### Pre-Skill Execution Checklist'"
    ((FAIL_COUNT++))
fi

# Test 4.2: Exact instruction text
echo -n "Test 4.2: Exact instruction 'Before invoking ANY skill with Skill(command=\"...\"), verify:'... "
if grep -qF '**Before invoking ANY skill with Skill(command="..."), verify:**' "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact instruction text"
    ((FAIL_COUNT++))
fi

# Test 4.3: Verification point 1 exact text - "ALL phases must execute in sequence"
echo -n "Test 4.3: Contains 'ALL phases must execute in sequence (not optional)'... "
if grep -qF "ALL phases must execute in sequence (not optional)" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact text: 'ALL phases must execute in sequence (not optional)'"
    ((FAIL_COUNT++))
fi

# Test 4.4: Verification point 2 exact text - "Load reference files in Phase 0 BEFORE Phase 1"
echo -n "Test 4.4: Contains 'Load reference files in Phase 0 BEFORE Phase 1'... "
if grep -qF "Load reference files in Phase 0 BEFORE Phase 1" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact text: 'Load reference files in Phase 0 BEFORE Phase 1'"
    ((FAIL_COUNT++))
fi

# Test 4.5: Verification point 3 exact text - "HALT if previous phase not verified complete"
echo -n "Test 4.5: Contains 'HALT if previous phase not verified complete'... "
if grep -qF "HALT if previous phase not verified complete" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact text: 'HALT if previous phase not verified complete'"
    ((FAIL_COUNT++))
fi

# Test 4.6: Verification point 4 exact text - "run all steps systematically"
echo -n "Test 4.6: Contains 'you run all steps systematically'... "
if grep -qF "you run all steps systematically" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact text: 'you run all steps systematically'"
    ((FAIL_COUNT++))
fi

# Test 4.7: Verification point 5 exact text - "Deep mode Execute all documented phases completely"
echo -n "Test 4.7: Contains 'Deep mode' and 'Execute all documented phases completely'... "
if grep -q "Deep mode" "$CLAUDE_MD" && grep -qF "Execute all documented phases completely" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact text for deep mode execution"
    ((FAIL_COUNT++))
fi

# Test 4.8: Exact enforcement text
echo -n "Test 4.8: Exact enforcement 'If any checklist item is unclear, HALT before invoking skill'... "
if grep -qF "If any checklist item is unclear, HALT before invoking skill" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing exact enforcement text"
    ((FAIL_COUNT++))
fi

echo ""
echo "=================================================="
echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "=================================================="

if [ $FAIL_COUNT -gt 0 ]; then
    echo "AC-4 FAILED: Exact text from RCA-021 REC-1 not present in CLAUDE.md"
    exit 1
else
    echo "AC-4 PASSED: Exact text from RCA-021 REC-1 present in CLAUDE.md"
    exit 0
fi
