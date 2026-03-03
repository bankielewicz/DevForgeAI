#!/bin/bash
# STORY-348 AC#2: Frontmatter Includes advisory: true Field
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== AC#2: Advisory Frontmatter Field Tests ==="
echo "Target files:"
echo "  - .claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
echo "  - .claude/skills/devforgeai-story-creation/SKILL.md"

FAILURES=0

# Test 2.1: Story template documents advisory field
echo -n "Test 2.1: Template has 'advisory:' field documentation... "
if grep -qE "^advisory:|advisory: true|advisory: false" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No 'advisory:' field in template"
    FAILURES=$((FAILURES + 1))
fi

# Test 2.2: Advisory field positioned after priority field
echo -n "Test 2.2: Advisory field after priority in template... "
PRIORITY_LINE=$(grep -n "^priority:" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md" 2>/dev/null | head -1 | cut -d: -f1)
ADVISORY_LINE=$(grep -n "^advisory:" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md" 2>/dev/null | head -1 | cut -d: -f1)
if [ -n "$PRIORITY_LINE" ] && [ -n "$ADVISORY_LINE" ] && [ "$ADVISORY_LINE" -gt "$PRIORITY_LINE" ]; then
    echo "PASS"
else
    echo "FAIL - Advisory field not positioned after priority"
    FAILURES=$((FAILURES + 1))
fi

# Test 2.3: Blocking stories exclude advisory: true
echo -n "Test 2.3: Documentation specifies blocking stories omit advisory field... "
if grep -qE "blocking.*omit.*advisory|blocking.*advisory.*false|advisory.*blocking.*false" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No blocking story advisory handling documented"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=== AC#2 Results: $((3 - FAILURES))/3 tests passed ==="
exit $FAILURES
