#!/bin/bash
# STORY-343 AC#2: Phase 02 Surfaces Relevant TDD Patterns
# TDD Red Phase - This test MUST FAIL until implementation complete

PHASE_FILE=".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
EXIT_CODE=0

echo "=== AC#2: Phase 02 Surfaces Relevant TDD Patterns ==="

# Test 1: Pattern matching logic exists
if grep -qE '(pattern.*match|match.*pattern|FOR.*pattern|keyword.*match)' "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] Pattern matching logic found"
else
    echo "[FAIL] Missing pattern matching logic in Phase 02"
    EXIT_CODE=1
fi

# Test 2: Display template with "Relevant TDD Patterns"
if grep -q "Relevant TDD Patterns" "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] 'Relevant TDD Patterns' display template found"
else
    echo "[FAIL] Missing 'Relevant TDD Patterns' display template"
    EXIT_CODE=1
fi

exit $EXIT_CODE
