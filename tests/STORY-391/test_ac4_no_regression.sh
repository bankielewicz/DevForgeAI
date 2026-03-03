#!/usr/bin/env bash
# =============================================================================
# STORY-391 AC#4: No Regression in Existing TDD Workflows
#
# Verifies all 8 regression checks pass against the updated test-automator:
# 1. YAML frontmatter valid and parseable
# 2. Remediation mode detection preserved ("MODE: REMEDIATION" marker)
# 3. All 6 existing reference files correctly referenced
# 4. Treelint search patterns shared reference preserved
# 5. Observation Capture section preserved with JSON schema and Write() path
# 6. Integration declarations preserved (devforgeai-development, devforgeai-qa, backend-architect)
# 7. All 4 proactive triggers unchanged
# 8. Coverage thresholds (95%/85%/80%) preserved
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"

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
echo "STORY-391 AC#4: No Regression Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Regression Check 1: YAML Frontmatter valid and parseable
# =============================================================================
echo "--- Check 1: YAML Frontmatter Valid ---"

# Frontmatter must start with --- on line 1
LINE1=$(head -1 "$AGENT_FILE")
run_test "Frontmatter starts with ---" "$( [ "$LINE1" = "---" ] && echo 0 || echo 1 )"

# Frontmatter must have closing ---
CLOSING_LINE=$(sed -n '2,/^---$/=' "$AGENT_FILE" | tail -1)
run_test "Frontmatter has closing --- delimiter" "$( [ -n "$CLOSING_LINE" ] && echo 0 || echo 1 )"

# Required frontmatter fields present
FRONTMATTER=$(sed -n '2,/^---$/p' "$AGENT_FILE" | head -n -1)

HAS_NAME=$(echo "$FRONTMATTER" | grep -c '^name:' || true)
run_test "Frontmatter: name field present" "$( [ "$HAS_NAME" -ge 1 ] && echo 0 || echo 1 )"

HAS_DESC=$(echo "$FRONTMATTER" | grep -c '^description:' || true)
run_test "Frontmatter: description field present" "$( [ "$HAS_DESC" -ge 1 ] && echo 0 || echo 1 )"

HAS_TOOLS=$(echo "$FRONTMATTER" | grep -c '^tools:' || true)
run_test "Frontmatter: tools field present" "$( [ "$HAS_TOOLS" -ge 1 ] && echo 0 || echo 1 )"

HAS_MODEL=$(echo "$FRONTMATTER" | grep -c '^model:' || true)
run_test "Frontmatter: model field present" "$( [ "$HAS_MODEL" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Regression Check 2: Remediation mode detection preserved
# =============================================================================
echo ""
echo "--- Check 2: Remediation Mode Detection ---"

HAS_REMEDIATION=$(grep -c 'MODE: REMEDIATION' "$AGENT_FILE" || true)
run_test "Remediation mode marker 'MODE: REMEDIATION' present" "$( [ "$HAS_REMEDIATION" -ge 1 ] && echo 0 || echo 1 )"

HAS_REMEDIATION_REF=$(grep -c 'remediation-mode.md' "$AGENT_FILE" || true)
run_test "Reference to remediation-mode.md present" "$( [ "$HAS_REMEDIATION_REF" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Regression Check 3: All 6 existing reference files correctly referenced
# =============================================================================
echo ""
echo "--- Check 3: 6 Reference Files Referenced ---"

REF_COUNT=0

REF1=$(grep -c 'framework-patterns.md' "$AGENT_FILE" || true)
run_test "Reference: framework-patterns.md" "$( [ "$REF1" -ge 1 ] && echo 0 || echo 1 )"
[ "$REF1" -ge 1 ] && REF_COUNT=$((REF_COUNT + 1))

REF2=$(grep -c 'remediation-mode.md' "$AGENT_FILE" || true)
run_test "Reference: remediation-mode.md" "$( [ "$REF2" -ge 1 ] && echo 0 || echo 1 )"
[ "$REF2" -ge 1 ] && REF_COUNT=$((REF_COUNT + 1))

REF3=$(grep -c 'exception-path-coverage.md' "$AGENT_FILE" || true)
run_test "Reference: exception-path-coverage.md" "$( [ "$REF3" -ge 1 ] && echo 0 || echo 1 )"
[ "$REF3" -ge 1 ] && REF_COUNT=$((REF_COUNT + 1))

REF4=$(grep -c 'technical-specification.md' "$AGENT_FILE" || true)
run_test "Reference: technical-specification.md" "$( [ "$REF4" -ge 1 ] && echo 0 || echo 1 )"
[ "$REF4" -ge 1 ] && REF_COUNT=$((REF_COUNT + 1))

REF5=$(grep -c 'common-patterns.md' "$AGENT_FILE" || true)
run_test "Reference: common-patterns.md" "$( [ "$REF5" -ge 1 ] && echo 0 || echo 1 )"
[ "$REF5" -ge 1 ] && REF_COUNT=$((REF_COUNT + 1))

REF6=$(grep -c 'coverage-optimization.md' "$AGENT_FILE" || true)
run_test "Reference: coverage-optimization.md" "$( [ "$REF6" -ge 1 ] && echo 0 || echo 1 )"
[ "$REF6" -ge 1 ] && REF_COUNT=$((REF_COUNT + 1))

run_test "All 6 reference files referenced (found: ${REF_COUNT}/6)" "$( [ "$REF_COUNT" -ge 6 ] && echo 0 || echo 1 )"

# =============================================================================
# Regression Check 4: Treelint search patterns shared reference preserved
# =============================================================================
echo ""
echo "--- Check 4: Treelint Patterns Reference ---"

