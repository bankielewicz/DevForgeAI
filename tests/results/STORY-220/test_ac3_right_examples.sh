#!/bin/bash
# Test AC-3b: RIGHT Behavior Examples
# DOC-004: Provide 3+ examples of RIGHT behavior with markers
# Expected: FAIL initially (before implementation)

CLAUDE_FILE="src/CLAUDE.md"

echo "=== AC-3b: RIGHT Behavior Examples ==="

# Check if CLAUDE.md exists
if [ ! -f "$CLAUDE_FILE" ]; then
    echo "FAIL: Target file $CLAUDE_FILE does not exist"
    exit 1
fi

# Get content of the CRITICAL section
CRITICAL_LINE=$(grep -n "## CRITICAL: No Deviation from Skill Phases" "$CLAUDE_FILE" | head -1 | cut -d: -f1)

if [ -z "$CRITICAL_LINE" ]; then
    echo "FAIL: Section '## CRITICAL: No Deviation from Skill Phases' not found"
    exit 1
fi

# Extract section content (skip header, find next ## section)
SECTION_START=$((CRITICAL_LINE + 1))
SECTION_END=$((CRITICAL_LINE + 150))
SECTION_CONTENT=$(sed -n "${SECTION_START},${SECTION_END}p" "$CLAUDE_FILE" | sed '/^## [A-Za-z]/q' | head -n -1)

# Test 1: Count RIGHT markers (various formats)
# Accepts: RIGHT, right, Right, CORRECT, correct with various marker styles
RIGHT_MARKERS=$(echo "$SECTION_CONTENT" | grep -cE ".*(RIGHT|CORRECT).*" | head -1)

if [ "$RIGHT_MARKERS" -ge 3 ]; then
    echo "  [PASS] Found $RIGHT_MARKERS RIGHT/CORRECT examples (minimum: 3)"
else
    echo "  [FAIL] Found only $RIGHT_MARKERS RIGHT/CORRECT examples (minimum: 3 required)"
    exit 1
fi

# Test 2: Check for specific correct behavior patterns
CORRECT_PATTERNS=0

if echo "$SECTION_CONTENT" | grep -qiE "(execute|run).*(all|every|complete).*(phase|step)"; then
    ((CORRECT_PATTERNS++))
    echo "  [PASS] Includes 'execute all phases' as correct behavior"
fi

if echo "$SECTION_CONTENT" | grep -qiE "(sequential|in.?order|step.?by.?step)"; then
    ((CORRECT_PATTERNS++))
    echo "  [PASS] Includes sequential execution as correct behavior"
fi

if echo "$SECTION_CONTENT" | grep -qiE "(complete|finish).*(before|then).*(proceed|next)"; then
    ((CORRECT_PATTERNS++))
    echo "  [PASS] Includes complete-before-proceed as correct behavior"
fi

if [ "$CORRECT_PATTERNS" -lt 2 ]; then
    echo "  [WARN] Only $CORRECT_PATTERNS correct pattern types found (recommend at least 2)"
fi

echo "PASS: AC-3b - At least 3 RIGHT behavior examples documented"
exit 0
