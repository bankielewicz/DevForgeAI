#!/usr/bin/env bash
# =============================================================================
# STORY-372 AC#2: Test Function Discovery and Name Pattern Extraction
# =============================================================================
# Validates that coverage-analyzer.md (or its reference files) contains:
#   1. Treelint search on test files to discover test functions
#   2. test_ prefix stripping logic for Python
#   3. Test class prefix stripping (TestClass.test_method -> Class.method)
#   4. Example mappings (e.g., test_processOrder -> processOrder)
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer.md"
REFERENCE_DIR="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer/references"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  FAIL: $1"
}

search_files() {
    local files="$TARGET_FILE"
    if [[ -d "$REFERENCE_DIR" ]]; then
        for f in "$REFERENCE_DIR"/*.md; do
            [[ -r "$f" ]] && files="$files $f"
        done
    fi
    echo "$files"
}

echo "=============================================="
echo "  AC#2: Test Function Discovery and Name Pattern Extraction"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "coverage-analyzer.md exists and is readable"
else
    fail "coverage-analyzer.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Treelint search on test files documented
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Search on Test Files ---"
if grep -qiE 'treelint search.*test.file|treelint.*--file.*test|test.*function.*discover' $(search_files) 2>/dev/null; then
    pass "Treelint search on test files documented"
else
    fail "Missing Treelint search instruction for test file discovery"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: test_ prefix stripping logic documented
# -----------------------------------------------------------------------------
echo "--- Test 3: test_ Prefix Stripping ---"
if grep -qE '(strip|remov|extract).*test_.*prefix|test_.*prefix.*(strip|remov)' $(search_files) 2>/dev/null; then
    pass "test_ prefix stripping logic documented"
else
    fail "Missing test_ prefix stripping logic documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Test class prefix stripping (TestClass -> Class)
# -----------------------------------------------------------------------------
echo "--- Test 4: TestClass Prefix Stripping ---"
if grep -qiE '(Test.*class.*prefix.*(strip|remov)|TestUserService.*UserService|Test.*prefix.*(strip|remov))' $(search_files) 2>/dev/null; then
    pass "Test class prefix stripping documented (TestClass -> Class)"
else
    fail "Missing TestClass prefix stripping logic (e.g., TestUserService.test_create -> UserService.create)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Example mapping documented (test_processOrder -> processOrder)
# -----------------------------------------------------------------------------
echo "--- Test 5: Example Name Mapping ---"
if grep -qE '(test_processOrder.*processOrder|test_.*maps to|test_.*->|test_.*=>)' $(search_files) 2>/dev/null; then
    pass "Example mapping documented (e.g., test_processOrder -> processOrder)"
else
    fail "Missing example name mapping (e.g., test_processOrder -> processOrder)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Section heading for test function discovery
# -----------------------------------------------------------------------------
echo "--- Test 6: Test Function Discovery Section ---"
if grep -qiE '^#{1,4}.*[Tt]est.*[Ff]unction.*[Dd]iscovery|^#{1,4}.*[Nn]ame.*[Pp]attern.*[Ee]xtract' $(search_files) 2>/dev/null; then
    pass "Test function discovery section heading found"
else
    fail "Missing section heading for test function discovery or name pattern extraction"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
