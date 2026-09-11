# Skill design specification — devforge-prototype

Working design document for the Claude `devforge-prototype` scaffold (SKILL-004). Derived from the builder's `assets/skill-design-spec.md` template at commit `4999f3106565c5e320d1f1a7db066b437e4e94be` (sha256 `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9`) and filled here, not in the package.

This is a DevForgeAI authoring document. It carries the design, the framework authority and source mapping, and the change record. It does not certify a skill, and completing it establishes nothing about behaviour.

No questions were asked of any user during this pass. The assignment directed that every material decision be recovered from the specification, templates and contracts, and that anything they leave silent be recorded as a labelled proposal. Every row marked **proposed** below is this author's proposal awaiting a decision, not a requirement anyone gave.

## 1. Identity and purpose

**Skill name:** `devforge-prototype`

**Purpose:** Run a bounded experiment that settles a consequential technical uncertainty before a product, design or architecture decision is committed, and leave a recorded result with an explicit disposition of the prototype code. Generic advice about how to prototype is not the point; the point is a threshold recorded before the measurement, evidence preserved as it came out, and a boundary that stops experiment code becoming production code.

**Description for discovery:** Written into the package frontmatter. It states what the skill does, the direct and indirect requests that should select it, and four near-miss exclusions naming the sibling that owns each — `devforge-develop`, `devforge-design`, `devforge-change`, `devforge-brainstorm` — plus the specification's own MVP support decision that an uncertainty resolvable by inspection or existing evidence needs no experiment.

**Intended users or role:** Whoever holds an open feasibility question that a decision is waiting on — the person about to accept an architecture contract, sign off a design, or commit a scope.

## 2. Scope and activation

**Use this skill when:** A concrete uncertainty exists, a product, design or architecture decision is waiting on it, and inspection or existing evidence will not settle it. SKILL-004: "Conditional when an experiment could change a decision."

**Outside its scope:**

| Near miss | Owner | Basis |
| --- | --- | --- |
| A fully specified production behaviour with no open feasibility question | `devforge-develop` | SKILL-004 "Does not activate for" row, verbatim |
| Screens, flows, a clickable UI mock | `devforge-design` | Roster SKILL-003; "prototype" in the UX sense is a different artifact |
| Reopening an accepted decision | `devforge-change` | Roster SKILL-012; the prototype's dashed edge back to architect is a finding, not an amendment |
| Working out what to build at all | `devforge-brainstorm` | Roster SKILL-001; a prototype needs a concrete uncertainty, which brainstorm precedes |
| An uncertainty inspection or existing evidence already settles | nobody — answer it directly | SKILL-004 "MVP support decision": "Skip when the uncertainty can be resolved reliably by inspection or existing evidence" |

**Example activating requests:** "Use DevForgeAI to prototype the risky part before we commit." (SKILL-004 direct request.) "Can this approach support the interaction or performance we need?" (SKILL-004 indirect request.) Full inventory in `evals/triggers/trigger-queries.json`.

**Near-miss requests that must not activate it:** Twelve, across the six categories above plus an unrelated use of the word "prototype" (`Array.prototype`), in the same file.

**How it should be invoked:** Automatically when relevant, and explicitly by name — the Claude default. No `disable-model-invocation`, no `allowed-tools`, no other frontmatter field; `name` and `description` only, per the authoring contract.

## 3. Inputs and expected results

**Required inputs:** At least one relevant product-brief, design-spec or architecture-contract; the concrete uncertainty and the decision waiting on it; the experiment constraints (permitted paths, allowed tools and services, the time or resource bound, and the observable success and failure measures); and the session assignment and write fence before any write. From SKILL-004's Inputs and provenance table and Required context row.

**Optional inputs:** An earlier `prototype-report` — what was already tried and what this iteration changes.

**When information is missing:** A missing required input stays missing, with a reason and the work it blocks. Two decisions worth stating because the specification implies but does not spell them out:

- A missing **time or resource bound** stops the experiment rather than acquiring a default (**proposed**). Basis: SKILL-004 makes the bound part of the required experiment constraints, and an unbounded experiment is not the thing the specification describes.
- A missing **threshold** stops the experiment. Basis: SKILL-004's phase-1 exit requires a plan whose measurements and result are not yet known, which a hypothesis without a threshold cannot satisfy.

