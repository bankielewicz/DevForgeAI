# Commands to Fix test_terminal_output.sh

## The Problem

File: `/mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh`

Error: `grep: Unmatched [, [^, [:, [., or [=`

Cause: Using `grep -q "${GREEN}"` where `GREEN='\033[32m'` - the `[` is interpreted as regex syntax.

---

## Solution: Use grep -F

Add the `-F` flag to convert grep from regex mode to fixed-string mode.

---

## Option 1: Manual Edits (5 Changes)

### Change 1: Line 56
**Before:**
```bash
if echo "${output}" | grep -q "${GREEN}"; then
```

**After:**
```bash
if echo "${output}" | grep -qF "${GREEN}"; then
```

### Change 2: Line 94
**Before:**
```bash
if echo "${output}" | grep -q "${YELLOW}"; then
```

**After:**
```bash
if echo "${output}" | grep -qF "${YELLOW}"; then
```

### Change 3: Line 132
**Before:**
```bash
if echo "${output}" | grep -q "${RED}"; then
```

**After:**
```bash
if echo "${output}" | grep -qF "${RED}"; then
```

### Change 4: Line 251
**Before:**
```bash
if echo "${output}" | grep -q "${RESET}"; then
```

**After:**
```bash
if echo "${output}" | grep -qF "${RESET}"; then
```

### Change 5: Line 289 (Compound Check)
**Before:**
```bash
if echo "${output}" | grep -q "${YELLOW}" && ! echo "${output}" | grep -q "${RED}"; then
```

**After:**
```bash
if echo "${output}" | grep -qF "${YELLOW}" && ! echo "${output}" | grep -qF "${RED}"; then
```

### Change 6: Line 216 (Complex - Optional Fix)
This is a complex pattern that combines regex with variables. Two options:

**Option A: Use multiple grep -qF (RECOMMENDED):**
```bash
# Before:
if echo "${output}" | grep -qE "(Overall|Total|Summary).*${GREEN}|${YELLOW}|${RED}"; then

# After:
if echo "${output}" | grep -qE "(Overall|Total|Summary)" && \
   (echo "${output}" | grep -qF "${GREEN}" || \
    echo "${output}" | grep -qF "${YELLOW}" || \
    echo "${output}" | grep -qF "${RED}"); then
```

**Option B: Define escaped variables (Alternative):**
```bash
# Add near the color definitions (around line 14):
GREEN_PATTERN='\033\[32m'
YELLOW_PATTERN='\033\[33m'
RED_PATTERN='\033\[31m'

# Then use at line 216:
if echo "${output}" | grep -qE "(Overall|Total|Summary).*(${GREEN_PATTERN}|${YELLOW_PATTERN}|${RED_PATTERN})"; then
```

---

## Option 2: Automated Script (Uses Edit Tool)

If using the Edit tool (recommended), here are the changes:

### Edit 1: Line 56
```
old_string: if echo "${output}" | grep -q "${GREEN}"; then
new_string: if echo "${output}" | grep -qF "${GREEN}"; then
```

### Edit 2: Line 94
```
old_string: if echo "${output}" | grep -q "${YELLOW}"; then
new_string: if echo "${output}" | grep -qF "${YELLOW}"; then
```

### Edit 3: Line 132
```
old_string: if echo "${output}" | grep -q "${RED}"; then
new_string: if echo "${output}" | grep -qF "${RED}"; then
```

### Edit 4: Line 251
```
old_string: if echo "${output}" | grep -q "${RESET}"; then
new_string: if echo "${output}" | grep -qF "${RESET}"; then
```

### Edit 5: Line 289
```
old_string: if echo "${output}" | grep -q "${YELLOW}" && ! echo "${output}" | grep -q "${RED}"; then
new_string: if echo "${output}" | grep -qF "${YELLOW}" && ! echo "${output}" | grep -qF "${RED}"; then
```

---

## Option 3: Sed Command (One-Liner)

Run this sed command to fix all simple grep -q instances:

```bash
sed -i 's/grep -q "\${/grep -qF "\${/g' /mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh
```

**What it does:**
- Finds all instances of `grep -q "${`
- Replaces with `grep -qF "${`
- Applies to file in-place with `-i`

**Caveat:** This catches the 5 simple cases but not the complex pattern at line 216.

---

## Option 4: Use Edit Tool from This Conversation

I can use the Edit tool to apply these changes directly. Would you like me to:

```
1. Apply all 6 changes now
2. Apply only the 5 simple changes (line 216 needs review)
3. Show you the diffs first
4. Apply changes interactively (one at a time)
```

---

## Testing the Fix

After making changes, run:

```bash
bash /mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh
```

Expected result:
- No more "Unmatched [" errors
- Tests either pass or fail on actual test logic (not syntax errors)

---

## Verification

Check that the changes took effect:

```bash
# Verify the grep -qF changes are in place
grep -n "grep -qF" /mnt/c/Projects/DevForgeAI2/tests/reporting/test_terminal_output.sh

# Should show:
# 56:    if echo "${output}" | grep -qF "${GREEN}"; then
# 94:    if echo "${output}" | grep -qF "${YELLOW}"; then
# 132:   if echo "${output}" | grep -qF "${RED}"; then
# 251:   if echo "${output}" | grep -qF "${RESET}"; then
# 289:   if echo "${output}" | grep -qF "${YELLOW}" && ! echo "${output}" | grep -qF "${RED}"; then
```

---

## Understanding the Fix

### Why grep -F Works

```bash
# Before (ERROR):
grep -q "${GREEN}"
# grep interprets: \033[32m as incomplete regex bracket expression
# Error: "Unmatched ["

# After (WORKS):
grep -qF "${GREEN}"
# -F flag tells grep: "Treat pattern as fixed string, not regex"
# Result: \033[32m is matched literally, no regex parsing
```

### What -F Does

- `-F` = `--fixed-strings`
- Disables all regex metacharacter interpretation
- Treats `[` as literal bracket, not bracket expression start
- Makes matching faster (no regex engine needed)
- All special characters become literal

### Example Comparison

```bash
GREEN='\033[32m'  # This contains: ESC, [, 3, 2, m

# WITHOUT -F (WRONG):
echo "text \033[32m" | grep -q "${GREEN}"
# grep sees pattern: \033[32m
# Tries to parse: \033, then [32 (incomplete bracket expression)
# ERROR: Unmatched [

# WITH -F (CORRECT):
echo "text \033[32m" | grep -qF "${GREEN}"
# grep sees pattern: literal match \033[32m
# Finds it: ESC + literal [ + 32 + m
# SUCCESS: Pattern found
```

---

## Summary

**Best Fix:** Add `-F` to all 5 `grep -q` calls for ANSI color matching.

**Most Common Changes:**
```
grep -q        → grep -qF      (all 5 places)
grep -q        → grep -qF      (for simple ANSI codes)
```

**No escaping needed** - `-F` handles everything literally.

---

## References

- [grep man page - -F flag](https://linux.die.net/man/1/grep)
- [Bash ANSI Color Codes](https://bashcommands.com/bash-ansi-color-codes/)
- [Regular Expressions in Grep](https://www.cyberciti.biz/faq/grep-regular-expressions/)
