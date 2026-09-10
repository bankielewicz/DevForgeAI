# Skill design specification: devforge-evaluate-expert (Claude)

Working design document, derived from the frozen builder's `assets/skill-design-spec.md` and filled here rather than in the package. It carries the design, the framework authority and source mapping, and the change record. It certifies nothing; completing it establishes nothing about behaviour.

Optional sections that do not apply to this assignment (11, evaluator repair intake) are removed.

## 1. Identity and purpose

**Skill name:** `devforge-evaluate-expert`

**Purpose:** Determine whether an exact installed skill package - a generated project expert or a framework skill - activates appropriately and improves representative project work while respecting its constraints, and return evidence-bound results with a bounded repair specification to its author. Project-specific guidance changes the result because the evaluation is measured against *that* candidate's governing specification, its real consuming project and a relevant baseline, not against a generic notion of a good skill.

**Description for discovery:** See the authored frontmatter. It states the capability, the situations that should select it (asking whether a generated expert works, wanting a skill checked or graded before adoption, asking whether a SKILL.md only looks convincing, receiving a candidate needing acceptance evidence) and the three nearest workflows that must route elsewhere.

## 2. Scope and activation

**Use this skill when:** an existing skill package needs evaluating against its specification; someone wants evidence before adopting a generated expert; a builder hands over a candidate for acceptance evidence; a prior evaluation needs re-running against changed bytes.

**Outside its scope:**

| Nearby request | Belongs to |
| --- | --- |
| Write, repair or refresh a skill | `devforge-project-expert-creator` |
| Review application code or a change for correctness | `devforge-review` |
| Work out what to build | `devforge-brainstorm` |
| Implement an already-accepted story | `devforge-develop` |
| Check frontmatter or file presence only | Not an evaluation; explicitly excluded in the description |

**Example activating requests:** "I need this generated expert evaluated before we use it on real stories." / "Does this expert actually help, or does its SKILL.md just look convincing?" / "Grade this skill package against its specification and tell me what to fix."

**Near-miss requests that must not activate it:** "Fix the three problems the evaluator found." / "Review my changes for correctness before I merge." / "Evaluate whether Postgres or SQLite is the better fit." / "Just check the frontmatter is valid."

**How it should be invoked:** Automatically when relevant and explicitly by name - the default. Project-local installation is the stated default for scaffold evaluation (`/devforge-evaluate-expert`); the exported plugin is the recorded alternative (`/devforgeai:devforge-evaluate-expert`). No invocation-control frontmatter field is set.

## 3. Inputs and expected results

**Required inputs:** the governing specification; the exact candidate, with source and installed identities recorded separately; the consuming project's real inputs where cases need them; a baseline for any quality comparison; terminal availability and a permitted isolated workspace for native observations.

**Optional inputs:** a prior evaluation report, for regression cases and the previous revision's identity.

**When information is missing:** it stays missing, with its cause and the claim it blocks. Ask for a consequential runtime or budget choice; resolve routine paths from the assignment. Never fabricate a revision, digest, owner or approval, and never substitute an easier baseline after seeing results.

**Expected deliverable:** an evaluation plan (EVPLAN), an evaluation report (EVREPORT) with its evidence records, a bounded repair or enhancement specification, and a handoff naming the next owner.

**Output format and destination:** the assigned evaluation directory and report destination. An externally selected destination governs; never inside the evaluated candidate.

**Completion criteria:**

- Every required observation has a real terminal status or an honest missing-evidence cause.
- Structure, independent review and each of tiers C, B and A are reported separately.
- Both missing-DevForge-CLI-capability statements appear in the report.
- The repair specification and the handoff exist, with exact identities and one real next action.

## 4. Workflow

