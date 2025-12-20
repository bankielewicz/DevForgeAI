#!/bin/bash
# STORY-110: Error Handling Patterns for Parallel Orchestration
# Test Suite: Documentation Structure Validation
# TDD Phase: Red (tests written before implementation)

# set -e  # Disabled to allow all tests to run

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass() {
    ((TESTS_PASSED++))
    echo -e "${GREEN}PASS${NC}: $1"
}

fail() {
    ((TESTS_FAILED++))
    echo -e "${RED}FAIL${NC}: $1"
}

skip() {
    echo -e "${YELLOW}SKIP${NC}: $1"
}

# Resolve project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
REFS_DIR="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references"

echo "=== STORY-110: Error Handling Patterns Test Suite ==="
echo "Project Root: $PROJECT_ROOT"
echo "References Dir: $REFS_DIR"
echo ""

# =============================================================================
# AC#1: Partial Failure Recovery - error-handling-patterns.md
# =============================================================================
echo "--- AC#1: Partial Failure Recovery Tests ---"

test_error_handling_file_exists() {
    ((TESTS_RUN++))
    if [[ -f "$REFS_DIR/error-handling-patterns.md" ]]; then
        pass "error-handling-patterns.md exists"
    else
        fail "error-handling-patterns.md does not exist"
    fi
}

test_error_handling_partial_failure_section() {
    ((TESTS_RUN++))
    if grep -q "## Partial Failure Recovery Pattern" "$REFS_DIR/error-handling-patterns.md" 2>/dev/null; then
        pass "Partial Failure Recovery Pattern section exists"
    else
        fail "Partial Failure Recovery Pattern section missing"
    fi
}

test_error_handling_result_aggregation_section() {
    ((TESTS_RUN++))
    if grep -q "## Result Aggregation Pattern" "$REFS_DIR/error-handling-patterns.md" 2>/dev/null; then
        pass "Result Aggregation Pattern section exists"
    else
        fail "Result Aggregation Pattern section missing"
    fi
}

test_error_handling_failure_logging_section() {
    ((TESTS_RUN++))
    if grep -q "## Failure Logging Pattern" "$REFS_DIR/error-handling-patterns.md" 2>/dev/null; then
        pass "Failure Logging Pattern section exists"
    else
        fail "Failure Logging Pattern section missing"
    fi
}

test_error_handling_partial_result_model() {
    ((TESTS_RUN++))
    local file="$REFS_DIR/error-handling-patterns.md"
    if grep -q "PartialResult" "$file" 2>/dev/null && \
       grep -q "successes" "$file" 2>/dev/null && \
       grep -q "failures" "$file" 2>/dev/null && \
       grep -q "total_tasks" "$file" 2>/dev/null && \
       grep -q "success_rate" "$file" 2>/dev/null; then
        pass "PartialResult data model documented"
    else
        fail "PartialResult data model incomplete or missing"
    fi
}

test_error_handling_task_failure_model() {
    ((TESTS_RUN++))
    local file="$REFS_DIR/error-handling-patterns.md"
    if grep -q "TaskFailure" "$file" 2>/dev/null && \
       grep -q "task_id" "$file" 2>/dev/null && \
       grep -q "error_type" "$file" 2>/dev/null && \
       grep -q "error_message" "$file" 2>/dev/null && \
       grep -q "retry_count" "$file" 2>/dev/null && \
       grep -q "is_retryable" "$file" 2>/dev/null; then
        pass "TaskFailure data model documented"
    else
        fail "TaskFailure data model incomplete or missing"
    fi
}

test_error_handling_3_success_2_failure_example() {
    ((TESTS_RUN++))
    # Test requirement: "Test: 3 success + 2 failure scenario handled correctly"
    local file="$REFS_DIR/error-handling-patterns.md"
    if grep -qE "(3.*success.*2.*fail|3/5|60%)" "$file" 2>/dev/null; then
        pass "3 success + 2 failure scenario example documented"
    else
        fail "3 success + 2 failure scenario example missing"
    fi
}

