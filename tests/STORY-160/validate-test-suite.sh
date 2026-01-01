#!/bin/bash
##############################################################################
# Validate Test Suite Structure
# 
# Sanity checks for the test suite itself to ensure all tests are properly
# structured and can be executed
##############################################################################

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Test Suite Validation${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo ""

TEST_DIR="/mnt/c/Projects/DevForgeAI2/tests/STORY-160"
passed=0
failed=0

##############################################################################
# V-1: All test scripts exist
##############################################################################
echo -e "${YELLOW}[V-1]${NC} Verify all test scripts exist"

required_scripts=(
    "test-ac1-skill-md-validation-steps.sh"
    "test-ac2-reference-files-documented.sh"
    "test-ac3-subagent-coordination-updated.sh"
    "test-ac4-changelog-entry.sh"
    "test-ac5-skills-reference-memory-file.sh"
    "test-integration-cross-file-references.sh"
    "test-documentation-accuracy.sh"
    "run-all-tests.sh"
)

missing=0
for script in "${required_scripts[@]}"; do
    if [ -f "${TEST_DIR}/${script}" ]; then
        echo "  ✓ ${script}"
    else
        echo "  ✗ MISSING: ${script}"
        ((missing++))
    fi
done

if [ ${missing} -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}: All required test scripts present"
    ((passed++))
else
    echo -e "${RED}FAIL${NC}: ${missing} script(s) missing"
    ((failed++))
fi
echo ""

##############################################################################
# V-2: All scripts are executable
##############################################################################
echo -e "${YELLOW}[V-2]${NC} Verify all scripts are executable"

non_exec=0
for script in "${required_scripts[@]}"; do
    if [ -x "${TEST_DIR}/${script}" ]; then
        echo "  ✓ ${script} is executable"
    else
        echo "  ✗ ${script} is NOT executable"
        ((non_exec++))
    fi
done

if [ ${non_exec} -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}: All scripts are executable"
    ((passed++))
else
    echo -e "${RED}FAIL${NC}: ${non_exec} script(s) not executable"
    ((failed++))
fi
echo ""

##############################################################################
# V-3: All scripts have proper shebang
##############################################################################
echo -e "${YELLOW}[V-3]${NC} Verify all scripts have proper shebang"

bad_shebang=0
for script in "${required_scripts[@]}"; do
    first_line=$(head -1 "${TEST_DIR}/${script}")
    if [[ "${first_line}" == "#!/bin/bash" ]]; then
        echo "  ✓ ${script}"
    else
        echo "  ✗ ${script} - Bad shebang: ${first_line}"
        ((bad_shebang++))
    fi
done

if [ ${bad_shebang} -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}: All scripts have proper shebang"
    ((passed++))
else
    echo -e "${RED}FAIL${NC}: ${bad_shebang} script(s) have bad shebang"
    ((failed++))
fi
echo ""

##############################################################################
# V-4: All scripts have set -euo pipefail
##############################################################################
echo -e "${YELLOW}[V-4]${NC} Verify all scripts have proper error handling"

bad_settings=0
for script in "${required_scripts[@]}"; do
    if grep -q "set -euo pipefail" "${TEST_DIR}/${script}"; then
        echo "  ✓ ${script}"
    else
        echo "  ✗ ${script} - Missing: set -euo pipefail"
        ((bad_settings++))
    fi
done

if [ ${bad_settings} -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}: All scripts have proper error handling"
    ((passed++))
else
    echo -e "${YELLOW}WARN${NC}: ${bad_settings} script(s) may have incomplete error handling"
    ((passed++))
fi
echo ""

##############################################################################
# V-5: All scripts have test blocks
##############################################################################
echo -e "${YELLOW}[V-5]${NC} Verify all scripts have test implementations"

test_ac_count=0
for script in test-ac*.sh; do
    full_path="${TEST_DIR}/${script}"
    if [ -f "${full_path}" ]; then
        test_blocks=$(grep -c "echo -e.*TEST.*AC-" "${full_path}" || echo "0")
        if [ "${test_blocks}" -gt 0 ]; then
            echo "  ✓ ${script} (${test_blocks} test blocks)"
            ((test_ac_count++))
        else
            echo "  ✗ ${script} (no test blocks found)"
        fi
    fi
done

if [ "${test_ac_count}" -eq 5 ]; then
    echo -e "${GREEN}PASS${NC}: All AC test scripts have test blocks"
    ((passed++))
else
    echo -e "${RED}FAIL${NC}: Only ${test_ac_count}/5 AC test scripts found"
    ((failed++))
fi
echo ""

##############################################################################
# V-6: All AC tests reference correct file
##############################################################################
echo -e "${YELLOW}[V-6]${NC} Verify AC tests reference correct documentation files"

validation_ok=0
ac1_check=$(grep -c "SKILL.md\|preflight-validation.md" "${TEST_DIR}/test-ac1-skill-md-validation-steps.sh" || echo "0")
ac2_check=$(grep -c "preflight-validation\|git-workflow-conventions" "${TEST_DIR}/test-ac2-reference-files-documented.sh" || echo "0")
ac3_check=$(grep -c "git-validator\|preflight" "${TEST_DIR}/test-ac3-subagent-coordination-updated.sh" || echo "0")
ac4_check=$(grep -c "SKILL.md\|Change Log\|RCA-008" "${TEST_DIR}/test-ac4-changelog-entry.sh" || echo "0")
ac5_check=$(grep -c "skills-reference.md" "${TEST_DIR}/test-ac5-skills-reference-memory-file.sh" || echo "0")

if [ "${ac1_check}" -gt 0 ]; then
    echo "  ✓ AC-1 test references correct files"
    ((validation_ok++))
fi
if [ "${ac2_check}" -gt 0 ]; then
    echo "  ✓ AC-2 test references correct files"
    ((validation_ok++))
fi
if [ "${ac3_check}" -gt 0 ]; then
    echo "  ✓ AC-3 test references correct files"
    ((validation_ok++))
fi
if [ "${ac4_check}" -gt 0 ]; then
    echo "  ✓ AC-4 test references correct files"
    ((validation_ok++))
fi
if [ "${ac5_check}" -gt 0 ]; then
    echo "  ✓ AC-5 test references correct files"
    ((validation_ok++))
fi

if [ "${validation_ok}" -eq 5 ]; then
    echo -e "${GREEN}PASS${NC}: All AC tests reference correct documentation files"
    ((passed++))
else
    echo -e "${RED}FAIL${NC}: Only ${validation_ok}/5 AC tests reference correct files"
    ((failed++))
fi
echo ""

##############################################################################
# V-7: Test runner includes all AC tests
##############################################################################
echo -e "${YELLOW}[V-7]${NC} Verify test runner includes all AC tests"

runner_file="${TEST_DIR}/run-all-tests.sh"
ac1_in_runner=$(grep -c "test-ac1\|AC-1" "${runner_file}" || echo "0")
ac2_in_runner=$(grep -c "test-ac2\|AC-2" "${runner_file}" || echo "0")
ac3_in_runner=$(grep -c "test-ac3\|AC-3" "${runner_file}" || echo "0")
ac4_in_runner=$(grep -c "test-ac4\|AC-4" "${runner_file}" || echo "0")
ac5_in_runner=$(grep -c "test-ac5\|AC-5" "${runner_file}" || echo "0")

ac_in_runner=0
[ "${ac1_in_runner}" -gt 0 ] && ((ac_in_runner++))
[ "${ac2_in_runner}" -gt 0 ] && ((ac_in_runner++))
[ "${ac3_in_runner}" -gt 0 ] && ((ac_in_runner++))
[ "${ac4_in_runner}" -gt 0 ] && ((ac_in_runner++))
[ "${ac5_in_runner}" -gt 0 ] && ((ac_in_runner++))

if [ "${ac_in_runner}" -eq 5 ]; then
    echo -e "${GREEN}PASS${NC}: Test runner includes all 5 AC tests"
    ((passed++))
else
    echo -e "${RED}FAIL${NC}: Test runner only includes ${ac_in_runner}/5 AC tests"
    ((failed++))
fi
echo ""

##############################################################################
# V-8: Documentation exists
##############################################################################
echo -e "${YELLOW}[V-8]${NC} Verify test documentation exists"

docs_present=0
if [ -f "${TEST_DIR}/README.md" ]; then
    echo "  ✓ README.md exists"
    ((docs_present++))
fi
if [ -f "${TEST_DIR}/VERIFICATION-REPORT.md" ]; then
    echo "  ✓ VERIFICATION-REPORT.md exists"
    ((docs_present++))
fi

if [ "${docs_present}" -eq 2 ]; then
    echo -e "${GREEN}PASS${NC}: All documentation files present"
    ((passed++))
else
    echo -e "${YELLOW}WARN${NC}: Only ${docs_present}/2 documentation files present"
    ((passed++))
fi
echo ""

##############################################################################
# Summary
##############################################################################
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo "Validation Results"
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "Passed: ${GREEN}${passed}${NC}"
echo -e "Failed: ${RED}${failed}${NC}"
echo ""

if [ ${failed} -eq 0 ]; then
    echo -e "${GREEN}✓ TEST SUITE VALIDATION PASSED${NC}"
    echo -e "${GREEN}All test scripts are properly structured and ready to execute.${NC}"
    exit 0
else
    echo -e "${RED}✗ TEST SUITE VALIDATION FAILED${NC}"
    echo -e "${RED}Please fix the ${failed} issue(s) above.${NC}"
    exit 1
fi
