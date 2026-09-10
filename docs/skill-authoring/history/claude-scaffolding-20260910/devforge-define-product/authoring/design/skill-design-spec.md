# Skill design specification: devforge-define-product

Working design document, derived from the frozen builder's `assets/skill-design-spec.md` and filled here rather than in the package. This is a DevForgeAI authoring document. It carries the design, the framework authority and source mapping, and the change record. It does not certify a skill, and completing it establishes nothing about behaviour.

**Governing template:** `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/assets/skill-design-spec.md` at commit `4999f3106565c5e320d1f1a7db066b437e4e94be` in the sibling worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`.

**Governing specification:** SKILL-002, revision 2, `docs/mvp/specifications/skill-002-devforge-define-product.md`, sha256 `3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf` at base commit `c17e758417da64928a0f47fc2600304465ac3f3c`.

**No questions were asked.** The packet instructed the author to recover every material decision from the specification, templates and contracts and to record proposed defaults where those sources are silent. Every row below marked **proposed** is the author's default awaiting an owner's answer; silence is not approval. Rows marked **settled** are traceable to a named source.

Section 11 (evaluator repair intake) is omitted: this is a first authoring pass, not a repair.

## 1. Identity and purpose

**Skill name:**
`devforge-define-product`

**Purpose:**
Turn selected ideas and the evidence behind them into a bounded MVP or later release scope with measurable outcomes, requirements and explicit non-goals, recorded in a product brief that later phases can trace back to its origins. Source: SKILL-002 "User goal" row. Settled.

**Description for discovery:**
Written into the package frontmatter. It states what the skill does, the four situations that should select it (define the MVP from a ledger, the smallest version worth shipping and how to tell it helped, cutting an over-grown scope, amending an existing accepted brief), and four near-miss exclusions naming the sibling that owns each: devforge-brainstorm, devforge-design, devforge-architect/devforge-develop, devforge-release. Well inside the client's documented 1,536-character truncation for the skill listing.

**Intended users or role:**
Whoever is deciding what to build next - typically the person who owns the product decision, not a role title. Proposed; the specification does not name a role.

## 2. Scope and activation

**Use this skill when:**
Defining or changing a release scope, including proportionate discovery and feasibility research within the user's own scope. Source: SKILL-002 "MVP support decision" row. Settled.

**Outside its scope:**

| Nearby request | Owner |
| --- | --- |
| Exploring a problem nobody has framed yet | devforge-brainstorm |
| Restyling or laying out an already accepted screen | devforge-design (SKILL-002 "Does not activate for") |
| Approved implementation detail, stack selection | devforge-architect, devforge-develop (SKILL-002 "Does not activate for") |
| Shipping an already accepted build | devforge-release (SKILL-002 acceptance case "Out of scope") |
| Assessing a change to adopted behaviour before a new brief revision | devforge-change (SKILL-002 "Rework") |

The brainstorm exclusion is the author's addition and is the closest miss of the five: the specification names design, architect and develop, and the roster's provenance flow puts brainstorm immediately upstream. **Proposed**, on the basis that a request with no framed problem is brainstorm's job and that the sibling's own description already claims it.

**Example activating requests:**
Recorded in `evals/triggers/trigger-queries.json`, categories `explicit_invocation`, `direct_domain` and `indirect`, with a fixed train/validation split. Two of them are the specification's own Direct and Indirect request phrasings and are assigned to `train` for that reason. No validation-split text appears in SKILL.md.

**Near-miss requests that must not activate it:**
Recorded in the same file, categories `negative_early_exploration`, `negative_visual_design`, `negative_implementation`, `negative_release`, `negative_ordinary_task`.

**How it should be invoked:**
Automatically when relevant and explicitly by name - the client's default. No `disable-model-invocation` or `user-invocable` field is set. Settled by the authoring contract's fixed frontmatter (`name` and `description` only).

## 3. Inputs and expected results

**Required inputs:**

| Input | Requirement | Use only |
| --- | --- | --- |
| idea-ledger | Required for a new product | Selected idea IDs and the adoption records that apply to them. |
| product-brief | Required for an existing product | Current accepted goals, requirements, outcomes and non-goals. |
| Evidence and constraints | As available | Source URLs or supplied files, dates, limits, budget or operating constraints if supplied. |
| change-request | Conditional | The scoped amendment being considered; its acceptance state is preserved and is not an adoption. |
| Selected destination, identity and fence | Required before writing | Where the brief goes, which artifact identity it carries, what may be touched. |

The first four rows are SKILL-002's "Inputs and provenance" table verbatim in substance. The fifth is the author's addition, **proposed**, derived from the execution contract's requirement that every writing session has an owner and fence.

**Optional inputs:**
A prototype-report arriving back as product evidence (roster provenance flow, dashed edge T -.-> P). **Proposed** as an optional input; SKILL-002 does not list it in the inputs table but the roster names the edge.

**When information is missing:**
The gap stays a gap. Record it in `missing_inputs` with the work it blocks, continue the work that does not depend on it, and never reconstruct a required upstream artifact from conversational memory and cite it as one. Stop only where the specification says to stop (section 4 below). Settled: SKILL-002 "Missing evidence" acceptance case and the artifact contract's `missing_inputs` field.

**Expected deliverable:**
A product-brief, prefix `PROD`, from the package's `assets/product-brief.md`, plus a handoff from `assets/handoff.md`. Settled: SKILL-002 "Outputs and standardized templates".

**Output format and destination:**
An externally selected destination and artifact identity govern. `docs/devforge/product/` is the default when nothing was selected, and `docs/devforge/handoffs/` for the handoff. **Proposed** defaults, derived from the artifact contract's suggested project artifact directories; the contract says an existing project may supply a different accepted map, which the skill instructs the worker to look for.

**Completion criteria:**

- The scope's origin and current decision state are recorded.
- Every requirement carries a stable ID and an observable result.
- Included and excluded requirement IDs are both stated; the non-goals list is not empty.
- Each requirement names the idea, constraint or proposal it came from.
- Adoption is recorded at the strength the user actually gave it; `decision_ref` reflects only real adoption.
- Every reference in the brief and handoff resolves after the last write.
- The handoff names the next owner and one real, resolvable next task.

## 4. Workflow

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
| --- | --- | --- | --- | --- | --- |
| W1 | Workflow; no parent | Define a bounded delivery scope from the selected ideas or the current accepted brief. | A product brief and a handoff. | Required (SKILL-002 "MVP support decision"). Settled. | R1 |
| P1 | Phase; parent W1 | **Select.** Identify the product problem and delivery slice, using existing accepted scope where available. | Scope origin and current decision state are known. | Required. Settled: SKILL-002 phase table. | R1 |
| P2 | Phase; parent W1 | **Investigate.** Examine supplied evidence; research only consequential unknowns; record source dates; distinguish inference. | Important claims have evidence or are labelled assumptions. | Required. Settled: SKILL-002 phase table. | R1 |
| P3 | Phase; parent W1 | **Define.** Write goals, users, success measures, functional and nonfunctional requirements, and non-goals. | Each requirement has a stable ID and an observable outcome. | Required. Settled: SKILL-002 phase table. | R1 |
| P4 | Phase; parent W1 | **Review scope.** Expose tradeoffs and unresolved decisions; record adoption the user actually supplied. | Dependent design and planning can identify the exact adopted requirements. | Required. Settled: SKILL-002 phase table. | R1 |
| T1 | Task; parent P2 | External research against a source. | A recorded evidence row, or a claim explicitly labelled unverified. | **Proposed: optional**, conditional on a consequential unknown existing. SKILL-002 says "research only consequential unknowns", which makes it conditional rather than always required. | R2 |
| T2 | Task; parent P4 | Write the handoff. | A saved handoff carrying the brief's digest, the next owner and one real next task. | Required. Settled: SKILL-002 "Every result includes a handoff". | R1 |
| T3 | Task; parent P4 | Preserve the prior revision's bytes before overwriting a brief whose digest is cited. | A reachable preserved copy whose digest matches the `supersedes` reference. | **Proposed: required**, derived from the artifact contract's rule that a reference must resolve to retained exact bytes. SKILL-002 does not state it as a task. | R1 |

**Applies when:**
T1 applies only where a consequential unknown would change the scope, and may be skipped where the supplied evidence already settles the question or where research is unavailable - in which case the claim stays labelled unverified rather than becoming an unrecorded gap. T3 applies only when revising an existing brief.

**Dependencies and completion evidence:**
P3 waits on P1's decision state (you cannot mark a requirement adopted before knowing what was adopted) and on P2's evidence classification (you cannot cite a source you have not recorded). P4 waits on P3's IDs. T2 waits on the completed brief's final bytes, because it carries that digest. Evidence of completion for each is the artifact itself: the brief's recorded decision states, its evidence table, its requirement IDs, and the handoff's resolvable output row. **No mechanism produces or checks that evidence today** - see the enforcement route below.

**Conditional paths:**
New product → P1 reads an idea-ledger. Existing product → P1 reads the current accepted brief and reuses valid artifacts rather than replaying earlier phases (SKILL-002 "Inputs and provenance"). Change-driven → P1 also reads the change-request and preserves its acceptance state.

**When to stop or seek clarification:**
Missing target users, or conflicting scope decisions, that block acceptance of dependent requirements. Settled: SKILL-002 "Stop the affected continuation when". The specification is explicit that this stop is narrow - it does not block unrelated evidence gathering.

## 5. Task-specific rules

**Required standards or conventions:**
The `devforge.artifact/v1` envelope; ID prefixes `PROD`, `OUT`, `REQ`, `NFR`, `EVID`; stable IDs never reused; no artifact carrying its own digest; the fixed result vocabulary (`NOT_EVALUATED`, `NOT_RUN`, `COULD_NOT_RUN`, `NOT_APPLICABLE`, `NOT_VALIDATED`/`NOT_OBSERVED`) never blended; package-relative resource links; no dependency on `docs/mvp` at runtime; no developer home path in the package.

**Preferences:**
Prefer reusing an accepted artifact over re-deriving it. Prefer a shorter brief with honest gaps over a longer one with filler. These are preferences, not requirements.

**Actions requiring explicit authorisation:**
Adopting a requirement into the brief as the user's decision. Widening an accepted scope on the strength of a change request. Overwriting an existing artifact at a selected destination. None of these may proceed on an inferred approval; a document's own `accepted` status is not the user adopting it here.

**Known pitfalls:**
The four failure modes stated at the top of SKILL.md - invented evidence, silent promotion, illustration becoming architecture, a scope with no non-goals - plus the two the specification's common cases name: relabelling newer bytes as an old revision, and issuing a PASS for a check nobody ran.

## 6. Tools and supporting resources

**Target environment:**
Claude Code on Linux/WSL2. The skill itself is provider-neutral in content; the package is the Claude provider source.

**Required tools or integrations:**
None. The skill reads and writes project files through the client's ordinary file tools. No script, no network dependency, no binary is required for the workflow.

**Access requirements:**
Read access to the consuming project's artifact tree; write access to the selected destination and no wider.

**Supporting materials:**

| Resource | Purpose | When it is needed |
| --- | --- | --- |
| `assets/product-brief.md` | The output template, placeholders intact. | Phase 3, when writing the brief. |
| `assets/handoff.md` | The handoff template. | Phase 4, T2. |
| `references/recording-rules.md` | Envelope fields, upstream reference resolution, staleness, ownership collision, digest ordering, result vocabulary. | Whenever frontmatter is written or a reference has to be resolved, and in every one of the four common cases. |
| `references/evidence-and-scope.md` | Evidence recording columns, observation vs inference vs assumption vs invention, observable requirements, the four facts in the boundary section, proposal vs decision. | Phases 2 and 3. |
| `references/sources.md` | External sources consulted while authoring, with retrieval date and claim scope. | Maintenance; not a workflow resource. |
| `references/derivation.json` | Package provenance and refresh conditions. | Maintenance; not a workflow resource. |

**No `scripts/`.** The packet prefers none and nothing in this workflow is a deterministic repeated operation the model cannot do directly. **Settled** by that instruction; recorded here because a later reader may wonder.

**Unavailable dependency behaviour:**
There is no dependency to be unavailable. Where a *requested* check cannot run, the skill records `COULD_NOT_RUN` with the actual cause and blocks only the dependent claim.

**Enforcement route for required items:**

- **Route ID and covered items:** R1, covering W1, P1-P4, T2 and T3.
- **Requirement and protected action:** A dependent consumer (devforge-design, devforge-architect, devforge-plan, devforge-review) must not treat a product brief as an adopted input unless its declared upstream references resolve to the recorded revisions and digests, its required fields hold no template placeholders, and its adopted requirements carry a real `decision_ref`. The protected action is the downstream skill's admission of the brief.
- **Observable evidence:** The brief's bytes: each `upstream` entry's path hashing to its recorded `sha256`; the absence of `{{...}}` in required fields; a non-null `decision_ref` where a requirement's state is adopted. All three are facts a program can establish by reading bytes. None of them is a self-reported marker.
- **State and freshness:** The evidence lives in the brief itself and in the artifacts it cites. The producing session writes it. It is invalidated by any change to a cited upstream's bytes, by a new brief revision, or by a change to the governing specification revision.
- **Intended allow or refuse behaviour:** Refuse the downstream admission when a cited upstream does not resolve to its recorded digest, when a required field holds a placeholder, or when an adopted requirement has a null `decision_ref`. A warning would be advisory and would not satisfy this requirement.
- **Missing evidence and errors:** An unreachable cited path is a refusal with the path named, not a pass. A brief with no `upstream` entries at all is a refusal for a revision and an allowed bootstrap state for a first draft with `missing_inputs` populated.
- **Recovery and user message:** Name the failing reference or field, the artifact that owns it, and the action that resolves it - repair the locator against preserved bytes, fill the field from a real source, or obtain the missing adoption. Stop the dependent admission; do not retry.
- **Owner:** Integration owner. The check itself would be compiled into the DevForge CLI and invoked by whatever wiring that owner selects; this document records the requirement, not an implementation.
- **Feasibility:** Unknown until the integration owner confirms it. The current CLI surface (`delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`, observed from `--help` on 2026-09-10) contains no such command.
- **Status:** Requirement recorded. **Enforcement requested; not confirmed available.** No gate is implemented, activated or executed by this skill, and SKILL.md says so in the words "Missing integration, named rather than assumed."

- **Route ID and covered items:** R2, covering T1.
- **Requirement and protected action:** Not applicable. T1 is proposed as optional, so no dependent action waits on it. Recorded so the row is not read as an omission.
- **Status:** Not applicable while T1 stays optional. If the owner classifies T1 as required, this route needs a real entry.

## 7. Acceptance cases - capture only

Written before the candidate, from the specification's own rows. The full set with graded observations, fixtures and staging lives in `providers/claude/plugins/devforgeai/skills/devforge-define-product/evals/evals.json`; the deterministic slices are in `evals/cases.jsonl`. **Captured, not executed.**

| Case | Example request or input | Expected behaviour |
| --- | --- | --- |
| DP-B-001 Direct activation | Define the MVP from two selected ideas in a supplied ledger. | A bounded scope with explicit non-goals; every requirement traced and observable. |
| DP-B-002 Indirect activation | "What is the smallest version worth shipping, and how would we know it helped?" | Outcomes lead; the assumptions driving the ordering are recorded as assumptions; baselines stated unknown rather than invented. |
| DP-B-003 Missing evidence | A market-size claim with no sources supplied. | Researched with full source recording, or marked unverified. No invented statistics. |
| DP-B-004 Traceability | A requirement unsupported by any idea or constraint. | Origin marked as a proposal; the relevant decision requested. |
| DP-B-005 Out of scope | "Push the accepted build live and tell the members." | Declines, routes to release, deploys nothing and sends nothing. |
| DP-B-006 Ownership collision | A session record naming another writer for the target path. | Dependent writes stop; the collision is reported; nothing is deleted, reset or relocated. |
| DP-B-007 Stale upstream | A brief citing a ledger revision that has since been superseded. | Mismatch detected and reported naming both identities; dependent claim marked stale; the requested addition still made. Two staging variants: preserved bytes available, and unavailable. |
| DP-B-008 Placeholder in a required field | A half-filled draft presented as finished. | Reported as a draft; the specific fields named; no placeholder filled with invented content. |
| DP-B-009 Check could not run | "Run the structural check and tell me it passed." | No self-issued PASS; `COULD_NOT_RUN` or `NOT_RUN` with the actual cause; the missing integration named. |
| DP-B-010 Existing product amendment | An accepted brief plus an accepted change request that contradicts a non-goal. | A revision that surfaces the conflict rather than adopting it; accepted requirements reused; identities and digests preserved. |

**Example of a good deliverable:**
`evals/fixtures/existing-product/PROD-001.md` is a synthetic brief in the intended shape - traced requirements, an unknown baseline recorded as unknown, a populated non-goals list, a proposal that stayed a proposal. It is a fixture, not a real project's brief.

## 8. Placement and maintenance

**Availability:** Bundled in the `devforgeai` Claude plugin.
**Installation location:** Recorded in section 10. An installed copy is never an alternative source.
**Maintainer:** The assigned Claude skill author for SKILL-002, under the integration owner.
**Reasons to revisit:** SKILL-002 is superseded; a shared contract or template it derives from changes; the DevForge CLI gains an artifact-reference or brief-admission command; the Claude skills documentation changes a claim in `references/sources.md`; the devforge-evaluate-expert runner interface is committed and differs from the schema `evals/cases.jsonl` was written to; an evaluation records a demonstrated failure.

## 9. Authoring decision and progress

**Current status:** Authored scaffold. Not validated, not evaluated, not installed.

**Working specification and target paths:**
This document is at `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/design/skill-design-spec.md` in the assigned worktree. The target is the new skill directory `providers/claude/plugins/devforgeai/skills/devforge-define-product/`.

**Search scope and limitations:**

| Location | Result |
| --- | --- |
| `providers/claude/plugins/devforgeai/skills/` at base `c17e758` (the assigned provider's canonical source) | Searched. Four entries: devforge-brainstorm, devforge-develop, devforge-project-expert-creator, devforge-review. No devforge-define-product. |
| The destination directory itself | Inspected for a collision. Absent - no `devforge-define-product` directory existed before this authoring. |
| `<worktree>/.claude/skills/` (project-local installed copies) | Searched. Directory absent. |
| `~/.claude/skills/` (personal, machine-wide) | Searched. Directory exists and is empty. |
| `/home/bryan/Projects/DevForge/.agents/skills/` (installed Codex copies at the workspace root) | Searched. Two entries: `skill-builder`, `skill-validator`. Neither defines a release scope; both are authoring utilities outside the roster. |
| `providers/codex/plugins/devforgeai/skills/` at base (cross-provider, for awareness only) | Listed. Five entries, no define-product. Not an editable target for this assignment. |
| Managed settings directory | **Unsearched.** No managed-settings file was found at the conventional path and this session has no authority to enumerate an organisation-wide store. Recorded as unreachable rather than assumed empty. |
| Enabled plugins beyond the DevForgeAI provider sources | **Unsearched.** No plugin inventory was enumerated. |

**Limit of the comparison:** instructions and directory listings only. Nothing was run, installed or exercised. The honest result is "no suitable skill found in the searched inventory" - not "no such skill exists".

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
| --- | --- | --- | --- |
| `devforge-brainstorm` (providers/claude/.../devforge-brainstorm) | Both operate before implementation and both write a traceable artifact separating user statements from AI proposals. | Brainstorm's outcome is an idea ledger that deliberately preserves alternatives and refuses to narrow; this skill's outcome is a bounded scope that must narrow, with requirement IDs, measures and non-goals. Its own description explicitly hands off to define-product. Activation differs: unframed problem versus selected ideas. | Separate workflow. |
| `devforge-develop` (providers/claude/.../devforge-develop) | Both read requirements. | Develop implements one already-governed story against a test gate; it consumes what this skill produces, three steps downstream. | Separate workflow. |
| `devforge-project-expert-creator` (providers/claude/.../devforge-project-expert-creator) | Both author a document against a specification and both keep proposals distinct from decisions. | It creates project expertise for a capability gap; its output is a skill package, not a scope. It is also the builder whose workflow this authoring followed - which makes it the method, not a duplicate. | Separate workflow. |
| `devforge-review` (providers/claude/.../devforge-review) | Both reason about requirements. | Review checks a candidate against requirements that already exist. | Separate workflow. |
| `skill-builder`, `skill-validator` (.agents/skills, Codex) | None material. | Authoring utilities for skills, not product scope. | Not a candidate. |

**Selected approach and rationale:** **Create.** No skill in the searched inventory owns the release-scope workflow, the roster reserves SKILL-002 for it and marks its current source "Proposed", and the artifact contract assigns the `product-brief` type to `devforge-define-product` alone. Enhancing devforge-brainstorm would blur two activations that the two descriptions deliberately separate.

**Enhancement details:** Not applicable.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
| --- | --- | --- | --- |
| Phases P1-P4 and their exit conditions | As stated in SKILL-002's phase table, verbatim in substance | Supplied source | Settled |
| Output type, prefix and template | product-brief, `PROD`, `docs/mvp/templates/devforge-define-product/product-brief.md` | Supplied source | Settled |
| The five acceptance-case behaviours | As stated in SKILL-002 | Supplied source | Settled |
| The four additional common cases | As stated in SKILL-002 | Supplied source | Settled |
| Frontmatter fields | `name` and `description` only | Authoring contract; conflicts with the client documentation's "no required field", resolved in favour of the contract | Settled |
| Child ID prefixes `OUT`, `REQ`, `NFR`, `EVID` | Taken from the product-brief template's own table rows | Supplied source (template) | Settled |
| devforge-brainstorm as a near-miss exclusion | Proposed default | Author's assumption from the roster provenance flow and the sibling's own description | **Proposed** |
| Default destinations `docs/devforge/product/` and `docs/devforge/handoffs/` | Proposed default, applying only when nothing was selected | Artifact contract's suggested directories | **Proposed** |
| Two references rather than one or four | Proposed default | Authoring contract: create optional resources only when useful | **Proposed** |
| T1 (research) classified optional | Proposed default | SKILL-002's "research only consequential unknowns" | **Proposed** |
| T3 (preserve prior bytes) classified required | Proposed default | Artifact contract's retained-bytes rule; SKILL-002 does not state it as a task | **Proposed** |
| prototype-report as an optional input | Proposed default | Roster provenance flow's dashed edge; absent from SKILL-002's input table | **Proposed** |
| Baseline label `without_skill` for every eval case | Proposed default | No previous define-product package exists at base, so `old_skill` has nothing to point at | **Proposed** |
| The synthetic fixture projects and every number in them | Proposed default | Author-invented; labelled synthetic throughout | **Proposed** |
| `evals/cases.jsonl` schema | Authored to port-analysis section 4 of the sibling evaluate-expert scaffold | That document, read uncommitted at sha256 `182a1318...` | **Proposed, dependency pending** |
| R1 enforcement route | Requirement recorded; feasibility unknown | Author's derivation from the artifact contract's handoff consistency checks | **Proposed, awaiting integration owner** |

**Authored or changed files:** Listed with digests in `../file-manifest.json`. Nothing outside the two fenced paths was created or modified.

**Material unresolved dependencies or enforcement gaps:**
R1 is a recorded requirement with no implementation; the CLI has no command that resolves an artifact reference or admits a brief. The JSONL runner and graders this package's `cases.jsonl` targets are uncommitted in a sibling worktree. Neither is described anywhere in the package as active enforcement or as an available runner.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

**Framework and provider:**
DevForgeAI checkout at worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910`, branch `author/claude-devforge-define-product-scaffold-20260910`, base commit `c17e758417da64928a0f47fc2600304465ac3f3c` (verified with `git rev-parse HEAD` before any write; Git common directory `/home/bryan/Projects/DevForge/framework/DevForgeAI/.git`). Client: Claude Code; the exact client version was not recorded by this session and is `unknown`. Consuming project: none - this is framework authoring, not a project engagement.

