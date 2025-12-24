#!/bin/bash

# Test AC#2: Ideation-Specific Output Parsing
# Purpose: Verify the subagent workflow includes parsing for ideation-specific metrics
# Expected: All checks pass (exit 0 on success, non-zero on failure)

STORY_ID="STORY-133"
AGENT_FILE=".claude/agents/ideation-result-interpreter.md"
TEST_RESULTS=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Change to project root
cd "$PROJECT_ROOT" || { echo "ERROR: Cannot cd to project root"; exit 1; }

echo "════════════════════════════════════════════════════════════════"
echo "Test AC#2: Ideation-Specific Output Parsing"
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

# Test 2: Workflow includes epic count extraction
echo "TEST 2: Workflow includes epic count extraction"
if grep -E "epic count|Epic count|epics identified|number of epics" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Epic count extraction mentioned in workflow"
    MATCH=$(grep -E "epic count|Epic count|epics identified|number of epics" "$AGENT_FILE" | grep -v "^#" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Epic count extraction not mentioned in workflow"
    echo "         Expected: Keywords like 'epic count', 'epics identified', etc."
    TEST_RESULTS=1
fi
echo ""

# Test 3: Workflow includes complexity score (0-60) extraction
echo "TEST 3: Workflow includes complexity score (0-60) extraction"
if grep -E "complexity|score|0-60|Complexity Score" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Complexity score extraction mentioned"
    MATCH=$(grep -E "complexity.*score|score.*complexity|0-60" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Complexity score extraction not mentioned"
    echo "         Expected: Keywords like 'complexity', 'score', '0-60', etc."
    TEST_RESULTS=1
fi
echo ""

# Test 4: Workflow includes architecture tier (1-4) extraction
echo "TEST 4: Workflow includes architecture tier (1-4) extraction"
if grep -E "architecture tier|Tier [1-4]|tier classification|tier level" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Architecture tier extraction mentioned"
    MATCH=$(grep -E "tier|Tier" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Architecture tier extraction not mentioned"
    echo "         Expected: Keywords like 'architecture tier', 'Tier 1', 'tier classification', etc."
    TEST_RESULTS=1
fi
echo ""

# Test 5: Workflow includes requirements summary parsing
echo "TEST 5: Workflow includes requirements summary parsing"
if grep -E "requirements summary|functional requirements|non-functional|NFR|integration.*count|integration points" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Requirements summary parsing mentioned"
    MATCH=$(grep -E "requirements|functional|NFR|integration" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Requirements summary parsing not mentioned"
    echo "         Expected: Keywords like 'requirements', 'functional', 'NFR', 'integration', etc."
    TEST_RESULTS=1
fi
echo ""

# Test 6: Workflow includes functional requirements extraction
echo "TEST 6: Workflow includes functional requirements extraction"
if grep -E "functional requirement|Functional requirement" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Functional requirements extraction mentioned"
    MATCH=$(grep -E "functional requirement" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Functional requirements not explicitly mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 7: Workflow includes non-functional requirements (NFR) extraction
echo "TEST 7: Workflow includes non-functional requirements extraction"
if grep -E "non-functional|NFR|performance|security|scalability" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Non-functional requirements extraction mentioned"
    MATCH=$(grep -E "non-functional|NFR" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Non-functional requirements not mentioned"
    echo "         Expected: Keywords like 'non-functional', 'NFR', etc."
    TEST_RESULTS=1
fi
echo ""

# Test 8: Workflow includes integration points extraction
echo "TEST 8: Workflow includes integration points extraction"
if grep -E "integration point|integration count|external.*integr|integr.*system" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Integration points extraction mentioned"
    MATCH=$(grep -E "integration" "$AGENT_FILE" | head -2 | tail -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Integration points extraction not mentioned"
    echo "         Expected: Keywords like 'integration points', 'external systems', etc."
    TEST_RESULTS=1
fi
echo ""

# Test 9: Workflow includes next-action guidance
echo "TEST 9: Workflow includes next-action guidance"
if grep -E "next.*action|next step|context-aware|command recommendation" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Next-action guidance mentioned"
    MATCH=$(grep -E "next.*action|next.*step|command" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Next-action guidance not mentioned"
    TEST_RESULTS=1
fi
echo ""

# Test 10: Workflow includes greenfield project guidance
echo "TEST 10: Workflow includes greenfield project guidance"
if grep -E "greenfield|/create-context" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Greenfield project guidance mentioned"
    MATCH=$(grep -E "greenfield|/create-context" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Greenfield project guidance not mentioned"
    echo "         Expected: Keywords like 'greenfield', '/create-context', etc."
    TEST_RESULTS=1
fi
echo ""

# Test 11: Workflow includes brownfield project guidance
echo "TEST 11: Workflow includes brownfield project guidance"
if grep -E "brownfield|/orchestrate" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✓ PASS: Brownfield project guidance mentioned"
    MATCH=$(grep -E "brownfield|/orchestrate" "$AGENT_FILE" | head -1)
    echo "         Found: $MATCH"
else
    echo "  ✗ FAIL: Brownfield project guidance not mentioned"
    echo "         Expected: Keywords like 'brownfield', '/orchestrate', etc."
    TEST_RESULTS=1
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
if [ $TEST_RESULTS -eq 0 ]; then
    echo "✓ AC#2 Test Suite: ALL TESTS PASSED"
else
    echo "✗ AC#2 Test Suite: SOME TESTS FAILED"
fi
echo "════════════════════════════════════════════════════════════════"

exit $TEST_RESULTS
