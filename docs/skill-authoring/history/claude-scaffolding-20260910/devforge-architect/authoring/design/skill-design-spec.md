# Skill design specification: devforge-architect

Working design document, filled from the template at `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/assets/skill-design-spec.md` as it stands at commit 4999f3106565c5e320d1f1a7db066b437e4e94be. Filled here, in the authoring evidence tree; the package template it derives from was not modified.

This is a DevForgeAI authoring document. It carries the design, the framework authority and source mapping, and the change record. It does not certify a skill, and completing it establishes nothing about behaviour.

**No questions were asked of the user.** The assignment directed a question-free pass: every material decision below is recovered from the governing specification, the shared templates and contracts, or the sibling packages, and every decision the sources are silent on is recorded as a **proposed default** and labelled as such. Proposed defaults are not requirements the user gave.

Filled 2026-09-10T19:47:56Z UTC.

## 1. Identity and purpose

**Skill name:**
`devforge-architect`

**Purpose:**
Record the architecture, dependency versions, source layout, interface responsibilities and test policy that govern a delivery slice, so that later sessions are governed by decisions the project actually made rather than by whatever the model reaches for. Source: SKILL-005 user goal row.

**Description for discovery:**
Written into the package frontmatter. It states the outcome, then the direct-domain and indirect activating conditions from the specification's use-case inventory, then the near-miss exclusions with the sibling that owns each. 1,297 characters, inside the 1,536-character budget Claude applies to `description` plus `when_to_use`.

**Intended users or role:**
The person establishing or amending a project's technical contract, in an ordinary subscribed Claude Code terminal. Not a role in an org chart.

## 2. Scope and activation

**Use this skill when:**
Establishing a project's architecture and stack contract; settling the stack before development starts; preventing dependency or layout drift across sessions; taking an evidence-backed inventory of an existing repository's real dependencies and layout; applying an already-approved amendment to adopted rules.

**Outside its scope:**

| Request | Owner |
| --- | --- |
| A new library release, or a security advisory, presented as reason to upgrade | `devforge-change` (SKILL-012). Specification "Does not activate for" row. |
| Working out what to build at all | `devforge-brainstorm` (SKILL-001) |
| Defining the delivery scope and requirements | `devforge-define-product` (SKILL-002) |
| Designing the user experience | `devforge-design` (SKILL-003) |
| Testing a consequential execution uncertainty by building something | `devforge-prototype` (SKILL-004) |
| Deriving epics and stories from adopted rules | `devforge-plan` (SKILL-006) |
| Authoring a project expert skill | `devforge-project-expert-creator` (SKILL-007) |
| Implementing an accepted story | `devforge-develop` (SKILL-009) |
| Reviewing a candidate for readiness | `devforge-review` (SKILL-010) |
| An isolated copy edit | No skill. Specification "Out of scope" acceptance row. |

**Example activating requests:**

- "Use DevForgeAI to establish this project's architecture and stack contract." (specification direct request)
- "How should we structure this SaaS so later sessions do not introduce incompatible libraries?" (specification indirect request)
- "A new person is joining next week and nothing about how this repo is organised is written down anywhere. Where do I even start?"

**Near-miss requests that must not activate it:**

- "Rails 8.1 just shipped. Upgrade us."
- "STORY-014 is accepted and ready. Implement it."
- "There is a typo in docs/getting-started.md. Fix that line, nothing else."

The three examples above are all drawn from the **train** split. The full positive and negative set with its fixed split is in the package's `evals/triggers/trigger-queries.json`; no validation-split query is quoted in this document or anywhere else this author wrote, so the held-out set stays held out.

**How it should be invoked:**
Automatically when relevant, and explicitly by name. **Proposed default:** the package sets neither `disable-model-invocation` nor `user-invocable`, matching the two-field frontmatter rule the authoring contract applies to these packages. The client's defaults then permit both paths.

## 3. Inputs and expected results

**Required inputs:**
product-brief with its requirement IDs; the repository, package manifests and lockfiles where a repository exists; primary technical sources for any selected API claim; the project root, write fence and artifact destination.

**Optional inputs:**
design-spec and prototype-report where the slice has them; an existing architecture-contract or an approved change-request for an amendment.

