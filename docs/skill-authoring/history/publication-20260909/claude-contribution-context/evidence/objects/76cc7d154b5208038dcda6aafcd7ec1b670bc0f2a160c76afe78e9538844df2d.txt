# Skill authoring: next steps

Status: proposed coordination plan. This document does not migrate sources, revise governing specifications, approve a candidate, create commits, or run evaluations.

## Verified starting point

- Both local repositories report `No commits yet on main`; normal worktree assignments therefore need an initial committed baseline first. No initial commit has been created by this task.
- DevForgeAI/AGENTS.md and CLAUDE.md still route authors to `plugins/devforgeai/skills`. The companion installer selects provider destinations from that shared source.
- Claude owns the current devforge-brainstorm candidate and its evaluation workspace. Preserve both the original POC snapshot and the current candidate before migration.
- The current brainstorm package contains SKILL.md, scripts, references, assets, and evals/evals.json. Its two input fixtures live in .poc/devforge-brainstorm-workspace/fixtures. The inspection found no iteration result files in that workspace; that is not a claim about unseen terminal activity.
- docs/mvp/research/sources.json records eight earlier OpenAI sources and does not yet capture the Agent Skills topic review.

## Recommended order and ownership

| Step | Proposed owner | Work | Observable completion |
| --- | --- | --- | --- |
| 1 | Existing Claude author | Checkpoint current package, original baseline, cases, and any existing run outputs; confirm whether any writers or runs remain active. | Saved paths, file hashes, and activity status. |
| 2 | This Codex session, as integration owner | Refresh shared authoring/evaluation contracts and provider routing; implement the source-selection migration and installer changes once the old paths are quiescent. | One consistent source layout, documented installation contents, preserved Claude bytes, and relevant checks. |
| 3 | User/operator with integration owner | Review and commit the intended local baseline; omit runtime credentials and disposable evaluation outputs. Assign distinct worktrees and branches from the recorded commit. | Real commit IDs, worktree paths, branch names, owners, and write fences. |
| 4 | Claude author and separate Codex author | Implement and evaluate SKILL-001 for their own provider from the same specification revision and raw test inputs. | Separate native installation, discovery, trigger, output-quality, and resource-resolution observations. |
| 5 | Independent reviewer and integration owner | Review evidence and the combined candidate, resolve findings, and update readiness records. | Scoped per-provider conclusions and verification of the integrated files. |
| 6 | Assigned authors | Expand to SKILL-002 and prove that it consumes the idea ledger; then expand the roster in bounded batches. | A demonstrated upstream-to-downstream workflow before bulk generation. |

A fresh session is useful for independent review. It is not automatically isolated: the assignment must identify its context, installed skills, raw inputs, worktree, and write scope. A new Codex session should start with read-only review now, or with one provider-specific skill only after step 3.

## Focused document refresh

| Document area | Required update |
| --- | --- |
| New docs/mvp/skill-authoring-contract.md | Standard minimum versus optional resources; provider authoring roots; runtime contents versus eval inputs/results; script and resource path rules; source/installed identities; evaluation stages and promotion evidence. Apply the common evaluation process to framework skills as well as generated experts. |
| docs/mvp/execution-contract.md | Explicit session assignment for provider sources, initial commit/worktree prerequisite, installation/discovery verification, and shared-document integration ownership. State which client behaviors must be observed rather than claimed from instructions. |
| docs/mvp/artifact-contract.md | Clarify identity and provenance of evaluation fixtures, cases, candidates, installed packages, and reports using existing envelope/sidecar rules where possible. Clarify bootstrap null/missing inputs without equating a missing session record with single-writer ownership. |
| SKILL-001 | Resolve adoption/early user constraints, bootstrap ownership, package-relative execution versus project artifact paths, and separate activation versus output-quality observations. Preserve its four phases and core purpose. |
| SKILL-007 and SKILL-008 | Require reproducible cases/fixtures, source-grounded expert knowledge, refresh triggers, explicit baselines, held-out trigger cases, and evidence for the target provider. Keep evaluation and authoring roles separate. |
| All 12 native creator prompts | Link the shared authoring contract and require an assigned provider destination, actual runtime target, and write fence. Avoid repeating the whole contract in every specification. |
| Authoring/evaluation templates | Add reusable eval-case, trigger-query, and run-manifest templates; update expert evaluation plan/report and expert-package templates. Cover framework-skill evaluations without pretending an expert-only artifact contract already covers them. |
| AGENTS.md, CLAUDE.md, README.md, docs/POC.md | Replace shared source routing when the migration is implemented; distinguish source paths, installed copies, optional metadata, agents, and executable gates. |
| docs/mvp/README.md and package-index.json | Register the new shared contract/templates and provider-specific implementation/evaluation status. Make the immediate continuation the brainstorm pilot. |
| docs/mvp/research/ | Record the seven Agent Skills topic URLs, retrieval date, concrete design applications, and provider-specific limits. |
| Validation evidence | Preserve the existing validation report as evidence for its original hashes. Run checks against the revised files and publish a new revision/result; do not relabel the old PASS as covering changed bytes. |

