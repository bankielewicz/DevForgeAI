#!/usr/bin/env bash
# =============================================================================
# STORY-394 AC#1: Scoring Rubric Defined with Objective Quality Dimensions
#
# Validates that devforgeai/specs/research/evaluation-rubric.md contains:
# - 5+ independently scorable quality dimensions
# - 1-5 numeric scale with descriptors for scores 1, 3, and 5
# - Concrete examples per score level
# - Weighting factors summing to 100%
# - Agent-agnostic language (no hardcoded agent names in rubric)
# - Rubric version identifier
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RUBRIC_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-rubric.md"

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
echo "STORY-394 AC#1: Scoring Rubric Validation Tests"
echo "Target: ${RUBRIC_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
echo "--- Pre-Check: File Exists ---"
if [ ! -f "$RUBRIC_FILE" ]; then
    echo "  FAIL: Rubric file does not exist at ${RUBRIC_FILE}"
    echo ""
    echo "================================================================"
    echo "AC#1 Results: 0 passed, 1 failed out of 1 tests"
    echo "================================================================"
    exit 1
fi

# =============================================================================
# Test 1: File contains at least 5 quality dimension headings
# Dimensions are expected as H2 or H3 sections (e.g., "## Task Completion Accuracy")
# =============================================================================
echo "--- Dimension Count ---"

DIMENSION_COUNT=$(grep -cE '^#{2,3}\s+.*' "$RUBRIC_FILE" || true)
run_test "Rubric contains at least 5 dimension headings (found: ${DIMENSION_COUNT})" "$( [ "$DIMENSION_COUNT" -ge 5 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Each dimension has score descriptors for 1, 3, and 5
# Look for score level markers like "Score 1:", "Score 3:", "Score 5:" or "| 1 |", "| 3 |", "| 5 |"
# =============================================================================
echo ""
echo "--- Score Descriptors ---"

SCORE_1_COUNT=$(grep -ciE '(Score\s*1[:\s]|\|\s*1\s*\|)' "$RUBRIC_FILE" || true)
run_test "Score level 1 descriptors present (found: ${SCORE_1_COUNT})" "$( [ "$SCORE_1_COUNT" -ge 5 ] && echo 0 || echo 1 )"

SCORE_3_COUNT=$(grep -ciE '(Score\s*3[:\s]|\|\s*3\s*\|)' "$RUBRIC_FILE" || true)
run_test "Score level 3 descriptors present (found: ${SCORE_3_COUNT})" "$( [ "$SCORE_3_COUNT" -ge 5 ] && echo 0 || echo 1 )"

SCORE_5_COUNT=$(grep -ciE '(Score\s*5[:\s]|\|\s*5\s*\|)' "$RUBRIC_FILE" || true)
run_test "Score level 5 descriptors present (found: ${SCORE_5_COUNT})" "$( [ "$SCORE_5_COUNT" -ge 5 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Concrete examples present per dimension
# Look for "Example:" or "example" markers near score levels
# =============================================================================
echo ""
echo "--- Concrete Examples ---"

EXAMPLE_COUNT=$(grep -ciE '(example|e\.g\.|for instance)' "$RUBRIC_FILE" || true)
run_test "At least 5 concrete examples in rubric (found: ${EXAMPLE_COUNT})" "$( [ "$EXAMPLE_COUNT" -ge 5 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Weighting factors present and sum to 100%
# Look for weight/percentage markers like "Weight: 25%" or "| 25% |"
# =============================================================================
echo ""
echo "--- Weighting Factors ---"

WEIGHT_COUNT=$(grep -ciE '(weight|%\s)' "$RUBRIC_FILE" || true)
run_test "Weight references present in rubric (found: ${WEIGHT_COUNT})" "$( [ "$WEIGHT_COUNT" -ge 5 ] && echo 0 || echo 1 )"

# Extract numeric weight values and sum them
# Pattern: match NN% where NN is 1-100
WEIGHT_SUM=$(grep -oE '[0-9]+%' "$RUBRIC_FILE" | grep -oE '[0-9]+' | awk '{sum += $1} END {print sum+0}')
run_test "Weights sum to 100% (actual sum: ${WEIGHT_SUM}%)" "$( [ "$WEIGHT_SUM" -ge 99 ] && [ "$WEIGHT_SUM" -le 101 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Rubric is agent-agnostic (no hardcoded pilot agent names in scoring sections)
# Should NOT contain specific agent names like "test-automator" in rubric dimensions
# =============================================================================
echo ""
echo "--- Agent-Agnostic Check ---"

HARDCODED_AGENTS=$(grep -ciE '(test-automator|backend-architect|code-reviewer|requirements-analyst)' "$RUBRIC_FILE" || true)
run_test "No hardcoded agent names in rubric (found: ${HARDCODED_AGENTS})" "$( [ "$HARDCODED_AGENTS" -eq 0 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Rubric version identifier present
# =============================================================================
echo ""
echo "--- Rubric Version ---"

HAS_VERSION=$(grep -ciE '(Rubric Version|version:\s*[0-9])' "$RUBRIC_FILE" || true)
run_test "Rubric version identifier present" "$( [ "$HAS_VERSION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 7: 1-5 numeric scale explicitly documented
# =============================================================================
echo ""
echo "--- Numeric Scale ---"

HAS_SCALE=$(grep -ciE '(1-5|1 to 5|scale.*[1-5]|scoring scale)' "$RUBRIC_FILE" || true)
run_test "1-5 numeric scale documented" "$( [ "$HAS_SCALE" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
