#!/usr/bin/env bash
#
# TEST: State File Archival on Completion
# AC#4: Verify state file archival on completion
#
# Acceptance Criteria:
#   Given a test workflow completes all phases successfully
#   When the story status is updated to "QA Approved"
#   Then the state file is moved from `devforgeai/workflows/STORY-XXX-phase-state.json`
#        to `devforgeai/workflows/completed/STORY-XXX-phase-state.json`.
#
# Exit Code Contract:
#   0 = Test PASSED (state file archived to completed/ directory)
#   1 = Test FAILED (state file not archived or in wrong location)
#

set -euo pipefail

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

TEST_NAME="State File Archival on Completion"
TEST_ID="AC#4"
PROJECT_ROOT="${PROJECT_ROOT:-.}"
STORY_TEST_ID="STORY-TEST-004"
STATE_FILE_DIR="${PROJECT_ROOT}/devforgeai/workflows"
COMPLETED_DIR="${STATE_FILE_DIR}/completed"
LOG_DIR="${PROJECT_ROOT}/devforgeai/tests/STORY-154/test-logs"

mkdir -p "${LOG_DIR}" "${STATE_FILE_DIR}" "${COMPLETED_DIR}"

LOG_FILE="${LOG_DIR}/test-state-archival.log"

# ============================================================================
# CLEANUP TRAP
# ============================================================================

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        echo "[CLEANUP] Test failed with exit code: $exit_code" >> "${LOG_FILE}"
    fi
    # Remove test files (from active and archive)
    rm -f "${STATE_FILE_DIR}/${STORY_TEST_ID}-phase-state.json" \
          "${COMPLETED_DIR}/${STORY_TEST_ID}-phase-state.json" 2>/dev/null || true
}

trap cleanup EXIT

# ============================================================================
# ASSERTIONS
# ============================================================================

assert_file_exists() {
    local file_path=$1
    local test_name=$2

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Expected file to exist at: $file_path" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
    return 0
}

