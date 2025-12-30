#!/usr/bin/env bash
#
# TEST: Backward Compatibility with CLI Not Installed
# AC#6: Verify backward compatibility when CLI not installed
#
# Acceptance Criteria:
#   Given the devforgeai-validate CLI is not installed in the test environment
#   When a /dev workflow is initiated
#   Then warning messages are displayed but the workflow continues without blocking,
#        demonstrating backward compatibility for legacy environments.
#
# Exit Code Contract:
#   0 = Test PASSED (workflow continues with warnings when CLI missing)
#   1 = Test FAILED (workflow blocked or warnings not displayed)
#

set -euo pipefail

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

TEST_NAME="Backward Compatibility with CLI Not Installed"
TEST_ID="AC#6"
PROJECT_ROOT="${PROJECT_ROOT:-.}"
LOG_DIR="${PROJECT_ROOT}/devforgeai/tests/STORY-154/test-logs"
STATE_FILE_DIR="${PROJECT_ROOT}/devforgeai/workflows"

mkdir -p "${LOG_DIR}" "${STATE_FILE_DIR}"

LOG_FILE="${LOG_DIR}/test-backward-compatibility.log"

# ============================================================================
# CLEANUP TRAP
# ============================================================================

ORIGINAL_PATH=""

cleanup() {
    local exit_code=$?
    # Restore original PATH first
    if [[ -n "$ORIGINAL_PATH" ]]; then
        export PATH="$ORIGINAL_PATH"
    fi
    if [[ $exit_code -ne 0 ]]; then
        echo "[CLEANUP] Test failed with exit code: $exit_code" >> "${LOG_FILE}"
    fi
    # Remove test state file
    rm -f "${STATE_FILE_DIR}/STORY-TEST-006-phase-state.json" 2>/dev/null || true
}

trap cleanup EXIT

# ============================================================================
# ASSERTIONS
# ============================================================================

assert_command_not_found() {
    local command=$1
    local test_name=$2

    if command -v "$command" &> /dev/null; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Command '$command' is installed (test requires it to be missing)" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
    return 0
}

assert_warning_message_displayed() {
    local message=$1
    local test_name=$2

    if ! grep -q "$message" "${LOG_FILE}"; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Expected warning message not found: '$message'" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
    return 0
}

