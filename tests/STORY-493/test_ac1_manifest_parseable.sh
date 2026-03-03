#!/bin/bash
# Test: AC#1 - Manifest block exists and is parseable
# Story: STORY-493
# Generated: 2026-02-23
set +e

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TEMPLATE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md"

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED+1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED+1))
    fi
}

echo "=== AC#1: Manifest block exists and is parseable ==="

# Test 1: Template file exists
test -f "$TEMPLATE_FILE"
run_test "Template file exists" $?

# Test 2: First 200 lines contain manifest start delimiter
head -200 "$TEMPLATE_FILE" | grep -q "<!-- SECTION_MANIFEST"
run_test "Manifest start delimiter found in first 200 lines" $?

# Test 3: First 200 lines contain manifest end delimiter
head -200 "$TEMPLATE_FILE" | grep -q "END_SECTION_MANIFEST -->"
run_test "Manifest end delimiter found in first 200 lines" $?

# Test 4: YAML content between delimiters parses without errors
YAML_CONTENT=$(sed -n '/<!-- SECTION_MANIFEST/,/END_SECTION_MANIFEST -->/p' "$TEMPLATE_FILE" | grep -v 'SECTION_MANIFEST')
echo "$YAML_CONTENT" | python3 -c "import sys, yaml; yaml.safe_load(sys.stdin.read())" 2>/dev/null
run_test "YAML content parses without errors" $?

# Test 5: Manifest contains a 'sections' key
echo "$YAML_CONTENT" | python3 -c "
import sys, yaml
data = yaml.safe_load(sys.stdin.read())
assert 'sections' in data, 'Missing sections key'
" 2>/dev/null
run_test "Manifest contains 'sections' key" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
