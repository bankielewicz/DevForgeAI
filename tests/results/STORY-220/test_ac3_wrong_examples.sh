#!/bin/bash
# Test AC-3a: WRONG Behavior Examples
# DOC-003: Provide 3+ examples of WRONG behavior with markers
# Expected: FAIL initially (before implementation)

CLAUDE_FILE="src/CLAUDE.md"

echo "=== AC-3a: WRONG Behavior Examples ==="

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

# Test 1: Count WRONG markers (various formats)
# Accepts: WRONG, wrong, Wrong with various marker styles
WRONG_COUNT=$(echo "$SECTION_CONTENT" | grep -ciE "(WRONG|wrong):" | head -1)
CROSS_WRONG_COUNT=$(echo "$SECTION_CONTENT" | grep -cE "^[[:space:]]*(x|X|wrong|WRONG)" | head -1)

# Count total WRONG examples with markers
WRONG_MARKERS=$(echo "$SECTION_CONTENT" | grep -cE ".*WRONG.*" | head -1)

if [ "$WRONG_MARKERS" -ge 3 ]; then
    echo "  [PASS] Found $WRONG_MARKERS WRONG examples (minimum: 3)"
else
    echo "  [FAIL] Found only $WRONG_MARKERS WRONG examples (minimum: 3 required)"
    exit 1
fi

# Test 2: Check for specific wrong behavior patterns (phase skipping, deviation)
DEVIATION_PATTERNS=0

if echo "$SECTION_CONTENT" | grep -qiE "skip.*(phase|step)"; then
    ((DEVIATION_PATTERNS++))
    echo "  [PASS] Includes phase skipping as wrong behavior"
fi

if echo "$SECTION_CONTENT" | grep -qiE "(deviat|omit|bypass)"; then
    ((DEVIATION_PATTERNS++))
    echo "  [PASS] Includes deviation/omission as wrong behavior"
fi

if echo "$SECTION_CONTENT" | grep -qiE "(partial|incomplete|half)"; then
    ((DEVIATION_PATTERNS++))
    echo "  [PASS] Includes partial execution as wrong behavior"
fi

if [ "$DEVIATION_PATTERNS" -lt 2 ]; then
    echo "  [WARN] Only $DEVIATION_PATTERNS deviation pattern types found (recommend at least 2)"
fi

echo "PASS: AC-3a - At least 3 WRONG behavior examples documented"
exit 0
