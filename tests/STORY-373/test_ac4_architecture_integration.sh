#!/bin/bash
##############################################################################
# Test Suite: STORY-373 AC#4 - Integration with devforgeai-architecture
#                               for brownfield analysis
# Purpose: Verify architecture skill queries treelint map during brownfield
#          analysis, extracts top 50 symbols, and generates Key Symbols section
# Phase: TDD Red - All tests expected to FAIL before implementation
##############################################################################

set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MAP_REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/references/treelint-repository-map.md"
ARCH_REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-architecture/references/brownfield-map-integration.md"
ARCH_SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-architecture/SKILL.md"

run_test() {
    local test_name=$1
    local test_func=$2
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n[Test $TESTS_RUN] $test_name"
    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASSED${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAILED${NC}"
    fi
}

# AC#4 Test 1: Architecture brownfield integration reference file exists
test_arch_integration_ref_exists() {
    [ -f "$ARCH_REF_FILE" ]
}

# AC#4 Test 2: Architecture skill references brownfield map integration
test_arch_skill_references_brownfield_map() {
    [ -f "$ARCH_SKILL_FILE" ] && grep -qi 'brownfield-map-integration\|repository.*map\|treelint.*map' "$ARCH_SKILL_FILE"
}

# AC#4 Test 3: Brownfield integration references treelint map --ranked command
test_brownfield_uses_map_ranked() {
    [ -f "$ARCH_REF_FILE" ] && grep -q 'treelint map --ranked' "$ARCH_REF_FILE"
}

# AC#4 Test 4: Brownfield integration specifies top 50 symbols extraction
test_brownfield_top_50_symbols() {
    [ -f "$ARCH_REF_FILE" ] && grep -q 'top 50\|top-50\|K.*50\|50.*symbols' "$ARCH_REF_FILE"
}

# AC#4 Test 5: Key Symbols section documented for architecture output
test_key_symbols_section_documented() {
    [ -f "$ARCH_REF_FILE" ] && grep -qi 'Key Symbols' "$ARCH_REF_FILE"
}

# AC#4 Test 6: Key Symbols section includes symbol name column
test_key_symbols_name_column() {
    [ -f "$ARCH_REF_FILE" ] && grep -qi 'name\|symbol.*name' "$ARCH_REF_FILE"
}

# AC#4 Test 7: Key Symbols section includes type column
test_key_symbols_type_column() {
    [ -f "$ARCH_REF_FILE" ] && grep -qi 'type' "$ARCH_REF_FILE"
}

# AC#4 Test 8: Key Symbols section includes reference count column
test_key_symbols_references_column() {
    [ -f "$ARCH_REF_FILE" ] && grep -qi 'references\|reference.*count\|ref.*count' "$ARCH_REF_FILE"
}

# AC#4 Test 9: Integration with project-context-discovery phase documented
test_project_context_discovery_phase() {
    [ -f "$ARCH_REF_FILE" ] && grep -qi 'project-context-discovery\|context.*discovery\|discovery.*phase' "$ARCH_REF_FILE"
}

# AC#4 Test 10: Brownfield mode detection documented
test_brownfield_mode_detection() {
    [ -f "$ARCH_REF_FILE" ] && grep -qi 'brownfield.*mode\|brownfield.*analysis\|existing.*codebase' "$ARCH_REF_FILE"
}

# AC#4 Test 11: Map service reference documented for cross-skill integration
test_cross_skill_map_reference() {
    [ -f "$ARCH_REF_FILE" ] && grep -qi 'treelint-repository-map\|map.*service\|TreelintRepositoryMapService' "$ARCH_REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-373 AC#4: Architecture brownfield integration"
echo "============================================================"

run_test "Architecture integration reference file exists" test_arch_integration_ref_exists
run_test "Architecture skill references brownfield map" test_arch_skill_references_brownfield_map
run_test "Brownfield uses treelint map --ranked" test_brownfield_uses_map_ranked
run_test "Top 50 symbols extraction specified" test_brownfield_top_50_symbols
run_test "Key Symbols section documented" test_key_symbols_section_documented
run_test "Key Symbols includes name column" test_key_symbols_name_column
run_test "Key Symbols includes type column" test_key_symbols_type_column
run_test "Key Symbols includes references column" test_key_symbols_references_column
run_test "Project-context-discovery phase integration" test_project_context_discovery_phase
run_test "Brownfield mode detection documented" test_brownfield_mode_detection
run_test "Cross-skill map service reference" test_cross_skill_map_reference

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