test_error_handling_br001_documented() {
    ((TESTS_RUN++))
    # BR-001: Partial success continues workflow if success_rate >= min_success_rate
    local file="$REFS_DIR/error-handling-patterns.md"
    if grep -qE "(min_success_rate|success_rate.*threshold|BR-001)" "$file" 2>/dev/null; then
        pass "BR-001 (min_success_rate threshold) documented"
    else
        fail "BR-001 (min_success_rate threshold) not documented"
    fi
}

# Run AC#1 tests
test_error_handling_file_exists
test_error_handling_partial_failure_section
test_error_handling_result_aggregation_section
test_error_handling_failure_logging_section
test_error_handling_partial_result_model
test_error_handling_task_failure_model
test_error_handling_3_success_2_failure_example
test_error_handling_br001_documented

echo ""

# =============================================================================
# AC#2: Timeout Handling - timeout-handling.md
# =============================================================================
echo "--- AC#2: Timeout Handling Tests ---"

test_timeout_handling_file_exists() {
    ((TESTS_RUN++))
    if [[ -f "$REFS_DIR/timeout-handling.md" ]]; then
        pass "timeout-handling.md exists"
    else
        fail "timeout-handling.md does not exist"
    fi
}

test_timeout_monitoring_section() {
    ((TESTS_RUN++))
    if grep -q "## Timeout Monitoring Pattern" "$REFS_DIR/timeout-handling.md" 2>/dev/null; then
        pass "Timeout Monitoring Pattern section exists"
    else
        fail "Timeout Monitoring Pattern section missing"
    fi
}

test_killshell_integration_section() {
    ((TESTS_RUN++))
    if grep -q "## KillShell Integration" "$REFS_DIR/timeout-handling.md" 2>/dev/null; then
        pass "KillShell Integration section exists"
    else
        fail "KillShell Integration section missing"
    fi
}

test_timeout_logging_section() {
    ((TESTS_RUN++))
    if grep -q "## Timeout Logging Pattern" "$REFS_DIR/timeout-handling.md" 2>/dev/null; then
        pass "Timeout Logging Pattern section exists"
    else
        fail "Timeout Logging Pattern section missing"
    fi
}

test_timeout_ms_config_reference() {
    ((TESTS_RUN++))
    local file="$REFS_DIR/timeout-handling.md"
    if grep -q "timeout_ms" "$file" 2>/dev/null; then
        pass "timeout_ms configuration referenced"
    else
        fail "timeout_ms configuration not referenced"
    fi
}

test_killshell_tool_documented() {
    ((TESTS_RUN++))
    local file="$REFS_DIR/timeout-handling.md"
    if grep -qE "(KillShell|shell_id)" "$file" 2>/dev/null; then
        pass "KillShell tool usage documented"
    else
        fail "KillShell tool usage not documented"
    fi
}

test_timeout_log_format() {
    ((TESTS_RUN++))
    # Test requirement: "Test: Timeout log includes task_id, duration, timeout_ms"
    local file="$REFS_DIR/timeout-handling.md"
    if grep -q "task_id" "$file" 2>/dev/null && \
       grep -q "duration" "$file" 2>/dev/null; then
        pass "Timeout log format documented (task_id, duration)"
    else
        fail "Timeout log format incomplete"
    fi
}

# Run AC#2 tests
test_timeout_handling_file_exists
test_timeout_monitoring_section
test_killshell_integration_section
test_timeout_logging_section
test_timeout_ms_config_reference
test_killshell_tool_documented
test_timeout_log_format

echo ""

# =============================================================================
# AC#3: Retry Logic - retry-patterns.md
# =============================================================================
echo "--- AC#3: Retry Logic Tests ---"

