# Brainstorm Codex native evaluation — 2026-09-28

**Outcome: NOT QUALIFIED for complete SPEC-001 acceptance.** All 48 planned native trials
ran: **21/24 plugin runs passed**, versus **3/24 no-plugin baseline runs** under the same
full-contract graders. Seven of eight imported cases meet the 0.8 threshold across three
runs. Eight scripted manual scenarios produced seven passes and one failure. Three
additional isolation controls confirmed their original outcomes.

The full ten-obligation imported plan remains **7 PASS / 2 FAIL / 1 BLOCKED**.
The blocked PRD-present branch is **NOT_RUN**, not silently replaced by the passing
absent-PRD branch. VER-09's original specification core passes; the expanded imported
manual plan fails its confirmed-convergence check.

## Evaluated candidate and host

- Plugin: devforgeai 0.1.0; Brainstorm SKL-001 v7; SPEC-001 v10.
- Exact 62-file candidate SHA-256:
  `319fdfe17a22688e7a39ae4018d3914777cbd2c76616f4486aaeba2e3e46ce8e`.
- Codex 0.158.0, WSL Ubuntu, host-selected model `gpt-6-astra`, high reasoning effort.
- Native app-server sessions were ephemeral, with workspace-write sandboxing and
  approval policy `never`. No sandbox bypass was used.
- The host discovered the exact candidate through process-scoped skill roots and
  exposed it as `devforgeai:brainstorm`. Prompts were the imported natural-language
  prompts, without forced skill injection. Baseline sessions had no Brainstorm in
  their native catalog. No plugin installation or marketplace registration occurred.

[Binding](binding.json), [frozen matrix](matrix.json), [manual plan](manual-plan.json),
and [machine-readable results](results.json) retain the denominator and identity.
The candidate's files remained unchanged. Its README and initial verification plan
retain their import-time NOT_RUN wording to preserve the evaluated bytes; this report
and results.json provide the current status.

## Repeated cases

A trial passes only if every applicable check passes. A case score is the mean of its
three binary trial results; the required threshold is 0.8. No failed repeat was removed.

| Case | Plugin | Baseline | Assessment |
|---|---:|---:|---|
| writes-valid-brn | 3/3 | 0/3 | Correct path, typed items, concrete ideas, executed validator and handoff |
| no-unconfirmed-dispositions | 3/3 | 0/3 | All unconfirmed ideas open/null; document draft |
| records-provenance | 0/3 | 0/3 | Session matches host; model remains unknown |
| uses-named-framework | 3/3 | 0/3 | Named method and collection-specific fields conform |
| ignores-unrelated-request | 3/3 | 3/3 | Reviews the PR; no Brainstorm skill read |
| asks-for-topic | 3/3 | 0/3* | Asks for a topic; no document created |
| existing-brn | 3/3 | 0/3 | Requests extend/new; full original file hash unchanged |
| hands-off-to-prd | 3/3 | 0/3 | Correct **absent-PRD** handoff only |

*The baseline asks an appropriate topic question in all three runs. Its full-contract
score is zero because the positive skill-load assertion necessarily fails without the
plugin. These scores do not claim a general model-quality improvement.

Grading uses the imported regex/file assertions, actual completed tool executions,
saved artifact parsing, full-file hashes, host identity comparison, and the primary
importing agent's semantic review. Model claims such as “PASS” are not grading evidence.
Semantic assessments are retained per run in `semantic-review.json`; this is
**not independent qualification** by a separate assessor.

## Manual and tool-specific scenarios

All supplied names, answers and decisions were synthetic test fixtures, not the owner's
approval of a real brainstorm.

| Scenario | Result | Observed evidence |
|---|---|---|
| Added framework | PASS | Selected validation-probe and emitted its method marker; SKILL.md unchanged |
| Missing framework | PASS | Disclosed missing file and used diverge-converge |
| Stop, save=yes | PASS | Asked about saving; wrote draft/open/null only after the answer |
| Stop, save=no | PASS | Asked about saving; wrote no document after refusal |
| Unfixable validator | PASS | Exactly three attempts, draft retained, remaining error reported; test validator unmodified |
| Confirmed decisions | **FAIL against SPEC** | Exact dispositions/reasons preserved, but explicit convergence still saved as draft |
| Extend existing BRN | PASS | Original item objects and history row retained; version 2 and new IDs allocated |
| Native question in Plan mode | PASS | Native request_user_input event; existing BRN untouched while unanswered |

