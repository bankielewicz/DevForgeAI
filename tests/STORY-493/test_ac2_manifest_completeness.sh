#!/bin/bash
# Test: AC#2 - Manifest lists all required sections with correct metadata
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

echo "=== AC#2: Manifest lists all required sections with correct metadata ==="

YAML_CONTENT=$(sed -n '/<!-- SECTION_MANIFEST/,/END_SECTION_MANIFEST -->/p' "$TEMPLATE_FILE" | grep -v 'SECTION_MANIFEST')

# Test 1: Exactly 12 ##-level entries
python3 -c "
import sys, yaml
data = yaml.safe_load('''$YAML_CONTENT''')
h2_entries = [s for s in data['sections'] if s['header_level'] == 2]
assert len(h2_entries) == 12, f'Expected 12 ##-level entries, got {len(h2_entries)}'
" 2>/dev/null
run_test "Exactly 12 ##-level entries" $?

# Test 2: Exactly 16 ###-level entries
python3 -c "
import sys, yaml
data = yaml.safe_load('''$YAML_CONTENT''')
h3_entries = [s for s in data['sections'] if s['header_level'] == 3]
assert len(h3_entries) == 16, f'Expected 16 ###-level entries, got {len(h3_entries)}'
" 2>/dev/null
run_test "Exactly 16 ###-level entries" $?

# Test 3: Exactly 2 entries have status "Optional"
python3 -c "
import sys, yaml
data = yaml.safe_load('''$YAML_CONTENT''')
optional = [s for s in data['sections'] if s.get('status') == 'Optional']
assert len(optional) == 2, f'Expected 2 Optional entries, got {len(optional)}'
" 2>/dev/null
run_test "Exactly 2 entries with status Optional" $?

# Test 4: Each entry has required fields (name, header_level, line_range, status)
python3 -c "
import sys, yaml
data = yaml.safe_load('''$YAML_CONTENT''')
required_fields = {'name', 'header_level', 'line_range', 'status'}
for i, section in enumerate(data['sections']):
    missing = required_fields - set(section.keys())
    assert not missing, f'Entry {i} missing fields: {missing}'
" 2>/dev/null
run_test "Each entry has name, header_level, line_range, status" $?

# Test 5: BR-001 - Manifest includes last_verified date in ISO 8601 format
python3 -c "
import sys, yaml, re
data = yaml.safe_load('''$YAML_CONTENT''')
lv = str(data.get('last_verified', ''))
assert re.match(r'^\d{4}-\d{2}-\d{2}', lv), f'last_verified not ISO 8601: {lv}'
" 2>/dev/null
run_test "BR-001: last_verified date in ISO 8601 format" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
