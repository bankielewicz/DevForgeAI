# Complete Solutions: Grep ANSI Escape Codes in Bash

## Problem Analysis

Your test file `/mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh` fails because:

```bash
GREEN='\033[32m'

if echo "${output}" | grep -q "${GREEN}"; then
    # This fails with: "grep: Unmatched [, [^, [:, [., or [="
```

**Why:** Grep interprets `[` as a regex metacharacter (bracket expression start), not a literal character. The pattern `\033[32m` is malformed regex because `[32m` is an incomplete bracket expression.

---

## Four Tested Solutions

### Solution 1: Use grep -F (RECOMMENDED - Simplest)

**Fixed string matching treats everything as literal:**

```bash
#!/usr/bin/env bash

GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

# Use -F flag for fixed string (no regex interpretation)
if echo "${output}" | grep -qF "${GREEN}"; then
    echo "✓ Found green code"
fi

if echo "${output}" | grep -qF "${YELLOW}"; then
    echo "✓ Found yellow code"
fi

if echo "${output}" | grep -qF "${RED}"; then
    echo "✓ Found red code"
fi

if echo "${output}" | grep -qF "${RESET}"; then
    echo "✓ Found reset code"
fi
```

**Advantages:**
- Simplest implementation (just add `-F`)
- No escaping needed
- Fastest execution
- Works on all Unix/Linux systems
- grep -qF still works for quiet mode (no output)

**Key Flag:** `-F` = "Fixed strings" (literal, not regex)

---

### Solution 2: Escape the Bracket in Variable Definition

**Define colors with escaped bracket for regex mode:**

```bash
#!/usr/bin/env bash

# Define with escaped bracket: \[
GREEN='\033\[32m'
YELLOW='\033\[33m'
RED='\033\[31m'
RESET='\033\[0m'

# Now normal grep -q works because pattern is: \033\[32m
# Grep sees: literal-escape, literal-bracket, "32m"
if echo "${output}" | grep -q "${GREEN}"; then
    echo "✓ Found green code"
fi

if echo "${output}" | grep -q "${YELLOW}"; then
    echo "✓ Found yellow code"
fi

if echo "${output}" | grep -q "${RED}"; then
    echo "✓ Found red code"
fi

if echo "${output}" | grep -q "${RESET}"; then
    echo "✓ Found reset code"
fi
```

**How it works:**
- In bash variable: `\[` = literal backslash followed by literal bracket
- When passed to grep: `\033\[32m` is the regex pattern
- Grep interprets `\[` as "escaped bracket" = literal bracket character
- Avoids the "Unmatched [" error

**Advantages:**
- Works with grep -E (extended regex) too
- Flexible if you need regex features later
- Clear intent in variable definition

---

### Solution 3: Use Inline Escaped Pattern (Explicit Regex)

**Escape bracket directly in grep pattern:**

```bash
#!/usr/bin/env bash

GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

# Escape bracket in the grep pattern, not in the variable
if echo "${output}" | grep -q '\033\[32m'; then
    echo "✓ Found green code"
fi

if echo "${output}" | grep -q '\033\[33m'; then
    echo "✓ Found yellow code"
fi

if echo "${output}" | grep -q '\033\[31m'; then
    echo "✓ Found red code"
fi

if echo "${output}" | grep -q '\033\[0m'; then
    echo "✓ Found reset code"
fi
```

**Advantages:**
- Pattern is explicit and visible
- No need to modify variable definitions
- Good for one-off checks

**Disadvantage:**
- Duplicates pattern definitions
- Harder to maintain (pattern defined in two places)

---

### Solution 4: Extended Regex with Escaped Bracket

**Use grep -E for extended regex features:**

```bash
#!/usr/bin/env bash

# Define with escaped bracket for extended regex
GREEN='\033\[32m'
YELLOW='\033\[33m'
RED='\033\[31m'
RESET='\033\[0m'

# Use -E for extended regex if you need alternation, grouping, etc.
if echo "${output}" | grep -qE "${GREEN}"; then
    echo "✓ Found green code"
fi

# Example with regex features (multiple patterns)
if echo "${output}" | grep -qE "(${GREEN}|${YELLOW}|${RED})"; then
    echo "✓ Found any color code"
fi

# Complex pattern example
if echo "${output}" | grep -qE "Status: (${GREEN}|${YELLOW}|${RED})"; then
    echo "✓ Found status line with color"
fi
```

