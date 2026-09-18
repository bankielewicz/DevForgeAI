---
id: DEVFORGEAI-SKILL-BUILDER-POSTMVP-001
target: codex-cli
specification_version: "1.0"
status: proposed
recorded: "2026-09-14"
artifact_kind: skill_extension_specification
implementation_status: not_implemented_by_this_document
---

# Skill Builder Post-MVP: Executable Workflow Design and Validation Handoff

## 1. Purpose, ownership, and compatibility

| Selection | Value |
| --- | --- |
| Document destination | `C:\Projects\DevForgeAI\docs\specs\skill-builder-postmvp-spec.md` |
| Specification ID | `DEVFORGEAI-SKILL-BUILDER-POSTMVP-001` |
| Authoring owner | `$skill-creator` |
| Development target | `C:\Projects\DevForgeAI\src\agents\skills\skill-builder` |
| Independent package evaluation owner | `$skill-validator` |
| Operational copy, excluded from implementation | `C:\Projects\DevForgeAI\.agents\skills\skill-builder` |

Enhance skill-builder so generated skills have explicit, observable workflows, economical resource loading, defined failure and delivery behavior, and a complete manual evaluation handoff.

These enhancements address avoidable ambiguity and missing execution contracts. They do not guarantee successful validation or establish that the existing builder caused the QA evaluation timeouts. The [referenced QA validation](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/skill-validations/qa/20260914T1949120508210Z/validation-report.md) concluded INCOMPLETE without confirming a runtime-source defect. The [RCA](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/root-cause-analyses/qa-completion/20260914T2024442802835Z/analysis.md) distinguishes source-authoring completion from evaluated-build completeness.

The user selected strict separation of authoring from validation and the addition of instructions plus deterministic custody support. Saving this specification completes the document-authoring task; it does not enhance, test, validate, or install either skill. A later implementation request must select this document explicitly.

Concrete authoring paths in this section and the final invocation are selection metadata. They MUST NOT be copied into reusable generated runtime instructions. Frontmatter deliberately omits `skill_name`: this is maintenance of the existing builder, not another candidate for ordinary name-based specification lookup.

### Governing contracts

Read the [current development package](../../src/agents/skills/skill-builder/SKILL.md) together with:

- [Skill Builder Authoring Enhancement](../plan/skill-builder-authoring-enhancement-spec.md).
- [Skill Builder Adaptive Enhancement](../plan/skill-builder-adaptive-enhancement-spec.md).
- [Repository instructions](../../AGENTS.md) and the [compiled-Rust authority design](../plan/devforgeai-codex-rust-enforcement-design.md).

This extension changes only the requirements explicitly defined below. Preserve existing conversational authoring, specification builds, imports, adoption, adaptive sets, metadata, custody, regeneration, and manual handoff behavior. Where historical documents assign generated-skill testing to builder, the current authoring-only contract and SBP-001 govern.

The RCA and QA validation report supply motivation and evidence limitations. They are not universal requirements for every generated skill. Existing source and manifests must be inspected and bound before implementation; historical digests are not permission to restore an older package.

MUST and MUST NOT identify mandatory behavior. Proposed interfaces and acceptance cases below are implementation requirements, not claims of available commands or executed tests.

### Required boundaries

**SBP-001 — Preserve independent evaluation.**

During ordinary authoring, builder MUST NOT run generated skills, structural checkers, graders, tests, smoke trials, or automatic validator calls. It MUST NOT generate executable evaluation campaigns.

Builder MAY perform its existing custody operations and the authoring-input capture operations specified here. These operations cannot determine skill quality. Parsing the shape, identity, paths, and references of the new authoring input is permitted custody work; it is not a structural or semantic assessment of the generated skill.

Maintenance through skill-creator MAY test changed builder implementation. That permission does not become permission for the resulting builder to test generated skills.

