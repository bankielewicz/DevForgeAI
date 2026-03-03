#!/usr/bin/env bash
# =============================================================================
# STORY-407 AC#5: Content-Only Output Contract Preserved
# =============================================================================
# Validates that story-requirements-analyst.md STILL preserves:
#   1. Content-only output contract (no file creation)
#   2. All 4 required sections (User Story, AC, Edge Cases, NFRs)
#   3. No Write/Edit tools in allowed tools
#   4. Output format: content_only in frontmatter
#   5. Treelint validation does not add file creation behavior
#
# This is a regression test: adding Treelint validation MUST NOT break
# the existing content-only output contract (RCA-007 compliance).
#
# Target: src/claude/agents/story-requirements-analyst.md
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/story-requirements-analyst.md"

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

echo "=============================================="
echo "  AC#5: Content-Only Output Contract Preserved"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "story-requirements-analyst.md exists and is readable"
else
    fail "story-requirements-analyst.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Frontmatter contains output_format: content_only
# -----------------------------------------------------------------------------
echo "--- Test 2: Frontmatter output_format: content_only ---"
if grep -q 'output_format: content_only' "$TARGET_FILE"; then
    pass "Frontmatter contains output_format: content_only"
else
    fail "Missing frontmatter output_format: content_only"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Tools list excludes Write and Edit
# -----------------------------------------------------------------------------
echo "--- Test 3: Write/Edit Tools Excluded ---"
# Extract the tools line from frontmatter
tools_line=$(grep -E '^tools:' "$TARGET_FILE" || echo "")
if [[ -n "$tools_line" ]]; then
    if echo "$tools_line" | grep -qv 'Write' && echo "$tools_line" | grep -qv 'Edit'; then
        pass "Write and Edit tools not in allowed tools list"
    else
        fail "Write or Edit found in tools list (violates content-only contract)"
    fi
else
    fail "No tools line found in frontmatter"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Required section 'User Story' referenced
# -----------------------------------------------------------------------------
echo "--- Test 4: Required Section - User Story ---"
if grep -q '## User Story' "$TARGET_FILE"; then
    pass "Required section 'User Story' present"
else
    fail "Missing required section 'User Story'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Required section 'Acceptance Criteria' referenced
# -----------------------------------------------------------------------------
echo "--- Test 5: Required Section - Acceptance Criteria ---"
if grep -q '## Acceptance Criteria' "$TARGET_FILE"; then
    pass "Required section 'Acceptance Criteria' present"
else
    fail "Missing required section 'Acceptance Criteria'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Required section 'Edge Cases' referenced
# -----------------------------------------------------------------------------
echo "--- Test 6: Required Section - Edge Cases ---"
if grep -q '## Edge Cases' "$TARGET_FILE"; then
    pass "Required section 'Edge Cases' present"
else
    fail "Missing required section 'Edge Cases'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Required section 'Non-Functional Requirements' referenced
# -----------------------------------------------------------------------------
echo "--- Test 7: Required Section - Non-Functional Requirements ---"
if grep -q '## Non-Functional Requirements' "$TARGET_FILE"; then
    pass "Required section 'Non-Functional Requirements' present"
else
    fail "Missing required section 'Non-Functional Requirements'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Content-only contract statement preserved
# -----------------------------------------------------------------------------
echo "--- Test 8: Content-Only Contract Statement ---"
if grep -qiE '(content.only|CONTENT ONLY|content generator.*not.*document creator|returns.*ONLY.*markdown)' "$TARGET_FILE"; then
    pass "Content-only contract statement preserved"
else
    fail "Missing content-only contract statement"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 9: Contract reference preserved
# -----------------------------------------------------------------------------
echo "--- Test 9: Contract Reference ---"
if grep -q 'requirements-analyst-contract.yaml' "$TARGET_FILE"; then
    pass "Contract reference to requirements-analyst-contract.yaml preserved"
else
    fail "Missing contract reference to requirements-analyst-contract.yaml"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 10: Treelint validation does not introduce Write/Edit usage
# (Scan the new Treelint section specifically for prohibited tools)
# -----------------------------------------------------------------------------
echo "--- Test 10: Treelint Section Does Not Introduce File Creation ---"
# Check if there's a Treelint section that mentions Write or file creation
if grep -qiE 'treelint.*valid|treelint.*schema' "$TARGET_FILE" 2>/dev/null; then
    # Treelint section exists - verify it doesn't introduce Write/Edit
    # This is a heuristic: check if Write() appears near treelint context
    if grep -A 10 -iE 'treelint.*valid' "$TARGET_FILE" | grep -qiE 'Write\(|Edit\(|create.*file'; then
        fail "Treelint validation section introduces file creation (violates contract)"
    else
        pass "Treelint validation section does not introduce file creation"
    fi
else
    # No Treelint section yet (RED phase expected)
    fail "No Treelint validation section found (implementation not yet added)"
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
