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
STEP COUNT: 9 mandatory steps

**NON-BLOCKING:** Hook/analysis failures do NOT prevent workflow completion. Failures are logged and workflow continues to Phase 10.

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-feedback/references/srfd-format.md")
```

IF any Read fails: HALT -- "Phase 09 reference files not loaded."

---

## Mandatory Steps

### Step 1: Check Hooks Status

EXECUTE: Check if user feedback hooks are enabled.
```bash
devforgeai-validate check-hooks --operation=dev --status=success --type=user
```
VERIFY: Exit code recorded.
```
Exit 0: Hooks enabled — proceed to Step 2
Exit 1: Hooks disabled — skip Step 2, proceed to Step 3
```

### Step 2: Invoke User Feedback Hooks (CONDITIONAL)

EXECUTE: If hooks enabled (Step 1 exit 0), invoke them.
```bash
devforgeai-validate invoke-hooks --operation=dev --story=${STORY_ID} --type=user
```
VERIFY: Hook invocation completed (exit code logged). Non-blocking on failure.

### Step 3: Aggregate Observations from All Phases

EXECUTE: Glob, merge, deduplicate, and sort all phase observation files via CLI.
```bash
devforgeai-validate aggregate-observations --story=${STORY_ID} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code 0 = consolidated file written. Display observation count and category breakdown.
```
IF exit code == 1: No observation files found — continue with empty observations (non-blocking).
```

### Step 4: Invoke Framework Analyst (was Step 5)

EXECUTE: Delegate AI analysis to framework-analyst subagent.
```
Task(
  subagent_type="framework-analyst",
  prompt="Analyze ${STORY_ID} workflow execution and generate framework improvement recommendations.

  INPUT:
  - Story ID: ${STORY_ID}
  - Story File: ${STORY_FILE}
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

### Step 5: Validate Recommendations & Apply Merit Filter (was Steps 6+7)

EXECUTE: Validate framework-analyst output (schema, aspirational language, evidence, effort, feasibility) and apply duplicate filter — all via CLI.
```bash
devforgeai-validate validate-recommendations --input=${FRAMEWORK_ANALYST_OUTPUT_FILE} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code 0 = all recommendations valid. Exit code 1 = some failed validation.
```
IF exit code == 1: log validation failures, do NOT store invalid items, continue to Step 6.
```

### Step 6: Write AI Analysis Report (was Step 8)

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

### Step 7: Write SRFD Document

EXECUTE: Write the SRFD markdown file using enriched data from framework-analyst Step 8.

Reference the SRFD section structure defined in `src/claude/skills/spec-driven-feedback/references/srfd-format.md` to populate all required sections.

```
Write(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/SRFD-${STORY_ID}-${YYYY-MM-DD}.md",
  content=<SRFD document with sections populated from SRFD-enriched analysis data>)
```

Populate SRFD sections from the enriched framework-analyst output:
- **Session Summary**: Story ID, workflow type, observation count
- **Metadata**: story_id, workflow_type, analysis_date, epic, sprint
- **Constraint analysis**: Context file effectiveness from constraint_citations
- **Recommendations**: Expanded recommendation entries with line number references
- **Patterns Observed**: patterns_observed array
- **Anti-Patterns Detected**: anti_patterns_detected array

VERIFY: SRFD file exists at `devforgeai/feedback/ai-analysis/${STORY_ID}/SRFD-${STORY_ID}-${YYYY-MM-DD}.md`.
```
Glob(pattern="devforgeai/feedback/ai-analysis/${STORY_ID}/SRFD-*.md")
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=09 --step=7`

### Step 8: Manage SRFD Index

EXECUTE: If srfd-index.json does not exist, create it from the template in srfd-format.md.

```
IF NOT exists("devforgeai/feedback/ai-analysis/aggregated/srfd-index.json"):
  Read(file_path=".claude/skills/spec-driven-feedback/references/srfd-format.md")
  Extract the empty srfd-index.json template from the JSON code block
  Write(file_path="devforgeai/feedback/ai-analysis/aggregated/srfd-index.json",
    content=<template from srfd-format.md>)
```

Append a new SRFD index entry with the following 8 required fields:

```json
{
  "id": "SRFD-${STORY_ID}-${YYYY-MM-DD}",
  "path": "devforgeai/feedback/ai-analysis/${STORY_ID}/SRFD-${STORY_ID}-${YYYY-MM-DD}.md",
  "source_story": "${STORY_ID}",
  "workflow": "dev",
  "generated": "${YYYY-MM-DD}",
  "recommendation_count": <total recommendations>,
  "open_count": <recommendations not yet implemented>,
  "implemented_count": <recommendations already implemented>
}
```

Add this entry to the srfd-index.json `entries` array.

