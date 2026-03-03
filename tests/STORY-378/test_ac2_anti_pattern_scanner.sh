#!/bin/bash
# Test AC#2: anti-pattern-scanner Task() Has Treelint Context
# STORY-378: Update devforgeai-qa Skill for Treelint
#
# Validates:
# - anti-pattern-detection-workflow.md contains "Treelint Integration" near anti-pattern-scanner Task()
# - Treelint context note mentions "Treelint-enabled" keyword
# - Treelint context note mentions "fallback" keyword
# - Treelint context note is delimited with "**Treelint Integration:**" prefix (BR-003)
# - Note size under 800 characters (NFR-001)
#
# Expected: FAIL initially (TDD Red phase - no Treelint context in file)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
ANTI_PATTERN_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() { TESTS_PASSED=$((TESTS_PASSED + 1)); echo "[PASS] $1"; }
fail_test() { TESTS_FAILED=$((TESTS_FAILED + 1)); echo "[FAIL] $1: $2"; }
run_test() { TESTS_RUN=$((TESTS_RUN + 1)); shift; "$@"; }

# Test 1: File exists
test_file_exists() {
    if [ -f "$ANTI_PATTERN_FILE" ]; then pass_test "anti-pattern-detection-workflow.md exists"
    else fail_test "anti-pattern-detection-workflow.md exists" "File not found"; fi
}

# Test 2: Contains Treelint-enabled keyword
test_treelint_enabled() {
    if grep -q "Treelint-enabled" "$ANTI_PATTERN_FILE"; then
        pass_test "Contains 'Treelint-enabled' keyword"
    else
        fail_test "Contains 'Treelint-enabled' keyword" "No 'Treelint-enabled' found"
    fi
}

# Test 3: Contains fallback keyword
test_fallback_keyword() {
    if grep -qi "fallback" "$ANTI_PATTERN_FILE"; then
        pass_test "Contains 'fallback' keyword"
    else
        fail_test "Contains 'fallback' keyword" "No 'fallback' found"
    fi
}

# Test 4: Treelint note uses **Treelint Integration:** delimiter (BR-003)
test_delimiter() {
    if grep -q '\*\*Treelint Integration:\*\*' "$ANTI_PATTERN_FILE"; then
        pass_test "Uses **Treelint Integration:** delimiter (BR-003)"
    else
        fail_test "Uses **Treelint Integration:** delimiter (BR-003)" "No '**Treelint Integration:**' delimiter found"
    fi
}

# Test 5: Treelint context note under 800 characters (NFR-001)
test_note_size() {
    local note_content
    note_content=$(sed -n '/\*\*Treelint Integration:\*\*/,/^$/p' "$ANTI_PATTERN_FILE" | head -20)
    if [ -z "$note_content" ]; then
        fail_test "Treelint note under 800 chars" "No Treelint note found to measure"
        return
    fi
    local chars; chars=$(echo "$note_content" | wc -c)
    if [ "$chars" -le 800 ]; then
        pass_test "Treelint note under 800 chars (actual: $chars)"
    else
        fail_test "Treelint note under 800 chars" "Note has $chars characters (max: 800)"
    fi
}

# Test 6: Existing anti-pattern-scanner content still present (BR-001 additive only)
test_existing_content_preserved() {
    if grep -q "anti-pattern-scanner" "$ANTI_PATTERN_FILE" && grep -q "context_files" "$ANTI_PATTERN_FILE"; then
        pass_test "Existing anti-pattern-scanner content preserved"
    else
        fail_test "Existing anti-pattern-scanner content preserved" "Original content appears modified"
    fi
}

# Main execution
echo "======================================================="
echo "STORY-378 AC#2: anti-pattern-scanner Treelint Context"
echo "======================================================="
echo "Target: $ANTI_PATTERN_FILE"
echo "-------------------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_treelint_enabled
run_test "3" test_fallback_keyword
run_test "4" test_delimiter
run_test "5" test_note_size
run_test "6" test_existing_content_preserved

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
