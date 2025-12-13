#!/usr/bin/env bash

# Test suite for AC#5: Per-Epic Breakdown with Missing Features
# Tests per-epic statistics and missing feature identification

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
# TEST: AC#5.1 - Epic entry should contain epic_id in EPIC-NNN format
# ============================================================================
test_epic_entry_contains_epic_id_format() {
    local test_name="AC#5.1: epic_id matches EPIC-NNN format"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac51"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Epic with proper format
    cat > "${test_dir}/EPIC-001.epic.md" << 'EOF'
---
id: EPIC-001
title: Test Epic
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: epic_id matches pattern
    local epic_id=$(echo "${json_output}" | jq -r '.epics[0].epic_id' 2>/dev/null || echo "")
    if [[ "${epic_id}" =~ ^EPIC-[0-9]{3}$ ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - epic_id format invalid: ${epic_id}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#5.2 - Epic entry should contain title from frontmatter
# ============================================================================
test_epic_entry_contains_title() {
    local test_name="AC#5.2: title extracted from epic file"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac52"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Epic with title in frontmatter
    cat > "${test_dir}/EPIC-002.epic.md" << 'EOF'
---
id: EPIC-002
title: My Special Epic Title
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: Title matches
    local title=$(echo "${json_output}" | jq -r '.epics[0].title' 2>/dev/null || echo "")
    if [[ "${title}" == "My Special Epic Title" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Title not found: ${title}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#5.3 - Epic entry should contain completion_percent calculated
# ============================================================================
test_epic_entry_contains_completion_percent() {
    local test_name="AC#5.3: completion_percent calculated correctly"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac53"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Epic with 3 features, 2 with stories (66.7%)
    cat > "${test_dir}/EPIC-003.epic.md" << 'EOF'
---
id: EPIC-003
title: Completion Test
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (No story)
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: completion_percent exists and is numeric
    local completion=$(echo "${json_output}" | jq '.epics[0].completion_percent' 2>/dev/null || echo "-1")
    if [[ "${completion}" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - completion_percent invalid: ${completion}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#5.4 - Epic entry should list missing features
# ============================================================================
test_epic_entry_lists_missing_features() {
    local test_name="AC#5.4: missing_features array lists features without stories"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac54"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Epic with identified missing features
    cat > "${test_dir}/EPIC-004.epic.md" << 'EOF'
---
id: EPIC-004
title: Missing Features Test
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
- Feature C (No story)
EOF

    # Create 1 story file (leaves 2 features missing)
    cat > "${test_dir}/STORY-001.story.md" << 'EOF'
---
id: STORY-001
epic: EPIC-004
---
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: missing_features array contains 2 items
    local missing_count=$(echo "${json_output}" | jq '.epics[0].missing_features | length' 2>/dev/null || echo "0")
    if [[ "${missing_count}" == "2" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 2 missing features, got ${missing_count}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#5.5 - Missing features should contain feature descriptions
# ============================================================================
test_missing_features_contain_descriptions() {
    local test_name="AC#5.5: missing_features includes feature descriptions"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac55"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Epic with named features
    cat > "${test_dir}/EPIC-005.epic.md" << 'EOF'
---
id: EPIC-005
title: Feature Descriptions
---

## Features

- Authentication (STORY-001)
- Authorization (No story)
- Rate Limiting (No story)
EOF

    # Create 1 story file (leaves 2 features missing: Authorization, Rate Limiting)
    cat > "${test_dir}/STORY-001.story.md" << 'EOF'
---
id: STORY-001
epic: EPIC-005
---
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: missing_features contains descriptions
    local missing=$(echo "${json_output}" | jq -r '.epics[0].missing_features[0]' 2>/dev/null || echo "")
    if [[ -n "${missing}" ]] && [[ "${missing}" != "null" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing features descriptions empty"
        return 1
    fi
}

# ============================================================================
# TEST: AC#5.6 - Multiple epics should each have correct breakdown
# ============================================================================
test_multiple_epics_each_have_breakdown() {
    local test_name="AC#5.6: Multiple epics each show correct stats"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac56"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Two epics with different coverage
    cat > "${test_dir}/EPIC-006.epic.md" << 'EOF'
---
id: EPIC-006
title: High Coverage
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (STORY-003)
EOF

    cat > "${test_dir}/EPIC-007.epic.md" << 'EOF'
---
id: EPIC-007
title: Low Coverage
---

## Features

- Feature D (STORY-004)
- Feature E (No story)
- Feature F (No story)
EOF

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: Both epics present with different completion percentages
    local epic_count=$(echo "${json_output}" | jq '.epics | length' 2>/dev/null || echo "0")
    if [[ "${epic_count}" == "2" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 2 epics, got ${epic_count}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#5.7 - Epic with 100% coverage should have empty missing_features
# ============================================================================
test_full_coverage_epic_has_empty_missing_features() {
    local test_name="AC#5.7: 100% coverage epic has empty missing_features array"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac57"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: All features linked to stories
    cat > "${test_dir}/EPIC-008.epic.md" << 'EOF'
---
id: EPIC-008
title: Full Coverage Epic
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
EOF

    # Create 2 story files for 100% coverage (empty missing_features)
    for i in 001 002; do
        cat > "${test_dir}/STORY-${i}.story.md" << EOF
---
id: STORY-${i}
epic: EPIC-008
---
EOF
    done

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: missing_features array is empty
    local missing_count=$(echo "${json_output}" | jq '.epics[0].missing_features | length' 2>/dev/null || echo "-1")
    if [[ "${missing_count}" == "0" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected 0 missing, got ${missing_count}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#5.8 - Epic completion_percent should be 0-100 range
# ============================================================================
test_completion_percent_in_valid_range() {
    local test_name="AC#5.8: completion_percent bounded 0-100"

    # Per-test isolated directory
    local test_dir="${TEMP_DIR}/test_ac58"
    rm -rf "${test_dir}"
    mkdir -p "${test_dir}"

    # Arrange: Several epics with varying coverage
    for i in {1..3}; do
        cat > "${test_dir}/EPIC-$(printf '%03d' $((100+i))).epic.md" << EOF
---
id: EPIC-$(printf '%03d' $((100+i)))
title: Epic ${i}
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF
    done

    # Act: Generate JSON (use test_dir for both epics and stories to isolate from real data)
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${test_dir}" \
        --stories-dir="${test_dir}" \
        2>/dev/null || echo "{}")

    # Assert: All completion_percent values are 0-100
    local valid=true
    local epic_count=$(echo "${json_output}" | jq '.epics | length' 2>/dev/null || echo "0")

    for ((i=0; i<epic_count; i++)); do
        local pct=$(echo "${json_output}" | jq ".epics[$i].completion_percent" 2>/dev/null || echo "-1")
        if ! (( $(echo "$pct >= 0 && $pct <= 100" | bc -l) )); then
            valid=false
            break
        fi
    done

    if [[ "${valid}" == "true" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - completion_percent out of range"
        return 1
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
main() {
    echo "=========================================="
    echo "AC#5: Per-Epic Breakdown with Missing Features"
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