**Expected deliverable:** an `experiment-plan` (XPLAN) and a `prototype-report` (XREPORT), plus a standardized handoff.

**Output format and destination:** The package's `assets/` templates. An externally selected destination governs. Where nothing was selected, the defaults are `docs/devforge/experiments/` for XPLAN and XREPORT and `docs/devforge/handoffs/` for the handoff (**both proposed**; basis is the installed `devforge-brainstorm` precedent of a `docs/devforge/<kind>/` map, so a project does not acquire two handoff locations).

**Completion criteria:**

- The plan exists, with hypothesis, threshold, cases and fence, before its measurements and result are known.
- The prototype is identified — location, manifest or reproduction steps — and nothing was written outside the fence.
- Every planned case carries an observation, a failure, or an explicit unavailability with its actual cause.
- The report separates observation from recommendation, names the limits of what was measured, and proposes a disposition whose adoption is still the user's.
- A handoff names the next owner and one real next action.

## 4. Workflow

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | Run a bounded experiment and record its result | XPLAN, prototype, XREPORT, handoff | Required when an experiment could change a decision; skipped entirely when inspection settles it | R1, R2, R3 (all recorded requirements only) |
| P1 | Phase; parent W1 | Specify: hypothesis, cases, observation method, bounded effort | A plan exists before its measurements or result are known | Required | R1 |
| P2 | Phase; parent W1 | Build: implement only enough inside the fence to test the hypothesis | Prototype files and reproduction steps identified | Required | R2 |
| P3 | Phase; parent W1 | Observe: run the planned checks, preserve outputs and environment | Each measurement observed, failed, or explicitly unavailable | Required | not applicable |
| P4 | Phase; parent W1 | Decide: compare evidence to the planned threshold, recommend a disposition and upstream revision | Consumers can distinguish observation from recommendation | Required | R3 |
| T1 | Task; parent P1 | Freeze the plan identity before execution | The plan's digest and where that identity is held | Required | R1 |
| T2 | Task; parent P4 | Propose a disposition for the prototype code | discard / reference / candidate-for-hardening, with `decision_ref` null | Required | R3 |

**Applies when:** W1 applies only when a consequential uncertainty exists that inspection cannot settle. P2 and P3 are skipped when the experiment cannot execute at all; P1 and P4 still produce a plan and a `COULD_NOT_RUN` record.

**Dependencies and completion evidence:** P3 must wait on P1's frozen plan; the evidence is the plan's recorded digest and the identity holding it. P4 must wait on P3's preserved observations; the evidence is the raw output locators in the report's `evidence`. Both go stale when the upstream revision, the prototype bytes or the runtime change.

**Conditional paths:** Experiment cannot execute at all → record `COULD_NOT_RUN` with cause, make no claim, name what would unblock it. Threshold missed → preserve the failure and recommend a revision to the owning skill. Threshold changed by the user → new plan revision, prior revision preserved.

**When to stop or seek clarification:** The resource bound is reached; the question needs authority beyond the declared fence; a conflicting write fence prevents recording the result; a required threshold or bound was never supplied.

## 5. Task-specific rules

**Required standards or conventions:** The `devforge.artifact/v1` envelope on all three outputs. The framework's fixed result vocabulary, unblended. No artifact carries its own digest. Exact upstream references with revision, digest and stable section IDs, with draft-versus-accepted status visible. Package-relative resource links; no dependency on `docs/mvp` at runtime; no developer home path in the package.

**Preferences:** Prefer the project's own artifact map over this package's proposed defaults wherever it has one.

**Actions requiring explicit authorisation:** Adopting a newer upstream revision into a recorded threshold. Promoting prototype code toward production. Using a credential, production data or an external service the constraints did not permit. Amending an accepted architecture decision — which this skill never does; it routes the finding.

**Known pitfalls:** The three framing failure modes opening `SKILL.md` — moving the threshold to fit the result, letting the prototype become the product, claiming a measurement nobody observed. Each is drawn from a SKILL-004 acceptance row rather than invented.

## 6. Tools and supporting resources

**Target environment:** Claude Code on Linux/WSL2, loaded from wherever the client installed the package, operating on a separately supplied consuming project.

**Required tools or integrations:** None that the skill itself requires. The consuming project supplies whatever the experiment measures. The DevForge CLI is optional context, not a dependency of this workflow.

