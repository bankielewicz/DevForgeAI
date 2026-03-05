#!/bin/bash
# Test: AC#2 - Adaptive Question Depth
# Story: STORY-531
# Generated: 2026-03-04

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REF_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/references/lean-canvas-workflow.md"

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

echo "=== AC#2: Adaptive Question Depth ==="

# Test 1: Three distinct adaptive depth sections exist as ### headers in Section 2
grep -q "^### Beginner$" "$REF_FILE" 2>/dev/null
run_test "Reference has ### Beginner section header" $?

grep -q "^### Intermediate$" "$REF_FILE" 2>/dev/null
run_test "Reference has ### Intermediate section header" $?

grep -q "^### Advanced$" "$REF_FILE" 2>/dev/null
run_test "Reference has ### Advanced section header" $?

# Extract Section 2 Beginner (intro + example) for depth keywords
BEGINNER_SECTION=$(sed -n '/^### Beginner$/,/^### /p' "$REF_FILE" | head -n -1)

# Extract Section 2 Intermediate for default check
INTERMEDIATE_SECTION=$(sed -n '/^### Intermediate$/,/^### /p' "$REF_FILE" | head -n -1)

# Extract Section 2 Advanced for concise keywords
ADVANCED_SECTION=$(sed -n '/^### Advanced$/,/^---$/p' "$REF_FILE")

# Test 2: Section 3 has per-block question descriptions for each depth level
# "Beginner Questions" and "Advanced Questions" paragraphs in Section 3
SECTION3=$(sed -n '/^## 3\. /,/^## [0-9]/p' "$REF_FILE" | head -n -1)

# Verify Beginner Questions paragraph references specific blocks
BEGINNER_BLOCKS=$(echo "$SECTION3" | sed -n '/^\*\*Beginner Questions\*\*/,/^\*\*Intermediate/p')
for block in "Problem" "Customer Segments" "Solution" "Channels" "Key Metrics"; do
    echo "$BEGINNER_BLOCKS" | grep -qi "$block"
    run_test "Beginner Questions references block: $block" $?
done

# Verify Advanced Questions paragraph references specific blocks
ADVANCED_BLOCKS=$(echo "$SECTION3" | sed -n '/^\*\*Advanced Questions\*\*/,/^---/p')
for block in "Problem" "Customer Segments" "Solution" "Channels" "Key Metrics"; do
    echo "$ADVANCED_BLOCKS" | grep -qi "$block"
    run_test "Advanced Questions references block: $block" $?
done

# Test 3: Beginner section (Section 2) has extended/detailed depth keywords
echo "$BEGINNER_SECTION" | grep -qi "extended"
run_test "Beginner section contains 'extended' keyword" $?

echo "$BEGINNER_SECTION" | grep -qi "detailed"
run_test "Beginner section contains 'detailed' keyword" $?

echo "$BEGINNER_SECTION" | grep -qi "additional"
run_test "Beginner section contains 'additional' keyword" $?

echo "$BEGINNER_SECTION" | grep -qi "sub-questions"
run_test "Beginner section contains 'sub-questions' keyword" $?

# Test 4: Advanced section (Section 2) has concise/streamlined keywords
echo "$ADVANCED_SECTION" | grep -qi "concise"
run_test "Advanced section contains 'concise' keyword" $?

echo "$ADVANCED_SECTION" | grep -qi "streamlined"
run_test "Advanced section contains 'streamlined' keyword" $?

echo "$ADVANCED_SECTION" | grep -qi "direct"
run_test "Advanced section contains 'direct' keyword" $?

# Test 5: Intermediate is documented as default level
echo "$INTERMEDIATE_SECTION" | grep -qi "default"
run_test "Intermediate section documented as default level" $?

# Test 6: Beginner section is physically longer (more lines) than Advanced section
BEGINNER_LINES=$(echo "$BEGINNER_SECTION" | wc -l)
ADVANCED_LINES=$(echo "$ADVANCED_SECTION" | wc -l)
test "$BEGINNER_LINES" -gt "$ADVANCED_LINES"
run_test "Beginner section ($BEGINNER_LINES lines) is longer than Advanced ($ADVANCED_LINES lines)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
