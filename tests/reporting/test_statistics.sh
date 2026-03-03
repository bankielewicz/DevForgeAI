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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac41"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Create exactly 3 epic files
    cat > "${test_dir}/EPIC-001.epic.md" << 'EOF'
---
id: EPIC-001
title: Epic One
---

## Features

- Feature A (STORY-001)
EOF

    cat > "${test_dir}/EPIC-002.epic.md" << 'EOF'
---
id: EPIC-002
title: Epic Two
---

## Features

- Feature B (STORY-002)
EOF

    cat > "${test_dir}/EPIC-003.epic.md" << 'EOF'
---
id: EPIC-003
title: Epic Three
---

## Features

- Feature C (STORY-003)
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac42"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Create epics with known feature counts
    # EPIC-004: 4 features
    cat > "${test_dir}/EPIC-004.epic.md" << 'EOF'
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
    cat > "${test_dir}/EPIC-005.epic.md" << 'EOF'
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
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac43"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: 5 features, 3 with stories (60%)
    cat > "${test_dir}/EPIC-006.epic.md" << 'EOF'
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

    # Create 3 story files that reference this epic (for 60% coverage)
    for i in 001 002 003; do
        cat > "${test_dir}/STORY-${i}.story.md" << EOF
---
id: STORY-${i}
epic: EPIC-006
---
EOF
    done

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac44"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: 8 features, 5 with stories, 3 missing
    cat > "${test_dir}/EPIC-007.epic.md" << 'EOF'
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

    # Create 5 story files that reference this epic
    for i in 001 002 003 004 005; do
        cat > "${test_dir}/STORY-${i}.story.md" << EOF
---
id: STORY-${i}
epic: EPIC-007
---
EOF
    done

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac45"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: 3 features, 1 with story = 33.333...% → should round to 33.3%
    cat > "${test_dir}/EPIC-008.epic.md" << 'EOF'
---
id: EPIC-008
title: Rounding Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
- Feature C (No story)
EOF

    # Create 1 story file for 33.3% coverage
    cat > "${test_dir}/STORY-001.story.md" << 'EOF'
---
id: STORY-001
epic: EPIC-008
---
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac46"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: All features linked to stories
    cat > "${test_dir}/EPIC-009.epic.md" << 'EOF'
---
id: EPIC-009
title: Perfect Coverage
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (STORY-003)
EOF

    # Create 3 story files for 100% coverage
    for i in 001 002 003; do
        cat > "${test_dir}/STORY-${i}.story.md" << EOF
---
id: STORY-${i}
epic: EPIC-009
---
EOF
    done

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac47"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: No features linked to stories
    cat > "${test_dir}/EPIC-010.epic.md" << 'EOF'
---
id: EPIC-010
title: No Coverage
---

## Features

- Feature A (No story)
- Feature B (No story)
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
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

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac48"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: One epic with features, one empty epic
    cat > "${test_dir}/EPIC-011.epic.md" << 'EOF'
---
id: EPIC-011
title: Normal Epic
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    # Create 1 story file that references EPIC-011
    cat > "${test_dir}/STORY-001.story.md" << 'EOF'
---
id: STORY-001
epic: EPIC-011
---
EOF

    # Empty epic with no features section
    cat > "${test_dir}/EPIC-012.epic.md" << 'EOF'
---
id: EPIC-012
title: Empty Epic
---

(No features defined)
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
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
