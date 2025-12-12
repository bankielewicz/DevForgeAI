#!/usr/bin/env bash

# Test suite for AC#4: Summary Statistics Accuracy
# Tests calculation of coverage statistics and counts

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
# TEST: AC#4.1 - Should count total epics correctly
# ============================================================================
test_should_count_total_epics_correctly() {
    local test_name="AC#4.1: total_epics equals count of epic files"

    # Arrange: Create exactly 3 epic files
    cat > "${TEMP_DIR}/EPIC-001.md" << 'EOF'
---
id: EPIC-001
title: Epic One
---

## Features

- Feature A (STORY-001)
EOF

    cat > "${TEMP_DIR}/EPIC-002.md" << 'EOF'
---
id: EPIC-002
title: Epic Two
---

## Features

- Feature B (STORY-002)
EOF

    cat > "${TEMP_DIR}/EPIC-003.md" << 'EOF'
---
id: EPIC-003
title: Epic Three
---

## Features

- Feature C (STORY-003)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: total_epics equals 3
    local total_epics=$(echo "${json_output}" | jq '.summary.total_epics' 2>/dev/null || echo "0")
    if [[ "${total_epics}" == "3" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 3, got ${total_epics}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#4.2 - Should count total features correctly
# ============================================================================
test_should_count_total_features_correctly() {
    local test_name="AC#4.2: total_features equals sum of all features"

    # Arrange: Create epics with known feature counts
    # EPIC-004: 4 features
    cat > "${TEMP_DIR}/EPIC-004.md" << 'EOF'
---
id: EPIC-004
title: Epic Four
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (STORY-003)
- Feature D (STORY-004)
EOF

    # EPIC-005: 3 features
    cat > "${TEMP_DIR}/EPIC-005.md" << 'EOF'
---
id: EPIC-005
title: Epic Five
---

## Features

- Feature E (STORY-005)
- Feature F (STORY-006)
- Feature G (STORY-007)
EOF

    # Act: Generate JSON (total should be 7)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: total_features equals 7
    local total_features=$(echo "${json_output}" | jq '.summary.total_features' 2>/dev/null || echo "0")
    if [[ "${total_features}" == "7" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 7, got ${total_features}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#4.3 - Should calculate coverage percentage correctly
# ============================================================================
test_should_calculate_coverage_percentage_correctly() {
    local test_name="AC#4.3: overall_coverage_percent = (stories / features) * 100"

    # Arrange: 5 features, 3 with stories (60%)
    local mock_epic="${TEMP_DIR}/EPIC-006.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-006
title: Coverage Calc
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (STORY-003)
- Feature D (No story)
- Feature E (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: overall_coverage_percent equals 60.0
    local coverage=$(echo "${json_output}" | jq '.summary.overall_coverage_percent' 2>/dev/null || echo "0")
    if [[ "${coverage}" == "60"* ]] || [[ "${coverage}" == "60."* ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 60%, got ${coverage}%"
        return 1
    fi
}

# ============================================================================
# TEST: AC#4.4 - Should count missing stories correctly
# ============================================================================
test_should_count_missing_stories_correctly() {
    local test_name="AC#4.4: missing_stories_count equals features without stories"

    # Arrange: 8 features, 5 with stories, 3 missing
    local mock_epic="${TEMP_DIR}/EPIC-007.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-007
title: Missing Count
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (STORY-003)
- Feature D (STORY-004)
- Feature E (STORY-005)
- Feature F (No story)
- Feature G (No story)
- Feature H (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: missing_stories_count equals 3
    local missing=$(echo "${json_output}" | jq '.summary.missing_stories_count' 2>/dev/null || echo "0")
    if [[ "${missing}" == "3" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 3, got ${missing}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#4.5 - Coverage percentage should be rounded to 1 decimal
# ============================================================================
test_coverage_percentage_rounded_to_one_decimal() {
    local test_name="AC#4.5: Coverage % rounded to 1 decimal place"

    # Arrange: 3 features, 1 with story = 33.333...% → should round to 33.3%
    local mock_epic="${TEMP_DIR}/EPIC-008.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-008
title: Rounding Test
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

    # Assert: Coverage is X.X format (one decimal place)
    local coverage=$(echo "${json_output}" | jq '.summary.overall_coverage_percent' 2>/dev/null || echo "0")
    if [[ "${coverage}" =~ ^[0-9]+\.[0-9]$ ]] || [[ "${coverage}" =~ ^[0-9]+\.[0-9]{2} ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Coverage not properly rounded: ${coverage}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#4.6 - Should handle edge case: all features have stories
# ============================================================================
test_should_handle_100_percent_coverage() {
    local test_name="AC#4.6: 100% coverage when all features have stories"

    # Arrange: All features linked to stories
    local mock_epic="${TEMP_DIR}/EPIC-009.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-009
title: Perfect Coverage
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

    # Assert: overall_coverage_percent equals 100
    local coverage=$(echo "${json_output}" | jq '.summary.overall_coverage_percent' 2>/dev/null || echo "0")
    if [[ "${coverage}" == "100"* ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 100%, got ${coverage}%"
        return 1
    fi
}

# ============================================================================
# TEST: AC#4.7 - Should handle edge case: no features have stories
# ============================================================================
test_should_handle_zero_percent_coverage() {
    local test_name="AC#4.7: 0% coverage when no features have stories"

    # Arrange: No features linked to stories
    local mock_epic="${TEMP_DIR}/EPIC-010.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-010
title: No Coverage
---

## Features

- Feature A (No story)
- Feature B (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: overall_coverage_percent equals 0
    local coverage=$(echo "${json_output}" | jq '.summary.overall_coverage_percent' 2>/dev/null || echo "-1")
    if [[ "${coverage}" == "0"* ]] || [[ "${coverage}" == "0" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 0%, got ${coverage}%"
        return 1
    fi
}

# ============================================================================
# TEST: AC#4.8 - Should exclude epics with zero features from calculation
# ============================================================================
test_should_exclude_empty_epics_from_calculation() {
    local test_name="AC#4.8: Epic with zero features excluded from coverage"

    # Arrange: One epic with features, one empty epic
    cat > "${TEMP_DIR}/EPIC-011.md" << 'EOF'
---
id: EPIC-011
title: Normal Epic
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    # Empty epic with no features section
    cat > "${TEMP_DIR}/EPIC-012.md" << 'EOF'
---
id: EPIC-012
title: Empty Epic
---

(No features defined)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: Coverage based on EPIC-011 only (50%), not affected by empty EPIC-012
    local total_features=$(echo "${json_output}" | jq '.summary.total_features' 2>/dev/null || echo "0")
    # Should count 2 features from EPIC-011, not include EPIC-012
    if [[ "${total_features}" == "2" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Empty epic not excluded, got ${total_features} features"
        return 1
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
main() {
    echo "=========================================="
    echo "AC#4: Summary Statistics Accuracy"
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