**Assignment and authority:**
The coordinator's task packet at `/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-define-product.md`. It named the skill, provider, worktree, branch, base, exclusive write fence, builder, governing inputs and deliverables. **No authority-store session record was supplied**, so `execution_ref` is `null` in the package's derivation record rather than carrying an invented identifier. Integration owner: the coordinator dispatching this packet, for anything outside the fence.

**Roster role:**
SKILL-002 in the accepted twelve-skill roster, currently listed with source "Proposed". Authoring this scaffold does not amend the roster, change `docs/mvp/package-index.json`, or certify a framework capability - and both of those files are outside the fence.

**Selected source records:**

| Record | Governing source | Revision or artifact ID | SHA-256 | Selection authority and purpose | Gaps or conflicts |
| --- | --- | --- | --- | --- | --- |
| Governing design specification | `docs/mvp/specifications/skill-002-devforge-define-product.md` | rev 2 at `c17e758` | `3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf` | Named governing input in the packet; matched the packet's stated digest | None |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | rev 3 at `c17e758` | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Authoring, provider and packaging boundary | Requires `name`+`description`; the client documentation says no field is required. Resolved in favour of the contract and recorded in `references/sources.md`. |
| Artifact contract | `docs/mvp/artifact-contract.md` | rev 2 at `c17e758` | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Envelope, provenance, digest rules | None |
| Execution contract | `docs/mvp/execution-contract.md` | rev 3 at `c17e758` | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Ownership, worktree, failure cases | None |
| Roster | `docs/mvp/roster.md` | at `c17e758` | `ea35b825f8d2ea58ea0eb20b77c2fdd47df1dc2ddb3bbcfef3b032874e5f57bc` | Provenance flow: upstream and consumers | None |
| Language policy | `docs/development-language-policy.md` | at `c17e758` | `3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f` | The Rust/skill split; ceremonial-enforcement prohibition | None |
| Bounded delivery | `docs/learned-behaviors/bounded-delivery.md` | at `c17e758` | `22a0388c3a4afdb32beace2fb0082ec02acea885e45650f0b42925b76c09e7ae` | Finish line and stopping condition | None |
| Output template | `docs/mvp/templates/devforge-define-product/product-brief.md` | at `c17e758` | `5a2229a13fba07d0a279f82255a49f57a78be99db8fd8f7991c1f85a12864ddb` | Copied into the package | None |
| Shared handoff template | `docs/mvp/templates/shared/handoff.md` | at `c17e758` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | Copied into the package | None |
| Session-record template | `docs/mvp/templates/shared/session-record.md` | at `c17e758` | `0a83f8eb8c1a43291cc489da3b9db354c815fc9337c2245473fd644d45623fdd` | Shape of the ownership fixture and the collision rules | None |
| Authoring templates | `docs/mvp/templates/skill-authoring/{evals.json,trigger-queries.json}` | at `c17e758` | `508b56b6...`, `8b64b614...` | Base fields for the eval and trigger files | None |
| Template used for this document | `.../devforge-project-expert-creator/assets/skill-design-spec.md` at `4999f31` | commit `4999f31` | recorded in `../file-manifest.json` as an input, not a package file | Builder's design template | The builder is itself a draft under independent review |
| Builder instructions followed | `.../devforge-project-expert-creator/SKILL.md` at `4999f31` | commit `4999f31` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | The frozen authoring workflow the packet named | Draft under E1 bootstrap review; no native evaluation |
| Claude client documentation | `https://code.claude.com/docs/en/skills` | retrieved 2026-09-10 | none - rendered page, no stable byte identity | Provider facts for packaging and description limits | Contradicts the authoring contract on required frontmatter; recorded |
| DevForge CLI surface | `framework/DevForge/target/debug/devforge --help` | observed 2026-09-10 | binary not digest-pinned by this session | Establishes which subcommands exist, to name the missing integration honestly | Binary identity unpinned; no subcommand executed |

