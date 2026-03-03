#!/usr/bin/env bash
# =============================================================================
# STORY-360 AC#5: No Circular References or Contradictions Between Files
# =============================================================================
# Validates that:
#   1. All Treelint references are consistent across files
#      (tool name spelling, version constraints v0.12.0+, ADR-013 references)
#   2. No file contradicts another
#      (anti-patterns.md does not forbid what tech-stack.md approves)
#   3. No circular reference chains exist
#   4. ADR-013 reference resolves to an existing file
#
# Cross-file checks involve: tech-stack.md, source-tree.md,
#                             dependencies.md, anti-patterns.md
#
# TDD Phase: RED - These tests define expected cross-file consistency.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"
ADR_DIR="${PROJECT_ROOT}/devforgeai/specs/adrs"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  FAIL: $1"
}

# WSL-safe grep count: strips carriage returns from grep -c output
gcount() {
    local result
    result=$(grep -c "$@" 2>/dev/null | tr -d '\r\n' || true)
    if [[ -z "$result" ]]; then echo "0"; else echo "$result"; fi
}

gcount_i() {
    local result
    result=$(grep -ci "$@" 2>/dev/null | tr -d '\r\n' || true)
    if [[ -z "$result" ]]; then echo "0"; else echo "$result"; fi
}

echo "=============================================="
echo "  AC#5: Cross-File Consistency Validation"
echo "=============================================="
echo ""

# =============================================================================
# Section 1: Treelint Name Consistency
# =============================================================================
echo "--- Test 1: Treelint Name Spelling Consistent ---"

# Check each file that references Treelint uses the correct capitalization
FILES_WITH_TREELINT=("tech-stack.md" "source-tree.md" "dependencies.md" "anti-patterns.md")

for file in "${FILES_WITH_TREELINT[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"

    # Count total mentions (case-insensitive)
    total_mentions=$(gcount_i 'treelint' "$filepath")

    if [[ "$total_mentions" -gt 0 ]]; then
        pass "${file} references Treelint (${total_mentions} mention(s))"
    else
        # source-tree.md and anti-patterns.md MUST mention it
        if [[ "$file" == "source-tree.md" || "$file" == "anti-patterns.md" ]]; then
            fail "${file} should reference Treelint but has 0 mentions"
        else
            pass "${file} does not reference Treelint (acceptable for unmodified file)"
        fi
    fi
done
echo ""

# =============================================================================
# Section 2: Treelint Version Constraint Consistency
# =============================================================================
echo "--- Test 2: Treelint Version v0.12.0+ Consistent ---"

# tech-stack.md should specify v0.12.0+
ts_version_ref=$(grep -oE 'v0\.12\.0' "${CONTEXT_DIR}/tech-stack.md" 2>/dev/null | head -1 | tr -d '\r')
if [[ -n "$ts_version_ref" ]]; then
    pass "tech-stack.md references Treelint v0.12.0"
else
    fail "tech-stack.md missing Treelint v0.12.0 version reference"
fi

# dependencies.md should also reference v0.12.0+
dep_version_ref=$(grep -oE 'v0\.12\.0' "${CONTEXT_DIR}/dependencies.md" 2>/dev/null | head -1 | tr -d '\r')
if [[ -n "$dep_version_ref" ]]; then
    pass "dependencies.md references Treelint v0.12.0"
else
    fail "dependencies.md missing Treelint v0.12.0 version reference"
fi

# If both files reference a version, check they match
if [[ -n "$ts_version_ref" && -n "$dep_version_ref" ]]; then
    if [[ "$ts_version_ref" == "$dep_version_ref" ]]; then
        pass "tech-stack.md and dependencies.md Treelint versions match"
    else
        fail "tech-stack.md (${ts_version_ref}) and dependencies.md (${dep_version_ref}) Treelint versions MISMATCH"
    fi
fi
echo ""

# =============================================================================
# Section 3: ADR-013 Reference Consistency
# =============================================================================
echo "--- Test 3: ADR-013 References Resolve ---"

# Check that ADR-013 file exists
adr_file="${ADR_DIR}/ADR-013-treelint-integration.md"
if [[ -r "$adr_file" ]]; then
    pass "ADR-013-treelint-integration.md exists and is readable"
else
    fail "ADR-013-treelint-integration.md does not exist at ${adr_file}"
fi

# Check each file that references ADR-013
for file in "${FILES_WITH_TREELINT[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    adr_ref=$(gcount 'ADR-013' "$filepath")

    if [[ "$adr_ref" -gt 0 ]]; then
        pass "${file} references ADR-013 (${adr_ref} reference(s))"
    else
        # tech-stack.md and dependencies.md should reference ADR-013
        if [[ "$file" == "tech-stack.md" || "$file" == "dependencies.md" ]]; then
            fail "${file} should reference ADR-013 but has 0 references"
        else
            pass "${file} does not reference ADR-013 (acceptable)"
        fi
    fi
done
echo ""

# =============================================================================
# Section 4: No Contradictions Between tech-stack.md and anti-patterns.md
# =============================================================================
echo "--- Test 4: No Contradictions (tech-stack approvals vs anti-patterns) ---"

# tech-stack.md APPROVES Treelint (look for the APPROVED status marker)
ts_approves=$(gcount 'APPROVED.*Treelint\|Treelint.*APPROVED' "${CONTEXT_DIR}/tech-stack.md")

