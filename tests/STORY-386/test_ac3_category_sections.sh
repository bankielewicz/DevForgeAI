#!/usr/bin/env bash
# STORY-386 AC#3: Optional Sections Defined Per Agent Category
# Verifies 4 categories exist, each with 3 optional sections.
# TDD RED phase - this test MUST FAIL until the template is created.

set -euo pipefail

TEMPLATE="src/claude/agents/agent-generator/references/canonical-agent-template.md"
ERRORS=0

if [[ ! -f "$TEMPLATE" ]]; then
  echo "FAIL: Template file does not exist at $TEMPLATE"
  exit 1
fi

# 4 agent categories
CATEGORIES=(
  "Validator"
  "Implementor"
  "Analyzer"
  "Formatter"
)

for cat in "${CATEGORIES[@]}"; do
  if ! grep -qi "$cat" "$TEMPLATE"; then
    echo "FAIL: Missing agent category: $cat"
    ERRORS=$((ERRORS + 1))
  fi
done

# Validator optional sections
VALIDATOR_SECTIONS=("Validation Rules" "Severity Classification" "Pass/Fail Criteria")
for sec in "${VALIDATOR_SECTIONS[@]}"; do
  if ! grep -qi "$sec" "$TEMPLATE"; then
    echo "FAIL: Validator category missing optional section: $sec"
    ERRORS=$((ERRORS + 1))
  fi
done

# Implementor optional sections
IMPLEMENTOR_SECTIONS=("Implementation Patterns" "Code Generation Rules" "Test Requirements")
for sec in "${IMPLEMENTOR_SECTIONS[@]}"; do
  if ! grep -qi "$sec" "$TEMPLATE"; then
    echo "FAIL: Implementor category missing optional section: $sec"
    ERRORS=$((ERRORS + 1))
  fi
done

# Analyzer optional sections
ANALYZER_SECTIONS=("Analysis Metrics" "Scoring Rubrics" "Threshold Definitions")
for sec in "${ANALYZER_SECTIONS[@]}"; do
  if ! grep -qi "$sec" "$TEMPLATE"; then
    echo "FAIL: Analyzer category missing optional section: $sec"
    ERRORS=$((ERRORS + 1))
  fi
done

# Formatter optional sections
FORMATTER_SECTIONS=("Output Templates" "Data Transformation Rules" "Display Modes")
for sec in "${FORMATTER_SECTIONS[@]}"; do
  if ! grep -qi "$sec" "$TEMPLATE"; then
    echo "FAIL: Formatter category missing optional section: $sec"
    ERRORS=$((ERRORS + 1))
  fi
done

# Decision table mapping agent function to category
if ! grep -qi "decision table\|decision matrix\|category mapping" "$TEMPLATE"; then
  echo "FAIL: Missing decision table mapping agent function to category"
  ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "FAIL: $ERRORS error(s) found in AC#3 validation"
  exit 1
fi

echo "PASS: All 4 categories defined with 3 optional sections each"
exit 0
