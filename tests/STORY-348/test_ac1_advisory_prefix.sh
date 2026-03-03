#!/bin/bash
# STORY-348 AC#1: Story Title Includes [ADVISORY] Prefix
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== AC#1: Advisory Story Title and Filename Tests ==="
echo "Target files:"
echo "  - .claude/skills/devforgeai-story-creation/SKILL.md"
echo "  - .claude/skills/devforgeai-qa-remediation/SKILL.md"

FAILURES=0

# Test 1.1: Story creation skill documents [ADVISORY] prefix handling
echo -n "Test 1.1: SKILL.md documents [ADVISORY] prefix for advisory gaps... "
if grep -q "\[ADVISORY\]" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No [ADVISORY] prefix documentation found"
    FAILURES=$((FAILURES + 1))
fi

# Test 1.2: Remediation skill handles advisory flag for title generation
echo -n "Test 1.2: Remediation SKILL.md has advisory title prefix logic... "
if grep -q "advisory.*prefix\|prefix.*advisory\|\[ADVISORY\]" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No advisory prefix logic in remediation skill"
    FAILURES=$((FAILURES + 1))
fi

# Test 1.3: Filename includes 'advisory' slug pattern
echo -n "Test 1.3: Documentation specifies 'advisory' slug in filename... "
if grep -qE "STORY-[0-9]+-advisory-|advisory.*slug|slug.*advisory" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No 'advisory' filename slug pattern documented"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=== AC#1 Results: $((3 - FAILURES))/3 tests passed ==="
exit $FAILURES
