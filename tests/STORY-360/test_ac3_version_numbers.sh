#!/usr/bin/env bash
# =============================================================================
# STORY-360 AC#3: Version Numbers Updated in Modified Files Only
# =============================================================================
# Validates that:
#   - source-tree.md shows version >= 3.6 (incremented from 3.5)
#   - anti-patterns.md shows version >= 1.1 (incremented from 1.0)
#   - 4 unmodified files retain their original versions:
#     * tech-stack.md = v1.4
#     * dependencies.md = v1.1
#     * coding-standards.md = v1.2
#     * architecture-constraints.md = v1.0
#
# TDD Phase: RED - These tests define expected version constraints.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"

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

# Extract version number from a context file's first 10 lines
# Usage: extract_version "filename.md"
# Returns: version string like "3.7" or "1.0"
extract_version() {
    local filepath="${CONTEXT_DIR}/$1"
    local version_line
    version_line=$(head -n 10 "$filepath" 2>/dev/null | grep -E '^\*\*Version\*\*:' || echo "")

    if [[ -z "$version_line" ]]; then
        echo "NOT_FOUND"
        return
    fi

    # Extract version number (major.minor) from the Version line
    # Matches patterns like: **Version**: 3.7 or **Version**: 1.4 (Added: ...)
    local version
    version=$(echo "$version_line" | grep -oE '[0-9]+\.[0-9]+' | head -1)

    if [[ -z "$version" ]]; then
        echo "PARSE_ERROR"
    else
        echo "$version"
    fi
}

# Compare versions: returns 0 if $1 >= $2
version_gte() {
    local v1_major v1_minor v2_major v2_minor
    v1_major=$(echo "$1" | cut -d. -f1)
    v1_minor=$(echo "$1" | cut -d. -f2)
    v2_major=$(echo "$2" | cut -d. -f1)
    v2_minor=$(echo "$2" | cut -d. -f2)

    if [[ "$v1_major" -gt "$v2_major" ]]; then
        return 0
    elif [[ "$v1_major" -eq "$v2_major" && "$v1_minor" -ge "$v2_minor" ]]; then
        return 0
    else
        return 1
    fi
}

echo "=============================================="
echo "  AC#3: Version Numbers - Modified & Unmodified Files"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: source-tree.md version >= 3.6 (modified by STORY-357/358)
# -----------------------------------------------------------------------------
echo "--- Test 1: source-tree.md Version >= 3.6 ---"
st_version=$(extract_version "source-tree.md")
echo "  Detected version: ${st_version}"

if [[ "$st_version" == "NOT_FOUND" || "$st_version" == "PARSE_ERROR" ]]; then
    fail "source-tree.md version could not be extracted"
elif version_gte "$st_version" "3.6"; then
    pass "source-tree.md version ${st_version} >= 3.6"
else
    fail "source-tree.md version ${st_version} < 3.6 (expected >= 3.6 after STORY-357/358)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: anti-patterns.md version >= 1.1 (modified by STORY-359)
# -----------------------------------------------------------------------------
echo "--- Test 2: anti-patterns.md Version >= 1.1 ---"
ap_version=$(extract_version "anti-patterns.md")
echo "  Detected version: ${ap_version}"

if [[ "$ap_version" == "NOT_FOUND" || "$ap_version" == "PARSE_ERROR" ]]; then
    fail "anti-patterns.md version could not be extracted"
elif version_gte "$ap_version" "1.1"; then
    pass "anti-patterns.md version ${ap_version} >= 1.1"
else
    fail "anti-patterns.md version ${ap_version} < 1.1 (expected >= 1.1 after STORY-359)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: tech-stack.md retains version 1.4 (unmodified by EPIC-056)
# -----------------------------------------------------------------------------
echo "--- Test 3: tech-stack.md Version == 1.4 (Unchanged) ---"
ts_version=$(extract_version "tech-stack.md")
echo "  Detected version: ${ts_version}"

if [[ "$ts_version" == "1.4" ]]; then
    pass "tech-stack.md version is 1.4 (unchanged)"
else
    fail "tech-stack.md version is ${ts_version}, expected 1.4 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: dependencies.md retains version 1.1 (unmodified by EPIC-056)
# -----------------------------------------------------------------------------
echo "--- Test 4: dependencies.md Version == 1.1 (Unchanged) ---"
dep_version=$(extract_version "dependencies.md")
echo "  Detected version: ${dep_version}"

if [[ "$dep_version" == "1.1" ]]; then
    pass "dependencies.md version is 1.1 (unchanged)"
else
    fail "dependencies.md version is ${dep_version}, expected 1.1 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: coding-standards.md retains version 1.2 (unmodified by EPIC-056)
# -----------------------------------------------------------------------------
echo "--- Test 5: coding-standards.md Version == 1.2 (Unchanged) ---"
cs_version=$(extract_version "coding-standards.md")
echo "  Detected version: ${cs_version}"

if [[ "$cs_version" == "1.2" ]]; then
    pass "coding-standards.md version is 1.2 (unchanged)"
else
    fail "coding-standards.md version is ${cs_version}, expected 1.2 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: architecture-constraints.md retains version 1.0 (unmodified by EPIC-056)
# -----------------------------------------------------------------------------
echo "--- Test 6: architecture-constraints.md Version == 1.0 (Unchanged) ---"
ac_version=$(extract_version "architecture-constraints.md")
echo "  Detected version: ${ac_version}"

if [[ "$ac_version" == "1.0" ]]; then
    pass "architecture-constraints.md version is 1.0 (unchanged)"
else
    fail "architecture-constraints.md version is ${ac_version}, expected 1.0 (should be unchanged by EPIC-056)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Modified files have HIGHER versions than unmodified baseline
# source-tree was 3.5 before EPIC-056, anti-patterns was 1.0
# -----------------------------------------------------------------------------
echo "--- Test 7: Modified Files Incremented From Baseline ---"
if [[ "$st_version" != "NOT_FOUND" && "$st_version" != "PARSE_ERROR" ]]; then
    if version_gte "$st_version" "3.6"; then
        pass "source-tree.md incremented from baseline 3.5 to ${st_version}"
    else
        fail "source-tree.md not incremented from baseline 3.5 (current: ${st_version})"
    fi
else
    fail "source-tree.md version not parseable for baseline comparison"
fi

if [[ "$ap_version" != "NOT_FOUND" && "$ap_version" != "PARSE_ERROR" ]]; then
    if version_gte "$ap_version" "1.1"; then
        pass "anti-patterns.md incremented from baseline 1.0 to ${ap_version}"
    else
        fail "anti-patterns.md not incremented from baseline 1.0 (current: ${ap_version})"
    fi
else
    fail "anti-patterns.md version not parseable for baseline comparison"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
