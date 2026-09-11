# Skill design specification: devforge-design

Working design document, filled from the builder's `assets/skill-design-spec.md` template. This is a DevForgeAI authoring document. It carries the design, the framework authority and source mapping, and the change record. It does not certify a skill, and completing it establishes nothing about behaviour.

**No questions were asked of a user during this authoring.** Every material decision below was recovered from the governing specification, the shared templates and contracts, or the roster. Where a source is silent, a proposed default is recorded and labelled `proposed`. A proposal is not a requirement anyone gave.

## 1. Identity and purpose

**Skill name:** `devforge-design`

**Purpose:** Make selected requirements reviewable as user journeys, screen states and local mockups before anyone commits to implementation behaviour. Project-specific guidance changes the result because the flows must resolve against the project's accepted requirements and its approved UI stack, not against generic UI advice.

**Description for discovery:** Authored into `SKILL.md` frontmatter. It states what the skill does, the explicit, direct-domain and indirect activating conditions taken from SKILL-003's use-case inventory, and the near-miss exclusions naming the sibling skill that owns each. It closes by narrowing the overloaded word "design" to the user experience, excluding schema, API, class-structure and pattern work. Length 950 characters, inside the client's documented 1,536-character listing budget.

**Intended users:** Anyone holding accepted or user-stated requirements who needs the experience reviewed before build.

## 2. Scope and activation

**Use this skill when:** mockups, wireframes or screen designs are requested for something already scoped; when someone asks what a screen should look like, how a user gets through a flow, or what happens on the error, loading or empty paths; when design feedback needs to be incorporated as traceable revisions.

**Outside its scope:**

| Near miss | Owner | Basis |
| --- | --- | --- |
| A technical uncertainty needing execution | `devforge-prototype` (SKILL-004) | SKILL-003 "Does not activate for" |
| A production patch or implementing an accepted story | `devforge-develop` (SKILL-009) | SKILL-003 "Does not activate for" |
| Working out what to build or what is in scope | `devforge-define-product` (SKILL-002) | Roster provenance flow: product-brief is this skill's upstream |
| Changing an accepted requirement | `devforge-change` (SKILL-012) | Roster: change routes to the owning skill for the affected artifact |
| Database schema, API surface, class structure, design-pattern choice, system design | Not this skill | Added by the author: SKILL-003's user goal is user journeys, screen states and mockups. `proposed` |

**Example activating requests:** "Use DevForgeAI to design mockups for this MVP" (specification direct request). "Show how a customer would complete signup, including errors and empty states" (specification indirect request). Plus the direct-domain and indirect entries in `evals/triggers/trigger-queries.json`.

**Near-miss requests that must not activate it:** the four negative categories in the trigger file - non-UI design, prototype, develop, define-product - plus ordinary tasks.

**How it should be invoked:** Automatically when relevant, and explicitly by name. `proposed`; SKILL-003 does not restrict invocation, and the roster states the MVP uses explicit native skill invocation, which this does not contradict.

## 3. Inputs and expected results

**Required inputs:** product-brief (requirement IDs and user goals); existing UI conventions and target device constraints where they exist.

**Optional inputs:** architecture-contract (approved UI stack and constraints, consume-only); an existing design-spec (current flows and accepted decisions); prototype-report or change-request (conditional - observed feedback or the requested revision); prior user feedback.

**When information is missing:** A missing required input stays missing, with its reason and the work it blocks, recorded in `missing_inputs`. Work that does not depend on it continues.

The specific case that matters now: `devforge-define-product` is specified and not implemented, so no product-brief usually exists. Proposed default, recorded in `SKILL.md` and `references/recording-rules.md`: take the user's requirement statements, record them in the coverage table marked `user-stated`, put `product-brief` in `missing_inputs`, keep `status: draft`, and never fabricate a `PROD` artifact ID or digest. `proposed`.

**Expected deliverable:** a design-spec (`UX` prefix) with linked mockup assets, plus a handoff.

