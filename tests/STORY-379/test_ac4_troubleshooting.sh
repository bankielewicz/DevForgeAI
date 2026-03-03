#!/bin/bash
# STORY-379 AC#4: Troubleshooting Guide with Minimum 5 Common Issues
# Tests verify the troubleshooting section contains:
#   - Minimum 5 structured issues
#   - Each issue has: symptom, cause, diagnostic command, resolution
#   - Required issues: binary not found, unsupported language, daemon not running,
#     stale index, permission denied
#
# TDD Red Phase: All tests MUST FAIL because docs/guides/treelint-integration-guide.md does not exist yet.

set -e

GUIDE="/mnt/c/Projects/DevForgeAI2/docs/guides/treelint-integration-guide.md"

echo "=== AC#4: Troubleshooting Guide with Minimum 5 Common Issues ==="

# Test 1: Guide file exists
echo -n "Test 1: Guide file exists... "
if [ -f "$GUIDE" ]; then
    echo "PASS"
else
    echo "FAIL - File does not exist"
    exit 1
fi

# Test 2: Troubleshooting section header exists
echo -n "Test 2: Troubleshooting section header exists... "
if grep -qi "## Troubleshooting\|## Common Issues\|## Troubleshooting Guide" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Troubleshooting section header not found"
    exit 1
fi

# Test 3: Issue - Treelint binary not found
echo -n "Test 3: Issue documented - Treelint binary not found... "
if grep -qi "binary not found\|command not found\|not installed" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Binary not found issue not documented"
    exit 1
fi

# Test 4: Issue - Unsupported language fallback
echo -n "Test 4: Issue documented - Unsupported language... "
if grep -qi "unsupported language\|unsupported file\|language not supported" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Unsupported language issue not documented"
    exit 1
fi

# Test 5: Issue - Daemon not running
echo -n "Test 5: Issue documented - Daemon not running... "
if grep -qi "daemon not running\|daemon.*not.*running\|daemon.*stopped\|daemon.*down" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Daemon not running issue not documented"
    exit 1
fi

# Test 6: Issue - Stale index results
echo -n "Test 6: Issue documented - Stale index results... "
if grep -qi "stale.*index\|outdated.*index\|index.*stale\|index.*outdated\|stale.*result" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Stale index issue not documented"
    exit 1
fi

# Test 7: Issue - Permission denied on binary
echo -n "Test 7: Issue documented - Permission denied... "
if grep -qi "permission denied\|permission.*error\|chmod" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Permission denied issue not documented"
    exit 1
fi

# Test 8: Structured fields - Symptom present
echo -n "Test 8: Structured field 'Symptom' present... "
if grep -qi "symptom\|symptoms\|error message\|you see\|appears" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Symptom field not found in troubleshooting entries"
    exit 1
fi

# Test 9: Structured fields - Cause present
echo -n "Test 9: Structured field 'Cause' present... "
if grep -qi "cause\|reason\|why\|because" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Cause field not found in troubleshooting entries"
    exit 1
fi

# Test 10: Structured fields - Diagnostic command present
echo -n "Test 10: Structured field 'Diagnostic' present... "
if grep -qi "diagnostic\|diagnose\|check\|verify\|debug" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Diagnostic field not found in troubleshooting entries"
    exit 1
fi

# Test 11: Structured fields - Resolution present
echo -n "Test 11: Structured field 'Resolution' present... "
if grep -qi "resolution\|solution\|fix\|resolve" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Resolution field not found in troubleshooting entries"
    exit 1
fi

# Test 12: At least 5 distinct issue entries (count issue headers)
echo -n "Test 12: At least 5 troubleshooting issue entries... "
ISSUE_COUNT=$(grep -ci "###.*\(issue\|problem\|error\|binary not found\|unsupported\|daemon\|stale\|permission\)" "$GUIDE" 2>/dev/null || echo "0")
if [ "$ISSUE_COUNT" -ge 5 ]; then
    echo "PASS ($ISSUE_COUNT entries found)"
else
    echo "FAIL - Only $ISSUE_COUNT issue entries found (need at least 5)"
    exit 1
fi

echo ""
echo "=== AC#4 All Tests Passed ==="
exit 0
