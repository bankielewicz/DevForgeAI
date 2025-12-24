#!/bin/bash

# Test AC#1: Subagent Structure and Initialization
# Purpose: Verify the ideation-result-interpreter subagent file exists with proper structure
# Expected: All checks pass (exit 0 on success, non-zero on failure)

STORY_ID="STORY-133"
AGENT_FILE=".claude/agents/ideation-result-interpreter.md"
TEST_RESULTS=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Change to project root
cd "$PROJECT_ROOT" || { echo "ERROR: Cannot cd to project root"; exit 1; }

echo "════════════════════════════════════════════════════════════════"
echo "Test AC#1: Subagent Structure and Initialization"
echo "Story: $STORY_ID"
echo "Testing: $AGENT_FILE"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Test 1: File exists
echo "TEST 1: File exists at $AGENT_FILE"
if [ -f "$AGENT_FILE" ]; then
    echo "  ✓ PASS: File found at $AGENT_FILE"
else
    echo "  ✗ FAIL: File not found at $AGENT_FILE"
    echo "         Expected location: $(pwd)/$AGENT_FILE"
    TEST_RESULTS=1
fi
echo ""

# Test 2: YAML frontmatter exists (between --- markers)
echo "TEST 2: YAML frontmatter exists (between --- markers)"
if [ -f "$AGENT_FILE" ]; then
    if head -1 "$AGENT_FILE" | grep -q "^---$"; then
        echo "  ✓ PASS: File starts with YAML frontmatter marker (---)"
    else
        echo "  ✗ FAIL: File does not start with YAML frontmatter marker"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test frontmatter"
fi
echo ""

# Test 3: Has 'name:' field in frontmatter
echo "TEST 3: Has 'name:' field in frontmatter"
if [ -f "$AGENT_FILE" ]; then
    if grep -E "^name:" "$AGENT_FILE" | head -5 | grep -q "ideation-result-interpreter"; then
        echo "  ✓ PASS: 'name:' field found with value 'ideation-result-interpreter'"
    else
        echo "  ✗ FAIL: 'name:' field not found or incorrect value"
        echo "         Expected: name: ideation-result-interpreter"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test name field"
fi
echo ""

# Test 4: Has 'description:' field in frontmatter
echo "TEST 4: Has 'description:' field in frontmatter"
if [ -f "$AGENT_FILE" ]; then
    if grep -E "^description:" "$AGENT_FILE" | head -5 | grep -q "."; then
        echo "  ✓ PASS: 'description:' field found"
        DESCRIPTION=$(grep -E "^description:" "$AGENT_FILE" | head -1 | sed 's/description: //')
        echo "         Value: $DESCRIPTION"
    else
        echo "  ✗ FAIL: 'description:' field not found or empty"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test description field"
fi
echo ""

# Test 5: Has 'tools:' field in frontmatter
echo "TEST 5: Has 'tools:' field in frontmatter"
if [ -f "$AGENT_FILE" ]; then
    if grep -E "^tools:" "$AGENT_FILE" | head -5 | grep -q "."; then
        echo "  ✓ PASS: 'tools:' field found"
        TOOLS=$(grep -E "^tools:" "$AGENT_FILE" | head -1 | sed 's/tools: //')
        echo "         Value: $TOOLS"
    else
        echo "  ✗ FAIL: 'tools:' field not found or empty"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test tools field"
fi
echo ""

# Test 6: Has 'model:' field in frontmatter
echo "TEST 6: Has 'model:' field in frontmatter"
if [ -f "$AGENT_FILE" ]; then
    if grep -E "^model:" "$AGENT_FILE" | head -5 | grep -q "."; then
        echo "  ✓ PASS: 'model:' field found"
        MODEL=$(grep -E "^model:" "$AGENT_FILE" | head -1 | sed 's/model: //')
        echo "         Value: $MODEL"
    else
        echo "  ✗ FAIL: 'model:' field not found or empty"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test model field"
fi
echo ""

# Test 7: Frontmatter closes with --- marker
echo "TEST 7: Frontmatter closes with --- marker"
if [ -f "$AGENT_FILE" ]; then
    # Find first 10 lines, check for closing --- after first line
    if head -20 "$AGENT_FILE" | tail -n +2 | grep -q "^---$"; then
        echo "  ✓ PASS: Frontmatter closing marker found"
    else
        echo "  ✗ FAIL: Frontmatter closing marker (---) not found"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test frontmatter closure"
fi
echo ""

# Test 8: Contains '# Purpose' section
echo "TEST 8: Contains '# Purpose' section"
if [ -f "$AGENT_FILE" ]; then
    if grep -q "^# Purpose" "$AGENT_FILE"; then
        echo "  ✓ PASS: '# Purpose' section found"
    else
        echo "  ✗ FAIL: '# Purpose' section not found"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test Purpose section"
fi
echo ""

# Test 9: Contains '# When Invoked' section
echo "TEST 9: Contains '# When Invoked' section"
if [ -f "$AGENT_FILE" ]; then
    if grep -q "^# When Invoked" "$AGENT_FILE"; then
        echo "  ✓ PASS: '# When Invoked' section found"
    else
        echo "  ✗ FAIL: '# When Invoked' section not found"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test When Invoked section"
fi
echo ""

# Test 10: Contains '# Workflow' section
echo "TEST 10: Contains '# Workflow' section"
if [ -f "$AGENT_FILE" ]; then
    if grep -q "^# Workflow" "$AGENT_FILE"; then
        echo "  ✓ PASS: '# Workflow' section found"
    else
        echo "  ✗ FAIL: '# Workflow' section not found"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test Workflow section"
fi
echo ""

# Test 11: Contains '# Templates' or '## Templates' section
echo "TEST 11: Contains '# Templates' section"
if [ -f "$AGENT_FILE" ]; then
    if grep -E "^#+ Templates" "$AGENT_FILE" | grep -q "."; then
        echo "  ✓ PASS: Templates section found"
    else
        echo "  ✗ FAIL: Templates section not found"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test Templates section"
fi
echo ""

# Test 12: Contains '# Error Handling' section
echo "TEST 12: Contains '# Error Handling' section"
if [ -f "$AGENT_FILE" ]; then
    if grep -q "^# Error Handling" "$AGENT_FILE"; then
        echo "  ✓ PASS: '# Error Handling' section found"
    else
        echo "  ✗ FAIL: '# Error Handling' section not found"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test Error Handling section"
fi
echo ""

# Test 13: Contains '# Related Subagents' section
echo "TEST 13: Contains '# Related Subagents' section"
if [ -f "$AGENT_FILE" ]; then
    if grep -E "^# Related Subagents|^## Related" "$AGENT_FILE" | grep -q "."; then
        echo "  ✓ PASS: Related Subagents section found"
    else
        echo "  ✗ FAIL: Related Subagents section not found"
        TEST_RESULTS=1
    fi
else
    echo "  ⊘ SKIP: File not found, cannot test Related Subagents section"
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
if [ $TEST_RESULTS -eq 0 ]; then
    echo "✓ AC#1 Test Suite: ALL TESTS PASSED"
else
    echo "✗ AC#1 Test Suite: SOME TESTS FAILED"
fi
echo "════════════════════════════════════════════════════════════════"

exit $TEST_RESULTS