Native `request_user_input` was also observed in both default-mode stop scenarios.
Pending questions were interrupted without supplying acceptance; subsequent synthetic
user turns exercised the stop/save choices. Silence was not treated as confirmation.

## Complete requirement denominator

| Obligation | Status | Scope |
|---|---|---|
| VER-01 | PASS | Writes-valid-brn, three runs |
| VER-02 | PASS | No unconfirmed dispositions, three runs |
| VER-03 | **FAIL** | Missing exact model identity in all three runs |
| VER-04 | PASS | Named framework, three runs plus two separate controls |
| VER-05 | PASS | Added/missing framework variants |
| VER-06 | PASS | Unrelated request, three runs |
| VER-07 | PASS | Missing topic, three runs |
| VER-08 | PASS | Existing BRN, three runs plus extension preservation |
| VER-09 | **FAIL, expanded plan** | Stop/save, three failures and static limits pass; planned confirmed-convergence check fails |
| VER-10 | **BLOCKED** | PRD-present branch NOT_RUN because Codex PRD is absent |

The literal SPEC-001 VER-09 obligation covers stop/save, three failed validation attempts,
and static limits; those checks passed. The imported eval README additionally requires
confirmed dispositions/convergence and extension. Its additional failure is retained
in the expanded plan rather than waived.

## Discrepancies requiring resolution

1. **Model provenance is incomplete (D-04 / VER-03).** The host records gpt-6-astra,
   while the generated BRNs record unknown. Session IDs match the actual host threads.
   The port honestly discloses the gap, but does not meet the provenance obligation.
   A hosting integration must expose an authoritative model ID, or the specification
   owner must define an accepted provider variation.
2. **The missing-model fallback changes convergence behavior (D-04 / BEH-06).**
   In the confirmed-decisions scenario, the user explicitly confirmed convergence.
   The port's own rule nevertheless forced status draft. This follows the imported
   instructions but diverges from the specification's confirmed-convergence behavior.
3. **Codex PRD is absent (D-01 / VER-10).** The imported absent-PRD branch passes, but
   the specification requires a runnable PRD-present handoff. Port PRD separately or
   obtain an owner-defined Brainstorm-only acceptance profile.
4. **Inherited validator gaps remain open (D-03).** The previous controlled probes
   still establish acceptance of numeric authors, an extra generated_by field and a
   Change Log placeholder. Successful native documents do not close those defects.

See the [import comparison](../../IMPORT-REPORT.md) for provider adaptations,
specification wording discrepancies, and the original validator probes.

## Isolation, attempts and reproducibility

The original matrix used distinct project directories under a shared temporary parent.
Two framework plugin runs and one handoff baseline run listed sibling filenames.
The audit found no explicit sibling-document reads. All three were retained and
repeated as **additional controls**, each under a unique temporary parent: both plugin
controls passed, and the baseline control again failed the same full contract.
No original score or denominator was replaced.
[Discovery audit](discovery-audit.json) records the exact events and limits;
this is not a claim of enforced read isolation.

Preparatory failures are retained: a non-login PATH lookup, invalid process-only MCP
option syntax, and a discovery guard that initially expected an unqualified skill name.
One successful native preflight is retained separately. The first derived grading
attempt failed to serialize YAML dates; its outputs were preserved before correcting
the grader. These are harness issues, not product failures.

Each run contains its prompt, launch parameters, native catalog, host identity, raw
protocol and stderr, before/after inventories, output files, and grading decisions.
The version-matched native protocol schemas and controller scripts are retained here.
This evaluation changed no candidate runtime files or Claude source files.

To recompute derived grades from the retained artifacts:

```bash
python3 -B src/codex/devforgeai/import-evidence/native-evaluation-20260928/grade_eval.py
python3 -B src/codex/devforgeai/import-evidence/native-evaluation-20260928/aggregate_eval.py
```

Those commands regrade saved evidence; they do not rerun models. The native driver
refuses to overwrite an existing trial. A new campaign needs a new evidence/workspace
root and a newly recorded candidate binding.

Native APIs were checked against the local 0.158.0 protocol schema and
[official Codex app-server documentation](https://learn.chatgpt.com/docs/app-server).
Installed-plugin discovery, deployment, independent acceptance and owner review remain
separate from this completed source evaluation.
