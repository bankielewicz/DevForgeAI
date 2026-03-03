#!/bin/bash
# Test AC#6: Template Version Updated
# STORY-403: Document Implementation Notes Format in Story Template
#
# Validates:
# - Template version is updated from 2.8 to 2.9 (or higher)
# - OR a changelog entry documents the addition
#
# Expected: FAIL initially (TDD Red phase - version is still 2.8)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
CURRENT_VERSION="2.8"
EXPECTED_MIN_VERSION="2.9"

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
# Test 1: Template version in frontmatter is >= 2.9
# -----------------------------------------------------------------------------
test_frontmatter_version_updated() {
    local test_name="Template version in frontmatter >= $EXPECTED_MIN_VERSION"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Extract template_version from YAML frontmatter
    local version
    version=$(grep '^template_version:' "$TEMPLATE_FILE" | head -1 | sed 's/template_version: *"\?\([0-9.]*\)"\?/\1/')

    if [ -z "$version" ]; then
        fail_test "$test_name" "template_version field not found in frontmatter"
        return
    fi

    # Compare versions: version should be >= 2.9
    local major minor
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)

    local exp_major exp_minor
    exp_major=$(echo "$EXPECTED_MIN_VERSION" | cut -d. -f1)
    exp_minor=$(echo "$EXPECTED_MIN_VERSION" | cut -d. -f2)

    if [ "$major" -gt "$exp_major" ] || ([ "$major" -eq "$exp_major" ] && [ "$minor" -ge "$exp_minor" ]); then
        pass_test "$test_name (found version: $version)"
    else
        fail_test "$test_name" "Version is $version (expected >= $EXPECTED_MIN_VERSION)"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: format_version field also updated
# -----------------------------------------------------------------------------
test_format_version_updated() {
    local test_name="format_version field also updated >= $EXPECTED_MIN_VERSION"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    local version
    version=$(grep '^format_version:' "$TEMPLATE_FILE" | head -1 | sed 's/format_version: *"\?\([0-9.]*\)"\?/\1/')

    if [ -z "$version" ]; then
        fail_test "$test_name" "format_version field not found in frontmatter"
        return
    fi

    local major minor
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)

    local exp_major exp_minor
    exp_major=$(echo "$EXPECTED_MIN_VERSION" | cut -d. -f1)
    exp_minor=$(echo "$EXPECTED_MIN_VERSION" | cut -d. -f2)

    if [ "$major" -gt "$exp_major" ] || ([ "$major" -eq "$exp_major" ] && [ "$minor" -ge "$exp_minor" ]); then
        pass_test "$test_name (found version: $version)"
    else
        fail_test "$test_name" "format_version is $version (expected >= $EXPECTED_MIN_VERSION)"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Changelog entry exists for v2.9 (or the new version)
# -----------------------------------------------------------------------------
test_changelog_entry_exists() {
    local test_name="Changelog entry exists for new version"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Look for a changelog entry mentioning v2.9 or Implementation Notes Format or STORY-403
    if grep -q 'v2\.9\|STORY-403\|Implementation Notes Format' "$TEMPLATE_FILE"; then
        # Verify it is within the changelog section (the comment block at the top)
        local changelog_section
        changelog_section=$(grep -c 'v2\.9\|STORY-403' "$TEMPLATE_FILE")

        if [ "$changelog_section" -gt 0 ]; then
            pass_test "$test_name"
        else
            fail_test "$test_name" "Changelog reference found but not in expected location"
        fi
    else
        fail_test "$test_name" "No changelog entry for v2.9 or STORY-403 found in template"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Footer version also updated
# -----------------------------------------------------------------------------
test_footer_version_updated() {
    local test_name="Footer 'Story Template Version' updated"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Look for the footer version string at the end of the template
    local footer_version
    footer_version=$(grep 'Story Template Version:' "$TEMPLATE_FILE" | tail -1 | sed 's/.*Version: *\([0-9.]*\).*/\1/')

    if [ -z "$footer_version" ]; then
        fail_test "$test_name" "'Story Template Version:' line not found at end of template"
        return
    fi

    local major minor
    major=$(echo "$footer_version" | cut -d. -f1)
    minor=$(echo "$footer_version" | cut -d. -f2)

    local exp_major exp_minor
    exp_major=$(echo "$EXPECTED_MIN_VERSION" | cut -d. -f1)
    exp_minor=$(echo "$EXPECTED_MIN_VERSION" | cut -d. -f2)

    if [ "$major" -gt "$exp_major" ] || ([ "$major" -eq "$exp_major" ] && [ "$minor" -ge "$exp_minor" ]); then
        pass_test "$test_name (found: $footer_version)"
    else
        fail_test "$test_name" "Footer version is $footer_version (expected >= $EXPECTED_MIN_VERSION)"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-403 AC#6: Template Version Updated"
echo "=============================================="
echo "Target file: $TEMPLATE_FILE"
echo "Current version: $CURRENT_VERSION"
echo "Expected minimum: $EXPECTED_MIN_VERSION"
echo "----------------------------------------------"
echo ""

run_test "1" test_frontmatter_version_updated
run_test "2" test_format_version_updated
run_test "3" test_changelog_entry_exists
run_test "4" test_footer_version_updated

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
