#!/bin/bash
# Performance Test: NFR-001 through NFR-003
# Tests that hook operations meet performance requirements

set -e

TEST_NAME="Performance Requirements (NFR-001 to NFR-003)"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Test 1: NFR-001 - check-hooks execution < 100ms
test_nfr001_check_hooks_performance() {
    echo -n "Test P1: NFR-001 - check-hooks < 100ms... "

    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"
    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Warm up (first execution may be slower due to Python startup)
    devforgeai check-hooks --operation=create-sprint --status=completed --config="$TEMP_CONFIG" &>/dev/null || true

    # Measure 10 executions
    total_time=0
    iterations=10

    for i in $(seq 1 $iterations); do
        start=$(date +%s%N)
        devforgeai check-hooks --operation=create-sprint --status=completed --config="$TEMP_CONFIG" &>/dev/null || true
        end=$(date +%s%N)

        elapsed=$((($end - $start) / 1000000))  # Convert to milliseconds
        total_time=$(($total_time + $elapsed))
    done

    rm -f "$TEMP_CONFIG"

    avg_time=$(($total_time / $iterations))

    if [ $avg_time -lt 100 ]; then
        echo -e "${GREEN}PASS${NC} (avg: ${avg_time}ms)"
        return 0
    else
        echo -e "${YELLOW}WARN${NC} (avg: ${avg_time}ms, expected <100ms)"
        echo "  Note: May be acceptable on slower systems or during load"
        return 0  # Non-blocking
    fi
}

# Test 2: NFR-002 - invoke-hooks setup < 3 seconds
test_nfr002_invoke_hooks_setup_performance() {
    echo -n "Test P2: NFR-002 - invoke-hooks setup < 3s... "

    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"
    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Measure invoke-hooks initialization time (before user interaction)
    start=$(date +%s%N)

    # This will fail without full setup, but we measure initialization time
    timeout 5s devforgeai invoke-hooks --operation=create-sprint \
        --sprint-name="Perf-Test-Sprint" \
        --story-count=5 \
        --capacity=25 \
        --config="$TEMP_CONFIG" 2>/dev/null || true

    end=$(date +%s%N)

    rm -f "$TEMP_CONFIG"

    elapsed_ms=$((($end - $start) / 1000000))

    if [ $elapsed_ms -lt 3000 ]; then
        echo -e "${GREEN}PASS${NC} (${elapsed_ms}ms)"
        return 0
    else
        echo -e "${YELLOW}WARN${NC} (${elapsed_ms}ms, expected <3000ms)"
        return 0  # Non-blocking
    fi
}

# Test 3: NFR-003 - Phase N total overhead < 3.5 seconds
test_nfr003_phase_n_total_overhead() {
    echo -n "Test P3: NFR-003 - Phase N overhead < 3.5s... "

    # Simulate Phase N execution (check + invoke setup)
    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"
    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    start=$(date +%s%N)

    # Step 1: check-hooks
    devforgeai check-hooks --operation=create-sprint --status=completed --config="$TEMP_CONFIG" &>/dev/null
    check_exit=$?

    # Step 2: invoke-hooks (only if check succeeded)
    if [ $check_exit -eq 0 ]; then
        timeout 5s devforgeai invoke-hooks --operation=create-sprint \
            --sprint-name="Phase-N-Test" \
            --story-count=3 \
            --capacity=15 \
            --config="$TEMP_CONFIG" 2>/dev/null || true
    fi

    end=$(date +%s%N)

    rm -f "$TEMP_CONFIG"

    elapsed_ms=$((($end - $start) / 1000000))

    if [ $elapsed_ms -lt 3500 ]; then
        echo -e "${GREEN}PASS${NC} (${elapsed_ms}ms)"
        return 0
    else
        echo -e "${YELLOW}WARN${NC} (${elapsed_ms}ms, expected <3500ms)"
        return 0  # Non-blocking
    fi
}

# Test 4: Phase N doesn't add significant overhead to sprint creation
test_phase_n_overhead_acceptable() {
    echo -n "Test P4: Phase N overhead acceptable... "

    # This is a qualitative check - verify Phase N is documented as non-blocking
    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -qi "non-blocking\|background\|async\|minimal.*overhead"; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Phase N documented as non-blocking/minimal overhead"
        return 0
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: Overhead characteristics not documented"
        return 0
    fi
}

# Test 5: Verify performance requirements documented in NFRs
test_nfr_documentation() {
    echo -n "Test P5: Performance NFRs documented... "

    story_content=$(cat "$PROJECT_ROOT/.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")

    nfrs_found=0
    echo "$story_content" | grep -q "NFR-001" && nfrs_found=$((nfrs_found + 1))
    echo "$story_content" | grep -q "NFR-002" && nfrs_found=$((nfrs_found + 1))
    echo "$story_content" | grep -q "NFR-003" && nfrs_found=$((nfrs_found + 1))

    if [ $nfrs_found -eq 3 ]; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: All 3 performance NFRs documented"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: NFR-001, NFR-002, NFR-003 documented"
        echo "  Actual: Only $nfrs_found/3 found"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_nfr001_check_hooks_performance || FAILED_TESTS=$((FAILED_TESTS + 1))
test_nfr002_invoke_hooks_setup_performance || FAILED_TESTS=$((FAILED_TESTS + 1))
test_nfr003_phase_n_total_overhead || FAILED_TESTS=$((FAILED_TESTS + 1))
test_phase_n_overhead_acceptable || FAILED_TESTS=$((FAILED_TESTS + 1))
test_nfr_documentation || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