Operational copies, validator implementation, existing generated skills, installation, hooks, CI, and Rust implementation are excluded from this enhancement. Disposable generated packages used by separately authorized evaluation are evaluation fixtures, not permission to modify existing generated development packages.

No required MCP server, browser, GUI, network service, or future framework command is introduced.

## 2. Generated-skill design requirements

### Observable behavior

**SBP-002 — Describe executable outcomes before generation.**

Before candidate generation, builder MUST record the selected skill's externally observable behaviors in the design artifact defined in section 3.

For each behavior, identify:

- Its invocation condition and required inputs.
- The selected requirement IDs or source-qualified locators.
- Its observable completion condition.
- Required outputs and how their destinations are selected.
- Necessary capabilities, dependencies, and authorized effects.
- Failure handling, interrupted-work recovery, and the next owner where applicable.
- The package resources responsible for implementing the behavior.

“Perform QA,” “ensure correctness,” or “follow all requirements” alone is not an observable completion condition.

Expected behavior MUST come from selected requirements or explicitly identified design decisions. Builder MUST NOT derive the expected result by copying current implementation output.

A missing decision that changes required behavior blocks the affected authoring work. It is not filled with an invented product fact. Independent authorized authoring may continue. Open questions record gaps; they do not certify the dependent design as complete.

**SBP-003 — Preserve task-specific execution semantics.**

Generated instructions MUST distinguish planning, execution, and handoff only where those distinctions apply to the selected skill.

Where the selected task authorizes a complete workflow, the generated instructions MUST define how work proceeds through its required outputs without an invented approval boundary.

Where the task expressly limits execution, requires additional permission, or belongs to another owner, the generated instructions MUST preserve that boundary.

Do not impose QA-specific modes, stop classifications, percentage thresholds, or phase names on unrelated skills.

### Resource loading and reusable operations

**SBP-004 — Make resource loading conditional and explicit.**

Every generated reference, template, or helper MUST have a consumer and an identifiable loading condition.

Keep shared purpose and essential constraints in `SKILL.md`. Put substantial branch-specific detail in the resource used by that branch.

Instructions MUST NOT require loading all resources before every task unless every resource is necessary for that task.

Requirements that must remain visible across branches may remain in the entrypoint. Their detailed explanation should have one authoritative location rather than multiple independently editable copies.

No fixed token limit or arbitrary file-count target is introduced.

**SBP-005 — Select helpers by concrete repeated operations.**

Builder MUST consider a helper when generated workflows would otherwise repeatedly reconstruct the same deterministic transformation or file operation.

A generated helper requires a defined:

- Input and output contract.
- Runtime and dependency requirement.
- Permitted write scope.
- Error behavior and exit semantics.
- Calling resource and invocation condition.
- Reason that a helper materially reduces repeated implementation work.

Do not generate a helper solely to create a status file, print a predetermined success result, or wrap a one-off action without a reusable benefit.

Builder authors helpers but does not execute them. Their testing remains an explicit validator obligation.

### Completion and interruption

**SBP-006 — Define artifact delivery as behavior.**

For skills that produce files, instructions MUST define:

- How the literal destination is resolved.
- When each required artifact becomes available.
- How required outputs are read back.
- How missing or failed writes are reported.
- What remains incomplete when delivery fails.

An announced intention, template, or future file path is not a delivered artifact.

For workflows with meaningful intermediate deliverables, preserve those deliverables at their natural completion boundaries. Do not postpone all useful output until a final narrative when the selected contract permits earlier delivery.

This does not require every simple skill to create checkpoints or intermediate files. Host write restrictions take precedence; describe unsaved outputs honestly instead of changing destinations or claiming successful delivery.

**SBP-007 — Define bounded recovery without inventing completion.**

For interruptible or retrying workflows, instructions MUST identify the state needed to resume safely, ownership of affected processes or resources, uncertain effects, and the conditions under which a retry is permitted.