| ID | Level and parent | Action | Expected result | Classification | Enforcement route |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | Evaluate an exact candidate against its specification and return findings | Saved results, repair specification and handoff | Required | ER-01 |
| P1 | Phase; W1 | Intake and freeze | Frozen identities, allocation where selected, plan before measured runs | Required | ER-01 |
| T01 | Task; P1 | Identify target, provider, authority, specification, write fence | Recorded assignment | Required | ER-01 |
| T02 | Task; P1 | Freeze candidate, specification, cases, rubric, baseline | Frozen input identities | Required | ER-01 |
| P2 | Phase; W1 | Deterministic observation | Structural rows labelled by method | Required | ER-02 |
| T03 | Task; P2 | Observe structure, references, source and installed identity | Raw observations; behaviour still unevaluated | Required | ER-02 |
| P3 | Phase; W1 | Independent review | Per-criterion findings with independence limits | Required | ER-03 |
| T04 | Task; P3 | Inspect prompt engineering and framework compliance against R01–R10 | Criterion records with evidence | Required | ER-03 |
| P4 | Phase; W1 | Behavioural tests | Separate case outcomes, manifests, transcripts | Required | ER-04 |
| T05 | Task; P4 | Establish runtime, fixtures and observed boundaries | Preparation and readiness recorded separately | Required | ER-04 |
| T06 | Task; P4 | Tier C installed resources | Resource resolution in a consuming project | Required | ER-04 |
| T07 | Task; P4 | Tier B output quality against a baseline | Graded arms with matched facts | Required | ER-04 |
| T08 | Task; P4 | Tier A discovery and activation | Four observations kept separate | Required | ER-04 |
| P5 | Phase; W1 | Adjudication | Evidence-based disposition | Required | ER-05 |
| T09 | Task; P5 | Weigh evidence, applicability, coverage, freshness | Disposition distinguishing failure from gap | Required | ER-05 |
| P6 | Phase; W1 | Return to the builder | Saved results, repair spec, handoff | Required | ER-06 |
| T10 | Task; P6 | Write the verification results | Saved report | Required | ER-06 |
| T11 | Task; P6 | Write the bounded repair specification and rerun plan | Actionable change request | Required | ER-06 |
| T12 | Task; P6 | Deliver the handoff | Handoff with exact identities and one real next action | Required | ER-06 |

All twelve tasks retain the Enforced classification carried forward from SKILL-008. This is a preserved accepted classification, not a new decision made here, and no classification question was reopened.

**Dependencies and completion evidence:** a failed prerequisite makes only the *dependent* observations `COULD_NOT_RUN`; independent work continues and P5 and P6 still complete. C failure blocks dependent B and A claims. A B quality failure with intact boundaries does not block A. Any unsafe boundary, identity mismatch or candidate mutation stops dependent execution immediately.

**Conditional paths:** static-only selection preserves every native case with an explicit missing-observation cause and finishes the remaining phases. Worktree selection adds bounded allocation and preparation before T05.

**When to stop or seek clarification:** an unavailable runtime, missing raw inputs, or an independence requirement that cannot be met blocks the corresponding claim and no other. A consequential runtime or budget choice that was never made is a question; a routine path is not.

## 5. Task-specific rules

**Required standards:** the fixed result vocabulary, never blended into a score. Separate reporting of structure, review, C, B and A. Freeze expectations before measuring. `MATCH`/`MISMATCH`/`INDETERMINATE` for grader rows, kept disjoint from the authority vocabulary. Package-relative resource resolution with the consuming project resolved separately.

**Preferences:** concise handoffs that route attention into existing records rather than copying them.

**Actions requiring explicit authorisation:** any native run (needs an observed boundary and an authentication arrangement); any write outside the assigned evaluation area; creating worktrees (needs the frozen allocation).

**Known pitfalls, demonstrated in the fixture set:** a self-claimed PASS with null evidence; an incomplete negative transcript treated as a passing negative; an embedded instruction addressed to the evaluator; a package that is structurally clean and semantically wrong; frontmatter that no restricted parser can read, where the honest answer is neither a pass nor a defect.

## 6. Tools and supporting resources

**Target environment:** Claude Code on Linux/WSL2; the DevForgeAI repository is not required at runtime.

**Required tools:** `/usr/bin/python3` 3.12 for the case runner (standard library only). The DevForge CLI for the `expert prepare` / `expert status` grounding commands, which are the operator's. No model API key.

**Supporting materials:**

| Resource | Purpose | When needed |
|---|---|---|
| `references/framework-context.md` | Ownership split, path resolution, vocabulary | Intake |
| `references/evaluation-boundaries.md` | Read-only rules, artifact mapping, command table | Boundaries; P6 |
| `references/missing-rust-capabilities.md` | The two absent capabilities and the manual procedure | P2, P5 |
| `references/runner-interface.md` | Runner and grader contract and limits | P2, P4 grading |
| `references/ai-review-rubric.md` | R01–R10 | P3 |
| `references/native-evaluation.md` | Boundaries, probes, tier procedures | P4 |
| `references/results-contract.md` | Outcomes, evidence groups, findings, closure | P5, P6 |
| `references/contracts/*` | Packaged shared contracts | P1 and the rubric |
| `assets/*` | Record shapes and output templates | Their respective phases |
| `scripts/run_cases.py`, `scripts/graders.py` | Authored-case observations | P2 |

