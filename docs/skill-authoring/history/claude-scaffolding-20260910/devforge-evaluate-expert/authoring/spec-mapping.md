# SKILL-008 requirement mapping

Every element of `docs/mvp/specifications/skill-008-devforge-evaluate-expert.md` (sha256 `0b3dbb7fe9f5f683d2022c86390e736346189e1ea4d92730c7234d9de1ecec0d`, verified equal to the task packet's stated digest) mapped to where it lives in the authored Claude package.

Paths are relative to `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/`. Case IDs beginning `EX-` are runner cases in `evals/cases.jsonl`; numbered eval IDs are tier-B acceptance cases in `evals/evals.json`; `A#` IDs are tier-A queries in `evals/triggers/trigger-queries.json`.

## User goal and use-case inventory

| Spec element | Destination | Case |
| --- | --- | --- |
| User goal: does an installed expert activate appropriately and improve representative work within its constraints | `SKILL.md` opening and phase table | eval 1 |
| Direct request: "Use DevForgeAI to evaluate this generated expert skill" | `SKILL.md` frontmatter `description` | eval 1; A1a–A1c, A2a–A2c |
| Indirect request: "Does this expert actually help, or does its SKILL.md just look convincing?" | `SKILL.md` frontmatter `description` | eval 2; A3a–A3d |
| Expected result: plan, report and standardized handoff | `assets/expert-evaluation-plan.md`, `assets/verification-results.md`, `assets/expert-evaluation-report.md`, `assets/handoff.md` | eval 1 |
| Required context: specification, exact candidate, raw inputs, terminal availability, permitted workspace | `SKILL.md` §Required inputs; `assets/validation-plan.json` | eval 1, eval 3 |
| Plugin capability: native subscribed runs; a manual separate-session evaluation is valid; no API harness required | `references/native-evaluation.md` §3; `references/framework-context.md` | eval 3 |
| State/action boundary: must not change the candidate or expectations to obtain a pass, or describe a contaminated session as independent | `SKILL.md` §Non-negotiable boundaries; `references/evaluation-boundaries.md`; `references/ai-review-rubric.md` §Preparing an independent review | eval 10; EX-DEF-005 |
| MVP support decision: record results separately per provider | `references/contracts/skill-authoring-contract.md` §Three separately reported tiers | eval 1 |
| Does not activate for: final acceptance of an application patch; frontmatter-only validation | `SKILL.md` `description` and §Non-negotiable boundaries | eval 5; A5a–A5b, A6a–A6b |

## Inputs and provenance

| Spec element | Destination | Case |
| --- | --- | --- |
| expert-spec required | `SKILL.md` §Required inputs; `assets/validation-plan.json` `input_refs` | eval 1 |
| expert-package required, exact source and installed identities | `assets/validation-plan.json`; `assets/run-manifest.json` | eval 1 |
| Story, architecture and raw evidence as applicable | `assets/test-cases.json`; `references/native-evaluation.md` §2 | eval 2 |
| Prior evaluation report optional, for regressions | `assets/validation-plan.json` `findings_from_previous_iteration` | eval 7 |
| Artifact contract: exact revisions, hashes, stable section IDs, decisions | `references/contracts/artifact-contract.md` | eval 8 |
| Execution contract: one owner and fence per writing session; distinct worktrees | `references/contracts/execution-contract.md`; `references/native-evaluation.md` §1 | eval 6 |

## Workflow and phase exits

All phases P1–P6 and tasks T01–T12 preserved as Enforced accepted requirements. Recorded as workflow content in the `SKILL.md` phase table and classified in the working design spec §4.

| Spec phase | Destination | Case |
| --- | --- | --- |
| P1 / T01 identify target, provider, authority, specification, fence | `SKILL.md` §P1; `assets/validation-plan.json` `assignment` | eval 1 |
| P1 / T02 freeze candidate, specification, cases, rubric, baseline | `SKILL.md` §P1; `assets/validation-plan.json` `criteria_freeze_record` | eval 1, eval 7 |
| P1 bounded workspace allocation when selected | `assets/workspace-allocation.json`; `references/native-evaluation.md` §1 | eval 1 |
| P2 / T03 inspect structure, references, source and installed identity | `SKILL.md` §P2; `references/missing-rust-capabilities.md`; `scripts/run_cases.py` | eval 12; EX-GOOD-001, EX-DEF-001…008 |
| P3 / T04 independent prompt and compliance review against the rubric | `SKILL.md` §P3; `references/ai-review-rubric.md`; `assets/ai-review.json` | eval 4 |
| P4 / T05 establish isolated runtime and fixtures | `references/native-evaluation.md` §3; `assets/environment-setup.json` | eval 3 |
| P4 / T06 tier C installed resources | `references/native-evaluation.md` §5 | EX-GOOD-001, EX-DEF-008 |
| P4 / T07 tier B candidate versus baseline output quality | `references/native-evaluation.md` §6 | eval 2 |
| P4 / T08 tier A discovery and activation | `references/native-evaluation.md` §7; `evals/triggers/trigger-queries.json` | eval 9; EX-GOOD-003, EX-DEF-007 |
| P5 / T09 adjudicate evidence, applicability, coverage, freshness | `SKILL.md` §P5; `references/results-contract.md`; `assets/validation-results.json` | eval 11, eval 12 |
| P6 / T10 write verification results | `assets/verification-results.md` | eval 1 |
| P6 / T11 bounded repair specification and rerun plan | `assets/skill-enhancement-spec.md` | eval 1 |
| P6 / T12 deliver custody handoff | `assets/handoff.md`; `references/evaluation-boundaries.md` §Concise handoffs | eval 1 |
| "These phases are not new CLI subcommands" | `SKILL.md` §The workflow; `references/evaluation-boundaries.md` §What no command here covers | eval 12 |
| On interruption preserve phase and evidence; resume after verifying identities | `SKILL.md` §Stopping | eval 7 |

## Outputs and templates

| Spec element | Destination | Case |
| --- | --- | --- |
| expert-evaluation-plan (EVPLAN) with its template | `assets/expert-evaluation-plan.md`, byte-identical copy of the shared template | eval 1 |
| expert-evaluation-report (EVREPORT) with its template | `assets/expert-evaluation-report.md`, byte-identical copy; detailed content in `assets/verification-results.md` | eval 1 |
| Consumer coverage: plan → evaluate/review; report → creator/develop/review/change | `references/evaluation-boundaries.md` §Artifact mapping | eval 1 |
| Handoff with output identities, observed checks, unresolved decisions, next owner, one copyable prompt | `assets/handoff.md`, byte-identical copy of the shared template | eval 1 |

## Validation and behavioural acceptance

| Spec case | Destination | Case |
| --- | --- | --- |
| Direct activation → plan and evidence-bound report | `SKILL.md` `description`, §P1, §P6 | eval 1 |
| Indirect activation → includes a relevant baseline comparison | `SKILL.md` §Required inputs; `references/native-evaluation.md` §6 | eval 2 |
| Unavailable terminal → `COULD_NOT_RUN`; file existence is not discovery | `SKILL.md` §When a check cannot run; `references/native-evaluation.md` §7 | eval 3 |
| Weak grader → expected headings but stack violated; fails behavioural compliance | `references/ai-review-rubric.md` R02/R03/R04 | eval 4; EX-SEM-001 |
| Out of scope → source-code QA routes to review | `SKILL.md` `description` | eval 5; A5a–A5b |
| Common: concurrent writer claims worktree or branch | `SKILL.md` §When a check cannot run; `references/contracts/execution-contract.md` | eval 6 |
| Common: upstream revision or candidate changes → mark prior evidence stale | `references/results-contract.md`; `SKILL.md` §Stopping | eval 7 |
| Common: template placeholder in a required field → stays a draft | `references/contracts/artifact-contract.md`; grader `required_report_fields` | eval 8; EX-GOOD-002 |
| Common: a requested check cannot execute → `COULD_NOT_RUN`, not PASS | `SKILL.md` §When a check cannot run | eval 9; EX-DEF-007 |
| Report A, B and C independently; explicit and implicit are distinct | `references/native-evaluation.md`; `assets/validation-results.json` | eval 1 |
| A no-skill baseline must not discover the candidate from another installation | `references/native-evaluation.md` §4 step 5 | eval 2 |
| Inspect a creator harness before relying on its detector | `references/native-evaluation.md` §7 | eval 9 |

## Rework, stopping and recovery

| Spec element | Destination | Case |
| --- | --- | --- |
| Failed behaviour returns to the creator with cases and evidence | `assets/skill-enhancement-spec.md`; `SKILL.md` §P6 | eval 1 |
| Changed candidates need a new evaluation identity | `references/results-contract.md` §Builder remediation contract | eval 7 |
| Stop when runtime, raw inputs or independence cannot be met | `SKILL.md` §When a check cannot run | eval 3 |
| Do not force-unlock, overwrite another session's result, or retry indefinitely | `SKILL.md` §When a check cannot run; `references/evaluation-boundaries.md` | eval 6 |

## Deliberately not carried into this package

| Spec element | Disposition |
| --- | --- |
| Native creator authoring prompt | Not package content. Recorded in `authoring-notes.md` as the instruction actually used, per the authoring contract's requirement to record whether the assigned creator instructions were used. |
| F01–F08 manual promotion contract; managed IDs `skill-builder` / `skill-validator`; `advance`/`resume`/`complete` | Codex-and-installer-specific. One short historical paragraph is retained in `references/framework-context.md` §Historical identities so the package does not imply a Claude adoption path exists. Coordinator answer Q4. |
| Accepted Routine/Full (VPR-2) validation policy for manual mode | Recorded `NOT_APPLICABLE` in `references/contracts/skill-authoring-contract.md`. Coordinator answer Q4. |
| Owner-approved local unqualified baseline and the `--manual-experts-only` installer mode | Recorded `NOT_APPLICABLE` in the same section and in `references/evaluation-boundaries.md`. Coordinator answer Q4. |

## Requirements added by the port, not present in SKILL-008

| Requirement | Destination | Basis |
| --- | --- | --- |
| Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI | `SKILL.md`, `references/framework-context.md`, `references/missing-rust-capabilities.md`, `assets/validation-results.json`, `assets/verification-results.md` | Development language policy; port constraint |
| Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI | the same five locations | Development language policy §Protect the trusted implementation |
| A JSONL evaluation runner plus deterministic graders as required evidence artifacts | `scripts/run_cases.py`, `scripts/graders.py`, `references/runner-interface.md`, `evals/cases.jsonl`, `evals/fixtures/**` | Development language policy §Rust framework authority and required Python evaluation |
