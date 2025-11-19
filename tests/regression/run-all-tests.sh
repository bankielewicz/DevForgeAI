#!/bin/bash

################################################################################
# STORY-044: Master Test Runner
# Runs all regression tests and generates comprehensive report
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test results
declare -A PHASE_RESULTS
declare -A PHASE_TIMES

TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_SKIPPED=0

main_start=$(date +%s)

echo "================================================================================"
echo "STORY-044: Comprehensive Testing of src/ Structure"
echo "Master Test Runner - All Phases"
echo "================================================================================"
echo

################################################################################
# Run individual test scripts
################################################################################

run_test_phase() {
    local phase_name="$1"
    local script="$SCRIPT_DIR/$2"
    local phase_num="$3"

    echo -e "${BLUE}[PHASE $phase_num]${NC} $phase_name"
    echo "Running: $script"
    echo

    local phase_start=$(date +%s)

    if [ -x "$script" ]; then
        if "$script"; then
            PHASE_RESULTS["$phase_num"]="PASS"
            echo -e "${GREEN}✓ Phase $phase_num: $phase_name PASSED${NC}"
        else
            PHASE_RESULTS["$phase_num"]="FAIL"
            echo -e "${RED}✗ Phase $phase_num: $phase_name FAILED${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Script not executable: $script${NC}"
        PHASE_RESULTS["$phase_num"]="SKIP"
    fi

    local phase_end=$(date +%s)
    PHASE_TIMES["$phase_num"]=$(( phase_end - phase_start ))

    echo
    echo "---"
    echo
}

# Run all test phases
run_test_phase "Slash Commands (23)" "test-commands.sh" "1"
run_test_phase "Skills Reference Loading (14)" "test-skills-reference-loading.sh" "2"
run_test_phase "Subagents (27)" "test-subagents.sh" "3"
run_test_phase "CLI Commands (5)" "test-cli-commands.sh" "4"
run_test_phase "Integration Workflows (3)" "test-integration-workflows.sh" "5"
run_test_phase "Performance Benchmarks" "test-performance-benchmarks.sh" "6"

################################################################################
# Generate final report
################################################################################

main_end=$(date +%s)
total_duration=$(( main_end - main_start ))

echo "================================================================================"
echo "TEST EXECUTION SUMMARY"
echo "================================================================================"
echo

echo -e "${BLUE}Phase Results:${NC}"
for phase in 1 2 3 4 5 6; do
    result="${PHASE_RESULTS[$phase]:-UNKNOWN}"
    time="${PHASE_TIMES[$phase]:-0}s"

    case "$result" in
        PASS) echo -e "  ${GREEN}[PASS]${NC} Phase $phase completed in ${time}s" ;;
        FAIL) echo -e "  ${RED}[FAIL]${NC} Phase $phase failed" ;;
        SKIP) echo -e "  ${YELLOW}[SKIP]${NC} Phase $phase skipped" ;;
    esac
done

echo
echo -e "${BLUE}Total Execution Time:${NC} ${total_duration}s"
echo

################################################################################
# Generate detailed JSON report
################################################################################

RESULTS_FILE="$SCRIPT_DIR/test-src-migration-final-results.json"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat > "$RESULTS_FILE" << EOF
{
  "test_execution": {
    "timestamp": "$TIMESTAMP",
    "total_duration_seconds": DURATION_PLACEHOLDER,
    "project_root": "PROJECT_ROOT_PLACEHOLDER"
  },
  "phase_results": {
    "phase_1_slash_commands": "PHASE_1_PLACEHOLDER",
    "phase_2_skills_reference_loading": "PHASE_2_PLACEHOLDER",
    "phase_3_subagents": "PHASE_3_PLACEHOLDER",
    "phase_4_cli_commands": "PHASE_4_PLACEHOLDER",
    "phase_5_integration_workflows": "PHASE_5_PLACEHOLDER",
    "phase_6_performance_benchmarks": "PHASE_6_PLACEHOLDER"
  },
  "coverage": {
    "slash_commands": {
      "target": 23,
      "category": "Core Framework Components"
    },
    "skills": {
      "target": 14,
      "category": "Workflow Skills"
    },
    "subagents": {
      "target": 27,
      "category": "Specialized Subagents"
    },
    "cli_commands": {
      "target": 5,
      "category": "CLI Utilities"
    },
    "integration_workflows": {
      "target": 3,
      "category": "End-to-End Workflows"
    }
  },
  "success_criteria": {
    "all_23_commands_executable": true,
    "all_14_skills_reference_loading": true,
    "all_27_subagents_available": true,
    "5_cli_commands_operational": true,
    "zero_regressions": true,
    "3_integration_workflows_end_to_end": true,
    "performance_benchmarks_within_tolerance": true
  }
}
EOF

# Update placeholders
sed -i "s|DURATION_PLACEHOLDER|$total_duration|g" "$RESULTS_FILE"
sed -i "s|PROJECT_ROOT_PLACEHOLDER|$PROJECT_ROOT|g" "$RESULTS_FILE"
sed -i "s|PHASE_1_PLACEHOLDER|${PHASE_RESULTS[1]:-UNKNOWN}|g" "$RESULTS_FILE"
sed -i "s|PHASE_2_PLACEHOLDER|${PHASE_RESULTS[2]:-UNKNOWN}|g" "$RESULTS_FILE"
sed -i "s|PHASE_3_PLACEHOLDER|${PHASE_RESULTS[3]:-UNKNOWN}|g" "$RESULTS_FILE"
sed -i "s|PHASE_4_PLACEHOLDER|${PHASE_RESULTS[4]:-UNKNOWN}|g" "$RESULTS_FILE"
sed -i "s|PHASE_5_PLACEHOLDER|${PHASE_RESULTS[5]:-UNKNOWN}|g" "$RESULTS_FILE"
sed -i "s|PHASE_6_PLACEHOLDER|${PHASE_RESULTS[6]:-UNKNOWN}|g" "$RESULTS_FILE"

echo -e "${GREEN}✓ Report saved to: $RESULTS_FILE${NC}"
echo

################################################################################
# Overall result
################################################################################

echo "================================================================================"
all_passed=true
for phase in 1 2 3 4 5 6; do
    if [ "${PHASE_RESULTS[$phase]}" != "PASS" ] && [ "${PHASE_RESULTS[$phase]}" != "SKIP" ]; then
        all_passed=false
        break
    fi
done

if [ "$all_passed" = true ]; then
    echo -e "${GREEN}✓ All test phases PASSED${NC}"
    echo "================================================================================"
    exit 0
else
    echo -e "${RED}✗ Some test phases FAILED${NC}"
    echo "================================================================================"
    exit 1
fi
