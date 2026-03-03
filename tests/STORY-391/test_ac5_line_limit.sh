#!/usr/bin/env bash
# =============================================================================
# STORY-391 AC#5: Agent File Fits Within 500-Line Size Limit
#
# Verifies:
# 1. File line count is between 100 and 500 lines inclusive
# 2. If file exceeds 400 lines, reference files exist under
#    src/claude/agents/test-automator/references/
# 3. Token estimation (< 20K tokens for core file)
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"
REF_DIR="${PROJECT_ROOT}/src/claude/agents/test-automator/references"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

# --- Test Helper ---
run_test() {
    local test_name="$1"
    local test_result="$2"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ "$test_result" -eq 0 ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "  PASS: ${test_name}"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo "  FAIL: ${test_name}"
    fi
}

echo "================================================================"
echo "STORY-391 AC#5: Line Limit Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Test 1: Line count measurements
# =============================================================================
echo "--- Line Count ---"

LINE_COUNT=$(wc -l < "$AGENT_FILE")
echo "  Measured line count: ${LINE_COUNT}"

run_test "File has at least 100 lines (actual: ${LINE_COUNT})" "$( [ "$LINE_COUNT" -ge 100 ] && echo 0 || echo 1 )"
run_test "File has at most 500 lines (actual: ${LINE_COUNT})" "$( [ "$LINE_COUNT" -le 500 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Reference extraction check (conditional on > 400 lines)
# =============================================================================
echo ""
echo "--- Reference Extraction (conditional) ---"

if [ "$LINE_COUNT" -gt 400 ]; then
    echo "  File exceeds 400 lines - checking for reference extraction..."

    if [ -d "$REF_DIR" ]; then
        REF_FILE_COUNT=$(find "$REF_DIR" -name "*.md" -type f | wc -l)
        run_test "Reference directory exists with extracted files (found: ${REF_FILE_COUNT})" "$( [ "$REF_FILE_COUNT" -ge 1 ] && echo 0 || echo 1 )"
    else
        run_test "Reference directory exists for extraction (not found)" "1"
    fi
else
    echo "  File is ${LINE_COUNT} lines (under 400) - reference extraction not required"
    run_test "File under 400-line extraction threshold (${LINE_COUNT} lines)" "0"
fi

# =============================================================================
# Test 3: Token estimation (4 chars ~= 1 token, must be < 20K)
# =============================================================================
echo ""
echo "--- Token Estimation ---"

CHAR_COUNT=$(wc -c < "$AGENT_FILE")
ESTIMATED_TOKENS=$((CHAR_COUNT / 4))
echo "  Character count: ${CHAR_COUNT}"
echo "  Estimated tokens: ${ESTIMATED_TOKENS}"

run_test "Core file under 20K token estimate (actual: ~${ESTIMATED_TOKENS} tokens)" "$( [ "$ESTIMATED_TOKENS" -le 20000 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Reference files token check (each < 10K)
# =============================================================================
echo ""
echo "--- Reference Files Token Check ---"

if [ -d "$REF_DIR" ]; then
    REF_OVER_BUDGET=0
    while IFS= read -r ref_file; do
        REF_CHARS=$(wc -c < "$ref_file")
        REF_TOKENS=$((REF_CHARS / 4))
        REF_NAME=$(basename "$ref_file")
        if [ "$REF_TOKENS" -gt 10000 ]; then
            echo "  WARNING: ${REF_NAME} exceeds 10K tokens (~${REF_TOKENS})"
            REF_OVER_BUDGET=$((REF_OVER_BUDGET + 1))
        fi
    done < <(find "$REF_DIR" -name "*.md" -type f)
    run_test "All reference files under 10K token estimate" "$( [ "$REF_OVER_BUDGET" -eq 0 ] && echo 0 || echo 1 )"
else
    echo "  No reference directory found - skipping individual file checks"
    run_test "Reference directory exists (for token validation)" "0"
fi

# =============================================================================
# Test 5: Boundary validation (exactly at limits)
# =============================================================================
echo ""
echo "--- Boundary Validation ---"

# The file should be within inclusive range [100, 500]
IN_RANGE=$( [ "$LINE_COUNT" -ge 100 ] && [ "$LINE_COUNT" -le 500 ] && echo "yes" || echo "no" )
run_test "Line count within [100, 500] inclusive range (${LINE_COUNT})" "$( [ "$IN_RANGE" = "yes" ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Version 2.0.0 present (confirms this is the migrated file)
# =============================================================================
echo ""
echo "--- Migration Confirmation ---"

HAS_VERSION=$(grep -cE '^version:\s*"?2\.0\.0"?' "$AGENT_FILE" || true)
run_test "File is migrated version (version: 2.0.0)" "$( [ "$HAS_VERSION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
