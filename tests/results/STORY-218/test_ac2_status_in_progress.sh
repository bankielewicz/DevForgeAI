#!/bin/bash
# Test AC-2: Phase Status Updates to "in_progress"
# Expected: FAIL initially (before implementation)

SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"

echo "=== AC-2: Status Updates to in_progress ==="

# Check for in_progress status pattern in TodoWrite calls
IN_PROGRESS_COUNT=$(grep -cE 'status.*in_progress|"in_progress"' "$SKILL_FILE" 2>/dev/null)
IN_PROGRESS_COUNT=${IN_PROGRESS_COUNT:-0}
IN_PROGRESS_COUNT=$(echo "$IN_PROGRESS_COUNT" | tr -d '[:space:]')

if [ "$IN_PROGRESS_COUNT" -ge 5 ] 2>/dev/null; then
    echo "PASS: Found $IN_PROGRESS_COUNT in_progress status references"
    exit 0
else
    echo "FAIL: Expected 5+ in_progress status references, found $IN_PROGRESS_COUNT"
    exit 1
fi
