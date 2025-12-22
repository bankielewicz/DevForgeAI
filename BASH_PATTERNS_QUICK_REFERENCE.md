# Bash Patterns Quick Reference - Gap Detection Fixes

**Quick lookup for the 5 core technical issues and their solutions**

---

## Issue 1: Associative Array Namerefs (`local -n`)

### The Problem
```bash
# WRONG - Creates scope issues
declare -A my_array
function_name() {
    local -n ref=$1  # Can cause circular reference if name collision
}
```

### The Solution
```bash
# RIGHT - Safe nameref pattern
declare -A my_array

function_name() {
    local -n ref
    ref=$1  # Separate declaration from assignment

    # Use ref to modify original array
    ref[key]="value"
}

# Call with ARRAY NAME (not expanded)
function_name my_array  # NOT "${my_array[@]}" or "$my_array"
```

### Test Pattern
```bash
test_function() {
    declare -A test_array  # Declare array in test
    local result

    result=$(function_name test_array "$dir")  # Pass name

    if [[ ${#test_array[@]} -gt 0 ]]; then
        pass_test "Array modified correctly"
    fi
}
```

---

## Issue 2: WSL2 File System Performance

### The Problem
```bash
# WSL2 /mnt/c/ is 10x slower than native Linux
TEST_DIR="/mnt/c/projects/test"  # SLOW
elapsed: 924ms (FAILS - expected <500ms)
```

### The Solution
```bash
# Use Linux filesystem instead
TEST_DIR="/tmp/gap-detection-fixtures-$$"  # FAST

# Detect WSL2 and adjust threshold
if grep -qi "microsoft\|wsl" /proc/version 2>/dev/null; then
    threshold=3000  # WSL2: 6x slower
else
    threshold=500   # Native Linux
fi
```

### Implementation
```bash
test_performance() {
    # Use /tmp for fast I/O
    TEST_FIXTURES_DIR="/tmp/gap-detection-fixtures-$$"

    # Detect environment
    local threshold=500
    [[ -f /proc/version ]] && grep -qi "microsoft\|wsl" /proc/version && threshold=3000

    # Run test with adaptive threshold
    elapsed=$((end_time - start_time))
    [[ $elapsed -lt $threshold ]] && pass_test || fail_test
}
```

---

## Issue 3: Bash Glob Patterns Not Matching

### The Problem
```bash
# WRONG - Returns literal "*.story.md" if no files exist
for file in "$dir"/*.story.md; do
    [[ -f "$file" ]] || continue
    # If no files: $file = "*.story.md" (string literal)
done

# Results in wrong count or processing literal filename
```

### The Solution
```bash
# RIGHT - Use find command instead
while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    # Process file
done < <(find "$dir" -maxdepth 1 -name "*.story.md" -type f)

# OR enable nullglob
shopt -s nullglob
local files=("$dir"/*.story.md)
if [[ ${#files[@]} -eq 0 ]]; then
    # Handle no matches case
fi
```

### Test Pattern
```bash
# Test with missing files
test_missing_features() {
    local epic_file=$(create_epic_file "015")
    append_epic_row "$epic_file" "001" "1" "Feature" "5" "Approved"
    # NOTE: Do NOT create STORY-001.story.md

    # find command should detect missing file
    find_missing_features "EPIC-015" epic_map story_map missing "$dir"

    [[ -v missing[STORY-001] ]] && pass_test || fail_test
}
```

---

## Issue 4: bc Calculator Returns 0 for Division

### The Problem
```bash
# WRONG - Default scale=0 (no decimals)
percentage=$(echo "1 / 3" | bc)
echo "$percentage"  # Output: 0 (not 0.333...)

completion=$(echo "$a / $b" | bc)
# If a=33, b=100: Output: 0 (should be 33.0)
```

### The Solution
```bash
# RIGHT - Explicitly set scale and multiply first
percentage=$(echo "scale=1; ($a * 100) / $b" | bc)

# Ensure decimal point always exists
[[ "$percentage" != *.* ]] && percentage="${percentage}.0"

echo "$percentage"  # Output: 33.3
```

### Test Cases
```bash
# 5/3 * 100 = 60.0
result=$(calculate_completion 5 3)
[[ "$result" == "60.0" ]] && pass_test || fail_test

# 1/3 * 100 = 33.3 (not 33)
result=$(calculate_completion 3 1)
[[ "$result" == "33.3" ]] && pass_test || fail_test

# 0/0 = 0.0 (division by zero handling)
result=$(calculate_completion 0 0)
[[ "$result" == "0.0" ]] && pass_test || fail_test
```

### Formula Pattern
```bash
calculate_completion() {
    local total=$1 completed=$2

    [[ $total -eq 0 ]] && echo "0.0" && return

    # scale=1 for 1 decimal place
    local pct=$(echo "scale=1; ($completed * 100) / $total" | bc)

    # Ensure .0 suffix for integers
    [[ "$pct" != *.* ]] && pct="${pct}.0"

    echo "$pct"
}
```

---

## Issue 5: Sourced Functions & Variable Scope