**Unavailable dependency behaviour:** record the specific unavailable dependency, the claim it blocks and its owner; continue everything that does not depend on it. Never fall back to an unconfined run or an API-backed harness while describing it as subscribed native testing.

**Enforcement routes ER-01 to ER-06 — requirement only:**

- **ER-01 / P1, T01–T02.** Requirement: frozen input identities and an assignment must exist before dependent inspection, review or any measured run. Protected action: starting a measured observation. Observable evidence: the frozen plan and its bound `{path, sha256}` input references. Freshness: invalidated by any change to the candidate, specification, cases, baseline or material runtime setting. Intended behaviour: refuse the measured run while an identity is missing or stale. Missing evidence: `COULD_NOT_RUN` for the dependent observation, reporting still possible.
- **ER-02 / P2, T03.** Requirement: structural observations must exist, with their method labelled, before a structural claim is made. Protected action: asserting a structural outcome. Observable evidence: the manual rows and any runner observations file. **This is the route the first missing capability would serve.**
- **ER-03 / P3, T04.** Requirement: one actual fresh independent review of every applicable criterion before a semantic claim. Observable evidence: the review record with reviewer identity and independence limits. Missing evidence: `COULD_NOT_RUN`; the claim is withheld, not softened.
- **ER-04 / P4, T05–T08.** Requirement: an observed boundary and installed identity before a measured worker launches; matching C before dependent B or A claims. Observable evidence: probe results, installation manifests, run manifests. Intended behaviour: refuse the launch when the boundary is unobserved.
- **ER-05 / P5, T09.** Requirement: complete current evidence and a coherent disposition before recording a suitability recommendation. **This is the route the second half of the first missing capability would serve.**
- **ER-06 / P6, T10–T12.** Requirement: saved results, a bounded repair specification and output identities before announcing delivery or transfer.

For every route: **Owner:** the DevForge integration owner. The check itself would be compiled into the DevForge CLI and invoked by whatever wiring that owner selects; this document records requirements, not implementations. **Feasibility:** unknown until that owner confirms it. **Status:** requirements recorded. No gate is implemented, activated or executed by this skill, and nothing in the authored package claims otherwise.

Two routes additionally record **"Enforcement requested; not confirmed available"**: ER-02 and ER-05 depend on capabilities that do not exist in the CLI today, which is exactly the dependency named in the package.

## 7. Acceptance cases — capture only

Captured, not executed. The full set with independently stated expectations is `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/evals/evals.json` (twelve tier-B cases) plus `evals/triggers/trigger-queries.json` (twenty-three tier-A queries with a fixed split). The runner's deterministic cases are `evals/cases.jsonl`.

| Case | Example request or input | Expected behaviour |
|---|---|---|
| Typical task | "Use DevForgeAI to evaluate this generated expert skill." | Plan and evidence-bound report plus handoff; missing capabilities named |
| Missing information | "…no working authenticated session right now." | Native observations `COULD_NOT_RUN` with cause; reporting still completes |
| Outside scope | "Check the error handling in this pull request." | Routes to `devforge-review`; no evaluation artifacts produced |
| Important variation | A structurally clean package that violates an excluded-work requirement | Structural pass, behavioural failure, finding cites both locations |

## 8. Placement and maintenance

**Availability:** bundled in the `devforgeai` plugin; project-local installation is the default evaluation mode.
**Installation location:** recorded in section 10. An installed copy is never an alternative source.
**Maintainer:** the DevForgeAI integration owner.
**Reasons to revisit:** a change to the Claude client's discovery or invocation surfaces; a revision of SKILL-008 or of the shared contracts; either missing CLI capability becoming available; a demonstrated failure in an actual evaluation.

## 9. Authoring decision and progress

**Current status:** authored; unevaluated.

**Working specification and target paths:** this document at `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/design/skill-design-spec.md`; the candidate at `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/`.

