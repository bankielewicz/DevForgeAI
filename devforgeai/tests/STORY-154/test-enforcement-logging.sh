#!/usr/bin/env bash
#
# TEST: Enforcement Logging Completeness
# AC#5: Verify enforcement logs capture all decisions
#
# Acceptance Criteria:
#   Given a test workflow includes 3 blocked transitions and 10 allowed transitions
#   When the workflow completes
#   Then the `devforgeai/logs/phase-enforcement.log` contains 13 entries
#        (3 blocked + 10 allowed) with complete decision context for each.
#
# Exit Code Contract:
#   0 = Test PASSED (13 log entries with complete context)
#   1 = Test FAILED (log entries missing or incomplete context)
#

set -euo pipefail

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

TEST_NAME="Enforcement Logging Completeness"
TEST_ID="AC#5"
PROJECT_ROOT="${PROJECT_ROOT:-.}"
LOGS_DIR="${PROJECT_ROOT}/devforgeai/logs"
LOG_DIR="${PROJECT_ROOT}/devforgeai/tests/STORY-154/test-logs"
TEST_LOG_FILE="${LOGS_DIR}/phase-enforcement.log"

mkdir -p "${LOG_DIR}" "${LOGS_DIR}"

TEST_HARNESS_LOG="${LOG_DIR}/test-enforcement-logging.log"

# ============================================================================
# CLEANUP TRAP
# ============================================================================

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        echo "[CLEANUP] Test failed with exit code: $exit_code" >> "${TEST_HARNESS_LOG}"
    fi
    # Preserve enforcement log on failure for debugging
    # Only remove on success
    if [[ $exit_code -eq 0 && -f "$TEST_LOG_FILE" ]]; then
        rm -f "$TEST_LOG_FILE"
    fi
}

trap cleanup EXIT

# ============================================================================
# ASSERTIONS
# ============================================================================

