#!/usr/bin/env bash
# STORY-382 AC#4: Patterns Include Source References with File Paths
# Validates each pattern cites: repository name (claude-cookbooks or claude-quickstarts),
# category/directory path, and specific filename.
#
# Expected: FAIL (cookbook/quickstart section does not exist yet - TDD Red phase)

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
DOC="$PROJECT_ROOT/devforgeai/specs/research/prompt-engineering-patterns.md"

PASS=0
FAIL=0

fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
pass() { echo "PASS: $1"; PASS=$((PASS + 1)); }

# Test 1: Document exists
if [ ! -f "$DOC" ]; then
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Research document exists"

# Test 2: Cookbook/quickstart section exists
if ! grep -q "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null; then
  fail "Cookbook and Quickstart Patterns section not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Cookbook and Quickstart Patterns section exists"

# Extract section content
section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$section_content" ]; then
  section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,$p' "$DOC" 2>/dev/null)
fi

# Test 3: Source references include repository name (claude-cookbooks or claude-quickstarts)
source_lines=$(echo "$section_content" | grep -E "^\*\*Source\*\*:" 2>/dev/null || true)
source_count=$(echo "$source_lines" | grep -c "." 2>/dev/null || echo "0")
sources_with_repo=$(echo "$source_lines" | grep -cE "(claude-cookbooks|claude-quickstarts)" 2>/dev/null || echo "0")

if [ "$source_count" -gt 0 ] && [ "$sources_with_repo" -ge "$source_count" ]; then
  pass "All source references include repository name ($sources_with_repo of $source_count)"
else
  fail "Not all source references include repository name ($sources_with_repo of $source_count)"
fi

# Test 4: Source references include category/directory path
sources_with_dir=$(echo "$source_lines" | grep -cE "[a-z_]+/" 2>/dev/null || echo "0")
if [ "$source_count" -gt 0 ] && [ "$sources_with_dir" -ge "$source_count" ]; then
  pass "All source references include directory path ($sources_with_dir of $source_count)"
else
  fail "Not all source references include directory path ($sources_with_dir of $source_count)"
fi

# Test 5: Source references include specific filename with extension
sources_with_file=$(echo "$source_lines" | grep -cE "\.(ipynb|md|py|js|ts)" 2>/dev/null || echo "0")
if [ "$source_count" -gt 0 ] && [ "$sources_with_file" -ge "$source_count" ]; then
  pass "All source references include specific filename ($sources_with_file of $source_count)"
else
  fail "Not all source references include specific filename ($sources_with_file of $source_count)"
fi

# Test 6: At least one source from claude-cookbooks
cookbooks_sources=$(echo "$source_lines" | grep -c "claude-cookbooks" 2>/dev/null || echo "0")
if [ "$cookbooks_sources" -ge 1 ]; then
  pass "At least one source from claude-cookbooks ($cookbooks_sources sources)"
else
  fail "No sources from claude-cookbooks repository"
fi

# Test 7: At least one source from claude-quickstarts
quickstarts_sources=$(echo "$source_lines" | grep -c "claude-quickstarts" 2>/dev/null || echo "0")
if [ "$quickstarts_sources" -ge 1 ]; then
  pass "At least one source from claude-quickstarts ($quickstarts_sources sources)"
else
  fail "No sources from claude-quickstarts repository"
fi

# Test 8: Source references contain 3 required parts (repo/directory/filename)
# Pattern: repo_name/directory_path/filename.ext
sources_complete=$(echo "$source_lines" | grep -cE "claude-(cookbooks|quickstarts)/[a-zA-Z0-9_/-]+/[a-zA-Z0-9_-]+\.(ipynb|md|py|js|ts)" 2>/dev/null || echo "0")
if [ "$source_count" -gt 0 ] && [ "$sources_complete" -ge "$source_count" ]; then
  pass "All source references contain 3 parts: repo/directory/filename ($sources_complete of $source_count)"
else
  fail "Not all sources have complete 3-part references ($sources_complete of $source_count)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
