#!/bin/bash
# Test: AC#10 - 6-Step Workflow Structure
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: File has exactly 6 steps (Step 1 through Step 6)
STEP_COUNT=$(grep -cE "^##? Step [1-9]|^### Step [1-9]|\*\*Step [1-9]\*\*" "$FILE" 2>/dev/null || echo 0)
if [ "$STEP_COUNT" -eq 6 ]; then
  echo "PASS: File has exactly 6 steps ($STEP_COUNT found)"
  ((PASS++))
else
  echo "FAIL: File has $STEP_COUNT steps (exactly 6 required)"
  ((FAIL++))
fi

# Test 2: Each step has an Inputs section
INPUTS_COUNT=$(grep -ciE "inputs:" "$FILE" 2>/dev/null || echo 0)
if [ "$INPUTS_COUNT" -ge 6 ]; then
  echo "PASS: File has $INPUTS_COUNT Inputs sections (>= 6 required)"
  ((PASS++))
else
  echo "FAIL: File has $INPUTS_COUNT Inputs sections (>= 6 required)"
  ((FAIL++))
fi

# Test 3: Each step has an Actions section
ACTIONS_COUNT=$(grep -ciE "actions:" "$FILE" 2>/dev/null || echo 0)
if [ "$ACTIONS_COUNT" -ge 6 ]; then
  echo "PASS: File has $ACTIONS_COUNT Actions sections (>= 6 required)"
  ((PASS++))
else
  echo "FAIL: File has $ACTIONS_COUNT Actions sections (>= 6 required)"
  ((FAIL++))
fi

# Test 4: Each step has a Tools section
TOOLS_COUNT=$(grep -ciE "tools:" "$FILE" 2>/dev/null || echo 0)
if [ "$TOOLS_COUNT" -ge 6 ]; then
  echo "PASS: File has $TOOLS_COUNT Tools sections (>= 6 required)"
  ((PASS++))
else
  echo "FAIL: File has $TOOLS_COUNT Tools sections (>= 6 required)"
  ((FAIL++))
fi

# Test 5: Each step has an Outputs section
OUTPUTS_COUNT=$(grep -ciE "outputs:" "$FILE" 2>/dev/null || echo 0)
if [ "$OUTPUTS_COUNT" -ge 6 ]; then
  echo "PASS: File has $OUTPUTS_COUNT Outputs sections (>= 6 required)"
  ((PASS++))
else
  echo "FAIL: File has $OUTPUTS_COUNT Outputs sections (>= 6 required)"
  ((FAIL++))
fi

# Test 6: Step 1 is Detect Configuration Layers
if grep -qiE "Step 1.*[Dd]etect|Step 1.*[Cc]onfiguration" "$FILE" 2>/dev/null; then
  echo "PASS: Step 1 is 'Detect Configuration Layers'"
  ((PASS++))
else
  echo "FAIL: Step 1 is NOT 'Detect Configuration Layers'"
  ((FAIL++))
fi

# Test 7: Step 2 is Invoke alignment-auditor
if grep -qiE "Step 2.*[Ii]nvoke|Step 2.*alignment-auditor" "$FILE" 2>/dev/null; then
  echo "PASS: Step 2 is 'Invoke alignment-auditor'"
  ((PASS++))
else
  echo "FAIL: Step 2 is NOT 'Invoke alignment-auditor'"
  ((FAIL++))
fi

# Test 8: Step 3 is Process Contradictions
if grep -qiE "Step 3.*[Cc]ontradiction|Step 3.*[Pp]rocess" "$FILE" 2>/dev/null; then
  echo "PASS: Step 3 is 'Process Contradictions'"
  ((PASS++))
else
  echo "FAIL: Step 3 is NOT 'Process Contradictions'"
  ((FAIL++))
fi

# Test 9: Step 6 is Report
if grep -qiE "Step 6.*[Rr]eport|Step 6.*[Ss]ummary" "$FILE" 2>/dev/null; then
  echo "PASS: Step 6 is 'Report'"
  ((PASS++))
else
  echo "FAIL: Step 6 is NOT 'Report'"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
