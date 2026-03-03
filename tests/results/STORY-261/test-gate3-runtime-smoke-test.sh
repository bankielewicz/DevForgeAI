#!/bin/bash
# STORY-261: Test Suite for Gate 3 Runtime Executable Criteria
# Test Type: Test Specification (Markdown validation)
# Expected Result: ALL TESTS FAIL with current file state
# TDD Phase: RED (failing tests before implementation)

# Note: set -e removed to allow all tests to run and report

FILE="/mnt/c/Projects/DevForgeAI2/.claude/rules/core/quality-gates.md"
SKILL_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/SKILL.md"

echo "=========================================="
echo "STORY-261: Gate 3 Runtime Smoke Test Tests"
echo "=========================================="

PASS=0
FAIL=0

# -------------------------------------------
# AC#1: Gate 3 Criteria Updated
# -------------------------------------------

echo ""
echo "### AC#1: Gate 3 Criteria Contains 'runtime smoke test'"

# Test 1.1: Gate 3 section contains "runtime smoke test"
echo -n "Test 1.1: Gate 3 mentions 'runtime smoke test'... "
if grep -q "runtime smoke test" "$FILE"; then
    echo "PASS"
    ((PASS++))
else
    echo "FAIL (expected: 'runtime smoke test' in Gate 3 section)"
    ((FAIL++))
fi

# Test 1.2: Runtime smoke test is in Requirements list
echo -n "Test 1.2: Runtime smoke test in Gate 3 Requirements list... "
if sed -n '/## Gate 3: QA Approval/,/## Gate 4/p' "$FILE" | grep -q "runtime smoke test"; then
    echo "PASS"
    ((PASS++))
else
    echo "FAIL (expected: runtime smoke test under Gate 3 Requirements)"
    ((FAIL++))
fi

# -------------------------------------------
# AC#2: Documentation Consistency
# -------------------------------------------

echo ""
echo "### AC#2: Consistency with QA SKILL.md Phase 1"

# Test 2.1: Gate 3 aligns with actual QA validation steps
echo -n "Test 2.1: Gate 3 criteria matches QA Phase 1 validation... "
# QA SKILL.md Phase 1 includes test coverage analysis (Step 1.2)
# Gate 3 should reference this validation
if sed -n '/## Gate 3: QA Approval/,/## Gate 4/p' "$FILE" | grep -qiE "(coverage|test.*pass|runtime)"; then
    echo "PASS"
    ((PASS++))
else
    echo "FAIL (expected: Gate 3 to reference coverage/test validation per SKILL.md)"
    ((FAIL++))
fi

# Test 2.2: Gate 3 references executable verification
echo -n "Test 2.2: Gate 3 references executable verification... "
if sed -n '/## Gate 3: QA Approval/,/## Gate 4/p' "$FILE" | grep -qiE "(executable|runtime|smoke)"; then
    echo "PASS"
    ((PASS++))
else
    echo "FAIL (expected: executable/runtime/smoke reference in Gate 3)"
    ((FAIL++))
fi

# -------------------------------------------
# AC#3: RCA Reference Added
# -------------------------------------------

echo ""
echo "### AC#3: RCA-002 Reference Present"

# Test 3.1: RCA-002 referenced in Gate 3 section
echo -n "Test 3.1: Gate 3 section references RCA-002... "
if sed -n '/## Gate 3: QA Approval/,/## Gate 4/p' "$FILE" | grep -q "RCA-002"; then
    echo "PASS"
    ((PASS++))
else
    echo "FAIL (expected: RCA-002 reference in Gate 3 section)"
    ((FAIL++))
fi

# Test 3.2: RCA reference exists anywhere in file (fallback)
echo -n "Test 3.2: RCA-002 referenced in quality-gates.md... "
if grep -q "RCA-002" "$FILE"; then
    echo "PASS"
    ((PASS++))
else
    echo "FAIL (expected: RCA-002 annotation in file)"
    ((FAIL++))
fi

# -------------------------------------------
# Summary
# -------------------------------------------

echo ""
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo "Total:  $((PASS + FAIL))"
echo ""

if [ $FAIL -gt 0 ]; then
    echo "STATUS: RED (TDD Phase - Tests failing as expected)"
    exit 1
else
    echo "STATUS: GREEN (All tests passing)"
    exit 0
fi
