#!/bin/bash
# Test AC-5: All 5 Phase Transitions Tracked (TodoWrite updated 5 times)
# Expected: FAIL initially (before implementation)

SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"

echo "=== AC-5: All 5 Phase Transitions Tracked ==="

# Count total TodoWrite calls that update phase status
TODOWRITE_CALLS=$(grep -cE "TodoWrite" "$SKILL_FILE" 2>/dev/null)
TODOWRITE_CALLS=${TODOWRITE_CALLS:-0}
TODOWRITE_CALLS=$(echo "$TODOWRITE_CALLS" | tr -d '[:space:]')

# Each phase needs at least 2 TodoWrite calls (start=in_progress, end=completed)
# Plus 1 initial call at Phase 0 start
EXPECTED_MIN_CALLS=6

if [ "$TODOWRITE_CALLS" -ge "$EXPECTED_MIN_CALLS" ] 2>/dev/null; then
    echo "PASS: Found $TODOWRITE_CALLS TodoWrite calls (minimum: $EXPECTED_MIN_CALLS)"
    exit 0
else
    echo "FAIL: Expected $EXPECTED_MIN_CALLS+ TodoWrite calls, found $TODOWRITE_CALLS"
    echo "  Need: 1 initial + 5 phases * (start + end) updates"
    exit 1
fi
