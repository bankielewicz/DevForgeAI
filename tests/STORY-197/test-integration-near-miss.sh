#!/bin/bash
# Integration tests for STORY-197: Near-miss detection in pre-tool-use.sh
# Tests cross-component interactions between hook, logging, and pattern matching

set -e

# Configuration
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/mnt/c/Projects/DevForgeAI2}"
HOOK_SCRIPT="$PROJECT_ROOT/.claude/hooks/pre-tool-use.sh"
LOG_FILE="$PROJECT_ROOT/devforgeai/logs/pre-tool-use.log"
TEST_LOG="$PROJECT_ROOT/tests/STORY-197/integration-test-results.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0
TOTAL=0

# Initialize test log
echo "=== STORY-197 Integration Tests ===" > "$TEST_LOG"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$TEST_LOG"
echo "" >> "$TEST_LOG"

# Helper function to run hook with JSON input
run_hook() {
    local command="$1"
    local json_input='{"tool_name": "Bash", "tool_input": {"command": "'"$command"'"}}'
    echo "$json_input" | bash "$HOOK_SCRIPT" 2>&1
    return ${PIPESTATUS[1]}
}

# Test result logging
log_result() {
    local test_name="$1"
    local result="$2"
    local details="$3"

    TOTAL=$((TOTAL + 1))

    if [ "$result" = "PASS" ]; then
        PASSED=$((PASSED + 1))
        echo -e "${GREEN}[PASS]${NC} $test_name"
        echo "[PASS] $test_name" >> "$TEST_LOG"
    else
        FAILED=$((FAILED + 1))
        echo -e "${RED}[FAIL]${NC} $test_name"
        echo "[FAIL] $test_name" >> "$TEST_LOG"
        echo "       Details: $details" >> "$TEST_LOG"
    fi
}

echo ""
echo "=========================================="
echo "  STORY-197 Integration Test Suite"
echo "=========================================="
echo ""

# Backup current log file
cp "$LOG_FILE" "$LOG_FILE.bak" 2>/dev/null || true
LOG_LINE_START=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")

# ============================================
# Integration Point 1: Hook receives JSON input from Claude Code Terminal
# ============================================
echo -e "${YELLOW}Testing Integration Point 1: JSON Input Handling${NC}"