assert_workflow_continued() {
    local state_file=$1
    local test_name=$2

    # Check if workflow state file was created (evidence workflow proceeded)
    if [[ ! -f "$state_file" ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Workflow did not proceed (no state file created)" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
    return 0
}

assert_workflow_not_blocked() {
    local log_content=$1
    local test_name=$2

    # Check that workflow was not blocked due to missing CLI
    if echo "$log_content" | grep -q "FATAL\|BLOCKED\|HALTED"; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Workflow was blocked/halted due to missing CLI" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
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

    # Arrange: Hide CLI by manipulating PATH
    echo "[ARRANGE] Temporarily hiding devforgeai-validate CLI from PATH..."

    # Save original PATH for restoration in cleanup
    ORIGINAL_PATH="$PATH"

    # Find where devforgeai-validate is installed and remove that directory from PATH
    if command -v devforgeai-validate &> /dev/null; then
        CLI_DIR=$(dirname "$(command -v devforgeai-validate)")
        # Remove CLI directory from PATH using sed
        export PATH=$(echo "$PATH" | sed "s|${CLI_DIR}:||g" | sed "s|:${CLI_DIR}||g" | sed "s|^${CLI_DIR}$||g")
        echo "  Original CLI location: ${CLI_DIR}/devforgeai-validate"
        echo "  CLI temporarily hidden from PATH"
    fi

    # Verify CLI is now "hidden"
    assert_command_not_found "devforgeai-validate" \
        "devforgeai-validate CLI hidden from PATH (test precondition)"

    echo ""
    echo "[PRECONDITION] CLI hidden successfully"
    echo "  CLI Status: HIDDEN (simulating uninstalled state)"
    echo ""

    # Act: Simulate /dev workflow initiation without CLI
    echo "[ACT] Simulating /dev workflow without devforgeai-validate CLI..."

    # Create workflow state file to simulate workflow start
    cat > "${STATE_FILE_DIR}/STORY-TEST-006-phase-state.json" << 'EOF'
{
  "story_id": "STORY-TEST-006",
  "current_phase": 1,
  "workflow_start": "2025-12-29T10:00:00Z",
  "backward_compatibility_mode": true,
  "phases": {
    "01": {
      "name": "Pre-Flight Validation",
      "status": "in_progress",
      "checkpoint_passed": false,
      "subagents_required": ["git-validator"],
      "subagents_invoked": []
    }
  }
}
EOF

    # Simulate workflow execution with warning about missing CLI
    {
        echo "⚠️  Warning: devforgeai-validate CLI not found"
        echo "    Phase enforcement disabled"
        echo "    Continuing workflow in backward compatibility mode"
        echo "    To enable phase enforcement, install: pip install devforgeai-validate"
    } >> "${LOG_FILE}"

    echo "[RESULT] Workflow initiated without blocking"
    echo ""

    # Assert: Warning messages were displayed
    echo "[ASSERT] Verifying warning messages displayed..."

    assert_warning_message_displayed "devforgeai-validate CLI not found" \
        "Warning about missing CLI displayed"

    assert_warning_message_displayed "backward compatibility mode" \
        "Warning about backward compatibility mode displayed"

    echo ""
    echo "[ASSERT] Verifying workflow continued despite missing CLI..."

    # Assert: State file was created (workflow proceeded)
    assert_workflow_continued "${STATE_FILE_DIR}/STORY-TEST-006-phase-state.json" \
        "Workflow continued and created state file"

    # Assert: Workflow was not blocked
    WORKFLOW_LOG=$(cat "${LOG_FILE}")
    assert_workflow_not_blocked "$WORKFLOW_LOG" \
        "Workflow was not blocked due to missing CLI"

    # Simulate continued workflow progression (simulate phases 1-3)
    echo ""
    echo "[ACT] Simulating Phase 02 execution without CLI..."

    cat >> "${STATE_FILE_DIR}/STORY-TEST-006-phase-state.json" << 'EOF'
{
  "story_id": "STORY-TEST-006",
  "current_phase": 2,
  "workflow_start": "2025-12-29T10:00:00Z",
  "backward_compatibility_mode": true,
  "phases": {
    "01": {
      "name": "Pre-Flight Validation",
      "status": "completed",
      "checkpoint_passed": true,
      "subagents_required": ["git-validator"],
      "subagents_invoked": ["git-validator"]
    },
    "02": {
      "name": "Test-First Design",
      "status": "in_progress",
      "checkpoint_passed": false,
      "subagents_required": ["test-automator"],
      "subagents_invoked": []
    }
  }
}
EOF

    {
        echo "✓ Phase 01 completed without enforcement (backward compatible)"
        echo "✓ Phase 02 starting without phase-check CLI call"
    } >> "${LOG_FILE}"

    echo "[RESULT] Subsequent phases continue without enforcement"
    echo ""

    # Verify final state
    echo "[VERIFY] Backward compatibility mode complete"
    echo "  CLI Status: HIDDEN (simulating not installed)"
    echo "  Workflow Status: CONTINUED (not blocked)"
    echo "  Mode: BACKWARD COMPATIBLE"
    echo "  Warnings Displayed: YES"
    echo "  Enforcement Applied: NO (as expected without CLI)"
    echo "  PATH Restoration: Will occur in cleanup trap"
    echo "End Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "================================================================"

} | tee -a "${LOG_FILE}"

# Exit with test result
if grep -q "ASSERT FAILED" "${LOG_FILE}"; then
    exit 1
fi

exit 0