**When information is missing:**
The input stays missing, named, with the work it blocks, recorded in `missing_inputs`. Nothing is inferred into a revision, digest, owner or approval. The work that does not depend on it continues. A contract can be a useful draft with a named gap; it cannot be presented as ready with an invented one. Stopping is reserved for a consequential rule needing an approval nobody has given, unverifiable required API behaviour, conflicting adopted rules, or a write-fence or ownership collision.

**Expected deliverable:**
An `architecture-contract` (ID prefix `ARCH`) from `assets/architecture-contract.md`, plus a handoff from `assets/handoff.md`.

**Output format and destination:**
A selected destination governs. **Proposed default when nothing was selected:** `docs/devforge/architecture/` for the contract and `docs/devforge/handoffs/` for the handoff, from the suggested artifact directories in the artifact contract; an existing project artifact map wins over this default. **Proposed default:** allocate the next unused `ARCH` number when no identity was selected.

**Completion criteria:**

- The contract exists at the selected destination with decisions, stack rules, layout rules, interface contracts and capability rows carrying stable IDs and requirement references.
- Every declared input resolves to the revision and digest cited.
- Adopted decisions are distinguishable from AI proposals, row by row.
- Enforcement requirements are recorded with their owner, and unimplemented adapters are named as unimplemented.
- No required field holds a template placeholder.
- The handoff carries the contract's digest, not its own, and gives one next task that actually exists.

## 4. Workflow

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
| --- | --- | --- | --- | --- | --- |
| W1 | Workflow; no parent | Establish or amend the project contract | An adopted-or-proposed architecture-contract and a handoff | Required (specification-defined) | R1 |
| P1 | Phase; parent W1 | Inventory: inspect scope, code, manifests, constraints; distinguish observed from desired | Existing decisions and evidence gaps listed | Required (specification-defined) | R1 |
| P2 | Phase; parent W1 | Resolve: compare consequential alternatives; check version-specific APIs | Each choice carries a reason and evidence, or an explicit open question | Required (specification-defined) | R1 |
| P3 | Phase; parent W1 | Specify: assign IDs; define dependencies, ownership, interfaces, boundaries, test commands, capabilities | Precise enough for a story author and a validator adapter | Required (specification-defined) | R1, R2 |
| P4 | Phase; parent W1 | Adopt and hand off: record accepted choices; supply the exact revision to the policy owner | No unsupported enforcement claim is made | Required (specification-defined) | R2, R3 |
| T1 | Task; parent P2 | Verify a version-specific API claim against a primary source | A recorded claim with source, version, date and limits, or a recorded uncertainty | **Proposed default: required** whenever a decision turns on the claim; conditional otherwise | R3 |
| T2 | Task; parent P3 | Record an enforcement requirement for each blocking rule | Requirement, evidence, intended refuse behaviour and owner recorded | **Proposed default: required** for any rule stated as blocking | R2 |
| T3 | Task; parent P4 | Preserve prior bytes before overwriting a cited artifact | The cited digest still resolves after the write | **Proposed default: required** whenever an existing contract is revised | R3 |

The four phases are the specification's; their required status follows from it. T1-T3 are decompositions this design proposes, and their classification is a proposed default awaiting the user's or integration owner's answer. No classification was invented as settled.

**Applies when:**
P2's prototype route applies only where an execution risk cannot be settled by reading. T3 applies only when an existing artifact whose digest is cited is being replaced. The amendment path (an existing contract plus an approved change-request) replaces a greenfield P1 with a bounded inventory of the affected rules.

**Dependencies and completion evidence:**
P3 waits on P1's inventory and P2's resolutions; its completion evidence is the contract's own filled rows and their requirement references. P4 waits on P3; its completion evidence is the adopted revision's identity delivered to the policy owner, plus the handoff. All of that evidence goes stale when the contract's bytes change, when an upstream revision moves, or when the assignment changes.

**Conditional paths:**
Existing project - inventory rather than replacement. Amendment - bounded change to the affected IDs, preserving prior accepted evidence. Unresolved execution risk - open question routed to prototype rather than a guessed decision.

**When to stop or seek clarification:**
A consequential rule needs an approval nobody has given; required API behaviour cannot be verified; adopted rules conflict; a write fence or a concurrent writer prevents declaring the result ready.

## 5. Task-specific rules

