#!/bin/bash
# =============================================================================
# STORY-180 AC-2: Anti-Pattern Scanner Accepts Summary
# =============================================================================
# Tests that verify anti-pattern-scanner.md accepts "Context Summary" in prompt
# and documents this capability.
#
# Expected to FAIL initially (TDD Red Phase):
#   - Input contract doesn't include context_summary field
#   - Workflow doesn't document using provided summaries
#
# Run: bash tests/STORY-180/test-ac2-anti-pattern-scanner-accepts-summary.sh
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    ((TESTS_PASSED++))
    ((TESTS_RUN++))
}

fail() {
    echo -e "${RED}FAIL${NC}: $1"
    echo "       Expected: $2"
    echo "       Actual: ${3:-'(not found)'}"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

# Target file
TARGET_FILE="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

# =============================================================================
# Test 1: Input contract includes context_summary field
# =============================================================================
test_input_contract_has_context_summary() {
    local test_name="Input contract includes context_summary or context_summaries field"

    # Look for context_summary in the input contract section
    if grep -qE '"context_summar(y|ies)":|context_summar(y|ies):' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Field 'context_summary' or 'context_summaries' in input contract" \
             "Field not found in anti-pattern-scanner.md"
    fi
}

# =============================================================================
# Test 2: Context Summary acceptance documented in workflow
# =============================================================================
test_workflow_documents_summary_acceptance() {
    local test_name="Workflow documents accepting Context Summary in prompt"

    # Look for documentation about accepting summary in prompt
    if grep -qiE 'accept.*context.*summar|context.*summar.*accept|use.*provided.*summar' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Documentation about accepting Context Summary in prompt" \
             "Acceptance documentation not found"
    fi
}

# =============================================================================
# Test 3: Phase 1 context loading has conditional for summaries
# =============================================================================
test_phase1_has_summary_conditional() {
    local test_name="Phase 1 context loading has conditional for pre-provided summaries"

    # Look for IF condition about summaries in Phase 1
    if grep -qiE 'IF.*context.*summar|if.*summar.*provided|skip.*re-read' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Conditional: 'IF context_summary provided: skip re-reading'" \
             "Summary conditional not found in Phase 1"
    fi
}

# =============================================================================
# Test 4: Token efficiency benefit documented
# =============================================================================
test_token_efficiency_documented() {
    local test_name="Token efficiency benefit of summaries documented"

    # Look for documentation about token savings
    if grep -qiE 'token.*sav|reduc.*token|3K.*token|token.*effic' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Documentation about token savings from using summaries" \
             "Token efficiency documentation not found"
    fi
}

# =============================================================================
# Test 5: Example prompt with Context Summary exists
# =============================================================================
test_example_prompt_with_summary() {
    local test_name="Example prompt template includes Context Summary block"

    # Look for example invocation with Context Summary
    if grep -qE 'Context Summary|context_summary.*:.*"' "$TARGET_FILE" 2>/dev/null && \
       grep -q 'prompt=' "$TARGET_FILE" 2>/dev/null; then
        # Check if they're in proximity (both in same section)
        if grep -B20 -A20 'prompt=' "$TARGET_FILE" 2>/dev/null | grep -qi 'summar'; then
            pass "$test_name"
        else
            fail "$test_name" \
                 "Example prompt with Context Summary in proximity" \
                 "Summary not found near prompt example"
        fi
    else
        fail "$test_name" \
             "Example prompt template with Context Summary block" \
             "Example not found"
    fi
}

# =============================================================================
# Test 6: Scanner doesn't reload files when summary provided
# =============================================================================
test_no_reload_when_summary_provided() {
    local test_name="Documentation states scanner doesn't reload when summary provided"

    # Look for documentation about not reloading
    if grep -qiE 'do not re-read|skip.*load|avoid.*reload|use.*provided.*instead' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Statement: 'Use provided summaries instead of re-reading files'" \
             "No-reload documentation not found"
    fi
}

# =============================================================================
# Run all tests
# =============================================================================
echo "========================================================================"
echo "STORY-180 AC-2: Anti-Pattern Scanner Accepts Summary"
echo "========================================================================"
echo ""

test_input_contract_has_context_summary
test_workflow_documents_summary_acceptance
test_phase1_has_summary_conditional
test_token_efficiency_documented
test_example_prompt_with_summary
test_no_reload_when_summary_provided

echo ""
echo "========================================================================"
echo "Test Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "========================================================================"

# Exit with failure if any tests failed (TDD Red expected)
if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${YELLOW}NOTE: Failures expected in TDD Red phase${NC}"
    exit 1
fi

exit 0
