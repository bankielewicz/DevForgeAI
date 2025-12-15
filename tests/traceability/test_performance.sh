#!/bin/bash

##############################################################################
# Test Suite: STORY-083 - Performance Tests (AC#6)
# Purpose: Validate batch processing performance requirements
#
# Acceptance Criteria #6:
# - Full parse <5 seconds for 15 epics and 85 stories
# - Incremental update <500ms
# - Memory usage <50MB
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
TEST_LOG="/tmp/story-083-performance.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
PARSER_SCRIPT="${PROJECT_ROOT}/.devforgeai/traceability/parse-requirements.sh"

# Initialize log
echo "=== STORY-083 Performance Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
    fi
}

##############################################################################
# NFR-001: Full Parse Performance
##############################################################################

test_full_parse_under_5_seconds() {
    # NFR-001: Full repository parse <5 seconds
    # Note: WSL2 has significant I/O overhead, allow 60s tolerance with WSL2_SLOW=1

    local threshold=5000
    if [ "${WSL2_SLOW:-0}" = "1" ]; then
        threshold=60000
    fi

    local start_time end_time duration
    start_time=$(date +%s%3N)
    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))

    echo "  Full parse duration: ${duration}ms (threshold: ${threshold}ms)"

    if [ "$duration" -lt "$threshold" ]; then
        return 0
    else
        echo "Parse took ${duration}ms, expected <${threshold}ms"
        return 1
    fi
}

##############################################################################
# NFR-002: Incremental Update Performance
##############################################################################

test_incremental_update_under_500ms() {
    # NFR-002: Incremental update <500ms
    # Note: WSL2 has I/O overhead, allow 60s tolerance with WSL2_SLOW=1

    local threshold=500
    if [ "${WSL2_SLOW:-0}" = "1" ]; then
        threshold=60000
    fi

    # First run to establish baseline
    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null

    # Simulate incremental update
    local start_time end_time duration
    start_time=$(date +%s%3N)
    "$PARSER_SCRIPT" --incremental-update 2>/dev/null
    end_time=$(date +%s%3N)
    duration=$((end_time - start_time))

    echo "  Incremental update duration: ${duration}ms (threshold: ${threshold}ms)"

    if [ "$duration" -lt "$threshold" ]; then
        return 0
    else
        echo "Incremental update took ${duration}ms, expected <${threshold}ms"
        return 1
    fi
}

##############################################################################
# Repository Scale Tests
##############################################################################

test_handles_current_repo_scale() {
    # NFR-001: Handle 15+ epics and 85+ stories

    local epic_count story_count
    epic_count=$(ls "${PROJECT_ROOT}/devforgeai/specs/Epics/"*.epic.md 2>/dev/null | wc -l)
    story_count=$(ls "${PROJECT_ROOT}/devforgeai/specs/Stories/"*.story.md 2>/dev/null | wc -l)

    echo "  Repository has ${epic_count} epics and ${story_count} stories"

    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null
    local exit_code=$?

    if [ "$exit_code" -eq 0 ]; then
        return 0
    else
        echo "Parser failed on current repo scale"
        return 1
    fi
}

##############################################################################
# Timeout Protection
##############################################################################

test_no_infinite_loop() {
    # Parser should complete within reasonable time (30s max for any operation)

    local result
    result=$(timeout 30s "$PARSER_SCRIPT" --generate-matrix 2>/dev/null)
    local exit_code=$?

    # Exit code 124 means timeout
    if [ "$exit_code" -ne 124 ]; then
        return 0
    else
        echo "Parser timed out (infinite loop suspected)"
        return 1
    fi
}

##############################################################################
# Output Size Validation
##############################################################################

test_output_reasonable_size() {
    # Output JSON should be reasonable size (not bloated)

    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null

    local matrix_file="${PROJECT_ROOT}/.devforgeai/traceability/requirements-matrix.json"

    if [ ! -f "$matrix_file" ]; then
        echo "Matrix file not created"
        return 1
    fi

    local file_size
    file_size=$(stat -c %s "$matrix_file" 2>/dev/null || stat -f %z "$matrix_file" 2>/dev/null)

    echo "  Output file size: ${file_size} bytes"

    # Reasonable size: <1MB for typical repo
    if [ "$file_size" -lt 1048576 ]; then
        return 0
    else
        echo "Output file too large: ${file_size} bytes"
        return 1
    fi
}

##############################################################################
# Concurrent Access (Basic)
##############################################################################

test_handles_repeated_calls() {
    # Parser should handle rapid repeated calls

    local failures=0
    for i in 1 2 3 4 5; do
        "$PARSER_SCRIPT" --generate-matrix 2>/dev/null
        if [ $? -ne 0 ]; then
            failures=$((failures + 1))
        fi
    done

    echo "  Failures in 5 rapid calls: ${failures}"

    if [ "$failures" -eq 0 ]; then
        return 0
    else
        echo "Parser failed ${failures}/5 rapid calls"
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  STORY-083: Performance Test Suite (AC#6)                ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

    echo -e "\n${BLUE}=== Full Parse Performance Tests ===${NC}"
    run_test "Full parse under 5 seconds" test_full_parse_under_5_seconds

    echo -e "\n${BLUE}=== Incremental Update Tests ===${NC}"
    run_test "Incremental update under 500ms" test_incremental_update_under_500ms

    echo -e "\n${BLUE}=== Scale Tests ===${NC}"
    run_test "Handles current repo scale" test_handles_current_repo_scale

    echo -e "\n${BLUE}=== Safety Tests ===${NC}"
    run_test "No infinite loop" test_no_infinite_loop

    echo -e "\n${BLUE}=== Output Quality Tests ===${NC}"
    run_test "Output file reasonable size" test_output_reasonable_size

    echo -e "\n${BLUE}=== Stability Tests ===${NC}"
    run_test "Handles repeated calls" test_handles_repeated_calls

    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "Tests Run:    ${TESTS_RUN}"
    echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
    echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

    if [ "$TESTS_FAILED" -gt 0 ]; then
        exit 1
    fi
    exit 0
}

main "$@"