**Output format and destination:** `devforge.artifact/v1` envelope from the package's own `assets/design-spec.md`. An externally selected destination governs. Proposed project defaults where nothing was selected: `docs/devforge/design/` for the design-spec, `docs/devforge/handoffs/` for the handoff, `docs/devforge/design/mockups/<UX-ID>/` for mockup assets. The first two follow the artifact contract's suggested directory list; the mockup subdirectory is the author's proposal. `proposed`.

**Completion criteria:**

- Design scope and its exclusions are explicit, or a NOT_APPLICABLE result names the change and why no UI is affected.
- Every flow and state carries a requirement reference or an explicit note of why it has none.
- Mockup files exist at recorded paths with digests, exact preview instructions, and an honest inspection result.
- Feedback and open questions are recorded with disposition and the phase or skill that would resolve each.
- The design-spec's declared inputs resolve; the handoff names actual identities, real limits and one concrete next task.

## 4. Workflow

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | Design and iterate the user experience for selected requirements | design-spec plus mockup assets plus handoff | `proposed`: required when the change has a user-facing surface, not applicable when it does not | R1 |
| P1 | Phase; parent W1 | Frame: choose the user task, affected requirements and existing design constraints | Design scope and missing decisions are explicit | `proposed`: required | R1 |
| P2 | Phase; parent W1 | Model: journeys, plus normal, loading, empty, error and keyboard behaviour where relevant | The flow covers the meaningful success and failure paths | `proposed`: required | R1 |
| P3 | Phase; parent W1 | Render: browser-viewable mockups with exact preview instructions | Mockup files exist and can be inspected, or an execution limitation is recorded | `proposed`: required | R2 |
| P4 | Phase; parent W1 | Iterate: incorporate feedback as traceable revisions; identify unresolved questions | The accepted revision and its remaining uncertainties are identifiable | `proposed`: conditional on feedback existing | R1 |
| T1 | Task; parent P1 | Resolve each declared upstream reference against its revision and digest before use | Reference resolves, or staleness is recorded | `proposed`: required | R1 |
| T2 | Task; parent P3 | Hash each mockup asset after its bytes are final and record the digest in the design-spec | Asset table digests match the bytes on disk | `proposed`: required | R2 |
| T3 | Task; parent P4 | Write the handoff after the design-spec is hashed, excluding its own digest | Handoff carries the design-spec digest; no self-digest | `proposed`: required | R1 |

**Applies when:** P4 applies only when feedback or a change request exists. W1 is not applicable when the change has no user-facing surface; that outcome is itself recorded.

**Dependencies and completion evidence:** None of these are enforced. Each row's evidence would be the produced artifact's bytes. Freshness is invalidated by a changed upstream revision, a changed installed skill identity, or a changed base commit.

**Conditional paths:** No product-brief exists, so requirements come from the user - see section 3. No browser tooling exists, so inspection is `COULD_NOT_RUN` with its cause and files plus manual steps are supplied. An ownership collision exists, so dependent writes stop.

**When to stop or seek clarification:** a missing requirement that materially changes a flow being declared ready; unavailable visual tooling where a visual check is the claim being made; a write fence or ownership collision.

## 5. Task-specific rules

**Required standards or conventions:** the `devforge.artifact/v1` envelope; the fixed result vocabulary (`NOT_EVALUATED`, `NOT_RUN`, `COULD_NOT_RUN`, `NOT_APPLICABLE`), never blended; stable `FLOW-nnn` and `UXS-nnn` IDs; the project's approved UI stack where one exists; the artifact contract's no-self-digest rule and its upstream-reference resolution.

**Preferences:** self-contained local HTML and CSS with no build step and no network fetch, so a reviewer can open the file. Approved existing UI tooling takes precedence where the project has adopted one. `proposed`.

**Actions requiring explicit authorisation:** adopting a newer upstream revision; departing from an accepted architecture rule; writing outside the assigned fence. None of these is authorised by this skill.

**Known pitfalls:** describing rendered appearance nobody observed; recording an AI proposal as a user decision; inventing a `PROD` artifact ID to fill an upstream slot; manufacturing a UI task for a backend-only change; treating a newer document's `accepted` status as the user's adoption.

