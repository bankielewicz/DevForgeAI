---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-CLAUDE-EVALUATE-EXPERT-20260910"
artifact_type: "handoff"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T00:00:00Z"
producer:
  skill: "devforge-project-expert-creator (source-loaded, not installed or discovered)"
  skill_revision: "342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9"
execution_ref: null
upstream:
  - artifact: "SKILL-008 specification"
    store: "project"
    path: "docs/mvp/specifications/skill-008-devforge-evaluate-expert.md"
    revision: "c17e758417da64928a0f47fc2600304465ac3f3c"
    sha256: "0b3dbb7fe9f5f683d2022c86390e736346189e1ea4d92730c7234d9de1ecec0d"
  - artifact: "skill authoring contract"
    store: "project"
    path: "docs/mvp/skill-authoring-contract.md"
    revision: "c17e758417da64928a0f47fc2600304465ac3f3c"
    sha256: "371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53"
  - artifact: "development language policy"
    store: "project"
    path: "docs/development-language-policy.md"
    sha256: "3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f"
evidence:
  - kind: "candidate file manifest"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/file-manifest.json"
    sha256: "c882eaa12f72f1cde2034260890a6125e489f7c69fc8c9715daade4db5928caa"
  - kind: "working design specification"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/design/skill-design-spec.md"
    sha256: "b4f7772ead4bac67bcc654e1fad3241410c417d6a3aa58911de19755e13c20dd"
  - kind: "port analysis"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/port-analysis.md"
    sha256: "182a131838f2241ad36e46c5a61b0ad4afa712179004b059898e101759aa87a3"
  - kind: "specification mapping"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/spec-mapping.md"
    sha256: "f76cb45204e5dbed5b805e77a36d9e17744c93e60b94539c0d2ef338c9559cf9"
  - kind: "authoring notes and local runner observations"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/authoring-notes.md"
    sha256: "95003627c8abe64c3a05eac4c8744f9e775a82dc96ec5191646b4e94fad06bc8"
supersedes: null
decision_ref: null
missing_inputs:
  - "No consuming project or policy file was assigned, so devforge expert prepare had no input and was not run."
  - "No Claude client version was observed; this was an authoring task, not a session evaluation."
---

# Authoring handoff: Claude devforge-evaluate-expert

## Result and next action

- **Result:** A new Claude package for SKILL-008 was authored at `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert`, ported from the Codex implementation. 50 files: 28 runtime, 22 authored evals. The candidate identity is the file manifest cited in `evidence`.
- **Why it matters for what happens next:** two capabilities the Codex evaluator relied on were deliberately **not** ported, because they are a validator gate and an acceptance decision that the language policy assigns to compiled Rust. The package names them as dependencies and works without them. Whether that substitution is adequate is the first thing an evaluator should form a view on.
- **Limits and blockers:** nothing about this candidate's behaviour has been observed. The builder followed for the authoring is itself unvalidated.
- **Next:** an independent evaluation by E2. See the copyable task below.
- **Readiness:** prepared. E2 needs an assigned evaluation output directory; everything else resolves from the paths below.
- **Validation status:** Not performed.
- **Behavioural status:** `NOT_EVALUATED`.
- **Enforcement status:** requirements recorded; no gate implemented by this skill.

## Outputs produced

This handoff is excluded from the table: it carries no digest of itself and does not list itself among its own outputs.

| Direction | Artifact | Path | SHA-256 | State |
| --- | --- | --- | --- | --- |
| output | Candidate package (50 files) | `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/` | per-file map in the manifest below | authored, unevaluated |
| output | Candidate file manifest | `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/file-manifest.json` | `c882eaa12f72f1cde2034260890a6125e489f7c69fc8c9715daade4db5928caa` | frozen |
| output | Working design specification | `.../authoring/design/skill-design-spec.md` | `b4f7772ead4bac67bcc654e1fad3241410c417d6a3aa58911de19755e13c20dd` | revision 1 |
| output | Port analysis (phase 1) | `.../authoring/port-analysis.md` | `182a131838f2241ad36e46c5a61b0ad4afa712179004b059898e101759aa87a3` | frozen |
| output | Specification mapping | `.../authoring/spec-mapping.md` | `f76cb45204e5dbed5b805e77a36d9e17744c93e60b94539c0d2ef338c9559cf9` | frozen |
| output | Authoring notes | `.../authoring/authoring-notes.md` | `95003627c8abe64c3a05eac4c8744f9e775a82dc96ec5191646b4e94fad06bc8` | frozen |
| input | SKILL-008 specification | `docs/mvp/specifications/skill-008-devforge-evaluate-expert.md` | `0b3dbb7f…` | accepted, unchanged |
| input | Codex port source | `providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert/` | per-file digests in the port analysis §1 | read-only; unchanged |

