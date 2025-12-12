#!/usr/bin/env bash

# Test suite for AC#7: Historical Tracking Persistence
# Tests history file creation, appending, and management

set -euo pipefail

# Test fixtures and helpers
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/temp"
HISTORY_DIR="${TEMP_DIR}/history"

# Create temp directories
mkdir -p "${TEMP_DIR}" "${HISTORY_DIR}"

# Cleanup function
cleanup() {
    rm -rf "${TEMP_DIR:?}"
}

trap cleanup EXIT

# ============================================================================
# TEST: AC#7.1 - Should create history file if not exists
# ============================================================================
test_should_create_history_file_if_not_exists() {
    local test_name="AC#7.1: Create history file on first run"

    # Arrange: Clean history directory
    rm -f "${HISTORY_DIR}/coverage-history.json"

    local mock_epic="${TEMP_DIR}/EPIC-001.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-001
title: Test Epic
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate report with history tracking
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History file exists
    if [[ -f "${HISTORY_DIR}/coverage-history.json" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - History file not created"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.2 - History file should contain valid JSON array
# ============================================================================
test_history_file_should_contain_valid_json() {
    local test_name="AC#7.2: History file is valid JSON array"

    # Arrange: Generate report to create/update history
    local mock_epic="${TEMP_DIR}/EPIC-002.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-002
title: JSON Test
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Assert: File contains valid JSON array
    if [[ -f "${HISTORY_DIR}/coverage-history.json" ]] && \
       jq empty < "${HISTORY_DIR}/coverage-history.json" 2>/dev/null && \
       jq -e 'type == "array"' "${HISTORY_DIR}/coverage-history.json" >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - History file is not valid JSON array"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.3 - History entry should contain timestamp
# ============================================================================
test_history_entry_contains_timestamp() {
    local test_name="AC#7.3: History entry includes 'timestamp'"

    # Arrange: Generate report
    local mock_epic="${TEMP_DIR}/EPIC-003.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-003
title: Timestamp Test
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have timestamp field
    if jq -e '.[0] | has("timestamp")' "${HISTORY_DIR}/coverage-history.json" >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Timestamp field missing"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.4 - History entry should contain overall_coverage_percent
# ============================================================================
test_history_entry_contains_coverage_percent() {
    local test_name="AC#7.4: History entry includes 'overall_coverage_percent'"

    # Arrange: Generate report
    local mock_epic="${TEMP_DIR}/EPIC-004.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-004
title: Coverage Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have coverage_percent
    if jq -e '.[0] | has("overall_coverage_percent")' "${HISTORY_DIR}/coverage-history.json" >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Coverage percent field missing"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.5 - History entry should contain total_epics
# ============================================================================
test_history_entry_contains_total_epics() {
    local test_name="AC#7.5: History entry includes 'total_epics'"

    # Arrange: Generate report
    local mock_epic="${TEMP_DIR}/EPIC-005.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-005
title: Epic Count Test
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have total_epics
    if jq -e '.[0] | has("total_epics")' "${HISTORY_DIR}/coverage-history.json" >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Total epics field missing"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.6 - History entry should contain total_features
# ============================================================================
test_history_entry_contains_total_features() {
    local test_name="AC#7.6: History entry includes 'total_features'"

    # Arrange: Generate report
    local mock_epic="${TEMP_DIR}/EPIC-006.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-006
title: Feature Count Test
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
EOF

    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have total_features
    if jq -e '.[0] | has("total_features")' "${HISTORY_DIR}/coverage-history.json" >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Total features field missing"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.7 - History entry should contain missing_count
# ============================================================================
test_history_entry_contains_missing_count() {
    local test_name="AC#7.7: History entry includes 'missing_count'"

    # Arrange: Generate report with gaps
    local mock_epic="${TEMP_DIR}/EPIC-007.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-007
title: Missing Count Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
- Feature C (No story)
EOF

    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have missing_count
    if jq -e '.[0] | has("missing_count")' "${HISTORY_DIR}/coverage-history.json" >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing count field missing"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.8 - Should append new entries to existing history
# ============================================================================
test_should_append_entries_to_history() {
    local test_name="AC#7.8: New runs append entries (not overwrite)"

    # Arrange: First run creates history
    local mock_epic="${TEMP_DIR}/EPIC-008.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-008
title: Append Test 1
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    local count_before=$(jq 'length' "${HISTORY_DIR}/coverage-history.json" 2>/dev/null || echo "0")

    # Sleep to ensure different timestamp
    sleep 1

    # Second run should append
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    local count_after=$(jq 'length' "${HISTORY_DIR}/coverage-history.json" 2>/dev/null || echo "0")

    # Assert: Count increased by 1
    if [[ $count_after -gt $count_before ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Entries not appended (before: $count_before, after: $count_after)"
        return 1
    fi
}

# ============================================================================
# TEST: AC#7.9 - History entries should be chronologically ordered
# ============================================================================
test_history_entries_chronologically_ordered() {
    local test_name="AC#7.9: History entries ordered chronologically (newest last)"

    # Assert: Last entry has most recent timestamp
    if [[ -f "${HISTORY_DIR}/coverage-history.json" ]]; then
        local last_timestamp=$(jq -r '.[-1].timestamp' "${HISTORY_DIR}/coverage-history.json" 2>/dev/null || echo "")
        local first_timestamp=$(jq -r '.[0].timestamp' "${HISTORY_DIR}/coverage-history.json" 2>/dev/null || echo "")

        if [[ -n "${last_timestamp}" ]] && [[ -n "${first_timestamp}" ]] && \
           [[ "${last_timestamp}" > "${first_timestamp}" ]] || [[ "${last_timestamp}" == "${first_timestamp}" ]]; then
            echo "✓ ${test_name}"
            return 0
        fi
    fi

    echo "✗ ${test_name} - Entries not properly ordered"
    return 1
}

# ============================================================================
# TEST: AC#7.10 - Should prevent duplicate entries for same timestamp
# ============================================================================
test_should_prevent_duplicate_timestamps() {
    local test_name="AC#7.10: Prevent duplicate entries (same timestamp)"

    # Arrange: Generate report twice without sleep (same second)
    local mock_epic="${TEMP_DIR}/EPIC-009.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-009
title: Duplicate Test
---

## Features

- Feature A (STORY-001)
EOF

    # First run
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    local count_first=$(jq 'length' "${HISTORY_DIR}/coverage-history.json" 2>/dev/null || echo "0")

    # Second run immediately (might have same timestamp)
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        --history-dir="${HISTORY_DIR}" \
        --enable-history \
        2>/dev/null || true

    # Check for duplicates - count unique timestamps
    local unique_timestamps=$(jq '[.[].timestamp] | unique | length' "${HISTORY_DIR}/coverage-history.json" 2>/dev/null || echo "0")
    local total_entries=$(jq 'length' "${HISTORY_DIR}/coverage-history.json" 2>/dev/null || echo "0")

    if [[ "${unique_timestamps}" == "${total_entries}" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Duplicate timestamps detected"
        return 1
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
main() {
    echo "=========================================="
    echo "AC#7: Historical Tracking Persistence"
    echo "=========================================="
    echo ""

    local passed=0
    local failed=0

    for test_func in $(compgen -A function | grep '^test_'); do
        if $test_func; then
            ((passed++))
        else
            ((failed++))
        fi
    done

    echo ""
    echo "=========================================="
    echo "Results: ${passed} passed, ${failed} failed"
    echo "=========================================="

    return $([[ $failed -eq 0 ]])
}

main "$@"
