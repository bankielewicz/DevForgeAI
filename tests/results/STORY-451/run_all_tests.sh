#!/bin/bash
# Run All Tests: STORY-451 YAML Frontmatter, Metadata and Naming Housekeeping
# Generated: 2026-02-19

SCRIPT_DIR="/mnt/c/Projects/DevForgeAI2/tests/results/STORY-451"
TOTAL_PASSED=0
TOTAL_FAILED=0
SCRIPTS_FAILED=0

run_suite() {
    local script="$1"
    echo ""
    bash "$script"
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        ((SCRIPTS_FAILED++))
    fi
}

chmod +x "$SCRIPT_DIR"/test_ac*.sh

run_suite "$SCRIPT_DIR/test_ac1_yaml_frontmatter.sh"
run_suite "$SCRIPT_DIR/test_ac2_naming_description.sh"
run_suite "$SCRIPT_DIR/test_ac3_xml_tag_naming.sh"
run_suite "$SCRIPT_DIR/test_ac4_orphaned_tag_removal.sh"

echo ""
echo "========================================"
echo "  STORY-451 Test Suite Complete"
echo "  Test scripts failed: $SCRIPTS_FAILED / 4"
echo "========================================"

[ $SCRIPTS_FAILED -eq 0 ] && exit 0 || exit 1
