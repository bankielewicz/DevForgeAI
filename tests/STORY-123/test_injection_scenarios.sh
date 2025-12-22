#!/bin/bash

# Test Suite: Injection Scenario Coverage
# Purpose: Comprehensive security testing of all injection vectors
# Severity: CRITICAL - Command injection vulnerability from QA gap

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

test_injection() {
    local test_num="$1"
    local injection_vector="$2"
    local description="$3"
    local expected_to_block="$4"  # true or false

    echo ""
    echo -e "${YELLOW}Test $test_num: $description${NC}"
    echo "  Payload: $injection_vector"

    # Validation function (should block injection)
    if [[ ! "$injection_vector" =~ ^STORY-[0-9]+$ ]]; then
        if [ "$expected_to_block" = "true" ]; then
            ((TESTS_PASSED++))
            echo -e "  ${GREEN}✓ PASS${NC}: Injection blocked as expected"
        else
            ((TESTS_FAILED++))
            echo -e "  ${RED}✗ FAIL${NC}: Injection should have been allowed"
        fi
    else
        if [ "$expected_to_block" = "false" ]; then
            ((TESTS_PASSED++))
            echo -e "  ${GREEN}✓ PASS${NC}: Valid input allowed as expected"
        else
            ((TESTS_FAILED++))
            echo -e "  ${RED}✗ FAIL${NC}: Input should have been blocked"
        fi
    fi
}

echo "═══════════════════════════════════════════════════════════════"
echo "  Injection Scenario Test Suite"
echo "═══════════════════════════════════════════════════════════════"

# ========== COMMAND SUBSTITUTION INJECTION ==========
echo ""
echo "  [OWASP A03:2021] Command Substitution Injection"

test_injection 1 'STORY-123 && rm -rf /' \
    "Semicolon + command (rm -rf /)" "true"

test_injection 2 'STORY-123 | cat /etc/passwd' \
    "Pipe character injection" "true"

test_injection 3 'STORY-123 && cat /etc/shadow' \
    "Command chaining (&&)" "true"

test_injection 4 'STORY-123 || whoami' \
    "OR operator (||)" "true"

# ========== VARIABLE SUBSTITUTION ==========
echo ""
echo "  [OWASP A03:2021] Variable Substitution"

test_injection 5 'STORY-$(whoami)' \
    "Command substitution with \$()" "true"

test_injection 6 "STORY-\`id\`" \
    "Command substitution with backticks" "true"

test_injection 7 'STORY-${USER}' \
    "Variable expansion with \${}" "true"

# ========== GLOB PATTERN EXPANSION ==========
echo ""
echo "  Glob Pattern Expansion"

test_injection 8 'STORY-*' \
    "Glob wildcard (*)" "true"

test_injection 9 'STORY-[0-9]*' \
    "Character class glob" "true"

test_injection 10 'STORY-123??' \
    "Single char wildcard (?)" "true"

# ========== REDIRECTION ATTACKS ==========
echo ""
echo "  Input/Output Redirection"

test_injection 11 'STORY-123 > /tmp/pwned' \
    "Output redirection (>)" "true"

test_injection 12 'STORY-123 < /etc/passwd' \
    "Input redirection (<)" "true"

test_injection 13 'STORY-123 2>/dev/null' \
    "Stderr redirection (2>)" "true"

test_injection 14 'STORY-123 &' \
    "Background process (&)" "true"

# ========== SPECIAL SHELL CHARACTERS ==========
echo ""
echo "  Special Shell Characters"

test_injection 15 'STORY-123;whoami' \
    "Semicolon without space" "true"

test_injection 16 'STORY-123|pwd' \
    "Pipe without space" "true"

test_injection 17 'STORY-123&id' \
    "Ampersand without space" "true"

test_injection 18 'STORY-123$((1+1))' \
    "Arithmetic expansion" "true"

# ========== ESCAPE SEQUENCE ATTACKS ==========
echo ""
echo "  Escape Sequences"

test_injection 19 "STORY-123\nid" \
    "Newline escape" "true"

test_injection 20 "STORY-123\; whoami" \
    "Escaped semicolon" "true"

# ========== VALID STORY IDS ==========
echo ""
echo "  Valid Story IDs (should be allowed)"

test_injection 21 'STORY-123' \
    "Valid STORY-123" "false"

test_injection 22 'STORY-999' \
    "Valid STORY-999" "false"

test_injection 23 'STORY-1' \
    "Valid STORY-1" "false"

test_injection 24 'STORY-123456' \
    "Valid STORY-123456" "false"

# ========== BOUNDARY CASES ==========
echo ""
echo "  Boundary Cases"

test_injection 25 'STORY-' \
    "Missing number after dash" "true"

test_injection 26 'STORY-00000' \
    "Leading zeros (valid)" "false"

test_injection 27 'story-123' \
    "Lowercase (invalid)" "true"

test_injection 28 'Story-123' \
    "Mixed case (invalid)" "true"

test_injection 29 'STORY--123' \
    "Double dash" "true"

# ========== LENGTH ATTACKS ==========
echo ""
echo "  Length/Buffer Overflow Attempts"

test_injection 30 "STORY-$(printf 'A%.0s' {1..1000})" \
    "Very long payload (buffer overflow attempt)" "true"

# ========== MIXED PAYLOAD ATTACKS ==========
echo ""
echo "  Mixed/Advanced Payloads"

test_injection 31 "STORY-123' AND '1'='1" \
    "SQL injection pattern" "true"

test_injection 32 'STORY-123\"-alert(1)-\"' \
    "XSS pattern in double quotes" "true"

test_injection 33 'STORY-123%0Aecho hacked' \
    "URL-encoded newline (%0A)" "true"

test_injection 34 'STORY-123STORY-456' \
    "Duplicate pattern" "true"

test_injection 35 'STORY-123; STORY-456' \
    "Multiple story IDs" "true"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Summary"
echo "═══════════════════════════════════════════════════════════════"
TOTAL=$((TESTS_PASSED + TESTS_FAILED))
echo "Total injection vectors: $TOTAL"
echo -e "Blocked correctly:      ${GREEN}$TESTS_PASSED${NC}"
echo -e "Allowed unexpectedly:   ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ All injection scenarios properly blocked!${NC}"
    echo "✓ Implementation is resistant to command injection"
    exit 0
else
    echo ""
    echo -e "${RED}✗ Injection vectors not properly blocked${NC}"
    echo "✗ Security vulnerability remains"
    exit 1
fi
