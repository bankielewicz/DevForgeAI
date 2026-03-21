#!/bin/bash

##############################################################################
# Test Suite: STORY-554 AC#4 - Progressive Disclosure and Micro-Task Chunking
#
# AC#4: Progressive Disclosure and Micro-Task Chunking
# Given: a user is working through the checklist and the checklist contains
#        more than 20 items
# When: the skill presents checklist items
# Then: items are presented in micro-task chunks of 5 to 7 items at a time
#       with adaptive pacing prompts between chunks
#
# Target file: src/claude/skills/operating-business/references/mvp-launch-checklist.md
#
# TDD Phase: RED - All tests expected to FAIL (target file does not exist)
# Story: STORY-554
# Generated: 2026-03-21
##############################################################################

set -euo pipefail

TEST_NAME="AC#4: Progressive Disclosure and Micro-Task Chunking"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"
TARGET_FILE="src/claude/skills/operating-business/references/mvp-launch-checklist.md"

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

# Helper functions
run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}  PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}  FAIL${NC}"
    fi
}

##############################################################################
# TEST 1: Reference file exists
##############################################################################

test_reference_file_exists() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ -f "$file" ]; then
        echo "  Reference file found: $TARGET_FILE"
        return 0
    else
        echo "  ERROR: Reference file not found at $TARGET_FILE"
        return 1
    fi
}

##############################################################################
# TEST 2: Progressive disclosure section exists
##############################################################################

test_progressive_disclosure_section_exists() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "progressive.*disclosure\|micro.*task\|chunking\|pacing" "$file"; then
        echo "  Progressive disclosure guidance found"
        return 0
    else
        echo "  ERROR: No progressive disclosure guidance found"
        return 1
    fi
}

##############################################################################
# TEST 3: Chunk size of 5-7 items documented
##############################################################################

test_chunk_size_documented() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # Look for chunk size specification (5-7 items, 5 to 7, etc.)
    if grep -qiE "5.*(to|-).*7|chunk.*size|5.*7.*items|items.*5.*7" "$file"; then
        echo "  Chunk size of 5-7 items documented"
        return 0
    else
        echo "  ERROR: Chunk size of 5-7 items not documented"
        return 1
    fi
}

##############################################################################
# TEST 4: Adaptive pacing prompts documented
##############################################################################

test_adaptive_pacing_prompts_documented() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # Look for pacing prompt examples or instructions
    if grep -qiE "pacing.*prompt|ready.*next.*section|pause.*between|adaptive.*pacing|continue.*next" "$file"; then
        echo "  Adaptive pacing prompts documented"
        return 0
    else
        echo "  ERROR: No adaptive pacing prompts documented"
        return 1
    fi
}

##############################################################################
# TEST 5: 20-item threshold documented
##############################################################################

test_twenty_item_threshold_documented() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # Look for the 20-item threshold that triggers chunking
    if grep -qiE "20.*items|more.*than.*20|exceed.*20|threshold.*20|20.*threshold" "$file"; then
        echo "  20-item threshold documented"
        return 0
    else
        echo "  ERROR: 20-item threshold not documented"
        return 1
    fi
}

##############################################################################
# TEST 6: Checklist contains more than 20 items (triggering chunking)
##############################################################################

test_checklist_exceeds_20_items() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    local item_count
    item_count=$(grep -c "^- \[ \]" "$file" 2>/dev/null || echo "0")

    if [ "$item_count" -gt 20 ]; then
        echo "  Checklist has $item_count items (exceeds 20-item threshold)"
        return 0
    else
        echo "  ERROR: Checklist has only $item_count items (must exceed 20 for chunking to apply)"
        return 1
    fi
}

##############################################################################
# TEST 7: Pacing prompt example text present
##############################################################################

test_pacing_prompt_example_present() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # Look for actual pacing prompt example text
    if grep -qiE "ready for|shall we|would you like|let.*continue|next section|move on" "$file"; then
        echo "  Pacing prompt example text found"
        return 0
    else
        echo "  ERROR: No pacing prompt example text found"
        return 1
    fi
}

##############################################################################
# TEST 8: Chunking logic instructions present for skill execution
##############################################################################

test_chunking_logic_instructions_present() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # Look for instructions on how the skill should chunk items
    if grep -qiE "present.*chunk|group.*items|display.*batch|show.*at.*time|section.*by.*section" "$file"; then
        echo "  Chunking logic instructions present"
        return 0
    else
        echo "  ERROR: No chunking logic instructions found"
        return 1
    fi
}

##############################################################################
# TEST 9: Fallback behavior documented (BR-002)
##############################################################################

test_fallback_behavior_documented() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # BR-002: "Fall back to full list if chunking fails"
    if grep -qiE "fall.*back|full.*list|all.*at.*once|display.*all|skip.*chunk" "$file"; then
        echo "  Fallback behavior documented"
        return 0
    else
        echo "  ERROR: No fallback behavior documented (BR-002 requires fallback)"
        return 1
    fi
}

##############################################################################
# TEST 10: Overwhelm prevention rationale documented
##############################################################################

test_overwhelm_prevention_rationale() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # AC#4 specifically mentions "preventing overwhelm through progressive disclosure"
    if grep -qiE "overwhelm|cognitive.*load|adhd|attention|manageable|digestible" "$file"; then
        echo "  Overwhelm prevention rationale documented"
        return 0
    else
        echo "  ERROR: No overwhelm prevention rationale found"
        return 1
    fi
}

##############################################################################
# Run all tests
##############################################################################

echo "============================================================"
echo "STORY-554 | $TEST_NAME"
echo "Target: $TARGET_FILE"
echo "============================================================"

run_test "Reference file exists" test_reference_file_exists
run_test "Progressive disclosure section exists" test_progressive_disclosure_section_exists
run_test "Chunk size of 5-7 items documented" test_chunk_size_documented
run_test "Adaptive pacing prompts documented" test_adaptive_pacing_prompts_documented
run_test "20-item threshold documented" test_twenty_item_threshold_documented
run_test "Checklist contains more than 20 items" test_checklist_exceeds_20_items
run_test "Pacing prompt example text present" test_pacing_prompt_example_present
run_test "Chunking logic instructions present" test_chunking_logic_instructions_present
run_test "Fallback behavior documented (BR-002)" test_fallback_behavior_documented
run_test "Overwhelm prevention rationale documented" test_overwhelm_prevention_rationale

##############################################################################
# Summary
##############################################################################

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed out of $TESTS_RUN tests"
echo "============================================================"

[ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
