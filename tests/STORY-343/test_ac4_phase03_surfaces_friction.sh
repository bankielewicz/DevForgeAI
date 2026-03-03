#!/bin/bash
# STORY-343 AC#4: Phase 03 Surfaces Friction Warnings
# TDD Red Phase - This test MUST FAIL until implementation complete

PHASE_FILE=".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
EXIT_CODE=0

echo "=== AC#4: Phase 03 Surfaces Friction Warnings ==="

# Test 1: Friction matching logic exists
if grep -qE '(friction.*match|match.*friction|FOR.*friction|implementation.*type)' "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] Friction matching logic found"
else
    echo "[FAIL] Missing friction matching logic in Phase 03"
    EXIT_CODE=1
fi

# Test 2: Display template with "Friction Warning"
if grep -q "Friction Warning" "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] 'Friction Warning' display template found"
else
    echo "[FAIL] Missing 'Friction Warning' display template"
    EXIT_CODE=1
fi

exit $EXIT_CODE
