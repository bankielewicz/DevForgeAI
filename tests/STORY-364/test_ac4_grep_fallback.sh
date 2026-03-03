#!/usr/bin/env bash
# =============================================================================
# STORY-364 AC#4: Automatic Grep Fallback for Unsupported Languages
# =============================================================================
# Validates that the reference file contains:
#   1. Supported file extension list (.py, .ts, .tsx, .js, .jsx, .rs, .md)
#   2. Grep fallback instructions for unsupported languages
#   3. Extension check before Treelint invocation
#   4. Warning-level messaging (not error/HALT) on fallback
#   5. Mentions unsupported languages (C#, Java, Go)
#   6. Equivalent output regardless of detection method
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer/references/treelint-review-patterns.md"

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
echo "  AC#4: Grep Fallback for Unsupported Languages"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Reference file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$REFERENCE_FILE" ]]; then
    pass "treelint-review-patterns.md exists and is readable"
else
    fail "treelint-review-patterns.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains supported extension list
# Must list all 7 supported extensions: .py, .ts, .tsx, .js, .jsx, .rs, .md
# -----------------------------------------------------------------------------
echo "--- Test 2: Supported Extension List ---"
ext_count=0

if grep -q '\.py' "$REFERENCE_FILE" 2>/dev/null; then ext_count=$((ext_count + 1)); fi
if grep -q '\.ts' "$REFERENCE_FILE" 2>/dev/null; then ext_count=$((ext_count + 1)); fi
if grep -q '\.tsx' "$REFERENCE_FILE" 2>/dev/null; then ext_count=$((ext_count + 1)); fi
if grep -qE '\.js[^x]|\.js$|\.js[^a-zA-Z]' "$REFERENCE_FILE" 2>/dev/null; then ext_count=$((ext_count + 1)); fi
if grep -q '\.jsx' "$REFERENCE_FILE" 2>/dev/null; then ext_count=$((ext_count + 1)); fi
if grep -q '\.rs' "$REFERENCE_FILE" 2>/dev/null; then ext_count=$((ext_count + 1)); fi
if grep -q '\.md' "$REFERENCE_FILE" 2>/dev/null; then ext_count=$((ext_count + 1)); fi

if [[ "$ext_count" -ge 5 ]]; then
    pass "Lists ${ext_count}/7 supported extensions (.py, .ts, .tsx, .js, .jsx, .rs, .md)"
else
    fail "Only ${ext_count}/7 supported extensions found (need .py, .ts, .tsx, .js, .jsx, .rs, .md)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains Grep fallback instructions
# Must have Grep-based pattern detection for unsupported files
# -----------------------------------------------------------------------------
echo "--- Test 3: Grep Fallback Instructions ---"
if grep -qiE '(fallback|Grep.*fallback|fallback.*Grep|grep.*pattern|text.*pattern)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains Grep fallback instructions"
else
    fail "Missing Grep fallback instructions for unsupported languages"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Documents extension check before Treelint invocation
# Must instruct checking file extensions before calling Treelint
# -----------------------------------------------------------------------------
echo "--- Test 4: Extension Check Documentation ---"
if grep -qiE '(check.*extension|extension.*check|supported.*file|file.*support|before.*invok)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents extension check before Treelint invocation"
else
    fail "Missing documentation for checking extensions before Treelint invocation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Warning-level messaging (not error/HALT)
# Fallback must log warning, not halt the review
# -----------------------------------------------------------------------------
echo "--- Test 5: Warning-Level Messaging ---"
if grep -qiE 'warning' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains warning-level messaging for fallback"
else
    fail "Missing warning-level messaging (fallback must use warning, not error/HALT)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Mentions unsupported languages (C#, Java, Go)
# Must acknowledge that some languages are unsupported by Treelint
# -----------------------------------------------------------------------------
echo "--- Test 6: Unsupported Languages Mentioned ---"
unsupported_count=0
if grep -qiE '(C#|csharp|\.cs)' "$REFERENCE_FILE" 2>/dev/null; then unsupported_count=$((unsupported_count + 1)); fi
if grep -qiE '(Java|\.java)' "$REFERENCE_FILE" 2>/dev/null; then unsupported_count=$((unsupported_count + 1)); fi
if grep -qiE '(Go|\.go|golang)' "$REFERENCE_FILE" 2>/dev/null; then unsupported_count=$((unsupported_count + 1)); fi

if [[ "$unsupported_count" -ge 2 ]]; then
    pass "Mentions ${unsupported_count}/3 unsupported languages (C#, Java, Go)"
else
    fail "Only ${unsupported_count}/3 unsupported languages mentioned (need C#, Java, Go)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Equivalent output regardless of detection method
# Must document that review findings are reported consistently
# regardless of whether Treelint or Grep was used
# -----------------------------------------------------------------------------
echo "--- Test 7: Equivalent Output Documentation ---"
if grep -qiE '(equivalent|consistent|regardless|same.*output|unified.*report|combined)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents equivalent output regardless of detection method"
else
    fail "Missing documentation for equivalent output between Treelint and Grep methods"
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
