#!/usr/bin/env bash

# Test suite for AC#1: Terminal Output with Color-Coded Status
# Tests ANSI color-coded coverage status in terminal output

set -euo pipefail

# Test fixtures and helpers
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_FIXTURES_DIR="${SCRIPT_DIR}/fixtures"
TEMP_DIR="${SCRIPT_DIR}/temp"

# ANSI color codes (use $'...' syntax for escape sequence interpretation)
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
RED=$'\033[31m'
RESET=$'\033[0m'

# Create temp directory
mkdir -p "${TEMP_DIR}"

# Cleanup function
cleanup() {
    rm -rf "${TEMP_DIR:?}"
}

trap cleanup EXIT

# ============================================================================
# TEST: AC#1.1 - Should display green color for 100% coverage
# ============================================================================
test_should_display_green_color_for_perfect_coverage() {
    local test_name="AC#1.1: Green color (100% coverage)"

    # Arrange: Mock epic with 100% coverage (all features have stories)
    local mock_epic="${TEMP_DIR}/EPIC-001.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-001
title: Test Epic
priority: High
---

## Features

### Feature 1.1: Feature A
**Description:** First test feature

### Feature 1.2: Feature B
**Description:** Second test feature
EOF

    # Create mock stories that link to the epic
    cat > "${TEMP_DIR}/STORY-001.md" << 'EOF'
---
id: STORY-001
epic: EPIC-001
---
EOF
    cat > "${TEMP_DIR}/STORY-002.md" << 'EOF'
---
id: STORY-002
epic: EPIC-001
---
EOF

    # Act: Generate terminal output
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        --stories-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Output contains green ANSI code
    if echo "${output}" | grep -qF "${GREEN}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing green color code"
        return 1
    fi
}

# ============================================================================
# TEST: AC#1.2 - Should display yellow color for 50-99% coverage
# ============================================================================
test_should_display_yellow_color_for_partial_coverage() {
    local test_name="AC#1.2: Yellow color (50-99% coverage)"

    # Arrange: Mock epic with 75% coverage (3 of 4 features have stories)
    local mock_epic="${TEMP_DIR}/EPIC-002.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-002
title: Partial Coverage Epic
priority: High
---

## Features

### Feature 1.1: Feature A
**Description:** Feature with story

### Feature 1.2: Feature B
**Description:** Feature with story

### Feature 1.3: Feature C
**Description:** Feature with story

### Feature 1.4: Feature D
**Description:** Feature without story
EOF

    # Create mock stories that link to the epic
    cat > "${TEMP_DIR}/STORY-003.md" << 'EOF'
---
id: STORY-003
epic: EPIC-002
---
EOF
    cat > "${TEMP_DIR}/STORY-004.md" << 'EOF'
---
id: STORY-004
epic: EPIC-002
---
EOF
    cat > "${TEMP_DIR}/STORY-005.md" << 'EOF'
---
id: STORY-005
epic: EPIC-002
---
EOF

    # Act: Generate terminal output
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        --stories-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Output contains yellow ANSI code
    if echo "${output}" | grep -qF "${YELLOW}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing yellow color code"
        return 1
    fi
}

# ============================================================================
# TEST: AC#1.3 - Should display red color for <50% coverage
# ============================================================================
test_should_display_red_color_for_low_coverage() {
    local test_name="AC#1.3: Red color (<50% coverage)"

    # Arrange: Mock epic with 25% coverage (1 of 4 features have stories)
    local mock_epic="${TEMP_DIR}/EPIC-003.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-003
title: Low Coverage Epic
priority: High
---

## Features

### Feature 1.1: Feature A
**Description:** Feature with story

### Feature 1.2: Feature B
**Description:** Feature without story

### Feature 1.3: Feature C
**Description:** Feature without story

### Feature 1.4: Feature D
**Description:** Feature without story
EOF

    # Create mock story that links to the epic
    cat > "${TEMP_DIR}/STORY-006.md" << 'EOF'
---
id: STORY-006
epic: EPIC-003
---
EOF

    # Act: Generate terminal output
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        --stories-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Output contains red ANSI code
    if echo "${output}" | grep -qF "${RED}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing red color code"
        return 1
    fi
}

