#!/bin/bash
# STORY-348 AC#3: Frontmatter Includes Source Traceability Fields
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== AC#3: Source Traceability Fields Tests ==="
echo "Target files:"
echo "  - .claude/skills/devforgeai-story-creation/SKILL.md"
echo "  - .claude/skills/devforgeai-qa-remediation/SKILL.md"

FAILURES=0

# Test 3.1: source_gap field documented
echo -n "Test 3.1: Template documents source_gap field... "
if grep -qE "source_gap:|source_gap" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No source_gap field in template"
    FAILURES=$((FAILURES + 1))
fi

# Test 3.2: source_story field documented
echo -n "Test 3.2: Template documents source_story field... "
if grep -qE "source_story:|source_story" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No source_story field in template"
    FAILURES=$((FAILURES + 1))
fi

# Test 3.3: GAP-XXX pattern validation
echo -n "Test 3.3: source_gap pattern GAP-XXX documented... "
if grep -qE "GAP-[0-9]{3}|GAP-\\\\d{3}" "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - No GAP-XXX pattern validation"
    FAILURES=$((FAILURES + 1))
fi

# Test 3.4: Remediation skill passes source fields
echo -n "Test 3.4: Remediation skill passes source_gap and source_story... "
if grep -qE "source_gap|source_story" "$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL - Remediation skill missing source field handling"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=== AC#3 Results: $((4 - FAILURES))/4 tests passed ==="
exit $FAILURES
