#!/bin/bash
# STORY-216 AC-1 Test: Phase 0 Completion Enforcement Section Added
# Tests that the "Phase 0 Completion Enforcement" subsection exists after Phase 0 Marker Write
#
# Expected: FAIL initially (TDD Red phase - section does not exist yet)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"

echo "=============================================="
echo "STORY-216 AC-1: Section Placement Test"
echo "=============================================="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: Verify target file exists
echo "[Test 1] Checking target file exists..."
if [ ! -f "$TARGET_FILE" ]; then
    echo "FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi
echo "PASS: Target file exists"

# Test 2: Check for section header "### Phase 0 Completion Enforcement"
echo ""
echo "[Test 2] Checking for 'Phase 0 Completion Enforcement' section header..."
if ! grep -q "^### Phase 0 Completion Enforcement" "$TARGET_FILE"; then
    echo "FAIL: Section header '### Phase 0 Completion Enforcement' not found"
    echo ""
    echo "Expected section header after Phase 0 Marker Write section:"
    echo "  ### Phase 0 Completion Enforcement"
    exit 1
fi
echo "PASS: Section header found"

# Test 3: Verify section appears AFTER Phase 0 Marker Write section
echo ""
echo "[Test 3] Checking section placement (after 'Phase 0 Marker Write')..."

# Get line numbers
MARKER_WRITE_LINE=$(grep -n "^### Phase 0 Marker Write" "$TARGET_FILE" | head -1 | cut -d: -f1)
ENFORCEMENT_LINE=$(grep -n "^### Phase 0 Completion Enforcement" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -z "$MARKER_WRITE_LINE" ]; then
    echo "FAIL: 'Phase 0 Marker Write' section not found (prerequisite)"
    exit 1
fi

if [ -z "$ENFORCEMENT_LINE" ]; then
    echo "FAIL: 'Phase 0 Completion Enforcement' section not found"
    exit 1
fi

if [ "$ENFORCEMENT_LINE" -le "$MARKER_WRITE_LINE" ]; then
    echo "FAIL: Section must appear AFTER 'Phase 0 Marker Write'"
    echo "  Phase 0 Marker Write: line $MARKER_WRITE_LINE"
    echo "  Phase 0 Completion Enforcement: line $ENFORCEMENT_LINE"
    exit 1
fi
echo "PASS: Section appears after Phase 0 Marker Write (line $MARKER_WRITE_LINE -> $ENFORCEMENT_LINE)"

# Test 4: Verify section appears BEFORE Phase 1 Pre-Flight (if it exists)
echo ""
echo "[Test 4] Checking section appears before Phase 1 Pre-Flight..."

PHASE1_LINE=$(grep -n "^## Phase 1:" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -n "$PHASE1_LINE" ] && [ "$ENFORCEMENT_LINE" -ge "$PHASE1_LINE" ]; then
    echo "FAIL: Section must appear BEFORE Phase 1"
    echo "  Phase 0 Completion Enforcement: line $ENFORCEMENT_LINE"
    echo "  Phase 1: line $PHASE1_LINE"
    exit 1
fi
echo "PASS: Section placed correctly in Phase 0 area"

echo ""
echo "=============================================="
echo "AC-1 RESULT: ALL TESTS PASSED"
echo "=============================================="
exit 0
