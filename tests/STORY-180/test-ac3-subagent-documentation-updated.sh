#!/bin/bash
# =============================================================================
# STORY-180 AC-3: Subagent Documentation Updated
# =============================================================================
# Tests that verify subagent documentation includes the conditional pattern:
# "IF context_files_in_prompt: Use provided summaries"
#
# Expected to FAIL initially (TDD Red Phase):
#   - Conditional pattern not yet documented in subagent files
#   - Standard subagent template doesn't include summary usage pattern
#
# Run: bash tests/STORY-180/test-ac3-subagent-documentation-updated.sh
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

# =============================================================================
# Test 1: Anti-pattern-scanner has conditional summary usage pattern
# =============================================================================
test_anti_pattern_scanner_conditional() {
    local test_name="anti-pattern-scanner.md has 'IF context_files_in_prompt' conditional"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qiE 'IF.*context.*(files|summar).*in.*prompt|IF.*summar.*provided' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Pattern: 'IF context_files_in_prompt:' or 'IF context_summary provided:'" \
             "Conditional not found"
    fi
}

# =============================================================================
# Test 2: Conditional includes "Use provided summaries" instruction
# =============================================================================
test_use_provided_summaries_instruction() {
    local test_name="Documentation includes 'Use provided summaries' instruction"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qiE 'use.*provided.*summar|use.*context.*summar' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Instruction: 'Use provided summaries'" \
             "Instruction not found"
    fi
}

# =============================================================================
# Test 3: Context loading phase documents summary shortcut
# =============================================================================
test_context_loading_summary_shortcut() {
    local test_name="Phase 1 Context Loading documents summary shortcut"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Look in Phase 1 section for summary shortcut
    if grep -A30 'Phase 1.*Context.*Load\|Context.*Load.*Phase' "$target_file" 2>/dev/null | \
       grep -qiE 'summar|skip.*load|shortcut'; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Phase 1 Context Loading mentions summary shortcut" \
             "Shortcut not found in Phase 1"
    fi
}

# =============================================================================
# Test 4: Documentation explicitly states files not re-read
# =============================================================================
test_explicit_no_reread_statement() {
    local test_name="Explicit statement that files are not re-read when summary provided"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qiE 'not.*re-read|skip.*read|do not.*load.*again|avoid.*reload' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Statement: 'do not re-read files' when summary provided" \
             "No-reread statement not found"
    fi
}

# =============================================================================
# Test 5: Guardrail 2 updated with summary exception
# =============================================================================
test_guardrail2_summary_exception() {
    local test_name="Guardrail #2 (ALL 6 Context Files Required) has summary exception"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Look for Guardrail 2 with exception for summaries
    if grep -A10 'Guardrail.*2\|ALL 6 Context Files' "$target_file" 2>/dev/null | \
       grep -qiE 'unless.*summar|except.*summar|or.*summar.*provided'; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Guardrail #2 has exception: 'unless summaries provided'" \
             "Summary exception not found in Guardrail #2"
    fi
}

# =============================================================================
# Test 6: Input Contract includes optional context_summary field
# =============================================================================
test_input_contract_optional_summary() {
    local test_name="Input Contract shows context_summary as optional field"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Check for context_summary in input contract with optional marker
    if grep -A30 'Input Contract\|Required Context' "$target_file" 2>/dev/null | \
       grep -qiE 'context_summar.*optional|"context_summar"'; then
        pass "$test_name"
    else
        fail "$test_name" \
             "context_summary field in Input Contract (optional)" \
             "Field not found in Input Contract"
    fi
}

# =============================================================================
# Run all tests
# =============================================================================
echo "========================================================================"
echo "STORY-180 AC-3: Subagent Documentation Updated"
echo "========================================================================"
echo ""

test_anti_pattern_scanner_conditional
test_use_provided_summaries_instruction
test_context_loading_summary_shortcut
test_explicit_no_reread_statement
test_guardrail2_summary_exception
test_input_contract_optional_summary

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
