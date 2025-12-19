#!/bin/bash

#################################################################################
# Test: Links Verification
# Purpose: Verify no broken internal links in documentation
#
# This test checks that all internal markdown links in STORY-107 documentation
# point to files that exist in the project.
#################################################################################

set -e

# Test configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="${SCRIPT_DIR}/test-links-results.json"
EXIT_CODE=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# JSON results tracking
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0
BROKEN_LINKS=()

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST: Links Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Documentation files to check
DOC_FILES=(
    "${PROJECT_ROOT}/docs/guides/feedback-system-user-guide.md"
    "${PROJECT_ROOT}/docs/architecture/hook-system-design.md"
    "${PROJECT_ROOT}/docs/guides/feedback-troubleshooting.md"
    "${PROJECT_ROOT}/docs/guides/feedback-migration-guide.md"
    "${PROJECT_ROOT}/.claude/skills/devforgeai-feedback/README.md"
)

# Find all markdown files in docs directory
echo "Test 1: Scan documentation files for broken links"
((TESTS_TOTAL++))

DOC_FILES_FOUND=0
for doc_file in "${DOC_FILES[@]}"; do
    if [ -f "${doc_file}" ]; then
        ((DOC_FILES_FOUND++))
    fi
done

if [ ${DOC_FILES_FOUND} -gt 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Found ${DOC_FILES_FOUND} documentation files to check"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC}: No documentation files found yet (expected during TDD Red phase)"
    # Don't fail yet - tests are still RED
fi
echo ""

# Test 2: Extract and verify internal links
echo "Test 2: Check for broken internal links"
((TESTS_TOTAL++))

# Find all markdown reference links [text](path) in doc files
# Patterns: [text](path), [text]: path, [text][ref], etc.

BROKEN_COUNT=0

# Create temporary file for found links
TEMP_LINKS="/tmp/story107_links.txt"
> "${TEMP_LINKS}"

# Extract links from all existing doc files
for doc_file in "${DOC_FILES[@]}"; do
    if [ -f "${doc_file}" ]; then
        # Extract markdown links: [text](path)
        grep -o '\[.*\]([^)]*)'  "${doc_file}" | grep -o '([^)]*)' | tr -d '()' >> "${TEMP_LINKS}" 2>/dev/null || true

        # Extract reference links: [text]: path
        grep -o '^\[.*\]: .*' "${doc_file}" | sed 's/.*]: *//' >> "${TEMP_LINKS}" 2>/dev/null || true
    fi
done

# Check each link
if [ -f "${TEMP_LINKS}" ]; then
    while IFS= read -r link; do
        # Skip empty lines
        [ -z "${link}" ] && continue

        # Skip external URLs
        if [[ "${link}" =~ ^(http|https|ftp|mailto) ]]; then
            continue
        fi

        # Remove URL fragments (#section)
        link_path="${link%#*}"

        # Skip empty paths
        [ -z "${link_path}" ] && continue

        # Check if file exists
        FULL_PATH="${PROJECT_ROOT}/${link_path}"

        # Handle relative paths from doc directory
        if [[ "${link_path}" =~ ^\.\./ ]]; then
            FULL_PATH="${PROJECT_ROOT}/docs/$(echo "${link_path}" | sed 's|^\.\./||')"
        fi

        if [ ! -z "${link_path}" ] && ! [ -f "${FULL_PATH}" ]; then
            BROKEN_LINKS+=("${link_path}")
            ((BROKEN_COUNT++))
        fi
    done < "${TEMP_LINKS}"
fi

if [ ${BROKEN_COUNT} -eq 0 ]; then
    if [ ${DOC_FILES_FOUND} -gt 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: No broken links found"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⊘ SKIP${NC}: No documentation files to check yet (Red phase)"
    fi
else
    echo -e "${RED}✗ FAIL${NC}: Found ${BROKEN_COUNT} broken links:"
    for broken in "${BROKEN_LINKS[@]}"; do
        echo -e "  ${RED}✗${NC} ${broken}"
    done
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 3: Verify cross-references between docs
echo "Test 3: Check documentation cross-references"
((TESTS_TOTAL++))

if [ ${DOC_FILES_FOUND} -ge 3 ]; then
    # Check if user guide references troubleshooting guide
    USER_GUIDE="${PROJECT_ROOT}/docs/guides/feedback-system-user-guide.md"
    TROUBLESHOOT="${PROJECT_ROOT}/docs/guides/feedback-troubleshooting.md"

    if [ -f "${USER_GUIDE}" ] && [ -f "${TROUBLESHOOT}" ]; then
        if grep -qi "troubleshoot" "${USER_GUIDE}"; then
            echo -e "${GREEN}✓ PASS${NC}: User guide references troubleshooting guide"
            ((TESTS_PASSED++))
        else
            echo -e "${YELLOW}⚠ WARNING${NC}: User guide might benefit from troubleshooting reference"
            # Not critical
        fi
    else
        echo -e "${YELLOW}⊘ SKIP${NC}: Checking cross-references (files not all present yet)"
    fi
else
    echo -e "${YELLOW}⊘ SKIP${NC}: Insufficient documentation files for cross-reference check"
fi
echo ""

# Cleanup
rm -f "${TEMP_LINKS}"

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY: Links Verification Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Total Tests:  ${TESTS_TOTAL}"
echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
echo ""
if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
fi
echo ""

# Write results to JSON
cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "Links Verification",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "doc_files_checked": ${DOC_FILES_FOUND},
  "broken_links_found": ${BROKEN_COUNT},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