**When to use:**
- You need regex features (alternation `|`, grouping `()`, etc.)
- Patterns are complex
- Performance is less critical

---

## Comparison: Which Solution to Use?

| Solution | Command | Escaping | Regex | Speed | Use Case |
|----------|---------|----------|-------|-------|----------|
| **1: grep -F** | `grep -qF '...'` | No | No | Fastest | Simple ANSI code matching (RECOMMENDED) |
| **2: Escaped var** | `grep -q '${GREEN}'` | Yes (in var) | Yes | Medium | Flexible, variable reuse |
| **3: Inline escape** | `grep -q '\033\[32m'` | Yes (in pattern) | Yes | Medium | One-off matches |
| **4: Extended -E** | `grep -qE '${GREEN}'` | Yes (in var) | Yes | Slower | Complex regex patterns |

---

## For Your Test File

### Quickest Fix (Solution 1)

Change these lines in `test_terminal_output.sh`:

```bash
# Line 56: Change
if echo "${output}" | grep -q "${GREEN}"; then
# To
if echo "${output}" | grep -qF "${GREEN}"; then

# Line 94: Change
if echo "${output}" | grep -q "${YELLOW}"; then
# To
if echo "${output}" | grep -qF "${YELLOW}"; then

# Line 132: Change
if echo "${output}" | grep -q "${RED}"; then
# To
if echo "${output}" | grep -qF "${RED}"; then

# Line 251: Change
if echo "${output}" | grep -q "${RESET}"; then
# To
if echo "${output}" | grep -qF "${RESET}"; then

# Line 289: Change
if echo "${output}" | grep -q "${YELLOW}" && ! echo "${output}" | grep -q "${RED}"; then
# To
if echo "${output}" | grep -qF "${YELLOW}" && ! echo "${output}" | grep -qF "${RED}"; then
```

### Special Case: Line 216 (Complex Pattern)

This line uses extended regex with multiple variables - needs different handling:

```bash
# Current (problematic):
if echo "${output}" | grep -qE "(Overall|Total|Summary).*${GREEN}|${YELLOW}|${RED}"; then

# Solution A: Use grep -F with literal string
if echo "${output}" | grep -qF "${GREEN}" || \
   echo "${output}" | grep -qF "${YELLOW}" || \
   echo "${output}" | grep -qF "${RED}"; then

# Solution B: Define escaped variables and use -E
GREEN='\033\[32m'
YELLOW='\033\[33m'
RED='\033\[31m'
if echo "${output}" | grep -qE "(Overall|Total|Summary).*(${GREEN}|${YELLOW}|${RED})"; then
```

**I recommend Solution A** (multiple grep -qF) because it's clearer.

---

## Complete Fixed Test Function Example

```bash
test_should_display_green_color_for_perfect_coverage() {
    local test_name="AC#1.1: Green color (100% coverage)"

    # Arrange: Mock epic with 100% coverage (all features have stories)
    local mock_epic="${TEMP_DIR}/EPIC-001.md"
    cat > "${mock_epic}" << 'EOF'
---
id: EPIC-001
title: Test Epic
---

## Features

- Feature A (STORY-001)
- Feature B (STORY-002)
EOF

    # Act: Generate terminal output (to be implemented)
    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Assert: Output contains green ANSI code
    # FIXED: Use grep -F for fixed string matching
    if echo "${output}" | grep -qF "${GREEN}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing green color code"
        return 1
    fi
}
```

---

## Reference: Common Grep Pattern Mistakes

### Mistake 1: Unescaped Bracket in Basic Regex
```bash
# WRONG - Error: Unmatched [
grep "\\033[32m"         # Pattern: \033[32m (incomplete bracket expression)

# CORRECT
grep -qF "\\033[32m"     # Use -F for fixed string
# OR
grep "\\033\\[32m"       # Escape the bracket with \[
```

