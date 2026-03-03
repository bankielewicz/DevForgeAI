#!/bin/bash
# =============================================================================
# STORY-180 AC-1: Context Summary Format Defined
# =============================================================================
# Tests that verify the context summary format is properly documented
# in the framework documentation.
#
# Expected to FAIL initially (TDD Red Phase):
#   - Context summary format section does not yet exist
#   - Format template not yet documented
#
# Run: bash tests/STORY-180/test-ac1-context-summary-format.sh
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
# Test 1: Context summary format header exists in documentation
# =============================================================================
test_context_summary_format_header_exists() {
    local test_name="Context summary format header exists in anti-pattern-scanner.md"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qE "^## Context Summary Format|^### Context Summary Format" "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Section header '## Context Summary Format' or '### Context Summary Format'" \
             "$(grep -c 'Context Summary' "$target_file" 2>/dev/null || echo '0') matches for 'Context Summary'"
    fi
}

# =============================================================================
# Test 2: Context summary format template exists
# =============================================================================
test_context_summary_template_exists() {
    local test_name="Context summary format template with example exists"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Look for the specific template format from the story
    if grep -q 'Context Summary (do not re-read files)' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Template: '**Context Summary (do not re-read files):**'" \
             "Template not found in anti-pattern-scanner.md"
    fi
}

# =============================================================================
# Test 3: Format includes tech-stack.md summary pattern
# =============================================================================
test_format_includes_tech_stack_pattern() {
    local test_name="Format includes tech-stack.md summary pattern"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Pattern: "- tech-stack.md: [key constraints]"
    if grep -qE '^\s*-\s*tech-stack\.md:' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Pattern: '- tech-stack.md: [constraints]'" \
             "tech-stack.md summary line not found"
    fi
}

# =============================================================================
# Test 4: Format includes anti-patterns.md summary pattern
# =============================================================================
test_format_includes_anti_patterns_pattern() {
    local test_name="Format includes anti-patterns.md summary pattern"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qE '^\s*-\s*anti-patterns\.md:' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Pattern: '- anti-patterns.md: [constraints]'" \
             "anti-patterns.md summary line not found"
    fi
}

# =============================================================================
# Test 5: Format includes architecture-constraints.md summary pattern
# =============================================================================
test_format_includes_architecture_constraints_pattern() {
    local test_name="Format includes architecture-constraints.md summary pattern"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    if grep -qE '^\s*-\s*architecture-constraints\.md:' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Pattern: '- architecture-constraints.md: [constraints]'" \
             "architecture-constraints.md summary line not found"
    fi
}

# =============================================================================
# Test 6: Summary format documented as concise (key constraints only)
# =============================================================================
test_summary_format_concise_documentation() {
    local test_name="Summary format documented as concise (key constraints only)"
    local target_file="$PROJECT_ROOT/.claude/agents/anti-pattern-scanner.md"

    # Check for documentation about concise format
    if grep -qiE 'concise|key constraints|summary' "$target_file" 2>/dev/null && \
       grep -qiE 'do not re-read|avoid re-reading|skip re-reading' "$target_file" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Documentation about concise format and avoiding re-reading files" \
             "Concise format documentation not found"
    fi
}

# =============================================================================
# Run all tests
# =============================================================================
echo "========================================================================"
echo "STORY-180 AC-1: Context Summary Format Defined"
echo "========================================================================"
echo ""

test_context_summary_format_header_exists
test_context_summary_template_exists
test_format_includes_tech_stack_pattern
test_format_includes_anti_patterns_pattern
test_format_includes_architecture_constraints_pattern
test_summary_format_concise_documentation

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
