#!/usr/bin/env bash
# =============================================================================
# STORY-360 AC#4: Last Updated Dates Updated in Modified Files Only
# =============================================================================
# Validates that:
#   - source-tree.md and anti-patterns.md show Last Updated dates
#     equal to or later than their predecessor story completion dates
#   - The 4 unmodified files retain their original dates:
#     * tech-stack.md: 2026-01-31
#     * dependencies.md: 2026-02-02
#     * coding-standards.md: 2026-01-19
#     * architecture-constraints.md: 2025-10-30
#
# TDD Phase: RED - These tests define expected date constraints.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"

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

# Extract Last Updated date from a context file's first 10 lines
# Returns: date string like "2026-02-05" or "NOT_FOUND"
extract_date() {
    local filepath="${CONTEXT_DIR}/$1"
    local date_line
    date_line=$(head -n 10 "$filepath" 2>/dev/null | grep -E '^\*\*Last Updated\*\*:' || echo "")

    if [[ -z "$date_line" ]]; then
        echo "NOT_FOUND"
        return
    fi

    local date_val
    date_val=$(echo "$date_line" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)

    if [[ -z "$date_val" ]]; then
        echo "PARSE_ERROR"
    else
        echo "$date_val"
    fi
}

# Compare dates: returns 0 if $1 >= $2 (both in YYYY-MM-DD format)
date_gte() {
    # Simple string comparison works for YYYY-MM-DD format
    [[ "$1" > "$2" ]] || [[ "$1" == "$2" ]]
}

echo "=============================================="
echo "  AC#4: Last Updated Dates - Modified & Unmodified Files"
echo "=============================================="
echo ""

# Baseline date: STORY-357/358/359 were completed around 2026-02-04/05
# Modified files should have dates >= 2026-02-04
EPIC_COMPLETION_BASELINE="2026-02-04"

# -----------------------------------------------------------------------------
# Test 1: source-tree.md Last Updated date is >= baseline
# (Modified by STORY-357 and STORY-358)
# -----------------------------------------------------------------------------
echo "--- Test 1: source-tree.md Date Updated ---"
st_date=$(extract_date "source-tree.md")
echo "  Detected date: ${st_date}"

if [[ "$st_date" == "NOT_FOUND" || "$st_date" == "PARSE_ERROR" ]]; then
    fail "source-tree.md Last Updated date could not be extracted"
elif date_gte "$st_date" "$EPIC_COMPLETION_BASELINE"; then
    pass "source-tree.md date ${st_date} >= ${EPIC_COMPLETION_BASELINE}"
else
    fail "source-tree.md date ${st_date} < ${EPIC_COMPLETION_BASELINE} (should be updated after STORY-357/358)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: anti-patterns.md Last Updated date is >= baseline
# (Modified by STORY-359)
# -----------------------------------------------------------------------------
echo "--- Test 2: anti-patterns.md Date Updated ---"
ap_date=$(extract_date "anti-patterns.md")
echo "  Detected date: ${ap_date}"

if [[ "$ap_date" == "NOT_FOUND" || "$ap_date" == "PARSE_ERROR" ]]; then
    fail "anti-patterns.md Last Updated date could not be extracted"
elif date_gte "$ap_date" "$EPIC_COMPLETION_BASELINE"; then
    pass "anti-patterns.md date ${ap_date} >= ${EPIC_COMPLETION_BASELINE}"
else
    fail "anti-patterns.md date ${ap_date} < ${EPIC_COMPLETION_BASELINE} (should be updated after STORY-359)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: tech-stack.md retains original date 2026-01-31 (unmodified)
# -----------------------------------------------------------------------------
echo "--- Test 3: tech-stack.md Date Unchanged ---"
ts_date=$(extract_date "tech-stack.md")
echo "  Detected date: ${ts_date}"

if [[ "$ts_date" == "2026-01-31" ]]; then
    pass "tech-stack.md date is 2026-01-31 (unchanged)"
else
    fail "tech-stack.md date is ${ts_date}, expected 2026-01-31 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: dependencies.md retains original date 2026-02-02 (unmodified)
# -----------------------------------------------------------------------------
echo "--- Test 4: dependencies.md Date Unchanged ---"
dep_date=$(extract_date "dependencies.md")
echo "  Detected date: ${dep_date}"

if [[ "$dep_date" == "2026-02-02" ]]; then
    pass "dependencies.md date is 2026-02-02 (unchanged)"
else
    fail "dependencies.md date is ${dep_date}, expected 2026-02-02 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: coding-standards.md retains original date 2026-01-19 (unmodified)
# -----------------------------------------------------------------------------
echo "--- Test 5: coding-standards.md Date Unchanged ---"
cs_date=$(extract_date "coding-standards.md")
echo "  Detected date: ${cs_date}"

if [[ "$cs_date" == "2026-01-19" ]]; then
    pass "coding-standards.md date is 2026-01-19 (unchanged)"
else
    fail "coding-standards.md date is ${cs_date}, expected 2026-01-19 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: architecture-constraints.md retains original date 2025-10-30 (unmodified)
# -----------------------------------------------------------------------------
echo "--- Test 6: architecture-constraints.md Date Unchanged ---"
ac_date=$(extract_date "architecture-constraints.md")
echo "  Detected date: ${ac_date}"

if [[ "$ac_date" == "2025-10-30" ]]; then
    pass "architecture-constraints.md date is 2025-10-30 (unchanged)"
else
    fail "architecture-constraints.md date is ${ac_date}, expected 2025-10-30 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Modified files have dates NEWER than unmodified files
# This confirms the modified files were actually updated.
# -----------------------------------------------------------------------------
echo "--- Test 7: Modified Files Newer Than Unmodified ---"
if [[ "$st_date" != "NOT_FOUND" && "$st_date" != "PARSE_ERROR" && "$ts_date" != "NOT_FOUND" ]]; then
    if date_gte "$st_date" "$ts_date"; then
        pass "source-tree.md date (${st_date}) >= tech-stack.md date (${ts_date})"
    else
        fail "source-tree.md date (${st_date}) < tech-stack.md date (${ts_date}) - modified file should be newer"
    fi
else
    fail "Could not compare dates for modified vs unmodified files"
fi

if [[ "$ap_date" != "NOT_FOUND" && "$ap_date" != "PARSE_ERROR" && "$ac_date" != "NOT_FOUND" ]]; then
    if date_gte "$ap_date" "$ac_date"; then
        pass "anti-patterns.md date (${ap_date}) >= architecture-constraints.md date (${ac_date})"
    else
        fail "anti-patterns.md date (${ap_date}) < architecture-constraints.md date (${ac_date}) - modified file should be newer"
    fi
else
    fail "Could not compare dates for modified vs unmodified files"
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