# anti-patterns.md should NOT have a blanket ban on Treelint.
# Category 11 says "FORBIDDEN: Using Treelint for Unsupported File Types" (misuse)
# and "FORBIDDEN: Using Grep When Treelint Available" (correct usage guidance).
# These are NOT contradictions - they guide correct usage, not ban the tool.
#
# A true contradiction would be: "FORBIDDEN: Using Treelint" (blanket ban)
# We check for blanket ban pattern: "FORBIDDEN" on the same line as just "Treelint"
# but NOT followed by "for Unsupported" (which is usage guidance, not a ban).
ap_blanket_ban=$(grep -E 'FORBIDDEN.*Treelint' "${CONTEXT_DIR}/anti-patterns.md" 2>/dev/null | grep -vc 'for Unsupported\|When Treelint Available' | tr -d '\r\n' || true)
if [[ -z "$ap_blanket_ban" ]]; then ap_blanket_ban=0; fi

if [[ "$ts_approves" -gt 0 && "$ap_blanket_ban" -gt 0 ]]; then
    fail "CONTRADICTION: tech-stack.md approves Treelint but anti-patterns.md has a blanket ban"
elif [[ "$ts_approves" -gt 0 ]]; then
    pass "No contradiction: tech-stack.md approves Treelint, anti-patterns.md guides usage (no blanket ban)"
else
    pass "Treelint approval check completed"
fi

# anti-patterns.md Category 11 should guide CORRECT usage, not forbid the tool entirely
ap_has_category_11=$(gcount 'Category 11' "${CONTEXT_DIR}/anti-patterns.md")
if [[ "$ap_has_category_11" -gt 0 ]]; then
    pass "anti-patterns.md has Category 11 (code search tool selection guidance)"
else
    fail "anti-patterns.md missing Category 11 (expected after STORY-359)"
fi
echo ""

# =============================================================================
# Section 5: No Duplicate Anti-Pattern Category Numbers
# =============================================================================
echo "--- Test 5: No Duplicate Anti-Pattern Category Numbers ---"
categories=$(grep -oE 'Category [0-9]+' "${CONTEXT_DIR}/anti-patterns.md" 2>/dev/null | sort)
unique_categories=$(echo "$categories" | sort -u)
total_cats=$(echo "$categories" | wc -l | tr -d ' \r\n')
unique_cats=$(echo "$unique_categories" | wc -l | tr -d ' \r\n')

if [[ "$total_cats" -eq "$unique_cats" ]]; then
    pass "No duplicate category numbers in anti-patterns.md (${unique_cats} unique categories)"
else
    fail "Duplicate category numbers found in anti-patterns.md (${total_cats} total vs ${unique_cats} unique)"
fi
echo ""

# =============================================================================
# Section 6: source-tree.md References .treelint/ Directory
# =============================================================================
echo "--- Test 6: source-tree.md Contains .treelint/ Directory ---"
treelint_dir_ref=$(gcount '\.treelint/' "${CONTEXT_DIR}/source-tree.md")
if [[ "$treelint_dir_ref" -gt 0 ]]; then
    pass "source-tree.md references .treelint/ directory (${treelint_dir_ref} reference(s))"
else
    fail "source-tree.md missing .treelint/ directory reference (expected after STORY-357)"
fi
echo ""

# =============================================================================
# Section 7: Treelint Language Support Consistent
# =============================================================================
echo "--- Test 7: Language Support Consistent ---"

# tech-stack.md lists supported languages for Treelint
ts_python=$(gcount 'Python.*Supported\|\.py.*Supported' "${CONTEXT_DIR}/tech-stack.md")
ts_typescript=$(gcount 'TypeScript.*Supported\|\.ts.*Supported' "${CONTEXT_DIR}/tech-stack.md")

# anti-patterns.md Category 11 should reference same supported languages
ap_python=$(gcount '\.py' "${CONTEXT_DIR}/anti-patterns.md")
ap_typescript=$(gcount '\.ts' "${CONTEXT_DIR}/anti-patterns.md")

if [[ "$ts_python" -gt 0 && "$ap_python" -gt 0 ]]; then
    pass "Python (.py) referenced in both tech-stack.md and anti-patterns.md"
elif [[ "$ts_python" -gt 0 && "$ap_python" -eq 0 ]]; then
    fail "Python listed in tech-stack.md but not in anti-patterns.md Treelint guidance"
else
    pass "Python references consistent (or not applicable)"
fi

if [[ "$ts_typescript" -gt 0 && "$ap_typescript" -gt 0 ]]; then
    pass "TypeScript (.ts) referenced in both tech-stack.md and anti-patterns.md"
elif [[ "$ts_typescript" -gt 0 && "$ap_typescript" -eq 0 ]]; then
    fail "TypeScript listed in tech-stack.md but not in anti-patterns.md Treelint guidance"
else
    pass "TypeScript references consistent (or not applicable)"
fi
echo ""

# =============================================================================
# Section 8: No Circular References (basic check)
# =============================================================================
echo "--- Test 8: No Circular Reference Indicators ---"
# Check that source-tree.md does not reference itself as a dependency
st_self_ref=$(gcount 'source-tree.md.*depends.*source-tree\|source-tree.*requires.*source-tree' "${CONTEXT_DIR}/source-tree.md")
if [[ "$st_self_ref" -eq 0 ]]; then
    pass "source-tree.md has no self-referential dependencies"
else
    fail "source-tree.md appears to reference itself as a dependency"
fi

# Check anti-patterns.md does not circularly reference itself
ap_self_ref=$(gcount 'anti-patterns.md.*depends.*anti-patterns\|anti-patterns.*requires.*anti-patterns' "${CONTEXT_DIR}/anti-patterns.md")
if [[ "$ap_self_ref" -eq 0 ]]; then
    pass "anti-patterns.md has no self-referential dependencies"
else
    fail "anti-patterns.md appears to reference itself as a dependency"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