**Required standards or conventions:**
`devforge.artifact/v1` envelope on the contract and the handoff. Stable ID prefixes `ADR`, `RULE`, `API`, `CAP`; IDs never reused; a superseded row keeps its ID. No artifact carries its own complete-byte digest. Version pins in the contract match the observed manifest exactly. Prohibited substitutions recorded explicitly. Fixed result vocabulary, never blended.

**Preferences:**
Bounded research - verify the claims that change a decision, and record the rest as not investigated. Prefer reusing valid accepted artifacts over replaying earlier phases.

**Actions requiring explicit authorisation:**
Adopting a decision into `accepted` state. Adopting a newer upstream revision. Changing an approved stack. Overwriting an existing contract. None of these follows from a document's own `accepted` status or `decision_ref`.

**Known pitfalls:**
Recording an AI proposal as the project's decision. Moving a version pin so a familiar snippet becomes correct. Replacing a retained stack by describing a better one. Writing a rule that reads as enforcement when nothing checks it. Relabelling newer bytes as an older revision.

## 6. Tools and supporting resources

**Target environment:**
Claude Code on Linux or WSL2, working against a consuming project supplied at task time. The DevForgeAI repository is not required at runtime.

**Required tools or integrations:**
File reading for manifests, lockfiles and existing artifacts. Web retrieval for primary technical sources where a claim needs verification. The companion DevForge CLI where the operator supplies it and a policy file exists - read-only from this skill's point of view.

**Access requirements:**
Read access to the consuming project; write access limited to the assigned artifact destination and fence. No credential or secret value is requested or recorded.

**Supporting materials:**

| Resource | Purpose | When it is needed |
| --- | --- | --- |
| `assets/architecture-contract.md` | The output template, placeholders intact | Specify |
| `assets/handoff.md` | The handoff template | Adopt and hand off |
| `references/framework-context.md` | Ownership split, enforcement-requirement shape, command boundaries, missing integrations, vocabulary | Whenever a gate, a command or a claim of enforcement is in question |
| `references/recording-rules.md` | Envelope fields, IDs, digest ordering, upstream resolution, decisions versus proposals, collisions, unrunnable checks | Filling the envelope, resolving an upstream, hitting a collision or a blocked check |
| `references/version-evidence.md` | Version verification, existing stacks, newer releases, bounded research | Resolve, and any factual API claim |
| `references/sources.md`, `references/derivation.json` | Provenance of external claims and package-local copies | Maintenance and refresh |

**Unavailable dependency behaviour:**
Name the unavailable tool, policy, binary or path, state what it blocks, record `COULD_NOT_RUN` with the actual cause, and continue the independent work.

**Enforcement route for required items:**

- **Route ID and covered items:** R1; W1, P1, P2.
  **Requirement and protected action:** A contract must not be presented as ready while a required input is unresolved or a required field holds a placeholder; the protected action is the handoff to a downstream consumer.
  **Observable evidence:** The contract's own bytes - `missing_inputs` contents and the absence of `{{...}}` in required fields.
  **State and freshness:** Lives in the contract at its selected path; written by this skill; invalidated by any later edit to those bytes.
  **Intended allow or refuse behaviour:** Refuse the ready claim while a placeholder remains in a required field. A warning is advisory, not a refusal.
  **Missing evidence and errors:** An unreadable or absent contract blocks the claim, not the reporting.
  **Recovery and user message:** Name the fields, route the facts to `missing_inputs`, and say what would resolve each.
  **Owner:** Integration owner. The check itself is compiled into the DevForge CLI and invoked by whatever wiring that owner selects; this document records the requirement, not an implementation.
  **Feasibility:** Unknown until the integration owner confirms it.
  **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

- **Route ID and covered items:** R2; P3, P4, T2.
  **Requirement and protected action:** A stack, layout or verification rule stated as blocking must not be described as enforced without a supported adapter and observed evidence; the protected action is any downstream claim of mechanical enforcement.
  **Observable evidence:** The contract's "External enforcement coverage" line and each rule's adapter column.
  **State and freshness:** In the contract; invalidated when an adapter is implemented or the policy changes.
  **Intended allow or refuse behaviour:** Refuse an enforcement claim whose adapter column names no implemented adapter.
  **Missing evidence and errors:** Absent coverage data blocks the enforcement claim only.
  **Recovery and user message:** Record the requirement and route it to the integration owner; keep it visible as unmet.
  **Owner:** Integration owner.
  **Feasibility:** Enforcement requested; not confirmed available. The POC's dependency check is a synthetic contract check, not a real ecosystem adapter.
  **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