**Access requirements:** Read access to the named upstream documents; write access to the declared fence and the selected artifact destinations. Nothing else, and explicitly not credentials.

**Supporting materials:**

| Resource | Purpose | When it is needed |
|---|---|---|
| `references/framework-context.md` | Ownership split, the CLI commands that exist and their limits, the open integration requirements, paths, vocabulary, packaging | When a command or an enforcement claim is about to be written, or when a result label is chosen |
| `references/recording-rules.md` | Envelope fields, upstream-reference resolution, digest write order, per-template fill guidance | When filling any of the three artifacts |
| `references/experiment-boundaries.md` | The fence, measurement discipline, blocked measurements, reading a result, the disposition table, concurrency, stopping | Phases 1 through 4, and every common case |
| `assets/experiment-plan.md`, `assets/prototype-report.md` | The governing output templates, byte-identical copies | Phases 1 and 4 |
| `assets/handoff.md` | The transfer document | Phase 4 |

**Unavailable dependency behaviour:** Name the unavailable dependency, record `COULD_NOT_RUN` with the actual cause for what it blocks, and continue the work that does not depend on it.

**Enforcement route for required items — requirement only:**

- **Route ID and covered items:** R1 — P1, T1 (plan before measurement).
  - **Requirement and protected action:** No measurement result may be recorded for a case whose plan revision was not frozen before the observation. The protected action is writing an XREPORT observation row.
  - **Observable evidence:** The plan's bytes and their digest, held somewhere the evaluated agent cannot rewrite, with a timestamp ordering relative to the raw evidence files.
  - **State and freshness:** Would live outside the candidate's writable boundary. Invalidated when the plan revision changes.
  - **Intended allow or refuse behaviour:** Refuse the dependent write when no frozen plan identity exists for that revision, or when the frozen bytes differ from the cited plan.
  - **Missing evidence and errors:** Missing frozen identity refuses rather than warns. A warning is advisory, not a refusal.
  - **Recovery and user message:** Name the missing freeze, its owner, and that the plan must be frozen before observations are recorded.
  - **Owner:** Integration owner. The check itself would be compiled into the DevForge CLI.
  - **Feasibility:** Unknown until the integration owner confirms it. Nothing in the current command surface does this.
  - **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

- **Route ID and covered items:** R2 — P2 (the fence).
  - **Requirement and protected action:** No file outside the declared experiment path may be written by experiment work. The protected action is any write outside the fence.
  - **Observable evidence:** The declared fence path from the plan, and the actual set of paths written.
  - **State and freshness:** Would be per-run, bound to the plan revision.
  - **Intended allow or refuse behaviour:** Refuse a write outside the declared path. `devforge isolate` bounds the whole project and is the closest existing containment; it does not implement this.
  - **Missing evidence and errors:** No declared fence means the experiment does not start.
  - **Recovery and user message:** Name the attempted path and the declared fence, and stop the dependent write.
  - **Owner:** Integration owner. **Feasibility:** Unknown. **Status:** Requirement recorded; no gate implemented.

- **Route ID and covered items:** R3 — P4, T2 (threshold integrity and promotion).
  - **Requirement and protected action:** A report may not state a threshold different from its cited plan revision, and a `candidate-for-hardening` disposition may not by itself place prototype files under a policy source root. The protected actions are recording a threshold comparison and promoting files.
  - **Observable evidence:** The threshold text in the frozen plan versus the report; the prototype file set versus the policy's source roots.
  - **State and freshness:** Bound to the plan revision and the policy; invalidated by either changing.
  - **Intended allow or refuse behaviour:** Refuse the report write on threshold mismatch; refuse promotion without an accepted hardening story.
  - **Missing evidence and errors:** An unresolvable plan reference refuses rather than defaulting to the report's own number.
  - **Recovery and user message:** Name both thresholds and the plan revision, and route the divergence to the owner.
  - **Owner:** Integration owner. **Feasibility:** Unknown. **Status:** Requirement recorded; no gate implemented.

The `evals/cases.jsonl` case `XP-B-001` deliberately demonstrates the R3 gap: every deterministic assertion matches on a report that moved its own threshold, and the defect is routed to independent review with a null grader. Recording that is design input; it is not evidence that anything enforces it.

