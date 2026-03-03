#!/bin/bash
# Test AC-4: TodoWrite After Each Phase Marker (5 locations)
# Expected: FAIL initially (before implementation)

SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"

echo "=== AC-4: TodoWrite After Each Phase Marker Write Section ==="

# Expected locations: After Phase 0, 1, 2, 3, 4 Marker Write sections
MARKER_SECTIONS=(
    "Phase 0 Marker Write"
    "Phase 1 Marker Write"
    "Phase 2 Marker Write"
    "Phase 3 Marker Write"
    "Phase 4 Marker Write"
)

TODOWRITE_COUNT=0

for section in "${MARKER_SECTIONS[@]}"; do
    # Check if TodoWrite appears within 30 lines after marker write
    if grep -A30 "$section" "$SKILL_FILE" | grep -qE "TodoWrite"; then
        ((TODOWRITE_COUNT++))
        echo "  Found TodoWrite after: $section"
    else
        echo "  MISSING TodoWrite after: $section"
    fi
done

if [ "$TODOWRITE_COUNT" -eq 5 ]; then
    echo "PASS: All 5 phase markers have TodoWrite calls"
    exit 0
else
    echo "FAIL: Expected 5 TodoWrite calls after markers, found $TODOWRITE_COUNT"
    exit 1
fi
