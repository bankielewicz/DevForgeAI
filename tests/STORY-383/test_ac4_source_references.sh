#!/usr/bin/env bash
# STORY-383 AC#4: Source References Include Repo Name and Specific File Path
# Validates each pattern cites the repo directory name and a specific file path
# within that repo (e.g., "claude-code-security-review", "claudecode/prompts.py").
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
if [ ! -f "$DOC" ]; then
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Research document exists"

# Test 2: Dev Tools section exists
if ! grep -q "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null; then
  fail "Dev Tools and Domain Patterns section not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Dev Tools and Domain Patterns section found"

# Extract Dev Tools section content
dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$dev_tools_section" ]; then
  dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,$p' "$DOC" 2>/dev/null)
fi

# The 8 repos that must appear in source references
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

# Test 3: Source lines reference repo directory names
source_lines=$(echo "$dev_tools_section" | grep -E "^\*\*Source\*\*:" 2>/dev/null || true)
source_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Source\*\*:" 2>/dev/null || echo "0")

repos_in_sources=0
for repo in "${REPOS[@]}"; do
  repo_in_source=$(echo "$source_lines" | grep -c "$repo" 2>/dev/null || echo "0")
  if [ "$repo_in_source" -ge 1 ]; then
    repos_in_sources=$((repos_in_sources + 1))
    pass "Repo '$repo' found in Source references"
  else
    fail "Repo '$repo' not found in any Source reference"
  fi
done

# Test 11: All 8 repos appear in source references
if [ "$repos_in_sources" -ge 8 ]; then
  pass "All 8 repos have Source references ($repos_in_sources found)"
else
  fail "Not all 8 repos in Source references ($repos_in_sources of 8 found)"
fi

# Test 12: Source lines contain specific file paths (with / separator indicating path)
sources_with_paths=$(echo "$dev_tools_section" | grep -E "^\*\*Source\*\*:" 2>/dev/null | grep -c "/" || echo "0")
if [ "$sources_with_paths" -ge "$source_count" ] && [ "$source_count" -gt 0 ]; then
  pass "All source references include file paths ($sources_with_paths of $source_count have paths)"
else
  fail "Not all source references include file paths ($sources_with_paths of $source_count)"
fi

# Test 13: Source lines include file extensions for specificity
sources_with_extensions=$(echo "$dev_tools_section" | grep -E "^\*\*Source\*\*:" 2>/dev/null | grep -cE "\.(py|md|yml|yaml|json|sh|js|ts|toml)" || echo "0")
if [ "$sources_with_extensions" -ge 1 ]; then
  pass "Source references include file extensions ($sources_with_extensions with extensions)"
else
  fail "No source references include file extensions"
fi

# Test 14: No secrets in Dev Tools section (NFR-004)
secret_count=$(echo "$dev_tools_section" | grep -cE "(api_key|password|token|secret|credential)\s*[=:]\s*['\"]" 2>/dev/null | tr -d '\n' || echo "0")
secret_count=${secret_count:-0}
if [ "$secret_count" -eq 0 ]; then
  pass "No secrets or credentials found in Dev Tools section"
else
  fail "$secret_count potential secret/credential patterns found"
fi

# Test 15: No PHI in Dev Tools section (BR-008)
phi_count=$(echo "$dev_tools_section" | grep -ciE "(patient_id|SSN|MRN|date_of_birth|medical_record)" 2>/dev/null | tr -d '\n' || echo "0")
phi_count=${phi_count:-0}
if [ "$phi_count" -eq 0 ]; then
  pass "No PHI patterns found in Dev Tools section"
else
  fail "$phi_count potential PHI patterns found"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
