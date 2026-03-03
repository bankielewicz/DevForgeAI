#!/usr/bin/env bash
# STORY-383 AC#1: All 8 Repos Analyzed with Patterns Extracted
# Validates that the research document's "Dev Tools and Domain Patterns" section
# references all 8 Anthropic repos and extracts at least 1 pattern from each.
#
# Expected: FAIL (Dev Tools section does not exist yet - TDD Red phase)

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
DOC="$PROJECT_ROOT/devforgeai/specs/research/prompt-engineering-patterns.md"

PASS=0
FAIL=0

fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
pass() { echo "PASS: $1"; PASS=$((PASS + 1)); }

# Test 1: Document exists
if [ -f "$DOC" ]; then
  pass "Research document exists"
else
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 2: "Dev Tools and Domain Patterns" section header exists
if grep -q "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null; then
  pass "Dev Tools and Domain Patterns section header found"
else
  fail "Dev Tools and Domain Patterns section header not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 3-10: Each of the 8 repos is referenced in the Dev Tools section
REPOS=(
  "claude-code-action"
  "claude-code-security-review"
  "claude-plugins-official"
  "claude-constitution"
  "healthcare"
  "life-sciences"
  "original_performance_takehome"
  "beam"
)

# Extract only the Dev Tools section content (from "## Dev Tools" to next h2 or EOF)
dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$dev_tools_section" ]; then
  # If it's the last section, take everything from header to EOF
  dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,$p' "$DOC" 2>/dev/null)
fi

for repo in "${REPOS[@]}"; do
  count=$(echo "$dev_tools_section" | grep -c "$repo" 2>/dev/null || echo "0")
  if [ "$count" -ge 1 ]; then
    pass "Repo '$repo' referenced in Dev Tools section ($count occurrences)"
  else
    fail "Repo '$repo' not found in Dev Tools section"
  fi
done

# Test 11: All 8 repos have at least one mention
repos_found=0
for repo in "${REPOS[@]}"; do
  if echo "$dev_tools_section" | grep -q "$repo" 2>/dev/null; then
    repos_found=$((repos_found + 1))
  fi
done

if [ "$repos_found" -ge 8 ]; then
  pass "All 8 repos represented in Dev Tools section ($repos_found found)"
else
  fail "Not all 8 repos represented ($repos_found of 8 found)"
fi

# Test 12: Minimum 8 patterns total in Dev Tools section (BR-004)
# Patterns are marked with "#### Pattern D" headers in the document (D for Dev Tools/Domain)
pattern_count=$(echo "$dev_tools_section" | grep -c "^#### Pattern D[0-9]" 2>/dev/null || echo "0")
if [ "$pattern_count" -ge 8 ]; then
  pass "At least 8 patterns found in Dev Tools section ($pattern_count)"
else
  fail "Fewer than 8 patterns in Dev Tools section ($pattern_count found, need 8+)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
