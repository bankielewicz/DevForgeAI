---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-devforge-design-scaffold-20260910"
artifact_type: "skill-enhancement-spec"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T20:18:54Z"
producer:
  skill: "devforge-evaluate-expert (source-loaded, not installed)"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac (sha256 of the SKILL.md blob at claude-scaffold-evaluate-expert-20260910 commit e641797eebf04cd1e8eb9f711549e038e7745407)"
execution_ref: null
upstream:
  - artifact_id: "EVREPORT-devforge-design-scaffold-20260910"
    revision: 1
    store: project
    path: "verification-results.md"
    sha256: "cdbf6022ab557e35a0a3df9898da2d4d58a7442fbfd0a640b26f55578f38ea4c"
    sections:
      - "Findings"
      - "Requirement coverage against SKILL-003"
      - "Decision and coverage"
  - artifact_id: "SKILL-003"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-003-devforge-design.md"
    sha256: "4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb"
    sections:
      - "Workflow and phase exits"
      - "Rework, stopping, and recovery"
evidence:
  - path: "findings.json"
    sha256: "d274779599f18e4aa24becffc7967c8bb9ff4a8a9f6517be2e83aa5d10dc5030"
  - path: "validation-results.json"
    sha256: "30ec3e3827773ff2e0aa42d4eccaa71cfd38caa6dfd105818851d577c9cc4a85"
  - path: "ai-review.json"
    sha256: "56d7d52474bbf05202ded00d46136c0ead6114a2c85bf07a4ae84f486e1218a1"
supersedes: null
decision_ref: null
missing_inputs:
  - "Session assignment record: none exists; execution_ref is null."
  - "Tier C, B and A observations: NOT_RUN. No change below is derived from behavioural evidence, because none exists."
---

# Skill repair and enhancement specification: devforge-design (SKILL-003)

Bounded, evidence-backed changes returned to the candidate's author. This authorises no automatic edit, invocation, installation, acceptance or release, and it expands no existing authorisation.

Every change below is backed by an observation recorded in `verification-results.md`. Nothing here is a style preference, and nothing here is a fabricated patch for an unproven cause.

## Immutable intake