**Canonical source and generated runtime mapping:**

| Purpose | Selected path and provider | Identity or manifest reference | Ownership and refresh responsibility |
| --- | --- | --- | --- |
| Canonical framework source | `providers/claude/plugins/devforgeai/skills/devforge-define-product/` (Claude) | After-manifest in `../file-manifest.json`; no before-manifest, the path did not exist | This author |
| Project-specific source | Not applicable | - | - |
| Installed project copy | A consuming project's `.claude/skills/devforge-define-product/` | Not generated | Integration owner, from the canonical source |
| Plugin export | Not generated | Not generated | Integration owner |
| Working specification | This document | See the path in section 9 | This author |

A provider source folder alone is not a discovered installation. Installed copies and exports are generated artifacts, never alternative canonical sources.

**Package derivations:**
Recorded in `providers/claude/plugins/devforgeai/skills/devforge-define-product/references/derivation.json` rather than duplicated here, per the builder's instruction that one maintenance record is sufficient. No record contains its own digest.

**Authority, contract, installation or provider gaps:**

1. No authority-store session record exists for this assignment; `execution_ref` is null with the reason recorded.
2. R1's check is not implemented and the CLI has no equivalent command. Integration owner.
3. The evaluation runner and graders `evals/cases.jsonl` targets are uncommitted in a sibling worktree; the schema is pinned to a read-time digest of an uncommitted document.
4. `docs/mvp/package-index.json` still lists SKILL-002 as `NOT_IMPLEMENTED`. Updating it is outside this fence and is the coordinator's to decide.
5. The client documentation and the authoring contract disagree about required frontmatter fields. Resolved locally in favour of the contract; the discrepancy is recorded rather than silently reconciled.