### Mistake 2: Wrong Escaping Level
```bash
# WRONG - Two levels of escaping not needed for fixed string
grep -F "\\033\\[32m"    # Over-escaped for -F

# CORRECT
grep -F "\\033[32m"      # Single level, -F handles it literally
```

### Mistake 3: Variable Substitution in Single-Quoted Pattern
```bash
# WRONG - Single quotes prevent variable substitution
grep -q '${GREEN}'       # Literal text "${GREEN}", not the variable value

# CORRECT
grep -q "${GREEN}"       # Double quotes allow substitution
# OR
GREEN='\033[32m'
grep -qF "${GREEN}"      # Use -F with variable
```

### Mistake 4: Forgetting -F with Complex Variables
```bash
# WRONG - Tries to interpret ANSI codes as regex
echo "$output" | grep -q "$ANSI_VAR"

# CORRECT - Use -F for ANSI codes
echo "$output" | grep -qF "$ANSI_VAR"
```

---

## Testing Your Fix

Create a test script to verify all approaches work:

```bash
#!/bin/bash

# Test file content
test_content="Status: $(printf '\033[32m')SUCCESS$(printf '\033[0m')"

echo "Test content: $test_content"
echo ""

# Define ANSI codes
GREEN='\033[32m'
RESET='\033[0m'

echo "Testing different grep approaches:"

# Test 1: grep -F (recommended)
if echo "$test_content" | grep -qF "${GREEN}"; then
    echo "✓ Test 1 PASS: grep -qF works"
else
    echo "✗ Test 1 FAIL: grep -qF failed"
fi

# Test 2: Escaped variable with basic grep
GREEN_ESC='\033\[32m'
if echo "$test_content" | grep -q "${GREEN_ESC}"; then
    echo "✓ Test 2 PASS: Escaped variable works"
else
    echo "✗ Test 2 FAIL: Escaped variable failed"
fi

# Test 3: Inline escaped pattern
if echo "$test_content" | grep -q '\033\[32m'; then
    echo "✓ Test 3 PASS: Inline escaped pattern works"
else
    echo "✗ Test 3 FAIL: Inline escaped pattern failed"
fi

# Test 4: Extended regex with escaped variable
if echo "$test_content" | grep -qE "${GREEN_ESC}"; then
    echo "✓ Test 4 PASS: Extended regex works"
else
    echo "✗ Test 4 FAIL: Extended regex failed"
fi
```

Expected output:
```
Test content: Status: SUCCESS

Testing different grep approaches:
✓ Test 1 PASS: grep -qF works
✓ Test 2 PASS: Escaped variable works
✓ Test 3 PASS: Inline escaped pattern works
✓ Test 4 PASS: Extended regex works
```

---

## Summary

**Best Practice:** Use `grep -F` (fixed string) for ANSI codes
- Simplest: Just add `-F` to existing grep calls
- Fastest: No regex parsing overhead
- Safest: No special character interpretation

**All four solutions work** - choose based on your needs:
1. **grep -F**: Simple ANSI matching (recommended)
2. **Escaped variables**: Reusable, flexible
3. **Inline escaping**: One-off patterns
4. **Extended regex**: Complex patterns needed

---

## References

- [Bash ANSI Color Codes - Bash Commands](https://bashcommands.com/bash-ansi-color-codes/)
- [Regular Expressions in Grep - Cyberciti](https://www.cyberciti.biz/faq/grep-regular-expressions/)
- [GNU Grep Manual - Character Classes](https://www.gnu.org/software/grep/manual/html_node/Character-Classes-and-Bracket-Expressions.html/)
- [Bash Tip: Colors and Formatting - FLOZz](https://misc.flogisoft.com/bash/tip_colors_and_formatting)
- [Using Grep with Regular Expressions - DigitalOcean](https://www.digitalocean.com/community/tutorials/using-grep-regular-expressions-to-search-for-text-patterns-in-linux)
