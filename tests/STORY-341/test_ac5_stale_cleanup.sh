#!/bin/bash
# Test AC#5: Stale Sessions Cleaned Up
# Verifies cleanup logic for sessions >7 days with status=active
# Expected: FAIL (TDD Red phase - implementation not yet done)

set -e
# Check src/ (source of truth) first, fallback to .claude/ (operational)
TARGET_FILE="src/claude/skills/devforgeai-development/phases/phase-01-preflight.md"
if [ ! -f "$TARGET_FILE" ]; then
    TARGET_FILE=".claude/skills/devforgeai-development/phases/phase-01-preflight.md"
fi

echo "AC#5: Verifying stale session cleanup logic..."

# Test 1: Stale Session Cleanup section exists
if ! grep -qiE '(stale.*session|session.*cleanup|cleanup.*stale)' "$TARGET_FILE"; then
    echo "FAIL: Missing stale session cleanup section in phase-01-preflight.md"
    exit 1
fi

# Test 2: 7-day threshold documented
if ! grep -qE '7.*(day|days)' "$TARGET_FILE"; then
    echo "FAIL: 7-day threshold not documented for stale sessions"
    exit 1
fi

# Test 3: Cleanup checks for status=active
if ! grep -qE 'status.*active|active.*status' "$TARGET_FILE"; then
    echo "FAIL: Cleanup logic does not check for status=active"
    exit 1
fi

# Test 4: Glob pattern for sessions directory
if ! grep -qE 'Glob.*sessions|\.claude/memory/sessions' "$TARGET_FILE"; then
    echo "FAIL: Missing Glob pattern for sessions directory"
    exit 1
fi

echo "PASS: AC#5 Stale sessions cleanup logic"
