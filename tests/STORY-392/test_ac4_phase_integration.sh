#!/usr/bin/env bash
# =============================================================================
# STORY-392 AC#4: No Regression in Phase 4.5/5.5 Workflow Integration
#
# Verifies the updated src/claude/agents/ac-compliance-verifier.md:
# 1. Accepts standard invocation parameters (story_id, phase number)
# 2. Returns structured JSON with observations_for_persistence
# 3. Correctly identifies invocation phase (4.5 or 5.5) in metadata
# 4. Completes within existing time budget
# 5. Orchestrator can persist observations without format changes
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

# --- Test Helper ---
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
echo "STORY-392 AC#4: Phase 4.5/5.5 Workflow Integration Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Test 1: Accepts standard invocation parameters (story_id, phase number)
# =============================================================================
echo "--- Standard Invocation Parameters ---"

# Input/Output Specification section must exist
HAS_IO_SPEC=$(grep -c '^## Input/Output Specification' "$AGENT_FILE" || true)
run_test "Input/Output Specification section exists" "$( [ "$HAS_IO_SPEC" -ge 1 ] && echo 0 || echo 1 )"

# Must accept story_id parameter
HAS_STORY_ID_PARAM=$(grep -ci 'story_id\|story.id\|STORY.ID' "$AGENT_FILE" || true)
run_test "Accepts story_id parameter (found: ${HAS_STORY_ID_PARAM})" "$( [ "$HAS_STORY_ID_PARAM" -ge 1 ] && echo 0 || echo 1 )"

# Must accept phase number parameter
HAS_PHASE_PARAM=$(grep -ci 'phase.*number\|phase_number\|PHASE_NUMBER\|phase.*4\.5\|phase.*5\.5' "$AGENT_FILE" || true)
run_test "Accepts phase number parameter (found: ${HAS_PHASE_PARAM})" "$( [ "$HAS_PHASE_PARAM" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Returns structured JSON with observations_for_persistence
# =============================================================================
echo ""
echo "--- Observations for Persistence ---"

# Must define observations_for_persistence in output
HAS_OBS_PERSIST=$(grep -c 'observations_for_persistence' "$AGENT_FILE" || true)
run_test "Output defines observations_for_persistence (found: ${HAS_OBS_PERSIST})" "$( [ "$HAS_OBS_PERSIST" -ge 1 ] && echo 0 || echo 1 )"

# Must contain JSON schema for observations
# Check for the observation structure with subagent, phase, observations array
HAS_OBS_SUBAGENT=$(grep -c '"subagent"' "$AGENT_FILE" || true)
run_test "Observations JSON contains 'subagent' field (found: ${HAS_OBS_SUBAGENT})" "$( [ "$HAS_OBS_SUBAGENT" -ge 1 ] && echo 0 || echo 1 )"

HAS_OBS_PHASE=$(grep -c '"phase"' "$AGENT_FILE" || true)
run_test "Observations JSON contains 'phase' field (found: ${HAS_OBS_PHASE})" "$( [ "$HAS_OBS_PHASE" -ge 1 ] && echo 0 || echo 1 )"

HAS_OBS_ARRAY=$(grep -c '"observations"' "$AGENT_FILE" || true)
run_test "Observations JSON contains 'observations' array (found: ${HAS_OBS_ARRAY})" "$( [ "$HAS_OBS_ARRAY" -ge 1 ] && echo 0 || echo 1 )"

# Each observation must have category, note, severity
HAS_OBS_CATEGORY=$(grep -c '"category"' "$AGENT_FILE" || true)
run_test "Observation schema has 'category' field (found: ${HAS_OBS_CATEGORY})" "$( [ "$HAS_OBS_CATEGORY" -ge 1 ] && echo 0 || echo 1 )"

HAS_OBS_SEVERITY=$(grep -c '"severity"' "$AGENT_FILE" || true)
run_test "Observation schema has 'severity' field (found: ${HAS_OBS_SEVERITY})" "$( [ "$HAS_OBS_SEVERITY" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Phase identification in observation metadata (4.5 or 5.5)
# =============================================================================
echo ""
echo "--- Phase Identification in Metadata ---"

# Must reference Phase 4.5 in observation metadata context
HAS_PHASE_45_META=$(grep -c '4\.5' "$AGENT_FILE" || true)
run_test "Phase 4.5 referenced in agent (found: ${HAS_PHASE_45_META})" "$( [ "$HAS_PHASE_45_META" -ge 1 ] && echo 0 || echo 1 )"

# Must reference Phase 5.5 in observation metadata context
HAS_PHASE_55_META=$(grep -c '5\.5' "$AGENT_FILE" || true)
run_test "Phase 5.5 referenced in agent (found: ${HAS_PHASE_55_META})" "$( [ "$HAS_PHASE_55_META" -ge 1 ] && echo 0 || echo 1 )"

# Must use PHASE_NUMBER variable or equivalent for dynamic phase identification
HAS_PHASE_VAR=$(grep -c 'PHASE_NUMBER\|PHASE\|phase' "$AGENT_FILE" || true)
run_test "Uses phase variable for dynamic identification (found: ${HAS_PHASE_VAR})" "$( [ "$HAS_PHASE_VAR" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Orchestrator persistence path
# =============================================================================
echo ""
echo "--- Orchestrator Persistence Path ---"

# Must reference the persistence path format
HAS_PERSIST_PATH=$(grep -c 'devforgeai/feedback/ai-analysis' "$AGENT_FILE" || true)
run_test "References orchestrator persistence path (found: ${HAS_PERSIST_PATH})" "$( [ "$HAS_PERSIST_PATH" -ge 1 ] && echo 0 || echo 1 )"

# Must mention orchestrator is responsible for writing (not the agent)
HAS_ORCHESTRATOR_WRITES=$(grep -ci 'orchestrator.*persist\|orchestrator.*write\|orchestrator.*extract' "$AGENT_FILE" || true)
run_test "States orchestrator handles persistence (found: ${HAS_ORCHESTRATOR_WRITES})" "$( [ "$HAS_ORCHESTRATOR_WRITES" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Stateless behavior documented
# =============================================================================
echo ""
echo "--- Stateless Behavior ---"

# Agent must document stateless behavior for independent Phase 4.5/5.5 invocations
HAS_STATELESS=$(grep -ci 'stateless\|independent\|fresh.*context\|no.*state\|no.*prior' "$AGENT_FILE" || true)
run_test "Stateless behavior documented (found: ${HAS_STATELESS})" "$( [ "$HAS_STATELESS" -ge 2 ] && echo 0 || echo 1 )"

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
