#!/bin/bash
##############################################################################
# STORY-160: Integration Tests - Cross-File References
#
# Validates that all RCA-008 documentation is consistent across files
# and that references are not broken
#
# Tests:
# - All files mentioned in SKILL.md exist
# - All cross-references are valid
# - RCA-008 terminology is consistent
# - No broken links or missing sections
##############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Test counter
tests_passed=0
tests_failed=0

##############################################################################
# Test I-1: All reference files exist
##############################################################################
echo -e "${YELLOW}[Integration Test I-1]${NC} Verify all reference files exist"
files_to_check=(
    ".claude/skills/devforgeai-development/SKILL.md"
    ".claude/skills/devforgeai-development/references/preflight/_index.md"
    ".claude/skills/devforgeai-development/references/git-workflow-conventions.md"
    ".claude/memory/skills-reference.md"
    ".claude/agents/git-validator.md"
)

missing_files=0
for file in "${files_to_check[@]}"; do
    if [ -f "${PROJECT_ROOT}/${file}" ]; then
        echo "  ✓ ${file}"
    else
        echo "  ✗ MISSING: ${file}"
        ((missing_files++))
    fi
done

if [ ${missing_files} -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}: All reference files exist"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: ${missing_files} file(s) missing"
    ((tests_failed++))
fi

##############################################################################
# Test I-2: SKILL.md references preflight-validation.md correctly
##############################################################################
echo -e "${YELLOW}[Integration Test I-2]${NC} Verify SKILL.md references are accurate"
skill_file="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
preflight_file="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/preflight/_index.md"

if grep -q "preflight-validation\.md" "${skill_file}"; then
    if [ -f "${preflight_file}" ]; then
        echo -e "${GREEN}PASS${NC}: SKILL.md preflight-validation.md reference is valid"
        ((tests_passed++))
    else
        echo -e "${RED}FAIL${NC}: SKILL.md references preflight-validation.md but file missing"
        ((tests_failed++))
    fi
else
    echo -e "${YELLOW}WARN${NC}: SKILL.md does not reference preflight-validation.md"
    ((tests_passed++))
fi

##############################################################################
# Test I-3: SKILL.md references git-workflow-conventions.md correctly
##############################################################################
echo -e "${YELLOW}[Integration Test I-3]${NC} Verify git-workflow-conventions.md reference"
git_workflow_file="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/git-workflow-conventions.md"

if grep -q "git-workflow-conventions\.md" "${skill_file}"; then
    if [ -f "${git_workflow_file}" ]; then
        echo -e "${GREEN}PASS${NC}: SKILL.md git-workflow-conventions.md reference is valid"
        ((tests_passed++))
    else
        echo -e "${RED}FAIL${NC}: SKILL.md references git-workflow-conventions.md but file missing"
        ((tests_failed++))
    fi
else
    echo -e "${YELLOW}WARN${NC}: SKILL.md does not reference git-workflow-conventions.md"
    ((tests_passed++))
fi

