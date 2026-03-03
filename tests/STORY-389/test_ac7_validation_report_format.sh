#!/bin/bash
# Test AC#7: Validation Report with Section-by-Section Status
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Validates that agent-generator.md and/or template-compliance-validation.md contain:
# - Section-by-section status table with Section Name/Status/Details columns
# - Required sections with PASS/FAIL status
# - Optional sections with PASS/WARN/N-A status
# - YAML frontmatter field validation in report
# - Overall summary line with counts
# - Final verdict (PASS, PASS WITH WARNINGS, or BLOCK)
#
# Expected: FAIL initially (TDD Red phase - report format not yet implemented)

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
# Test 1: Section-by-section status table defined
# -----------------------------------------------------------------------------
test_section_status_table() {
    local test_name="Section-by-section status table defined"

    if search_both_files "Section.*(Name|Status|Details).*\|"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No section-by-section status table with columns"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: PASS status for required sections
# -----------------------------------------------------------------------------
test_pass_status_for_required() {
    local test_name="PASS status for required sections"

    if search_both_files "PASS"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No PASS status defined"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: FAIL status for required sections
# -----------------------------------------------------------------------------
test_fail_status_for_required() {
    local test_name="FAIL status for required sections"

    if search_both_files "FAIL"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No FAIL status defined"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: WARN status for optional sections
# -----------------------------------------------------------------------------
test_warn_status_for_optional() {
    local test_name="WARN status for optional sections"

    if search_both_files "WARN"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No WARN status defined"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: N/A or N-A status for non-applicable optional sections
# -----------------------------------------------------------------------------
test_na_status() {
    local test_name="N/A status for non-applicable optional sections"

    if search_both_files "N.?A"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No N/A or N-A status defined"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Frontmatter field validation in report
# -----------------------------------------------------------------------------
test_frontmatter_validation_in_report() {
    local test_name="Frontmatter field validation in report"

    if search_both_files "(frontmatter|YAML).*(validat|check).*(report|status)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No frontmatter validation in report"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Overall summary line with counts
# -----------------------------------------------------------------------------
test_summary_line_with_counts() {
    local test_name="Overall summary line with counts"

    if search_both_files "(summary|total).*(count|pass|fail)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No summary line with counts defined"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Three final verdicts defined (PASS, PASS WITH WARNINGS, BLOCK)
# -----------------------------------------------------------------------------
test_three_verdicts() {
    local test_name="Three final verdicts defined"

    local count=0
    if search_both_files "\bPASS\b"; then
        count=$((count + 1))
    fi
    if search_both_files "PASS WITH WARNINGS"; then
        count=$((count + 1))
    fi
    if search_both_files "\bBLOCK\b"; then
        count=$((count + 1))
    fi

    if [ "$count" -ge 3 ]; then
        pass_test "$test_name (found $count/3 verdicts)"
    else
        fail_test "$test_name" "Only $count/3 final verdicts found (need PASS, PASS WITH WARNINGS, BLOCK)"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Report mentions final verdict
# -----------------------------------------------------------------------------
test_final_verdict_label() {
    local test_name="Report includes final verdict label"

    if search_both_files "(final|overall).*(verdict|result|status)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'final verdict' or 'overall result' label in report"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-389 AC#7: Validation Report Format"
echo "=============================================="
echo "Agent-generator: $AGENT_GENERATOR"
echo "Compliance ref: $COMPLIANCE_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_section_status_table
run_test "2" test_pass_status_for_required
run_test "3" test_fail_status_for_required
run_test "4" test_warn_status_for_optional
run_test "5" test_na_status
run_test "6" test_frontmatter_validation_in_report
run_test "7" test_summary_line_with_counts
run_test "8" test_three_verdicts
run_test "9" test_final_verdict_label

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
