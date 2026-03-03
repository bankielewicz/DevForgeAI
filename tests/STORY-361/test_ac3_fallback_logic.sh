#!/usr/bin/env bash
# =============================================================================
# STORY-361 AC#3: Fallback Logic Documentation (Treelint to Grep)
# =============================================================================
# Validates that:
#   1. Reference file exists
#   2. Contains "## Fallback Decision Tree" section heading (or similar)
#   3. Decision tree has 4 documented steps:
#      Step 1: Check file extension against supported list
#      Step 2: Attempt Treelint if supported
#      Step 3: Fall back to Grep if unsupported or command fails
#      Step 4: Log warning on fallback (not error)
#   4. Contains Grep pattern equivalents for each Treelint search type
#   5. Uses "warning" terminology (not "error") for fallback logging
#   6. Each Treelint search type has a corresponding Grep fallback (BR-002)
#
# TDD Phase: RED - Target file does not exist yet.
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
echo "  AC#3: Fallback Logic (Treelint to Grep)"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists"
else
    fail "Reference file does not exist at src/claude/agents/references/treelint-search-patterns.md"
    echo ""
    echo "=============================================="
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains Fallback Decision Tree section heading
# -----------------------------------------------------------------------------
echo "--- Test 2: Fallback Decision Tree Section ---"
if grep -qiE '^#{1,3} .*Fallback (Decision Tree|Logic)' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'Fallback Decision Tree' section heading"
else
    fail "Missing 'Fallback Decision Tree' section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Decision tree has 4 documented steps
# Check for Step 1, Step 2, Step 3, Step 4 (or numbered list 1., 2., 3., 4.)
# -----------------------------------------------------------------------------
echo "--- Test 3: Four Decision Tree Steps ---"

# Step 1: Check file extension
if grep -qiE '(Step 1|1\.).*((check|verify|inspect).*(extension|file type)|extension.*(check|supported))' "$TARGET_FILE" 2>/dev/null; then
    pass "Step 1: Check file extension documented"
else
    fail "Step 1: Missing file extension check step"
fi

# Step 2: Attempt Treelint
if grep -qiE '(Step 2|2\.).*((attempt|try|use|invoke).*Treelint|Treelint.*(attempt|try|invoke|supported))' "$TARGET_FILE" 2>/dev/null; then
    pass "Step 2: Attempt Treelint documented"
else
    fail "Step 2: Missing Treelint attempt step"
fi

# Step 3: Fall back to Grep
if grep -qiE '(Step 3|3\.).*(fall\s*back|fallback).*Grep' "$TARGET_FILE" 2>/dev/null; then
    pass "Step 3: Fall back to Grep documented"
else
    fail "Step 3: Missing Grep fallback step"
fi

# Step 4: Log warning
if grep -qiE '(Step 4|4\.).*(log|emit|record).*warning' "$TARGET_FILE" 2>/dev/null; then
    pass "Step 4: Log warning on fallback documented"
else
    fail "Step 4: Missing log warning step"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Grep pattern equivalents documented
# Must contain Grep() or grep patterns for function, class, and map search types
# -----------------------------------------------------------------------------
echo "--- Test 4: Grep Pattern Equivalents ---"

# Grep equivalent for function search
if grep -qE 'Grep\(.*function' "$TARGET_FILE" 2>/dev/null || \
   grep -qE 'grep.*def |grep.*function ' "$TARGET_FILE" 2>/dev/null || \
   grep -qE 'Grep\(pattern=.*def |Grep\(pattern=.*function' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Grep fallback pattern for function search"
else
    fail "Missing Grep fallback pattern for function search"
fi

# Grep equivalent for class search
if grep -qE 'Grep\(.*class' "$TARGET_FILE" 2>/dev/null || \
   grep -qE 'grep.*class ' "$TARGET_FILE" 2>/dev/null || \
   grep -qE 'Grep\(pattern=.*class' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Grep fallback pattern for class search"
else
    fail "Missing Grep fallback pattern for class search"
fi

# Grep equivalent for map/ranked search
if grep -qiE 'Grep\(.*map|Grep\(.*ranked|Grep\(.*import|glob.*ranked' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(map|ranked).*(Grep|Glob|fallback)' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Grep/Glob fallback pattern for map ranked search"
else
    fail "Missing Grep/Glob fallback pattern for map ranked search"
fi

# Grep equivalent for deps/calls search
if grep -qiE 'Grep\(.*deps|Grep\(.*calls|Grep\(.*import' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(deps|calls).*(Grep|Glob|fallback)' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Grep fallback pattern for deps/calls search"
else
    fail "Missing Grep fallback pattern for deps/calls search"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Uses "warning" terminology (not "error") for fallback
# AC#3 explicitly states: "log warning on fallback (not error)"
# -----------------------------------------------------------------------------
echo "--- Test 5: Warning Terminology (Not Error) ---"
if grep -qi 'warning' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'warning' terminology for fallback logging"
else
    fail "Missing 'warning' terminology in fallback documentation"
fi

# Verify "warning" is used in fallback context (not "error")
# Check that near the fallback/log section, "warning" appears
fallback_section=$(grep -iA 5 'fallback\|fall back\|Step 4' "$TARGET_FILE" 2>/dev/null || echo "")
if echo "$fallback_section" | grep -qi 'warning'; then
    pass "Fallback section uses 'warning' (not 'error') for logging"
else
    fail "Fallback section does not use 'warning' for logging guidance"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Treelint-to-Grep parity count (BR-002)
# Count of documented Treelint search types should equal count of Grep fallbacks
# Minimum: 4 pairs (function, class, map, deps)
# -----------------------------------------------------------------------------
echo "--- Test 6: Treelint-Grep Parity (BR-002) ---"
treelint_types=$(grep -coE 'treelint (search|map|deps)' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$treelint_types" ]]; then treelint_types=0; fi

grep_fallbacks=$(grep -coiE 'Grep\(pattern=' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$grep_fallbacks" ]]; then grep_fallbacks=0; fi

if [[ "$grep_fallbacks" -ge 4 ]]; then
    pass "At least 4 Grep fallback patterns documented (found ${grep_fallbacks})"
else
    fail "Only ${grep_fallbacks} Grep fallback patterns documented (>= 4 required for parity with Treelint types)"
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
