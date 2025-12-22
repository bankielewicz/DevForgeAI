#!/bin/bash
# ============================================================================
# STORY-122 Integration Test 2: Shell Script Executes Without $'\r' Error
# ============================================================================
#
# AC#3: Shell Scripts Explicitly Set to LF
#
# Given: A shell script committed through git with .gitattributes
# When: The script is executed on Linux/WSL
# Then: No "$'\r': command not found" error occurs
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GITATTRIBUTES_PATH="$PROJECT_ROOT/.gitattributes"
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

# Check prerequisites
if [ ! -f "$GITATTRIBUTES_PATH" ]; then
    echo "SKIP: .gitattributes not found at project root" >&2
    exit 77
fi

cd "$TEST_TMPDIR"

# Initialize test repository
git init >/dev/null 2>&1
git config user.email "test@test.com"
git config user.name "Test User"

# Copy project's .gitattributes
cp "$GITATTRIBUTES_PATH" .gitattributes
git add .gitattributes
git commit -m "Add .gitattributes" >/dev/null 2>&1

# Create a shell script with CRLF endings (simulating Windows edit)
printf '#!/bin/bash\r\necho "Hello World"\r\nexit 0\r\n' > test_script.sh
chmod +x test_script.sh

# Commit the script (should normalize to LF)
git add test_script.sh
git commit -m "Add test script" >/dev/null 2>&1

# Checkout fresh to apply .gitattributes normalization
rm test_script.sh
git checkout test_script.sh

# Execute the script
OUTPUT=$(./test_script.sh 2>&1) || {
    echo "FAIL: Script execution failed with: $OUTPUT" >&2
    exit 1
}

# Verify output
if [[ "$OUTPUT" != "Hello World" ]]; then
    echo "FAIL: Unexpected output: $OUTPUT" >&2
    exit 1
fi

echo "PASS: Shell script executes without line ending errors"
exit 0
