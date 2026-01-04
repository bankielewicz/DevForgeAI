#!/bin/bash
#
# Test: NFR-020 - Performance Requirement
# Story: STORY-223 - Catalog Session File Structure and Relationships
#
# NFR-020: Performance
#   Requirement: Catalog 3000+ files within 15 seconds
#   Metric: <15 seconds for full catalog
#   Priority: Medium
#
# Test Framework: Bash shell script with assertions
# Status: FAILING (TDD Red Phase - no implementation exists yet)
#

set -euo pipefail

# Source the shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

# Source the session catalog functions (expected implementation)
# This will fail until the implementation exists
source "$SCRIPT_DIR/../../.claude/scripts/session_catalog.sh" 2>/dev/null || true

# Create temporary test directory
TEST_TEMP_DIR="/tmp/test-story-223-nfr020-$$"
mkdir -p "$TEST_TEMP_DIR"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# Performance thresholds
readonly PERFORMANCE_THRESHOLD_SECONDS=15
readonly FILE_COUNT_TARGET=3000

# ============================================================================
# Helper: Create N test files
# ============================================================================
create_many_test_files() {
    local base_dir="$1"
    local count="${2:-100}"

    mkdir -p "$base_dir/plans"
    mkdir -p "$base_dir/sessions"
    mkdir -p "$base_dir/artifacts"

    local i=0
    while [[ $i -lt $count ]]; do
        # Distribute files across directories
        local file_type=$((i % 3))

        case $file_type in
            0)
                # Plan file
                echo "---
id: PLAN-$i
status: draft
---
# Plan $i" > "$base_dir/plans/plan-$i.md"
                ;;
            1)
                # Session file
                echo "{\"uuid\": \"session-$i\", \"timestamp\": \"2025-01-02T10:00:00Z\"}" > "$base_dir/sessions/session-$i.json"
                ;;
            2)
                # Artifact file
                mkdir -p "$base_dir/artifacts/STORY-$i"
                echo "{\"result\": \"test-$i\"}" > "$base_dir/artifacts/STORY-$i/output.json"
                ;;
        esac

        i=$((i + 1))
    done
}

# ============================================================================
# Test 1: Catalog 100 files within threshold (baseline)
# ============================================================================
test_should_catalog_100_files_quickly() {
    echo "--- Test 1: Catalog 100 files (baseline performance) ---"

    # Arrange: Create 100 test files
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test1")
    create_many_test_files "$test_dir" 100

    # Count files created
    local file_count
    file_count=$(find "$test_dir" -type f | wc -l)
    echo "  Created $file_count test files"

    # Act: Time the catalog operation
    local start_time
    local end_time
    local duration

    if declare -f catalog_session_files &> /dev/null; then
        start_time=$(date +%s.%N)
        catalog_session_files "$test_dir" > /dev/null 2>&1
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)
    else
        # Function doesn't exist - simulate failure
        duration=999
    fi

    # Assert: Should complete within 2 seconds for 100 files
    local threshold=2
    if (( $(echo "$duration < $threshold" | bc -l) )); then
        assert_equal "true" "true" "100 files cataloged in ${duration}s (threshold: ${threshold}s)"
    else
        assert_equal "<$threshold" "$duration" "100 files should be cataloged within ${threshold}s"
    fi
}

# ============================================================================
# Test 2: Catalog 500 files within threshold
# ============================================================================
test_should_catalog_500_files_within_threshold() {
    echo "--- Test 2: Catalog 500 files ---"

    # Arrange: Create 500 test files
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test2")
    create_many_test_files "$test_dir" 500

    local file_count
    file_count=$(find "$test_dir" -type f | wc -l)
    echo "  Created $file_count test files"

    # Act: Time the catalog operation
    local start_time
    local end_time
    local duration

    if declare -f catalog_session_files &> /dev/null; then
        start_time=$(date +%s.%N)
        catalog_session_files "$test_dir" > /dev/null 2>&1
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)
    else
        duration=999
    fi

    # Assert: Should complete within 5 seconds for 500 files
    local threshold=5
    if (( $(echo "$duration < $threshold" | bc -l) )); then
        assert_equal "true" "true" "500 files cataloged in ${duration}s (threshold: ${threshold}s)"
    else
        assert_equal "<$threshold" "$duration" "500 files should be cataloged within ${threshold}s"
    fi
}