**Search scope and limitations:** searched the Claude canonical source inventory `providers/claude/plugins/devforgeai/skills/` in the assigned worktree at base `c17e758417da64928a0f47fc2600304465ac3f3c`, and the Codex canonical inventory for the port source. Not searched: any machine-level `~/.claude/skills`, any managed settings directory, any enabled plugin inventory in a live session, and any `--add-dir` location - none of which is reachable from this authoring context. The comparison is therefore bounded to the repository's provider sources.

**Related skills:**

| Candidate and source | Relevant overlap | Gap or distinction | Recommendation |
|---|---|---|---|
| `providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert` | Same SKILL-008 capability | Different provider; canonical sources are provider-specific by contract and the packages have diverged | Port, not reuse |
| `providers/claude/.../devforge-project-expert-creator` | Same paired workflow | Authors and repairs; explicitly excludes evaluating or grading | Separate workflow; it is the receiver of this skill's output |
| `providers/claude/.../devforge-brainstorm` | Framework skill in the same roster | Early-stage exploration; no overlap | Separate workflow |
| `providers/claude/.../devforge-develop`, `.../devforge-review` | Roster siblings | Implementation and application-code review | Separate workflows; `devforge-review` is the routing target for application QA |

**Selected approach and rationale:** **create**. No skill in the searched Claude inventory evaluates a skill package. The honest form of the result is "no suitable skill found in the searched inventory" - not a claim of global uniqueness. The Codex implementation exists but canonical sources are provider-specific under the authoring contract, so it is a port source rather than a reuse target.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| Run-manifest schema | v1 base plus four native extensions; no VPR-2 fields | Coordinator answer Q1 | Settled |
| Name/folder equality | Grader records both; asserts equality only on request | Coordinator answer Q2 | Settled |
| P3 independence | Manual fresh-session; coordinator-dispatched evaluator contexts | Coordinator answer Q3 | Settled |
| Frontmatter fields | `name` and `description` only | Coordinator answer Q3 | Settled |
| F01–F08, VPR-2, local baseline | Out of scope; one short historical paragraph retained | Coordinator answer Q4 | Settled |
| Default installation mode | Project-local `.claude/skills/`; plugin export recorded as the alternative | Coordinator answer Q5 | Settled |
| Missing-capability routing | Named in the package, the handoff and the coordinator report | Coordinator answer Q6 | Settled |
| Shell-injection syntax | Never used; command examples in plain text fences | Coordinator adopted constraint | Settled |
| Grader result vocabulary | `MATCH`/`MISMATCH`/`INDETERMINATE`, disjoint from the authority vocabulary | Proposed default by this author | Proposed; recorded for review |
| Runner exit-code semantics | Describes the program, never the candidate | Proposed default by this author | Proposed; recorded for review |
| `graders.py` has no CLI | Deliberate, so no second executable resembles a gate | Proposed default by this author | Proposed; recorded for review |
| Merging the worktree reference into native-evaluation | Reduction to keep the reference count below the Codex package's | Proposed default by this author | Proposed; recorded for review |

The four proposed defaults were not put to the coordinator as questions because the packet directed that no questions be asked and every material decision was already supplied. They are recorded here as proposals rather than as supplied requirements.

**Authored or changed files:** see the file manifest at `../file-manifest.json`.

**Material unresolved dependencies:** the two missing DevForge CLI capabilities (ER-02 and ER-05 routes). The frozen builder followed for this authoring is itself unvalidated; its bootstrap review runs in parallel and was not waited on.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

**Framework and provider:** DevForgeAI worktree `claude-scaffold-evaluate-expert-20260910`, branch `author/claude-devforge-evaluate-expert-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c`. Provider: Claude. Client version: not observed from a live session; this was an authoring task.

**Assignment and authority:** worker A2 under the coordinator's task packet, phases 1 and 2. Write fence: the package directory and this authoring directory. Integration owner: the DevForgeAI integration owner for shared contracts, installation and export.

**Roster role:** SKILL-008 in the accepted twelve-skill roster. Authoring this package amends no roster entry and certifies no framework capability.

**Selected source records:**

