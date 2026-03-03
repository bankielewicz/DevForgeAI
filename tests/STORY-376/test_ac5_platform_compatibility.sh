#!/bin/sh
# STORY-376 AC#5: Tests Pass on All Supported Platforms
# Validates:
#   (a) Test scripts use POSIX-compatible shell syntax
#   (b) Platform-agnostic path handling
#   (c) No hardcoded platform-specific binary paths
#   (d) Binary name matches current platform
#   (e) Platform-specific execution instructions documented
#
# Exit code: 0 = all pass, 1 = any failure
# POSIX-compatible shell syntax for cross-platform support

set -e

# Source shared helpers (DRY: helpers, counters, config)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "${SCRIPT_DIR}/test_helpers.sh"
init_test_env

# -------------------------------------------------------------------
# Test 1: POSIX-compatible shebang line
# All scripts must use #!/bin/sh (NOT #!/bin/bash)
# -------------------------------------------------------------------
printf "=== AC#5 Test 1: POSIX-compatible shebang ===\n"
for script in $TEST_SCRIPTS; do
    script_file="${TEST_DIR}/${script}"
    if [ ! -f "$script_file" ]; then
        fail_test "${script} not found"
        continue
    fi
    first_line=$(head -1 "$script_file")
    if [ "$first_line" = "#!/bin/sh" ]; then
        pass_test "${script} uses POSIX shebang (#!/bin/sh)"
    else
        fail_test "${script} does NOT use POSIX shebang: ${first_line}"
    fi
done

# -------------------------------------------------------------------
# Test 2: No bash-specific syntax (bashisms)
# Check for common bashisms: [[ ]], (( )), ${var//}, arrays, etc.
# -------------------------------------------------------------------
printf "\n=== AC#5 Test 2: No bash-specific syntax ===\n"
for script in $TEST_SCRIPTS; do
    script_file="${TEST_DIR}/${script}"
    if [ ! -f "$script_file" ]; then
        fail_test "${script} not found - cannot check for bashisms"
        continue
    fi
    bashisms_found=0

    # Check for [[ double bracket test (excluding comments and grep patterns)
    if grep -n "\[\[" "$script_file" 2>/dev/null | grep -v "^[0-9]*:[[:space:]]*#" | grep -v "grep" | grep -v "WARNING" >/dev/null 2>&1; then
        bashisms_found=$((bashisms_found + 1))
        printf "    WARNING: bare [[ test found in %s\n" "$script"
    fi

    # Check for declare / typeset keywords (not in comments)
    if grep -n "^[[:space:]]*declare \|^[[:space:]]*typeset " "$script_file" 2>/dev/null >/dev/null 2>&1; then
        bashisms_found=$((bashisms_found + 1))
        printf "    WARNING: declare/typeset found in %s\n" "$script"
    fi

    # Check for bash-only 'source' instead of POSIX '.' (not in comments)
    if grep -n "^[[:space:]]*source " "$script_file" 2>/dev/null >/dev/null 2>&1; then
        bashisms_found=$((bashisms_found + 1))
        printf "    WARNING: bash source (use . instead) found in %s\n" "$script"
    fi

    # Check for 'local' keyword used outside functions (bash-specific)
    if grep -n "^local " "$script_file" 2>/dev/null >/dev/null 2>&1; then
        bashisms_found=$((bashisms_found + 1))
        printf "    WARNING: top-level local keyword found in %s\n" "$script"
    fi

    if [ "$bashisms_found" -eq 0 ]; then
        pass_test "${script} - no bashisms detected"
    else
        fail_test "${script} - ${bashisms_found} bashism(s) detected"
    fi
done

# -------------------------------------------------------------------
# Test 3: No hardcoded platform-specific binary paths
# Forbidden: hardcoded absolute paths to treelint binary
# -------------------------------------------------------------------
printf "\n=== AC#5 Test 3: No hardcoded platform-specific paths ===\n"
for script in $TEST_SCRIPTS; do
    script_file="${TEST_DIR}/${script}"
    if [ ! -f "$script_file" ]; then
        fail_test "${script} not found"
        continue
    fi
    hardcoded_found=0

    # Check for hardcoded absolute paths to treelint binary
    if grep -n "/usr/local/bin/" "$script_file" 2>/dev/null | grep -v "^[0-9]*:[[:space:]]*#" | grep -v "hardcoded_patterns\|hc_pattern" >/dev/null 2>&1; then
        hardcoded_found=$((hardcoded_found + 1))
    fi
    if grep -n "/opt/" "$script_file" 2>/dev/null | grep -v "^[0-9]*:[[:space:]]*#" | grep -v "hardcoded_patterns\|hc_pattern" >/dev/null 2>&1; then
        hardcoded_found=$((hardcoded_found + 1))
    fi

    if [ "$hardcoded_found" -eq 0 ]; then
        pass_test "${script} - no hardcoded platform-specific paths"
    else
        fail_test "${script} - ${hardcoded_found} hardcoded path(s) found"
    fi
done

# -------------------------------------------------------------------
# Test 4: Platform-agnostic path construction
# Scripts should use variable-based paths (PROJECT_ROOT, SCRIPT_DIR)
# -------------------------------------------------------------------
printf "\n=== AC#5 Test 4: Platform-agnostic path construction ===\n"
for script in $TEST_SCRIPTS; do
    script_file="${TEST_DIR}/${script}"
    if [ ! -f "$script_file" ]; then
        fail_test "${script} not found"
        continue
    fi
    if grep -q "PROJECT_ROOT\|SCRIPT_DIR" "$script_file" 2>/dev/null; then
        pass_test "${script} uses variable-based path construction"
    else
        fail_test "${script} does NOT use variable-based path construction"
    fi
done

# -------------------------------------------------------------------
# Test 5: Scripts are independently executable (BR-002)
# Each script must have execute permission capability
# -------------------------------------------------------------------
printf "\n=== AC#5 Test 5: Scripts are executable ===\n"
for script in $TEST_SCRIPTS; do
    script_file="${TEST_DIR}/${script}"
    if [ ! -f "$script_file" ]; then
        fail_test "${script} not found"
        continue
    fi
    # Check if file starts with shebang (can be made executable)
    if head -1 "$script_file" | grep -q "^#!" 2>/dev/null; then
        pass_test "${script} has shebang (can be made executable)"
    else
        fail_test "${script} missing shebang line"
    fi
done

# -------------------------------------------------------------------
# Test 6: Treelint binary distribution covers supported platforms
# src/bin/treelint/ should contain binaries for Linux, macOS, Windows
# -------------------------------------------------------------------
printf "\n=== AC#5 Test 6: Binary distribution covers platforms ===\n"
BIN_DIR="${PROJECT_ROOT}/src/bin/treelint"
if [ -d "$BIN_DIR" ]; then
    for platform_binary in treelint-linux-x86_64 treelint-darwin-x86_64 treelint-darwin-aarch64 treelint-windows-x86_64.exe; do
        if [ -f "${BIN_DIR}/${platform_binary}" ]; then
            pass_test "Binary ${platform_binary} exists"
        else
            fail_test "Binary ${platform_binary} NOT found in ${BIN_DIR}"
        fi
    done
else
    fail_test "Binary distribution directory not found: ${BIN_DIR}"
fi

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print_summary_and_exit "AC#5"