## 7. Acceptance cases — capture only

Captured before the candidate was authored, from SKILL-004's own rows. Eleven tier-B cases in `evals/evals.json`; nine deterministic cases in `evals/cases.jsonl`. Full requirement-to-case mapping in `spec-mapping.md`. None has been executed.

| Case | Example request or input | Expected behaviour |
|---|---|---|
| Typical task | "Use DevForgeAI to prototype the risky part before we commit." | Plan, prototype and result all tied to the original uncertainty |
| Indirect | "Is a quarter of a second realistic at 400 viewers?" | Defines a measurement before claiming a result |
| Missing information | Experiment constraints absent | Names the missing bound and fence as required inputs rather than inventing them |
| Outside scope | "STORY-031 is accepted and ready. Implement it." | Routes to `devforge-develop`; no plan, prototype or report |
| Important variation | Measurements miss the stated threshold under user pressure to reframe | Preserves the failure; routes a proposed revision; does not move the threshold |

**Example of a good deliverable:** `evals/fixtures/good/experiments/XREPORT-001.md` — synthetic, and deliberately a *missed* threshold, because the specification's hardest case is the one that reports a failure honestly.

## 8. Placement and maintenance

**Availability:** Bundled in the `devforgeai` plugin, Claude provider.

**Installation location:** Recorded in section 10. An installed copy is never an alternative source.

**Maintainer:** The assigned Claude skill author, under the coordinator for this scaffolding pass.

**Reasons to revisit:** SKILL-004 revises past revision 2; either output template changes; the `devforge-evaluate-expert` runner interface changes; the DevForge CLI gains any of the four missing integrations; a named sibling skill is implemented, renamed or retired.

## 9. Authoring decision and progress

**Current status:** Authored — first scaffold, unevaluated.

**Working specification and target paths:** This document at `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/authoring/design/skill-design-spec.md`; the candidate at `providers/claude/plugins/devforgeai/skills/devforge-prototype/`.

**Search scope and limitations:** Searched `providers/claude/plugins/devforgeai/skills/` and `providers/codex/plugins/devforgeai/skills/` at base `c17e758417da64928a0f47fc2600304465ac3f3c`, plus `docs/mvp/roster.md`. Not searched: `~/.claude/skills`, any managed settings directory, any `--add-dir` directory, and project-local `.claude/skills` installations. The result this establishes is "no suitable skill found in the searched inventory"; it does not establish that no such skill exists anywhere.

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
|---|---|---|---|
| `devforge-develop` (Claude, draft) | Both produce working code | Develop implements an accepted, fully specified story behind the RED/GREEN gate. A prototype answers an open question and is explicitly not production code. | Separate workflow |
| `devforge-brainstorm` (Claude, draft) | Both handle uncertainty | Brainstorm handles an unformed problem; a prototype needs a concrete uncertainty and a decision waiting on it | Separate workflow |
| `devforge-review` (Claude, draft) | Reads an experiment-plan per the roster | Reviews a candidate's correctness and readiness; does not run experiments | Separate workflow |
| `devforge-project-expert-creator` (Claude, `4999f31`) | Followed as the builder here | An authoring workflow for project expertise; not a duplicate of what it helps author | Separate workflow |
| Codex inventory | `devforge-evaluate-expert` exists there only | No Codex `devforge-prototype` exists, so there is no port source for this skill | Create from specification |

**Selected approach and rationale:** **Create.** No `devforge-prototype` exists in either provider's canonical source at the searched base, the roster records SKILL-004 as Proposed, and the boundary against develop, design, change and brainstorm is expressible in terms of activation and scope rather than subject matter. The destination did not exist at base; nothing was overwritten.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| Four workflow phases with exit conditions | Specify, Build, Observe, Decide | SKILL-004 Workflow table | Settled by specification |
| Output IDs XPLAN and XREPORT | Fixed prefixes | SKILL-004 Outputs table | Settled by specification |
| Near-miss exclusion naming develop | Required in the description | SKILL-004 "Does not activate for" | Settled by specification |
| Three further exclusions (design, change, brainstorm) | Included in the description | Roster provenance flow and skill boundaries | **Proposed** — the specification names only develop |
| XPLAN/XREPORT default destination | `docs/devforge/experiments/` | `devforge-brainstorm` precedent | **Proposed** |
| Handoff default destination | `docs/devforge/handoffs/` | `devforge-brainstorm` precedent | **Proposed** |
| Default fence path | `experiments/<XPLAN-ID>/` | Keeps the prototype identifiable and outside a policy source root | **Proposed** |
| Missing time/resource bound | A missing required input, not a default | SKILL-004 Required context | **Proposed** reading of the specification |
| Three reference files rather than shipped contract copies | `framework-context`, `recording-rules`, `experiment-boundaries` | Authoring contract's progressive-disclosure guidance | **Proposed** packaging decision |
| No `scripts/` | The runner lives in `devforge-evaluate-expert` | Language policy; the packet prefers none | Settled |
| No managed-runtime section | SKILL-004 describes no managed operation | Assignment; specification silence | Settled |

