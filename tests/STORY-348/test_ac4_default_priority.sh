#!/bin/bash
# STORY-348 AC#4: Advisory Stories Default to Low Priority
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== AC#4: Advisory Stories Default Priority Tests ==="
echo "Target files:"
echo "  - .claude/skills/devforgeai-story-creation/SKILL.md"
echo "  - .claude/skills/devforgeai-qa-remediation/SKILL.md"

FAILURES=0

# Test 4.1: Advisory stories default to Low priority
echo -n "Test 4.1: Documentation specifies advisory = Low priority default... "
if grep -qiE "advisory.*priority.*low|priority.*low.*advisory|advisory.*default.*low" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No Low priority default for advisory stories"
    FAILURES=$((FAILURES + 1))
fi

# Test 4.2: Priority override mechanism documented
echo -n "Test 4.2: Priority override for advisory stories documented... "
if grep -qiE "override.*priority|priority.*override|user.*priority" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No priority override mechanism documented"
    FAILURES=$((FAILURES + 1))
fi

# Test 4.3: Story creation skill handles advisory priority
echo -n "Test 4.3: Story creation skill handles advisory priority... "
if grep -qiE "advisory.*priority|priority.*advisory" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - Story creation missing advisory priority handling"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=== AC#4 Results: $((3 - FAILURES))/3 tests passed ==="
exit $FAILURES