### The Problem
```bash
# In test file:
declare -A global_array
source gap-detector.sh  # Defines functions

# In gap-detector.sh:
function_from_source() {
    # Can't find global_array due to scope issues
    # Especially in subshells
}
```

### The Solution
```bash
# WRONG - Subshell breaks nameref scope
local count=$(find "$dir" -name "*.md" | wc -l)

# RIGHT - Avoid subshells, pass variables explicitly
while IFS= read -r file; do
    ((count++))
done < <(find "$dir" -name "*.md" -type f)

# RIGHT - Make dependencies explicit
function_that_needs_array() {
    local -n array_ref=$1  # Get array as parameter
    local dir=$2           # Get path as parameter

    # Use explicitly passed variables
    for file in "$dir"/*; do
        array_ref[key]="value"
    done
}
```

### Testing Pattern
```bash
# Test cross-function variable passing
test_cross_function() {
    declare -A array1 array2

    # Function 1 populates array1
    function1 array1 "$dir"

    # Function 2 reads from array1, writes to array2
    function2 array1 array2

    # Verify both arrays modified
    [[ ${#array1[@]} -gt 0 ]] && [[ ${#array2[@]} -gt 0 ]] && pass_test
}
```

---

## Combined Example: Complete Function Pattern

```bash
#!/bin/bash

# CORRECT pattern combining all 5 fixes

# Setup (fix #2: use /tmp)
TEST_DIR="/tmp/gap-test-$$"
mkdir -p "$TEST_DIR"

# Function with nameref, glob, and scope fixes
process_stories() {
    local -n story_map  # Fix #1: nameref
    story_map=$1
    local dir=$2
    local count=0

    # Fix #3: use find instead of glob
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue

        local id=$(basename "$file" .story.md)
        story_map["$id"]="EPIC-VALUE"
        ((count++))
    done < <(find "$dir" -maxdepth 1 -name "STORY-*.story.md" -type f)

    echo "$count"
}

# Calculation function
calculate_percent() {
    local a=$1 b=$2

    [[ $b -eq 0 ]] && echo "0.0" && return

    # Fix #4: bc with scale=1
    local result=$(echo "scale=1; ($a * 100) / $b" | bc)
    [[ "$result" != *.* ]] && result="${result}.0"
    echo "$result"
}

# Main test
main() {
    # Detect WSL2 (fix #2)
    local threshold=500
    grep -qi "microsoft\|wsl" /proc/version 2>/dev/null && threshold=3000

    # Declare array (fix #1)
    declare -A stories

    # Call function with array name (fix #1 & #5)
    local count=$(process_stories stories "$TEST_DIR")

    # Calculate percentage (fix #4)
    local pct=$(calculate_percent 3 1)

    echo "Found $count stories (${pct}%)"

    # Cleanup
    rm -rf "$TEST_DIR"
}

main
```

---

## Debugging Checklist

When test fails, check:

- [ ] **Nameref Issue?** - Is array name passed without `${}`? (`func_name array_name` NOT `func_name "${array_name[@]}"`)
- [ ] **Performance Issue?** - Is `/tmp` used for TEST_DIR? Is WSL2 detected?
- [ ] **Glob Issue?** - Is code using `find` or `nullglob`? Does `[[ -f "$file" ]]` check exist?
- [ ] **bc Issue?** - Is `scale=1` set? Does output have `.0` suffix?
- [ ] **Scope Issue?** - Are variables passed as parameters? Are subshells avoided?

### Trace Script
```bash
# Debug a failing test
set -x  # Enable trace
set -o pipefail  # Fail on pipe errors

# Run single test
bash test_gap_detection.sh 2>&1 | grep "test_strategy1_build_mapping"

# Check what array contains after function call
declare -A test_array
strategy1_extract_epics test_array "$TEST_DIR"
echo "Array size: ${#test_array[@]}"
echo "Contents: ${!test_array[@]}"
```

---

## Reference Links

1. [Bash FAQs - Arrays](https://mywiki.wooledge.org/BashFAQ/006)
2. [bc Precision](https://labex.io/tutorials/linux-how-to-control-decimal-precision-with-the-bc-command-414535)
3. [WSL2 Performance](https://pomeroy.me/2023/12/how-i-fixed-wsl-2-filesystem-performance-issues/)
4. [Bash Globbing](https://mywiki.wooledge.org/glob)
5. [Namerefs](https://rednafi.com/misc/bash_namerefs/)

---

## Quick Command Reference

```bash
# Test nameref locally
declare -A arr=([key]="val")
test_ref() { local -n r=$1; echo "${r[key]}"; }
test_ref arr  # Output: val

# Test bc precision
echo "scale=1; 1*100/3" | bc  # Output: 33.3

# Test find vs glob
find /dir -name "*.md" -type f | wc -l
# vs
shopt -s nullglob; files=(/dir/*.md); echo ${#files[@]}

# Test WSL2 detection
grep -qi "microsoft\|wsl" /proc/version && echo "WSL2" || echo "Native"

# Test variable scope in sourced function
declare -A global_arr
some_func() { local -n ref=$1; ref[x]=1; }
some_func global_arr
echo "${global_arr[x]}"  # Output: 1
```
