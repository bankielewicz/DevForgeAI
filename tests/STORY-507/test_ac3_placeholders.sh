#!/bin/bash
# Test: AC#3 - Subsections Have Descriptive Placeholders
# Story: STORY-507
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/assets/templates/epic-template.md"

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

# Extract text between two markdown headers (section content)
extract_section() {
    local file="$1"
    local header="$2"
    # Get content from header until next ### or ## header
    awk -v h="### ${header}" 'found && /^##/{exit} $0==h{found=1} found{print}' "$file"
}

echo "=== AC#3: Subsections Have Descriptive Placeholders ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Design Rationale has bracketed placeholder
SECTION_CONTENT=$(extract_section "$TARGET_FILE" "Design Rationale")
echo "$SECTION_CONTENT" | grep -q '\[.*\]'
run_test "Design Rationale subsection contains bracketed placeholder text" $?

# Test 2: Rejected Alternatives has bracketed placeholder
SECTION_CONTENT=$(extract_section "$TARGET_FILE" "Rejected Alternatives")
echo "$SECTION_CONTENT" | grep -q '\[.*\]'
run_test "Rejected Alternatives subsection contains bracketed placeholder text" $?

# Test 3: Adversary/Threat Model has bracketed placeholder
SECTION_CONTENT=$(extract_section "$TARGET_FILE" "Adversary/Threat Model")
echo "$SECTION_CONTENT" | grep -q '\[.*\]'
run_test "Adversary/Threat Model subsection contains bracketed placeholder text" $?

# Test 4: Implementation Constraints has bracketed placeholder
SECTION_CONTENT=$(extract_section "$TARGET_FILE" "Implementation Constraints")
echo "$SECTION_CONTENT" | grep -q '\[.*\]'
run_test "Implementation Constraints subsection contains bracketed placeholder text" $?

# Test 5: Key Insights from Discovery has bracketed placeholder
SECTION_CONTENT=$(extract_section "$TARGET_FILE" "Key Insights from Discovery")
echo "$SECTION_CONTENT" | grep -q '\[.*\]'
run_test "Key Insights from Discovery subsection contains bracketed placeholder text" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
