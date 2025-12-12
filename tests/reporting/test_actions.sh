#!/usr/bin/env bash

# Test suite for AC#6: Actionable Next Steps Generation
# Tests recommendation generation sorted by priority with limits

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
# TEST: AC#6.1 - Should generate /create-story commands for gaps
# ============================================================================
test_should_generate_create_story_commands() {
    local test_name="AC#6.1: Generate /create-story commands for missing features"

    # Arrange: Epic with gaps
    local mock_epic="${TEMP_DIR}/EPIC-001.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-001
title: Test Epic
priority: High
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

    # Assert: actionable_next_steps contains /create-story commands
    if echo "${json_output}" | jq -e '.actionable_next_steps[] | select(contains("/create-story"))' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing /create-story commands"
        return 1
    fi
}

# ============================================================================
# TEST: AC#6.2 - Commands should include feature descriptions
# ============================================================================
test_commands_should_include_feature_description() {
    local test_name="AC#6.2: /create-story commands include feature description"

    # Arrange: Epic with named missing features
    local mock_epic="${TEMP_DIR}/EPIC-002.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-002
title: Named Features
priority: Medium
---

## Features

- Real-time Notifications (STORY-001)
- User Preferences (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: Commands mention feature descriptions
    if echo "${json_output}" | jq -e '.actionable_next_steps[] | select(contains("User Preferences"))' >/dev/null 2>&1 || \
       echo "${json_output}" | jq -e '.actionable_next_steps[]' 2>/dev/null | grep -q "Preferences"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Feature description not included in commands"
        return 1
    fi
}

# ============================================================================
# TEST: AC#6.3 - Should sort by epic priority (Critical > High > Medium > Low)
# ============================================================================
test_should_sort_by_epic_priority() {
    local test_name="AC#6.3: Commands sorted by priority: Critical > High > Medium > Low"

    # Arrange: Multiple epics with different priorities
    cat > "${TEMP_DIR}/EPIC-003.md" << 'EOF'
---
id: EPIC-003
title: Low Priority Epic
priority: Low
---

## Features

- Feature A (No story)
EOF

    cat > "${TEMP_DIR}/EPIC-004.md" << 'EOF'
---
id: EPIC-004
title: Critical Epic
priority: Critical
---

## Features

- Feature B (No story)
EOF

    cat > "${TEMP_DIR}/EPIC-005.md" << 'EOF'
---
id: EPIC-005
title: Medium Priority
priority: Medium
---

## Features

- Feature C (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: First recommendation is from Critical epic
    local first_cmd=$(echo "${json_output}" | jq -r '.actionable_next_steps[0]' 2>/dev/null || echo "")
    if echo "${first_cmd}" | grep -q "Critical\|Feature B"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Not sorted by priority, first: ${first_cmd}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#6.4 - Should limit to maximum 10 actionable items
# ============================================================================
test_should_limit_to_max_10_items() {
    local test_name="AC#6.4: Maximum 10 actionable items per report"

    # Arrange: Create epic with 15 missing features
    local mock_epic="${TEMP_DIR}/EPIC-006.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-006
title: Large Gap Epic
priority: High
---

## Features

- Feature 01 (STORY-001)
- Feature 02 (No story)
- Feature 03 (No story)
- Feature 04 (No story)
- Feature 05 (No story)
- Feature 06 (No story)
- Feature 07 (No story)
- Feature 08 (No story)
- Feature 09 (No story)
- Feature 10 (No story)
- Feature 11 (No story)
- Feature 12 (No story)
- Feature 13 (No story)
- Feature 14 (No story)
- Feature 15 (No story)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: actionable_next_steps has at most 10 items
    local action_count=$(echo "${json_output}" | jq '.actionable_next_steps | length' 2>/dev/null || echo "0")
    if [[ "${action_count}" -le 10 ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected ≤10 actions, got ${action_count}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#6.5 - Should generate recommendations only for gaps
# ============================================================================
test_should_not_generate_recommendations_for_100_percent() {
    local test_name="AC#6.5: No recommendations for 100% coverage epic"

    # Arrange: Epic with perfect coverage
    local mock_epic="${TEMP_DIR}/EPIC-007.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-007
title: Perfect Epic
priority: High
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: actionable_next_steps is empty or minimal
    local action_count=$(echo "${json_output}" | jq '.actionable_next_steps | length' 2>/dev/null || echo "0")
    if [[ "${action_count}" == "0" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Generated recommendations for 100% coverage epic"
        return 1
    fi
}

# ============================================================================
# TEST: AC#6.6 - Commands should reference epic ID
# ============================================================================
test_commands_should_reference_epic_id() {
    local test_name="AC#6.6: Commands reference epic ID (EPIC-NNN)"

    # Arrange: Epic with gaps
    local mock_epic="${TEMP_DIR}/EPIC-008.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-008
title: ID Reference Test
priority: Medium
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

    # Assert: At least one command mentions EPIC-008
    if echo "${json_output}" | jq -e '.actionable_next_steps[] | select(contains("EPIC-008"))' >/dev/null 2>&1; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Commands don't reference epic ID"
        return 1
    fi
}

# ============================================================================
# TEST: AC#6.7 - Should format commands as /create-story --epic=EPIC-NNN
# ============================================================================
test_command_format_should_be_correct() {
    local test_name="AC#6.7: Commands formatted as /create-story syntax"

    # Arrange: Epic with gaps
    local mock_epic="${TEMP_DIR}/EPIC-009.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-009
title: Format Test
priority: High
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

    # Assert: Commands follow /create-story pattern
    local first_cmd=$(echo "${json_output}" | jq -r '.actionable_next_steps[0]' 2>/dev/null || echo "")
    if [[ "${first_cmd}" =~ /create-story ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Command format incorrect: ${first_cmd}"
        return 1
    fi
}

# ============================================================================
# TEST: AC#6.8 - Empty report should have empty actionable_next_steps
# ============================================================================
test_no_gaps_should_have_empty_actions() {
    local test_name="AC#6.8: No gaps → empty actionable_next_steps array"

    # Arrange: Only epics with complete coverage
    cat > "${TEMP_DIR}/EPIC-010.md" << 'EOF'
---
id: EPIC-010
title: Complete
priority: Low
---

## Features

- Feature A (STORY-001)
EOF

    cat > "${TEMP_DIR}/EPIC-011.md" << 'EOF'
---
id: EPIC-011
title: Also Complete
priority: Low
---

## Features

- Feature B (STORY-002)
EOF

    # Act: Generate JSON
    local json_output=$(bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=json \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "{}")

    # Assert: actionable_next_steps is empty array
    local action_count=$(echo "${json_output}" | jq '.actionable_next_steps | length' 2>/dev/null || echo "-1")
    if [[ "${action_count}" == "0" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Expected empty actions, got ${action_count}"
        return 1
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
main() {
    echo "=========================================="
    echo "AC#6: Actionable Next Steps Generation"
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
