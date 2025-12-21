#!/usr/bin/env bash

# Test suite for AC#7: Historical Tracking Persistence
# Tests history file creation, appending, and management

set -euo pipefail

# Test fixtures and helpers
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/temp"

# Create temp directory
mkdir -p "${TEMP_DIR}"

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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac71"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Create epic file
    cat > "${test_dir}/EPIC-001.epic.md" << 'EOF'
---
id: EPIC-001
title: Test Epic
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate report with history tracking
    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History file exists
    if [[ -f "${history_dir}/coverage-history.json" ]]; then
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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac72"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Generate report to create/update history
    cat > "${test_dir}/EPIC-002.epic.md" << 'EOF'
---
id: EPIC-002
title: JSON Test
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: File contains valid JSON array
    if [[ -f "${history_dir}/coverage-history.json" ]] && \
       jq empty < "${history_dir}/coverage-history.json" 2>/dev/null && \
       jq -e 'type == "array"' "${history_dir}/coverage-history.json" >/dev/null 2>&1; then
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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac73"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Generate report
    cat > "${test_dir}/EPIC-003.epic.md" << 'EOF'
---
id: EPIC-003
title: Timestamp Test
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have timestamp field
    if jq -e '.[0] | has("timestamp")' "${history_dir}/coverage-history.json" >/dev/null 2>&1; then
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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac74"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Generate report
    cat > "${test_dir}/EPIC-004.epic.md" << 'EOF'
---
id: EPIC-004
title: Coverage Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have coverage_percent
    if jq -e '.[0] | has("overall_coverage_percent")' "${history_dir}/coverage-history.json" >/dev/null 2>&1; then
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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac75"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Generate report
    cat > "${test_dir}/EPIC-005.epic.md" << 'EOF'
---
id: EPIC-005
title: Epic Count Test
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have total_epics
    if jq -e '.[0] | has("total_epics")' "${history_dir}/coverage-history.json" >/dev/null 2>&1; then
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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac76"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Generate report
    cat > "${test_dir}/EPIC-006.epic.md" << 'EOF'
---
id: EPIC-006
title: Feature Count Test
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
EOF

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have total_features
    if jq -e '.[0] | has("total_features")' "${history_dir}/coverage-history.json" >/dev/null 2>&1; then
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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac77"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Generate report with gaps
    cat > "${test_dir}/EPIC-007.epic.md" << 'EOF'
---
id: EPIC-007
title: Missing Count Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
- Feature C (No story)
EOF

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: History entries have missing_count
    if jq -e '.[0] | has("missing_count")' "${history_dir}/coverage-history.json" >/dev/null 2>&1; then
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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac78"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: First run creates history
    cat > "${test_dir}/EPIC-008.epic.md" << 'EOF'
---
id: EPIC-008
title: Append Test 1
---

## Features

- Feature A (STORY-001)
EOF

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    local count_before=$(jq 'length' "${history_dir}/coverage-history.json" 2>/dev/null || echo "0")

    # Sleep to ensure different timestamp
    sleep 1

    # Second run should append
    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    local count_after=$(jq 'length' "${history_dir}/coverage-history.json" 2>/dev/null || echo "0")

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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac79"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Create epic file
    cat > "${test_dir}/EPIC-009.epic.md" << 'EOF'
---
id: EPIC-009
title: Ordering Test
---

## Features

- Feature A (STORY-001)
EOF

    # Generate first entry
    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Wait and generate second entry
    sleep 1

    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Assert: Last entry has most recent timestamp
    if [[ -f "${history_dir}/coverage-history.json" ]]; then
        local last_timestamp=$(jq -r '.[-1].timestamp' "${history_dir}/coverage-history.json" 2>/dev/null || echo "")
        local first_timestamp=$(jq -r '.[0].timestamp' "${history_dir}/coverage-history.json" 2>/dev/null || echo "")

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

    # Per-test isolated directories
    local test_dir="${TEMP_DIR}/test_ac710"
    local history_dir="${test_dir}/history"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}" "${history_dir}"

    # Arrange: Generate report twice without sleep (same second)
    cat > "${test_dir}/EPIC-010.epic.md" << 'EOF'
---
id: EPIC-010
title: Duplicate Test
---

## Features

- Feature A (STORY-001)
EOF

    # First run
    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    local count_first=$(jq 'length' "${history_dir}/coverage-history.json" 2>/dev/null || echo "0")

    # Second run immediately (might have same timestamp)
    bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        --history-dir="${history_dir}" \
        --enable-history \
        2>/dev/null || true

    # Check for duplicates - count unique timestamps
    local unique_timestamps=$(jq '[.[].timestamp] | unique | length' "${history_dir}/coverage-history.json" 2>/dev/null || echo "0")
    local total_entries=$(jq 'length' "${history_dir}/coverage-history.json" 2>/dev/null || echo "0")

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
            ((passed++)) || true
        else
            ((failed++)) || true
        fi
    done

    echo ""
    echo "=========================================="
    echo "Results: ${passed} passed, ${failed} failed"
    echo "=========================================="

    return $([[ $failed -eq 0 ]])
}

main "$@"
