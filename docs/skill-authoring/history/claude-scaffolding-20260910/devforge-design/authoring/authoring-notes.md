# Authoring notes: devforge-design (SKILL-003), Claude scaffold

Date: 2026-09-10 UTC. Worktree `claude-scaffold-design-20260910`, branch `author/claude-devforge-design-scaffold-20260910`, base commit `c17e758417da64928a0f47fc2600304465ac3f3c` (verified before the first write and again before commit).

## Builder files actually loaded

The Claude `devforge-project-expert-creator` package was **source-loaded, not installed**. Its bytes were read from a frozen commit in a sibling worktree using `git show <commit>:<path>`; nothing was installed, discovered by a client, or invoked. The sibling worktree was never written to.

Sibling worktree absolute path: `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`
Frozen commit: `4999f3106565c5e320d1f1a7db066b437e4e94be`
Package path within it: `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/`

| File loaded (absolute) | SHA-256 of the blob at `4999f31` |
| --- | --- |
| `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` |
| `.../references/framework-context.md` | `884d915f6b65f11540283ee3ed241d2e33cd54c24d22d93e51e3496d49501c66` |
| `.../references/existing-skill-selection.md` | `89a070c3fbee10a8bce513101a0dd50bbfaec431fd3056fddc8d3113e5b933df` |
| `.../references/interview-guide.md` | `0157e51472cbf206b73d818e0243708906496ab8d72a9b1cbefd7cfab3134d76` |
| `.../references/manual-operation.md` | `3b3eb092033239bd8f20f0eb1d087b810cbd87fd641225531b15abc02b3b572c` |
| `.../assets/skill-design-spec.md` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` |
| `.../assets/handoff.md` | `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790` |

`references/validator-handoff.md` and the four expert-authoring assets (`expert-spec.md`, `expert-skill.md`, `expert-package.md`, `evaluation-cases.md`) were **not** loaded. They govern authoring a project expert, which this assignment is not: the target here is a framework roster skill.

**Builder status.** The builder is itself a draft under independent review. An E1 bootstrap review was revise-bounded and its repairs were applied at `4999f31`; no native evaluation of the builder has been recorded. Its head at authoring time was `b7e7152` (a later docs commit recording that review), which was deliberately not used - the packet froze the builder at `4999f31`. Following a draft builder is what the packet assigned; it is not evidence that the builder is correct.

## Workflow actually run

The builder's five phases were run for a framework skill rather than a project expert.

**Intake.** Recovered from disk rather than from questions: the governing specification, the two templates, four contracts, the roster's provenance flow, the repository `AGENTS.md` and `CLAUDE.md`, and the Claude conventions exemplar. The packet's declared digests for the specification, the design-spec template, the shared handoff template and the authoring contract were each re-computed and matched. `devforge expert prepare` was **not** run: no consuming project, policy file or grounding context exists for a framework-authoring task, and running it would have proved nothing about this work.

**Selection.** The Claude canonical inventory was listed in full at the base commit. `providers/claude/plugins/devforgeai/skills/` contains exactly `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator` and `devforge-review`. **No `devforge-design` exists there, and the destination directory did not exist before this authoring** - there was no collision to reconcile. Creation is justified by SKILL-003 being an accepted roster role with its own artifact type, its own template and its own position in the provenance flow, which no searched candidate owns.

Search limits, stated because the claim is bounded: the Codex provider source was not searched (different owner's fence, outside this assignment); installed `.claude/skills` copies and plugin exports were not searched (generated artifacts, never alternative sources); `~/.claude/skills`, any enterprise managed settings directory, and any `--add-dir` inventory were not searched. Candidates were read as source only; nothing was run or installed. The supportable statement is **"no suitable skill found in the searched inventory"**, not "no such skill exists".

**Design.** `design/skill-design-spec.md` was filled from the builder's template. **No questions were asked.** Every material decision was recovered from the specification, templates, contracts or roster; where a source is silent, a proposed default is recorded and labelled `proposed` in section 9's decision table. Silence is not approval and none of these proposals is a requirement anyone gave.

**Authoring.** The package was written; see `file-manifest.json`.

**Prepared transfer.** `handoff.md`, addressed to an independent evaluator, with **Validation status: Not performed.**

## Proposed defaults recorded

Each of these is the author's proposal filling a gap the governing sources leave open. None was approved.

| Proposal | Where it lives | Why |
| --- | --- | --- |
| The overloaded word "design" is narrowed by naming what is excluded: database schema, API surface, class structure, design-pattern choice, system design | `SKILL.md` description and the trigger negatives | SKILL-003's "Does not activate for" row names only prototype and develop. Without this, the most common false activation in a software repository is a schema or API request |
| No product-brief: use the user's own requirement statements marked `user-stated`, put `product-brief` in `missing_inputs`, keep `status: draft`, never fabricate a `PROD` ID or digest | `SKILL.md` and `references/recording-rules.md` | `devforge-define-product` is specified and not implemented, so the required upstream normally does not exist. The alternative - inventing an artifact reference - is unrecoverable for a later reader |
| Mockup destination `docs/devforge/design/mockups/<UX-ID>/` when nothing is selected | `SKILL.md` | The artifact contract suggests a `design` directory but says nothing about assets. Any selected destination governs over this |
| Mockups are self-contained local HTML and CSS with no build step and no network fetch | `references/mockups-and-preview.md` | SKILL-003 phase 3 says "local HTML/CSS"; the no-build, no-fetch reading is the author's, and it is what makes a mockup actually openable by a reviewer |
| Two prose references plus `sources.md` and `derivation.json`; no `scripts/` | package layout | Bounded delivery and progressive disclosure. No deterministic operation in this workflow justifies a helper |
| Invocation is automatic when relevant and explicit by name | design spec section 2 | SKILL-003 does not restrict invocation |
| Trigger split is fixed at authoring time, stratified by `should_trigger` and category | `evals/triggers/trigger-queries.json` | Authoring contract requires a fixed split and forbids held-out answers reaching an author loop |

## Deliberate omissions

- **No managed-runtime section.** The brainstorm exemplar carries one because SKILL-001 selects managed operation. SKILL-003 does not, and the packet forbids copying it without that requirement.
- **No `scripts/`.**
- **No `agents/openai.yaml`.** Codex-only metadata; this is a Claude package.
- **No `allowed-tools`, `disallowed-tools`, `disable-model-invocation` or `user-invocable`.** Frontmatter is `name` and `description` only.
- **No dynamic-context-injection syntax anywhere.** Every command example is inside a `text` fence. The one place the client's shell-substitution syntax is discussed - `references/sources.md` - describes it in words without reproducing the token sequence.
- **Nothing outside the fence.** `docs/mvp`, `docs/mvp/package-index.json`, the roster, hooks, agents, plugin manifests, sibling skills and the Codex tree were read but never written.

## Commands actually run

Read-only inspection and hashing only. No build, no test, no install, no export, no evaluation.

```text
git rev-parse HEAD / git status --porcelain / git branch --show-current   (this worktree)
git ls-tree / git show <commit>:<path>                                    (frozen builder blobs, read-only)
sha256sum                                                                 (governing inputs, package files)
<devforge-binary> --help                                                  (observed subcommand surface)
python3 (stdlib)                                                          (JSON validity, Markdown link resolution, manifest hashing)
```

The `devforge --help` output listed exactly `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`. No subcommand reads a design-spec, resolves its upstream references, or verifies a mockup digest, so `SKILL.md` names that as a missing integration instead of borrowing authority from a command.

Static checks that were run, and what they establish - which is only that these specific facts hold, never that the skill behaves correctly:

| Check | Result |
| --- | --- |
| `evals.json`, `trigger-queries.json`, `derivation.json`, `inspection-claim.json` parse as JSON | pass |
| `cases.jsonl`: 10 lines, each valid JSON, no key outside the section 4.4 set, no assertion key outside `{assertion_id, grader, args, expect, routed_to}` | pass |
| Every local Markdown link in the package resolves to an existing path inside the package | pass, 0 unresolved |
| No `/home/` path anywhere in the package | pass |
| No `docs/mvp` runtime dependency; the only occurrences are provenance records and schema notes | pass |
| `SKILL.md` is 131 lines; description is 950 characters | inside the documented 500-line and 1,536-character guidance |

Evaluation tiers A, B and C: `NOT_RUN`. Behavioural status: `NOT_EVALUATED`.

## Evaluation-runner dependency: PENDING

The packet named the Claude `devforge-evaluate-expert` package as the supplier of the Python JSONL runner and deterministic graders, conditional on its scaffold commit existing.

**It does not exist.** `git log` in `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910` showed `c17e758` at HEAD - the same base commit as this worktree - with no scaffold commit on top. So the packet's fallback applies: `evals/cases.jsonl` was authored to the schema documented in that worktree's `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/port-analysis.md`, sections 4.4 (case schema) and 4.6 (grader set). That analysis file is itself uncommitted, so it has no stable identity and is not pinned as a selected input.

**Unstable observation, recorded as such.** That worktree's uncommitted `evals/cases.jsonl` was read once, read-only, to see how its author shaped a case with no deterministic grader - section 4.7 describes such cases but section 4.4's schema rejects unknown keys and does not show the shape. The observed form was `{"assertion_id": "...", "grader": null, "routed_to": "...", "expect": "..."}`, and this package follows it. **These were uncommitted bytes in another session's working tree.** They may change without notice, they are not a selected input, and nothing was written to that worktree.

Consequences to check when the runner is committed:

1. `routed_to` must be an accepted key, or every routed assertion here needs rewriting.
2. `name_folder_relation` was deliberately **omitted** from `DX-C-001`. Section 4.6 documents its flag as `expect_name_matches_folder`; the observed uncommitted case used `expect_equal`. Rather than bind to a key that may be either, the assertion was left out; DevForgeAI's name-equals-folder convention is not asserted deterministically here.
3. `DX-C-001` uses `candidate_subpath: "."` because its candidate root *is* the package. Whether the runner accepts `"."` is unverified.
4. `claim_evidence_binding`'s observed arg shape (`file`, `claim_field`, `evidence_fields`) addresses named fields in a structured file. The claim this skill actually needs to test lives in a Markdown table cell. A JSON sidecar fixture, `evals/fixtures/unverified-inspection/inspection-claim.json`, was added so the assertion is expressible; either the runner needs a way to address a Markdown cell, or fixtures of this shape stay the convention.
5. `required_report_fields` is applied only to top-level frontmatter keys (`created_at_utc`, `execution_ref`). Nested keys such as `producer.skill_revision` were not asserted, because whether the grader addresses nested paths is undocumented - `placeholder/UX-006.md` holds a placeholder there too, and a later reader should not read its absence from the assertions as a claim that it is clean.

Evals are source-only authoring inputs. They are excluded from installed copies and plugin exports, and nothing in them is a runtime resource.

## Unresolved items for the coordinator

1. **Runner dependency pending** - the five consequences above. Until the runner and graders are committed and their `--help` observed, `cases.jsonl` is authored against a document, not an interface.
2. **No Rust check for this artifact.** Routes R1 and R2 in the design spec are recorded requirements with no implementation. The integration owner decides whether a `devforge` subcommand should resolve a design-spec's upstream references and mockup digests. This author neither implemented nor simulated one.
3. **Upstream producer absent.** `devforge-define-product` is unimplemented, so the required product-brief usually will not exist. The `user-stated` fallback is a proposed default awaiting an owner's decision.
4. **Downstream consumers absent.** prototype, architect, plan and change are unimplemented; develop and review are drafts. Handoff continuations are written in plain language accordingly.
5. **Package index not updated.** `docs/mvp/package-index.json` is outside the fence. Recording `devforge-design`'s readiness state there is the integration owner's action.
6. **Claude client version not observed.** No version probe was run, so the client identity in the design spec is `unknown; not observed`. A tier A or C run must record its own.
7. **Non-UI "design" exclusion is the author's proposal**, not something SKILL-003 states. If an owner disagrees, both the description and four trigger negatives change together.

## What this authoring does not claim

No skill was installed, exported, discovered, activated, run or evaluated. No hook was registered. No gate was implemented, invoked or simulated. No baseline was measured. The package's digests prove which bytes exist; they say nothing about whether the skill produces good designs. Behavioural status is `NOT_EVALUATED` and stays there until an independent evaluator records an actual evaluation.
