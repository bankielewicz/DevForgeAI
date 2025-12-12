# Quick Fix: ANSI Grep Error in test_terminal_output.sh

## The Error
```
grep: Unmatched [, [^, [:, [., or [=
```

## The Problem
Your test uses:
```bash
if echo "${output}" | grep -q "${GREEN}"; then
```

Where `GREEN='\033[32m'`. The `[32m` part is interpreted by grep as an incomplete bracket expression (regex syntax), not a literal character sequence.

## The Quickest Fix

Change all instances of `grep -q "${COLOR_VAR}"` to `grep -qF "${COLOR_VAR}"`:

```bash
# BEFORE (causes error)
if echo "${output}" | grep -q "${GREEN}"; then

# AFTER (fixed)
if echo "${output}" | grep -qF "${GREEN}"; then
```

The `-F` flag tells grep to treat the pattern as a fixed string, not a regex pattern.

## Apply to Your Test File

Replace these lines in `/mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh`:

**Line 56:**
```bash
# OLD
if echo "${output}" | grep -q "${GREEN}"; then

# NEW
if echo "${output}" | grep -qF "${GREEN}"; then
```

**Line 94:**
```bash
# OLD
if echo "${output}" | grep -q "${YELLOW}"; then

# NEW
if echo "${output}" | grep -qF "${YELLOW}"; then
```

**Line 132:**
```bash
# OLD
if echo "${output}" | grep -q "${RED}"; then

# NEW
if echo "${output}" | grep -qF "${RED}"; then
```

**Line 251:**
```bash
# OLD
if echo "${output}" | grep -q "${RESET}"; then

# NEW
if echo "${output}" | grep -qF "${RESET}"; then
```

**Lines 289-290:**
```bash
# OLD
if echo "${output}" | grep -q "${YELLOW}" && ! echo "${output}" | grep -q "${RED}"; then

# NEW
if echo "${output}" | grep -qF "${YELLOW}" && ! echo "${output}" | grep -qF "${RED}"; then
```

**Line 216:**
```bash
# OLD
if echo "${output}" | grep -qE "(Overall|Total|Summary).*${GREEN}|${YELLOW}|${RED}"; then

# NEW - This one needs a different fix (variable substitution in regex)
if echo "${output}" | grep -qE "(Overall|Total|Summary).*($(echo -n "${GREEN}" | sed 's/\[/\\[/g' | sed 's/\]/\\]/g')|$(echo -n "${YELLOW}" | sed 's/\[/\\[/g' | sed 's/\]/\\]/g')|$(echo -n "${RED}" | sed 's/\[/\\[/g' | sed 's/\]/\\]/g'))"; then
```

## Why This Works

- `grep` interprets patterns as regex by default
- In regex, `[...]` denotes a character class (bracket expression)
- When grep sees `[32m`, it tries to parse it as a bracket expression and fails
- `-F` flag forces fixed-string matching, treating `[` as a literal character
- No escaping needed with `-F`

## Test It

```bash
bash /mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh
```

Should now pass without the "Unmatched [" error.

## Alternative Fix (If You Need Regex)

If you need regex features, escape the bracket in the variable definition:

```bash
# Define with escaped bracket
GREEN='\033\[32m'
YELLOW='\033\[33m'
RED='\033\[31m'
RESET='\033\[0m'

# Then use normal grep
if echo "${output}" | grep -q "${GREEN}"; then
```

Both approaches work - the `-F` approach is simpler and faster.