# ============================================================================
# Test 3: Catalog 1000 files within threshold
# ============================================================================
test_should_catalog_1000_files_within_threshold() {
    echo "--- Test 3: Catalog 1000 files ---"

    # Arrange: Create 1000 test files
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test3")
    create_many_test_files "$test_dir" 1000

    local file_count
    file_count=$(find "$test_dir" -type f | wc -l)
    echo "  Created $file_count test files"

    # Act: Time the catalog operation
    local start_time
    local end_time
    local duration

    if declare -f catalog_session_files &> /dev/null; then
        start_time=$(date +%s.%N)
        catalog_session_files "$test_dir" > /dev/null 2>&1
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)
    else
        duration=999
    fi

    # Assert: Should complete within 8 seconds for 1000 files
    local threshold=8
    if (( $(echo "$duration < $threshold" | bc -l) )); then
        assert_equal "true" "true" "1000 files cataloged in ${duration}s (threshold: ${threshold}s)"
    else
        assert_equal "<$threshold" "$duration" "1000 files should be cataloged within ${threshold}s"
    fi
}

# ============================================================================
# Test 4: NFR-020 Requirement - Catalog 3000+ files within 15 seconds
# ============================================================================
test_should_catalog_3000_files_within_15_seconds() {
    echo "--- Test 4: NFR-020 - Catalog 3000+ files within 15 seconds ---"

    # Arrange: Create 3000 test files (matches NFR-020 requirement)
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test4")

    echo "  Creating $FILE_COUNT_TARGET test files (this may take a moment)..."
    create_many_test_files "$test_dir" "$FILE_COUNT_TARGET"

    local file_count
    file_count=$(find "$test_dir" -type f | wc -l)
    echo "  Created $file_count test files"

    # Act: Time the catalog operation
    local start_time
    local end_time
    local duration

    if declare -f catalog_session_files &> /dev/null; then
        start_time=$(date +%s.%N)
        catalog_session_files "$test_dir" > /dev/null 2>&1
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)
    else
        # Function doesn't exist - simulate timeout
        duration=999
    fi

    # Assert: MUST complete within 15 seconds (NFR-020 requirement)
    if (( $(echo "$duration < $PERFORMANCE_THRESHOLD_SECONDS" | bc -l) )); then
        assert_equal "true" "true" \
            "NFR-020 PASSED: $FILE_COUNT_TARGET files cataloged in ${duration}s (limit: ${PERFORMANCE_THRESHOLD_SECONDS}s)"
    else
        assert_equal "<$PERFORMANCE_THRESHOLD_SECONDS" "$duration" \
            "NFR-020 FAILED: 3000+ files MUST be cataloged within 15 seconds"
    fi
}

# ============================================================================
# Test 5: Memory efficiency - no excessive memory allocation
# ============================================================================
test_should_have_bounded_memory_usage() {
    echo "--- Test 5: Memory efficiency during large catalog ---"

    # Arrange: Create moderate number of files for memory test
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test5")
    create_many_test_files "$test_dir" 500

    # Act: Measure memory before and after (simplified check)
    local memory_before
    local memory_after

    if declare -f catalog_session_files &> /dev/null; then
        # Get initial memory
        memory_before=$(free -m | awk '/Mem:/ {print $3}' 2>/dev/null || echo "0")

        # Run catalog
        catalog_session_files "$test_dir" > /dev/null 2>&1

        # Get final memory
        memory_after=$(free -m | awk '/Mem:/ {print $3}' 2>/dev/null || echo "0")

        local memory_increase=$((memory_after - memory_before))

        # Assert: Memory increase should be reasonable (< 500MB for 500 files)
        if [[ $memory_increase -lt 500 ]]; then
            assert_equal "true" "true" \
                "Memory efficiency: increased by ${memory_increase}MB (acceptable)"
        else
            assert_equal "<500MB" "${memory_increase}MB" \
                "Memory usage should be bounded during catalog operation"
        fi
    else
        # Function doesn't exist - report as failed
        assert_equal "FUNCTION_EXISTS" "MISSING" \
            "Cannot test memory efficiency - catalog_session_files not implemented"
    fi
}