# ============================================================================
# TEST: AC#1.4 - Should display epic coverage percentage with color
# ============================================================================
test_should_display_epic_coverage_percentage_with_color() {
    local test_name="AC#1.4: Epic coverage % with color coding"

    # Arrange: Mock epic with known coverage
    local mock_epic="${TEMP_DIR}/EPIC-004.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-004
title: Measurement Epic
priority: Medium
---

## Features

### Feature 1.1: Feature A
**Description:** Feature with story

### Feature 1.2: Feature B
**Description:** Feature with story

### Feature 1.3: Feature C
**Description:** Feature without story
EOF

    # Create mock stories that link to the epic
    cat > "${TEMP_DIR}/STORY-007.md" << 'EOF'
---
id: STORY-007
epic: EPIC-004
---
EOF
    cat > "${TEMP_DIR}/STORY-008.md" << 'EOF'
---
id: STORY-008
epic: EPIC-004
---
EOF

    # Act: Generate terminal output
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        --stories-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Output contains percentage (66.7% or similar)
    if echo "${output}" | grep -qE '[0-9]+\.[0-9]%|[0-9]+%'; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing coverage percentage"
        return 1
    fi
}

# ============================================================================
# TEST: AC#1.5 - Should display summary line with overall coverage color
# ============================================================================
test_should_display_summary_with_overall_coverage_color() {
    local test_name="AC#1.5: Summary line with overall coverage color"

    # Arrange: Mock multiple epics for overall calculation
    cat > "${TEMP_DIR}/EPIC-005.epic.md" << 'EOF'
---
id: EPIC-005
title: Epic Five
priority: High
---

## Features

### Feature 1.1: Feature A
**Description:** Feature with story

### Feature 1.2: Feature B
**Description:** Feature with story
EOF

    cat > "${TEMP_DIR}/EPIC-006.epic.md" << 'EOF'
---
id: EPIC-006
title: Epic Six
priority: Medium
---

## Features

### Feature 1.1: Feature C
**Description:** Feature with story

### Feature 1.2: Feature D
**Description:** Feature without story
EOF

    # Create mock stories that link to the epics
    cat > "${TEMP_DIR}/STORY-009.md" << 'EOF'
---
id: STORY-009
epic: EPIC-005
---
EOF
    cat > "${TEMP_DIR}/STORY-010.md" << 'EOF'
---
id: STORY-010
epic: EPIC-005
---
EOF
    cat > "${TEMP_DIR}/STORY-011.md" << 'EOF'
---
id: STORY-011
epic: EPIC-006
---
EOF

    # Act: Generate terminal output
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        --stories-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Output contains summary line with color (check for Overall and any color)
    if echo "${output}" | grep -q "Overall" && (echo "${output}" | grep -qF "${GREEN}" || echo "${output}" | grep -qF "${YELLOW}" || echo "${output}" | grep -qF "${RED}"); then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing summary line or color"
        return 1
    fi
}

# ============================================================================
# TEST: AC#1.6 - Should reset color after colored output
# ============================================================================
test_should_reset_color_after_output() {
    local test_name="AC#1.6: Color reset (ANSI reset code)"

    # Arrange: Any valid epic
    local mock_epic="${TEMP_DIR}/EPIC-007.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-007
title: Reset Test Epic
priority: High
---

## Features

### Feature 1.1: Feature A
**Description:** Feature with story
EOF

    # Create mock story that links to the epic
    cat > "${TEMP_DIR}/STORY-012.md" << 'EOF'
---
id: STORY-012
epic: EPIC-007
---
EOF

    # Act: Generate terminal output
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        --stories-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Output contains ANSI reset code
    if echo "${output}" | grep -qF "${RESET}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing color reset code"
        return 1
    fi
}

# ============================================================================
# TEST: AC#1.7 - Boundary condition: 50% should be yellow not red
# ============================================================================
test_boundary_50_percent_should_be_yellow() {
    local test_name="AC#1.7: Boundary - 50% exactly shows yellow"

    # Arrange: Mock epic with exactly 50% coverage (2 of 4 features)
    local mock_epic="${TEMP_DIR}/EPIC-008.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-008
title: Boundary Epic
priority: High
---

## Features

### Feature 1.1: Feature A
**Description:** Feature with story

### Feature 1.2: Feature B
**Description:** Feature with story

### Feature 1.3: Feature C
**Description:** Feature without story

### Feature 1.4: Feature D
**Description:** Feature without story
EOF

    # Create mock stories that link to the epic
    cat > "${TEMP_DIR}/STORY-013.md" << 'EOF'
---
id: STORY-013
epic: EPIC-008
---
EOF
    cat > "${TEMP_DIR}/STORY-014.md" << 'EOF'
---
id: STORY-014
epic: EPIC-008
---
EOF

    # Act: Generate terminal output
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        --stories-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Should contain yellow, not red
    if echo "${output}" | grep -qF "${YELLOW}" && ! echo "${output}" | grep -qF "${RED}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Boundary condition not met"
        return 1
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
main() {
    echo "=========================================="
    echo "AC#1: Terminal Output - Color-Coded Status"
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
