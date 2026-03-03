#!/bin/bash
# Test: AC#6 - Operational Copy Synchronization
# Story: STORY-332 - Refactor session-miner.md with Progressive Disclosure
# Purpose: Verify src/ and .claude/ copies are identical
#
# Expected: FAIL (Red phase) - Refactored files do not exist yet

# set -e  # Removed to allow all tests to run

# Configuration
SRC_CORE="src/claude/agents/session-miner.md"
OPS_CORE=".claude/agents/session-miner.md"
SRC_REFS="src/claude/agents/session-miner/references"
OPS_REFS=".claude/agents/session-miner/references"

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0

echo "=============================================="
echo "  AC#6: Operational Copy Synchronization Tests"
echo "  STORY-332 - Progressive Disclosure Refactor"
echo "=============================================="
echo ""

# Test 1: Verify source core file exists
echo "Test 1: Source core file exists"
if [[ -f "$SRC_CORE" ]]; then
    echo "  PASS: $SRC_CORE exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $SRC_CORE does not exist"
    ((TESTS_FAILED++))
fi

# Test 2: Verify operational core file exists
echo ""
echo "Test 2: Operational core file exists"
if [[ -f "$OPS_CORE" ]]; then
    echo "  PASS: $OPS_CORE exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $OPS_CORE does not exist"
    ((TESTS_FAILED++))
fi

# Test 3: Verify core files are identical
echo ""
echo "Test 3: Core files are identical"
if [[ -f "$SRC_CORE" && -f "$OPS_CORE" ]]; then
    DIFF_OUTPUT=$(diff "$SRC_CORE" "$OPS_CORE" 2>&1 || true)
    if [[ -z "$DIFF_OUTPUT" ]]; then
        echo "  PASS: Core files are identical"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Core files differ"
        echo "  Diff summary:"
        echo "$DIFF_OUTPUT" | head -10
        ((TESTS_FAILED++))
    fi
else
    echo "  SKIP: Cannot compare - one or both files missing"
    ((TESTS_FAILED++))
fi

# Test 4: Verify source references directory exists
echo ""
echo "Test 4: Source references directory exists"
if [[ -d "$SRC_REFS" ]]; then
    echo "  PASS: $SRC_REFS exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $SRC_REFS does not exist"
    ((TESTS_FAILED++))
fi

# Test 5: Verify operational references directory exists
echo ""
echo "Test 5: Operational references directory exists"
if [[ -d "$OPS_REFS" ]]; then
    echo "  PASS: $OPS_REFS exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $OPS_REFS does not exist"
    ((TESTS_FAILED++))
fi

# Test 6: Verify reference directories are identical (recursive diff)
echo ""
echo "Test 6: Reference directories are identical (recursive diff)"
if [[ -d "$SRC_REFS" && -d "$OPS_REFS" ]]; then
    DIFF_OUTPUT=$(diff -r "$SRC_REFS" "$OPS_REFS" 2>&1 || true)
    if [[ -z "$DIFF_OUTPUT" ]]; then
        echo "  PASS: Reference directories are identical"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Reference directories differ"
        echo "  Diff summary:"
        echo "$DIFF_OUTPUT" | head -15
        ((TESTS_FAILED++))
    fi
else
    echo "  SKIP: Cannot compare - one or both directories missing"
    ((TESTS_FAILED++))
fi

# Test 7: Verify file counts match
echo ""
echo "Test 7: File counts match between src/ and .claude/"
if [[ -d "$SRC_REFS" && -d "$OPS_REFS" ]]; then
    SRC_COUNT=$(find "$SRC_REFS" -type f -name "*.md" | wc -l)
    OPS_COUNT=$(find "$OPS_REFS" -type f -name "*.md" | wc -l)

    if [[ $SRC_COUNT -eq $OPS_COUNT ]]; then
        echo "  PASS: File counts match ($SRC_COUNT files)"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: File counts differ"
        echo "    src/ references: $SRC_COUNT files"
        echo "    .claude/ references: $OPS_COUNT files"
        ((TESTS_FAILED++))
    fi
else
    echo "  SKIP: Cannot compare - directories missing"
    ((TESTS_FAILED++))
fi

# Test 8: List files in both locations
echo ""
echo "Test 8: File inventory"
echo "  Source ($SRC_REFS):"
if [[ -d "$SRC_REFS" ]]; then
    for file in "$SRC_REFS"/*.md; do
        if [[ -f "$file" ]]; then
            echo "    - $(basename "$file")"
        fi
    done
else
    echo "    (directory not found)"
fi

echo "  Operational ($OPS_REFS):"
if [[ -d "$OPS_REFS" ]]; then
    for file in "$OPS_REFS"/*.md; do
        if [[ -f "$file" ]]; then
            echo "    - $(basename "$file")"
        fi
    done
else
    echo "    (directory not found)"
fi
((TESTS_PASSED++))

# Summary
echo ""
echo "=============================================="
echo "  AC#6 TEST SUMMARY"
echo "=============================================="
echo "  Tests passed: $TESTS_PASSED"
echo "  Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "  STATUS: PASSED - All AC#6 requirements met"
    exit 0
else
    echo "  STATUS: FAILED - $TESTS_FAILED requirement(s) not met"
    exit 1
fi
