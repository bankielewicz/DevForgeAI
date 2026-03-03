#!/usr/bin/env bash
# STORY-385 AC#5: Output Integrated into Research Documentation
# Validates:
#   - Output exists as either:
#     (a) New section appended to research artifact (if combined < 2000 lines), OR
#     (b) Companion document at devforgeai/specs/research/new-capability-opportunities.md
#         with cross-reference link added to the research artifact
#   - If companion document: research artifact contains cross-reference to it
#   - If appended: combined document stays under 2000 lines

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

# ---------------------------------------------------------------------------
# Test 1: Determine integration strategy (appended vs companion document)
# ---------------------------------------------------------------------------
companion_exists=false
appended=false

if [ -f "$DOC" ]; then
  companion_exists=true
  pass "Companion document exists at $DOC"
else
  # Check if capabilities are appended to research artifact
  if [ -f "$RESEARCH_ARTIFACT" ]; then
    if grep -qiE "^## (New Capabilit|Capability Opportunit)" "$RESEARCH_ARTIFACT" 2>/dev/null; then
      appended=true
      pass "New Capabilities section found appended to research artifact"
    else
      fail "Neither companion document nor appended section found"
      print_results
    fi
  else
    fail "Neither companion document nor research artifact exists"
    print_results
  fi
fi

# ---------------------------------------------------------------------------
# Test 2: If companion document - research artifact has cross-reference
# ---------------------------------------------------------------------------
if [ "$companion_exists" = true ]; then
  if [ -f "$RESEARCH_ARTIFACT" ]; then
    if grep -qiE "(new-capability-opportunities|new.capability.opportunities|companion.document)" "$RESEARCH_ARTIFACT" 2>/dev/null; then
      pass "Research artifact contains cross-reference to companion document"
    else
      fail "Research artifact missing cross-reference to companion document"
    fi
  else
    fail "Research artifact not found - cannot verify cross-reference"
  fi
fi

# ---------------------------------------------------------------------------
# Test 3: If appended - combined document stays under 2000 lines
# ---------------------------------------------------------------------------
if [ "$appended" = true ]; then
  total_lines=$(wc -l < "$RESEARCH_ARTIFACT")
  if [ "$total_lines" -lt 2000 ]; then
    pass "Combined document is under 2000 lines ($total_lines lines)"
  else
    fail "Combined document exceeds 2000 lines ($total_lines lines)"
  fi
fi

# ---------------------------------------------------------------------------
# Test 4: If companion document - it is a valid standalone document
# ---------------------------------------------------------------------------
if [ "$companion_exists" = true ]; then
  # Check it has a title header
  if grep -qE "^# " "$DOC" 2>/dev/null; then
    pass "Companion document has a title header"
  else
    fail "Companion document missing title header"
  fi

  # Check it has meaningful content (not empty/stub)
  line_count=$(wc -l < "$DOC")
  if [ "$line_count" -ge 50 ]; then
    pass "Companion document has substantial content ($line_count lines)"
  else
    fail "Companion document appears too short ($line_count lines, expected 50+)"
  fi
fi

# ---------------------------------------------------------------------------
# Test 5: Output document is valid Markdown (NFR-003)
# Check for unclosed code blocks
# ---------------------------------------------------------------------------
target_doc="$DOC"
if [ "$appended" = true ]; then
  target_doc="$RESEARCH_ARTIFACT"
fi

if [ -f "$target_doc" ]; then
  # Count opening and closing code block fences
  fence_count=$(grep -c '```' "$target_doc" 2>/dev/null || echo "0")
  remainder=$((fence_count % 2))
  if [ "$remainder" -eq 0 ]; then
    pass "All code block fences are properly paired ($fence_count fences)"
  else
    fail "Unclosed code block detected ($fence_count fences - odd number)"
  fi
fi

# ---------------------------------------------------------------------------
# Test 6: Document location is within devforgeai/specs/research/ (source-tree.md)
# ---------------------------------------------------------------------------
if [ "$companion_exists" = true ]; then
  doc_dir=$(dirname "$DOC")
  expected_dir="$PROJECT_ROOT/devforgeai/specs/research"
  if [ "$doc_dir" = "$expected_dir" ]; then
    pass "Document is in correct directory (devforgeai/specs/research/)"
  else
    fail "Document is in wrong directory: $doc_dir (expected: $expected_dir)"
  fi
fi

print_results