The roster and causal provenance diagram need no wholesale redesign. Update readiness/authoring annotations only where the final contracts change them. Business-output templates need changes only when an identified contract correction affects their fields.

## Implementation changes accompanying the documents

- Establish `providers/claude/plugins/devforgeai/` and `providers/codex/plugins/devforgeai/` as separately owned provider package sources. Keep each installed skill self-contained. Separate sources are a DevForgeAI ownership choice; the underlying Agent Skills format is portable.
- Preserve standalone Codex subagent templates under `providers/codex/agents/`. Per-skill `agents/openai.yaml` is optional Codex metadata, not a subagent definition.
- Update the installer, structural validator, tests, examples, and documented source references together. Identify which authoring-only files are excluded from normal installation, while preserving all declared runtime resources.
- Put reproducible authored fixtures with eval cases, not only in an ignored run workspace. Keep generated outputs, transcripts, grading, and measurements outside the installed package.
- Test meaningful cases: distinct provider source selection, installed resource resolution from a consumer project, preservation of locally edited installed files, and actual per-provider discovery. Structural tests do not establish native skill behavior.
- Keep deterministic acceptance implementations in DevForge. A shared folder convention, a prose rule, or a plugin manifest is not enforcement.

## Prompt to relay to Claude now

```text
Keep ownership of your existing devforge-brainstorm candidate. We are
standardizing provider-specific source locations and a shared authoring and
evaluation contract before expanding skill generation.

First checkpoint your work: preserve the original POC skill-snapshot, save
an exact snapshot and SHA-256 file manifest of the current candidate, and
preserve evals.json, input fixtures, and any completed or partial run outputs.
Report the paths and whether any writer or eval run is still active. Do not
move or delete the existing package or replace earlier evidence.

Your five proposed cases are a useful initial set. Review the evaluation
plan against agentskills.io/skill-creation/evaluating-skills and
agentskills.io/skill-creation/optimizing-descriptions. Identify the additions
needed for separate native trigger tests, user adoption of a proposal,
staleness/collision handling, and installed resource/script path resolution.
Report specification ambiguities without changing shared specifications.

Treat direct instruction to read SKILL.md as output-quality evaluation;
it does not demonstrate implicit activation. Label comparisons against the
original snapshot old_skill, not without_skill. Keep Codex results explicitly
unavailable unless they were actually observed in Codex.

Limit writes to a new checkpoint/report directory beneath your existing
.poc/devforge-brainstorm-workspace. Pause new package edits and new eval runs
at this checkpoint while the integration owner migrates sources. Continue
with your Claude provider package only after receiving the recorded baseline,
assigned worktree, write fence, and revised contract paths. Then fix the
candidate within that assignment and run the bounded Claude evaluations.
Do not edit the Codex provider tree or companion DevForge gates.
```

## Prompt for another Codex session now

```text
Perform a read-only authoring-readiness review of
/home/bryan/Projects/DevForge/framework/DevForgeAI.

Read AGENTS.md, docs/mvp/README.md, artifact-contract.md,
execution-contract.md, and SKILL-001/007/008 with their relevant templates.
Compare them with the Agent Skills specification, best practices,
optimizing descriptions, evaluating skills, using scripts, and client
implementation guidance at agentskills.io. Treat this as an independent
review; derive findings from the documents and current files.

Report concrete contradictions, missing contracts, and the smallest changes
needed for reproducible authoring and evaluation in subscribed Claude and
Codex terminals. Distinguish standard requirements, provider extensions,
DevForgeAI conventions, and behavior requiring actual terminal evidence.

Do not generate or edit skills, change shared documents, install packages,
commit, launch evals, or modify companion DevForge. Another author owns the
current brainstorm candidate. Save your report in a new uniquely named
/tmp directory, read it back, and report its absolute path and SHA-256.
```

## Subsequent Codex author assignment

After the baseline and worktree exist, give the Codex author the actual
worktree path, branch, base commit, shared contract revisions, and write
fence. Assign only SKILL-001 in the Codex provider tree plus its separate
evaluation workspace. Invoke the native skill-creator. Require the same
behavioral contract and raw cases as Claude, independently observed Codex
activation and installed-resource behavior, and a handoff with actual
outputs and limitations. Do not use a report from one terminal as evidence
that the other terminal works.

## Sources

- https://agentskills.io/home
- https://agentskills.io/specification
- https://agentskills.io/skill-creation/best-practices
- https://agentskills.io/skill-creation/optimizing-descriptions
- https://agentskills.io/skill-creation/evaluating-skills
- https://agentskills.io/skill-creation/using-scripts
- https://agentskills.io/client-implementation/adding-skills-support
- https://learn.chatgpt.com/docs/build-skills

These links were consulted in this conversation. This plan is a design
application of the guidance, not an implementation or acceptance report.