A killed process cannot be assumed to have executed its cleanup instructions. Parent-owned recovery and skill-owned recovery must remain distinguishable.

A selected timeout MUST be classified as either:

- A specified behavior/performance requirement; or
- An execution ceiling whose exhaustion leaves evidence incomplete.

Builder MUST NOT invent runtime measurements or treat the validator's default 120-second ceiling as a universal product requirement.

### Adversarial authoring

**SBP-008 — Record relevant adverse conditions before handoff.**

For each applicable selected requirement, identify conditions that could produce a superficially successful but incorrect result.

Examples include:

- Missing or contradictory input.
- A dependency or platform that is unavailable.
- A partially completed workflow.
- A stale candidate or evidence reference.
- A required output that was announced but not written.
- Correct detection followed by incomplete failure-report delivery.
- A retry that repeats an uncertain side effect.
- A successful helper presented as proof of the entire workflow.

Record the condition and requirement-derived expected observation. Do not generate executable fixtures, score the candidate, claim the condition was tested, or add irrelevant adversarial requirements.

Validator must derive its own fixtures and oracles independently. Builder's examples are design information, not authoritative expected-results files.

## 3. Design artifact and deterministic custody support

### Artifact contract

**SBP-009 — Add one external design artifact.**

Add these resources to the development builder package:

- `assets/authoring-design-template.json`
- `schemas/authoring-design.schema.json`
- `references/workflow-design.md`

The template is consumed during authoring. It is not copied into generated runtime packages by default. The filled artifact is stored in the selected disjoint authoring input area before staging, following existing input capture rules.

The JSON artifact uses `schema_version: "authoring-design-v1"` and these required fields:

| Field | Type and meaning |
| --- | --- |
| `target_name` | Nonempty string matching the selected contract identity. |
| `source_refs` | Array of existing `{path, sha256}` requirement/input references; excludes the design itself. |
| `behaviors` | Nonempty array of the behavior records below. |
| `resources` | Array of planned package-resource records. |
| `adverse_conditions` | Array of relevant non-executable challenge descriptions. |
| `execution_limits` | Array of supplied limits and their provenance; empty when none is selected. |
| `open_questions` | Array of unresolved decisions with affected behavior IDs and owner. |

Each behavior contains:

`id`, `requirement_ids`, `trigger`, `inputs`, `completion`, `outputs`, `resource_paths`, `prerequisites`, `effects`, `failure`, and `recovery`.

- `id`, `trigger`, `completion`, `failure`, and `recovery` are nonempty strings.
- `requirement_ids` is a nonempty array of strings.
- Other fields are arrays of strings.
- A genuinely inapplicable failure or recovery condition is described explicitly rather than left blank.
- Output descriptions include observable content and destination-selection rules; a concrete runtime destination is not guessed during authoring.

Each resource contains:

- `path`: package-relative path.
- `kind`: `instruction`, `reference`, `template`, or `helper`.
- `purpose`: nonempty string.
- `load_when`: nonempty string.
- `helper_contract`: null for nonhelpers; otherwise an object containing nonempty `inputs`, `outputs`, `runtime`, `effects`, `errors`, and `reuse_reason` strings.

Each adverse condition contains nonempty `id`, `behavior_id`, `condition`, `expected_observation`, and `requirement_basis` strings.

Each execution limit contains:

- `behavior_id`: nonempty string.
- `seconds`: positive integer.
- `kind`: `specified_requirement` or `execution_ceiling`.
- `source_basis`: nonempty string.

Each open question contains nonempty `id`, `question`, and `owner`, plus a nonempty `affected_behavior_ids` array.

Reject unknown fields, duplicate JSON keys, nonfinite numbers, duplicate IDs, and invalid package-relative paths. Behavior IDs are unique within `behaviors`; adverse-condition and question IDs are unique within their respective arrays. Resource paths are unique. Referenced behavior IDs must resolve within this artifact, and behavior resource paths must name declared resources. String-array members are nonempty. `source_refs` follow the existing raw-byte SHA-256 reference contract and must resolve to selected contract inputs other than the design itself.

