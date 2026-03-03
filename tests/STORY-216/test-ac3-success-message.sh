#!/bin/bash
# STORY-216 AC-3 Test: Success Path Confirmation
# Tests that success message is displayed when deep-validation-workflow.md WAS loaded
#
# Expected: FAIL initially (TDD Red phase - success message does not exist yet)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"

echo "=============================================="
echo "STORY-216 AC-3: Success Path Confirmation Test"
echo "=============================================="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: Check for ELSE branch (success path)
echo "[Test 1] Checking for ELSE branch in verification logic..."
# Need to find ELSE within the Phase 0 Completion Enforcement section
if ! grep -A 20 "^### Phase 0 Completion Enforcement" "$TARGET_FILE" | grep -q "ELSE:"; then
    echo "FAIL: ELSE branch not found in Phase 0 Completion Enforcement section"
    echo ""
    echo "Expected: ELSE branch for success path when file WAS loaded"
    exit 1
fi
echo "PASS: ELSE branch found"

# Test 2: Check for exact success message
echo ""
echo "[Test 2] Checking for success confirmation message..."
EXPECTED_MESSAGE="Deep mode workflow reference verified loaded"

if ! grep -q "$EXPECTED_MESSAGE" "$TARGET_FILE"; then
    echo "FAIL: Success message not found"
    echo ""
    echo "Expected message: '$EXPECTED_MESSAGE'"
    exit 1
fi
echo "PASS: Success message found"

# Test 3: Verify success message has checkmark indicator
echo ""
echo "[Test 3] Checking success message includes checkmark indicator..."

# Check for checkmark pattern with the success message
if ! grep -E "(✓|\\\\u2713).*Deep mode workflow reference verified" "$TARGET_FILE"; then
    echo "FAIL: Success message missing checkmark indicator"
    echo ""
    echo "Expected pattern: checkmark followed by success message"
    exit 1
fi
echo "PASS: Checkmark indicator present"

# Test 4: Verify success message is within the enforcement section
echo ""
echo "[Test 4] Checking success message is in correct section..."

# Get the section content and verify message is there
SECTION_CONTENT=$(grep -A 30 "^### Phase 0 Completion Enforcement" "$TARGET_FILE" | head -30)

if ! echo "$SECTION_CONTENT" | grep -q "Deep mode workflow reference verified loaded"; then
    echo "FAIL: Success message not within Phase 0 Completion Enforcement section"
    exit 1
fi
echo "PASS: Success message correctly placed in enforcement section"

echo ""
echo "=============================================="
echo "AC-3 RESULT: ALL TESTS PASSED"
echo "=============================================="
exit 0
