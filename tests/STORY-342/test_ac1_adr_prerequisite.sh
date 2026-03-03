#!/bin/bash
# STORY-342 AC#1: ADR Created for Source Tree Update
# Tests that ADR-014 is approved and STORY-339 prerequisite is met

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
ADR_FILE="$PROJECT_ROOT/devforgeai/specs/adrs/ADR-014-memory-directory-structure.md"
LEARNING_DIR="$PROJECT_ROOT/.claude/memory/learning"

echo "=== AC#1: ADR Prerequisite Tests ==="

# Test 1: ADR-014 exists
echo -n "Test 1: ADR-014 file exists... "
if [ -f "$ADR_FILE" ]; then
    echo "PASS"
else
    echo "FAIL - ADR-014 not found at $ADR_FILE"
    exit 1
fi

# Test 2: ADR-014 status is APPROVED
echo -n "Test 2: ADR-014 status is APPROVED... "
if grep -q "^status: APPROVED" "$ADR_FILE"; then
    echo "PASS"
else
    echo "FAIL - ADR-014 status is not APPROVED"
    exit 1
fi

# Test 3: Learning directory exists per ADR
echo -n "Test 3: Learning directory exists (.claude/memory/learning/)... "
if [ -d "$LEARNING_DIR" ]; then
    echo "PASS"
else
    echo "FAIL - Learning directory not found at $LEARNING_DIR"
    exit 1
fi

echo ""
echo "=== AC#1 Tests Complete: All PASSED ==="
