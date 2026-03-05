#!/bin/bash
# Test: AC#2 - Entity Recommendations Include Contextual Rationale
# Story: STORY-544
# Generated: 2026-03-04
# TDD Phase: RED (all tests expected to FAIL - source files do not exist yet)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/src/claude/skills/advising-legal/references/business-structure-guide.md"

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

echo "=== AC#2: Entity Recommendations with Rationale ==="
echo ""

# === Arrange ===
# Target: business-structure-guide.md must contain recommendation output structure

# === Act & Assert ===

# Test 1: Source file exists
test -f "$TARGET_FILE"
run_test "test_should_exist_when_guide_file_created" $?

# Test 2: Entity name included in recommendation section
grep -qi "recommended.*entity\|entity.*recommendation\|recommendation.*output" "$TARGET_FILE" 2>/dev/null
run_test "test_should_include_entity_name_in_recommendation_when_output_generated" $?

# Test 3: Plain-language rationale section exists
grep -qi "rationale\|why this.*fits\|explanation.*match\|plain.language" "$TARGET_FILE" 2>/dev/null
run_test "test_should_include_plain_language_rationale_when_recommendation_produced" $?

# Test 4: Comparison of top two candidates documented
grep -qi "comparison\|top two\|close.*score\|runner.up\|alternate.*candidate" "$TARGET_FILE" 2>/dev/null
run_test "test_should_include_comparison_of_top_two_when_scores_close" $?

# Test 5: Disclaimer header documented
grep -qi "disclaimer\|educational.*only\|not.*legal.*advice\|informational.*purpose" "$TARGET_FILE" 2>/dev/null
run_test "test_should_include_disclaimer_header_when_recommendation_output_defined" $?

# Test 6: Each entity type has a description section
for entity in "Sole Proprietorship" "LLC" "S-Corp" "C-Corp"; do
    grep -qi "$entity" "$TARGET_FILE" 2>/dev/null
    if [ $? -eq 0 ]; then
        # Check that there is descriptive content near the entity mention
        grep -A5 -i "$entity" "$TARGET_FILE" 2>/dev/null | grep -qi "description\|overview\|suited.*for\|best.*for\|ideal.*for\|characteristics"
        run_test "test_should_have_description_for_${entity// /_}_when_entities_documented" $?
    else
        run_test "test_should_have_description_for_${entity// /_}_when_entities_documented" 1
    fi
done

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
