#!/bin/bash

# STORY-183: Adaptive Parallel Validation Based on Story Type
# Status: TDD Red (should FAIL - feature not implemented)
#
# Tests validate that QA skill selects validators based on story type
# to optimize token usage (documentation stories don't need test-automator)

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
QA_SKILL="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"
PARALLEL_REF="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/parallel-validation.md"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

echo "========================================================================"
echo "STORY-183: Adaptive Parallel Validation Based on Story Type"
echo "========================================================================"
echo ""

# -----------------------------------------------------------------------------
# AC-1: Story Type Extracted in Phase 0
# -----------------------------------------------------------------------------
echo "--- AC-1: Story Type Extraction ---"
echo ""

echo "Test 1.1: QA skill extracts story type from YAML frontmatter"
if grep -qE "story[_-]?type|type:.*extract|extract.*type.*frontmatter" "$QA_SKILL" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} QA skill has story type extraction"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} QA skill missing story type extraction from frontmatter"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 1.2: Phase 0 includes story type detection step"
if grep -qE "Phase 0.*story.*type|story.*type.*Phase 0|detect.*story.*type" "$QA_SKILL" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Phase 0 has story type detection"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 0 missing story type detection step"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# -----------------------------------------------------------------------------
# AC-2: Documentation Stories Use Fewer Validators
# -----------------------------------------------------------------------------
echo ""
echo "--- AC-2: Documentation Stories Use Fewer Validators ---"
echo ""

echo "Test 2.1: Documentation story type skips test-automator"
if grep -qE "documentation.*skip.*test-automator|type.*documentation.*no.*test-automator" "$QA_SKILL" 2>/dev/null || \
   grep -qE "documentation.*skip.*test-automator|type.*documentation.*no.*test-automator" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Documentation stories skip test-automator"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing rule: documentation stories should skip test-automator"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 2.2: Documentation story type skips security-auditor"
if grep -qE "documentation.*skip.*security-auditor|type.*documentation.*no.*security" "$QA_SKILL" 2>/dev/null || \
   grep -qE "documentation.*skip.*security-auditor|type.*documentation.*no.*security" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Documentation stories skip security-auditor"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing rule: documentation stories should skip security-auditor"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 2.3: Documentation stories only run code-reviewer"
if grep -qE "documentation.*only.*code-reviewer|documentation.*:.*code-reviewer" "$QA_SKILL" 2>/dev/null || \
   grep -qE "documentation.*only.*code-reviewer|documentation.*:.*code-reviewer" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Documentation stories run only code-reviewer"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing rule: documentation stories should run only code-reviewer"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# -----------------------------------------------------------------------------
# AC-3: Refactor Stories Skip Test-Automator
# -----------------------------------------------------------------------------
echo ""
echo "--- AC-3: Refactor Stories Skip Test-Automator ---"
echo ""

echo "Test 3.1: Refactor story type skips test-automator"
if grep -qE "refactor.*skip.*test-automator|type.*refactor.*no.*test-automator" "$QA_SKILL" 2>/dev/null || \
   grep -qE "refactor.*skip.*test-automator|type.*refactor.*no.*test-automator" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Refactor stories skip test-automator"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing rule: refactor stories should skip test-automator (tests already exist)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 3.2: Refactor stories include code-reviewer"
if grep -qE "refactor.*code-reviewer|refactor.*:.*code-reviewer" "$QA_SKILL" 2>/dev/null || \
   grep -qE "refactor.*code-reviewer|refactor.*:.*code-reviewer" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Refactor stories include code-reviewer"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing: refactor stories should include code-reviewer"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 3.3: Refactor stories include security-auditor"
if grep -qE "refactor.*security-auditor|refactor.*:.*security" "$QA_SKILL" 2>/dev/null || \
   grep -qE "refactor.*security-auditor|refactor.*:.*security" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Refactor stories include security-auditor"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing: refactor stories should include security-auditor"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# -----------------------------------------------------------------------------
# AC-4: Feature/Bugfix Use All Validators
# -----------------------------------------------------------------------------
echo ""
echo "--- AC-4: Feature/Bugfix Use All Validators ---"
echo ""

echo "Test 4.1: Feature stories run all 3 validators"
if grep -qE "feature.*all.*validator|feature.*:.*test-automator.*code-reviewer.*security|type.*feature.*full" "$QA_SKILL" 2>/dev/null || \
   grep -qE "feature.*all.*validator|feature.*:.*test-automator.*code-reviewer.*security|type.*feature.*full" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Feature stories run all validators"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing rule: feature stories should run all 3 validators"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 4.2: Bugfix stories run all 3 validators"
if grep -qE "bugfix.*all.*validator|bugfix.*:.*test-automator.*code-reviewer.*security|type.*bugfix.*full" "$QA_SKILL" 2>/dev/null || \
   grep -qE "bugfix.*all.*validator|bugfix.*:.*test-automator.*code-reviewer.*security|type.*bugfix.*full" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Bugfix stories run all validators"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing rule: bugfix stories should run all 3 validators"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# -----------------------------------------------------------------------------
# AC-5: Success Threshold Adjusted
# -----------------------------------------------------------------------------
echo ""
echo "--- AC-5: Success Threshold Adjusted ---"
echo ""

echo "Test 5.1: Validator mapping table exists"
if grep -qE "validator.*mapping|story.*type.*validator|type.*->.*validator" "$QA_SKILL" 2>/dev/null || \
   grep -qE "validator.*mapping|story.*type.*validator|type.*->.*validator" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Validator mapping table exists"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing: validator mapping table by story type"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 5.2: Success threshold adjusts based on validator count"
if grep -qE "threshold.*adjust|success.*threshold.*validator.*count|validator.*count.*threshold" "$QA_SKILL" 2>/dev/null || \
   grep -qE "threshold.*adjust|success.*threshold.*validator.*count|validator.*count.*threshold" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Success threshold adjusts based on validator count"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing: success threshold adjustment based on validator count"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test 5.3: Threshold formula documented (e.g., validators_passed / validators_run)"
if grep -qE "validator.*passed.*run|threshold.*formula|pass.*ratio" "$QA_SKILL" 2>/dev/null || \
   grep -qE "validator.*passed.*run|threshold.*formula|pass.*ratio" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Threshold formula documented"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing: threshold formula documentation"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# -----------------------------------------------------------------------------
# Edge Cases
# -----------------------------------------------------------------------------
echo ""
echo "--- Edge Cases ---"
echo ""

echo "Test E1: Unknown story type defaults to full validation"
if grep -qE "unknown.*type.*full|default.*all.*validator|fallback.*full" "$QA_SKILL" 2>/dev/null || \
   grep -qE "unknown.*type.*full|default.*all.*validator|fallback.*full" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Unknown story type defaults to full validation"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing: unknown story type should default to full validation"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo ""
echo "Test E2: Missing story type field defaults to full validation"
if grep -qE "missing.*type.*full|no.*type.*default|type.*field.*missing" "$QA_SKILL" 2>/dev/null || \
   grep -qE "missing.*type.*full|no.*type.*default|type.*field.*missing" "$PARALLEL_REF" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC} Missing type field defaults to full validation"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing: stories without type field should default to full validation"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "========================================================================"
echo "Test Summary"
echo "========================================================================"
echo "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}$TESTS_FAILED test(s) failed - TDD Red phase active${NC}"
    exit 1
fi
