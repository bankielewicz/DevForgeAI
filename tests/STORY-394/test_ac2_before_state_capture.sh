#!/usr/bin/env bash
# =============================================================================
# STORY-394 AC#2: Before-State Capture Mechanism
#
# Validates that the evaluation pipeline documents a before-state capture
# process containing:
# - Agent name and file path capture
# - Capture timestamp
# - 3+ standardized evaluation prompts per agent
# - Rubric scores for each output
# - Process works for ANY agent (parameterized, not hardcoded)
# - Results stored in evaluation-results.md
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PIPELINE_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-pipeline.md"
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
echo "STORY-394 AC#2: Before-State Capture Mechanism Tests"
echo "Target: ${PIPELINE_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: Pipeline file exists ---
echo "--- Pre-Check: Files Exist ---"
if [ ! -f "$PIPELINE_FILE" ]; then
    echo "  FAIL: Pipeline file does not exist at ${PIPELINE_FILE}"
    echo ""
    echo "================================================================"
    echo "AC#2 Results: 0 passed, 1 failed out of 1 tests"
    echo "================================================================"
    exit 1
fi

# =============================================================================
# Test 1: Before-state capture section exists in pipeline
# =============================================================================
echo "--- Before-State Capture Section ---"

HAS_BEFORE_SECTION=$(grep -ciE '(before.state|before state|capture.*before|pre.migration)' "$PIPELINE_FILE" || true)
run_test "Before-state capture section documented" "$( [ "$HAS_BEFORE_SECTION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Agent name and file path capture documented
# =============================================================================
echo ""
echo "--- Agent Name and Path ---"

HAS_AGENT_NAME=$(grep -ciE '(agent.name|agent name|file.path|file path)' "$PIPELINE_FILE" || true)
run_test "Agent name and file path capture documented (found: ${HAS_AGENT_NAME})" "$( [ "$HAS_AGENT_NAME" -ge 2 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Timestamp capture documented
# =============================================================================
echo ""
echo "--- Timestamp ---"

HAS_TIMESTAMP=$(grep -ciE '(timestamp|date.*capture|capture.*date|ISO.8601)' "$PIPELINE_FILE" || true)
run_test "Timestamp capture documented" "$( [ "$HAS_TIMESTAMP" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Evaluation prompts requirement (3+ per agent)
# =============================================================================
echo ""
echo "--- Evaluation Prompts ---"

HAS_EVAL_PROMPTS=$(grep -ciE '(evaluation prompt|eval prompt|test prompt|standardized prompt)' "$PIPELINE_FILE" || true)
run_test "Evaluation prompts referenced in pipeline" "$( [ "$HAS_EVAL_PROMPTS" -ge 1 ] && echo 0 || echo 1 )"

HAS_MIN_3=$(grep -ciE '(3\+|at least 3|minimum.*3|three.*prompt)' "$PIPELINE_FILE" || true)
run_test "Minimum 3 prompts per agent specified" "$( [ "$HAS_MIN_3" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Rubric scoring for each output documented
# =============================================================================
echo ""
echo "--- Rubric Scoring ---"

HAS_SCORING=$(grep -ciE '(rubric.scor|score.*rubric|scoring.*output|dimension.*score)' "$PIPELINE_FILE" || true)
run_test "Rubric scoring process documented" "$( [ "$HAS_SCORING" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Parameterized agent name (not hardcoded)
# Pipeline should use {agent_name} or similar placeholder
# =============================================================================
echo ""
echo "--- Parameterization ---"

HAS_PARAM=$(grep -cE '(\{agent_name\}|\{agent\}|\[agent.name\]|<agent.name>|AGENT_NAME)' "$PIPELINE_FILE" || true)
run_test "Agent name parameterized with placeholder (found: ${HAS_PARAM})" "$( [ "$HAS_PARAM" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 7: Results storage location referenced
# =============================================================================
echo ""
echo "--- Results Storage ---"

HAS_RESULTS_REF=$(grep -c 'evaluation-results.md' "$PIPELINE_FILE" || true)
run_test "Pipeline references evaluation-results.md for storage" "$( [ "$HAS_RESULTS_REF" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 8: Results file exists (template initialized)
# =============================================================================
echo ""
echo "--- Results File ---"

if [ -f "$RESULTS_FILE" ]; then
    run_test "evaluation-results.md file exists" "0"
else
    run_test "evaluation-results.md file exists" "1"
fi

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