## Evidence and reading order

| Read when | Record | Why |
| --- | --- | --- |
| First | this handoff, then `authoring-notes.md` | What was and was not done, the builder dependency, and the local runner observations |
| Before evaluating | `design/skill-design-spec.md` §2, §4, §7, §9 | The independently stated expectations, the workflow classification and the selection record |
| For requirement coverage | `spec-mapping.md` | Every SKILL-008 element mapped to a file, section and case ID |
| For a disposition question | `port-analysis.md` §1 and §3 | Why each Codex file was ported, reduced, dropped or replaced, and the Rust-authority boundary |
| For the candidate itself | `providers/claude/.../devforge-evaluate-expert/SKILL.md`, then the reference it links for the phase in question | The candidate |

## Proposed evaluation cases

Captured, not executed. Twelve tier-B acceptance cases in `evals/evals.json`, twenty-three tier-A queries with a fixed train/validation split in `evals/triggers/trigger-queries.json`, thirteen deterministic runner cases in `evals/cases.jsonl`.

| Check | Outcome | Evidence | Cause or limit |
| --- | --- | --- | --- |
| Tier A discovery and activation | NOT_RUN | none | Requires installation and a fresh session |
| Tier B output quality against a baseline | NOT_RUN | none | Requires a baseline arm and an observed boundary |
| Tier C installed resources | NOT_RUN | none | Requires an actual installed copy in a consuming project |
| Independent review R01–R10 | NOT_RUN | none | An author cannot supply it |
| Runner and grader discrimination on synthetic fixtures | observed | `authoring-notes.md` §Runner and grader observations | **Author observation, not validation.** Synthetic inputs only; says nothing about the skill's behaviour |

## Copyable next task

```text
Goal: Independently evaluate the authored Claude devforge-evaluate-expert candidate against SKILL-008.

Context:
  Handoff:     /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/handoff.md
  Candidate:   /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert
  Manifest:    /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/file-manifest.json
  Design spec: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/design/skill-design-spec.md
  Mapping:     /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/spec-mapping.md
  Governing:   /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/docs/mvp/specifications/skill-008-devforge-evaluate-expert.md
               sha256 0b3dbb7fe9f5f683d2022c86390e736346189e1ea4d92730c7234d9de1ecec0d

Task: Evaluate this candidate read-only. Confirm the manifest digests before reading anything
  else; a mismatch means the bytes drifted and the evaluation targets a different candidate.
  Cover at minimum:
    - the two missing-DevForge-CLI-capability statements and whether the manual procedure that
      replaces them is honest and sufficient for the claims the package makes;
    - whether scripts/run_cases.py and scripts/graders.py stay inside the language policy's
      evaluation exception, or amount to a gate under another name;
    - requirement coverage against spec-mapping.md;
    - the trigger set for realistic activation and near-miss exclusion.
  Report structural observations, semantic review and any native tiers separately.

Preserve: the candidate bytes, this worktree, the Codex package, and every digest cited above.
  Do not edit the candidate - findings go back to the author. Do not weaken a case or an
  expectation to reach a pass.

Output: an evaluation report, a bounded repair specification if changes are justified, and a
  handoff, in the evaluation output directory the coordinator assigns.

Stop at: an honest terminal status or missing-evidence cause for every required observation.
  Tier A/B/C remain COULD_NOT_RUN if no installation and observed boundary are available;
  that is an acceptable result, and inventing one is not.
```

## Retention and continuation limits

- **Output readback:** every path in the outputs table was written and its digest computed after its bytes were final. This handoff is excluded from that table.
- **This handoff's location:** the path given in the copyable task. It carries no digest of itself; compute and deliver that externally.
- **Worktree ownership:** retained by worker A2's branch `author/claude-devforge-evaluate-expert-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c`. Committed, not pushed.
- **External gate state:** none. No DevForge command was run against this candidate, and none of the six workflow phases is intercepted by any command.
- **Conditions invalidating this handoff:** any change to the candidate bytes, to SKILL-008, to the packaged contracts' governing sources, or to the two missing CLI capabilities becoming available. Also: the parallel bootstrap review E1 finding a defect in the builder followed for this authoring.

A prepared transfer is not receiving execution and not acceptance. This document authorises no evaluation, installation, activation or automatic invocation.
