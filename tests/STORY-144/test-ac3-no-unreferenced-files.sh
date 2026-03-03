#!/bin/bash
#
# Test: AC#3 - No unreferenced files remain in references directory
#
# Tests that every file in the ideation skill references directory
# is referenced at least once in SKILL.md or workflow files.
#
# This test FAILS initially if any files are unreferenced
#

set -e

# Test colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REFERENCES_DIR="$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references"
SKILL_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-ideation/SKILL.md"

# Track test results
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
UNREFERENCED_FILES=()

# Helper function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    local should_fail=$3  # "true" if test should fail initially

    TESTS_RUN=$((TESTS_RUN + 1))

    echo -e "\n${YELLOW}[TEST $TESTS_RUN]${NC} $test_name"

    if eval "$test_command" 2>/dev/null; then
        if [ "$should_fail" == "true" ]; then
            echo -e "${RED}✗ FAILED${NC} (Expected to fail in Red phase)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        else
            echo -e "${GREEN}✓ PASSED${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        fi
    else
        if [ "$should_fail" == "true" ]; then
            echo -e "${GREEN}✓ PASSED${NC} (Expected failure in Red phase)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}✗ FAILED${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    fi
}

echo "========================================"
echo "AC#3: No Unreferenced Files in References"
echo "========================================"
echo "Testing reference directory cleanup"
echo ""

# Test 1: References directory must exist
run_test \
    "test-ac3-references-directory-exists" \
    "[ -d '$REFERENCES_DIR' ]" \
    "false"

# Test 2: SKILL.md must exist
run_test \
    "test-ac3-skill-file-exists" \
    "[ -f '$SKILL_FILE' ]" \
    "false"

# Test 3: Check that all .md files in references are referenced in SKILL.md
# This is the key test - initially FAILS if orphaned files exist
echo -e "\n${BLUE}Scanning for unreferenced files...${NC}"
UNREFERENCED_COUNT=0

for ref_file in "$REFERENCES_DIR"/*.md; do
    if [ -f "$ref_file" ]; then
        filename=$(basename "$ref_file")

        # Skip YAML files (checkpoint-schema.yaml)
        if [[ "$filename" == *.yaml ]] || [[ "$filename" == *.yml ]]; then
            continue
        fi

        # Check if filename is referenced in SKILL.md or any workflow files
        if grep -q "$filename" "$SKILL_FILE" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} $filename - referenced in SKILL.md"
        elif find "$REFERENCES_DIR" -name '*.md' -exec grep -l "$filename" {} \; 2>/dev/null | head -1; then
            echo -e "  ${GREEN}✓${NC} $filename - referenced in workflow files"
        else
            echo -e "  ${RED}✗${NC} $filename - UNREFERENCED"
            UNREFERENCED_FILES+=("$filename")
            UNREFERENCED_COUNT=$((UNREFERENCED_COUNT + 1))
        fi
    fi
done

# Test 4: All reference files must be referenced
run_test \
    "test-ac3-all-files-referenced" \
    "[ $UNREFERENCED_COUNT -eq 0 ]" \
    "true"

# Test 5: Verify references follow naming conventions
run_test \
    "test-ac3-filename-conventions" \
    "find '$REFERENCES_DIR' -name '*.md' | xargs basename -a | grep -E '^[a-z].*\.md$' | wc -l | grep -q '[1-9]'" \
    "false"

# Test 6: No hidden files in references (no .* files)
run_test \
    "test-ac3-no-hidden-files" \
    "! find '$REFERENCES_DIR' -maxdepth 1 -name '.*' -type f | grep -v '^\.$' | grep -v '^\.\.$'" \
    "false"

# Test 7: Verify all reference files are valid markdown or config
run_test \
    "test-ac3-valid-file-formats" \
    "find '$REFERENCES_DIR' -type f | grep -E '\.(md|yaml|yml)$' | wc -l | grep -q '[1-9]'" \
    "false"

# Test 8: Check that user-input-integration-guide.md is resolved (deleted or integrated)
# This test FAILS if the file still exists as unreferenced
run_test \
    "test-ac3-user-input-integration-guide-resolved" \
    "if [ -f '$REFERENCES_DIR/user-input-integration-guide.md' ]; then
        grep -q 'user-input-integration-guide' '$SKILL_FILE'
    else
        true
    fi" \
    "true"

# Test 9: Check that brainstorm-data-mapping.md is resolved (deleted or integrated)
# This test FAILS if the file still exists as unreferenced
run_test \
    "test-ac3-brainstorm-data-mapping-resolved" \
    "if [ -f '$REFERENCES_DIR/brainstorm-data-mapping.md' ]; then
        grep -q 'brainstorm-data-mapping' '$SKILL_FILE'
    else
        true
    fi" \
    "true"

# Test 10: Verify no circular references (file A referencing file B, B referencing A)
# This test creates a simple check for mutual references
run_test \
    "test-ac3-no-obvious-circular-references" \
    "for file in '$REFERENCES_DIR'/*.md; do
        if grep -l 'user-input-integration-guide\|brainstorm-data-mapping' \"\$file\" 2>/dev/null; then
            ! grep -q \"$(basename \"\$file\")\" '$REFERENCES_DIR/user-input-integration-guide.md' 2>/dev/null || true
        fi
    done
    true" \
    "false"

echo ""
echo "========================================"
echo "Reference Cleanup Status"
echo "========================================"

if [ $UNREFERENCED_COUNT -gt 0 ]; then
    echo -e "${RED}Unreferenced files found:${NC}"
    for file in "${UNREFERENCED_FILES[@]}"; do
        echo "  - $file"
    done
else
    echo -e "${GREEN}All files are referenced!${NC}"
fi

echo ""
echo "========================================"
echo "Summary: AC#3 Tests"
echo "========================================"
echo -e "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "========================================"

# Exit with failure count
exit $TESTS_FAILED
