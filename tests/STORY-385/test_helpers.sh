#!/usr/bin/env bash
# STORY-385 Shared Test Helpers
# Provides: PROJECT_ROOT, DOC, RESEARCH_ARTIFACT, pass/fail counters,
# pass()/fail()/print_results()/require_doc() functions.

set -euo pipefail

# --- Project and Document Paths ---
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
DOC="$PROJECT_ROOT/devforgeai/specs/research/new-capability-opportunities.md"
RESEARCH_ARTIFACT="$PROJECT_ROOT/devforgeai/specs/research/prompt-engineering-patterns.md"

# --- Test Counters ---
PASS=0
FAIL=0

# --- Test Result Functions ---
pass() { echo "PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }

# --- Print final results and exit with appropriate code ---
print_results() {
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  [ "$FAIL" -eq 0 ] && exit 0 || exit 1
}

# --- Require document exists (early exit if missing) ---
require_doc() {
  local label="${1:-New capabilities document}"
  if [ -f "$DOC" ]; then
    pass "$label exists"
  else
    fail "$label does not exist at $DOC"
    echo ""
    echo "Results: $PASS passed, $FAIL failed"
    exit 1
  fi
}

# --- Assert count meets minimum threshold ---
# Usage: assert_min_count <actual> <minimum> <pass_msg> <fail_msg>
# Messages may use {actual} and {min} placeholders.
assert_min_count() {
  local actual="$1" minimum="$2" pass_msg="$3" fail_msg="$4"
  pass_msg="${pass_msg//\{actual\}/$actual}"
  pass_msg="${pass_msg//\{min\}/$minimum}"
  fail_msg="${fail_msg//\{actual\}/$actual}"
  fail_msg="${fail_msg//\{min\}/$minimum}"
  if [ "$actual" -ge "$minimum" ]; then
    pass "$pass_msg"
  else
    fail "$fail_msg"
  fi
}

# --- Extract a ## section from DOC into stdout ---
# Usage: extract_section "Section Name"
# Returns content from "## Section Name" up to next "## " header (exclusive).
extract_section() {
  local section_name="$1"
  local content
  content=$(sed -n "/^## ${section_name}/,/^## [^#]/p" "$DOC" 2>/dev/null | head -n -1)
  if [ -z "$content" ]; then
    content=$(sed -n "/^## ${section_name}/,\$p" "$DOC" 2>/dev/null)
  fi
  echo "$content"
}

# --- Assert a ## section header exists in DOC ---
# Usage: assert_section_exists "Section Name"
assert_section_exists() {
  local section_name="$1"
  if grep -qE "^## ${section_name}" "$DOC" 2>/dev/null; then
    pass "${section_name} section found"
  else
    fail "${section_name} section not found"
  fi
}

# --- Count opportunity entries ---
# Opportunities are identified by ### headers containing an opportunity name
# or by a structured pattern like "### N. Opportunity Name" or "### Opportunity: Name"
count_opportunities() {
  local count
  count=$(grep -cE "^### " "$DOC" 2>/dev/null || echo "0")
  echo "$count"
}
