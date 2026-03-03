#!/usr/bin/env bash
# =============================================================================
# STORY-366 AC#4: Security-Sensitive Function Pattern Documentation
# =============================================================================
# Validates that security-auditor.md documents Treelint search patterns for
# at least 5 security categories:
#   1. Authentication functions (authenticate*, login*, verify_password*)
#   2. Cryptography functions (encrypt*, decrypt*, hash*)
#   3. Input validation functions (validate*, sanitize*, escape*)
#   4. Authorization functions (authorize*, check_permission*)
#   5. Data access functions (query*, execute*, raw_sql*)
#
# Each category must have a Treelint command example.
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/security-auditor.md"
# Also check reference file if it exists (progressive disclosure)
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
echo "  AC#4: Security-Sensitive Function Pattern Documentation"
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
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
if [[ -r "$REFERENCE_FILE" ]]; then
    echo "  Info: Reference file found at treelint-security-patterns.md (will also search)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Authentication patterns documented
# Must contain authenticate*, login*, or verify_password*
# -----------------------------------------------------------------------------
echo "--- Test 2: Authentication Patterns ---"
if search_files '(authenticate|login|verify_password)'; then
    pass "Authentication patterns documented (authenticate*, login*, verify_password*)"
else
    fail "Missing authentication function patterns (expected: authenticate*, login*, verify_password*)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Cryptography patterns documented
# Must contain encrypt*, decrypt*, or hash*
# -----------------------------------------------------------------------------
echo "--- Test 3: Cryptography Patterns ---"
if search_files '(encrypt|decrypt|hash)'; then
    pass "Cryptography patterns documented (encrypt*, decrypt*, hash*)"
else
    fail "Missing cryptography function patterns (expected: encrypt*, decrypt*, hash*)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Input validation patterns documented
# Must contain validate*, sanitize*, or escape*
# -----------------------------------------------------------------------------
echo "--- Test 4: Input Validation Patterns ---"
if search_files '(validate|sanitize|escape)'; then
    pass "Input validation patterns documented (validate*, sanitize*, escape*)"
else
    fail "Missing input validation function patterns (expected: validate*, sanitize*, escape*)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Authorization patterns documented
# Must contain authorize*, check_permission*, or is_admin*
# -----------------------------------------------------------------------------
echo "--- Test 5: Authorization Patterns ---"
if search_files '(authorize|check_permission|is_admin)'; then
    pass "Authorization patterns documented (authorize*, check_permission*, is_admin*)"
else
    fail "Missing authorization function patterns (expected: authorize*, check_permission*, is_admin*)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Data access patterns documented
# Must contain query*, execute*, or raw_sql*
# -----------------------------------------------------------------------------
echo "--- Test 6: Data Access Patterns ---"
if search_files '(query|execute|raw_sql)'; then
    pass "Data access patterns documented (query*, execute*, raw_sql*)"
else
    fail "Missing data access function patterns (expected: query*, execute*, raw_sql*)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: At least 5 distinct security categories present
# Count how many of the 5 categories are documented
# -----------------------------------------------------------------------------
echo "--- Test 7: Minimum 5 Security Categories (BR-005) ---"
categories_found=0

if search_files '(authenticate|login|verify_password)'; then
    categories_found=$((categories_found + 1))
fi
if search_files '(encrypt|decrypt|hash\*)'; then
    categories_found=$((categories_found + 1))
fi
if search_files '(validate|sanitize|escape)'; then
    categories_found=$((categories_found + 1))
fi
if search_files '(authorize|check_permission|is_admin)'; then
    categories_found=$((categories_found + 1))
fi
if search_files '(query\*|execute\*|raw_sql)'; then
    categories_found=$((categories_found + 1))
fi

if [[ "$categories_found" -ge 5 ]]; then
    pass "All 5 security categories documented (${categories_found}/5)"
else
    fail "Only ${categories_found}/5 security categories documented (need all 5: auth, crypto, validation, authz, data access)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Treelint command examples for security patterns
# Must contain at least one treelint search command with security function name
# -----------------------------------------------------------------------------
echo "--- Test 8: Treelint Command Examples for Patterns ---"
if search_files 'treelint search.*--name.*(authenticate|encrypt|validate|authorize|query)'; then
    pass "Contains Treelint command examples with security function patterns"
else
    fail "Missing Treelint command examples for security patterns (e.g., treelint search --name 'authenticate*')"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