test_retry_patterns_file_exists() {
    ((TESTS_RUN++))
    if [[ -f "$REFS_DIR/retry-patterns.md" ]]; then
        pass "retry-patterns.md exists"
    else
        fail "retry-patterns.md does not exist"
    fi
}

test_exponential_backoff_section() {
    ((TESTS_RUN++))
    if grep -q "## Exponential Backoff Pattern" "$REFS_DIR/retry-patterns.md" 2>/dev/null; then
        pass "Exponential Backoff Pattern section exists"
    else
        fail "Exponential Backoff Pattern section missing"
    fi
}

test_error_classification_section() {
    ((TESTS_RUN++))
    if grep -q "## Error Classification" "$REFS_DIR/retry-patterns.md" 2>/dev/null; then
        pass "Error Classification section exists"
    else
        fail "Error Classification section missing"
    fi
}

test_max_attempts_section() {
    ((TESTS_RUN++))
    if grep -q "## Max Attempts Pattern" "$REFS_DIR/retry-patterns.md" 2>/dev/null; then
        pass "Max Attempts Pattern section exists"
    else
        fail "Max Attempts Pattern section missing"
    fi
}

test_exponential_backoff_formula() {
    ((TESTS_RUN++))
    # Test requirement: delay = base_delay_ms * (2 ^ attempt_number)
    local file="$REFS_DIR/retry-patterns.md"
    if grep -qE "(base_delay.*2.*attempt|exponential|2\^)" "$file" 2>/dev/null; then
        pass "Exponential backoff formula documented"
    else
        fail "Exponential backoff formula not documented"
    fi
}

test_error_classification_transient_permanent() {
    ((TESTS_RUN++))
    # Test requirement: "Test: Rate limit = transient, ValidationError = permanent"
    local file="$REFS_DIR/retry-patterns.md"
    if grep -qiE "(transient|permanent)" "$file" 2>/dev/null; then
        pass "Transient vs permanent error classification documented"
    else
        fail "Transient vs permanent error classification not documented"
    fi
}

test_max_attempts_config() {
    ((TESTS_RUN++))
    local file="$REFS_DIR/retry-patterns.md"
    if grep -q "max_attempts" "$file" 2>/dev/null; then
        pass "max_attempts configuration documented"
    else
        fail "max_attempts configuration not documented"
    fi
}

test_br002_documented() {
    ((TESTS_RUN++))
    # BR-002: Transient errors are retried; permanent errors are not
    local file="$REFS_DIR/retry-patterns.md"
    if grep -qiE "(transient.*retr|permanent.*not.*retr|BR-002)" "$file" 2>/dev/null; then
        pass "BR-002 (transient retry, permanent no-retry) documented"
    else
        fail "BR-002 (transient retry, permanent no-retry) not documented"
    fi
}

test_br003_documented() {
    ((TESTS_RUN++))
    # BR-003: Exponential backoff doubles delay on each retry, cap at max_backoff_ms
    local file="$REFS_DIR/retry-patterns.md"
    if grep -qE "(max_backoff|backoff.*cap|BR-003)" "$file" 2>/dev/null; then
        pass "BR-003 (max_backoff_ms cap) documented"
    else
        fail "BR-003 (max_backoff_ms cap) not documented"
    fi
}

# Run AC#3 tests
test_retry_patterns_file_exists
test_exponential_backoff_section
test_error_classification_section
test_max_attempts_section
test_exponential_backoff_formula
test_error_classification_transient_permanent
test_max_attempts_config
test_br002_documented
test_br003_documented

echo ""

# =============================================================================
# AC#4: Fallback to Sequential - sequential-fallback.md
# =============================================================================
echo "--- AC#4: Fallback to Sequential Tests ---"

test_sequential_fallback_file_exists() {
    ((TESTS_RUN++))
    if [[ -f "$REFS_DIR/sequential-fallback.md" ]]; then
        pass "sequential-fallback.md exists"
    else
        fail "sequential-fallback.md does not exist"
    fi
}