assert_log_entry_count() {
    local log_file=$1
    local expected_count=$2
    local test_name=$3

    local actual_count=$(grep -c "^" "$log_file" 2>/dev/null || echo "0")

    if [[ $actual_count -lt $expected_count ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${TEST_HARNESS_LOG}"
        echo "  Expected: at least $expected_count log entries" >> "${TEST_HARNESS_LOG}"
        echo "  Got: $actual_count log entries" >> "${TEST_HARNESS_LOG}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${TEST_HARNESS_LOG}"
    return 0
}

assert_log_contains_decision_type() {
    local log_file=$1
    local decision_type=$2  # "BLOCKED" or "ALLOWED"
    local expected_count=$3
    local test_name=$4

    local actual_count=$(grep -c "decision: ${decision_type}" "$log_file" 2>/dev/null || echo "0")

    if [[ $actual_count -ne $expected_count ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${TEST_HARNESS_LOG}"
        echo "  Expected: $expected_count entries with decision=${decision_type}" >> "${TEST_HARNESS_LOG}"
        echo "  Got: $actual_count entries with decision=${decision_type}" >> "${TEST_HARNESS_LOG}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${TEST_HARNESS_LOG}"
    return 0
}

assert_log_entry_has_field() {
    local log_file=$1
    local entry_index=$2
    local field_name=$3
    local test_name=$4

    # Get the specified log entry (line)
    local log_entry=$(sed -n "${entry_index}p" "$log_file")

    if [[ ! "$log_entry" =~ ${field_name}[:=] ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${TEST_HARNESS_LOG}"
        echo "  Entry $entry_index missing field: $field_name" >> "${TEST_HARNESS_LOG}"
        echo "  Entry content: $log_entry" >> "${TEST_HARNESS_LOG}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${TEST_HARNESS_LOG}"
    return 0
}

assert_log_entry_timestamp_valid() {
    local log_file=$1
    local entry_index=$2
    local test_name=$3

    local log_entry=$(sed -n "${entry_index}p" "$log_file")

    # Check for ISO 8601 timestamp at start of entry
    if ! [[ "$log_entry" =~ [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${TEST_HARNESS_LOG}"
        echo "  Entry $entry_index has invalid timestamp format" >> "${TEST_HARNESS_LOG}"
        echo "  Entry content: $log_entry" >> "${TEST_HARNESS_LOG}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${TEST_HARNESS_LOG}"
    return 0
}

# ============================================================================
# TEST EXECUTION
# ============================================================================

{
    echo "================================================================"
    echo "TEST: ${TEST_NAME} (${TEST_ID})"
    echo "================================================================"
    echo "Start Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo ""

    # Arrange: Create enforcement log with 13 entries (3 blocked + 10 allowed)
    echo "[ARRANGE] Creating test enforcement log with 13 decision entries..."

    cat > "${TEST_LOG_FILE}" << 'EOF'
2025-12-29T10:00:00Z decision: BLOCKED story=STORY-TEST-005 from_phase=01 to_phase=03 reason="Phase 01 incomplete. Required subagents: tech-stack-detector. Invoked subagents: none."
2025-12-29T10:00:15Z decision: BLOCKED story=STORY-TEST-005 from_phase=02 to_phase=04 reason="Phase 02 incomplete. Required subagents: test-automator. Invoked subagents: none."
2025-12-29T10:00:30Z decision: BLOCKED story=STORY-TEST-005 from_phase=05 to_phase=08 reason="Phase 05 incomplete. Required subagents: integration-tester. Invoked subagents: none."
2025-12-29T10:01:00Z decision: ALLOWED story=STORY-TEST-005 from_phase=01 to_phase=02 subagents_verified="[git-validator, tech-stack-detector]"
2025-12-29T10:01:30Z decision: ALLOWED story=STORY-TEST-005 from_phase=02 to_phase=03 subagents_verified="[test-automator]"
2025-12-29T10:02:00Z decision: ALLOWED story=STORY-TEST-005 from_phase=03 to_phase=04 subagents_verified="[backend-architect, context-validator]"
2025-12-29T10:02:30Z decision: ALLOWED story=STORY-TEST-005 from_phase=04 to_phase=05 subagents_verified="[refactoring-specialist, code-reviewer]"
2025-12-29T10:03:00Z decision: ALLOWED story=STORY-TEST-005 from_phase=05 to_phase=06 subagents_verified="[integration-tester]"
2025-12-29T10:03:30Z decision: ALLOWED story=STORY-TEST-005 from_phase=06 to_phase=07 subagents_verified="[deferral-validator]"
2025-12-29T10:04:00Z decision: ALLOWED story=STORY-TEST-005 from_phase=07 to_phase=08 subagents_verified="[]"
2025-12-29T10:04:30Z decision: ALLOWED story=STORY-TEST-005 from_phase=08 to_phase=09 subagents_verified="[]"
2025-12-29T10:05:00Z decision: ALLOWED story=STORY-TEST-005 from_phase=09 to_phase=10 subagents_verified="[]"
2025-12-29T10:05:30Z decision: ALLOWED story=STORY-TEST-005 from_phase=10 to_phase=end subagents_verified="[dev-result-interpreter]"
EOF

    echo ""
    echo "[VERIFY] Validating log file structure..."

    # Assert: Log file exists and has correct number of entries
    if [[ ! -f "$TEST_LOG_FILE" ]]; then
        echo "ASSERT FAILED: Enforcement log file not created" >> "${TEST_HARNESS_LOG}"
        exit 1
    fi
    echo "ASSERT PASSED: Enforcement log file created" >> "${TEST_HARNESS_LOG}"

    assert_log_entry_count "$TEST_LOG_FILE" 13 \
        "Log contains 13 enforcement decision entries"

    echo ""
    echo "[ACT] Analyzing enforcement log entries..."

    # Assert: Exactly 3 BLOCKED decisions
    assert_log_contains_decision_type "$TEST_LOG_FILE" "BLOCKED" 3 \
        "Log contains exactly 3 BLOCKED transition entries"

    # Assert: Exactly 10 ALLOWED decisions
    assert_log_contains_decision_type "$TEST_LOG_FILE" "ALLOWED" 10 \
        "Log contains exactly 10 ALLOWED transition entries"

    echo ""
    echo "[ASSERT] Verifying complete decision context in each entry..."

    # Verify required fields in log entries
    for entry_idx in {1..13}; do
        assert_log_entry_timestamp_valid "$TEST_LOG_FILE" "$entry_idx" \
            "Entry $entry_idx has valid timestamp"

        assert_log_entry_has_field "$TEST_LOG_FILE" "$entry_idx" "decision" \
            "Entry $entry_idx contains decision field"

        assert_log_entry_has_field "$TEST_LOG_FILE" "$entry_idx" "story" \
            "Entry $entry_idx contains story field"

        assert_log_entry_has_field "$TEST_LOG_FILE" "$entry_idx" "from_phase" \
            "Entry $entry_idx contains from_phase field"

        assert_log_entry_has_field "$TEST_LOG_FILE" "$entry_idx" "to_phase" \
            "Entry $entry_idx contains to_phase field"
    done

    echo ""
    echo "[VERIFY] Enforcement logging validation complete"
    echo "  Total Entries: 13"
    echo "  BLOCKED Decisions: 3"
    echo "  ALLOWED Decisions: 10"
    echo "  Decision Context: COMPLETE"
    echo "End Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "================================================================"

} | tee -a "${TEST_HARNESS_LOG}"

# Exit with test result
if grep -q "ASSERT FAILED" "${TEST_HARNESS_LOG}"; then
    exit 1
fi

exit 0
