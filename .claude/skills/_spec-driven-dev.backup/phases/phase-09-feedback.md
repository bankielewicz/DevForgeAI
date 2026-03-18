# Phase 09: Feedback Hook Integration

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=08 --to=09
# Exit 0: proceed | Exit 1: Phase 08 incomplete
```

## Contract

PURPOSE: Collect workflow observations, invoke AI analysis, and store framework improvement recommendations.
REQUIRED SUBAGENTS: framework-analyst
REQUIRED ARTIFACTS: `devforgeai/feedback/ai-analysis/${STORY_ID}/consolidated-analysis.json`
STEP COUNT: 8 mandatory steps

**NON-BLOCKING:** Hook/analysis failures do NOT prevent workflow completion. Failures are logged and workflow continues to Phase 10.

---

## Mandatory Steps

### Step 1: Check Hooks Status

EXECUTE: Check if user feedback hooks are enabled.
```bash
source .venv/bin/activate && devforgeai-validate check-hooks --operation=dev --status=success --type=user
```
VERIFY: Exit code recorded.
```
Exit 0: Hooks enabled — proceed to Step 2
Exit 1: Hooks disabled — skip Step 2, proceed to Step 3
```

### Step 2: Invoke User Feedback Hooks (CONDITIONAL)

EXECUTE: If hooks enabled (Step 1 exit 0), invoke them.
```bash
source .venv/bin/activate && devforgeai-validate invoke-hooks --operation=dev --story=${STORY_ID} --type=user
```
VERIFY: Hook invocation completed (exit code logged). Non-blocking on failure.

### Step 3: Read Observation Files from Disk

EXECUTE: Collect all observation files written during phases 02-08.
```
Glob(pattern="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-*-observations.json")
# Read each file and aggregate observations
```
VERIFY: Observations loaded. Display count.
```
IF no observation files found:
  # Fallback: Read from phase-state.json (backward compatibility)
  Read(file_path="devforgeai/workflows/${STORY_ID}-phase-state.json")
```

### Step 4: Consolidate Observations

EXECUTE: Merge all phase observations into a single consolidated list.
```
# Deduplicate, sort by severity (high > medium > low)
# Count by category: friction, success, pattern, gap, idea, bug
```
VERIFY: Consolidated list is non-empty (warning if empty, not blocking).

### Step 5: Invoke Framework Analyst

EXECUTE: Delegate AI analysis to framework-analyst subagent.
```
Task(
  subagent_type="framework-analyst",
  prompt="Analyze ${STORY_ID} workflow execution and generate framework improvement recommendations.

  INPUT:
  - Story ID: ${STORY_ID}
  - Workflow Type: dev
  - Observation Directory: devforgeai/feedback/ai-analysis/${STORY_ID}/
  - Consolidated Observations: ${CONSOLIDATED_OBSERVATIONS}
  - Observation Count: ${COUNT}

  INSTRUCTIONS:
  1. Read each file mentioned in observations
  2. Check recommendations-queue.json for duplicates
  3. Check recent git commits for already-implemented items
  4. Expand terse observations into structured recommendations
  5. Return ONLY valid JSON matching the required schema

  Return ONLY valid JSON - no markdown, no explanation text."
)
```
VERIFY: Task result returned as JSON.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=09 --subagent=framework-analyst`

### Step 6: Validate Subagent Output (BLOCKING for storage, non-blocking for workflow)

EXECUTE: Validate the framework-analyst output against quality gates.
```
# 6.1 JSON Schema Validation: Parse as JSON
# 6.2 Aspirational Language Check: FAIL if "could", "might", "consider", "should explore", "potentially"
# 6.3 Evidence Requirement: Each item must have non-empty evidence + specific file paths
# 6.4 Effort Estimate Check: Valid values: "15 min", "30 min", "45 min", "1 hour", "2 hours", "4 hours"
# 6.5 Feasibility Check: Each recommendation must have feasible_in_claude_code: true
```
VERIFY: All 5 validation checks pass. If any fail: log error, do NOT store, continue to Step 8.

### Step 7: Apply Merit Filter

EXECUTE: Filter validated recommendations against existing queue.
```
Read(file_path="devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json")
# Check for >80% description similarity (duplicates)
# Check if affected files modified in last 7 days with related commit
# PASS or FILTER each recommendation
```
VERIFY: Merit filter results logged.

### Step 8: Write AI Analysis Report

EXECUTE: Store validated and filtered results to disk.
```
Write(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/consolidated-analysis.json",
  content=<consolidated analysis with recommendations, validation results, merit filter results>)

# If HIGH priority recommendations exist, append to aggregated queue:
Read + Write(file_path="devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json")
```
VERIFY: consolidated-analysis.json exists.
```
Glob(pattern="devforgeai/feedback/ai-analysis/${STORY_ID}/consolidated-analysis.json")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=09 --checkpoint-passed
# Exit 0: always succeeds (non-blocking phase) | Proceed to Phase 10
```
