# Phase 06: Cleanup

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=05 --to=06 --project-root=.
# Exit 0: proceed | Exit 1: Phase 05 incomplete
```

## Contract

| | |
|---|---|
| **PURPOSE** | Release locks, invoke feedback hooks, display execution summary, persist QA deliverables before merge/delete cleanup. |
| **REQUIRED SUBAGENTS** | none |
| **REQUIRED ARTIFACTS** | Execution summary displayed, feedback hooks invoked, QA deliverables committed |
| **STEP COUNT** | 6 mandatory steps + 1 conditional merge step |

## CLI Consolidation (OPT-003)

Steps 6.1, 6.2, 6.5, and 6.5.5 are deterministic and replaceable by one CLI:
```bash
devforgeai-validate qa-cleanup ${STORY_ID} --result="${overall_status}" --workflow=qa --project-root=. \
  --story-file="${STORY_FILE}" --mode="${MODE}" \
  --persist-deliverables --push --open-pr-if-missing --base="${pr_base}"
# Exit 0: cleanup complete (JSON with lock_released, hooks_invoked, markers_cleaned, deliverable_persistence)
# Exit 1: cleanup issue (gaps.json missing for FAILED result)
```

On exit 0, the orchestrator still MUST execute Steps 6.3 and 6.4 (execution summary requires LLM formatting). Extract cleanup status from JSON.

If CLI unavailable (exit 127) or fails, fall back to the manual steps below.

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-qa/references/phase-4-cleanup-workflow.md")
Read(file_path=".claude/skills/spec-driven-qa/references/feedback-hooks-workflow.md")
```

---

## Mandatory Steps

### Step 6.1: Release Lock File

EXECUTE: Delete the QA lock file acquired in Phase 01.
```
lock_file = "{story_paths.results_dir}/.qa-lock"
Glob(pattern=lock_file)
IF exists:
    Bash(command="rm {lock_file}")
    Display "Lock released for ${STORY_ID}"
ELSE:
    Display "Lock file not found (already released or not acquired)"
```
VERIFY: Lock file no longer exists.
```
Glob(pattern=lock_file)
IF still exists: Display "WARNING: Lock file removal failed"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.1 --project-root=.`

---

### Step 6.2: Invoke Feedback Hooks (Non-Blocking)

EXECUTE: Map QA result to hook status; invoke if available. Hook failures do NOT block QA completion.
```
IF overall_status == "PASSED":  STATUS = "success"
ELIF overall_status == "FAILED": STATUS = "failure"
ELSE:                            STATUS = "partial"

Bash(command="devforgeai-validate check-hooks --operation=qa --status=${STATUS} --project-root=. 2>&1")

IF exit_code == 0:
    Bash(command="devforgeai-validate invoke-hooks --operation=qa --story=${STORY_ID} --project-root=. 2>&1")
    Display "Feedback hooks: Invoked (status: ${STATUS})"
ELSE:
    Display "Feedback hooks: Not available or disabled"
# Non-blocking: continue regardless.
```
VERIFY: Hook check executed; invocation attempted if available; workflow continues regardless.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.2 --project-root=.`

---

### Step 6.3: Display Execution Summary (MANDATORY)

EXECUTE: Display phase-by-phase status — enforces visibility before completion.
```
Display:
"
======================================================================
                      QA EXECUTION SUMMARY
======================================================================
  Story: ${STORY_ID}
  Mode:  ${MODE}
----------------------------------------------------------------------
  PHASE EXECUTION STATUS:
  - [x] Phase 01: Setup           (Lock: YES, Type: ${DELIVERABLE_TYPE})
  - [x] Phase 02: Validation      (Traceability: {traceability_score}%)
  - [x] Phase 03: Diff Regression (Result: {phase_3_result})
  - [x] Phase 04: Analysis        (Validators: {success}/{total})
  - [x] Phase 05: Reporting       (Status: {overall_status})
  - [x] Phase 06: Cleanup         (Hooks: {hook_status})
----------------------------------------------------------------------
  Story File Updated: YES
  Result: {overall_status}
======================================================================
"
```

**Enforcement Logic:**
```
unchecked_count = count_unchecked_phases()

IF unchecked_count > 0:
    Display "WARNING: {unchecked_count} phases may have been skipped"
    AskUserQuestion: "Phases appear incomplete. Re-run skipped phases, Continue (NOT RECOMMENDED), or Abort?"
    IF "Re-run":  GOTO first skipped phase
    IF "Continue": Log warning
    IF "Abort":    HALT workflow

IF unchecked_count == 0:
    Display "All phases complete — no skipped steps detected"
```

VERIFY: Execution summary displayed; all phases marked complete (or user acknowledged incomplete state).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.3 --project-root=.`

---

### Step 6.4: Display Final QA Validation Summary

