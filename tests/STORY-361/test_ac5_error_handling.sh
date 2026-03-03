#!/usr/bin/env bash
# =============================================================================
# STORY-361 AC#5: Error Handling Patterns for Treelint Failures
# =============================================================================
# Validates that:
#   1. Reference file exists
#   2. Contains "## Error Handling" section heading (or similar)
#   3. Documents 4+ failure scenarios:
#      a. Binary not found (exit code 127)
#      b. Version too old (missing --format json)
#      c. Empty results (valid query, no matches)
#      d. Malformed JSON (parse error)
#   4. Each scenario has:
#      - Detection method
#      - Example error output
#      - Recommended response / recovery action
#      - Whether to fall back to Grep or report error
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
echo "  AC#5: Error Handling Patterns"
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
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains Error Handling section heading
# -----------------------------------------------------------------------------
echo "--- Test 2: Error Handling Section ---"
if grep -qiE '^#{1,3} .*Error Handling' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'Error Handling' section heading"
else
    fail "Missing 'Error Handling' section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Scenario 1 - Binary not found (exit code 127)
# Must document the case where treelint binary is not installed
# -----------------------------------------------------------------------------
echo "--- Test 3: Scenario 1 - Binary Not Found ---"
if grep -qiE '(binary|command).*not found' "$TARGET_FILE" 2>/dev/null || \
   grep -qi 'not found' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents 'binary not found' scenario"
else
    fail "Missing 'binary not found' failure scenario"
fi

if grep -q '127' "$TARGET_FILE" 2>/dev/null; then
    pass "References exit code 127"
else
    fail "Missing exit code 127 reference for binary not found"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Scenario 2 - Version too old (missing --format json)
# Must document version incompatibility
# -----------------------------------------------------------------------------
echo "--- Test 4: Scenario 2 - Version Too Old ---"
if grep -qiE '(version|too old|outdated|incompatible)' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents version compatibility scenario"
else
    fail "Missing version too old / incompatible failure scenario"
fi

if grep -qiE '(--format json|format.*json).*(missing|unsupported|not.*supported|unavailable)' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(missing|unsupported|unavailable).*(--format json|format.*json)' "$TARGET_FILE" 2>/dev/null; then
    pass "References --format json being missing/unsupported in old versions"
else
    fail "Missing reference to --format json unavailability in old versions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Scenario 3 - Empty results (valid query, no matches)
# Must document handling of zero-match queries
# -----------------------------------------------------------------------------
echo "--- Test 5: Scenario 3 - Empty Results ---"
if grep -qiE '(empty|no (match|result)|zero result)' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents empty results / no matches scenario"
else
    fail "Missing empty results failure scenario"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Scenario 4 - Malformed JSON (parse error)
# Must document handling of invalid JSON output
# -----------------------------------------------------------------------------
echo "--- Test 6: Scenario 4 - Malformed JSON ---"
if grep -qiE '(malformed|invalid|corrupt|broken).*JSON' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE 'JSON.*(malformed|invalid|corrupt|parse.*error|broken)' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents malformed JSON / parse error scenario"
else
    fail "Missing malformed JSON failure scenario"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: At least 4 distinct error scenario subsections
# Count subsection headings within or after the Error Handling section
# -----------------------------------------------------------------------------
echo "--- Test 7: Minimum 4 Error Scenario Subsections ---"
# Count headings that appear after "Error Handling" heading and look like error scenarios
# These could be ### subsections or numbered entries
error_subsection_count=$(grep -ciE '(binary not found|version too old|empty result|malformed JSON|parse error|command not found|no match|outdated version)' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$error_subsection_count" ]]; then error_subsection_count=0; fi

if [[ "$error_subsection_count" -ge 4 ]]; then
    pass "At least 4 error scenario references found (${error_subsection_count})"
else
    fail "Only ${error_subsection_count} error scenario references found (>= 4 required)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Each scenario has detection method
# Look for "Detection" or "Detect" labels in the error handling section
# -----------------------------------------------------------------------------
echo "--- Test 8: Detection Methods ---"
detection_count=$(grep -ciE '(detection|detect|how to identify|check for|exit.code)' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$detection_count" ]]; then detection_count=0; fi

if [[ "$detection_count" -ge 4 ]]; then
    pass "Contains ${detection_count} detection method references (>= 4 required)"
else
    fail "Only ${detection_count} detection method references found (>= 4 required, one per scenario)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 9: Each scenario has recovery/response action
# Look for "Recovery", "Response", "Action", or "Recommendation" labels
# -----------------------------------------------------------------------------
echo "--- Test 9: Recovery Actions ---"
recovery_count=$(grep -ciE '(recovery|response|action|recommendation|fall\s*back|fallback|remedy)' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$recovery_count" ]]; then recovery_count=0; fi

if [[ "$recovery_count" -ge 4 ]]; then
    pass "Contains ${recovery_count} recovery/response action references (>= 4 required)"
else
    fail "Only ${recovery_count} recovery/response action references found (>= 4 required, one per scenario)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 10: Grep fallback decision documented per scenario
# Some scenarios should fall back to Grep, others should report error
# Check that fallback vs. error distinction exists
# -----------------------------------------------------------------------------
echo "--- Test 10: Fallback vs Error Decision ---"
if grep -qiE '(fall\s*back to Grep|use Grep|Grep fallback)' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents when to fall back to Grep on error"
else
    fail "Missing documentation of when to fall back to Grep on error"
fi

if grep -qiE '(report error|raise error|log error|do not fall\s*back|cannot fall\s*back)' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(error.*report|halt|abort)' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents when to report error instead of falling back"
else
    fail "Missing documentation of when to report error (not all scenarios should fallback)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