## 6. Tools and supporting resources

**Target environment:** Claude Code on Linux/WSL2. Client version `unknown; not observed` - no client version probe was run during this authoring.

**Required tools or integrations:** none beyond file reading and writing. A browser or rendering tool is optional and its absence is a recorded limitation, not a blocker.

**Access requirements:** read access to the project's artifact store and the referenced upstream documents; write access to the selected design and handoff destinations.

**Supporting materials:**

| Resource | Purpose | When it is needed |
|---|---|---|
| `assets/design-spec.md` | The design-spec output shape | Whenever a design-spec is written |
| `assets/handoff.md` | The handoff shape | At the end of every run that produces an artifact |
| `references/recording-rules.md` | Envelope fields, upstream resolution, write ordering, the no-product-brief case, research recording | Filling frontmatter; a reference that does not resolve; a blocked check |
| `references/mockups-and-preview.md` | What to build, preview instructions, inspection honesty, what a mockup does not prove | The Render phase |
| `references/sources.md` | What was read while authoring, with dates and claims | Maintenance |
| `references/derivation.json` | Source-to-package derivation records | Refreshing a copied template |

**Unavailable dependency behaviour:** record the specific limitation and its cause, supply what can be supplied, and continue the independent work.

**Enforcement route for required items:**

- **Route ID and covered items:** R1; W1, P1, P2, P4, T1, T3.
- **Requirement and protected action:** before a design-spec is treated as an accepted input by a downstream consumer, its declared upstream references should resolve to the cited revision and digest, and no required field should hold a template placeholder. The protected action is downstream consumption.
- **Observable evidence:** the design-spec's bytes - its frontmatter fields, its `upstream` entries, and the referenced files' digests. This is proof of what was referenced, never that the design is any good.
- **State and freshness:** the artifact lives in the project's artifact store. It goes stale when a referenced upstream revision changes or the producing skill identity changes.
- **Intended allow or refuse behaviour:** refuse the dependent consumption when a required field holds a placeholder or a declared upstream reference does not resolve. A warning would be advisory, not a refusal.
- **Missing evidence and errors:** an unreachable referenced path is a refusal with the cause, not a pass.
- **Recovery and user message:** name the field or reference, and the smallest action that resolves it.
- **Owner:** Integration owner. The check itself would be compiled into the DevForge CLI and invoked by whatever wiring that owner selects; this document records the requirement, not an implementation.
- **Feasibility:** Unknown until the integration owner confirms it.
- **Status:** Requirement recorded. **No gate is implemented, activated or executed by this skill.** The observed `devforge --help` surface contains no subcommand that reads a design-spec.

- **Route ID and covered items:** R2; P3, T2.
- **Requirement and protected action:** a mockup asset's recorded digest should match its bytes, and an `Inspection result` other than `NOT_RUN` or `COULD_NOT_RUN` should carry a resolvable evidence locator. The protected action is presenting the design as visually reviewed.
- **Observable evidence:** the asset file's digest and the design-spec's `evidence` entries.
- **State and freshness:** invalidated by any edit to the asset after hashing.
- **Intended allow or refuse behaviour:** refuse the "visually reviewed" claim when the digest mismatches or the evidence locator is absent or unresolvable.
- **Missing evidence and errors:** absent evidence refuses the claim; it does not refuse the design-spec.
- **Recovery and user message:** name the asset, the mismatch, and that re-hashing after the last edit resolves it.
- **Owner:** Integration owner.
- **Feasibility:** Unknown until the integration owner confirms it. Enforcement requested; not confirmed available.
- **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

## 7. Acceptance cases - capture only

Written before the candidate and carried into `evals/evals.json` and `evals/cases.jsonl`. This skill's author does not run them. Every outcome is `NOT_RUN`.