- **Route ID and covered items:** R3; T1, T3, P4.
  **Requirement and protected action:** Every cited upstream reference must resolve to bytes matching the cited digest after the last write; the protected action is handing the contract to a consumer.
  **Observable evidence:** The referenced files at their locators and their digests.
  **State and freshness:** In the project artifact store and any preserved archive; invalidated by an overwrite without preservation.
  **Intended allow or refuse behaviour:** Refuse the handoff claim when a cited digest no longer resolves.
  **Missing evidence and errors:** Unreachable prior bytes go to `missing_inputs`, and only what exists is cited.
  **Recovery and user message:** Preserve the prior bytes at an authorised location and repoint the locator, or record the loss.
  **Owner:** Integration owner.
  **Feasibility:** Unknown until the integration owner confirms it.
  **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

## 7. Acceptance cases - capture only

Captured before the candidate was authored, from the specification's acceptance table and its four additional common cases. They were captured, not executed.

| Case | Example request or input | Expected behaviour | Package case |
| --- | --- | --- | --- |
| Direct activation | Establish this project's architecture and stack contract, with an accepted brief and no repository | A contract mapped to the product requirements | evals id 1 / ARCH-B-001 |
| Indirect activation | How do we stop later sessions introducing incompatible libraries | Dependency and layout rules with separate enforcement requirements | evals id 2 / ARCH-B-002 |
| Existing stack | Repository on Dapper, user has retained it | The decision is preserved; EF appears only as an explicitly requested proposal | evals id 3 / ARCH-B-003 |
| Version uncertainty | A familiar snippet does not match the pinned version | Verified, or the uncertainty recorded; the version is not silently changed | evals id 4 / ARCH-B-004 |
| Out of scope | An isolated copy edit | No architecture process is imposed | evals id 5 / ARCH-B-005 |
| Concurrent writer | A session record shows another writer holds the destination | Dependent writes stop; the collision is reported; nothing is reset or deleted | evals id 6 / ARCH-B-006 |
| Stale upstream | The cited brief revision has been superseded | The prior evidence is marked stale and a new check routed; no silent adoption | evals id 7 / ARCH-B-007 |
| Placeholder remaining | A required field still holds a template placeholder | The result stays a draft and is not presented as ready | evals id 8 / ARCH-B-008 |
| Check cannot run | The policy the requested check needs is absent | COULD_NOT_RUN with the actual cause; absence of an error is not PASS | evals id 9 / ARCH-B-009 |

Structural cases for the package itself are ARCH-PKG-001 and ARCH-PKG-002. Trigger queries for discovery and activation are separate and live in `evals/triggers/trigger-queries.json`.

## 8. Placement and maintenance

**Availability:** Bundled in the `devforgeai` Claude plugin.
**Installation location:** Recorded in section 10. An installed copy is never an alternative source.
**Maintainer:** The DevForgeAI integration owner.
**Reasons to revisit:** SKILL-005 changes; either shared template changes; the artifact, execution or authoring contract changes; the Claude client's skills documentation changes; a real stack or test adapter is implemented; an evaluation records a failure.

## 9. Authoring decision and progress

**Current status:** Authored candidate. Not evaluated.

**Working specification and target paths:** This document, at `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/authoring/design/skill-design-spec.md` in the assigned worktree. Target: `providers/claude/plugins/devforgeai/skills/devforge-architect/`.

**Search scope and limitations:**
Searched: the Claude provider inventory at base commit `c17e758417da64928a0f47fc2600304465ac3f3c`, `providers/claude/plugins/devforgeai/skills/`, which contains exactly `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator` and `devforge-review`. No `devforge-architect` exists there. Also read: `docs/mvp/roster.md` (SKILL-005 recorded as "Proposed", no source), and the two in-flight sibling worktrees for the frozen builder and the runner dependency.

