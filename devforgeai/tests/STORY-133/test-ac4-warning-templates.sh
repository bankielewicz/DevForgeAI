#!/bin/bash

# Test AC#4: Display Template Generation for Warning Cases
# Purpose: Verify warning template includes all required sections
# Expected: All checks pass (exit 0 on success, non-zero on failure)

STORY_ID="STORY-133"
AGENT_FILE=".claude/agents/ideation-result-interpreter.md"
TEST_RESULTS=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Change to project root
cd "$PROJECT_ROOT" || { echo "ERROR: Cannot cd to project root"; exit 1; }

echo "════════════════════════════════════════════════════════════════"
echo "Test AC#4: Display Template Generation for Warning Cases"
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

# Test 3: Warning template mentioned
echo "TEST 3: Warning template mentioned"
if grep -E "warning.*template|Warning.*template|⚠️|incomplete.*template" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Warning template mentioned"
    MATCH=$(grep -E "warning.*template|Warning.*template|⚠️" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Warning template not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 4: Completion status display mentioned
echo "TEST 4: Completion status display mentioned"
if grep -E "completion.*status|Completion|progress.*percent|complete" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Completion status display mentioned"
    MATCH=$(grep -E "completion.*status|Completion|progress" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Completion status display not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 5: Quality warnings with severity levels mentioned
echo "TEST 5: Quality warnings with severity levels mentioned"
if grep -E "warning.*severity|severity.*level|Quality warning|incomplete.*section" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Quality warnings with severity mentioned"
    MATCH=$(grep -E "warning.*severity|Quality warning" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Quality warnings with severity not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 6: Incomplete sections highlighted mentioned
echo "TEST 6: Incomplete sections highlighted mentioned"
if grep -E "incomplete.*section|section.*highlight|highlight|missing|gap" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Incomplete sections highlighting mentioned"
    MATCH=$(grep -E "incomplete.*section|highlight" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Incomplete sections highlighting not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 7: Resolution path mentioned
echo "TEST 7: Resolution path mentioned"
if grep -E "resolution path|Resolution|resolve|fix" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Resolution path mentioned"
    MATCH=$(grep -E "resolution path|Resolution" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Resolution path not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 8: Recommendations mentioned
echo "TEST 8: Recommendations mentioned"
if grep -E "recommendation|recommend|recommend|suggest" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Recommendations mentioned"
    MATCH=$(grep -E "recommendation|recommend" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Recommendations not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 9: Resume ideation option mentioned
echo "TEST 9: Resume ideation option mentioned"
if grep -E "resume|Resume|/ideate|continue" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Resume ideation option mentioned"
    MATCH=$(grep -E "resume|Resume|/ideate" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Resume ideation option not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 10: Proceed despite gaps option mentioned
echo "TEST 10: Proceed despite gaps option mentioned"
if grep -E "proceed|Proceed|despite|continue.*gap" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Proceed despite gaps option mentioned"
    MATCH=$(grep -E "proceed|despite" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Proceed despite gaps option not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 11: Impact assessment mentioned
echo "TEST 11: Impact assessment mentioned"
if grep -E "impact|Impact|consequence|effect" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Impact assessment mentioned"
    MATCH=$(grep -E "impact|Impact" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Impact assessment not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 12: Missing information guidance mentioned
echo "TEST 12: Missing information guidance mentioned"
if grep -E "missing.*info|Missing|undefined|unclear|gap" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Missing information guidance mentioned"
    MATCH=$(grep -E "missing|Missing|undefined|gap" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Missing information guidance not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
if [ $TEST_RESULTS -eq 0 ]; then
    echo "✓ AC#4 Test Suite: ALL TESTS PASSED"
else
    echo "✗ AC#4 Test Suite: SOME TESTS FAILED"
fi
echo "════════════════════════════════════════════════════════════════"

exit $TEST_RESULTS
