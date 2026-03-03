#!/bin/bash
# STORY-343 AC#1: Phase 02 Reads TDD Patterns
# TDD Red Phase - This test MUST FAIL until implementation complete

PHASE_FILE=".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
EXIT_CODE=0

echo "=== AC#1: Phase 02 Reads TDD Patterns ==="

# Test 1: Memory Context section exists
if grep -q "## Memory Context" "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] Memory Context section header found"
else
    echo "[FAIL] Missing 'Memory Context' section header"
    EXIT_CODE=1
fi

# Test 2: Read() instruction for tdd-patterns.md
if grep -qE 'Read\(.*tdd-patterns\.md' "$PHASE_FILE" 2>/dev/null; then
    echo "[PASS] Read() for tdd-patterns.md found"
else
    echo "[FAIL] Missing Read() instruction for .claude/memory/learning/tdd-patterns.md"
    EXIT_CODE=1
fi

exit $EXIT_CODE
