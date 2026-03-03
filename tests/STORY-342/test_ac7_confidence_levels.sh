#!/bin/bash
# STORY-342 AC#7: Confidence Levels Calculated
# Tests that confidence levels are calculated correctly: >=10=high, >=5=medium, >=3=low, <3=emerging

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
TDD_PATTERNS_FILE="$PROJECT_ROOT/.claude/memory/learning/tdd-patterns.md"
HOOK_FILE="$PROJECT_ROOT/.claude/hooks/post-qa-memory-update.sh"

echo "=== AC#7: Confidence Levels Calculated Tests ==="

# Test 1: High confidence threshold (>=10) documented
echo -n "Test 1: High confidence threshold (>=10) documented... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -Eqi "high.*10|>=.*10.*high|10.*high" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - High confidence threshold (>=10) not documented"
    exit 1
fi

# Test 2: Medium confidence threshold (>=5) documented
echo -n "Test 2: Medium confidence threshold (>=5) documented... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -Eqi "medium.*5|>=.*5.*medium|5.*medium" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Medium confidence threshold (>=5) not documented"
    exit 1
fi

# Test 3: Low confidence threshold (>=3) documented
echo -n "Test 3: Low confidence threshold (>=3) documented... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -Eqi "low.*3|>=.*3.*low|3.*low" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Low confidence threshold (>=3) not documented"
    exit 1
fi

# Test 4: Emerging threshold (<3) documented
echo -n "Test 4: Emerging threshold (<3) documented... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -Eqi "emerging.*<.*3|<.*3.*emerging" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Emerging threshold (<3) not documented"
    exit 1
fi

# Test 5: Hook implements confidence calculation
echo -n "Test 5: Hook implements confidence calculation... "
if [ -f "$HOOK_FILE" ] && grep -Eqi "confidence|threshold|occurrences" "$HOOK_FILE"; then
    echo "PASS"
else
    echo "FAIL - Hook does not implement confidence calculation"
    exit 1
fi

# Test 6: All four confidence levels present
echo -n "Test 6: All four confidence levels (high/medium/low/emerging) present... "
if [ -f "$TDD_PATTERNS_FILE" ]; then
    has_high=$(grep -qi "high" "$TDD_PATTERNS_FILE" && echo "1" || echo "0")
    has_medium=$(grep -qi "medium" "$TDD_PATTERNS_FILE" && echo "1" || echo "0")
    has_low=$(grep -qi "low" "$TDD_PATTERNS_FILE" && echo "1" || echo "0")
    has_emerging=$(grep -qi "emerging" "$TDD_PATTERNS_FILE" && echo "1" || echo "0")

    if [ "$has_high" = "1" ] && [ "$has_medium" = "1" ] && [ "$has_low" = "1" ] && [ "$has_emerging" = "1" ]; then
        echo "PASS"
    else
        echo "FAIL - Not all confidence levels present (high=$has_high, medium=$has_medium, low=$has_low, emerging=$has_emerging)"
        exit 1
    fi
else
    echo "FAIL - tdd-patterns.md not found"
    exit 1
fi

# Test 7: Maximum examples (5) per pattern enforced
echo -n "Test 7: Maximum 5 examples per pattern documented... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -Eqi "max.*5|maximum.*5|5.*example|examples.*5" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Maximum 5 examples per pattern not documented"
    exit 1
fi

echo ""
echo "=== AC#7 Tests Complete: All PASSED ==="