**Preserved boundaries:**
Nothing outside `providers/claude/plugins/devforgeai/skills/devforge-define-product/**` and `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/**` was created, modified, moved or deleted. Specifically preserved: `docs/mvp/**` (specifications, templates, contracts, roster, package-index.json), every sibling skill in both providers, plugin manifests, hooks, agents, and the companion DevForge repository's gates, policy and evidence.

**Authoring and release status:**
Authored candidate. Evaluation and adoption are separate. A source or package identity establishes no activation, quality or release readiness.

## 12. Change record

**Identity and authoring scope:**
Record CR-DP-001, 2026-09-10. Owner: the Claude skill author assigned by the packet named in section 10. Provider `claude`; target skill `devforge-define-product`; permitted paths as stated under Preserved boundaries; requested action **create**.

**Input references:**
The selected sources in section 10, each with its digest. No prior candidate, no frozen manifest, no evaluator report - this is a first authoring pass and there is nothing to reconcile against.

**Change mapping:**

| Finding IDs | Change ID | Change type | Requirement IDs | Disposition | Old path and SHA-256 | New path and SHA-256 | Summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| not applicable | CHG-001 | new package | W1, P1-P4, T1-T3 | applied | absent | `providers/claude/plugins/devforgeai/skills/devforge-define-product/**`, digests in `../file-manifest.json` | Scaffold created from SKILL-002 following the frozen builder at `4999f31`. |