These are authoring-input integrity checks, not generated-skill quality checks. Mechanical reference resolution does not establish that an oracle is correct or a resource implements the promised behavior.

Simple skills may use one behavior, one resource, and empty arrays where applicable. Do not manufacture complexity to populate the artifact. Preserve the bounded capture ceiling of 2,000 files and 32 MiB; this artifact and its referenced inputs remain within the existing boundary rules.

### Capture and publication

**SBP-010 — Extend the existing begin interface.**

Add an optional `--design` file argument to `scripts/authoring.py begin`.

This is a proposed interface addition, not a command currently claimed to exist. The existing `--contract` and `--run-root` arguments retain their meanings. Relative input arguments resolve from the actual command working directory under the existing safe-path rules; filenames and arguments remain data for the native shell.

For new create, edit, import, and specification-build invocations through the enhanced skill:

1. Prepare the design before staging.
2. Include its exact `{path, sha256}` reference in the existing authoring contract's `inputs`.
3. Supply that same file through `--design`.
4. Validate its authoring-input shape and identity.
5. Capture its exact bytes using the existing bounded, disjoint-input rules.
6. Write `design-capture.json` binding the original reference and captured input reference.
7. Bind that capture record from the run's internal origin metadata.

The original reference must identify the same source path and digest as the contract input; reject an unbound or conflicting design. Reuse the normal input snapshot instead of introducing a second independently mutable design copy. Do not change the supplied contract bytes or add fields to `validation-request-v1`.

`design-capture.json` contains `schema_version: "authoring-design-capture-v1"`, `run_id`, `target_name`, `source_ref`, and `snapshot_ref`. The two references use the existing `{path, sha256}` shape. Add `design_capture_ref` to the internal origin metadata for design-enabled runs; do not add it to the closed authoring contract or validator request schemas. Capture and readback must finish before returning STAGED.

Legacy CLI calls without `--design` remain supported. Existing stages remain readable and publishable under their original contract. Adoption-only, proposal, and update-review operations do not acquire a mandatory design artifact unless they also perform selected authoring. Preserve the existing exit-code contract: successful operations return 0, recorded BLOCKED/PARTIAL results return 1, and rejected input/uncaught handled command errors return 2. Retained error artifacts and stdout/stderr must describe actual effects rather than imply rollback.

**SBP-011 — Preserve design custody during publication.**

For a design-enabled run, publication MUST recheck:

- Original design bytes.
- Captured design bytes.
- The design capture record.
- Their contract and origin bindings.

Missing or changed design evidence stops dependent publication under existing BLOCKED/PARTIAL semantics. Preserve failed attempts and actual applied deltas. Do not silently downgrade a design-enabled run to legacy behavior.

A substantive design change after staging requires a fresh linked run. Do not modify the captured contract or design to match later output.

These checks do not determine whether the authored workflow implements the design correctly. Existing per-path rechecks, delivered readback, baseline publication ordering, and failure preservation continue to apply. A failed capture or publication cannot become a successful new baseline by omitting its design records.

**SBP-012 — Keep the validator handoff backward compatible.**

The design travels through the existing contract input and `specification_refs` mechanism. Preserve the exact current validator packet field set.

The generated manual prompt MUST identify:

- The design's path and digest.
- The original selected requirement sources.
- Open questions and unperformed helper/native obligations.
- The requirement for independent fixture and oracle construction.
- The distinction between authored design and observed behavior.

An absent validator does not block authoring. The handoff creates no permission for evaluation, installation, external effects, or automatic repair.

No validator source change is required by this extension. The existing validator can bind the added input through its current packet intake; it must still independently assess the generated package using the original requirements, rather than treat builder's design as a waiver or executed result.

## 4. Reporting and implementation scope