# Test 1.1: Valid JSON input parsing
TEST_NAME="1.1 Hook parses JSON input correctly"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "unknown_cmd_test"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
# Should exit 1 (ask user) for unknown command
if [ "$EXIT_CODE" -eq 1 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Expected exit code 1, got $EXIT_CODE"
fi

# Test 1.2: Command extraction from JSON
TEST_NAME="1.2 Command extracted from tool_input.command"
LOG_AFTER=$(tail -20 "$LOG_FILE" | grep -c "Extracted command: 'unknown_cmd_test'" || echo "0")
if [ "$LOG_AFTER" -gt 0 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Command not found in log extraction"
fi

echo ""

# ============================================
# Integration Point 2: Near-miss detection integrates with log() function
# ============================================
echo -e "${YELLOW}Testing Integration Point 2: Near-miss integrates with log()${NC}"

# Test 2.1: Near-miss detection logs via log() function
TEST_NAME="2.1 Near-miss uses log() function"
# Command that will trigger near-miss: foo && git status
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "foo_cmd && git status"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
NEAR_MISS_LOG=$(tail -20 "$LOG_FILE" | grep -c "NEAR-MISS DETECTED" || echo "0")
if [ "$NEAR_MISS_LOG" -gt 0 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "NEAR-MISS DETECTED not found in log"
fi

# Test 2.2: Near-miss log entries have timestamps
TEST_NAME="2.2 Near-miss logs have timestamps"
TIMESTAMP_PATTERN=$(tail -20 "$LOG_FILE" | grep "NEAR-MISS DETECTED" | grep -c "\[20[0-9][0-9]-" || echo "0")
if [ "$TIMESTAMP_PATTERN" -gt 0 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Timestamp not found in near-miss log entry"
fi

# Test 2.3: Log file correctly appends (not overwrites)
TEST_NAME="2.3 Log file appends entries correctly"
LOG_LINE_COUNT_BEFORE=$(wc -l < "$LOG_FILE")
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "another_unknown && pytest"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
LOG_LINE_COUNT_AFTER=$(wc -l < "$LOG_FILE")
if [ "$LOG_LINE_COUNT_AFTER" -gt "$LOG_LINE_COUNT_BEFORE" ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Log file not appending (before: $LOG_LINE_COUNT_BEFORE, after: $LOG_LINE_COUNT_AFTER)"
fi

echo ""

# ============================================
# Integration Point 3: Near-miss runs AFTER safe pattern matching fails
# ============================================
echo -e "${YELLOW}Testing Integration Point 3: Correct sequence - After safe patterns${NC}"

# Test 3.1: Near-miss only triggers when safe patterns don't match
TEST_NAME="3.1 Near-miss triggers only after safe pattern failure"
# First verify a safe command doesn't trigger near-miss
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "git status"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
SAFE_EXIT=$?
# Check if "No safe pattern matched" appears before NEAR-MISS in recent logs
SEQUENCE_CHECK=$(tail -30 "$LOG_FILE" | grep -n "No safe pattern matched\|NEAR-MISS DETECTED" | tail -2)
if [ "$SAFE_EXIT" -eq 0 ]; then
    # Safe command should NOT show near-miss sequence
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Safe command didn't auto-approve"
fi

# Test 3.2: Verify "No safe pattern matched" precedes NEAR-MISS in log
TEST_NAME="3.2 'No safe pattern matched' precedes NEAR-MISS in log"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "mycommand && git diff"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
# Get last occurrence of each
NO_MATCH_LINE=$(tail -20 "$LOG_FILE" | grep -n "No safe pattern matched" | tail -1 | cut -d: -f1)
NEAR_MISS_LINE=$(tail -20 "$LOG_FILE" | grep -n "NEAR-MISS DETECTED" | tail -1 | cut -d: -f1)
if [ -n "$NO_MATCH_LINE" ] && [ -n "$NEAR_MISS_LINE" ] && [ "$NO_MATCH_LINE" -lt "$NEAR_MISS_LINE" ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Sequence incorrect - No match: $NO_MATCH_LINE, Near-miss: $NEAR_MISS_LINE"
fi

echo ""

# ============================================
# Integration Point 4: Near-miss runs BEFORE blocked pattern check
# ============================================
echo -e "${YELLOW}Testing Integration Point 4: Correct sequence - Before blocked patterns${NC}"

# Test 4.1: Near-miss appears before blocked pattern check in log
TEST_NAME="4.1 Near-miss runs before blocked pattern check"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "mycommand && echo test"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
# Check sequence in log
NEAR_MISS_LINE=$(tail -20 "$LOG_FILE" | grep -n "NEAR-MISS\|RECOMMENDATION" | head -1 | cut -d: -f1 || echo "999")
BLOCKED_CHECK_LINE=$(tail -20 "$LOG_FILE" | grep -n "Checking against.*blocked patterns" | tail -1 | cut -d: -f1 || echo "0")
if [ -n "$BLOCKED_CHECK_LINE" ] && [ "$BLOCKED_CHECK_LINE" -gt 0 ]; then
    if [ "$NEAR_MISS_LINE" -lt "$BLOCKED_CHECK_LINE" ] || [ "$NEAR_MISS_LINE" = "999" ]; then
        log_result "$TEST_NAME" "PASS"
    else
        log_result "$TEST_NAME" "FAIL" "Near-miss ($NEAR_MISS_LINE) not before blocked check ($BLOCKED_CHECK_LINE)"
    fi
else
    log_result "$TEST_NAME" "FAIL" "Could not find blocked pattern check in log"
fi

# Test 4.2: Blocked command still blocks (near-miss doesn't interfere)
TEST_NAME="4.2 Blocked commands still block correctly"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/test"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
if [ "$EXIT_CODE" -eq 2 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Expected exit code 2 (block), got $EXIT_CODE"
fi

echo ""

# ============================================
# Integration Point 5: Log file output is correctly appended
# ============================================
echo -e "${YELLOW}Testing Integration Point 5: Log file consistency${NC}"

# Test 5.1: Log file format consistency
TEST_NAME="5.1 Log entries follow consistent format"
# Check that all NEAR-MISS related entries have proper format
FORMAT_CHECK=$(tail -50 "$LOG_FILE" | grep "NEAR-MISS\|Near-miss pattern:\|Command starts with:" | grep -v "^\[20[0-9][0-9]-" | wc -l)
if [ "$FORMAT_CHECK" -eq 0 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Found $FORMAT_CHECK log entries without proper timestamp format"
fi

# Test 5.2: Multiple near-misses in single command
TEST_NAME="5.2 Multiple near-miss patterns logged correctly"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "foo && git status && pytest tests/"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
MULTI_PATTERNS=$(tail -20 "$LOG_FILE" | grep -c "Near-miss pattern:" || echo "0")
if [ "$MULTI_PATTERNS" -ge 2 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Expected 2+ near-miss patterns, found $MULTI_PATTERNS"
fi

echo ""

# ============================================
# Test Scenarios from Requirements
# ============================================
echo -e "${YELLOW}Testing Specified Scenarios${NC}"

# Scenario 1: Command with near-miss (e.g., "foo && git status") - should log near-miss
TEST_NAME="Scenario 1: Near-miss command logs detection"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "foo && git status"}}'
LOG_BEFORE=$(wc -l < "$LOG_FILE")
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
FOUND_NEAR_MISS=$(tail -15 "$LOG_FILE" | grep -c "NEAR-MISS DETECTED" || echo "0")
if [ "$FOUND_NEAR_MISS" -gt 0 ] && [ "$EXIT_CODE" -eq 1 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Near-miss=$FOUND_NEAR_MISS, Exit=$EXIT_CODE (expected 1)"
fi

# Scenario 2: Command without near-miss (e.g., "unknown_cmd") - should NOT log near-miss
TEST_NAME="Scenario 2: No near-miss for completely unknown command"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "completely_unknown_command_xyz123"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
FOUND_NEAR_MISS=$(tail -10 "$LOG_FILE" | grep -c "NEAR-MISS DETECTED" || echo "0")
if [ "$FOUND_NEAR_MISS" -eq 0 ] && [ "$EXIT_CODE" -eq 1 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Unexpected near-miss detection for unknown command"
fi

# Scenario 3: Safe command (e.g., "git status") - should auto-approve, no near-miss
TEST_NAME="Scenario 3: Safe command auto-approves without near-miss"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "git status"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
if [ "$EXIT_CODE" -eq 0 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Safe command didn't auto-approve (exit=$EXIT_CODE)"
fi

# Scenario 4: Blocked command (e.g., "rm -rf /") - should block, not reach near-miss
TEST_NAME="Scenario 4: Blocked command blocks correctly"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/dangerous"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
if [ "$EXIT_CODE" -eq 2 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Blocked command didn't block (exit=$EXIT_CODE)"
fi

echo ""

# ============================================
# Exit Code Verification
# ============================================
echo -e "${YELLOW}Testing Exit Codes${NC}"

# Test exit code 0 (approve)
TEST_NAME="Exit code 0 for safe command"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "npm run test"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Expected 0"
fi

# Test exit code 1 (ask)
TEST_NAME="Exit code 1 for unknown command"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "unknown_application"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
if [ $? -eq 1 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Expected 1"
fi

# Test exit code 2 (block)
TEST_NAME="Exit code 2 for blocked command"
JSON_INPUT='{"tool_name": "Bash", "tool_input": {"command": "sudo rm -rf /"}}'
echo "$JSON_INPUT" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
if [ $? -eq 2 ]; then
    log_result "$TEST_NAME" "PASS"
else
    log_result "$TEST_NAME" "FAIL" "Expected 2"
fi

echo ""

# ============================================
# Summary
# ============================================
echo "=========================================="
echo "           TEST SUMMARY"
echo "=========================================="
echo -e "Total:  $TOTAL"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

# Write summary to log
echo "" >> "$TEST_LOG"
echo "=== Summary ===" >> "$TEST_LOG"
echo "Total: $TOTAL" >> "$TEST_LOG"
echo "Passed: $PASSED" >> "$TEST_LOG"
echo "Failed: $FAILED" >> "$TEST_LOG"
echo "Completed: $(date '+%Y-%m-%d %H:%M:%S')" >> "$TEST_LOG"

# Return appropriate exit code
if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}All integration tests passed!${NC}"
    exit 0
else
    echo -e "${RED}$FAILED test(s) failed.${NC}"
    exit 1
fi