Not searched, and therefore not claimed empty: the user's personal `~/.claude/skills/`, any enterprise or managed settings directory, any installed plugin cache, any `--add-dir` directory, claude.ai account-synced skills, the Codex provider inventory (a different provider's source is outside this fence), and any catalogue outside this repository. Skills were compared by reading names, descriptions and instructions only; none was run, installed or tested.

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
| --- | --- | --- | --- |
| `devforge-project-expert-creator` (providers/claude/.../devforge-project-expert-creator) | Both work from accepted architecture and pinned versions; the expert creator consumes ARCH capability rows | It authors a skill package; it produces no architecture-contract and owns no stack, layout, interface or test rules. Its activation is a capability gap, not a technical contract | Separate workflow |
| `devforge-brainstorm` (same tree) | Both record decisions with origin and adoption state | Early exploration, explicitly forbidden from selecting a stack. Its output is an idea-ledger upstream of the product brief this skill consumes | Separate workflow |
| `devforge-develop` (same tree) | Both read the architecture contract | Implements one accepted story under the TDD gate; consumes rules rather than establishing them | Separate workflow |
| `devforge-review` (same tree) | Both assess a candidate against governing rules | Reviews correctness and readiness of an implementation; produces a review-report | Separate workflow |

**Selected approach and rationale:** **Create.** No suitable skill was found in the searched inventory: no `devforge-architect` exists in the Claude provider source, no sibling produces an `architecture-contract`, and no sibling's activation covers establishing a project's technical contract. The nearest neighbour, `devforge-project-expert-creator`, is a consumer of this skill's output rather than an owner of the workflow, so absorbing SKILL-005 into it would blur two distinct activations. "No suitable skill found in the searched inventory" is the claim; global uniqueness is not claimed. The destination directory was inspected before writing and did not exist, so no collision required reconciliation.

**Enhancement details:** Not applicable.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
| --- | --- | --- | --- |
| Output artifact and template | architecture-contract, prefix ARCH, from the named template | SKILL-005 outputs table | Settled by specification |
| Phases and exit conditions | Inventory, Resolve, Specify, Adopt and hand off | SKILL-005 workflow table | Settled by specification |
| Acceptance cases | Five rows plus four common cases | SKILL-005 validation section | Settled by specification |
| Frontmatter fields | `name` and `description` only | Authoring contract as applied by the sibling Claude packages | Settled by contract |
| Output destination | `docs/devforge/architecture/`; handoff `docs/devforge/handoffs/` | Artifact contract's suggested directories | **Proposed default** |
| ARCH numbering | Next unused number when no identity was selected | Sibling convention | **Proposed default** |
| Invocation policy | Automatic and explicit; no invocation-control fields set | Two-field frontmatter rule | **Proposed default** |
| T1-T3 classification | Required as described in section 4 | This design's decomposition | **Proposed default; awaiting an answer** |
| Existing-project entry point | Evidence-backed inventory rather than replacement | SKILL-005 MVP support decision row | Settled by specification |
| Reference set | framework-context, recording-rules, version-evidence, sources, derivation | Assignment's "only what the workflow needs" | **Proposed default** |
| `scripts/` | None | Assignment prefers none; no deterministic operation is required | **Proposed default** |
| Baseline label for tier B | `without_skill` | No previous revision of this skill exists | Settled by contract |

**Authored or changed files:** Listed in the change record in section 12 and enumerated with digests in `../file-manifest.json`.

**Material unresolved dependencies or enforcement gaps:**
No real stack or test adapter exists; the POC dependency check is a synthetic contract check. Making an adopted contract effective as external DevForge policy is an operator step with no implemented route from this skill. `devforge-change`, `devforge-define-product`, `devforge-plan`, `devforge-design` and `devforge-prototype` are specified but not implemented, which constrains what a continuation may name as installed. The evaluation runner and graders live in another package, recorded in section 10.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

**Framework and provider:**
DevForgeAI at base commit `c17e758417da64928a0f47fc2600304465ac3f3c`, Claude provider. Claude Code client version: not recorded - no client version probe was performed and none is claimed. Consuming project: not applicable; this is framework authoring, not a project engagement.

