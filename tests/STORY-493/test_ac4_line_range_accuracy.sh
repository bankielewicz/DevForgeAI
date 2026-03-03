#!/bin/bash
# Test: AC#4 - Line ranges in manifest match actual section positions
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

echo "=== AC#4: Line ranges in manifest match actual section positions ==="

YAML_CONTENT=$(sed -n '/<!-- SECTION_MANIFEST/,/END_SECTION_MANIFEST -->/p' "$TEMPLATE_FILE" | grep -v 'SECTION_MANIFEST')

# Test 1: Each manifest entry's line_range start matches the actual line of that header
python3 -c "
import sys, yaml

yaml_content = '''$YAML_CONTENT'''
data = yaml.safe_load(yaml_content)

# Read the template file to get actual line numbers
with open('$TEMPLATE_FILE', 'r') as f:
    lines = f.readlines()

errors = []
for section in data['sections']:
    name = section['name']
    level = section['header_level']
    line_start = section['line_range']['start'] if isinstance(section['line_range'], dict) else section['line_range'][0]

    # Build expected header prefix
    prefix = '#' * level + ' '

    # Check that the line at line_start contains the expected header
    actual_line_idx = line_start - 1  # 0-indexed
    if actual_line_idx < 0 or actual_line_idx >= len(lines):
        errors.append(f'{name}: line {line_start} out of range')
        continue

    actual_line = lines[actual_line_idx].strip()
    if not actual_line.startswith(prefix):
        errors.append(f'{name}: expected header at line {line_start}, got: {actual_line[:60]}')

if errors:
    for e in errors:
        print(f'  MISMATCH: {e}')
    sys.exit(1)
" 2>/dev/null
run_test "All manifest line_range start values match actual header positions" $?

# Test 2: At least 5 sections verified (sanity check on test coverage)
python3 -c "
import sys, yaml
data = yaml.safe_load('''$YAML_CONTENT''')
assert len(data['sections']) >= 5, f'Too few sections: {len(data[\"sections\"])}'
" 2>/dev/null
run_test "Manifest contains at least 5 sections" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