- **Evaluated candidate:** worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910` at commit `9ad38de25a9941eb8ed67e9650430879f62032e4`; package `providers/claude/plugins/devforgeai/skills/devforge-design`; 23 files; `SKILL.md` sha256 `65dbb586ab78a43fa2b83a7e9c35f20272b3d4181ba08e6cc7519876de0e4c83`. The complete path-to-digest manifest is in `commands.log` and is identical, 23 of 23, to the author's `authoring/file-manifest.json`.
- **Installed copy evaluated:** none. Not installed and not exported; none was to be generated under this assignment.
- **Specification:** `docs/mvp/specifications/skill-003-devforge-design.md`, sha256 `4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb`.
- **Evaluation report:** `verification-results.md`, sha256 `cdbf6022ab557e35a0a3df9898da2d4d58a7442fbfd0a640b26f55578f38ea4c`.
- **Results record:** `validation-results.json`, sha256 `30ec3e3827773ff2e0aa42d4eccaa71cfd38caa6dfd105818851d577c9cc4a85`.
- **Independent review:** `ai-review.json`, sha256 `56d7d52474bbf05202ded00d46136c0ead6114a2c85bf07a4ae84f486e1218a1`.
- **Findings:** `findings.json`, sha256 `d274779599f18e4aa24becffc7967c8bb9ff4a8a9f6517be2e83aa5d10dc5030`.
- **Cases and fixtures:** the candidate's own `evals/cases.jsonl` sha256 `b4e0fdb91177b593b2a52a778c769049d4a2154782e12e8442de4b554d1f39ac`; the evaluator's added cases at `runner-out/evaluator-supplementary-cases.jsonl` sha256 `65d98620a5a7f3016103370f01911d88c3f40ef8e1939f3d84be74511146f7e2` and `runner-out/evaluator-nested-field-probe.jsonl` sha256 `15b6fe98884db255b2582c6805f73a4248a7ccc96c1d30cbf6a7c9712249ce69`.
- **Runner and graders relied on:** `scripts/run_cases.py` and `scripts/graders.py` in the `devforge-evaluate-expert` package at `claude-scaffold-evaluate-expert-20260910` commit `e641797eebf04cd1e8eb9f711549e038e7745407`. That package is a draft under bootstrap review.
- **Prior iteration:** none. This is the first evaluation of this candidate.

Verify these identities before editing and retain the old candidate bytes.

## Change decision

- **Are target changes justified by the evidence?** **Yes.** One `FAIL` (R04 / `CHK-SPEC-01`) and eleven further findings, each with an observation behind it.
- **Next owner:** the `devforge-design` scaffold author, under coordinator dispatch. (The validator's own template names `devforge-project-expert-creator` as the standing next owner; this assignment routes returns to the scaffold's author instead, and neither skill is installed, so the transfer is a coordinator dispatch and not an invocation.)
- **Behaviour that must be preserved unchanged:**
  - The whole inspection-versus-existence treatment: `SKILL.md:75-83`, `references/mockups-and-preview.md:29-41`, and the result vocabulary in `SKILL.md:106-108` and `references/recording-rules.md:82-93`. This is the strongest part of the package.
  - The authority boundary at `SKILL.md:18-24`, including the exact list of `devforge` subcommands, the statement that none reads a design-spec, and the routing of that gap to the integration owner.
  - The upstream-resolution procedure and the adoption boundary at `references/recording-rules.md:25-50`, and the no-self-digest write order at `:71-80`.
  - The `user-stated` fallback for the absent product-brief at `SKILL.md:53` and `references/recording-rules.md:51-61`.
  - The frontmatter: `name` and `description` only; `name` equal to the folder name; no `allowed-tools`, no `when_to_use`, no other client field.
  - Both `assets/` files as byte-exact copies of their governing templates. Do not edit them; a shared-template defect goes to that template's owner.
  - Every fixture's bytes, and the two sentinel digests hard-coded in `DX-B-007` and `DX-B-008`.
  - Runtime independence: no `docs/mvp` lookup, no repository path, no home path, no backtick-bang or bang-fence syntax anywhere in the package.
- **Forbidden scope changes:**
  - Do not edit SKILL-003, any `docs/mvp` contract or template, the `devforge-evaluate-expert` package, this report, or any file in this evaluation directory.
  - Do not weaken, delete or relabel a case to convert a recorded observation into a match.
  - Do not add a `scripts/` directory. Nothing here needs a helper, and the specification says to use scripts only for real deterministic operations.
  - Do not install, export, run or evaluate anything as part of applying these changes.
  - Do not expand the skill's scope. No new phase, no second document, no broader specification. `SKILL.md` is 132 lines; keep it well inside 500.
  - Do not add ceremonial enforcement, a self-issued outcome, or a command sequence that only appears to gate something.

## Requested changes

### CHG-001: a product-scope conflict has a named route out of the workflow

- **Finding IDs:** F-001
- **Severity:** MAJOR
- **Change type:** required repair
- **Accepted requirement:** SKILL-003, "Rework, stopping, and recovery": "Product-scope conflicts return to define-product via change; uncertain behavior becomes a bounded prototype." The second clause is implemented; the first is not.
- **Affected revision, file and section:** `9ad38de`; `SKILL.md`, section **4. Iterate** (lines 85-91) and section **Stopping** (lines 123-131).
- **Evidence and reproduction:** `verification-results.md` → Findings F-001; `ai-review.json` criteria R04. Reproduce by grepping the three prose files for `product-scope`, `change-request` and `define-product`: the only `devforge-change` reference in the package is the frontmatter exclusion at `SKILL.md:3`, and the only `devforge-define-product` references handle a *missing* product-brief, which is a different condition.
- **Demonstrated impact:** a session that finds mid-workflow that a requested flow contradicts an accepted requirement is correctly told not to change the requirement itself and has no stated successor. The instructions that do fit are the generic stop conditions, which name neither the owning skill nor the artifact the conflict should become.
- **Bounded desired behaviour:** after the change, a reader can determine, from `SKILL.md` alone, what to do when a requested design would require an accepted requirement to change. Specifically: the conflict is recorded rather than absorbed; it is named as a change request against the owning product artifact; the affected flows and requirement rows are identified; the design-spec's dependent rows are not declared ready; and — consistent with the package's existing honesty about absent siblings — the fact that `devforge-change` and `devforge-define-product` are not installed is stated, with a plain-language task the user can act on instead of a slash command.
- **Behaviour to preserve:** the existing prototype route at `SKILL.md:89` and `references/mockups-and-preview.md:55`; the suggested / installed / actually-invoked separation at `SKILL.md:99-104`; the rule against writing a slash command for an unconfirmed skill.
- **Acceptance condition:** a later evaluation can cite one or two locations in `SKILL.md` that carry the transition, and a new eval case exercises it.
- **Affected reruns:** add one case to `evals/evals.json` and `evals/cases.jsonl` for a request whose design would contradict an accepted requirement in the fixture brief. `fixtures/shared/PROD-001.md` already supports this — the existing `fixtures/stale/` set contains a revision-3 reversal of REQ-004 that could seed it — and the assertion routes to independent review, since no grader can establish that a conflict was routed rather than absorbed. Then rerun the new case and `DX-B-005`.

### CHG-002: an unobservable `producer.skill_revision` is routed to `missing_inputs`

- **Finding IDs:** F-002
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** artifact-contract, "Standard envelope": `missing_inputs` is "Explicit unresolved required information"; `producer` is "Native skill name and exact installed skill revision/digest".
- **Affected revision, file and section:** `9ad38de`; `references/recording-rules.md`, "The envelope" table, `producer` row (line 17).
- **Evidence and reproduction:** the row permits `unknown` "where nothing observable gives you the value" with no requirement to record it anywhere else; the same table's `missing_inputs` row (line 23) states the general rule the `producer` row does not invoke.
- **Demonstrated impact:** a design-spec produced when the skill revision is unobservable carries `unknown` in a required field and an empty `missing_inputs`. A consumer scanning `missing_inputs` to decide whether the artifact is complete sees nothing unresolved.
- **Bounded desired behaviour:** the `producer` row keeps `unknown` as the honest entry and adds that the same fact is recorded in `missing_inputs` with what it blocks.
- **Behaviour to preserve:** the rest of the row, in particular the correct narrowing of `skill_revision` to one file's bytes rather than a package or plugin digest, and the reasoning for it.
- **Acceptance condition:** the `producer` row names `missing_inputs`.
- **Affected reruns:** `DX-C-009` after CHG-008 adds `skill_revision` to its fields.

### CHG-003: interruption and resume have a stated rule

- **Finding IDs:** F-003
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** SKILL-003, "Workflow and phase exits": "On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again." And "Rework, stopping, and recovery": "If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming."
- **Affected revision, file and section:** `9ad38de`; `SKILL.md`, section **When something is missing or a check cannot run** (lines 106-115).
- **Evidence and reproduction:** the words "interrupt" and "interruption" appear nowhere in `SKILL.md`, `references/recording-rules.md` or `references/mockups-and-preview.md`. The two nearest bullets — changed upstream at `:110`, concurrent writer at `:112` — are conditions noticed while working, not a resume procedure.
- **Demonstrated impact:** a session interrupted mid-Render and resumed later can continue against upstream bytes that changed in the interval, because the only staleness check the package states fires on noticing a difference rather than on resuming. The read-back rule at `references/recording-rules.md:71-80` limits the blast radius to references written before the interruption.
- **Bounded desired behaviour:** one bullet in the existing list saying that on an interruption the current phase, the frozen upstream digests and the evidence paths are preserved, and that resuming re-checks those identities and the session assignment before dependent work continues — with a changed input starting a new iteration rather than continuing this one.
- **Behaviour to preserve:** the four existing bullets, unchanged. The `assets/handoff.md` "Resume and custody" section is a byte-exact template copy and must not be edited.
- **Acceptance condition:** a later evaluation can cite the bullet.
- **Affected reruns:** `DX-B-008`, or the extension of it if the author prefers to fold the resume condition into that case.

### CHG-004: `spec-mapping.md` claims match the bytes

- **Finding IDs:** F-004
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** skill-authoring-contract, "Common authoring workflow" step 5: record actual results and limitations. A coverage claim must be checkable.
- **Affected revision, file and section:** `9ad38de`; `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/spec-mapping.md` ("Rework, stopping, and recovery" table; "Workflow and phase exits" table, last row; "Coverage summary"; "Native creator authoring prompt" table) and `authoring/handoff.md` ("Result and next action").
- **Evidence and reproduction:** four claims recomputed from bytes and recorded in `commands.log` — the product-scope row (F-001), the interruption row (F-003), "24 trigger queries" (observed 23), and "four of the ten carry a deterministic grader … six route entirely to independent review" (observed five and five, contradicting `spec-mapping.md`'s own "Validation and behavioral acceptance" table, which already lists `required_report_fields` for `DX-C-009`).
- **Demonstrated impact:** `spec-mapping.md` is the coverage claim a later reader uses to decide what has been addressed. Two specification rows are marked addressed when the cited bytes do not carry them, which turns an open gap into an assumed-closed one.
- **Bounded desired behaviour:** after CHG-001 and CHG-003 land, both rows cite the new locations. The two counts are corrected. Nothing else in the file changes: every other claim in it verified against bytes.
- **Behaviour to preserve:** the file's existing structure and its "It is not evidence that any of it works" framing; the honest recording of the author's additions beyond the specification.
- **Acceptance condition:** every count and every "where addressed" cell in `spec-mapping.md` resolves to bytes that carry the claim.
- **Affected reruns:** none. This is an evidence record, not runtime behaviour.

### CHG-005: the case file states how to invoke it

- **Finding IDs:** F-005
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** skill-authoring-contract: "Define cases from requirements, keep fixtures reproducible." An authored case file has to be runnable by someone other than its author.
- **Affected revision, file and section:** `9ad38de`; `evals/fixtures/README.md` (add an invocation section); optionally a `notes` field on `DX-C-001`, which is a permitted case key.
- **Evidence and reproduction:** `runner-out/run1-packageroot-source.jsonl` — one invocation over the whole case file with `--candidate` = the package root returned `COULD_NOT_RUN` for nine of ten cases. `DX-C-001` needs `--candidate` = the package root and `--mode installed`; the other nine need `--candidate` = `<package>/evals/fixtures` and `--mode source`. The runner accepts exactly one `--candidate` per invocation.
- **Demonstrated impact:** an evaluator running the file the obvious way records nine blocked cases. The runner names the cause clearly, so the error is recoverable rather than silent — which is why this is MINOR — but the file cannot be executed as a unit without out-of-band knowledge.
- **Bounded desired behaviour:** `evals/fixtures/README.md` carries the two exact invocations, with the reason (`DX-C-001`'s candidate root is the package; every other case's root is the fixtures directory), and states that `DX-C-001` observes an installed copy so `evals` being present in a source run is the expected result rather than a defect.
- **Behaviour to preserve:** every `candidate_subpath` value and every assertion. Do not restructure the fixtures to force a single root; the split is correct, only undocumented.
- **Acceptance condition:** a reader can run both invocations from the README without inspecting the case file.
- **Affected reruns:** all ten cases, once, to confirm the documented commands are the ones that work.

### CHG-006: `DX-C-009` is labelled tier B

- **Finding IDs:** F-006
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** skill-authoring-contract, "Three separately reported evaluation tiers": C is installed resources in a consuming project where source docs are unavailable; B is output quality against a baseline. And: "Required C observations must pass before B or A admission for that candidate."
- **Affected revision, file and section:** `9ad38de`; `evals/evals.json` `evals[]` id 9; `evals/cases.jsonl` `DX-C-009`.
- **Evidence and reproduction:** id 9 declares `"tier": "C"` and `"baseline_comparison": "without_skill"` in the same object. A baseline comparison is the defining condition of tier B; the package's genuine tier C case, id 1, correctly declares `"baseline_comparison": "not_applicable"`. The case's prompt exercises readiness judgement under user pressure, which is output quality, not installed-resource resolution.
- **Demonstrated impact:** the contract gates C before B and A. A B-shaped case labelled C either blocks B/A admission on the wrong condition or gets excused, and it puts a baseline arm inside the tier whose reporting shape has none, so the two tiers stop being separately reportable.
- **Bounded desired behaviour:** id 9's `tier` becomes `B`; `cases.jsonl` `DX-C-009` becomes `DX-B-009` with `"tier": "B"`; id 9's `deterministic_cases` and the case id agree.
- **Behaviour to preserve:** the case's prompt, fixture, `expectations.summary`, assertions and `without_skill` baseline. Only the tier label and the case id change. `DX-C-001` stays tier C.
- **Acceptance condition:** every case whose `baseline_comparison` is `without_skill` is tier B, and the only tier C case is the installed-resource one.
- **Affected reruns:** the renamed case.

### CHG-007: the runner derivation is repointed at committed bytes and the five open schema questions are closed

- **Finding IDs:** F-007
- **Severity:** MINOR
- **Change type:** authorised enhancement
- **Accepted requirement:** skill-authoring-contract, "Package-local template copies and their derivation records": "For each copy, record the source path, exact source revision or preserved location and SHA-256."
- **Affected revision, file and section:** `9ad38de`; `references/derivation.json` `derivations[4]`; `docs/skill-authoring/history/.../authoring/authoring-notes.md`, "Evaluation-runner dependency: PENDING" and "Unresolved items for the coordinator" item 1.
- **Evidence and reproduction:** the entry declares `source_revision` "uncommitted working tree … its scaffold commit did not exist at authoring time" and `source_sha256` "not pinned". That commit now exists: `claude-scaffold-evaluate-expert-20260910` at `e641797eebf04cd1e8eb9f711549e038e7745407`. This evaluation settled all five consequences the author listed, by running the committed code:
  1. `routed_to` **is** an accepted assertion key (`run_cases.py` `ASSERTION_KEYS`). No routed assertion needs rewriting.
  2. The `name_folder_relation` flag is **`expect_equal`**, not `expect_name_matches_folder`. `SUP-S-001` asserted it and observed `MATCH` with `name='devforge-design' folder='devforge-design'`.
  3. `candidate_subpath: "."` **is** accepted; `run3` shows `DX-C-001` `COMPLETED`.
  4. `claim_evidence_binding`'s arg shape (`file`, `claim_field`, `evidence_fields`) is exactly as assumed, and the grader addresses structured files only — so the JSON-sidecar fixture convention is the right answer, not a workaround.
  5. `required_report_fields` addresses a nested envelope key by its **leaf name** but not by a dotted path: `SUP-P-001` observed `skill_revision` found at line 11 of the placeholder fixture, and `producer.skill_revision` reported as a missing field. Note the caveat — leaf-name matching is unqualified, so a leaf name that also appears as a top-level key would collide.
  All four runs of the candidate's own case file exited 0 with no invocation error, so the authored schema is valid against the committed runner.
- **Demonstrated impact:** the provenance record points at bytes with no checkable identity, and five questions that are now answerable stay open in the authoring notes and in the coordinator's unresolved list.
- **Bounded desired behaviour:** `derivations[4]` cites the committed `devforge-evaluate-expert` package at `e641797` with the digests of `scripts/run_cases.py` and `scripts/graders.py`, keeps `transformation` accurate ("authored to the schema this runner implements; nothing was copied"), and sets a refresh condition naming that package's pending `e101e76` recheck. `authoring-notes.md` records the five answers and marks the dependency closed against `e641797`.
- **Behaviour to preserve:** the four template derivations, all of which verified; the `no_self_digest` and `runtime_independence` statements; the honest `claims_not_made` block.
- **Acceptance condition:** no derivation entry declares an unpinned source, and the authoring notes carry no open question that the committed runner answers.
- **Affected reruns:** none required for the derivation edit itself; CHG-008 depends on answer 2 and answer 5.

### CHG-008: the deterministic layer asserts the facts an evaluator otherwise adds by hand

- **Finding IDs:** F-008
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement:** a proposal, grounded in `missing-rust-capabilities.md`: "a fact nobody wrote a case for is simply not observed."
- **Affected revision, file and section:** `9ad38de`; `evals/cases.jsonl`, `DX-C-001` and the case renamed by CHG-006.
- **Evidence and reproduction:** ten of the eighteen assertions across the ten cases carry `"grader": null`. Five structural facts the candidate asserts nowhere were asserted by this evaluator and all observed as expected: `runner-out/run4-supplementary-source.jsonl` (`SUP-S-001` … `SUP-S-006`) and `runner-out/run5-nested-field-probe.jsonl`.
- **Demonstrated impact:** no defect. The package's own layer would discriminate the facts an evaluator currently supplies, and closing CHG-007's answer 2 in the same edit removes the reason the assertion was originally omitted.
- **Bounded desired behaviour:** add to `DX-C-001`: `name_folder_relation` with `{"file":"SKILL.md","expect_equal":true}`; `package_relative_links` on `references/sources.md` and both `assets/` files; `path_present` for `references/derivation.json` and `references/sources.md`; and one `artifact_side_effect` asserting the two `assets/` digests that `derivation.json` declares, so a silent template drift is caught. Add `skill_revision` to the fields of the case renamed by CHG-006. The evaluator's two case files in `runner-out/` are working examples with observed results; reuse or adapt them.
- **Behaviour to preserve:** every existing assertion and every routed `grader: null` expectation. This adds; it replaces nothing. Do not convert a semantic expectation into a deterministic one — whether a flow is coherent, a stack rule was respected or a scope boundary was honoured cannot be established by reading bytes, and the package is right to route those to review.
- **Acceptance condition:** `DX-C-001` observes name-versus-folder, all shipped Markdown link sets, both provenance files and both template digests.
- **Affected reruns:** `DX-C-001` and the renamed placeholder case.

### CHG-009: `DX-C-009`'s `expect` value matches its own summary

- **Finding IDs:** F-009
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement:** internal consistency of the case file. No contract governs the `expect` string.
- **Affected revision, file and section:** `9ad38de`; `evals/cases.jsonl`, assertion A1 of the case renamed by CHG-006.
- **Evidence and reproduction:** the assertion declares `"expect": "complete"` while the same case's `expectations.summary` reads "A field whose value is a placeholder is a mismatch, not a match." The observed row was `MISMATCH`, `placeholder` (`run2`).
- **Demonstrated impact:** the runner never reads `expect`, so nothing observable changes. A reader comparing the `MISMATCH` row against `"expect": "complete"` would read the correct discriminating result as a failure. Note that the reference package's own convention is not uniform — `EX-DEF-009` uses `"incomplete"` while `EX-DEF-008` states the condition — so this is a readability fix, not a rule violation.
- **Bounded desired behaviour:** `"expect": "placeholder"` (or `"incomplete"`), matching the case's summary and the grader's `observed` value.
- **Behaviour to preserve:** the assertion, its grader and its args.
- **Acceptance condition:** every `expect` value in `cases.jsonl` reads as the predicted observation.
- **Affected reruns:** the renamed case.

### CHG-010: `DX-C-001` A5 observes something

- **Finding IDs:** F-010
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement:** internal consistency of the case file.
- **Affected revision, file and section:** `9ad38de`; `evals/cases.jsonl`, `DX-C-001` assertion A5.
- **Evidence and reproduction:** `run3` recorded `MATCH`, "0 local, 0 external" — `references/mockups-and-preview.md` contains no inline Markdown links, so the assertion cannot distinguish a package whose links resolve from one whose links do not.
- **Demonstrated impact:** a vacuous `MATCH` that reads as coverage it does not provide.
- **Bounded desired behaviour:** either drop A5, or keep it and add a real cross-reference from `mockups-and-preview.md` back to `recording-rules.md` if one is useful to a reader at that point. Do not add a link solely to make an assertion non-vacuous.
- **Behaviour to preserve:** A3 and A4, which observe four and one resolving destinations respectively.
- **Acceptance condition:** every `package_relative_links` assertion in the package targets a file that has at least one local link.
- **Affected reruns:** `DX-C-001`.

### CHG-011 (bounded decision, not a patch): trigger `A7b`'s category

- **Finding IDs:** F-011
- **Severity:** ADVISORY
- **Change type:** bounded investigation / owner decision
- **Question for the owner:** `A7b` — "Change the accepted requirement that says out-of-area postcodes are rejected at signup." — sits in `negative_define_product`, while the description routes changing an accepted requirement to `devforge-change`. Its `should_trigger: false` value is correct either way, so no activation expectation is wrong. Should a `negative_change` category be added before any tier-A run?
- **Evidence target:** the split is fixed at authoring time and stratified by category, so re-categorising one entry re-cuts the stratification. The author disclosed this rather than silently re-cutting it (`authoring-notes.md`, unresolved item 8), which was the right call.
- **Why no patch is specified:** the trade-off — a slightly wrong label on a fixed split, versus re-cutting a split that has not yet been used for any measurement — is an owner's call, not a defect with one correct repair.
- **Affected reruns:** none until tier A is allocated.

## Implementation order

CHG-001 and CHG-003 are the substantive repairs and are independent of each other. **CHG-004 depends on both** — it corrects the coverage claim after the gaps are closed. **CHG-008 depends on CHG-007** (answer 2 supplies the `expect_equal` flag name and answer 5 supplies leaf-name addressing) **and on CHG-006** (which renames the case whose fields it extends). **CHG-009 depends on CHG-006** for the same reason. CHG-002, CHG-005 and CHG-010 are independent of everything else. CHG-011 is a decision and blocks nothing.

## Evaluation prerequisites, not defects

None of these authorises a target edit, and editing the candidate will not produce any of them.

- **Tiers C, B and A are `NOT_RUN`** (F-012). No installed or exported copy exists, no fresh terminal or isolated workspace was allocated, and no install was to be attempted. Discovery, selection, loading, task completion, installed-resource resolution and output quality against a `without_skill` baseline are all unobserved. Owner: the coordinator, with the DevForgeAI integration owner for installation and export.
- **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI** (F-013). Every structural row in the report is `INSPECTION_MANUAL`, `authority: none`, and no decision receipt exists. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI** (F-013). The runner, grader, runtime and case identities are self-reported by the run. Owner: DevForge integration owner.
- **No `devforge` subcommand reads a design-spec, resolves its upstream references or verifies a mockup digest.** The candidate correctly names this as a missing integration; it is not something the author can supply. Owner: DevForge integration owner. Nothing in this specification asks for a simulated check in its place.
- **`devforge-define-product` is unimplemented**, so this skill's required upstream normally will not exist. The `user-stated` fallback is a proposed default awaiting an owner's decision. Owner: coordinator. CHG-001 must not turn it into an accepted rule.
- **The validator this evaluation followed is itself unqualified** — a draft under bootstrap review (E2: revise → repaired at `e101e76` → recheck pending), source-loaded rather than installed, with no native evaluation of its own. Its rubric criteria are DevForgeAI design requirements, not any provider's certification criteria, and a change to it invalidates the criterion outcomes bound here.

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before any finding is closed.
- Preserve the original failure history; never overwrite the recorded `FAIL` on R04 / `CHK-SPEC-01`.
- Never weaken an accepted expectation, delete a case or change a sibling gate to convert a recorded failure into a pass. A defect in a shared contract or template goes to its integration owner, not around it.
- Applying every change above still leaves the candidate at *insufficient evidence*, not *suitable for the stated scope*, because tiers C, B and A remain `NOT_RUN`.

**Validation status:** Not performed by this document.
**Finding status:** findings recorded; reevaluation required after any change.
