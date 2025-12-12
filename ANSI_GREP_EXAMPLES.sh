#!/bin/bash

# ============================================================================
# ANSI Grep Examples - Test All Four Solutions
# ============================================================================
# This script demonstrates how to properly grep for ANSI escape codes
# in bash. Run this to verify each approach works correctly.
# ============================================================================

echo "=========================================="
echo "ANSI Grep Pattern Examples"
echo "=========================================="
echo ""

# Define ANSI color codes (standard definition)
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

# Create test output with ANSI codes embedded
test_output="$(cat <<'EOF'
Deployment Status: ✓ Complete
  Service A: $(printf '\033[32m')RUNNING$(printf '\033[0m')
  Service B: $(printf '\033[33m')WARNING$(printf '\033[0m')
  Service C: $(printf '\033[31m')FAILED$(printf '\033[0m')
Coverage Report:
  Module 1: $(printf '\033[32m')95%$(printf '\033[0m') - PASS
  Module 2: $(printf '\033[33m')78%$(printf '\033[0m') - WARN
  Module 3: $(printf '\033[31m')45%$(printf '\033[0m') - FAIL
EOF
)"

# Actually create the output with real ANSI codes
test_output=$(cat <<EOF
Deployment Status: Complete
  Service A: $(printf '\033[32m')RUNNING$(printf '\033[0m')
  Service B: $(printf '\033[33m')WARNING$(printf '\033[0m')
  Service C: $(printf '\033[31m')FAILED$(printf '\033[0m')
Coverage Report:
  Module 1: $(printf '\033[32m')95%$(printf '\033[0m') - PASS
  Module 2: $(printf '\033[33m')78%$(printf '\033[0m') - WARN
  Module 3: $(printf '\033[31m')45%$(printf '\033[0m') - FAIL
EOF
)

echo "Test output (with ANSI colors):"
echo "$test_output"
echo ""
echo "=========================================="
echo ""

# ============================================================================
# SOLUTION 1: Use grep -F (RECOMMENDED)
# ============================================================================
echo "SOLUTION 1: grep -F (Fixed String)"
echo "  Command: grep -qF \"\${COLOR}\""
echo "  Pros: Simplest, fastest, no escaping"
echo "  Cons: No regex features"
echo ""

GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

test_count=0
pass_count=0

# Test 1.1: Find green color
test_count=$((test_count + 1))
if echo "$test_output" | grep -qF "${GREEN}"; then
    echo "  [PASS] Found green color with grep -qF"
    pass_count=$((pass_count + 1))
else
    echo "  [FAIL] Did not find green color with grep -qF"
fi

# Test 1.2: Find yellow color
test_count=$((test_count + 1))
if echo "$test_output" | grep -qF "${YELLOW}"; then
    echo "  [PASS] Found yellow color with grep -qF"
    pass_count=$((pass_count + 1))
else
    echo "  [FAIL] Did not find yellow color with grep -qF"
fi

# Test 1.3: Find red color
test_count=$((test_count + 1))
if echo "$test_output" | grep -qF "${RED}"; then
    echo "  [PASS] Found red color with grep -qF"
    pass_count=$((pass_count + 1))
else
    echo "  [FAIL] Did not find red color with grep -qF"
fi

# Test 1.4: Find reset code
test_count=$((test_count + 1))
if echo "$test_output" | grep -qF "${RESET}"; then
    echo "  [PASS] Found reset code with grep -qF"
    pass_count=$((pass_count + 1))
else
    echo "  [FAIL] Did not find reset code with grep -qF"
fi

echo "  Result: $pass_count/$test_count passed"
echo ""

# ============================================================================
# SOLUTION 2: Escape the Bracket in Variable
# ============================================================================
echo "SOLUTION 2: Escaped Bracket Variable"
echo "  Define: GREEN='\\033\\[32m'"
echo "  Command: grep -q \"\${GREEN}\""
echo "  Pros: Flexible, works with regex"
echo "  Cons: Harder to read variable definitions"
echo ""

GREEN_ESC='\033\[32m'
YELLOW_ESC='\033\[33m'
RED_ESC='\033\[31m'
RESET_ESC='\033\[0m'

sol2_pass=0
sol2_total=0

# Test 2.1: Find green with escaped bracket
sol2_total=$((sol2_total + 1))
if echo "$test_output" | grep -q "${GREEN_ESC}"; then
    echo "  [PASS] Found green with escaped bracket grep -q"
    sol2_pass=$((sol2_pass + 1))
else
    echo "  [FAIL] Did not find green with escaped bracket"
fi

# Test 2.2: Find yellow with escaped bracket
sol2_total=$((sol2_total + 1))
if echo "$test_output" | grep -q "${YELLOW_ESC}"; then
    echo "  [PASS] Found yellow with escaped bracket grep -q"
    sol2_pass=$((sol2_pass + 1))
else
    echo "  [FAIL] Did not find yellow with escaped bracket"
