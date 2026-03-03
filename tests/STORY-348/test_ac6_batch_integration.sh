#!/bin/bash
# STORY-348 AC#6: Integration with Batch Story Creation Workflow
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== AC#6: Batch Story Creation Integration Tests ==="
echo "Target files:"
echo "  - .claude/commands/review-qa-reports.md"
echo "  - .claude/skills/devforgeai-qa-remediation/SKILL.md"

FAILURES=0

# Test 6.1: Review command supports --create-stories with advisory gaps
echo -n "Test 6.1: review-qa-reports documents advisory gap handling... "
if grep -qiE "advisory.*gap|gap.*advisory|\[ADVISORY\]" "$PROJECT_ROOT/.claude/commands/review-qa-reports.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No advisory gap handling in review command"
    FAILURES=$((FAILURES + 1))
fi

# Test 6.2: Separate counts for advisory vs blocking stories
echo -n "Test 6.2: Summary shows separate advisory/blocking counts... "
if grep -qiE "Advisory Stories Created|Blocking Stories Created|advisory.*count|blocking.*count" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No separate advisory/blocking counts in summary"
    FAILURES=$((FAILURES + 1))
fi

# Test 6.3: Gap classification logic documented
echo -n "Test 6.3: Gap classification (blocking vs advisory) documented... "
if grep -qiE "classify.*gap|gap.*classification|blocking.*false.*advisory|advisory.*blocking.*false" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No gap classification logic documented"
    FAILURES=$((FAILURES + 1))
fi

# Test 6.4: is_advisory flag passed to story creation
echo -n "Test 6.4: is_advisory flag passed during story creation... "
if grep -qiE "is_advisory|advisory.*flag|flag.*advisory" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - is_advisory flag not documented"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=== AC#6 Results: $((4 - FAILURES))/4 tests passed ==="
exit $FAILURES