HAS_TREELINT_REF=$(grep -c 'treelint-search-patterns.md' "$AGENT_FILE" || true)
run_test "Treelint shared reference (treelint-search-patterns.md) present" "$( [ "$HAS_TREELINT_REF" -ge 1 ] && echo 0 || echo 1 )"

HAS_TREELINT_SEARCH=$(grep -c 'treelint search' "$AGENT_FILE" || true)
run_test "Treelint search command pattern present" "$( [ "$HAS_TREELINT_SEARCH" -ge 1 ] && echo 0 || echo 1 )"

HAS_TREELINT_FALLBACK=$(grep -ciE 'fallback.*grep|grep.*fallback' "$AGENT_FILE" || true)
run_test "Treelint-to-Grep fallback mechanism documented" "$( [ "$HAS_TREELINT_FALLBACK" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Regression Check 5: Observation Capture section preserved
# =============================================================================
echo ""
echo "--- Check 5: Observation Capture ---"

HAS_OBS_SECTION=$(grep -c 'Observation Capture' "$AGENT_FILE" || true)
run_test "Observation Capture section present" "$( [ "$HAS_OBS_SECTION" -ge 1 ] && echo 0 || echo 1 )"

# Check for JSON schema fields
HAS_SUBAGENT_FIELD=$(grep -c '"subagent"' "$AGENT_FILE" || true)
run_test "Observation JSON schema: 'subagent' field" "$( [ "$HAS_SUBAGENT_FIELD" -ge 1 ] && echo 0 || echo 1 )"

HAS_PHASE_FIELD=$(grep -c '"phase"' "$AGENT_FILE" || true)
run_test "Observation JSON schema: 'phase' field" "$( [ "$HAS_PHASE_FIELD" -ge 1 ] && echo 0 || echo 1 )"

HAS_STORY_FIELD=$(grep -c '"story_id"' "$AGENT_FILE" || true)
run_test "Observation JSON schema: 'story_id' field" "$( [ "$HAS_STORY_FIELD" -ge 1 ] && echo 0 || echo 1 )"

HAS_OBSERVATIONS_ARRAY=$(grep -c '"observations"' "$AGENT_FILE" || true)
run_test "Observation JSON schema: 'observations' array" "$( [ "$HAS_OBSERVATIONS_ARRAY" -ge 1 ] && echo 0 || echo 1 )"

# Check Write() path for observation capture
HAS_WRITE_PATH=$(grep -c 'devforgeai/feedback/ai-analysis' "$AGENT_FILE" || true)
run_test "Observation Write() path (devforgeai/feedback/ai-analysis) present" "$( [ "$HAS_WRITE_PATH" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Regression Check 6: Integration declarations preserved
# =============================================================================
echo ""
echo "--- Check 6: Integration Declarations ---"

HAS_DEV_INTEGRATION=$(grep -c 'devforgeai-development' "$AGENT_FILE" || true)
run_test "Integration: devforgeai-development skill referenced" "$( [ "$HAS_DEV_INTEGRATION" -ge 1 ] && echo 0 || echo 1 )"

HAS_QA_INTEGRATION=$(grep -c 'devforgeai-qa' "$AGENT_FILE" || true)
run_test "Integration: devforgeai-qa skill referenced" "$( [ "$HAS_QA_INTEGRATION" -ge 1 ] && echo 0 || echo 1 )"

HAS_BACKEND_INTEGRATION=$(grep -c 'backend-architect' "$AGENT_FILE" || true)
run_test "Integration: backend-architect subagent referenced" "$( [ "$HAS_BACKEND_INTEGRATION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Regression Check 7: All 4 proactive triggers unchanged
# =============================================================================
echo ""
echo "--- Check 7: Proactive Triggers ---"

HAS_TRIGGER1=$(grep -c 'implementing features requiring test coverage' "$AGENT_FILE" || true)
run_test "Trigger 1: 'implementing features requiring test coverage'" "$( [ "$HAS_TRIGGER1" -ge 1 ] && echo 0 || echo 1 )"

HAS_TRIGGER2=$(grep -c 'generating tests from acceptance criteria' "$AGENT_FILE" || true)
run_test "Trigger 2: 'generating tests from acceptance criteria'" "$( [ "$HAS_TRIGGER2" -ge 1 ] && echo 0 || echo 1 )"

HAS_TRIGGER3=$(grep -c 'coverage gaps detected' "$AGENT_FILE" || true)
run_test "Trigger 3: 'coverage gaps detected'" "$( [ "$HAS_TRIGGER3" -ge 1 ] && echo 0 || echo 1 )"

HAS_TRIGGER4=$(grep -c 'TDD Red phase' "$AGENT_FILE" || true)
run_test "Trigger 4: 'TDD Red phase'" "$( [ "$HAS_TRIGGER4" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Regression Check 8: Coverage thresholds preserved
# =============================================================================
echo ""
echo "--- Check 8: Coverage Thresholds ---"

HAS_95=$(grep -c '95%' "$AGENT_FILE" || true)
run_test "Coverage threshold: 95% (business logic) present" "$( [ "$HAS_95" -ge 1 ] && echo 0 || echo 1 )"

HAS_85=$(grep -c '85%' "$AGENT_FILE" || true)
run_test "Coverage threshold: 85% (application) present" "$( [ "$HAS_85" -ge 1 ] && echo 0 || echo 1 )"

HAS_80=$(grep -c '80%' "$AGENT_FILE" || true)
run_test "Coverage threshold: 80% (infrastructure) present" "$( [ "$HAS_80" -ge 1 ] && echo 0 || echo 1 )"

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