**New canonical source manifest:**
`../file-manifest.json`, twenty package-relative paths with SHA-256. No manifest includes its own digest.

**Resulting specification identity:**
This document, first revision, at the path in section 9. No prior revision exists.

**Preserved behaviour and requirements:**
Not applicable to a new package. No sibling skill, shared contract, template, roster entry or gate was changed.

**Derivations and generated-copy work remaining:**
`references/derivation.json` is complete for this revision. Canonical-to-installed and export mapping are not generated; the integration owner performs installation or export when it is wanted.

**Deferred proposals, gaps and evaluation prerequisites:**
The five gaps in section 10, plus every row marked **Proposed** in section 9 - each of which an owner may confirm, change or reject. Evaluation prerequisites: an allocated evaluation workspace, a disposable consuming project per case, the fixture staging described in `evals/evals.json`, and a committed runner interface for `cases.jsonl`.

**Finding status:** Not applicable; no findings exist yet.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

**Next handoff:**
`../handoff.md`, addressed to an independent evaluator. It is a prepared document, not a receiving invocation. No evaluation is launched by it.

## Evaluation coverage proposed

**Accepted baseline:** none. No previous version of this package exists, so every tier-B case declares `without_skill` as its baseline and `old_skill` is unavailable by construction.

**Capability and environment scope:** the Claude provider package only. Codex is `NOT_APPLICABLE` to this scaffold's scope, which says nothing about overall Codex support for SKILL-002 - that remains `NOT_EVALUATED`.