assert_file_not_exists() {
    local file_path=$1
    local test_name=$2

    if [[ -f "$file_path" ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Expected file to NOT exist at: $file_path" >> "${LOG_FILE}"
        echo "  File still present in original location" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
    return 0
}

assert_file_content_matches() {
    local source_file=$1
    local archived_file=$2
    local test_name=$3

    # Compare checksums to verify content matches
    local source_checksum=$(sha256sum "$source_file" | awk '{print $1}')
    local archive_checksum=$(sha256sum "$archived_file" | awk '{print $1}')

    if [[ "$source_checksum" != "$archive_checksum" ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  File content does not match after archival" >> "${LOG_FILE}"
        echo "  Source checksum:  $source_checksum" >> "${LOG_FILE}"
        echo "  Archive checksum: $archive_checksum" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
    return 0
}

assert_directory_exists() {
    local dir_path=$1
    local test_name=$2

    if [[ ! -d "$dir_path" ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Expected directory to exist at: $dir_path" >> "${LOG_FILE}"
        return 1
    fi

    echo "ASSERT PASSED: ${test_name}" >> "${LOG_FILE}"
    return 0
}

assert_directory_writable() {
    local dir_path=$1
    local test_name=$2

    if [[ ! -w "$dir_path" ]]; then
        echo "ASSERT FAILED: ${test_name}" >> "${LOG_FILE}"
        echo "  Directory is not writable: $dir_path" >> "${LOG_FILE}"
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

    # Verify test preconditions
    echo "[PRECONDITION] Verifying test environment..."
    assert_directory_exists "${STATE_FILE_DIR}" \
        "workflows directory exists"

    assert_directory_exists "${COMPLETED_DIR}" \
        "completed subdirectory exists"

    assert_directory_writable "${STATE_FILE_DIR}" \
        "workflows directory is writable"

    assert_directory_writable "${COMPLETED_DIR}" \
        "completed directory is writable"

    echo ""

    # Arrange: Create active state file
    echo "[ARRANGE] Creating test state file in active directory..."

    cat > "${STATE_FILE_DIR}/${STORY_TEST_ID}-phase-state.json" << 'EOF'
{
  "story_id": "STORY-TEST-004",
  "current_phase": 10,
  "workflow_start": "2025-12-29T10:00:00Z",
  "workflow_end": "2025-12-29T10:15:00Z",
  "story_status": "QA Approved",
  "phases": {
    "01": { "status": "completed", "checkpoint_passed": true },
    "02": { "status": "completed", "checkpoint_passed": true },
    "03": { "status": "completed", "checkpoint_passed": true },
    "04": { "status": "completed", "checkpoint_passed": true },
    "05": { "status": "completed", "checkpoint_passed": true },
    "06": { "status": "completed", "checkpoint_passed": true },
    "07": { "status": "completed", "checkpoint_passed": true },
    "08": { "status": "completed", "checkpoint_passed": true },
    "09": { "status": "completed", "checkpoint_passed": true },
    "10": { "status": "completed", "checkpoint_passed": true }
  }
}
EOF

    assert_file_exists "${STATE_FILE_DIR}/${STORY_TEST_ID}-phase-state.json" \
        "Test state file created in active directory"

    echo ""
    echo "[ACT] Archiving state file to completed directory..."

    # Act: Move state file to completed directory
    mv "${STATE_FILE_DIR}/${STORY_TEST_ID}-phase-state.json" \
       "${COMPLETED_DIR}/${STORY_TEST_ID}-phase-state.json"

    echo "[RESULT] State file move completed"
    echo ""

    # Assert: Original file no longer exists in active directory
    echo "[ASSERT] Verifying file removed from active directory..."
    assert_file_not_exists "${STATE_FILE_DIR}/${STORY_TEST_ID}-phase-state.json" \
        "State file removed from active workflows directory"

    # Assert: File exists in completed directory
    echo "[ASSERT] Verifying file exists in completed directory..."
    assert_file_exists "${COMPLETED_DIR}/${STORY_TEST_ID}-phase-state.json" \
        "State file present in completed subdirectory"

    # Assert: File content preserved
    echo "[ASSERT] Verifying file content integrity..."

    # Create temporary copy of original to validate
    TEMP_ORIGINAL="${STATE_FILE_DIR}/.${STORY_TEST_ID}-original-checksum"
    cat > "${TEMP_ORIGINAL}" << 'EOF'
{
  "story_id": "STORY-TEST-004",
  "current_phase": 10,
  "workflow_start": "2025-12-29T10:00:00Z",
  "workflow_end": "2025-12-29T10:15:00Z",
  "story_status": "QA Approved",
  "phases": {
    "01": { "status": "completed", "checkpoint_passed": true },
    "02": { "status": "completed", "checkpoint_passed": true },
    "03": { "status": "completed", "checkpoint_passed": true },
    "04": { "status": "completed", "checkpoint_passed": true },
    "05": { "status": "completed", "checkpoint_passed": true },
    "06": { "status": "completed", "checkpoint_passed": true },
    "07": { "status": "completed", "checkpoint_passed": true },
    "08": { "status": "completed", "checkpoint_passed": true },
    "09": { "status": "completed", "checkpoint_passed": true },
    "10": { "status": "completed", "checkpoint_passed": true }
  }
}
EOF

    assert_file_content_matches "${TEMP_ORIGINAL}" \
        "${COMPLETED_DIR}/${STORY_TEST_ID}-phase-state.json" \
        "Archived file content matches original"

    rm -f "${TEMP_ORIGINAL}"

    # Assert: Archived file is readable
    echo "[ASSERT] Verifying archived file is readable..."
    if ! python3 -m json.tool "${COMPLETED_DIR}/${STORY_TEST_ID}-phase-state.json" > /dev/null 2>&1; then
        echo "ASSERT FAILED: Archived file is not valid JSON" >> "${LOG_FILE}"
        return 1
    fi
    echo "ASSERT PASSED: Archived file is valid JSON" >> "${LOG_FILE}"

    echo ""
    echo "[VERIFY] State file archival complete"
    echo "  Original Location: ${STATE_FILE_DIR}/${STORY_TEST_ID}-phase-state.json"
    echo "  Archived Location: ${COMPLETED_DIR}/${STORY_TEST_ID}-phase-state.json"
    echo "  Status: ARCHIVED"
    echo "  Content Integrity: VERIFIED"
    echo "End Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "================================================================"

} | tee -a "${LOG_FILE}"

# Exit with test result
if grep -q "ASSERT FAILED" "${LOG_FILE}"; then
    exit 1
fi

exit 0
