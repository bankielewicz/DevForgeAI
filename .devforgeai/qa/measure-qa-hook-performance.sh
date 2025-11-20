#!/bin/bash

# STORY-024: Performance Measurement Script
# Measures Phase 4 hook integration overhead for /qa command
# Target: <5 seconds overhead

set -e

echo "======================================================"
echo "  STORY-024: QA Hook Integration Performance Test"
echo "======================================================"
echo ""

# Configuration
RUNS=20
STORY_ID="${1:-STORY-014}"  # Default to STORY-014 if not specified
RESULTS_FILE=".devforgeai/qa/performance-results-$(date +%Y-%m-%d-%H%M%S).txt"

echo "Configuration:"
echo "  - Story ID: $STORY_ID"
echo "  - Number of runs: $RUNS"
echo "  - Results file: $RESULTS_FILE"
echo ""

# Verify story exists
if [ ! -f ".ai_docs/Stories/${STORY_ID}"*.story.md ]; then
  echo "ERROR: Story file not found for $STORY_ID"
  echo "Usage: $0 [STORY-ID]"
  echo "Example: $0 STORY-014"
  exit 1
fi

# Create results file
echo "STORY-024 Performance Measurement Results" > "$RESULTS_FILE"
echo "Date: $(date)" >> "$RESULTS_FILE"
echo "Story: $STORY_ID" >> "$RESULTS_FILE"
echo "Runs: $RUNS" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Function to measure /qa execution time
measure_qa_time() {
  local run_num=$1

  echo -n "Run $run_num/$RUNS: "

  # Measure total /qa execution time
  START_TIME=$(date +%s.%N)

  # Run /qa command (suppress output to focus on timing)
  # Note: This is a simulation - actual /qa would be run via Claude Code Terminal
  # For now, we measure the hook check/invoke CLIs directly

  # Simulate Phase 4 execution
  devforgeai check-hooks --operation=qa --status=failed > /dev/null 2>&1 || true
  CHECK_EXIT=$?

  if [ $CHECK_EXIT -eq 0 ]; then
    devforgeai invoke-hooks --operation=qa --story=$STORY_ID --context="Test context" > /dev/null 2>&1 || true
  fi

  END_TIME=$(date +%s.%N)

  # Calculate duration
  DURATION=$(echo "$END_TIME - $START_TIME" | bc)

  echo "${DURATION}s"
  echo "$DURATION" >> "$RESULTS_FILE"

  # Return duration for averaging
  echo "$DURATION"
}

echo "Starting performance measurements..."
echo ""

# Array to store durations
declare -a durations

# Run measurements
for i in $(seq 1 $RUNS); do
  duration=$(measure_qa_time $i)
  durations+=("$duration")

  # Small delay between runs
  sleep 0.5
done

echo ""
echo "Calculating statistics..."
echo ""

# Calculate statistics
total=0
min=999999
max=0

for duration in "${durations[@]}"; do
  total=$(echo "$total + $duration" | bc)

  # Update min
  if (( $(echo "$duration < $min" | bc -l) )); then
    min=$duration
  fi

  # Update max
  if (( $(echo "$duration > $max" | bc -l) )); then
    max=$duration
  fi
done

average=$(echo "scale=3; $total / $RUNS" | bc)

# Write statistics to results file
echo "" >> "$RESULTS_FILE"
echo "Statistics:" >> "$RESULTS_FILE"
echo "  Min: ${min}s" >> "$RESULTS_FILE"
echo "  Max: ${max}s" >> "$RESULTS_FILE"
echo "  Average: ${average}s" >> "$RESULTS_FILE"
echo "  Total runs: $RUNS" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Determine pass/fail
TARGET=5.0
if (( $(echo "$average < $TARGET" | bc -l) )); then
  result="PASS"
  echo "Result: PASS ✅" >> "$RESULTS_FILE"
else
  result="FAIL"
  echo "Result: FAIL ❌ (exceeded $TARGET second target)" >> "$RESULTS_FILE"
fi

# Display summary
echo "======================================================"
echo "  Performance Test Results"
echo "======================================================"
echo ""
echo "Measurements:"
echo "  - Minimum time: ${min}s"
echo "  - Maximum time: ${max}s"
echo "  - Average time: ${average}s"
echo ""
echo "Target: <${TARGET}s per hook invocation"
echo ""

if [ "$result" = "PASS" ]; then
  echo "✅ PASS: Average ${average}s < ${TARGET}s target"
  echo ""
  echo "NFR-P1 (Performance) requirement met!"
else
  echo "❌ FAIL: Average ${average}s ≥ ${TARGET}s target"
  echo ""
  echo "Performance optimization needed to meet NFR-P1 requirement."
fi

echo ""
echo "Detailed results saved to: $RESULTS_FILE"
echo ""

# Exit with appropriate code
if [ "$result" = "PASS" ]; then
  exit 0
else
  exit 1
fi