| Case | Example request or input | Expected behaviour |
|---|---|---|
| Direct activation | Ask for mockups of an accepted workflow | Creates assets and a design record linked to requirement IDs |
| Indirect activation | Ask what happens when a signup form fails | Includes a concrete error state and recovery path |
| Missing tooling | Browser preview is unavailable | Supplies files and truthful manual preview steps; does not claim visual inspection |
| Scope preservation | An established project has an approved UI stack | Uses its conventions or records an explicit proposal |
| Out of scope | Ask for a database index with no UI impact | Does not manufacture a UI design task |
| Concurrent writer | Another session holds the design destination | Stops dependent writes and reports the collision without deleting or resetting anyone's work |
| Stale upstream | A cited revision no longer matches the live bytes | Marks the prior evidence stale and routes a new check; does not relabel newer bytes as the old revision |
| Placeholder in a required field | A design-spec still holding `{{...}}` is presented as finished | The result stays a draft and cannot be presented as ready |
| Blocked check | A requested check has no implementation | Records `COULD_NOT_RUN` with the actual cause; the absence of an error is not `PASS` |
| Installed resources | The package is installed in a consuming project without the DevForgeAI docs tree | Templates and references resolve inside the installed package; outputs land in the project's artifact map |

## 8. Placement and maintenance

**Availability:** the DevForgeAI Claude plugin.

**Installation location:** recorded in section 10. An installed copy is never an alternative source.

**Maintainer:** the assigned Claude skill author; shared templates and contracts belong to the integration owner.

**Reasons to revisit:** SKILL-003 is revised; a shared template changes; `devforge-define-product` becomes implemented, changing the no-product-brief default; a `devforge` subcommand that reads a design-spec appears; the evaluate-expert runner's case schema is committed and differs from what was authored against; a demonstrated activation failure against the trigger set.

## 9. Authoring decision and progress

**Current status:** authored scaffold; not validated.

**Working specification and target paths:** this document; target `providers/claude/plugins/devforgeai/skills/devforge-design/`.

**Search scope and limitations:** The Claude canonical source inventory at base commit `c17e758417da64928a0f47fc2600304465ac3f3c` was listed in full: `providers/claude/plugins/devforgeai/skills/` contains exactly `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator` and `devforge-review`. No `devforge-design` exists there.