EXECUTE: Final formatted summary with metrics and next steps.
```
Display:
"
======================================================================
                    QA VALIDATION COMPLETE
======================================================================
  Story: ${STORY_ID}
  Mode:  ${MODE}
  Result: {overall_status}
----------------------------------------------------------------------
  Coverage:
    Business Logic: {biz}%    | Application: {app}%
    Infrastructure: {infra}% | Overall:     {overall}%
----------------------------------------------------------------------
  Violations: {critical} CRITICAL | {high} HIGH
              {medium} MEDIUM   | {low} LOW
----------------------------------------------------------------------
  Next Steps:
    [If PASSED] Ready for /release ${STORY_ID}
    [If FAILED] Run /dev ${STORY_ID} --fix for remediation
======================================================================
"
```
<!-- gaps.json verified in Phase 05 Step 5.3 — not re-checked here per optimization R-005 -->

VERIFY: Final summary displayed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.4 --project-root=.`

---

### Step 6.5: Marker Cleanup (PASSED Only)

EXECUTE: Preserve qa-phase-state.json as permanent audit trail. Delete legacy markers only if PASSED.
```
IF overall_status == "PASSED":
    # PRESERVE: qa-phase-state.json (permanent audit trail — DO NOT DELETE)
    Glob(pattern="devforgeai/workflows/${STORY_ID}-qa-phase-state.json")
    IF found: Display "qa-phase-state.json preserved as permanent audit trail"
    ELSE:     Display "WARNING: qa-phase-state.json not found — audit trail missing"

    # DELETE: legacy .qa-phase-N.marker files (superseded by qa-phase-state.json)
    Glob(pattern="devforgeai/qa/reports/${STORY_ID}/.qa-phase-*.marker")
    FOR each marker_file: Bash(command="rm {marker_file}")
    Display "Legacy .qa-phase-N.marker files cleaned up"
ELSE:
    Display "QA FAILED — all files retained for debugging and resume capability"
```
VERIFY: If PASSED, qa-phase-state.json preserved + legacy markers deleted. If FAILED, all files retained.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.5 --project-root=.`

---

### Step 6.5.5: Persist QA Deliverables (MANDATORY before merge/delete)

EXECUTE: Commit QA deliverables and the story status update before any Step 6.6 merge can delete the branch. The CLI stages the workflow-scoped QA report, QA recommendations, story file, and optional QA sidecars that exist.

```bash
devforgeai-validate qa-cleanup ${STORY_ID} --result="${overall_status}" --workflow=qa --project-root=. \
  --story-file="${STORY_FILE}" --mode="${MODE}" \
  --persist-deliverables --push --open-pr-if-missing --base="${pr_base}"
```

Behavior:
- If story frontmatter has non-null `pr_number`, the CLI commits and pushes to the existing PR branch and does not create a PR.
- If `pr_number` is null, the CLI commits to the current branch, reuses an existing open PR for that branch when one exists, and creates exactly one PR only when none exists.
- The CLI never uses `--no-verify`; git hooks remain active.

VERIFY: Required QA deliverables are clean before Step 6.6:
```bash
git status --porcelain -- \
  "devforgeai/qa/reports/${STORY_ID}-qa-report.md" \
  "devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md" \
  "${STORY_FILE}"
```
Expected output: empty. If any path is listed, HALT before Step 6.6.

RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.5.5 --project-root=.`

---

### Step 6.6: Squash-merge story PR [CONDITIONAL: QA Approved + open PR + pr_merged == false; requires Step 6.5.5 clean]

EXECUTE: Read `pr_number` and `pr_merged` from story front-matter.
- If `pr_number` is null OR `pr_merged == true` → SKIP this step.
- Otherwise: wait for CI checks, get approval, then squash-merge.

```bash
gh pr checks ${pr_number} --watch
```
VERIFY: All required CI checks green (exit 0). If checks fail → HALT → AskUserQuestion (options: wait and retry / skip merge / abort QA).

EXECUTE: AskUserQuestion: "CI checks green on PR #${pr_number} targeting ${pr_base}. Squash-merge into ${pr_base} and delete the story branch?" [options: Merge / Skip]

IF approved:
```bash
gh pr merge ${pr_number} --squash --delete-branch
```
VERIFY: `gh pr view ${pr_number} --json state` returns `"state": "MERGED"`.
Read the merge SHA and timestamp:
```bash
gh pr view ${pr_number} --json mergeCommit,mergedAt
```
Write `pr_merged: true`, `merged_sha`, and `merged_at` to story front-matter:
```bash
devforgeai-validate update-story-frontmatter ${STORY_FILE} --field pr_merged --value true --project-root=${PROJECT_ROOT}
devforgeai-validate update-story-frontmatter ${STORY_FILE} --field merged_sha --value ${merge_sha} --project-root=${PROJECT_ROOT}
devforgeai-validate update-story-frontmatter ${STORY_FILE} --field merged_at --value ${merged_at} --project-root=${PROJECT_ROOT}
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.6 --project-root=.`

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
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=06 --checkpoint-passed --project-root=.
# Exit 0: QA workflow complete | Exit 1: HALT
```

## Phase 06 Completion Display

```
Phase 06 Complete: Cleanup
  QA workflow complete — all 6 phase gates passed
  Result: {overall_status}
```
