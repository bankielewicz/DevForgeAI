#!/bin/bash

# Test AC#3: Display Template Generation for Success Cases
# Purpose: Verify success template includes all required sections
# Expected: All checks pass (exit 0 on success, non-zero on failure)

STORY_ID="STORY-133"
AGENT_FILE=".claude/agents/ideation-result-interpreter.md"
TEST_RESULTS=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Change to project root
cd "$PROJECT_ROOT" || { echo "ERROR: Cannot cd to project root"; exit 1; }

echo "════════════════════════════════════════════════════════════════"
echo "Test AC#3: Display Template Generation for Success Cases"
echo "Story: $STORY_ID"
echo "Testing: $AGENT_FILE"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Test 1: File exists (prerequisite)
echo "TEST 1: File exists (prerequisite)"
if [ -f "$AGENT_FILE" ]; then
    echo "  ✓ PASS: File found"
else
    echo "  ✗ FAIL: File not found at $AGENT_FILE"
    echo "         Cannot proceed with remaining tests"
    exit 1
fi
echo ""

# Test 2: Templates section exists
echo "TEST 2: Templates section exists"
if grep -E "^# Templates|^## Templates" "$AGENT_FILE" | grep -q "."; then
    echo "  ✓ PASS: Templates section found"
else
    echo "  ✗ FAIL: Templates section not found"
    TEST_RESULTS=1
fi
echo ""

# Test 3: Success template header mentioned
echo "TEST 3: Success template header mentioned"
if grep -E "success.*template|Success.*template|✅|PASS.*template|complete.*template" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Success template mentioned"
    MATCH=$(grep -E "success.*template|Success.*template|✅" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Success template not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 4: Header with epic count mentioned
echo "TEST 4: Header with epic count mentioned"
if grep -E "epic.*count|count.*epic|Identified.*epic|number of epic" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Epic count in header mentioned"
    MATCH=$(grep -E "epic.*count|Identified.*epic" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Epic count in header not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 5: Header with complexity score mentioned
echo "TEST 5: Header with complexity score mentioned"
if grep -E "complexity.*score|score.*complexity|Complexity Score" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Complexity score in header mentioned"
    MATCH=$(grep -E "complexity.*score|Complexity Score" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Complexity score in header not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 6: Architecture tier classification section mentioned
echo "TEST 6: Architecture tier classification section mentioned"
if grep -E "architecture.*tier|Tier.*classification|tier.*level|Architecture Tier" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Architecture tier classification mentioned"
    MATCH=$(grep -E "architecture.*tier|Architecture Tier" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Architecture tier classification not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 7: Requirements breakdown section mentioned
echo "TEST 7: Requirements breakdown section mentioned"
if grep -E "requirements.*breakdown|Breakdown|functional.*count|NFR.*count" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Requirements breakdown section mentioned"
    MATCH=$(grep -E "requirements.*breakdown|Breakdown" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Requirements breakdown section not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 8: Key design decisions section mentioned
echo "TEST 8: Key design decisions section mentioned"
if grep -E "design decision|Design Decision|key design|technology decision" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Key design decisions section mentioned"
    MATCH=$(grep -E "design decision|Design Decision" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Key design decisions section not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 9: Recommended next command mentioned
echo "TEST 9: Recommended next command mentioned"
if grep -E "next command|recommended command|Next Step|recommended next" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Recommended next command mentioned"
    MATCH=$(grep -E "next command|recommended" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Recommended next command not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 10: Functional requirements breakdown mentioned
echo "TEST 10: Functional requirements breakdown mentioned"
if grep -E "functional.*count|functional.*requirement|F.*functional" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Functional requirements breakdown mentioned"
    MATCH=$(grep -E "functional.*count|functional.*requirement" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Functional requirements breakdown not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 11: Non-functional requirements breakdown mentioned
echo "TEST 11: Non-functional requirements breakdown mentioned"
if grep -E "non-functional|NFR.*count|N.*non-functional" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Non-functional requirements breakdown mentioned"
    MATCH=$(grep -E "non-functional|NFR" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Non-functional requirements breakdown not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 12: Integration points breakdown mentioned
echo "TEST 12: Integration points breakdown mentioned"
if grep -E "integration.*count|integration.*point|I.*integration" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Integration points breakdown mentioned"
    MATCH=$(grep -E "integration.*count|integration.*point" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Integration points breakdown not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
if [ $TEST_RESULTS -eq 0 ]; then
    echo "✓ AC#3 Test Suite: ALL TESTS PASSED"
else
    echo "✗ AC#3 Test Suite: SOME TESTS FAILED"
fi
echo "════════════════════════════════════════════════════════════════"

exit $TEST_RESULTS
