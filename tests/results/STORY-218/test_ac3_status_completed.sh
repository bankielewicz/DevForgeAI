#!/bin/bash
# Test AC-3: Phase Status Updates to "completed" (when phase marker written)
# Expected: FAIL initially (before implementation)

SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"

echo "=== AC-3: Status Updates to completed After Phase Marker ==="

# Test: TodoWrite with completed status after each "Phase N Marker Write" section
COMPLETED_AFTER_MARKER=0

for phase in 0 1 2 3 4; do
    # Find Phase Marker Write section and check for TodoWrite completed after it
    if grep -A20 "Phase $phase Marker Write" "$SKILL_FILE" | grep -qE 'TodoWrite.*completed|status.*completed'; then
        ((COMPLETED_AFTER_MARKER++))
    fi
done

if [ "$COMPLETED_AFTER_MARKER" -ge 5 ]; then
    echo "PASS: Found TodoWrite completed status after $COMPLETED_AFTER_MARKER phase markers"
    exit 0
else
    echo "FAIL: Expected 5 TodoWrite calls after marker writes, found $COMPLETED_AFTER_MARKER"
    exit 1
fi
