#!/bin/bash
# STORY-213: Documentation Update Test Specification
# Target: .claude/commands/create-missing-stories.md
# Type: Structural validation (grep-based) - TDD RED phase
# All tests should FAIL initially (documentation not yet updated)

TARGET_FILE=".claude/commands/create-missing-stories.md"
PASS=0
FAIL=0

run_test() {
    local desc="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        ((PASS++))
        echo "PASS: $desc"
    else
        ((FAIL++))
        echo "FAIL: $desc"
    fi
}

echo "=== STORY-213 Documentation Tests ==="
echo "Target: $TARGET_FILE"
echo ""

# DOC-001: Story Quality Gates section header
run_test "DOC-001: Story Quality Gates section exists" grep -q "## Story Quality Gates" "$TARGET_FILE"

# DOC-002: 4 required story elements
run_test "DOC-002a: verified_violations documented" grep -q "verified_violations" "$TARGET_FILE"
run_test "DOC-002b: File paths requirement documented" grep -qi "file paths" "$TARGET_FILE"
run_test "DOC-002c: Line numbers requirement documented" grep -qi "line numbers" "$TARGET_FILE"
run_test "DOC-002d: No placeholders requirement documented" grep -qi "placeholder" "$TARGET_FILE"

# DOC-003: Failure reasons table with 4+ entries
run_test "DOC-003: Failure reasons table has 4+ rows" bash -c "grep -c '^|.*|.*|.*|$' '$TARGET_FILE' | grep -q '[4-9]'"

# DOC-004: Example error with CRITICAL marker
run_test "DOC-004: Example error with CRITICAL marker" grep -q "CRITICAL" "$TARGET_FILE"

# DOC-005: Evidence rationale (4 reasons)
run_test "DOC-005: 4+ evidence rationale reasons" bash -c "count=\$(grep -cE '^[0-9]+\\. \\*\\*' '$TARGET_FILE'); [ \"\$count\" -ge 4 ]"

# DOC-006: Reference to citation-requirements.md
run_test "DOC-006: Citation requirements path referenced" grep -q "citation-requirements.md" "$TARGET_FILE"

# DOC-007: References to STORY-211 and STORY-212
run_test "DOC-007a: STORY-211 referenced" grep -q "STORY-211" "$TARGET_FILE"
run_test "DOC-007b: STORY-212 referenced" grep -q "STORY-212" "$TARGET_FILE"

# DOC-008: Position after Implementation Notes
run_test "DOC-008: Section after Implementation Notes" bash -c "awk '/## Implementation Notes/{f=1} f && /## Story Quality Gates/{print 1; exit}' '$TARGET_FILE' | grep -q 1"

# DOC-009: RCA-020 reference
run_test "DOC-009: RCA-020 referenced" grep -q "RCA-020" "$TARGET_FILE"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
