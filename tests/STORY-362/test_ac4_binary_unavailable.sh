#!/usr/bin/env bash
# =============================================================================
# STORY-362 AC#4: No Workflow Failure When Treelint Binary Is Unavailable
# =============================================================================
# Validates that treelint-search-patterns.md:
#   1. Documents exit code 127 handling (binary not found)
#   2. Documents exit code 126 handling (permission denied)
#   3. Specifies Grep fallback for binary unavailability
#   4. Warning message for binary not found scenario
#   5. Zero impact on calling skill workflow state (no HALT)
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/references/treelint-search-patterns.md"

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

echo "=============================================="
echo "  AC#4: Binary Unavailable Handling"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: File exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists"
else
    fail "Reference file does not exist"
    echo ""
    echo "=============================================="
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Exit code 127 documented (binary not found)
# FALLBACK-004: Must handle exit code 127
# -----------------------------------------------------------------------------
echo "--- Test 2: Exit Code 127 Documented ---"
if grep -qE '127' "$TARGET_FILE" 2>/dev/null; then
    pass "Exit code 127 (binary not found) documented"
else
    fail "Missing exit code 127 (binary not found) documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Exit code 126 documented (permission denied)
# FALLBACK-004: Must handle exit code 126
# -----------------------------------------------------------------------------
echo "--- Test 3: Exit Code 126 Documented ---"
if grep -qE '126' "$TARGET_FILE" 2>/dev/null; then
    pass "Exit code 126 (permission denied) documented"
else
    fail "Missing exit code 126 (permission denied) documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: "Binary Not Found" scenario explicitly documented
# Must have a section or paragraph covering binary unavailability
# -----------------------------------------------------------------------------
echo "--- Test 4: Binary Not Found Scenario ---"
if grep -qiE '(binary|command).*(not found|unavailable|missing)' "$TARGET_FILE" 2>/dev/null; then
    pass "Binary not found scenario documented"
else
    fail "Missing explicit binary not found scenario documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Grep fallback specified for binary unavailability
# When binary is missing, must fall back to Grep (not HALT)
# -----------------------------------------------------------------------------
echo "--- Test 5: Grep Fallback for Binary Unavailability ---"
# Check that the error handling section mentions Grep fallback
if grep -qiE '(not found|127|unavailable).*(Grep|fall.?back)' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(fall.?back|Grep).*(not found|127|unavailable)' "$TARGET_FILE" 2>/dev/null; then
    pass "Grep fallback documented for binary unavailability"
else
    fail "Missing Grep fallback for binary not found / exit code 127"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: No HALT or workflow termination on binary failure (BR-001)
# Fallback must never halt the workflow
# -----------------------------------------------------------------------------
echo "--- Test 6: No HALT on Binary Failure (BR-001) ---"
# Extract the error handling / binary not found section
error_section=$(grep -iA 5 -B 2 '(binary|not found|127|126)' "$TARGET_FILE" 2>/dev/null || echo "")

# Check that HALT is not mentioned as an action in this section
halt_in_section=$(echo "$error_section" | grep -ci 'HALT' 2>/dev/null || echo "0")
halt_in_section=$(echo "$halt_in_section" | tr -d '\r\n')

if [[ "$halt_in_section" -eq 0 ]]; then
    pass "No HALT instruction in binary failure handling (BR-001)"
else
    fail "Found ${halt_in_section} HALT reference(s) in binary failure handling (BR-001 violation)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Warning message for binary unavailable (not error)
# Must emit warning, not error, when binary is missing
# -----------------------------------------------------------------------------
echo "--- Test 7: Warning for Binary Unavailable ---"
if grep -qiE '(warning|warn).*(not found|binary|unavailable)' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(not found|binary|unavailable).*(warning|warn)' "$TARGET_FILE" 2>/dev/null; then
    pass "Warning message specified for binary unavailability"
else
    fail "Missing warning message for binary not found scenario"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