**Assignment and authority:**
Authoring scope is the coordinator-supplied packet at `tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-architect.md`. Provider `claude`, skill `devforge-architect`, exclusive fence `providers/claude/plugins/devforgeai/skills/devforge-architect/**` and `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/authoring/**`. Worktree `claude-scaffold-architect-20260910`, branch `author/claude-devforge-architect-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c` (verified before writing). No session-record artifact ID was supplied and none is invented; `execution_ref` for any artifact produced under this assignment would be `null` with the reason in `missing_inputs`. Integration owner: the DevForgeAI integration owner, for shared contracts, roster, manifests, hooks and installation.

**Roster role:**
SKILL-005 in the accepted roster, currently recorded there as "Proposed" with no source. Authoring this candidate does not amend the roster, change `docs/mvp/package-index.json`, or certify a framework capability. Neither file was touched.

**Selected source records:**

| Record | Governing source or preserved location | Revision or artifact ID | SHA-256 | Selection authority and purpose | Gaps or conflicts |
| --- | --- | --- | --- | --- | --- |
| Governing design specification | `docs/mvp/specifications/skill-005-devforge-architect.md` | c17e758 | `b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b` | Packet-selected; defines required behaviour | Matches the digest the packet named |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | c17e758 | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Authoring, provider and packaging boundary | Matches the packet's prefix |
| Artifact contract | `docs/mvp/artifact-contract.md` | c17e758 | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Envelope, provenance, storage | None |
| Execution contract | `docs/mvp/execution-contract.md` | c17e758 | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Worktree ownership, failure cases | None |
| Development language policy | `docs/development-language-policy.md` | c17e758 | `3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f` | Rust authority; the ceremonial-enforcement prohibition | None |
| Bounded delivery | `docs/learned-behaviors/bounded-delivery.md` | c17e758 | `22a0388c3a4afdb32beace2fb0082ec02acea885e45650f0b42925b76c09e7ae` | Finish line and stopping conditions | None |
| Roster | `docs/mvp/roster.md` | c17e758 | `ea35b825f8d2ea58ea0eb20b77c2fdd47df1dc2ddb3bbcfef3b032874e5f57bc` | Provenance flow and sibling ownership | SKILL-005 recorded as Proposed |
| Output template | `docs/mvp/templates/devforge-architect/architecture-contract.md` | c17e758 | `38b4ec73345e05563fcffc0efe6a8165b9cfa2f32eca40254e90b53ae5ad1218` | Copied to `assets/`, byte-identical | Matches the packet's digest |
| Shared handoff template | `docs/mvp/templates/shared/handoff.md` | c17e758 | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | Copied to `assets/`, byte-identical | Matches the packet's digest |
| Template for this document | `providers/claude/.../devforge-project-expert-creator/assets/skill-design-spec.md` | 4999f31 (worktree `claude-scaffold-project-expert-creator-20260910`) | not recorded; read via `git show` at that commit, and that worktree's HEAD has since advanced to 8c0bdd0 | Packet-selected frozen builder | The builder is a draft under independent review; see the change record |
| Evaluation runner and graders | `providers/claude/.../devforge-evaluate-expert/scripts/{run_cases.py,graders.py}` | e52ac596cbf790dfa156d883852d392c512fdbcc (worktree `claude-scaffold-evaluate-expert-20260910`) | not recorded; read at that commit for its interface only | Packet-named dependency for the `cases.jsonl` schema | That package is itself under independent review; its bytes were read, never run against this candidate |
| Claude client facts | `https://code.claude.com/docs/en/skills` | retrieved 2026-09-10 UTC | not applicable | Frontmatter, discovery, invocation and shell-injection behaviour | Documentation describes the client; no running client was observed |

**Canonical source and generated runtime mapping:**

| Purpose | Selected path and provider | Identity or manifest reference | Ownership and refresh responsibility |
| --- | --- | --- | --- |
| Canonical framework source | `providers/claude/plugins/devforgeai/skills/devforge-architect` (claude) | `../file-manifest.json` | This assignment's author |
| Installed project copy | The consuming project's `.claude/skills/devforge-architect`, when an owner generates it | Not generated | Integration owner |
| Plugin export | The `devforgeai` plugin export, when an owner generates it | Not generated | Integration owner |
| Working specification | This document, in the authoring evidence tree | Digest in `../file-manifest.json` is package-scoped and excludes this file | Authoring owner |

A provider source folder alone is not a discovered installation. Nothing was installed, exported, bound or run.

