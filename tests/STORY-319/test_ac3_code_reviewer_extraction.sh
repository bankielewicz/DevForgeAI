#!/bin/bash
# STORY-319 AC#3: Code-Reviewer Extraction Rules
# Tests that extraction rules for code-reviewer output are documented
# Expected: FAIL (file does not exist yet - TDD Red phase)

set -e

SOURCE_FILE="src/claude/agents/observation-extractor.md"

echo "=== AC#3: Code-Reviewer Extraction Rules Tests ==="

# Pre-check: File must exist
if [ ! -f "$SOURCE_FILE" ]; then
    echo "FAIL: Source file does not exist: $SOURCE_FILE"
    exit 1
fi

# Test 3.1: Extraction rule for high severity issues exists
echo -n "Test 3.1: Extraction rule for high severity issues documented... "
if grep -qi "severity.*high\|high.*severity" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to high severity issue extraction"
    exit 1
fi

# Test 3.2: High severity maps to category "friction"
echo -n "Test 3.2: High severity issues map to category 'friction'... "
# Look for high severity and friction in proximity
if grep -A10 -B10 -i "high" "$SOURCE_FILE" | grep -qi "friction"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: High severity issues to map to category 'friction'"
    exit 1
fi

# Test 3.3: Extraction rule for medium severity issues exists
echo -n "Test 3.3: Extraction rule for medium severity issues documented... "
if grep -qi "severity.*medium\|medium.*severity" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to medium severity issue extraction"
    exit 1
fi

# Test 3.4: Medium severity maps to category "warning"
echo -n "Test 3.4: Medium severity issues map to category 'warning'... "
if grep -A10 -B10 -i "medium" "$SOURCE_FILE" | grep -qi "warning"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Medium severity issues to map to category 'warning'"
    exit 1
fi

# Test 3.5: code-reviewer is mentioned as source subagent
echo -n "Test 3.5: code-reviewer mentioned as source subagent... "
if grep -qi "code-reviewer" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'code-reviewer' subagent"
    exit 1
fi

# Test 3.6: issues[] field mentioned
echo -n "Test 3.6: issues[] field mentioned in extraction rules... "
if grep -q "issues" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'issues' field in extraction rules"
    exit 1
fi

echo ""
echo "=== AC#3: All tests passed ==="
exit 0
