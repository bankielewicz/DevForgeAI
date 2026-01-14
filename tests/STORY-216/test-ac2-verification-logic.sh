#!/bin/bash
# STORY-216 AC-2 Test: Deep Mode Workflow Verification Logic
# Tests that verification logic checks if deep-validation-workflow.md was loaded
#
# Expected: FAIL initially (TDD Red phase - verification logic does not exist yet)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"

echo "=============================================="
echo "STORY-216 AC-2: Deep Mode Verification Logic Test"
echo "=============================================="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: Check for mode == "deep" condition
echo "[Test 1] Checking for deep mode conditional check..."
if ! grep -q 'IF mode == "deep"' "$TARGET_FILE"; then
    echo "FAIL: Deep mode conditional 'IF mode == \"deep\"' not found in enforcement section"
    exit 1
fi
echo "PASS: Deep mode conditional found"

# Test 2: Check for deep-validation-workflow.md reference check
echo ""
echo "[Test 2] Checking for deep-validation-workflow.md loading verification..."
if ! grep -q 'deep-validation-workflow.md.*NOT loaded' "$TARGET_FILE"; then
    echo "FAIL: Reference file loading check not found"
    echo ""
    echo "Expected pattern: 'deep-validation-workflow.md.*NOT loaded'"
    exit 1
fi
echo "PASS: Reference file loading check found"

# Test 3: Check for HALT instruction on failure
echo ""
echo "[Test 3] Checking for HALT instruction when not loaded..."
if ! grep -q 'HALT:.*Cannot proceed to Phase 1' "$TARGET_FILE"; then
    echo "FAIL: HALT instruction for Phase 1 blocking not found"
    echo ""
    echo "Expected pattern: 'HALT:.*Cannot proceed to Phase 1'"
    exit 1
fi
echo "PASS: HALT instruction found"

# Test 4: Verify error display message exists
echo ""
echo "[Test 4] Checking for critical error display message..."
if ! grep -q 'CRITICAL ERROR.*Phase 0 Step 0.5 incomplete' "$TARGET_FILE"; then
    echo "FAIL: Critical error display message not found"
    echo ""
    echo "Expected: 'CRITICAL ERROR.*Phase 0 Step 0.5 incomplete'"
    exit 1
fi
echo "PASS: Critical error display message found"

# Test 5: Verify file path is provided in error message
echo ""
echo "[Test 5] Checking error message includes file path for resolution..."
if ! grep -q '.claude/skills/devforgeai-qa/references/deep-validation-workflow.md' "$TARGET_FILE"; then
    echo "FAIL: Full file path not included in error/instruction message"
    echo ""
    echo "Expected path: .claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
    exit 1
fi
echo "PASS: File path included in message"

echo ""
echo "=============================================="
echo "AC-2 RESULT: ALL TESTS PASSED"
echo "=============================================="
exit 0