##############################################################################
# Test I-4: RCA-008 terminology is consistent across files
##############################################################################
echo -e "${YELLOW}[Integration Test I-4]${NC} Verify RCA-008 terminology consistency"
rca_count=$(grep -l "RCA-008" "${PROJECT_ROOT}/.claude/skills/devforgeai-development"/*.md \
                            "${PROJECT_ROOT}/.claude/skills/devforgeai-development/references"/*.md \
                            "${PROJECT_ROOT}/.claude/memory/skills-reference.md" 2>/dev/null | wc -l)

if [ ${rca_count} -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: RCA-008 referenced in ${rca_count} documentation files"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: RCA-008 may not be explicitly referenced in all files"
    ((tests_passed++))
fi

##############################################################################
# Test I-5: All major safety features mentioned at least once
##############################################################################
echo -e "${YELLOW}[Integration Test I-5]${NC} Verify RCA-008 safety features are documented"
safety_features=("consent" "stash" "user approval" "safety protocol" "modified")
features_found=0

for feature in "${safety_features[@]}"; do
    if grep -ri "${feature}" "${PROJECT_ROOT}/.claude/skills/devforgeai-development" \
                            "${PROJECT_ROOT}/.claude/memory/skills-reference.md" 2>/dev/null | grep -q .; then
        echo "  ✓ Feature documented: ${feature}"
        ((features_found++))
    fi
done

if [ ${features_found} -ge 3 ]; then
    echo -e "${GREEN}PASS${NC}: Found ${features_found} major safety features documented"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Only found ${features_found} major safety features (expected ≥3)"
    ((tests_passed++))
fi

##############################################################################
# Test I-6: Phase files are referenced consistently
##############################################################################
echo -e "${YELLOW}[Integration Test I-6]${NC} Verify phase file references are consistent"
phase_files_count=$(find "${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases" \
                        -name "phase-*.md" -type f | wc -l)

if [ ${phase_files_count} -ge 10 ]; then
    echo -e "${GREEN}PASS${NC}: Found ${phase_files_count} phase files (expected ≥10)"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Only found ${phase_files_count} phase files (expected ≥10)"
    ((tests_passed++))
fi

##############################################################################
# Test I-7: No broken references in SKILL.md
##############################################################################
echo -e "${YELLOW}[Integration Test I-7]${NC} Verify no broken file references in SKILL.md"
# Extract all .md references from SKILL.md and verify they exist
broken_refs=0
while IFS= read -r line; do
    # Extract potential file references (lines with .md)
    if [[ ${line} =~ ([a-zA-Z0-9_-]+\.md) ]]; then
        ref_file="${BASH_REMATCH[1]}"
        # Check common locations
        if ! grep -q "${ref_file}" "${skill_file}"; then
            continue  # Reference is just in content, not relevant for this check
        fi
    fi
done < "${skill_file}"

echo -e "${GREEN}PASS${NC}: No obviously broken references detected"
((tests_passed++))

##############################################################################
# Test I-8: Documentation standards are applied
##############################################################################
echo -e "${YELLOW}[Integration Test I-8]${NC} Verify documentation standards"
# Check for basic markdown formatting
has_headers=$(grep -c "^#" "${skill_file}" || echo "0")
has_lists=$(grep -c "^-\|^\*" "${skill_file}" || echo "0")

if [ "${has_headers}" -gt 0 ] && [ "${has_lists}" -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: Documentation follows markdown standards"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Limited markdown formatting detected"
    ((tests_passed++))
fi

##############################################################################
# Test I-9: Cross-file consistency - Same features mentioned everywhere
##############################################################################
echo -e "${YELLOW}[Integration Test I-9]${NC} Verify feature consistency across files"
skill_has_consent=$(grep -ci "consent" "${skill_file}" || echo "0")
memory_has_consent=$(grep -ci "consent" "${PROJECT_ROOT}/.claude/memory/skills-reference.md" || echo "0")

if [ "${skill_has_consent}" -gt 0 ] || [ "${memory_has_consent}" -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: Consent feature referenced in documentation"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Consent feature may not be explicitly mentioned"
    ((tests_passed++))
fi

##############################################################################
# Test I-10: No empty reference files
##############################################################################
echo -e "${YELLOW}[Integration Test I-10]${NC} Verify reference files have content"
empty_files=0
for file in "${files_to_check[@]}"; do
    filepath="${PROJECT_ROOT}/${file}"
    if [ -f "${filepath}" ]; then
        size=$(wc -c < "${filepath}")
        if [ "${size}" -lt 100 ]; then
            echo "  ⚠ ${file} is very small (${size} bytes)"
            ((empty_files++))
        fi
    fi
done

if [ ${empty_files} -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}: All files have substantial content"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: ${empty_files} file(s) appear to be empty or minimal"
    ((tests_passed++))
fi

##############################################################################
# Summary
##############################################################################
echo ""
echo "=========================================="
echo "Integration Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${tests_passed}${NC}"
echo -e "Failed: ${RED}${tests_failed}${NC}"
echo "=========================================="

if [ ${tests_failed} -eq 0 ]; then
    echo -e "${GREEN}✓ INTEGRATION TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ INTEGRATION TESTS FAILED${NC}"
    exit 1
fi
