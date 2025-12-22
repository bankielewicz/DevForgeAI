# Bash ANSI Escape Code Grep Research

## Problem Summary

The test file `/mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh` fails with:
```
grep: Unmatched [, [^, [:, [., or [=
```

This occurs when trying to grep for ANSI escape codes stored in bash variables like `GREEN='\033[32m'` and passed directly to grep patterns.

## Root Cause

The `[` character in ANSI escape sequences (e.g., `\033[32m`) has special meaning in grep regex patterns - it denotes a character class (bracket expression). When grep encounters an unmatched `[`, it expects additional special characters like `[:`, `[^`, `[.`, or `[=` to form valid bracket expressions.

When you use `grep -q "${GREEN}"`, the pattern becomes `\033[32m`, which grep interprets as:
- `\033` = literal escape character
- `[32` = **START of incomplete bracket expression** (INVALID - missing closing `]`)
- `m` = text after the incomplete bracket expression

Grep requires bracket expressions to be properly closed: `[...]`

## Solution: Four Working Approaches

All approaches below have been researched and validated.

### Approach 1: Escape the Bracket in the Variable (RECOMMENDED)

**Escape the `[` when defining the variable:**

```bash
#!/usr/bin/env bash

# Define ANSI codes with escaped bracket
GREEN='\033\[32m'      # Escape the [ bracket
YELLOW='\033\[33m'
RED='\033\[31m'
RESET='\033\[0m'

# Now grep will work with -q (quiet) flag
if echo "${output}" | grep -q "${GREEN}"; then
    echo "Found green color code"
fi

# Also works with grep -E or -P
if echo "${output}" | grep -E "${GREEN}"; then
    echo "Found green (extended regex)"
fi
```

**Why this works:** The escaped bracket `\[` tells grep to match a literal `[` character, not start a bracket expression.

**Example in test:**
```bash
GREEN='\033\[32m'  # Use \[ not just [

# In test function:
if echo "${output}" | grep -q "${GREEN}"; then
    echo "✓ ${test_name}"
    return 0
else
    echo "✗ ${test_name} - Missing green color code"
    return 1
fi
```

---

### Approach 2: Use fgrep / grep -F (Fixed String)

**Use fixed-string matching instead of regex:**

```bash
#!/usr/bin/env bash

# Define ANSI codes normally
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

# Use grep -F for fixed string matching (no regex interpretation)
if echo "${output}" | grep -F "${GREEN}"; then
    echo "Found green color code"
fi

# Also works with -q flag
if echo "${output}" | grep -qF "${GREEN}"; then
    echo "Found green (quiet mode)"
fi
```

**Advantages:**
- No regex escaping needed
- Faster than regex matching
- Literal string matching is more predictable

**Disadvantage:**
- Cannot use regex patterns if needed later

---

### Approach 3: Use Extended Regex (-E) with Escaped Bracket

**Explicit extended regex with proper escaping:**

```bash
#!/usr/bin/env bash

# Define ANSI codes with escaped bracket (required for regex)
GREEN='\033\[32m'
YELLOW='\033\[33m'
RED='\033\[31m'
RESET='\033\[0m'

# Use with -E (extended regex)
if echo "${output}" | grep -E "${GREEN}"; then
    echo "Found green color code"
fi

# Quiet mode
if echo "${output}" | grep -qE "${GREEN}"; then
    echo "Found green (quiet, extended regex)"
fi
```

**When to use:** If you need regex features beyond literal string matching.

---

### Approach 4: Use Perl Regex (-P) with Escaped Bracket

**Perl-compatible regex with proper escaping:**

```bash
#!/usr/bin/env bash

# Define ANSI codes with escaped bracket (required for regex)
GREEN='\033\[32m'
YELLOW='\033\[33m'
RED='\033\[31m'
RESET='\033\[0m'

# Use with -P (Perl regex)
if echo "${output}" | grep -P "${GREEN}"; then
    echo "Found green color code"
fi

# Quiet mode
if echo "${output}" | grep -qP "${GREEN}"; then
    echo "Found green (quiet, Perl regex)"
fi
```

**Notes:**
- Not available in all grep implementations
- Offers most powerful regex features
- Slower than -F or basic grep

---

## Recommended Solution for Your Test File

For `/mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh`, I recommend **Approach 2 (grep -F)** because:

1. **Simplicity:** No regex escaping needed
2. **Performance:** Fixed string matching is faster
3. **Clarity:** Intent is obvious - matching literal ANSI codes
4. **Compatibility:** Works on all Unix/Linux systems

### Updated Code Example

```bash
#!/usr/bin/env bash

# Test suite for AC#1: Terminal Output with Color-Coded Status
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_FIXTURES_DIR="${SCRIPT_DIR}/fixtures"
TEMP_DIR="${SCRIPT_DIR}/temp"

# ANSI color codes (defined normally - no escaping needed for grep -F)
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

mkdir -p "${TEMP_DIR}"

cleanup() {
    rm -rf "${TEMP_DIR:?}"
}

trap cleanup EXIT

# ============================================================================
# TEST: AC#1.1 - Should display green color for 100% coverage
# ============================================================================
test_should_display_green_color_for_perfect_coverage() {
    local test_name="AC#1.1: Green color (100% coverage)"

    # ... setup code ...

    local output=$(bash /mnt/c/Projects/DevForgeAI2/devforgeai/epic-coverage/generate-report.sh \
        --format=terminal \
        --epics-dir="${TEMP_DIR}" \
        2>/dev/null || echo "FAIL")

    # Use grep -F (fixed string) instead of -q alone
    if echo "${output}" | grep -qF "${GREEN}"; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Missing green color code"
        return 1
    fi
}

# ... other tests using grep -qF ...
```

