#!/bin/bash
# =============================================================================
# STORY-180 AC-5: Token Reduction Measurable
# =============================================================================
# Tests that verify the token reduction target (-3K tokens per subagent call)
# is documented and measurable.
#
# Expected to FAIL initially (TDD Red Phase):
#   - Token reduction metrics not yet documented
#   - Before/after comparison not established
#
# Run: bash tests/STORY-180/test-ac5-token-reduction-measurable.sh
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
# Test 1: Token reduction target documented (3K tokens)
# =============================================================================
test_token_reduction_target_documented() {
    local test_name="Token reduction target (3K tokens) documented"

    # Check anti-pattern-scanner.md for 3K token target
    local scanner_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qiE '3K.*token|3,?000.*token|-3K|3K.*reduc|3K.*sav' "$scanner_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Token target: '-3K tokens' or '3K token reduction'" \
             "3K token target not found in anti-pattern-scanner.md"
    fi
}

# =============================================================================
# Test 2: Before/after comparison documented
# =============================================================================
test_before_after_comparison() {
    local test_name="Before/after token comparison documented"
    local scanner_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Look for before/after or current/new comparison
    if grep -qiE 'before.*after|without.*with.*summar|current.*new|~[0-9]+K.*vs.*~[0-9]+K' "$scanner_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Before/after comparison: 'X tokens without summary vs Y tokens with summary'" \
             "Comparison not documented"
    fi
}

# =============================================================================
# Test 3: Context file sizes documented (what's being saved)
# =============================================================================
test_context_file_sizes_documented() {
    local test_name="Context file sizes documented (3-4K tokens per full load)"
    local scanner_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qiE '3-4K.*token|~[34]K.*token|context.*file.*[34],?000' "$scanner_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Documentation: 'context files ~3-4K tokens'" \
             "Context file size documentation not found"
    fi
}

# =============================================================================
# Test 4: Summary size documented (reduced from full)
# =============================================================================
test_summary_size_documented() {
    local test_name="Summary size documented (smaller than full context)"
    local scanner_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Look for summary size specification
    if grep -qiE 'summar.*[0-9]+.*token|~[0-9]+.*line.*summar|concise.*[0-9]+' "$scanner_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Summary size: 'summary ~X tokens' or '~X lines per summary'" \
             "Summary size not documented"
    fi
}

# =============================================================================
# Test 5: Token efficiency section in documentation
# =============================================================================
test_token_efficiency_section() {
    local test_name="Token Efficiency section exists in documentation"
    local scanner_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qiE '^##.*Token.*Effic|^###.*Token.*Effic|^##.*Token.*Sav' "$scanner_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Section: '## Token Efficiency' or '### Token Savings'" \
             "Token efficiency section not found"
    fi
}

# =============================================================================
# Test 6: Measurable metric documented (not just qualitative)
# =============================================================================
test_measurable_metric() {
    local test_name="Measurable metric (specific number, not qualitative)"
    local scanner_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Look for specific numbers like "saves 3K", "reduces by 3000", "~3K reduction"
    if grep -qiE '[0-9]+K.*token|[0-9],?000.*token|~[0-9]+K' "$scanner_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Specific metric: '3K tokens' or '3,000 tokens'" \
             "Quantitative metric not found"
    fi
}

# =============================================================================
# Test 7: Parallel validation references token savings
# =============================================================================
test_parallel_validation_token_savings() {
    local test_name="parallel-validation.md references token savings from summaries"
    local parallel_file="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/parallel-validation.md"

    if grep -qiE 'token.*sav|reduc.*token|[0-9]+K.*token' "$parallel_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Token savings mentioned in parallel-validation.md" \
             "Token savings not referenced"
    fi
}

# =============================================================================
# Test 8: Per-subagent calculation documented
# =============================================================================
test_per_subagent_calculation() {
    local test_name="Per-subagent token calculation documented"
    local scanner_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Look for per-invocation or per-subagent calculation
    if grep -qiE 'per.*subagent|per.*invocation|each.*call|per.*call' "$scanner_file" 2>/dev/null && \
       grep -qiE '[0-9]+K.*token' "$scanner_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Per-subagent calculation: 'saves X tokens per subagent call'" \
             "Per-subagent calculation not documented"
    fi
}

# =============================================================================
# Run all tests
# =============================================================================
echo "========================================================================"
echo "STORY-180 AC-5: Token Reduction Measurable"
echo "========================================================================"
echo ""

test_token_reduction_target_documented
test_before_after_comparison
test_context_file_sizes_documented
test_summary_size_documented
test_token_efficiency_section
test_measurable_metric
test_parallel_validation_token_savings
test_per_subagent_calculation

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
