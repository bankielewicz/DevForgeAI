#!/bin/bash
# STORY-216 AC-4 Test: Exact Text Added Per RCA-021
# Tests that the exact text from RCA-021 REC-2 was added to SKILL.md
#
# Expected: FAIL initially (TDD Red phase - exact text does not exist yet)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"

echo "=============================================="
echo "STORY-216 AC-4: Exact Text From RCA-021 Test"
echo "=============================================="
echo "Target: $TARGET_FILE"
echo ""

# The exact text from RCA-021 REC-2 (lines 215-233) that must be present
# We'll check for key structural elements that confirm exact implementation

# Test 1: Check section header matches exactly
echo "[Test 1] Checking section header matches RCA-021..."
if ! grep -q "^### Phase 0 Completion Enforcement$" "$TARGET_FILE"; then
    echo "FAIL: Exact section header not found"
    echo ""
    echo "Expected: '### Phase 0 Completion Enforcement'"
    exit 1
fi
echo "PASS: Section header matches"

# Test 2: Check verification description line
echo ""
echo "[Test 2] Checking verification description line..."
if ! grep -q "Verify deep-validation-workflow.md was loaded (deep mode only)" "$TARGET_FILE"; then
    echo "FAIL: Verification description not found"
    echo ""
    echo "Expected: 'Verify deep-validation-workflow.md was loaded (deep mode only)'"
    exit 1
fi
echo "PASS: Verification description found"

# Test 3: Check for the exact error display lines from RCA-021
echo ""
echo "[Test 3] Checking for RCA-021 specified error messages..."

# Check line 1 of error display
if ! grep -q 'Display:.*CRITICAL ERROR.*Phase 0 Step 0.5 incomplete' "$TARGET_FILE"; then
    echo "FAIL: First error display line not found"
    echo ""
    echo "Expected: 'Display:.*CRITICAL ERROR.*Phase 0 Step 0.5 incomplete'"
    exit 1
fi

# Check line 2 of error display
if ! grep -q 'Deep validation workflow reference file was not loaded' "$TARGET_FILE"; then
    echo "FAIL: Second error display line not found"
    echo ""
    echo "Expected: 'Deep validation workflow reference file was not loaded'"
    exit 1
fi
echo "PASS: Error messages match RCA-021"

# Test 4: Check for instruction line with resume command pattern
echo ""
echo "[Test 4] Checking for resume instruction..."
if ! grep -q 'Instruction:.*Load.*reference file.*resume' "$TARGET_FILE"; then
    echo "FAIL: Resume instruction not found"
    echo ""
    echo "Expected pattern: 'Instruction:.*Load.*reference file.*resume'"
    exit 1
fi
echo "PASS: Resume instruction found"

# Test 5: Check for closing statement
echo ""
echo "[Test 5] Checking for enforcement rationale statement..."
if ! grep -q 'enforcement prevents Phase 1.*executing without complete initialization' "$TARGET_FILE"; then
    echo "FAIL: Enforcement rationale statement not found"
    echo ""
    echo "Expected: 'enforcement prevents Phase 1.*executing without complete initialization'"
    exit 1
fi
echo "PASS: Enforcement rationale statement found"

# Test 6: Verify the code block structure (IF/ELSE pattern)
echo ""
echo "[Test 6] Checking IF/ELSE code block structure..."
SECTION=$(grep -A 25 "^### Phase 0 Completion Enforcement" "$TARGET_FILE")

# Check IF structure
if ! echo "$SECTION" | grep -q 'IF mode == "deep":'; then
    echo "FAIL: IF mode == \"deep\": not found in section"
    exit 1
fi

# Check nested IF for file not loaded
if ! echo "$SECTION" | grep -q 'IF.*NOT loaded'; then
    echo "FAIL: Nested IF for 'NOT loaded' check not found"
    exit 1
fi

# Check ELSE for success path
if ! echo "$SECTION" | grep -q 'ELSE:'; then
    echo "FAIL: ELSE branch not found"
    exit 1
fi

echo "PASS: IF/ELSE code block structure correct"

echo ""
echo "=============================================="
echo "AC-4 RESULT: ALL TESTS PASSED"
echo "=============================================="
exit 0