**Package derivations:**
Recorded in the package's own maintenance record at `references/derivation.json`, which carries both shared-template copies with their source and destination digests, the three distilled references with the contract sections they narrow, and the refresh conditions. That record contains no digest of itself.

**Authority, contract, installation or provider gaps:**
The evaluation runner and graders are in a sibling package under independent review at `e52ac596cbf790dfa156d883852d392c512fdbcc`; if that package changes its case schema, `evals/cases.jsonl` needs a matching refresh. No real stack or test adapter exists. No route exists from this skill to the external policy file. Several named sibling skills are not implemented.

**Preserved boundaries:**
Untouched, and outside this fence: `docs/mvp/**` including the specification, both shared templates and every contract; `docs/mvp/package-index.json` and `docs/mvp/roster.md`; every sibling skill in either provider; plugin manifests, hooks and agents; the companion DevForge repository's gates, policies and tests; and both sibling worktrees, which were read only.

**Authoring and release status:**
Authored candidate. Evaluation and adoption are separate; a source or package identity establishes no activation, quality or release readiness.

## 11. Evaluator repair intake

Not applicable. This is a first authoring pass, not a repair from an evaluator handoff.

## 12. Change record

**Identity and authoring scope:**
Record `ARCH-SCAFFOLD-R1`, 2026-09-10 UTC. Assignment: the coordinator packet named in section 10. Provider `claude`, target skill `devforge-architect`, permitted paths as fenced there, requested action **create**.

**Input references:**
The selected sources in section 10, at the digests recorded there. No prior candidate, report or frozen manifest exists for this skill, so there is no drift reconciliation to perform.

**Change mapping:**

| Finding IDs | Change ID | Change type | Requirement IDs | Disposition | Old path and SHA-256 | New path and SHA-256 | Summary or reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| not applicable | CHG-001 | new package | SKILL-005 whole | applied | absent | see `../file-manifest.json` | Create the Claude `devforge-architect` scaffold from SKILL-005 |

**New canonical source manifest:**
`../file-manifest.json` holds the complete package-relative path-to-digest map. It does not include its own digest, and it excludes the authoring evidence files, which are not part of the package.

**Resulting specification identity:**
This document, revision 1, at the path in section 9. No prior revision exists.

**Preserved behaviour and requirements:**
No existing behaviour was changed. Every sibling skill, shared template, contract, manifest and roster entry is byte-unchanged.

**Derivations and generated-copy work remaining:**
`references/derivation.json` is complete for the two copied templates and the three distilled references. No installed copy or export was generated; that is integration-owner work.

**Deferred proposals, gaps and evaluation prerequisites:**
The proposed defaults in section 9 await a user or integration-owner answer. The T1-T3 classifications await the same. Tiers A, B and C are `NOT_RUN`. An independent evaluator, an evaluation workspace, and the runner package's confirmed identity are prerequisites for any of them.

**Finding status:** Not applicable; no evaluator findings exist.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

**Next handoff:**
`../handoff.md`, allocated to an independent evaluator. It is a prepared document, not a receiving invocation. No evaluation is launched, and no adapter gap is closed by writing it.

## Evaluation coverage proposed

Accepted baseline: none exists, so the tier-B baseline label is `without_skill`; `old_skill` becomes available only after a second revision. Capability and environment scope: the Claude provider only. Codex is `NOT_APPLICABLE` to this assignment's scope, while overall Codex support for SKILL-005 remains `NOT_EVALUATED`.

Current candidate: the package enumerated in `../file-manifest.json`. No prior accepted baseline exists, so no earlier observation transfers.

Coverage proposed: tier C first (ARCH-PKG-001, ARCH-PKG-002, run against an actual installed or exported copy in a consuming project where the source docs are unavailable), then tier B (`evals/evals.json` ids 1-9 with their `cases.jsonl` deterministic anchors), then tier A (`evals/triggers/trigger-queries.json`, train split only for any description iteration, validation split held out and never placed in an author-loop context).

Evidence that is missing: everything behavioural. No installation, export, binding, discovery, activation, loading or output observation exists for this package. Tiers A, B and C are `NOT_RUN`. This skill proposes evaluation coverage; a separate evaluator and an independent reviewer assess it.