**SBP-013 — Report authoring and qualification separately.**

Update the authoring report and final handoff instructions to state:

- Source action: created, edited, or unchanged.
- Authoring state using existing AUTHORED/PARTIAL/BLOCKED meanings.
- Actual publication and design-capture references.
- Outstanding evaluation obligations.
- Validation and Testing as NOT_PERFORMED unless explicitly supplied, current-byte external evidence supports another statement.
- The next owner and concrete next action.

“Unchanged,” “AUTHORED,” or “handoff delivered” MUST NOT imply evaluated-build completion.

Do not search for and automatically consume validator findings or initiate a repair cycle. A current user-selected external result may be bound and reported under the existing exact-byte rules without rewriting earlier authoring records.

**SBP-014 — Make narrow, compatible implementation changes.**

Implement through skill-creator in development source.

Update the entrypoint, authoring/specification references, custody documentation, regeneration guidance, handoff guidance, and authoring report template coherently. Add the three design resources and the bounded `authoring.py` support specified above.

Reuse the existing schema utility where its supported vocabulary suffices. Add no dependency, service, package initializer, plugin, or universal phase registry.

Preserve:

- Supported metadata and automatic invocation.
- Existing contract/request schemas and legacy meanings.
- Baseline/current/candidate comparison.
- Path and source-drift safeguards.
- Adaptive member independence and set boundaries.
- Historical evidence and failed attempts.

For selected adaptive sets, capture a design per authored member through its existing authoring contract. Do not infer or expand set membership.

Update the development package manifest for the actual delivered artifact changes. A package manifest establishes artifact identity, not successful execution or acceptance.

## 5. Independent verification and acceptance

**SBP-015 — Test the enhancement without transferring evaluation ownership.**

Skill-creator maintenance must follow repository TDD for changed executable custody behavior. Retain red, green, refactor decisions, regression results, and actual command receipts in a fresh maintenance evidence directory.

A separate skill-validator task must independently evaluate the enhanced builder and representative skills it generates.

The mandatory Python JSONL evaluation bundle remains external to generated runtime packages and includes runner, graders, fixtures, expected results, schema, runtime/dependencies, and byte bindings.

A test of the custody helper cannot substitute for a cold builder workflow. A cold builder workflow cannot substitute for independent evaluation of its generated skill.

Required scenarios follow. These are future obligations, not executed tests. SBP-015 governs the entire campaign; SBP-016 governs final delivery of its results.