| Record | Governing source | Revision | SHA-256 | Purpose | Gaps |
|---|---|---|---|---|---|
| Governing specification | `docs/mvp/specifications/skill-008-devforge-evaluate-expert.md` | `c17e758…` | `0b3dbb7fe9f5f683d2022c86390e736346189e1ea4d92730c7234d9de1ecec0d` | Accepted requirements | Verified equal to the packet's stated digest |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | `c17e758…` | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Authoring, provider and packaging boundary | VPR-2 section recorded `NOT_APPLICABLE` |
| Artifact contract | `docs/mvp/artifact-contract.md` | `c17e758…` | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Envelope and digest rules | None |
| Execution contract | `docs/mvp/execution-contract.md` | `c17e758…` | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Authority, isolation, handoff | None |
| Language policy | `docs/development-language-policy.md` | working tree, read 2026-09-10 | recorded in the authoring notes | Rust authority and the evaluation exception | None |
| Builder followed | `providers/claude/.../devforge-project-expert-creator/**` at `69b6090bde458f48cae0f5751035be65fdb4593c` | that commit | recorded in the authoring notes | Authoring workflow | The builder is itself unvalidated |

**Canonical source and generated runtime mapping:**

| Purpose | Path | Ownership |
|---|---|---|
| Canonical framework source | `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert` | This author, under the assigned fence |
| Installed project copy | the consuming project's `.claude/skills/devforge-evaluate-expert` | Integration owner; generated, never edited as a source |
| Plugin export | an assigned `devforgeai` export directory | Integration owner; staging only |
| Working specification | this document | This author |

**Package derivations:** recorded in `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/references/derivation.json` with source path, revision `c17e758…`, source digest, destination digest, transformation and refresh condition for every copied template and contract, plus the ported and not-ported dispositions.

**Authority, contract or installation gaps:** the two missing CLI capabilities. No installation or export was performed; both belong to the integration owner.

**Preserved boundaries:** the Codex package (read only; unchanged), the DevForge CLI, its policies and gates, the shared contracts and templates in `docs/mvp`, the accepted roster, every other Claude skill, and the builder's worktree.

**Authoring and release status:** authored candidate. Evaluation and adoption are separate and have not occurred.

## 12. Change record

**Identity and authoring scope:** Claude scaffolding, 2026-09-10. Worker A2. Provider Claude, target skill `devforge-evaluate-expert`, action **create**.

**Input references:** the specification, contracts and templates listed in section 10; the Codex port source; the frozen builder at `69b6090…`; the phase-1 port analysis at `../port-analysis.md`.

**Change mapping:**

| Change ID | Type | Disposition | Old | New | Summary |
|---|---|---|---|---|---|
| CHG-001 | create | applied | none | `SKILL.md` | Ported entrypoint: P1–P6/T01–T12, boundaries, missing capabilities, progressive links |
| CHG-002 | create | applied | none | `references/**` (12 files) | Ported and reduced references, three packaged contracts, new derivation record |
| CHG-003 | create | applied | none | `assets/**` (13 files) | Three verbatim template copies plus ported record shapes at v1 with native extensions |
| CHG-004 | create | applied | none | `scripts/run_cases.py`, `scripts/graders.py` | The permitted JSONL runner and deterministic graders |
| CHG-005 | create | applied | none | `evals/**` (22 files) | Twelve acceptance cases, thirteen runner cases, twenty-three trigger queries, nineteen fixture files |
| CHG-006 | decline | declined | `scripts/inspect_skill.py`, `scripts/assess_evidence.py` | none | Not ported: validator gate and acceptance decision belong to compiled Rust. Replaced by the two named missing capabilities |

**New canonical source manifest:** `../file-manifest.json`, referenced separately; it contains no digest of itself.

**Resulting specification identity:** this document, revision 1.

**Preserved behaviour and requirements:** every SKILL-008 requirement mapped in `../spec-mapping.md`; the Enforced classification of all twelve tasks; the fixed result vocabulary; the author/evaluator separation.

**Derivations and generated-copy work remaining:** installation and export are the integration owner's and were not performed.

**Deferred proposals, gaps and evaluation prerequisites:** the two missing CLI capabilities; the unvalidated builder dependency; every tier A, B and C observation, which remain `NOT_RUN` because authoring is not evaluation.

**Finding status:** not applicable; this is a first authoring, not a repair.

**Validation status:** Not performed.

**Enforcement status:** Requirements recorded; no gate implemented by this skill.

**Next handoff:** `../handoff.md`, naming the independent evaluator (E2) as the next owner.
