#!/usr/bin/env bash
# =============================================================================
# STORY-362 AC#3: Warning Message on Fallback (Not Error)
# =============================================================================
# Validates that treelint-search-patterns.md:
#   1. Specifies warning-level messages for all fallback events
#   2. Uses "Treelint fallback:" prefix format in warning templates
#   3. Contains ZERO instances of "error" or "ERROR" in warning message templates
#   4. Explicitly states fallback is NOT an error (workflow continues)
#   5. Warning messages include the reason for fallback (BR-005)
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
echo "  AC#3: Warning Message (Not Error)"
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
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Warning-level terminology present
# Must contain the word "warning" in context of fallback
# -----------------------------------------------------------------------------
echo "--- Test 2: Warning Terminology Present ---"
if grep -qi 'warning' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'warning' terminology"
else
    fail "Missing 'warning' terminology in fallback documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: "Treelint fallback:" prefix in warning message format
# AC#3 specifies format like: "Treelint fallback: .cs files not supported, using Grep"
# -----------------------------------------------------------------------------
echo "--- Test 3: Warning Message Prefix Format ---"
if grep -qiE 'Treelint fallback:' "$TARGET_FILE" 2>/dev/null; then
    pass "Warning message uses 'Treelint fallback:' prefix format"
else
    fail "Missing 'Treelint fallback:' prefix in warning message templates"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Warning messages do NOT contain "error" or "ERROR" (BR-005)
# Extract lines near "Treelint fallback:" and "Warning:" to check for "error"
# This specifically checks the warning MESSAGE TEMPLATES, not the entire file
# (The file may legitimately mention "error" in other contexts like section headers)
# -----------------------------------------------------------------------------
echo "--- Test 4: Zero 'error' in Warning Templates (BR-005) ---"
# Extract warning message template lines (lines containing "Treelint fallback:" or "Warning:")
warning_lines=$(grep -iE '(Treelint fallback:|Warning:.*fallback|Display:.*warning|"Warning)' "$TARGET_FILE" 2>/dev/null || echo "")

if [[ -n "$warning_lines" ]]; then
    error_in_warnings=$(echo "$warning_lines" | grep -ci 'error' 2>/dev/null || echo "0")
    error_in_warnings=$(echo "$error_in_warnings" | tr -d '\r\n')
    if [[ "$error_in_warnings" -eq 0 ]]; then
        pass "Warning templates contain zero instances of 'error' (BR-005)"
    else
        fail "Found ${error_in_warnings} instance(s) of 'error' in warning templates (BR-005 violation)"
    fi
else
    fail "No warning message templates found to validate"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Explicitly states fallback is NOT an error
# Must contain language like "not error", "not an error", "Do NOT treat as error"
# -----------------------------------------------------------------------------
echo "--- Test 5: Explicit 'Not Error' Statement ---"
if grep -qiE '(not.*(an )?error|do not.*(treat|mark|classify).*error|warning.*(not|never).*error)' "$TARGET_FILE" 2>/dev/null; then
    pass "Explicitly states fallback is not an error"
else
    fail "Missing explicit statement that fallback is not an error"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Warning includes reason for fallback
# Templates should include reason placeholder (e.g., "for {reason}", "unsupported")
# -----------------------------------------------------------------------------
echo "--- Test 6: Warning Includes Fallback Reason ---"
if grep -qiE '(Treelint fallback:.*reason|warning.*reason|{reason}|unsupported|not supported|not found|unavailable)' "$TARGET_FILE" 2>/dev/null; then
    pass "Warning messages include reason for fallback"
else
    fail "Warning messages do not include a reason for fallback"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