test_complete_failure_detection_section() {
    ((TESTS_RUN++))
    if grep -q "## Complete Failure Detection" "$REFS_DIR/sequential-fallback.md" 2>/dev/null; then
        pass "Complete Failure Detection section exists"
    else
        fail "Complete Failure Detection section missing"
    fi
}

test_sequential_reexecution_section() {
    ((TESTS_RUN++))
    if grep -q "## Sequential Re-execution Pattern" "$REFS_DIR/sequential-fallback.md" 2>/dev/null; then
        pass "Sequential Re-execution Pattern section exists"
    else
        fail "Sequential Re-execution Pattern section missing"
    fi
}

test_fallback_logging_section() {
    ((TESTS_RUN++))
    if grep -q "## Fallback Logging Pattern" "$REFS_DIR/sequential-fallback.md" 2>/dev/null; then
        pass "Fallback Logging Pattern section exists"
    else
        fail "Fallback Logging Pattern section missing"
    fi
}

test_zero_success_triggers_fallback() {
    ((TESTS_RUN++))
    # Test requirement: "Test: 0/5 success triggers fallback"
    local file="$REFS_DIR/sequential-fallback.md"
    if grep -qE "(0/[0-9]+|success_rate.*=.*0|all.*fail)" "$file" 2>/dev/null; then
        pass "0/N success triggers fallback documented"
    else
        fail "0/N success triggers fallback not documented"
    fi
}

test_br004_documented() {
    ((TESTS_RUN++))
    # BR-004: Fallback to sequential only when ALL parallel tasks fail
    local file="$REFS_DIR/sequential-fallback.md"
    if grep -qiE "(all.*fail|complete.*fail|BR-004)" "$file" 2>/dev/null; then
        pass "BR-004 (fallback only when all fail) documented"
    else
        fail "BR-004 (fallback only when all fail) not documented"
    fi
}

test_fallback_to_sequential_enabled() {
    ((TESTS_RUN++))
    local file="$REFS_DIR/sequential-fallback.md"
    if grep -q "fallback_to_sequential" "$file" 2>/dev/null; then
        pass "fallback_to_sequential config referenced"
    else
        fail "fallback_to_sequential config not referenced"
    fi
}

# Run AC#4 tests
test_sequential_fallback_file_exists
test_complete_failure_detection_section
test_sequential_reexecution_section
test_fallback_logging_section
test_zero_success_triggers_fallback
test_br004_documented
test_fallback_to_sequential_enabled

echo ""

# =============================================================================
# Cross-File Reference Tests
# =============================================================================
echo "--- Cross-File Reference Tests ---"

test_parallel_config_reference() {
    ((TESTS_RUN++))
    # All files should reference parallel-config.md or parallel-orchestration.yaml
    local found=0
    for file in error-handling-patterns.md timeout-handling.md retry-patterns.md sequential-fallback.md; do
        if grep -qE "(parallel-config|parallel-orchestration)" "$REFS_DIR/$file" 2>/dev/null; then
            ((found++))
        fi
    done
    if [[ $found -ge 2 ]]; then
        pass "At least 2 files reference parallel configuration"
    else
        fail "Less than 2 files reference parallel configuration (found: $found)"
    fi
}

test_story_110_metadata() {
    ((TESTS_RUN++))
    # Files should reference STORY-110
    local found=0
    for file in error-handling-patterns.md timeout-handling.md retry-patterns.md sequential-fallback.md; do
        if grep -q "STORY-110" "$REFS_DIR/$file" 2>/dev/null; then
            ((found++))
        fi
    done
    if [[ $found -eq 4 ]]; then
        pass "All 4 files reference STORY-110"
    else
        fail "Not all files reference STORY-110 (found: $found/4)"
    fi
}

# Run cross-file tests
test_parallel_config_reference
test_story_110_metadata

echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=== Test Summary ==="
echo "Tests Run: $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}$TESTS_FAILED test(s) failed${NC}"
    exit 1
fi
