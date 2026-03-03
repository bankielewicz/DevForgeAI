#!/bin/bash
# STORY-348 AC#5: Story Template Updated with Advisory Fields
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

TEMPLATE="$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md"

echo "=== AC#5: Story Template Advisory Fields Tests ==="
echo "Target file: $TEMPLATE"

FAILURES=0

# Test 5.1: Template version updated to 2.8
echo -n "Test 5.1: Template version is 2.8... "
if grep -qE "template_version.*2\.8|version.*2\.8" "$TEMPLATE" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - Template version is not 2.8"
    FAILURES=$((FAILURES + 1))
fi

# Test 5.2: Advisory field documented with comment
echo -n "Test 5.2: Advisory field has documentation comment... "
if grep -qE "#.*advisory|advisory.*#|advisory.*comment" "$TEMPLATE" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - Advisory field lacks documentation"
    FAILURES=$((FAILURES + 1))
fi

# Test 5.3: source_gap field documented with pattern
echo -n "Test 5.3: source_gap field documented with GAP pattern... "
if grep -qE "source_gap.*GAP|GAP.*source_gap" "$TEMPLATE" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - source_gap pattern not documented"
    FAILURES=$((FAILURES + 1))
fi

# Test 5.4: source_story field documented
echo -n "Test 5.4: source_story field documented with STORY pattern... "
if grep -qE "source_story.*STORY|STORY.*source_story" "$TEMPLATE" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - source_story pattern not documented"
    FAILURES=$((FAILURES + 1))
fi

# Test 5.5: Changelog entry for v2.8
echo -n "Test 5.5: Changelog has v2.8 entry... "
if grep -qE "v2\.8.*advisory|2\.8.*Advisory" "$TEMPLATE" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No v2.8 changelog entry"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=== AC#5 Results: $((5 - FAILURES))/5 tests passed ==="
exit $FAILURES
