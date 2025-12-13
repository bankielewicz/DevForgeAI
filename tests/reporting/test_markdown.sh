#!/usr/bin/env bash

# Test suite for AC#2: Markdown Report Generation
# Tests markdown file creation with timestamp filename and proper format

set -euo pipefail

# Test fixtures and helpers
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_FIXTURES_DIR="${SCRIPT_DIR}/fixtures"
TEMP_DIR="${SCRIPT_DIR}/temp"
REPORTS_DIR="${TEMP_DIR}/reports"

# Create temp directories
mkdir -p "${TEMP_DIR}" "${REPORTS_DIR}"

# Cleanup function
cleanup() {
    rm -rf "${TEMP_DIR:?}"
}

trap cleanup EXIT

# ============================================================================
# TEST: AC#2.1 - Should create markdown file with timestamp filename
# ============================================================================
test_should_create_markdown_file_with_timestamp() {
    local test_name="AC#2.1: File created at .devforgeai/epic-coverage/reports/YYYY-MM-DD-HH-MM-SS.md"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-001.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-001
title: Test Epic
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate markdown report
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=markdown \
        --epics-dir="${TEMP_DIR}" \
        --reports-dir="${REPORTS_DIR}" \
        2>/dev/null || true

    # Assert: File exists matching pattern YYYY-MM-DD-HH-MM-SS.md
    if ls "${REPORTS_DIR}"/*-*-*-*-*-*.md 2>/dev/null | grep -q .; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Report file not created with timestamp"
        return 1
    fi
}

# ============================================================================
# TEST: AC#2.2 - Should create reports directory if not exists
# ============================================================================
test_should_create_reports_directory_if_not_exists() {
    local test_name="AC#2.2: Directory created if missing"

    # Arrange: Delete reports directory
    local custom_reports_dir="${TEMP_DIR}/new_reports"
    rm -rf "${custom_reports_dir}"

    local mock_epic="${TEMP_DIR}/EPIC-002.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-002
title: Test Epic
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate markdown report to non-existent directory
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=markdown \
        --epics-dir="${TEMP_DIR}" \
        --reports-dir="${custom_reports_dir}" \
        2>/dev/null || true

    # Assert: Directory exists
    if [[ -d "${custom_reports_dir}" ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Reports directory not created"
        return 1
    fi
}

# ============================================================================
# TEST: AC#2.3 - Markdown should contain summary statistics section
# ============================================================================
test_should_contain_summary_statistics_section() {
    local test_name="AC#2.3: Contains summary statistics section"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-003.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-003
title: Test Epic
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
- Feature C (No story)
EOF

    # Act: Generate markdown report
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=markdown \
        --epics-dir="${TEMP_DIR}" \
        --reports-dir="${REPORTS_DIR}" \
        2>/dev/null || true

    # Get the report file
    local report_file=$(ls "${REPORTS_DIR}"/*-*-*-*-*-*.md 2>/dev/null | head -1)

    # Assert: File contains summary section with table
    if [[ -f "${report_file}" ]] && grep -q "Summary\|summary\|Statistics\|statistics" "${report_file}" && \
       grep -q "|" "${report_file}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing summary statistics section or table"
        return 1
    fi
}

# ============================================================================
# TEST: AC#2.4 - Markdown should contain per-epic breakdown
# ============================================================================
test_should_contain_per_epic_breakdown() {
    local test_name="AC#2.4: Contains per-epic breakdown section"

    # Arrange: Use isolated directory for this test
    local test_epics_dir="${TEMP_DIR}/epics_ac24"
    local test_reports_dir="${TEMP_DIR}/reports_ac24"
    mkdir -p "${test_epics_dir}" "${test_reports_dir}"

    cat > "${test_epics_dir}/EPIC-004.epic.md" << 'EOF'
---
id: EPIC-004
title: Epic Four
---

## Features

- Feature A
EOF

    cat > "${test_epics_dir}/EPIC-005.epic.md" << 'EOF'
---
id: EPIC-005
title: Epic Five
---

## Features

- Feature B
- Feature C
EOF

    # Act: Generate markdown report
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=markdown \
        --epics-dir="${test_epics_dir}" \
        --reports-dir="${test_reports_dir}" \
        2>/dev/null || true

    local report_file=$(ls "${test_reports_dir}"/*-*-*-*-*-*.md 2>/dev/null | head -1)

    # Assert: Report mentions epics by ID
    if [[ -f "${report_file}" ]] && grep -q "EPIC-00[45]\|Epic.*Four\|Epic.*Five" "${report_file}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing per-epic breakdown"
        return 1
    fi
}

# ============================================================================
# TEST: AC#2.5 - Markdown should contain actionable next steps
# ============================================================================
test_should_contain_actionable_next_steps() {
    local test_name="AC#2.5: Contains actionable next steps section"

    # Arrange: Epic with missing features
    local mock_epic="${TEMP_DIR}/EPIC-006.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-006
title: Epic with Gaps
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF

    # Act: Generate markdown report
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=markdown \
        --epics-dir="${TEMP_DIR}" \
        --reports-dir="${REPORTS_DIR}" \
        2>/dev/null || true

    local report_file=$(ls "${REPORTS_DIR}"/*-*-*-*-*-*.md 2>/dev/null | head -1)

    # Assert: File contains next steps section with /create-story commands
    if [[ -f "${report_file}" ]] && grep -q "/create-story\|Next.*[Ss]teps\|Recommendations" "${report_file}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing actionable next steps"
        return 1
    fi
}

# ============================================================================
# TEST: AC#2.6 - Markdown report completion percentages should be accurate
# ============================================================================
test_markdown_completion_percentages_accurate() {
    local test_name="AC#2.6: Completion percentages accurate in markdown"

    # Arrange: Use isolated directories for this test
    local test_epics_dir="${TEMP_DIR}/epics_ac26"
    local test_stories_dir="${TEMP_DIR}/stories_ac26"
    local test_reports_dir="${TEMP_DIR}/reports_ac26"
    mkdir -p "${test_epics_dir}" "${test_stories_dir}" "${test_reports_dir}"

    # Create epic with 4 features
    cat > "${test_epics_dir}/EPIC-007.epic.md" << 'EOF'
---
id: EPIC-007
title: Calculation Test
---

## Features

- Feature A
- Feature B
- Feature C
- Feature D
EOF

    # Create 3 stories linked to this epic (75% coverage)
    for i in 1 2 3; do
        cat > "${test_stories_dir}/STORY-00${i}.story.md" << EOF
---
id: STORY-00${i}
epic: EPIC-007
---
# Story ${i}
EOF
    done

    # Act: Generate markdown report
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=markdown \
        --epics-dir="${test_epics_dir}" \
        --stories-dir="${test_stories_dir}" \
        --reports-dir="${test_reports_dir}" \
        2>/dev/null || true

    local report_file=$(ls "${test_reports_dir}"/*-*-*-*-*-*.md 2>/dev/null | head -1)

    # Assert: Report contains 75% or similar percentage
    if [[ -f "${report_file}" ]] && grep -q "75\.\|75%" "${report_file}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Percentages not accurate"
        return 1
    fi
}

# ============================================================================
# TEST: AC#2.7 - Filename should use ISO 8601-like format
# ============================================================================
test_filename_should_use_iso_format() {
    local test_name="AC#2.7: Filename uses YYYY-MM-DD-HH-MM-SS format"

    # Arrange: Mock epic
    local mock_epic="${TEMP_DIR}/EPIC-008.epic.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-008
title: Format Test
---

## Features

- Feature A (STORY-001)
EOF

    # Act: Generate markdown report
    bash /mnt/c/Projects/DevForgeAI2/.devforgeai/epic-coverage/generate-report.sh \
        --format=markdown \
        --epics-dir="${TEMP_DIR}" \
        --reports-dir="${REPORTS_DIR}" \
        2>/dev/null || true

    # Get report filename
    local report_file=$(ls "${REPORTS_DIR}"/*-*-*-*-*-*.md 2>/dev/null | head -1)
    local filename=$(basename "${report_file}")

    # Assert: Filename matches YYYY-MM-DD-HH-MM-SS.md pattern
    if [[ "${filename}" =~ [0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}\.md$ ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Filename does not match expected format: ${filename}"
        return 1
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
main() {
    echo "=========================================="
    echo "AC#2: Markdown Report Generation"
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