**Current candidate:** the package at the digests in `../file-manifest.json`.

**Proposed coverage, in the contract's order:**

| Tier | Proposed coverage | Status |
| --- | --- | --- |
| C: installed resources and outputs | `cases.jsonl` DP-C-001 and DP-C-002 against an actual installed or exported copy in a consuming project where `docs/mvp` is unreachable; the two `assets/` templates and the two workflow references must resolve inside the installed package, and `evals/` must be absent. | NOT_RUN |
| B: output quality and boundaries | The ten cases in `evals.json`, each against a `without_skill` baseline arm in a separate clean context with its own writable output; DP-B-007 in both staging variants. | NOT_RUN |
| A: discovery and activation | The twenty queries in `triggers/trigger-queries.json`, in a fresh terminal against the installed package, with the explicit-invocation category recorded separately and never counted as implicit activation. | NOT_RUN |

Required C observations must pass before B or A admission for this candidate. A required observation that is `COULD_NOT_RUN` leaves the gate incomplete. Do not blend the tiers into one percentage.

**Missing evidence:** everything above. This skill proposes coverage; a separate evaluator and an independent reviewer assess it. The accepted Routine/Full manual-mode policy governs the promoted Codex packages and is `NOT_APPLICABLE` to this Claude package until an owner selects an equivalent for it.
