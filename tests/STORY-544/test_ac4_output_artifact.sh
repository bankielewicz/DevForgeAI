#!/bin/bash
# Test: AC#4 - Output Artifact Written to Correct Path with Disclaimer Header
# Story: STORY-544
# Generated: 2026-03-04
# TDD Phase: RED (all tests expected to FAIL - source files do not exist yet)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
GUIDE_FILE="${PROJECT_ROOT}/src/claude/skills/advising-legal/references/business-structure-guide.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#4: Output Artifact Path and Disclaimer ==="
echo ""

# === Arrange ===
# The guide file must define the output artifact path and disclaimer template

# === Act & Assert ===

# Test 1: Guide file exists (source of truth for output artifact format)
test -f "$GUIDE_FILE"
run_test "test_should_exist_when_guide_file_created" $?

# Test 2: Output path documented in guide
grep -qi "devforgeai/specs/business/legal/business-structure.md\|output.*artifact.*path\|output.*path.*business-structure" "$GUIDE_FILE" 2>/dev/null
run_test "test_should_document_output_path_when_artifact_format_defined" $?

# Test 3: Disclaimer header template defined
grep -qi "disclaimer.*header\|disclaimer.*template\|standard.*disclaimer" "$GUIDE_FILE" 2>/dev/null
run_test "test_should_define_disclaimer_header_template_when_output_format_specified" $?

# Test 4: Disclaimer must appear in first 3 lines (documented as requirement)
grep -qi "first.*3.*line\|line.*1.*3\|lines.*1-3\|top.*three.*line" "$GUIDE_FILE" 2>/dev/null
run_test "test_should_specify_disclaimer_in_first_3_lines_when_output_format_defined" $?

# Test 5: Decision path summary section documented
grep -qi "decision.*path.*summary\|path.*summary\|summary.*decision\|user.*decision.*path" "$GUIDE_FILE" 2>/dev/null
run_test "test_should_include_decision_path_summary_when_output_format_defined" $?

# Test 6: Educational-only scope language in disclaimer
grep -qi "educational.*only\|not.*legal.*advice\|informational.*purpose\|general.*guidance" "$GUIDE_FILE" 2>/dev/null
run_test "test_should_contain_educational_only_language_when_disclaimer_defined" $?

# Test 7: Guide is sole authoritative source for entity descriptions
grep -qi "authoritative.*source\|single.*source.*truth\|sole.*source\|canonical.*source" "$GUIDE_FILE" 2>/dev/null
run_test "test_should_be_sole_authoritative_source_when_entity_descriptions_referenced" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
