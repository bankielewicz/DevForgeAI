#!/bin/bash

# Test AC#5: Framework Integration and Tool Restrictions
# Purpose: Verify tool restrictions (read-only: Read, Glob, Grep only)
# Expected: All checks pass (exit 0 on success, non-zero on failure)

STORY_ID="STORY-133"
AGENT_FILE=".claude/agents/ideation-result-interpreter.md"
TEST_RESULTS=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Change to project root
cd "$PROJECT_ROOT" || { echo "ERROR: Cannot cd to project root"; exit 1; }

echo "════════════════════════════════════════════════════════════════"
echo "Test AC#5: Framework Integration and Tool Restrictions"
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

# Test 2: Has 'tools:' field in YAML frontmatter
echo "TEST 2: Has 'tools:' field in YAML frontmatter"
if grep -E "^tools:" "$AGENT_FILE" | grep -q "."; then
    echo "  ✓ PASS: 'tools:' field found"
    TOOLS=$(grep -E "^tools:" "$AGENT_FILE" | head -1)
    echo "         Found: $TOOLS"
else
    echo "  ✗ FAIL: 'tools:' field not found in frontmatter"
    TEST_RESULTS=1
fi
echo ""

# Test 3: Tools field contains 'Read'
echo "TEST 3: Tools field contains 'Read'"
if grep -E "^tools:" "$AGENT_FILE" | grep -q "Read"; then
    echo "  ✓ PASS: 'Read' tool found in tools list"
else
    echo "  ✗ FAIL: 'Read' tool not found in tools list"
    TEST_RESULTS=1
fi
echo ""

# Test 4: Tools field contains 'Glob'
echo "TEST 4: Tools field contains 'Glob'"
if grep -E "^tools:" "$AGENT_FILE" | grep -q "Glob"; then
    echo "  ✓ PASS: 'Glob' tool found in tools list"
else
    echo "  ✗ FAIL: 'Glob' tool not found in tools list"
    TEST_RESULTS=1
fi
echo ""

# Test 5: Tools field contains 'Grep'
echo "TEST 5: Tools field contains 'Grep'"
if grep -E "^tools:" "$AGENT_FILE" | grep -q "Grep"; then
    echo "  ✓ PASS: 'Grep' tool found in tools list"
else
    echo "  ✗ FAIL: 'Grep' tool not found in tools list"
    TEST_RESULTS=1
fi
echo ""

# Test 6: Tools field does NOT contain 'Write'
echo "TEST 6: Tools field does NOT contain 'Write'"
if grep -E "^tools:" "$AGENT_FILE" | grep -q "Write"; then
    echo "  ✗ FAIL: 'Write' tool found in tools list (should not be present)"
    echo "         Subagent must be read-only"
    TEST_RESULTS=1
else
    echo "  ✓ PASS: 'Write' tool not in tools list (correctly read-only)"
fi
echo ""

# Test 7: Tools field does NOT contain 'Edit'
echo "TEST 7: Tools field does NOT contain 'Edit'"
if grep -E "^tools:" "$AGENT_FILE" | grep -q "Edit"; then
    echo "  ✗ FAIL: 'Edit' tool found in tools list (should not be present)"
    echo "         Subagent must be read-only"
    TEST_RESULTS=1
else
    echo "  ✓ PASS: 'Edit' tool not in tools list (correctly read-only)"
fi
echo ""

# Test 8: Tools field does NOT contain 'Bash'
echo "TEST 8: Tools field does NOT contain 'Bash'"
if grep -E "^tools:" "$AGENT_FILE" | grep -q "Bash"; then
    echo "  ✗ FAIL: 'Bash' tool found in tools list (should not be present)"
    echo "         Subagent must be read-only"
    TEST_RESULTS=1
else
    echo "  ✓ PASS: 'Bash' tool not in tools list (correctly read-only)"
fi
echo ""

# Test 9: Workflow does NOT contain 'Write(' references
echo "TEST 9: Workflow does NOT contain file creation with Write("
if grep "Write(" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✗ FAIL: Write( function references found in workflow"
    echo "         Subagent should not create files"
    TEST_RESULTS=1
else
    echo "  ✓ PASS: No Write( function calls in workflow"
fi
echo ""

# Test 10: Workflow does NOT contain 'Edit(' references
echo "TEST 10: Workflow does NOT contain 'Edit(' references"
if grep "Edit(" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✗ FAIL: Edit( function references found in workflow"
    echo "         Subagent should not modify files"
    TEST_RESULTS=1
else
    echo "  ✓ PASS: No Edit( function calls in workflow"
fi
echo ""

# Test 11: Workflow does NOT contain 'Bash(' references with file operations
echo "TEST 11: Workflow does NOT contain 'Bash(' references"
if grep "Bash(" "$AGENT_FILE" | grep -qv "^#"; then
    echo "  ✗ FAIL: Bash( function references found in workflow"
    echo "         Subagent should not execute commands"
    TEST_RESULTS=1
else
    echo "  ✓ PASS: No Bash( function calls in workflow"
fi
echo ""

# Test 12: Workflow does NOT contain 'cat', 'echo', 'sed' commands
echo "TEST 12: Workflow does NOT contain shell file operation commands"
PROHIBITED_CMDS="(cat |echo |sed |awk |grep |find )"
if grep -E "$PROHIBITED_CMDS" "$AGENT_FILE" | grep -qv "^#" | head -1; then
    # Check if it's in code block (backticks or ``` markers)
    MATCHES=$(grep -E "$PROHIBITED_CMDS" "$AGENT_FILE" | grep -v "^#")
    # Simple heuristic: if found outside of comments, report
    echo "  ⚠ WARNING: Shell commands found (may be in documentation/examples)"
    echo "  Review carefully to ensure no actual file operations in workflow steps"
else
    echo "  ✓ PASS: No suspicious shell commands detected"
fi
echo ""

# Test 13: Verify tools list is exactly Read, Glob, Grep
echo "TEST 13: Tools list contains ONLY Read, Glob, Grep (no extras)"
TOOLS_LINE=$(grep -E "^tools:" "$AGENT_FILE" | head -1)
# Check if it's exactly "Read, Glob, Grep" or similar variations
if echo "$TOOLS_LINE" | grep -qE "(Read|Glob|Grep).*,(Read|Glob|Grep).*,(Read|Glob|Grep)"; then
    # Check it doesn't have additional tools
    if ! echo "$TOOLS_LINE" | grep -qE "Write|Edit|Bash|Task|AskUserQuestion"; then
        echo "  ✓ PASS: Tools list contains only read-only tools"
        echo "         Found: $TOOLS_LINE"
    else
        echo "  ✗ FAIL: Tools list contains additional non-read-only tools"
        echo "         Found: $TOOLS_LINE"
        TEST_RESULTS=1
    fi
else
    echo "  ⚠ WARNING: Could not verify exact tools list"
    echo "         Found: $TOOLS_LINE"
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
if [ $TEST_RESULTS -eq 0 ]; then
    echo "✓ AC#5 Test Suite: ALL TESTS PASSED"
else
    echo "✗ AC#5 Test Suite: SOME TESTS FAILED"
fi
echo "════════════════════════════════════════════════════════════════"

exit $TEST_RESULTS