**Duplicate Detection:** If an existing SRFD index entry has the same source_story and generated date, update that entry instead of appending a duplicate. This prevents duplicate SRFD index entries for the same story run on the same date -- update rather than append when an existing entry matches.

VERIFY: srfd-index.json contains entry for current SRFD.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=09 --step=8`

### Step 9: Add Queue Backlinks

EXECUTE: For each recommendation added to recommendations-queue.json, add a source_srfd backlink field with value `${STORY_ID}/SRFD-${STORY_ID}-${YYYY-MM-DD}.md`.

```
FOR each recommendation in queue:
  Set recommendation.source_srfd = "${STORY_ID}/SRFD-${STORY_ID}-${YYYY-MM-DD}.md"
```

This backlink connects each queue recommendation to its source SRFD document, enabling traceability from the recommendation queue back to the analysis that produced it.

VERIFY: Each recommendation has a source_srfd field matching the SRFD path.
```
Grep(pattern="source_srfd", path="devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json")
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=09 --step=9`

---

### Final Step (conditional): End-of-run framework-friction review (#620)

EXECUTE (toggle-gated, default-OFF): read the friction-reporting toggle —
`devforgeai-validate friction-config --get enabled --project-root=${PROJECT_ROOT}`. If it is not
`true`, SKIP this step (friction reporting is opt-in). When `true`, run the verbatim friction
prompt below (`${ID}` is this workflow's id — here `${STORY_ID}`). Honest determinism boundary:
the `pre-friction-report-gate.sh` gate forces exactly ONE verdict artifact to exist; it does NOT
make the friction judgment deterministic — that judgment is **NOT-DETERMINISTIC** (the gate can be
satisfied with `{"friction":"none"}`). The deterministic teeth are the toggle, the gate's
force-one-emission, the enforcement-hook auto-append, and the mandatory remote dedup.

```
Role. You are the workflow orchestrator performing the end-of-run framework-friction review for DevForgeAI. Decide whether this run surfaced any framework defect or missing enforcement worth filing, and if so file it correctly and non-redundantly.
Scope. Only friction caused by the framework itself: a skill/phase/subagent that failed to guide a required action without a user reminder (e.g. not being prompted to create a worktree), a gate that fired wrongly or not at all, a phase file that contradicts a hook, prose an LLM predictably skipped, or a CLI/hook defect. Exclude: your own mistakes, the bug this run was fixing, and environment/network issues.
Inputs. (1) devforgeai/feedback/ai-analysis/${ID}/consolidated-analysis.json (captured observations). (2) Your session memory of where the workflow under- or mis-guided you.
Grounding contract. Every candidate must cite verifiable evidence: an exact file:line, the exact command/tool-call + path, and/or an exit code. No claim from memory. Drop any candidate that is not grounded. Use no aspirational language; describe only what IS broken and what WILL change.
Duplicate check (remote, mandatory). For each grounded candidate search open AND closed issues before filing: gh issue list --repo bankielewicz/DevForgeAI --state all --search "<3-5 keywords>" and gh search issues "<phrase>" --repo bankielewicz/DevForgeAI. If any result is the same defect/enhancement, do not file; record its number as the duplicate.
Decision gate. File via /create-incident ONLY when ALL hold: grounded, non-duplicate, scoped to one concrete change, non-aspirational. Otherwise do not file.
Filing. For each qualifying item: /create-incident "<one-sentence observation>" --type=<bug|enhancement> --work="<originating ID> -> <plan path> -> PR #<n>" --related="<chain>". Keep the provenance chain intact end-to-end.
Output (mandatory artifact). Write devforgeai/feedback/ai-analysis/${ID}/friction-summary.json: either {"friction":"filed","issues":[...],"duplicates_skipped":[...]} or {"friction":"none","rationale":"<one sentence>"}. The friction gate requires this artifact; the run cannot complete without it.
Few-shot (file it). "spec-sprint Phase 03 created the worktree but the phase file never told me to set CLAUDE_PROJECT_DIR, so the first gate ran against main (evidence: phase-03-worktree-materialize.md:35; gate exit 2)." -> grounded, scoped: file as bug.
Few-shot (do NOT file). "The board did not auto-update" when that IS the bug this run fixed -> exclude (own-scope). "Tests felt slow" with no file/command/exit evidence -> exclude (ungrounded).
```

VERIFY: `devforgeai/feedback/ai-analysis/${ID}/friction-summary.json` exists with one of the two
shapes — `{"friction":"filed","issues":[...],"duplicates_skipped":[...]}` or
`{"friction":"none","rationale":"..."}`. `duplicates_skipped` records any remote duplicate found by
the mandatory remote dedup probe. The `pre-friction-report-gate.sh` gate reads this artifact at the
final-phase `phase-complete`.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=09 --checkpoint-passed
# Exit 0: always succeeds (non-blocking phase) | Proceed to Phase 10
```

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