Locations **not** searched, and therefore not claimed empty: the Codex provider source (a different owner's fence and outside this assignment); installed project-local `.claude/skills` copies and exported plugins (generated artifacts, never alternative sources); personal `~/.claude/skills`; any enterprise managed settings directory; any `--add-dir` inventory. Candidates were read as source only - nothing was installed, run or tested. The honest statement is **"no suitable skill found in the searched inventory"**, not that no such skill exists anywhere.

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
|---|---|---|---|
| `devforge-brainstorm` (`providers/claude/.../devforge-brainstorm`) | Early-stage exploration; produces a durable ledger; same envelope and recording discipline | Explores what to build; does not produce journeys, screen states or mockups, and has no requirement-coverage obligation | Separate workflow. Used as the Claude conventions exemplar only |
| `devforge-develop` (`providers/claude/.../devforge-develop`) | Touches user-facing code | Implements one accepted story under the RED/GREEN gate; is downstream of design | Separate workflow |
| `devforge-review` (`providers/claude/.../devforge-review`) | Reads a design-spec as an input | Judges a candidate's correctness and readiness; produces a review-report | Separate workflow |
| `devforge-project-expert-creator` (`providers/claude/.../devforge-project-expert-creator`) | Authoring workflow | Creates project expertise, not a user experience. Used here as the builder, source-loaded | Separate workflow |

**Selected approach and rationale:** **Create.** SKILL-003 is an accepted roster role with its own artifact type (`design-spec`), its own template, and its own place in the provenance flow. No searched candidate owns that workflow, and no candidate could absorb it without blurring its own activation. The destination directory did not exist before this authoring; there was no collision to reconcile.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| Frontmatter fields | `name` and `description` only | Packet assignment and authoring contract | Settled |
| Description content | Explicit, direct-domain and indirect phrasings plus near-miss exclusions naming siblings | SKILL-003 use-case inventory and roster | Settled |
| Non-UI "design" exclusion | Schema, API, class structure, pattern and system design are excluded by name | Proposed assumption by the author; SKILL-003 does not name them | `proposed` |
| No-product-brief handling | User-stated requirements, `missing_inputs`, `draft` status, no fabricated `PROD` ID | Proposed assumption; follows the artifact contract's prohibition on template filler | `proposed` |
| Mockup destination | `docs/devforge/design/mockups/<UX-ID>/` when nothing is selected | Proposed assumption; extends the artifact contract's suggested `design` directory | `proposed` |
| Mockup technology | Self-contained local HTML and CSS, no build step, no network fetch | Proposed reading of SKILL-003 phase 3 ("browser-viewable mockups with local HTML/CSS") | `proposed` |
| Inspection default | `NOT_RUN` unless a rendering tool was actually used | Template default plus SKILL-003 "does not claim visual inspection" | Settled |
| Managed-runtime section | Omitted | SKILL-003 does not require managed operation; packet forbids copying it without that requirement | Settled |
| Scripts directory | None | Packet prefers none; no deterministic operation in this workflow justifies one | Settled |
| Reference count | Two prose references plus `sources.md` and `derivation.json` | Bounded delivery; progressive disclosure | `proposed` |
| Eval case schema | Port-analysis section 4.4 and 4.6 | Packet instruction; the evaluate-expert scaffold commit did not exist | `proposed`, dependency pending |

**Authored or changed files:** the 23 package files listed in `../file-manifest.json`, plus this authoring evidence set.

**Material unresolved dependencies or enforcement gaps:**

1. No `devforge` subcommand reads a design-spec, resolves its upstream references, or verifies a mockup digest. R1 and R2 are recorded requirements with no implementation.
2. The `devforge-evaluate-expert` Python JSONL runner and graders are not committed. `evals/cases.jsonl` is authored against a documented schema, not an observed interface.
3. `devforge-define-product` is not implemented, so this skill's required upstream normally does not exist.
4. Every downstream consumer of `design-spec` - prototype, architect, plan, change - is unimplemented; review and develop exist as drafts.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

**Framework and provider:** DevForgeAI worktree `claude-scaffold-design-20260910`, branch `author/claude-devforge-design-scaffold-20260910`, base commit `c17e758417da64928a0f47fc2600304465ac3f3c`. Provider: Claude. Claude Code client version: `unknown; not observed` - no version probe was run. Consuming project: none; this is framework authoring, not a project engagement.

**Assignment and authority:** operator task packet at `tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-design.md` in the workspace root. No `SESSION` record artifact exists, so `execution_ref` is `null` with the packet named in `missing_inputs`. Integration owner: unassigned in this packet; shared contracts, hooks, agents, `docs/mvp` and the package index are outside the fence and untouched.

**Roster role:** SKILL-003, an accepted roster role. Authoring it does not amend the roster, promote the skill, or certify a framework capability. `docs/mvp/package-index.json` was not touched; recording this package's readiness there belongs to the integration owner.

**Selected source records:**

| Record | Governing source | Revision | SHA-256 | Purpose | Gaps |
|---|---|---|---|---|---|
| Governing design specification | `docs/mvp/specifications/skill-003-devforge-design.md` | `c17e758` | `4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb` | Accepted scope, phases, outputs, acceptance cases | None; matches the packet's declared digest |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | `c17e758` | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Packaging, evals, tiers | None |
| Artifact contract | `docs/mvp/artifact-contract.md` | `c17e758` | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Envelope, provenance, no-self-digest | None |
| Execution contract | `docs/mvp/execution-contract.md` | `c17e758` | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Ownership collision, command honesty | None |
| Roster | `docs/mvp/roster.md` | `c17e758` | `ea35b825f8d2ea58ea0eb20b77c2fdd47df1dc2ddb3bbcfef3b032874e5f57bc` | Provenance flow in and out | None |
| Output template | `docs/mvp/templates/devforge-design/design-spec.md` | `c17e758` | `5a30b17a40a52be8c1efb453415d0e77d3406c29c71674408a5506bf5e6ab661` | design-spec shape | None |
| Shared handoff template | `docs/mvp/templates/shared/handoff.md` | `c17e758` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | handoff shape | None |
| Template used for this document | Builder `assets/skill-design-spec.md` at commit `4999f31` | `4999f31` | see `../authoring-notes.md` | Working design shape | Builder is a draft under independent review |

**Canonical source and generated runtime mapping:**

| Purpose | Path | Identity | Ownership |
|---|---|---|---|
| Canonical framework source | `providers/claude/plugins/devforgeai/skills/devforge-design/` | `../file-manifest.json` | This author |
| Installed project copy | not generated | not generated | Integration owner |
| Plugin export | not generated | not generated | Integration owner |
| Working specification | this document | `../handoff.md` records its digest | This author |

**Package derivations:** recorded in the package's own `references/derivation.json`; not duplicated here.

**Authority, contract, installation or provider gaps:** the four items in section 9. Each affects a dependent claim, not this authoring.

**Preserved boundaries:** `docs/mvp` and every specification, template and contract in it; `docs/mvp/package-index.json`; the roster; provider hooks, agents and plugin manifests; every sibling skill including the builder; the Codex provider tree; the companion DevForge repository's gates, policy and tests. None was read for writing and none was modified.

**Authoring and release status:** Authored candidate. Evaluation and adoption are separate. A source or package identity establishes no activation, quality or release readiness.

## 11. Evaluator repair intake

Not applicable. This is a first scaffold; no evaluator report or repair specification exists.

## 12. Change record

**Identity and authoring scope:** scaffold of `devforge-design` (SKILL-003) for the Claude provider, 2026-09-10, in worktree `claude-scaffold-design-20260910` on branch `author/claude-devforge-design-scaffold-20260910` from base `c17e758417da64928a0f47fc2600304465ac3f3c`. Requested action: create. Permitted paths: the package directory and this authoring evidence directory.

**Input references:** section 10's table and the package's `references/derivation.json`.

**Change mapping:**

| Change ID | Type | Disposition | Old path and SHA-256 | New path | Summary |
|---|---|---|---|---|---|
| CHG-001 | new file | applied | absent | `providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md` | The skill instructions |
| CHG-002 | template copy | applied | absent | `.../assets/design-spec.md` | Exact copy of the governing output template |
| CHG-003 | template copy | applied | absent | `.../assets/handoff.md` | Exact copy of the shared handoff template |
| CHG-004 | new files | applied | absent | `.../references/` | Two prose references plus `sources.md` and `derivation.json` |
| CHG-005 | new files | applied | absent | `.../evals/` | 10 cases, 10 JSONL cases, 12 fixture files, 24 trigger queries |

Digests for every new file are in `../file-manifest.json`.

**New canonical source manifest:** `../file-manifest.json`, 23 package-relative paths. It does not record its own digest.

**Resulting specification identity:** this document, revision 1, at this path. Its digest is recorded in `../handoff.md`.

**Preserved behaviour and requirements:** no existing behaviour was changed; nothing existed at the destination.

**Derivations and generated-copy work remaining:** no installed copy and no plugin export was generated. That is the integration owner's action.

**Deferred proposals, gaps and evaluation prerequisites:** section 9's unresolved dependencies, and the open items in `../authoring-notes.md`.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

**Next handoff:** `../handoff.md`. The next owner is an independent evaluator. A prepared handoff is not a receiving invocation; no evaluation was launched.

## Evaluation coverage proposed

The candidate is the package at `../file-manifest.json`. There is no prior accepted baseline for this skill, so tier B compares against `without_skill` rather than `old_skill`. Tier C requires an actual installed or exported copy in a consuming project where the DevForgeAI docs tree is unavailable; that installation does not yet exist. Tier A requires a fresh terminal and the trigger set in `evals/triggers/trigger-queries.json`, whose split is fixed and must not enter an author loop.

Contract order applies: required C observations before B or A admission for this candidate. All three tiers are `NOT_RUN`. The Codex Routine/Full manual-mode policy is `NOT_APPLICABLE` to this Claude package until an owner selects an equivalent for it.

This author proposes coverage. A separate evaluator and an independent reviewer assess it.