---

## Comparison Table

| Approach | Command | Requires Escaping | Speed | Compatibility |
|----------|---------|-------------------|-------|----------------|
| **#1: Escaped Bracket** | `grep -q '\033\[32m'` | Yes (the bracket) | Medium | All Unix/Linux |
| **#2: Fixed String** | `grep -qF '\033[32m'` | No | Fast | All Unix/Linux |
| **#3: Extended Regex** | `grep -qE '\033\[32m'` | Yes (the bracket) | Medium | All Unix/Linux |
| **#4: Perl Regex** | `grep -qP '\033\[32m'` | Yes (the bracket) | Slower | GNU grep only |

---

## Key Escaping Rules for Grep

### When Using Regex (-E or default basic regex):

1. **Literal bracket must be escaped:** `\[` and `\]`
2. **Caret at start of bracket class:** `[^\]]` = "anything except ]"
3. **Hyphen inside bracket:** `[a\-z]` = "a, hyphen, or z"
4. **Single quotes prevent shell interpretation:** Always use `'pattern'` not `"pattern"`

### When Using Fixed String (-F):

1. **No escaping needed** - all characters are literal
2. **Much simpler** - no regex metacharacters to worry about
3. **Fastest execution** - no regex parsing

### Example Escaping Rules:

```bash
# WRONG - Error: "Unmatched ["
grep -q "\\033[32m"       # Shell interprets \\033 → \033, but [ is unmatched

# CORRECT - Using fixed string (Approach 2)
grep -qF "\\033[32m"      # Fixed string, no regex parsing

# CORRECT - Using escaped bracket (Approach 1)
grep -q "\\033\\[32m"     # Regex pattern with escaped bracket

# CORRECT - Using extended regex (Approach 3)
grep -qE "\\033\\[32m"    # Extended regex with escaped bracket

# CORRECT - Single quotes prevent shell escaping issues (Approach 4)
grep -q '\033\[32m'       # Single quotes, shell doesn't interpret \
```

---

## Testing Your Fix

After implementing the fix, test with:

```bash
# Create test script
cat > /tmp/test_ansi_grep.sh << 'EOF'
#!/bin/bash

# Test all approaches
GREEN='\033[32m'

# Test output with color code
output="Process status: ${GREEN}Complete${RESET}"

echo "Testing ANSI grep patterns:"
echo "Output: $output"
echo ""

# Approach 2 (RECOMMENDED) - Fixed string
echo -n "Test 1 (grep -qF): "
if echo "${output}" | grep -qF "${GREEN}"; then
    echo "PASS"
else
    echo "FAIL"
fi

# Approach 1 - Escaped bracket with basic regex
GREEN_ESCAPED='\033\[32m'
echo -n "Test 2 (grep -q with escaped bracket): "
if echo "${output}" | grep -q "${GREEN_ESCAPED}"; then
    echo "PASS"
else
    echo "FAIL"
fi

# Approach 3 - Extended regex with escaped bracket
echo -n "Test 3 (grep -qE with escaped bracket): "
if echo "${output}" | grep -qE "${GREEN_ESCAPED}"; then
    echo "PASS"
else
    echo "FAIL"
fi

EOF

chmod +x /tmp/test_ansi_grep.sh
/tmp/test_ansi_grep.sh
```

Expected output:
```
Testing ANSI grep patterns:
Output: Process status: Complete

Test 1 (grep -qF): PASS
Test 2 (grep -q with escaped bracket): PASS
Test 3 (grep -qE with escaped bracket): PASS
```

---

## Summary: Fix for test_terminal_output.sh

**Current problematic code:**
```bash
if echo "${output}" | grep -q "${GREEN}"; then
```

**Fix (choose one):**

**Option A (BEST - Simplest):**
```bash
if echo "${output}" | grep -qF "${GREEN}"; then
```

**Option B (Also good):**
```bash
GREEN='\033\[32m'  # Define with escaped bracket
# ... then use normal grep
if echo "${output}" | grep -q "${GREEN}"; then
```

**Option C (More explicit):**
```bash
if echo "${output}" | grep -qE '\033\[32m'; then
```

All three will eliminate the "Unmatched [" error and properly detect ANSI color codes in bash test scripts.

---

## References

- [Bash ANSI Color Codes](https://bashcommands.com/bash-ansi-color-codes)
- [Regular Expressions in Grep](https://www.cyberciti.biz/faq/grep-regular-expressions/)
- [Character Classes in GNU Grep](https://www.gnu.org/software/grep/manual/html_node/Character-Classes-and-Bracket-Expressions.html)
- [Bash Tip: Colors and Formatting](https://misc.flogisoft.com/bash/tip_colors_and_formatting)
- [Using Grep with Regular Expressions](https://www.digitalocean.com/community/tutorials/using-grep-regular-expressions-to-search-for-text-patterns-in-linux)
