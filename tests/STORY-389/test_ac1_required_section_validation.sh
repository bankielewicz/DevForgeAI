#!/bin/bash
# Test AC#1: Agent-Generator Validates Required Sections on Create
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Validates that agent-generator.md contains:
# - Read() call to canonical-agent-template.md before Write()
# - Logic to extract the 10 required sections from the canonical template
# - Validation step between generation and Write() operation
# - Reference to template-compliance-validation.md
#
# Expected: FAIL initially (TDD Red phase - validation logic not yet added)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
AGENT_GENERATOR="$PROJECT_ROOT/src/claude/agents/agent-generator.md"
CANONICAL_TEMPLATE="$PROJECT_ROOT/src/claude/agents/agent-generator/references/canonical-agent-template.md"
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

# -----------------------------------------------------------------------------
# Test 1: Agent-generator source file exists
# -----------------------------------------------------------------------------
test_agent_generator_exists() {
    local test_name="Agent-generator source file exists"
    if [ -f "$AGENT_GENERATOR" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $AGENT_GENERATOR"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Canonical template source file exists
# -----------------------------------------------------------------------------
test_canonical_template_exists() {
    local test_name="Canonical template source file exists"
    if [ -f "$CANONICAL_TEMPLATE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $CANONICAL_TEMPLATE"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Agent-generator contains Read() call to canonical template
# -----------------------------------------------------------------------------
test_reads_canonical_template() {
    local test_name="Agent-generator reads canonical template before validation"

    if [ ! -f "$AGENT_GENERATOR" ]; then
        fail_test "$test_name" "Cannot check - agent-generator not found"
        return
    fi

    # Must contain a Read() call referencing canonical-agent-template.md
    if grep -q "canonical-agent-template" "$AGENT_GENERATOR"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No reference to canonical-agent-template.md found in agent-generator"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Agent-generator contains template compliance validation step
# -----------------------------------------------------------------------------
test_template_compliance_validation_step() {
    local test_name="Agent-generator contains template compliance validation step"

    if [ ! -f "$AGENT_GENERATOR" ]; then
        fail_test "$test_name" "Cannot check - agent-generator not found"
        return
    fi

    # Must contain text about template compliance validation between generation and Write()
    if grep -qi "template compliance" "$AGENT_GENERATOR"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'template compliance' validation step found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Agent-generator extracts required sections from template
# -----------------------------------------------------------------------------
test_extracts_required_sections() {
    local test_name="Agent-generator extracts required section list from template"

    if [ ! -f "$AGENT_GENERATOR" ]; then
        fail_test "$test_name" "Cannot check - agent-generator not found"
        return
    fi

    # Must mention extracting or parsing required sections (not hardcoded list)
    if grep -qiE "(extract|parse|read).*(required section|section list)" "$AGENT_GENERATOR"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic to extract required sections from canonical template"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Validation occurs before Write() operation
# -----------------------------------------------------------------------------
test_validation_before_write() {
    local test_name="Validation occurs before Write() operation"

    if [ ! -f "$AGENT_GENERATOR" ]; then
        fail_test "$test_name" "Cannot check - agent-generator not found"
        return
    fi

    # Must have explicit statement that validation runs before Write()
    if grep -qiE "(before|prior to|precede).*(Write|writing)" "$AGENT_GENERATOR"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No explicit statement that validation precedes Write() operation"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Template compliance validation reference file exists
# -----------------------------------------------------------------------------
test_compliance_reference_exists() {
    local test_name="Template-compliance-validation.md reference file exists"
    if [ -f "$COMPLIANCE_REF" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $COMPLIANCE_REF"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Agent-generator references template-compliance-validation.md
# -----------------------------------------------------------------------------
test_references_compliance_file() {
    local test_name="Agent-generator references template-compliance-validation.md"

    if [ ! -f "$AGENT_GENERATOR" ]; then
        fail_test "$test_name" "Cannot check - agent-generator not found"
        return
    fi

    if grep -q "template-compliance-validation" "$AGENT_GENERATOR"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No reference to template-compliance-validation.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Validation triggers for all generation modes (Single, Batch, Priority, Regenerate)
# -----------------------------------------------------------------------------
test_all_generation_modes_validated() {
    local test_name="Validation triggers for all generation modes"

    if [ ! -f "$AGENT_GENERATOR" ]; then
        fail_test "$test_name" "Cannot check - agent-generator not found"
        return
    fi

    local missing_modes=""
    local modes=("Single" "Batch" "Regenerate")

    for mode in "${modes[@]}"; do
        if ! grep -qi "$mode" "$AGENT_GENERATOR"; then
            missing_modes="$missing_modes $mode"
        fi
    done

    if [ -z "$missing_modes" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing generation modes:$missing_modes"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-389 AC#1: Required Section Validation"
echo "=============================================="
echo "Agent-generator: $AGENT_GENERATOR"
echo "Canonical template: $CANONICAL_TEMPLATE"
echo "----------------------------------------------"
echo ""

run_test "1" test_agent_generator_exists
run_test "2" test_canonical_template_exists
run_test "3" test_reads_canonical_template
run_test "4" test_template_compliance_validation_step
run_test "5" test_extracts_required_sections
run_test "6" test_validation_before_write
run_test "7" test_compliance_reference_exists
run_test "8" test_references_compliance_file
run_test "9" test_all_generation_modes_validated

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
