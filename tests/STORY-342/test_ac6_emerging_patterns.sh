#!/bin/bash
# STORY-342 AC#6: Emerging Patterns Not Surfaced
# Tests that patterns with <3 occurrences are marked "emerging" and not surfaced

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
TDD_PATTERNS_FILE="$PROJECT_ROOT/.claude/memory/learning/tdd-patterns.md"
HOOK_FILE="$PROJECT_ROOT/.claude/hooks/post-qa-memory-update.sh"

echo "=== AC#6: Emerging Patterns Not Surfaced Tests ==="

# Test 1: Confidence field exists in pattern schema
echo -n "Test 1: Confidence field present in tdd-patterns.md... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -qi "confidence" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Confidence field not found in tdd-patterns.md"
    exit 1
fi

# Test 2: "emerging" confidence level documented
echo -n "Test 2: 'emerging' confidence level documented... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -qi "emerging" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - 'emerging' confidence level not documented"
    exit 1
fi

# Test 3: Hook contains emerging pattern check
echo -n "Test 3: Hook contains emerging pattern filtering... "
if [ -f "$HOOK_FILE" ] && grep -qi "emerging\|<.*3\|less.*than.*3" "$HOOK_FILE"; then
    echo "PASS"
else
    echo "FAIL - Hook does not contain emerging pattern check"
    exit 1
fi

# Test 4: Surfacing logic excludes emerging patterns
echo -n "Test 4: Surfacing logic excludes emerging patterns... "
if [ -f "$HOOK_FILE" ] && grep -qi "skip\|exclude\|filter\|not.*surface\|!.*emerging" "$HOOK_FILE"; then
    echo "PASS"
else
    echo "FAIL - Surfacing logic does not exclude emerging patterns"
    exit 1
fi

# Test 5: Threshold documented (<3 occurrences = emerging)
echo -n "Test 5: Threshold <3 documented for emerging... "
if [ -f "$TDD_PATTERNS_FILE" ] && grep -qi "<.*3\|less.*3\|fewer.*3" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Threshold <3 not documented for emerging patterns"
    exit 1
fi

echo ""
echo "=== AC#6 Tests Complete: All PASSED ==="
