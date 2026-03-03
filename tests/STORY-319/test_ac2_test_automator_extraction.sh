#!/bin/bash
# STORY-319 AC#2: Test-Automator Extraction Rules
# Tests that extraction rules for test-automator output are documented
# Expected: FAIL (file does not exist yet - TDD Red phase)

set -e

SOURCE_FILE="src/claude/agents/observation-extractor.md"

echo "=== AC#2: Test-Automator Extraction Rules Tests ==="

# Pre-check: File must exist
if [ ! -f "$SOURCE_FILE" ]; then
    echo "FAIL: Source file does not exist: $SOURCE_FILE"
    exit 1
fi

# Test 2.1: Extraction rule for coverage_result.gaps[] exists
echo -n "Test 2.1: Extraction rule for 'coverage_result.gaps' documented... "
if grep -q "coverage_result\.gaps" "$SOURCE_FILE" || grep -q "coverage_result.gaps" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'coverage_result.gaps' extraction rule"
    exit 1
fi

# Test 2.2: coverage_result.gaps maps to category "gap"
echo -n "Test 2.2: coverage_result.gaps maps to category 'gap'... "
if grep -A5 -B5 "coverage_result" "$SOURCE_FILE" | grep -qi "gap"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: coverage_result.gaps to map to category 'gap'"
    exit 1
fi

# Test 2.3: Extraction rule for test_failures[] exists
echo -n "Test 2.3: Extraction rule for 'test_failures' documented... "
if grep -q "test_failures" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'test_failures' extraction rule"
    exit 1
fi

# Test 2.4: test_failures maps to category "friction"
echo -n "Test 2.4: test_failures maps to category 'friction'... "
if grep -A5 -B5 "test_failures" "$SOURCE_FILE" | grep -qi "friction"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: test_failures to map to category 'friction'"
    exit 1
fi

# Test 2.5: test-automator is mentioned as source subagent
echo -n "Test 2.5: test-automator mentioned as source subagent... "
if grep -qi "test-automator" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'test-automator' subagent"
    exit 1
fi

echo ""
echo "=== AC#2: All tests passed ==="
exit 0
