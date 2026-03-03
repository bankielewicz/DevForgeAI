#!/bin/bash
# STORY-343 AC#3: Phase 03 Reads Friction Catalog
# TDD Red Phase - This test MUST FAIL until implementation complete

PHASE_FILE=".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
EXIT_CODE=0

echo "=== AC#3: Phase 03 Reads Friction Catalog ==="

# Test 1: Friction Awareness section exists
if grep -q "## Friction Awareness" "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] Friction Awareness section header found"
else
    echo "[FAIL] Missing 'Friction Awareness' section header"
    EXIT_CODE=1
fi

# Test 2: Read() instruction for friction-catalog.md
if grep -qE 'Read\(.*friction-catalog\.md' "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] Read() for friction-catalog.md found"
else
    echo "[FAIL] Missing Read() instruction for .claude/memory/learning/friction-catalog.md"
    EXIT_CODE=1
fi

exit $EXIT_CODE
