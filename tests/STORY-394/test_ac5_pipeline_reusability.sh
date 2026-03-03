#!/usr/bin/env bash
# =============================================================================
# STORY-394 AC#5: Pipeline Reusability Across Migration Waves
#
# Validates that the pipeline and rubric support reuse across waves:
# - Agent name used as parameter (not hardcoded)
# - Evaluation prompts categorizable by agent role type
# - Results accumulate with wave/sprint identifiers
# - Rubric dimensions apply equally to all agent types
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PIPELINE_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-pipeline.md"
RUBRIC_FILE="${PROJECT_ROOT}/devforgeai/specs/research/evaluation-rubric.md"
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
echo "STORY-394 AC#5: Pipeline Reusability Tests"
echo "Target: ${PIPELINE_FILE}, ${RUBRIC_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: Files exist ---
echo "--- Pre-Check: Files Exist ---"
MISSING=0
for FILE in "$PIPELINE_FILE" "$RUBRIC_FILE"; do
    if [ ! -f "$FILE" ]; then
        echo "  FAIL: File does not exist: ${FILE}"
        MISSING=1
    fi
done
if [ "$MISSING" -eq 1 ]; then
    echo ""
    echo "================================================================"
    echo "AC#5 Results: 0 passed, 1 failed out of 1 tests"
    echo "================================================================"
    exit 1
fi

# =============================================================================
# Test 1: Agent name parameterized in pipeline process steps
# Should use {agent_name} or similar placeholder, not hardcoded names
# =============================================================================
echo "--- Parameterized Agent Name ---"

PARAM_COUNT=$(grep -cE '(\{agent_name\}|\{agent\}|\[agent.name\]|<agent.name>|AGENT_NAME)' "$PIPELINE_FILE" || true)
run_test "Pipeline uses parameterized agent name (found: ${PARAM_COUNT})" "$( [ "$PARAM_COUNT" -ge 3 ] && echo 0 || echo 1 )"

# Verify no hardcoded pilot agent names in process steps
# (References in examples section are OK, but process steps should be generic)
HARDCODED_IN_STEPS=$(grep -ciE '(test-automator|backend-architect|requirements-analyst)' "$PIPELINE_FILE" || true)
# Allow some references (in examples) but not excessive hardcoding
run_test "Pipeline process steps not excessively hardcoded (found: ${HARDCODED_IN_STEPS})" "$( [ "$HARDCODED_IN_STEPS" -le 5 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Agent role type categories for evaluation prompts
# Should define categories like validator, implementor, reviewer, etc.
# =============================================================================
echo ""
echo "--- Role-Type Categories ---"

ROLE_TYPES=$(grep -ciE '(role.type|agent.type|agent.role|validator|implementor|reviewer|analyzer)' "$PIPELINE_FILE" || true)
run_test "Agent role type categories documented (found: ${ROLE_TYPES})" "$( [ "$ROLE_TYPES" -ge 4 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Wave/sprint identifiers in results format
# =============================================================================
echo ""
echo "--- Wave/Sprint Identifiers ---"

if [ -f "$RESULTS_FILE" ]; then
    HAS_WAVE=$(grep -ciE '(wave|sprint)' "$RESULTS_FILE" || true)
    run_test "Wave/sprint identifiers in results file (found: ${HAS_WAVE})" "$( [ "$HAS_WAVE" -ge 1 ] && echo 0 || echo 1 )"
else
    run_test "Results file exists for wave identifier check" "1"
fi

# Also check pipeline documents accumulation
HAS_ACCUMULATE=$(grep -ciE '(accumulat|append|add.*results|results.*grow)' "$PIPELINE_FILE" || true)
run_test "Pipeline documents results accumulation across waves" "$( [ "$HAS_ACCUMULATE" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Rubric dimensions are universally applicable
# No dimension should reference specific agent types
# =============================================================================
echo ""
echo "--- Universal Rubric Dimensions ---"

RUBRIC_HARDCODED=$(grep -ciE '(only.*validator|only.*implementor|specific.*agent)' "$RUBRIC_FILE" || true)
run_test "Rubric dimensions are universally applicable (no agent-specific restrictions)" "$( [ "$RUBRIC_HARDCODED" -eq 0 ] && echo 0 || echo 1 )"

# Check rubric explicitly states universality
HAS_UNIVERSAL=$(grep -ciE '(all agent|any agent|agent.agnostic|universal|applicable.*across)' "$RUBRIC_FILE" || true)
run_test "Rubric states universal applicability" "$( [ "$HAS_UNIVERSAL" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Pipeline documents prompt reuse across same-type agents
# =============================================================================
echo ""
echo "--- Prompt Reuse ---"

HAS_REUSE=$(grep -ciE '(reuse|reusab|shared.*prompt|prompt.*shared|same.*type)' "$PIPELINE_FILE" || true)
run_test "Pipeline documents prompt reuse for same-type agents" "$( [ "$HAS_REUSE" -ge 1 ] && echo 0 || echo 1 )"

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