| Case | Requirement mapping | Required observation |
| --- | --- | --- |
| SBPV-01 Simple skill | SBP-002, SBP-004, SBP-009 | Produces a minimal design and self-contained runtime skill without unnecessary helpers, phases, or resources. |
| SBPV-02 Multiple branches | SBP-003, SBP-004 | Generated resource loading follows the selected branch; unrelated references are not required unconditionally. |
| SBPV-03 Observable outcome | SBP-002, SBP-009 | Design and generated instructions define actual outputs and completion observations rather than restating a goal. |
| SBPV-04 Missing decision | SBP-002, SBP-003, SBP-008 | Reports the exact unresolved behavior decision and blocks dependent authoring without inventing an oracle. |
| SBPV-05 Helper selection | SBP-005, SBP-009 | A repeated deterministic operation receives a concrete helper contract; a trivial one-off operation does not generate a gratuitous helper. |
| SBPV-06 Authoring-only boundary | SBP-001, SBP-012 | Builder executes no candidate checker, generated helper, test, grader, or native workflow. |
| SBPV-07 Artifact delivery | SBP-006 | Independently exercised generated skill writes and reads back required outputs at the selected literal destination. |
| SBPV-08 Interrupted work | SBP-006, SBP-007 | Generated workflow preserves permitted intermediate evidence and distinguishes uncertain effects from completed work. |
| SBPV-09 Negative-path completion | SBP-006, SBP-008, SBP-013 | Detection of a failure does not count as complete when required report or recovery output is absent. |
| SBPV-10 Timeout distinction | SBP-007, SBP-009 | An execution ceiling is not presented as a universal performance requirement or a confirmed source defect. |
| SBPV-11 Design custody | SBP-009, SBP-010, SBP-011 | Original and captured design modification, deletion, incorrect hash, or incorrect target identity prevents successful publication. |
| SBPV-12 Invalid input | SBP-009, SBP-010 | Duplicate keys/IDs, unknown fields, nonfinite values, traversal, links, and disallowed overlaps are rejected without unintended writes. |
| SBPV-13 Publication interruption | SBP-011, SBP-014 | Retains actual applied changes and failure evidence; no successful next baseline after failed publication/readback. |
| SBPV-14 Existing workflows | SBP-010, SBP-014 | Legacy stages, no-design CLI calls, adoption-only operations, metadata preservation, and adaptive sets retain their defined behavior. |
| SBPV-15 Validator compatibility | SBP-012 | The unchanged validator intake accepts a valid new packet and rejects stale bindings; no new packet fields are required. |
| SBPV-16 Unchanged source | SBP-013 | Reports unchanged authoring separately from unperformed evaluation; does not manufacture source edits or claim qualification. |
| SBPV-17 Independent oracles | SBP-008, SBP-012 | Validator expectations are derived independently; builder's challenge descriptions are not treated as executed or authoritative results. |
| SBPV-18 End-to-end generation | SBP-001 through SBP-016 | A cold enhanced-builder invocation produces a skill, then separately authorized independent validation exercises that skill to complete required outputs. |

Use at least two representative generated skills for SBPV-18: one simple transformation and one branching workflow with file delivery and a relevant failure path. Fixtures must use different project layouts and include literal paths with spaces or Unicode.

Retain applicable existing builder regression scenarios. Any omitted case needs a requirement-based applicability decision; missing capability is not inapplicability. Discover the actual current regression/evaluation location instead of assuming the historical builder `tests/` directory or evaluator still exists.

Predeclare native trial commands, effects, outputs, case budgets, and retry policy. Do not increase a timeout silently after failure or count partial workflow observations as complete scenarios. Independently inspect and exercise actual generated artifacts; a model-authored design or a keyword match does not establish behavioral acceptance.

Apply repository numeric quality requirements to the declared executable implementation and required test inventories: executed-line coverage >=95% and required-case pass rate >=95%, independently per required platform and declared overall scope. Declare denominators and exclusions before collection, retain nonpasses and failed attempts, and report branch coverage separately. Report helper coverage separately from complete native scenario qualification. A passing percentage does not waive a failed mandatory scenario. Missing measurement is NOT_RUN or BLOCKED, not an estimate.

**SBP-016 — Final delivery and future invocation.**

Deliver:

- Updated development builder package.
- Exact change and preservation evidence.
- Updated artifact manifest.
- Executed maintenance evidence.
- Manual independent validator handoff.
- Explicit unresolved native or integration obligations.

The later implementation request is Codex conversation input:

```text
$skill-creator Implement C:\Projects\DevForgeAI\docs\specs\skill-builder-postmvp-spec.md in C:\Projects\DevForgeAI\src\agents\skills\skill-builder. Preserve the authoring-only boundary, operational copies, current contracts, and historical evidence. Follow the specification's maintenance testing and independent validation handoff requirements.
```

This document does not authorize operational installation or implement protected framework acceptance. Python custody and evaluation results remain evidence; compiled Rust retains protected DevForgeAI authority.

### Completion of the present specification task

Review this document's local links, schema-field definitions, requirement/scenario mappings, interface compatibility, ownership, failure handling, and terminal feasibility. Save and read back its actual bytes at the selected destination. Document checks establish only the reviewed specification artifact; do not claim builder implementation, red/green execution, native qualification, skill-validation PASS, or framework acceptance from writing this document.