# ============================================================================
# Test 6: Linear or sub-linear scaling
# ============================================================================
test_should_scale_linearly_or_better() {
    echo "--- Test 6: Scaling behavior (linear or better) ---"

    # Arrange: Create two test sets of different sizes
    local test_dir_small
    local test_dir_large

    test_dir_small=$(create_test_session_dir "$TEST_TEMP_DIR/test6_small")
    test_dir_large=$(create_test_session_dir "$TEST_TEMP_DIR/test6_large")

    create_many_test_files "$test_dir_small" 100
    create_many_test_files "$test_dir_large" 400  # 4x more files

    # Act: Time both operations
    local duration_small=999
    local duration_large=999

    if declare -f catalog_session_files &> /dev/null; then
        # Time small set
        local start_time=$(date +%s.%N)
        catalog_session_files "$test_dir_small" > /dev/null 2>&1
        local end_time=$(date +%s.%N)
        duration_small=$(echo "$end_time - $start_time" | bc)

        # Time large set
        start_time=$(date +%s.%N)
        catalog_session_files "$test_dir_large" > /dev/null 2>&1
        end_time=$(date +%s.%N)
        duration_large=$(echo "$end_time - $start_time" | bc)
    fi

    # Assert: Large set should take at most 6x longer (allowing for some overhead)
    # 4x files with perfect linear scaling = 4x time
    # Allow up to 6x for overhead
    local ratio
    ratio=$(echo "$duration_large / $duration_small" | bc -l 2>/dev/null || echo "999")

    if (( $(echo "$ratio < 6" | bc -l) )); then
        assert_equal "true" "true" \
            "Scaling: 4x files took ${ratio}x time (acceptable, < 6x)"
    else
        assert_equal "<6x" "${ratio}x" \
            "4x files should not take more than 6x time (linear + overhead)"
    fi
}

# ============================================================================
# Test 7: Incremental catalog update performance (if supported)
# ============================================================================
test_incremental_update_should_be_faster_than_full_scan() {
    echo "--- Test 7: Incremental update performance (optional feature) ---"

    # Arrange: Create initial test set
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test7")
    create_many_test_files "$test_dir" 500

    # Act: Time full catalog
    local duration_full=999
    local duration_incremental=999

    if declare -f catalog_session_files &> /dev/null; then
        # Full catalog
        local start_time=$(date +%s.%N)
        catalog_session_files "$test_dir" > /dev/null 2>&1
        local end_time=$(date +%s.%N)
        duration_full=$(echo "$end_time - $start_time" | bc)

        # Add one new file
        echo "new file" > "$test_dir/plans/new-plan.md"

        # Incremental update (if supported)
        if declare -f catalog_incremental_update &> /dev/null; then
            start_time=$(date +%s.%N)
            catalog_incremental_update "$test_dir" > /dev/null 2>&1
            end_time=$(date +%s.%N)
            duration_incremental=$(echo "$end_time - $start_time" | bc)

            # Assert: Incremental should be at least 50% faster
            if (( $(echo "$duration_incremental < $duration_full * 0.5" | bc -l) )); then
                assert_equal "true" "true" \
                    "Incremental update: ${duration_incremental}s vs full: ${duration_full}s (faster)"
            else
                assert_equal "faster_than_50%_full" "${duration_incremental}s" \
                    "Incremental update should be significantly faster than full scan"
            fi
        else
            # Incremental not implemented - informational only
            echo "  INFO: catalog_incremental_update not implemented (optional feature)"
            assert_equal "true" "true" "Incremental update is optional feature"
        fi
    else
        assert_equal "FUNCTION_EXISTS" "MISSING" \
            "Cannot test incremental update - catalog_session_files not implemented"
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: NFR-020 - Performance Requirement"
echo "Story: STORY-223 - Catalog Session File Structure and Relationships"
echo "Requirement: Catalog 3000+ files within 15 seconds"
echo "========================================================================"
echo ""
echo "NOTE: Performance tests create many temporary files."
echo "      This may take a few moments to set up."
echo ""

test_should_catalog_100_files_quickly
echo ""

test_should_catalog_500_files_within_threshold
echo ""

test_should_catalog_1000_files_within_threshold
echo ""

test_should_catalog_3000_files_within_15_seconds
echo ""

test_should_have_bounded_memory_usage
echo ""

test_should_scale_linearly_or_better
echo ""

test_incremental_update_should_be_faster_than_full_scan
echo ""

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "NFR-020 Performance Test Results"
exit_with_result
