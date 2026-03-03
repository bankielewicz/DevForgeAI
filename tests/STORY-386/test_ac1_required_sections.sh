#!/usr/bin/env bash
# STORY-386 AC#1: Template Defines All Required Sections
# Verifies the canonical template contains all 10 required section headings.
# TDD RED phase - this test MUST FAIL until the template is created.

set -euo pipefail

TEMPLATE="src/claude/agents/agent-generator/references/canonical-agent-template.md"
ERRORS=0

# Pre-check: file must exist
if [[ ! -f "$TEMPLATE" ]]; then
  echo "FAIL: Template file does not exist at $TEMPLATE"
  exit 1
fi

# 10 required sections (order-independent grep)
SECTIONS=(
  "YAML Frontmatter"
  "Title"
  "Purpose"
  "When Invoked"
  "Input/Output Specification"
  "Constraints and Boundaries"
  "Workflow"
  "Success Criteria"
  "Output Format"
  "Examples"
)

for section in "${SECTIONS[@]}"; do
  if ! grep -qi "$section" "$TEMPLATE"; then
    echo "FAIL: Missing required section heading: $section"
    ERRORS=$((ERRORS + 1))
  fi
done

# Each section should have a specification block with Purpose and Format
for section in "${SECTIONS[@]}"; do
  # Check for Purpose subsection within the document
  if ! grep -qi "purpose" "$TEMPLATE"; then
    echo "FAIL: No 'Purpose' subsection found for section: $section"
    ERRORS=$((ERRORS + 1))
    break
  fi
done

if [[ $ERRORS -gt 0 ]]; then
  echo "FAIL: $ERRORS error(s) found in AC#1 validation"
  exit 1
fi

echo "PASS: All 10 required sections present"
exit 0