**Authored or changed files:** The full package and this evidence tree. Inventory with digests in `file-manifest.json`.

**Material unresolved dependencies or enforcement gaps:** The four missing integrations in `references/framework-context.md` (sub-project fence, pre-execution plan freeze, promotion check, threshold immutability), recorded as R1–R3 above. The deterministic eval arm depends on a runner in a package that is source-only and under independent review. None of these is described as active enforcement anywhere in the package.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

**Framework and provider:** DevForgeAI at base `c17e758417da64928a0f47fc2600304465ac3f3c`, branch `author/claude-devforge-prototype-scaffold-20260910`. Claude provider. Client version not recorded — no client was observed loading this package.

**Assignment and authority:** Coordinator-issued scaffold packet for SKILL-004, Claude package, with an exclusive fence over `providers/claude/plugins/devforgeai/skills/devforge-prototype/**` and `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/authoring/**`. Integration owner for shared changes: not this author.

**Roster role:** SKILL-004, an accepted roster role recorded as "Proposed" in `docs/mvp/roster.md`. Authoring a scaffold does not amend the roster or certify a framework capability, and this pass changed no roster or package-index file.

**Selected source records:**

| Record | Governing source | Revision | SHA-256 | Purpose | Gaps |
|---|---|---|---|---|---|
| Governing specification | `docs/mvp/specifications/skill-004-devforge-prototype.md` | rev 2, at base | `e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c` | Required behaviour | Silent on destinations and default fence; recorded as proposals |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | rev 3, at base | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Packaging, tiers, eval fixtures | none |
| Artifact contract | `docs/mvp/artifact-contract.md` | rev 2, at base | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Envelope, provenance, digests | none |
| Execution contract | `docs/mvp/execution-contract.md` | rev 3, at base | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Worktree ownership, concurrency | none |
| Development language policy | `docs/development-language-policy.md` | at base | `3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f` | Rust authority; the Python evaluation exception | none |
| Bounded delivery | `docs/learned-behaviors/bounded-delivery.md` | at base | `22a0388c3a4afdb32beace2fb0082ec02acea885e45650f0b42925b76c09e7ae` | Finish-line discipline | none |
| Roster | `docs/mvp/roster.md` | at base | `ea35b825f8d2ea58ea0eb20b77c2fdd47df1dc2ddb3bbcfef3b032874e5f57bc` | Provenance flow, consumer edges | none |
| Template for this document | builder `assets/skill-design-spec.md` | `4999f31` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` | This document's structure | Section 11 omitted as not applicable |

**Canonical source and generated runtime mapping:**

| Purpose | Path | Identity | Ownership |
|---|---|---|---|
| Canonical framework source | `providers/claude/plugins/devforgeai/skills/devforge-prototype` | `file-manifest.json` | This author, within the assigned fence |
| Installed project copy | A consuming project's `.claude/skills/devforge-prototype` | Not generated | Integration owner |
| Plugin export | Not generated | — | Integration owner |
| Working specification | This document | Evidence tree above | This author |

A provider source folder alone is not a discovered installation. No installation, export or binding was performed.

**Package derivations:** Recorded in the package's own `references/derivation.json` rather than duplicated here, per the template's note that the maintenance record is the appropriate home. That record carries no digest of itself.

**Authority, contract, installation or provider gaps:** The four missing CLI integrations (R1–R3). The `devforge-evaluate-expert` runner dependency. No client was observed, so tier A is unobserved rather than negative.

**Preserved boundaries:** `docs/mvp` and every specification, template and contract in it; `docs/mvp/package-index.json` and the roster; provider hooks, manifests and agents; every sibling skill in both providers; the companion DevForge repository's gates, policy and tests. None was read for anything but reference and none was modified.

**Authoring and release status:** Authored candidate. Evaluation and adoption are separate; a source or package identity establishes no activation, quality or release readiness.

## 11. Evaluator repair intake

Not applicable. This is a first scaffold with no evaluator handoff to intake.

## 12. Change record

**Identity and authoring scope:** Scaffold pass `claude-scaffolding-20260910`, `devforge-prototype`, 2026-09-10. Create action, Claude provider, within the exclusive fence named in section 10.

**Input references:** The eight selected source records in section 10, plus the builder files listed with their `4999f31` digests in the package's `references/derivation.json`, plus the `devforge-evaluate-expert` runner, graders, runner-interface and cases at `e52ac596cbf790dfa156d883852d392c512fdbcc`.

**Change mapping:**

| Change ID | Type | Disposition | New path | Summary |
|---|---|---|---|---|
| CHG-001 | new | applied | `SKILL.md` | Instructions authored from SKILL-004; four phases with exit conditions, inputs table, common cases, stopping condition |
| CHG-002 | new | applied | `assets/experiment-plan.md`, `assets/prototype-report.md` | Byte-identical copies of the governing templates; digests verified equal to source |
| CHG-003 | new | applied | `assets/handoff.md` | Bounded adaptation of the shared handoff template for this skill's transfer |
| CHG-004 | new | applied | `references/framework-context.md`, `references/recording-rules.md`, `references/experiment-boundaries.md` | Distilled and authored references; no `docs/mvp` dependency at runtime |
| CHG-005 | new | applied | `references/derivation.json`, `references/sources.md` | Maintenance and source records |
| CHG-006 | new | applied | `evals/**` | 11 tier-B cases, 9 deterministic cases, 22 trigger queries, 19 synthetic fixtures |

**New canonical source manifest:** `file-manifest.json` in this authoring directory. It contains no digest of itself.

**Resulting specification identity:** This document, revision 1, at the path in section 9.

**Preserved behaviour and requirements:** No prior candidate existed. Nothing outside the fence was read for modification or modified.

**Derivations and generated-copy work remaining:** No installed copy or export was generated. `docs/mvp/package-index.json` still records nothing for SKILL-004; updating the roster or index is the integration owner's action and was explicitly outside this fence.

**Deferred proposals, gaps and evaluation prerequisites:** Every **proposed** row in section 9 awaits a decision. Tiers A, B and C are `NOT_RUN`; the deterministic arm additionally depends on the `devforge-evaluate-expert` package, which is itself unevaluated.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

**Next handoff:** `handoff.md` in this authoring directory, allocating an independent evaluator as next owner.

## Evaluation coverage proposed

Accepted baseline: none — this is a first candidate, so **every one of the eleven tier-B cases uses `without_skill`**.

*Corrected in repair pass 1 (finding F-002, CHG-002).* This paragraph previously said case 8 named `old_skill` because a prior report artifact is supplied as its fixture, and that the arm would become `NOT_APPLICABLE` if no earlier candidate existed. Both halves were wrong and are withdrawn. A fixture supplied *to* a case is an input to that case, not a baseline arm of the comparison; and `NOT_APPLICABLE` is reserved for a stated scope exclusion, which an absent baseline is not. No `devforge-prototype` exists at base `c17e758417da64928a0f47fc2600304465ac3f3c`, so `old_skill` had nothing to resolve to. The original text is preserved at commit `e199230858d871926fff2d55de8b015fa0ce335e`.

Proposed coverage: tier A from `evals/triggers/trigger-queries.json` in a fresh terminal against an actual installation, reporting the explicit-invocation entries separately and never as implicit activation evidence; tier B from `evals/evals.json` with the skill path supplied; tier C from an actual export or project-local installation in a project where `docs/mvp` is absent, checking that `assets/` and `references/` resolve inside the installed package and that `evals/` is absent from the installed copy.

Missing evidence: everything. No tier has been observed. This skill proposes evaluation coverage; a separate evaluator and an independent reviewer assess it, and the appearance of the words "validate" or "install" in a request does not by itself select a level of evidence.
