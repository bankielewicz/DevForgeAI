#!/bin/bash
# Test AC#6: Operational Copy Synchronization
# STORY-331: Refactor agent-generator.md with Progressive Disclosure
#
# Validates:
# - src/claude/agents/agent-generator.md and .claude/agents/agent-generator.md are identical
# - src/claude/agents/agent-generator/references/ and .claude/agents/agent-generator/references/
#   contain identical files
#
# Expected: FAIL initially (TDD Red phase - copies not yet synchronized)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Source files (src/ is source of truth)
SRC_CORE="$PROJECT_ROOT/src/claude/agents/agent-generator.md"
SRC_REF_DIR="$PROJECT_ROOT/src/claude/agents/agent-generator/references"

# Operational files (.claude/ is operational copy)
OP_CORE="$PROJECT_ROOT/.claude/agents/agent-generator.md"
OP_REF_DIR="$PROJECT_ROOT/.claude/agents/agent-generator/references"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: Source core file exists
# -----------------------------------------------------------------------------
test_src_core_exists() {
    local test_name="Source core file exists"

    if [ -f "$SRC_CORE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $SRC_CORE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Operational core file exists
# -----------------------------------------------------------------------------
test_op_core_exists() {
    local test_name="Operational core file exists"

    if [ -f "$OP_CORE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $OP_CORE"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Core files are identical
# -----------------------------------------------------------------------------
test_core_files_identical() {
    local test_name="Core files are identical (src/ == .claude/)"

    if [ ! -f "$SRC_CORE" ]; then
        fail_test "$test_name" "Source file not found"
        return
    fi

    if [ ! -f "$OP_CORE" ]; then
        fail_test "$test_name" "Operational file not found"
        return
    fi

    if diff -q "$SRC_CORE" "$OP_CORE" > /dev/null 2>&1; then
        pass_test "$test_name"
    else
        local diff_lines
        diff_lines=$(diff "$SRC_CORE" "$OP_CORE" | wc -l)
        fail_test "$test_name" "Files differ ($diff_lines lines of diff)"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Source reference directory exists
# -----------------------------------------------------------------------------
test_src_ref_dir_exists() {
    local test_name="Source reference directory exists"

    if [ -d "$SRC_REF_DIR" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Directory not found: $SRC_REF_DIR"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Operational reference directory exists
# -----------------------------------------------------------------------------
test_op_ref_dir_exists() {
    local test_name="Operational reference directory exists"

    if [ -d "$OP_REF_DIR" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Directory not found: $OP_REF_DIR"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Reference directories have same file count
# -----------------------------------------------------------------------------
test_ref_file_count_match() {
    local test_name="Reference directories have same file count"

    if [ ! -d "$SRC_REF_DIR" ]; then
        fail_test "$test_name" "Source directory not found"
        return
    fi

    if [ ! -d "$OP_REF_DIR" ]; then
        fail_test "$test_name" "Operational directory not found"
        return
    fi

    local src_count
    local op_count
    src_count=$(find "$SRC_REF_DIR" -maxdepth 1 -type f -name "*.md" | wc -l)
    op_count=$(find "$OP_REF_DIR" -maxdepth 1 -type f -name "*.md" | wc -l)

    if [ "$src_count" -eq "$op_count" ]; then
        pass_test "$test_name (both have $src_count files)"
    else
        fail_test "$test_name" "src/ has $src_count, .claude/ has $op_count files"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Reference directories have same files
# -----------------------------------------------------------------------------
test_ref_same_files() {
    local test_name="Reference directories have same filenames"

    if [ ! -d "$SRC_REF_DIR" ]; then
        fail_test "$test_name" "Source directory not found"
        return
    fi

    if [ ! -d "$OP_REF_DIR" ]; then
        fail_test "$test_name" "Operational directory not found"
        return
    fi

    local src_files
    local op_files
    src_files=$(find "$SRC_REF_DIR" -maxdepth 1 -type f -name "*.md" -exec basename {} \; | sort)
    op_files=$(find "$OP_REF_DIR" -maxdepth 1 -type f -name "*.md" -exec basename {} \; | sort)

    if [ "$src_files" = "$op_files" ]; then
        pass_test "$test_name"
    else
        local in_src_only
        local in_op_only
        in_src_only=$(comm -23 <(echo "$src_files") <(echo "$op_files") | tr '\n' ' ')
        in_op_only=$(comm -13 <(echo "$src_files") <(echo "$op_files") | tr '\n' ' ')
        fail_test "$test_name" "Only in src/: [$in_src_only] Only in .claude/: [$in_op_only]"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: All reference files are identical
# -----------------------------------------------------------------------------
test_ref_files_identical() {
    local test_name="All reference files are identical"

    if [ ! -d "$SRC_REF_DIR" ]; then
        fail_test "$test_name" "Source directory not found"
        return
    fi

    if [ ! -d "$OP_REF_DIR" ]; then
        fail_test "$test_name" "Operational directory not found"
        return
    fi

    local different_files=""

    while IFS= read -r file; do
        local basename
        basename=$(basename "$file")
        local op_file="$OP_REF_DIR/$basename"

        if [ -f "$op_file" ]; then
            if ! diff -q "$file" "$op_file" > /dev/null 2>&1; then
                different_files="$different_files $basename"
            fi
        else
            different_files="$different_files $basename(missing)"
        fi
    done < <(find "$SRC_REF_DIR" -maxdepth 1 -type f -name "*.md")

    if [ -z "$different_files" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Different files:$different_files"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Diff returns empty for full directory comparison
# -----------------------------------------------------------------------------
test_full_directory_diff() {
    local test_name="Full directory diff returns empty"

    if [ ! -d "$SRC_REF_DIR" ]; then
        fail_test "$test_name" "Source directory not found"
        return
    fi

    if [ ! -d "$OP_REF_DIR" ]; then
        fail_test "$test_name" "Operational directory not found"
        return
    fi

    local diff_output
    diff_output=$(diff -rq "$SRC_REF_DIR" "$OP_REF_DIR" 2>&1 || true)

    if [ -z "$diff_output" ]; then
        pass_test "$test_name"
    else
        local diff_count
        diff_count=$(echo "$diff_output" | wc -l)
        fail_test "$test_name" "$diff_count differences found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-331 AC#6: Sync Verification"
echo "=============================================="
echo "Source core: $SRC_CORE"
echo "Operational core: $OP_CORE"
echo "Source refs: $SRC_REF_DIR"
echo "Operational refs: $OP_REF_DIR"
echo "----------------------------------------------"
echo ""

run_test "1" test_src_core_exists
run_test "2" test_op_core_exists
run_test "3" test_core_files_identical
run_test "4" test_src_ref_dir_exists
run_test "5" test_op_ref_dir_exists
run_test "6" test_ref_file_count_match
run_test "7" test_ref_same_files
run_test "8" test_ref_files_identical
run_test "9" test_full_directory_diff

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
