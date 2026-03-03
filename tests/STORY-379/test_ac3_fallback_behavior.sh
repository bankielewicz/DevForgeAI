#!/bin/bash
# STORY-379 AC#3: Fallback Behavior Documentation with Decision Flowchart
# Tests verify the fallback behavior section contains:
#   - Three fallback triggers (binary not found, unsupported extension, non-zero exit code)
#   - Grep as fallback target
#   - Step-by-step decision flow
#   - Automatic/transparent fallback statement
#   - STORY-362 reference
#
# TDD Red Phase: All tests MUST FAIL because docs/guides/treelint-integration-guide.md does not exist yet.

set -e

GUIDE="/mnt/c/Projects/DevForgeAI2/docs/guides/treelint-integration-guide.md"

echo "=== AC#3: Fallback Behavior Documentation with Decision Flowchart ==="

# Test 1: Guide file exists
echo -n "Test 1: Guide file exists... "
if [ -f "$GUIDE" ]; then
    echo "PASS"
else
    echo "FAIL - File does not exist"
    exit 1
fi

# Test 2: Fallback behavior section header exists
echo -n "Test 2: Fallback behavior section header exists... "
if grep -qi "Fallback" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Fallback section header not found"
    exit 1
fi

# Test 3: Trigger - binary not found documented
echo -n "Test 3: Trigger - binary not found documented... "
if grep -qi "binary not found\|not found\|not installed\|command not found" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Binary not found trigger not documented"
    exit 1
fi

# Test 4: Trigger - unsupported file extension documented
echo -n "Test 4: Trigger - unsupported file extension documented... "
if grep -qi "unsupported.*extension\|unsupported.*file\|unsupported.*language\|file.*not supported" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Unsupported file extension trigger not documented"
    exit 1
fi

# Test 5: Trigger - non-zero exit code documented
echo -n "Test 5: Trigger - non-zero exit code documented... "
if grep -qi "non-zero\|exit code\|error code\|command fails" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Non-zero exit code trigger not documented"
    exit 1
fi

# Test 6: Grep identified as fallback target
echo -n "Test 6: Grep identified as fallback target... "
if grep -qi "Grep" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Grep as fallback target not documented"
    exit 1
fi

# Test 7: Decision flow documented (step-by-step)
echo -n "Test 7: Decision flow documented... "
if grep -qi "check.*binary\|step.*1\|decision.*flow\|flowchart\|decision tree" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Decision flow not documented"
    exit 1
fi

# Test 8: Automatic/transparent fallback statement
echo -n "Test 8: Automatic and transparent fallback stated... "
if grep -qi "automatic\|transparent\|seamless" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Automatic/transparent fallback statement not found"
    exit 1
fi

# Test 9: STORY-362 referenced
echo -n "Test 9: STORY-362 referenced... "
if grep -q "STORY-362" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - STORY-362 reference not found"
    exit 1
fi

echo ""
echo "=== AC#3 All Tests Passed ==="
exit 0
