#!/bin/bash
# Test AC#4: Malformed Section Triggers BLOCK with Guidance
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Validates that agent-generator.md and/or template-compliance-validation.md contain:
# - Detection of empty section body
# - Detection of wrong heading level
# - Detection of invalid YAML frontmatter field value
# - BLOCK with TEMPLATE_COMPLIANCE_FAILED for malformed sections
# - Correction guidance per malformation type
# - Minimum content requirements for empty sections
# - Allowed values for invalid frontmatter
#
# Expected: FAIL initially (TDD Red phase - malformed section detection not yet implemented)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
AGENT_GENERATOR="$PROJECT_ROOT/src/claude/agents/agent-generator.md"
COMPLIANCE_REF="$PROJECT_ROOT/src/claude/agents/agent-generator/references/template-compliance-validation.md"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# Helper: search both files
search_both_files() {
    local pattern="$1"
    local found=false

    if [ -f "$AGENT_GENERATOR" ] && grep -qiE "$pattern" "$AGENT_GENERATOR"; then
        found=true
    fi
    if [ -f "$COMPLIANCE_REF" ] && grep -qiE "$pattern" "$COMPLIANCE_REF"; then
        found=true
    fi

    $found
}

# -----------------------------------------------------------------------------
# Test 1: Empty section body detection
# -----------------------------------------------------------------------------
test_empty_body_detection() {
    local test_name="Empty section body detection"

    if search_both_files "empty.*(body|content|section)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic to detect empty section body"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Wrong heading level detection
# -----------------------------------------------------------------------------
test_wrong_heading_level() {
    local test_name="Wrong heading level detection"

    if search_both_files "(wrong|incorrect|invalid).*(heading|level)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic to detect wrong heading level"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Invalid frontmatter field value detection
# -----------------------------------------------------------------------------
test_invalid_frontmatter() {
    local test_name="Invalid YAML frontmatter field value detection"

    if search_both_files "(invalid|malformed).*(frontmatter|YAML|field)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic to detect invalid frontmatter field values"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: BLOCK for malformed sections (not just missing)
# -----------------------------------------------------------------------------
test_block_for_malformed() {
    local test_name="BLOCK triggered for malformed sections"

    if search_both_files "(malformed|malformation).*(BLOCK|block|halt)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No BLOCK logic for malformed sections"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Correction guidance provided
# -----------------------------------------------------------------------------
test_correction_guidance() {
    local test_name="Correction guidance provided per malformation type"

    if search_both_files "(correction|guidance|fix).*(malform|empty|heading|frontmatter)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No correction guidance for malformed sections"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Minimum content requirements for empty sections
# -----------------------------------------------------------------------------
test_minimum_content_requirements() {
    local test_name="Minimum content requirements for empty sections"

    if search_both_files "minimum.*(content|requirement)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No minimum content requirements specified"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Allowed values listed for invalid frontmatter
# -----------------------------------------------------------------------------
test_allowed_values_for_frontmatter() {
    local test_name="Allowed values for invalid frontmatter fields"

    if search_both_files "allowed.*(value|option|enum)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No allowed values specified for frontmatter fields"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Three distinct malformation types documented
# -----------------------------------------------------------------------------
test_three_malformation_types() {
    local test_name="Three malformation types documented (empty, heading, frontmatter)"

    local count=0
    if search_both_files "empty.*(body|content|section)"; then
        count=$((count + 1))
    fi
    if search_both_files "(wrong|incorrect).*(heading|level)"; then
        count=$((count + 1))
    fi
    if search_both_files "(invalid).*(frontmatter|YAML)"; then
        count=$((count + 1))
    fi

    if [ "$count" -ge 3 ]; then
        pass_test "$test_name (found $count/3 types)"
    else
        fail_test "$test_name" "Only $count/3 malformation types found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-389 AC#4: Block Malformed Section"
echo "=============================================="
echo "Agent-generator: $AGENT_GENERATOR"
echo "Compliance ref: $COMPLIANCE_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_empty_body_detection
run_test "2" test_wrong_heading_level
run_test "3" test_invalid_frontmatter
run_test "4" test_block_for_malformed
run_test "5" test_correction_guidance
run_test "6" test_minimum_content_requirements
run_test "7" test_allowed_values_for_frontmatter
run_test "8" test_three_malformation_types

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
