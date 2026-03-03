#!/usr/bin/env bash
# =============================================================================
# STORY-394 AC#4: Evaluation Results Stored in Structured Format
#
# Validates that devforgeai/specs/research/evaluation-results.md contains:
# - Summary table with columns: Agent | Wave | Before Score | After Score | Delta | Pass/Fail
# - Per-agent detail sections with dimension-level breakdown
# - Timestamps for each evaluation run
# - Rubric version identifier per evaluation
# - Markdown format consistent with devforgeai/specs/ conventions
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RESULTS_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-results.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

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
echo "STORY-394 AC#4: Results Format Validation Tests"
echo "Target: ${RESULTS_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
echo "--- Pre-Check: File Exists ---"
if [ ! -f "$RESULTS_FILE" ]; then
    echo "  FAIL: Results file does not exist at ${RESULTS_FILE}"
    echo ""
    echo "================================================================"
    echo "AC#4 Results: 0 passed, 1 failed out of 1 tests"
    echo "================================================================"
    exit 1
fi

# =============================================================================
# Test 1: Summary table exists with required columns
# =============================================================================
echo "--- Summary Table ---"

HAS_SUMMARY_TABLE=$(grep -ciE '(summary|overview)' "$RESULTS_FILE" || true)
run_test "Summary section exists" "$( [ "$HAS_SUMMARY_TABLE" -ge 1 ] && echo 0 || echo 1 )"

# Check for Markdown table header with required columns
HAS_AGENT_COL=$(grep -ci 'Agent' "$RESULTS_FILE" || true)
run_test "Agent column present in table" "$( [ "$HAS_AGENT_COL" -ge 1 ] && echo 0 || echo 1 )"

HAS_WAVE_COL=$(grep -ci 'Wave' "$RESULTS_FILE" || true)
run_test "Wave column present in table" "$( [ "$HAS_WAVE_COL" -ge 1 ] && echo 0 || echo 1 )"

HAS_BEFORE_COL=$(grep -ciE 'Before.*Score' "$RESULTS_FILE" || true)
run_test "Before Score column present in table" "$( [ "$HAS_BEFORE_COL" -ge 1 ] && echo 0 || echo 1 )"

HAS_AFTER_COL=$(grep -ciE 'After.*Score' "$RESULTS_FILE" || true)
run_test "After Score column present in table" "$( [ "$HAS_AFTER_COL" -ge 1 ] && echo 0 || echo 1 )"

HAS_DELTA_COL=$(grep -ci 'Delta' "$RESULTS_FILE" || true)
run_test "Delta column present in table" "$( [ "$HAS_DELTA_COL" -ge 1 ] && echo 0 || echo 1 )"

HAS_PASSFAIL_COL=$(grep -ciE 'Pass.*Fail' "$RESULTS_FILE" || true)
run_test "Pass/Fail column present in table" "$( [ "$HAS_PASSFAIL_COL" -ge 1 ] && echo 0 || echo 1 )"

# Check for actual Markdown table syntax (pipe-delimited)
HAS_TABLE_SYNTAX=$(grep -cE '^\|.*\|.*\|' "$RESULTS_FILE" || true)
run_test "Markdown table syntax present (pipe-delimited rows)" "$( [ "$HAS_TABLE_SYNTAX" -ge 2 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Per-agent detail section structure
# =============================================================================
echo ""
echo "--- Per-Agent Detail Sections ---"

HAS_DETAIL_SECTION=$(grep -ciE '(detail|per.agent|agent.*detail|dimension.*breakdown)' "$RESULTS_FILE" || true)
run_test "Per-agent detail section documented" "$( [ "$HAS_DETAIL_SECTION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Timestamp field documented in results template
# =============================================================================
echo ""
echo "--- Timestamps ---"

HAS_TIMESTAMP=$(grep -ciE '(timestamp|evaluated.*on|evaluation.*date|date.*evaluation)' "$RESULTS_FILE" || true)
run_test "Timestamp field present in results template" "$( [ "$HAS_TIMESTAMP" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Rubric version identifier in results
# =============================================================================
echo ""
echo "--- Rubric Version ---"

HAS_RUBRIC_VERSION=$(grep -ciE '(rubric.*version|version.*rubric|scored.*with.*version)' "$RESULTS_FILE" || true)
run_test "Rubric version identifier in results template" "$( [ "$HAS_RUBRIC_VERSION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: File is valid Markdown (has H1 title)
# =============================================================================
echo ""
echo "--- Markdown Format ---"

HAS_H1=$(grep -c '^# ' "$RESULTS_FILE" || true)
run_test "File has H1 title heading" "$( [ "$HAS_H1" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
