#!/usr/bin/env bash

# Test suite for AC#3: JSON Export for Programmatic Access
# Tests JSON output format with required fields and schema validation

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

# Helper: Check if string is valid JSON
is_valid_json() {
    echo "$1" | jq empty 2>/dev/null
}

# ============================================================================
# TEST: AC#3.1 - Should output valid JSON
# ============================================================================
test_should_output_valid_json() {
    local test_name="AC#3.1: Output is valid JSON"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-001.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-001
title: Test Epic
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
EOF

    # Act: Generate JSON output
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "INVALID")

    # Assert: Output is valid JSON
    if is_valid_json "${json_output}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Output is not valid JSON"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.2 - JSON should contain summary object
# ============================================================================
test_json_should_contain_summary_object() {
    local test_name="AC#3.2: Contains 'summary' object"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-002.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-002
title: Summary Test
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: JSON contains 'summary' key
    if echo "${json_output}" | jq -e '.summary' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing 'summary' object"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.3 - Summary should contain total_epics
# ============================================================================
test_summary_should_contain_total_epics() {
    local test_name="AC#3.3: Summary contains 'total_epics'"

    # Arrange: Two epics
    cat > "${TEMP_DIR}/EPIC-003.epic.md" << 'EOF'
---
id: EPIC-003
title: Epic Three
---

## Features

- Feature A (STORY-001)
EOF

    cat > "${TEMP_DIR}/EPIC-004.epic.md" << 'EOF'
---
id: EPIC-004
title: Epic Four
---

## Features

- Feature B (STORY-002)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: summary.total_epics exists
    if echo "${json_output}" | jq -e '.summary.total_epics' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing 'total_epics' in summary"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.4 - Summary should contain total_features
# ============================================================================
test_summary_should_contain_total_features() {
    local test_name="AC#3.4: Summary contains 'total_features'"

    # Arrange: Epic with features
    local mock_epic="${TEMP_DIR}/EPIC-005.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-005
title: Features Test
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (STORY-003)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: summary.total_features exists
    if echo "${json_output}" | jq -e '.summary.total_features' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing 'total_features' in summary"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.5 - Summary should contain overall_coverage_percent
# ============================================================================
test_summary_should_contain_overall_coverage_percent() {
    local test_name="AC#3.5: Summary contains 'overall_coverage_percent'"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-006.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-006
title: Coverage Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: summary.overall_coverage_percent exists
    if echo "${json_output}" | jq -e '.summary.overall_coverage_percent' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing 'overall_coverage_percent' in summary"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.6 - Summary should contain missing_stories_count
# ============================================================================
test_summary_should_contain_missing_stories_count() {
    local test_name="AC#3.6: Summary contains 'missing_stories_count'"

    # Arrange: Epic with gaps
    local mock_epic="${TEMP_DIR}/EPIC-007.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-007
title: Gap Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
- Feature C (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: summary.missing_stories_count exists
    if echo "${json_output}" | jq -e '.summary.missing_stories_count' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing 'missing_stories_count' in summary"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.7 - JSON should contain epics array
# ============================================================================
test_json_should_contain_epics_array() {
    local test_name="AC#3.7: Contains 'epics' array"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-008.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-008
title: Epic Array Test
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: JSON contains 'epics' array
    if echo "${json_output}" | jq -e '.epics | type == "array"' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing or invalid 'epics' array"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.8 - Epic entries should contain required fields
# ============================================================================
test_epic_entries_contain_required_fields() {
    local test_name="AC#3.8: Epic entries have epic_id, title, completion_percent"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-009.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-009
title: Field Test Epic
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: Epic entries have required fields
    if echo "${json_output}" | jq -e '.epics[0] | has("epic_id") and has("title") and has("completion_percent")' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Epic entries missing required fields"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.9 - Epic entries should contain missing_features array
# ============================================================================
test_epic_entries_contain_missing_features() {
    local test_name="AC#3.9: Epic entries have 'missing_features' array"

    # Arrange: Epic with gaps
    local mock_epic="${TEMP_DIR}/EPIC-010.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-010
title: Missing Features Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: Epic entries have missing_features array
    if echo "${json_output}" | jq -e '.epics[0] | has("missing_features") and (.missing_features | type == "array")' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing 'missing_features' array"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.10 - JSON should contain actionable_next_steps array
# ============================================================================
test_json_should_contain_actionable_next_steps() {
    local test_name="AC#3.10: Contains 'actionable_next_steps' array"

    # Arrange: Epic with gaps to generate recommendations
    local mock_epic="${TEMP_DIR}/EPIC-011.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-011
title: Actions Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: JSON contains actionable_next_steps array
    if echo "${json_output}" | jq -e '.actionable_next_steps | type == "array"' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing 'actionable_next_steps' array"
        return 1
    fi
}

# ============================================================================
# TEST: AC#3.11 - JSON should contain generated_at timestamp
# ============================================================================
test_json_should_contain_generated_at_timestamp() {
    local test_name="AC#3.11: Contains 'generated_at' in ISO 8601 format"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-012.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-012
title: Timestamp Test
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: JSON contains generated_at field with ISO format
    if echo "${json_output}" | jq -e '.generated_at' >/dev/null 2>&1; then
        local timestamp=$(echo "${json_output}" | jq -r '.generated_at')
        # Check ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ or similar)
        if [[ "${timestamp}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T?[0-9]{2}:[0-9]{2}:[0-9]{2} ]]; then
            echo "✓ ${test_name}"
            return 0
        fi
    fi

    echo "✗ ${test_name} - Missing or invalid 'generated_at' timestamp"
    return 1
}

# ============================================================================
# Run all tests
# ============================================================================
main() {
    echo "=========================================="
    echo "AC#3: JSON Export for Programmatic Access"
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
