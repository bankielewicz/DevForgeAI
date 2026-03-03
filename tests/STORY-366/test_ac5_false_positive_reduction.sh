#!/usr/bin/env bash
# =============================================================================
# STORY-366 AC#5: False Positive Reduction via AST-Aware Search
# =============================================================================
# Validates that security-auditor.md documents:
#   1. False positive reduction rationale (why AST-aware is better)
#   2. AST vs text-based comparison (explains the difference)
#   3. Specific false positive categories eliminated:
#      - Comments containing security keywords
#      - String literals with security terms
#      - Variable names matching security patterns
#      - Import/require statements referencing security modules
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/security-auditor.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/security-auditor/references/treelint-security-patterns.md"

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

# Helper: search in target file AND reference file (if it exists)
search_files() {
    local pattern="$1"
    if grep -qiE "$pattern" "$TARGET_FILE" 2>/dev/null; then
        return 0
    fi
    if [[ -r "$REFERENCE_FILE" ]] && grep -qiE "$pattern" "$REFERENCE_FILE" 2>/dev/null; then
        return 0
    fi
    return 1
}

echo "=============================================="
echo "  AC#5: False Positive Reduction via AST-Aware Search"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "security-auditor.md exists and is readable"
else
    fail "security-auditor.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: False positive reduction rationale documented
# Must explain WHY AST-aware search reduces false positives
# -----------------------------------------------------------------------------
echo "--- Test 2: False Positive Reduction Rationale ---"
if search_files '(false.positiv|reduce.*false|eliminat.*false|AST.*filter|AST.*aware.*reduc)'; then
    pass "False positive reduction rationale documented"
else
    fail "Missing false positive reduction rationale (explain why AST-aware search reduces false positives)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: AST vs text-based comparison explained
# Must contrast AST-aware search with text-based Grep matching
# -----------------------------------------------------------------------------
echo "--- Test 3: AST vs Text-Based Comparison ---"
if search_files '(AST.*text|text.*AST|AST.*Grep|Grep.*AST|AST.*aware.*vs|pattern.*match.*vs.*AST|semantic.*vs.*text)'; then
    pass "AST vs text-based comparison explained"
else
    fail "Missing AST vs text-based comparison (explain how AST differs from Grep text matching)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Comments as false positive source
# Must mention that comments containing security keywords are eliminated
# -----------------------------------------------------------------------------
echo "--- Test 4: Comments False Positive Category ---"
if search_files '(comment.*security|comment.*keyword|comment.*false|false.*comment|comment.*match)'; then
    pass "Documents comments as false positive source"
else
    fail "Missing documentation of comments as false positive source (e.g., '# authenticate user' in a comment)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: String literals as false positive source
# Must mention that string literals with security terms are eliminated
# -----------------------------------------------------------------------------
echo "--- Test 5: String Literals False Positive Category ---"
if search_files '(string.*literal|literal.*string|string.*false|false.*string|log.*message|print.*statement)'; then
    pass "Documents string literals as false positive source"
else
    fail "Missing documentation of string literals as false positive source (e.g., 'password' in a log message)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Variable names as false positive source
# Must mention that variable names matching security patterns are eliminated
# -----------------------------------------------------------------------------
echo "--- Test 6: Variable Names False Positive Category ---"
if search_files '(variable.*name|variable.*match|variable.*false|false.*variable|identifier.*match)'; then
    pass "Documents variable names as false positive source"
else
    fail "Missing documentation of variable names as false positive source (e.g., variable named 'password_field')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Import/require statements as false positive source
# Must mention that import statements are eliminated from results
# -----------------------------------------------------------------------------
echo "--- Test 7: Import Statements False Positive Category ---"
if search_files '(import.*statement|require.*statement|import.*false|false.*import|import.*module)'; then
    pass "Documents import/require statements as false positive source"
else
    fail "Missing documentation of import/require statements as false positive source"
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
