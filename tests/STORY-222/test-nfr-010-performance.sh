#!/bin/bash
#
# Test: NFR-010 - Performance Requirement
# Story: STORY-222 - Extract Plan File Knowledge Base for Decision Archive
#
# NFR-010: Performance
#   Requirement: Index 350+ plan files within 10 seconds
#   Metric: <10 seconds for full index
#   Priority: High
#
# Test Framework: Bash shell script with timing assertions
# Status: FAILING (no implementation exists yet)
#

set -euo pipefail

# Source the plan file KB functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.claude/scripts/plan_file_kb.sh" 2>/dev/null || true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Performance tracking
TIMING_RESULTS=""

# Test utilities
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "$expected" == "$actual" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_less_than() {
    local actual="$1"
    local threshold="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ $actual -lt $threshold ]]; then
        echo -e "${GREEN}✓${NC} $message (${actual}ms < ${threshold}ms)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message (${actual}ms >= ${threshold}ms)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Create temporary test directory
TEST_TEMP_DIR="/tmp/test-story-222-nfr-$$"
mkdir -p "$TEST_TEMP_DIR"
mkdir -p "$TEST_TEMP_DIR/plans"
mkdir -p "$TEST_TEMP_DIR/archive"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# Generate test plan files
generate_test_plans() {
    local count=$1
    echo "Generating $count test plan files..."

    for i in $(seq 1 $count); do
        local plan_file="$TEST_TEMP_DIR/plans/plan-$i.md"

        # Create YAML frontmatter
        cat > "$plan_file" << EOF
---
id: PLAN-$i
title: Decision $i
status: approved
created: 2025-01-$(printf '%02d' $((i % 31 + 1)))
author: claude/test
---

# Decision: Architecture Pattern $i

This plan documents decision $i for story references.

Related to STORY-$((1000 + i)) and STORY-$((2000 + i)).

## Rationale
Some content here for decision $i.

## Implementation
Additional details about implementation for decision $i.
EOF
    done

    echo "Generated $count plan files in $TEST_TEMP_DIR/plans/"
}

# ============================================================================
# Test 1: Index 100 plan files within acceptable time
# ============================================================================
test_should_index_100_plans_efficiently() {
    local test_name="Index 100 plan files in <5 seconds"

    # Arrange: Generate 100 plan files
    echo -n "  "
    generate_test_plans 100

    # Act: Time the indexing operation
    if declare -f build_decision_archive &> /dev/null; then
        local start_time=$(date +%s%N)
        build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        local end_time=$(date +%s%N)
        local elapsed_ms=$(( (end_time - start_time) / 1000000 ))
    else
        # No implementation - mark as placeholder
        local elapsed_ms=0
    fi

    # Assert: Should complete in < 5 seconds
    TIMING_RESULTS="${TIMING_RESULTS}100 plans: ${elapsed_ms}ms\n"

    if [[ $elapsed_ms -eq 0 ]]; then
        assert_equal "FUNCTION" "DEFINED" "build_decision_archive function should be defined"
    else
        assert_less_than "$elapsed_ms" "5000" "Index 100 plans in <5 seconds"
    fi
}

# ============================================================================
# Test 2: Index 250 plan files within acceptable time
# ============================================================================
test_should_index_250_plans_efficiently() {
    local test_name="Index 250 plan files in <8 seconds"

    # Arrange: Generate 250 plan files
    echo -n "  "
    generate_test_plans 250

    # Act: Time the indexing operation
    if declare -f build_decision_archive &> /dev/null; then
        local start_time=$(date +%s%N)
        build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        local end_time=$(date +%s%N)
        local elapsed_ms=$(( (end_time - start_time) / 1000000 ))
    else
        local elapsed_ms=0
    fi

    # Assert: Should complete in < 8 seconds
    TIMING_RESULTS="${TIMING_RESULTS}250 plans: ${elapsed_ms}ms\n"

    if [[ $elapsed_ms -eq 0 ]]; then
        assert_equal "FUNCTION" "DEFINED" "build_decision_archive function should be defined"
    else
        assert_less_than "$elapsed_ms" "8000" "Index 250 plans in <8 seconds"
    fi
}

# ============================================================================
# Test 3: Index 350+ plan files (CRITICAL) within 10 seconds
# ============================================================================
test_should_index_350_plans_within_target() {
    local test_name="Index 350+ plan files in <10 seconds (CRITICAL REQUIREMENT)"

    # Arrange: Generate 350 plan files
    echo -n "  "
    generate_test_plans 350

    # Act: Time the indexing operation
    if declare -f build_decision_archive &> /dev/null; then
        echo "  Building decision archive for 350 plans..."
        local start_time=$(date +%s%N)
        build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        local end_time=$(date +%s%N)
        local elapsed_ms=$(( (end_time - start_time) / 1000000 ))
    else
        echo "  WARNING: build_decision_archive function not found (placeholder)"
        local elapsed_ms=0
    fi

    # Assert: CRITICAL - Must complete in < 10 seconds
    TIMING_RESULTS="${TIMING_RESULTS}350 plans: ${elapsed_ms}ms\n"

    if [[ $elapsed_ms -eq 0 ]]; then
        assert_equal "NFR-010" "PENDING" "build_decision_archive implementation pending"
    else
        if [[ $elapsed_ms -lt 10000 ]]; then
            echo -e "${GREEN}✓ CRITICAL: Index 350 plans in ${elapsed_ms}ms (<10s requirement)${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            TESTS_RUN=$((TESTS_RUN + 1))
        else
            echo -e "${RED}✗ CRITICAL: Index 350 plans in ${elapsed_ms}ms (>=10s FAILED)${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            TESTS_RUN=$((TESTS_RUN + 1))
        fi
    fi
}

# ============================================================================
# Test 4: Query performance with 350+ plan archive
# ============================================================================
test_should_query_large_archive_efficiently() {
    local test_name="Query 350+ plan archive in <500ms"

    # Arrange: Archive already built from previous test
    if [[ ! -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
        echo -n "  "
        generate_test_plans 350
        if declare -f build_decision_archive &> /dev/null; then
            build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        fi
    fi

    # Act: Time a query operation
    if declare -f query_archive &> /dev/null; then
        local start_time=$(date +%s%N)
        local result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-1000" 2>/dev/null || echo "")
        local end_time=$(date +%s%N)
        local elapsed_ms=$(( (end_time - start_time) / 1000000 ))
    else
        # Fallback: time a grep search (worst-case for large JSON)
        if [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
            local start_time=$(date +%s%N)
            grep -q "STORY-1000" "$TEST_TEMP_DIR/archive/decision_archive.json" 2>/dev/null || true
            local end_time=$(date +%s%N)
            local elapsed_ms=$(( (end_time - start_time) / 1000000 ))
        else
            local elapsed_ms=0
        fi
    fi

    # Assert: Query should complete in < 500ms
    TIMING_RESULTS="${TIMING_RESULTS}Query (350 plans): ${elapsed_ms}ms\n"

    if [[ $elapsed_ms -eq 0 ]]; then
        assert_equal "ARCHIVE" "EXISTS" "Archive should exist for query testing"
    else
        assert_less_than "$elapsed_ms" "500" "Query 350+ plan archive in <500ms"
    fi
}

# ============================================================================
# Test 5: Incremental indexing performance (add 50 new plans)
# ============================================================================
test_should_handle_incremental_updates() {
    local test_name="Incremental update: add 50 new plans to existing 350"

    # Arrange: Start with existing 350-plan archive
    if [[ ! -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
        echo -n "  "
        generate_test_plans 350
        if declare -f build_decision_archive &> /dev/null; then
            build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        fi
    fi

    # Act: Add 50 more plans and re-index
    echo -n "  "
    echo "Adding 50 new plans to existing 350..."
    for i in $(seq 351 400); do
        cat > "$TEST_TEMP_DIR/plans/plan-$i.md" << EOF
---
id: PLAN-$i
title: Decision $i
---

Related to STORY-$((1000 + i))
EOF
    done

    if declare -f build_decision_archive &> /dev/null; then
        local start_time=$(date +%s%N)
        build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        local end_time=$(date +%s%N)
        local elapsed_ms=$(( (end_time - start_time) / 1000000 ))
    else
        local elapsed_ms=0
    fi

    # Assert: Re-indexing 400 plans should still be reasonable (<12 seconds)
    TIMING_RESULTS="${TIMING_RESULTS}400 plans (incremental): ${elapsed_ms}ms\n"

    if [[ $elapsed_ms -eq 0 ]]; then
        assert_equal "FUNCTION" "DEFINED" "build_decision_archive should support updates"
    else
        assert_less_than "$elapsed_ms" "12000" "Incremental update of 400 plans in <12 seconds"
    fi
}

# ============================================================================
# Test 6: Memory efficiency - archive file size for 350 plans
# ============================================================================
test_should_maintain_reasonable_memory_footprint() {
    local test_name="Archive file size for 350 plans is reasonable (<10MB)"

    # Arrange: Archive should exist from previous tests
    if [[ ! -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
        echo -n "  "
        generate_test_plans 350
        if declare -f build_decision_archive &> /dev/null; then
            build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        fi
    fi

    # Act: Check archive file size
    if [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
        local archive_size=$(stat -f%z "$TEST_TEMP_DIR/archive/decision_archive.json" 2>/dev/null || \
                            stat -c%s "$TEST_TEMP_DIR/archive/decision_archive.json" 2>/dev/null || \
                            du -b "$TEST_TEMP_DIR/archive/decision_archive.json" | cut -f1)
        local size_mb=$((archive_size / 1024 / 1024))
    else
        local size_mb=0
    fi

    # Assert: Archive should be <10MB (efficient representation)
    TIMING_RESULTS="${TIMING_RESULTS}Archive size (350 plans): ${size_mb}MB\n"

    if [[ $size_mb -eq 0 ]]; then
        assert_equal "ARCHIVE" "EXISTS" "Archive file should exist"
    else
        if [[ $size_mb -lt 10 ]]; then
            echo -e "${GREEN}✓${NC} Archive file size is ${size_mb}MB (<10MB)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            TESTS_RUN=$((TESTS_RUN + 1))
        else
            echo -e "${RED}✗${NC} Archive file size is ${size_mb}MB (>=10MB)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            TESTS_RUN=$((TESTS_RUN + 1))
        fi
    fi
}

# ============================================================================
# Test 7: Concurrent query performance
# ============================================================================
test_should_handle_concurrent_queries() {
    local test_name="Handle concurrent queries efficiently"

    # Arrange: Archive from previous tests
    if [[ ! -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
        echo -n "  "
        generate_test_plans 350
        if declare -f build_decision_archive &> /dev/null; then
            build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
        fi
    fi

    # Act: Execute 10 concurrent queries using background jobs
    echo "  Running 10 concurrent queries on 350-plan archive..."
    local total_start=$(date +%s%N)

    for i in {1..10}; do
        (
            if declare -f query_archive &> /dev/null; then
                query_archive "$TEST_TEMP_DIR/archive" "STORY-$((1000 + i))" 2>/dev/null > /dev/null || true
            else
                grep "STORY-$((1000 + i))" "$TEST_TEMP_DIR/archive/decision_archive.json" 2>/dev/null > /dev/null || true
            fi
        ) &
    done
    wait

    local total_end=$(date +%s%N)
    local total_ms=$(( (total_end - total_start) / 1000000 ))

    # Assert: 10 concurrent queries should complete in < 2 seconds
    TIMING_RESULTS="${TIMING_RESULTS}10 concurrent queries: ${total_ms}ms\n"

    assert_less_than "$total_ms" "2000" "Execute 10 concurrent queries in <2 seconds"
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: NFR-010 - Performance Requirement"
echo "Story: STORY-222 - Plan File Knowledge Base"
echo "Requirement: Index 350+ plan files within 10 seconds"
echo "========================================================================"
echo ""

test_should_index_100_plans_efficiently
echo ""

test_should_index_250_plans_efficiently
echo ""

test_should_index_350_plans_within_target
echo ""

test_should_query_large_archive_efficiently
echo ""

test_should_handle_incremental_updates
echo ""

test_should_maintain_reasonable_memory_footprint
echo ""

test_should_handle_concurrent_queries
echo ""

# ============================================================================
# Print summary with timing results
# ============================================================================
echo "========================================================================"
echo "Performance Timing Results"
echo "========================================================================"
echo -e "$TIMING_RESULTS"
echo ""

echo "========================================================================"
echo "Test Results Summary"
echo "========================================================================"
echo "Tests run:    $TESTS_RUN"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo ""

echo "NFR-010 Target: Index 350+ plans in <10 seconds"
if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}RESULT: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