fi

# Test 2.3: Find red with escaped bracket
sol2_total=$((sol2_total + 1))
if echo "$test_output" | grep -q "${RED_ESC}"; then
    echo "  [PASS] Found red with escaped bracket grep -q"
    sol2_pass=$((sol2_pass + 1))
else
    echo "  [FAIL] Did not find red with escaped bracket"
fi

echo "  Result: $sol2_pass/$sol2_total passed"
echo ""

# ============================================================================
# SOLUTION 3: Inline Escaped Pattern
# ============================================================================
echo "SOLUTION 3: Inline Escaped Pattern"
echo "  Command: grep -q '\\033\\[32m'"
echo "  Pros: Explicit, no variable needed"
echo "  Cons: Pattern duplicated in code"
echo ""

sol3_pass=0
sol3_total=0

# Test 3.1: Inline green pattern
sol3_total=$((sol3_total + 1))
if echo "$test_output" | grep -q '\033\[32m'; then
    echo "  [PASS] Found green with inline escaped pattern"
    sol3_pass=$((sol3_pass + 1))
else
    echo "  [FAIL] Did not find green with inline pattern"
fi

# Test 3.2: Inline yellow pattern
sol3_total=$((sol3_total + 1))
if echo "$test_output" | grep -q '\033\[33m'; then
    echo "  [PASS] Found yellow with inline escaped pattern"
    sol3_pass=$((sol3_pass + 1))
else
    echo "  [FAIL] Did not find yellow with inline pattern"
fi

# Test 3.3: Inline red pattern
sol3_total=$((sol3_total + 1))
if echo "$test_output" | grep -q '\033\[31m'; then
    echo "  [PASS] Found red with inline escaped pattern"
    sol3_pass=$((sol3_pass + 1))
else
    echo "  [FAIL] Did not find red with inline pattern"
fi

echo "  Result: $sol3_pass/$sol3_total passed"
echo ""

# ============================================================================
# SOLUTION 4: Extended Regex with Escaped Bracket
# ============================================================================
echo "SOLUTION 4: Extended Regex (-E) with Escaped Bracket"
echo "  Define: GREEN_PAT='\\033\\[32m'"
echo "  Command: grep -qE \"\${GREEN_PAT}\""
echo "  Pros: Supports regex features, alternation"
echo "  Cons: Slower, more complex"
echo ""

GREEN_PATTERN='\033\[32m'
YELLOW_PATTERN='\033\[33m'
RED_PATTERN='\033\[31m'

sol4_pass=0
sol4_total=0

# Test 4.1: Extended regex with escaped bracket - green
sol4_total=$((sol4_total + 1))
if echo "$test_output" | grep -qE "${GREEN_PATTERN}"; then
    echo "  [PASS] Found green with grep -qE"
    sol4_pass=$((sol4_pass + 1))
else
    echo "  [FAIL] Did not find green with grep -qE"
fi

# Test 4.2: Extended regex - alternation (multiple colors)
sol4_total=$((sol4_total + 1))
if echo "$test_output" | grep -qE "(${GREEN_PATTERN}|${YELLOW_PATTERN}|${RED_PATTERN})"; then
    echo "  [PASS] Found any color using alternation with grep -qE"
    sol4_pass=$((sol4_pass + 1))
else
    echo "  [FAIL] Did not find colors with alternation"
fi

# Test 4.3: Extended regex - complex pattern
sol4_total=$((sol4_total + 1))
if echo "$test_output" | grep -qE "WARN.*${YELLOW_PATTERN}"; then
    echo "  [PASS] Found complex pattern (WARN + yellow) with grep -qE"
    sol4_pass=$((sol4_pass + 1))
else
    echo "  [FAIL] Did not find complex pattern"
fi

echo "  Result: $sol4_pass/$sol4_total passed"
echo ""

# ============================================================================
# COMPARISON & SUMMARY
# ============================================================================
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo ""
echo "Solution 1 (grep -F):           $pass_count/$test_count passed"
echo "Solution 2 (Escaped bracket):   $sol2_pass/$sol2_total passed"
echo "Solution 3 (Inline escape):     $sol3_pass/$sol3_total passed"
echo "Solution 4 (Extended regex):    $sol4_pass/$sol4_total passed"
echo ""

total_tests=$((test_count + sol2_total + sol3_total + sol4_total))
total_passed=$((pass_count + sol2_pass + sol3_pass + sol4_pass))

echo "OVERALL: $total_passed/$total_tests tests passed"
echo ""

if [ "$total_passed" -eq "$total_tests" ]; then
    echo "Result: ALL TESTS PASSED ✓"
    echo ""
    echo "Recommendation: Use Solution 1 (grep -F)"
    echo "  - Simplest: Just add -F flag"
    echo "  - Fastest: No regex parsing"
    echo "  - Safest: No special character interpretation"
    exit 0
else
    echo "Result: SOME TESTS FAILED ✗"
    exit 1
fi
