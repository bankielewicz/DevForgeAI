---
id: CODEX-SKILL-BUILDER-AUTHORING-ENHANCEMENT-SPEC-001
target: codex
status: proposed
specification_version: "1.0"
recorded: "2026-09-12"
---

# Specification: Skill Builder Authoring Enhancement and Validator Handoff

This document records the agreed design for enhancing skill-builder. The current delivery creates this specification only; it does not implement or install either enhanced skill. A later package implementation request must select this document explicitly. It intentionally omits `skill_name` frontmatter because it is an enhancement specification for existing packages, not an ordinary new-skill build input.

## 1. Objective and design decisions

Enhance skill-builder with skill-creator's conversational creation, focused editing, scaffolding, and metadata-authoring capabilities. Make skill-builder an **authoring-only workflow**; skill-validator owns both validation and testing.

The specification covers the builder enhancement and the companion validator changes necessary for a complete handoff.

Confirmed decisions:

- A sufficiently clear conversational request authorizes authoring without separately approving a specification.
- During execution, ask where to save the skill. Recommend `{project root}\src\agents\skills\`, but accept another explicitly selected development-source location.
- Do not hardcode this repository's paths or assume every project uses a `src` tree.
- Builder returns the authored package and a validator request. It does not automatically invoke validator.
- Further authoring is allowed before validation or testing. An untested skill may be revised in the same way that untested code may be revised; that permission does not imply quality assurance.
- An existing skill without builder history can be captured and edited under the current request's authorized scope.
- Operational installation, personal active-skill folders, hooks, CI, and Rust implementation remain outside this enhancement.

Existing imports, explicit adoption, traceability, ownership protection, and conflict handling remain supported. Their completion semantics must be updated to separate successful authoring from successful testing.

The development packages in this repository are [skill-builder](../../src/agents/skills/skill-builder/SKILL.md) and [skill-validator](../../src/agents/skills/skill-validator/SKILL.md). Those links identify the current implementation targets, not mandatory locations for generated skills in other projects.

## 2. Authoring requirements

| ID | Capability | Required behavior |
| --- | --- | --- |
| AB-001 | Conversational creation | Accept a skill description, desired outcome, examples, and constraints without requiring an existing Markdown specification. Capture the resulting requirements before generating files. |
| AB-002 | Proportionate clarification | Resolve discoverable facts first. Ask only questions that materially affect behavior, scope, dependencies, or output. Reuse answers and current authorization; do not impose an interview count. |
| AB-003 | Portable destination selection | Ask for the destination and show the resolved project-relative recommendation. A destination already supplied in the current request answers that question. Distinguish the parent folder from the final skill directory. |
| AB-004 | Focused existing-skill editing | Support a requested correction or enhancement without reinitializing the package or demanding a separately approved specification. Preserve unrelated content, supported metadata, and resources. |
| AB-005 | Editing without prior history | Capture the existing package before editing. Record its origin as observed/unknown and the exact authorized change scope. Do not invent a previously successful build or silently adopt the entire package. |
| AB-006 | Optional scaffolding | Provide bundled, portable initialization functionality equivalent to skill-creator's initializer. Create the entrypoint, UI metadata, and selected resource directories when useful. Refuse an occupied destination; never initialize an existing skill again. |
| AB-007 | Resource selection | Create scripts, references, assets, examples, and templates only when they support concrete requirements. Complete or remove initialization placeholders during authoring. Do not generate an automatic README, changelog, installation guide, or empty resource tree. |
| AB-008 | UI metadata authoring | Support creation and focused updates of `agents/openai.yaml`, including display name, short description, default prompt, invocation policy, and explicitly requested optional fields. Preserve unrelated policy, dependency, and interface fields. |
| AB-009 | Invocation and naming | Preserve valid existing identities. For new skills, derive concise lowercase hyphenated names. Keep automatic invocation unless the user explicitly requests otherwise. Resolve collisions without silently selecting another identity. |
| AB-010 | Instruction design | Capture purpose, activation, inputs, outputs, operational constraints, dependencies, side effects, and recovery. Use the specificity needed by the task rather than a fixed phase structure. |
| AB-011 | Progressive disclosure | Keep shared purpose and essential routing in the entrypoint. Place substantial conditional detail in focused references. Small skills may remain self-contained. Inspect resource consumers before removing or consolidating files. |
| AB-012 | Examples and output contracts | Add representative examples only when they clarify decisions. Define structured output when the task requires it; do not impose JSON, particular headings, or fixed example counts universally. |
| AB-013 | Narrow revisions | Apply the requested change while retaining useful existing structure and domain contracts. Broader restructuring requires a concrete requirement or current user direction. |
| AB-014 | Honest completion | Report the authored destination, changed files, recorded history, unresolved authoring gaps, and validator handoff. Never describe unperformed validation or testing as passed. |

Conversational creation, direct editing without history, portable destination selection, and bundled scaffolding add capabilities to the current builder workflow. Resource selection, metadata preservation, instruction design, progressive disclosure, and narrow revisions extend existing guidance; they are not claims that those principles were entirely absent.

### Application of the supplied documentation

| Local source | Apply to the enhancement | Exclude from universal builder requirements |
| --- | --- | --- |
| [model-guidance.md](../codex/model-guidance.md) | Follow-through, focused questions, clear communication, and proportionate workflow instructions. | Hardcoded model selection, API settings, automatic delegation, or model-specific runtime configuration. |
| [prompt-engineering.md](../codex/prompt-engineering.md) | Explicit task contracts, useful examples, relevant context, and clear separation of instructions from supplied material. | Mandatory API integrations, prompt-service migrations, fixed layouts, or exhaustive planning rituals. |
| [prompt-generation.md](../codex/prompt-generation.md) | Creation from a task description, preservation of user content, and focused editing of existing instructions. | Forced disclosure of internal reasoning, mandatory conclusion ordering, claims that constants are immune to injection, or universal schema transformations. |
| [citation-formatting.md](../codex/citation-formatting.md) | For citation-producing skills, specify available sources, supported citation syntax, placement, and missing-support behavior. | A mandatory citation subsystem, fabricated source IDs, or citation parsers added to unrelated skills. |

These documents inform authoring decisions. Their examples do not override the current user request, supported host behavior, or the selected skill's actual output contract. They are local documentation snapshots; this specification makes no claim that every API or model statement in them has been refreshed against current online documentation.

## 3. Authoring lifecycle and public interfaces

### Execution flow

1. Resolve the project, requested operation, skill identity, and development destination.
2. Capture supplied inputs and existing package bytes where applicable.
3. Record the authoring contract, distinguishing user requirements from inferred defaults.
4. Stage the new package or focused edit. Use initializer and metadata helpers only where applicable.
5. Apply authorized changes with ownership, conflict, and filesystem safeguards.
6. Read back delivered bytes and publish an authoring record.
7. Return the package and a ready-to-use skill-validator request. Stop without executing validation or tests.

For existing managed packages, retain the baseline/current/candidate comparison. For a first edit without history, use the captured current package as an explicitly **observed edit base**, not as fabricated successful generated provenance.

Only paths justified by the requested work become managed. Capturing a file does not itself grant management or modification authority. A first edit without history does not bypass contradictory known history or erase an existing valid baseline.

### Authoring records

Introduce a distinct versioned authoring-record family rather than changing the meaning of existing successful-build records.

The record must contain:

- Project, selected destination, skill identity, operation, and run identity.
- Input/specification references and actual authorization.
- Prior origin: observed, adopted, legacy generated, or authored.
- Managed paths, retained user paths, before/candidate/delivered manifests, and actual applied changes.
- Authoring state: `AUTHORED`, `PARTIAL`, or `BLOCKED`.
- Validation and testing status at authoring time: `NOT_PERFORMED`, unless an explicitly referenced external result applies to those exact bytes.
- Any unresolved authoring prerequisite or conflict.

A completed authoring record may establish the next **authoring baseline** after successful write/readback. Validation is not required to establish that baseline.

Validation results remain separate records bound to an exact package digest. Editing a previously tested package must not carry its old result forward as the current package's result. Preserve old results as history without relabeling them or rewriting the original authoring record.

Explicit adoption remains a distinct custody operation. A captured observed edit base does not imply that explicit adoption occurred; authoring records must preserve that distinction.

### Builder-to-validator handoff

Add `validation-request.json` and a concise human-readable invocation request. The machine request must identify:

- Request schema/version and originating authoring run.
- Project root, actual target root, and skill identity.
- Target manifest reference and package digest.
- Authoring record and applicable specification references.
- Changed paths and known unresolved issues.
- Relevant capabilities, expected outputs, and declared side effects for assessment planning.

The request proposes assessment; it does not fabricate permission for network access, credentials, installation, or external writes.

Validator must accept this packet when the user later invokes it, independently re-read the target, and reject stale byte bindings. It creates its own assessment rules, fixtures, expected outcomes, test cases, execution records, and reports.

Builder does not automatically consume the validator report, repair findings, or start another validation cycle. A later authorized edit may reference that report as an input.

### Safeguards retained in builder

Removing quality checks does not remove ordinary write safeguards. Builder retains:

- Path resolution, link/junction exclusions, and selected write boundaries.
- Input parsing needed to interpret authoring records safely.
- File inventories, hashing, ownership accounting, and source-drift detection.
- Conflict detection, per-path write rechecks, and delivery readback.
- Retention of partial operations and failed publication attempts.

These establish what was requested and written. They do not assess skill quality or execute the authored skill.

## 4. Validation ownership and compatibility migration

### Transfer to skill-validator

Move responsibility for all quality assessment and testing to validator, including:

- Installed Skill Creator structural checking.
- Package links and instruction-quality assessment.
- Standards applicability and source interpretation.
- Deterministic evaluation profiles and grading.
- Generated-script execution and positive/negative behavior cases.
- Cold workflow trials, routing classification, and applicable enhancement campaigns.
- Assessment reductions, findings, and revalidation.

Builder may author executable helpers required by the generated skill, but it must not execute them as tests or generate an evaluation campaign during authoring. Requirement examples and expected behavior descriptions remain legitimate authoring inputs; executable test suites belong to validator.

### Package changes

- Update the development builder package's entrypoint, references, reporting templates, and helper interfaces together.
- Bundle adapted initializer and metadata-authoring helpers so installed builder copies do not depend on this machine's personal skill-creator path. Preserve applicable source notices when adapting helper code.
- Separate custody/planning utilities from grader code. The current evidence helper imports `graders`; remove that coupling before removing evaluator ownership.
- Relocate evaluator implementations, quality profiles, fixtures, and regression-test ownership to the development validator package.
- Retain builder's necessary authoring schemas and package-identity data.
- Update validator to understand the new authoring records and handoff while retaining its standalone assessment operation.

### Historical compatibility

- Preserve all existing evidence, snapshots, failed attempts, and adopted/generated provenance bytes.
- Keep legacy schema-1 and schema-2 meanings intact. Their historical `COMPLETE` states must not be reinterpreted as authoring-only completion.
- Add explicit readers for the new authoring record family and authoring baselines.
- Permit a new authoring run to reference a verified legacy origin without rewriting it.
- Replace fixed development-directory assumptions in active helpers with the selected destination recorded by the current request. Historical absolute paths remain historical identity data.
- Preserve existing import/adoption/regeneration behavior and rejection cases under validator-owned assessment, rather than deleting those expectations during relocation.
- Builder must remain usable for authoring when validator is unavailable. Report validation/testing as unperformed and return the handoff without installing anything.

Implementation changes apply to development packages only. Operational copies, installed caches, personal skills, historical evidence, and the supplied documentation remain unchanged.

## 5. Acceptance scenarios - executed by skill-validator

The implementation is assessed through validator-owned tests and behavioral trials. No tests are executed as part of preparing this specification.

| Case | Requirements | Required observation |
| --- | --- | --- |
| AC-01: Conversational creation | AB-001, AB-010 | A clear natural-language request produces an authoring contract and package without demanding a pre-existing approved specification. |
| AC-02: Material ambiguity | AB-002 | Missing consequential behavior prompts a focused question; routine discoverable facts do not. |
| AC-03: Portable location | AB-003 | Execution in another project asks for a location, recommends that project's source path, and honors a different selected development directory, including paths with spaces. |
| AC-04: Occupied destination | AB-006, AB-009 | Initialization refuses to overwrite an existing directory or silently rename the skill. |
| AC-05: Existing skill without history | AB-004, AB-005, AB-013 | Requested edits proceed after capture, preserve unrelated bytes, and record observed origin without fabricated legacy provenance or whole-package adoption. |
| AC-06: Untested revisions | AB-004, AB-014 | A second authorized edit succeeds from the authoring baseline while validation/testing remain explicitly unperformed. |
| AC-07: Ownership and drift | AB-005, AB-013, AB-014 | Divergent managed edits, unowned collisions, source changes, and interrupted writes preserve the appropriate conflict or partial evidence. |
| AC-08: Metadata editing | AB-008, AB-009 | Requested UI changes preserve unrelated fields and invocation policy; explicit-only behavior changes only when requested. |
| AC-09: Resource and instruction authoring | AB-007, AB-010, AB-011, AB-012 | Small skills remain small; conditional detail is routed appropriately; generated resources serve declared requirements. |
| AC-10: Authoring-only execution | AB-014; section 4 | Tool traces show no structural checker, grader, test suite, sample-task execution, or automatic validator invocation from builder. |
| AC-11: Manual handoff | AB-014; section 3 | Builder returns an exact target-bound request. Validator later performs both validation and testing and detects a stale request if the package changed. |
| AC-12: Historical compatibility | Section 4 | Existing evidence retains its bytes and meaning; new authoring records are distinguishable from legacy validated-build records. |
| AC-13: Missing validator | AB-014; section 4 | Authoring completes where its own prerequisites are available, with an explicit unperformed quality status and usable handoff. |
| AC-14: Assessment limitations | AB-014; section 4 | Structural success, schema fixtures, routing classification, native activation, and actual generated-skill behavior remain separately reported. |

These are acceptance requirements for a later implementation, not claims that the enhanced behavior has already been built or tested. Specifying test cases here does not assign their execution to skill-builder.

## 6. Source register and delivery boundary

Source identities below were rehashed on 2026-09-12 when this specification was saved. Absolute source locations identify inspected material only; they are not runtime paths to embed in the portable builder.

| Source | SHA-256 |
| --- | --- |
| [docs/codex/citation-formatting.md](../codex/citation-formatting.md) | `7a7c6bd2982e1c41287738ebb52b776f5159af7e45a187a3fb30ec7acb6b97be` |
| [docs/codex/model-guidance.md](../codex/model-guidance.md) | `d0514c9b721b9e608130ee6822b98d3b449aea7426406faa5b5db7db5f3c1220` |
| [docs/codex/prompt-engineering.md](../codex/prompt-engineering.md) | `92cb6fdb973f791d891c21ada93774cf436a87afa6919a60df2e14ee23a3f0de` |
| [docs/codex/prompt-generation.md](../codex/prompt-generation.md) | `9abfaf6866eb12e6913e5ec632bbe0e2f90764b61b2e020f3742d33390c4a8a4` |
| [Development skill-builder entrypoint](../../src/agents/skills/skill-builder/SKILL.md) | `96881f3ad173c4d46f2e486b8ee1b14fa1e00eab9a8c03ebcf93813c8270ada7` |
| [Development skill-validator entrypoint](../../src/agents/skills/skill-validator/SKILL.md) | `a4aad44434bacbe522cd1fe635db0a6b043ccb126e408c06999f8453fb23ed0c` |
| `C:/Users/bryan/.codex/skills/.system/skill-creator/SKILL.md` | `cccd291077ec57c6f50ca6529f0f3fb93212da09473effb2fcec808e81b21288` |

Supporting interface references are the current builder's [specification-build contract](../../src/agents/skills/skill-builder/references/spec-build.md), [adoption workflow](../../src/agents/skills/skill-builder/references/adoption.md), [regeneration workflow](../../src/agents/skills/skill-builder/references/regeneration.md), and the validator's [handoff contract](../../src/agents/skills/skill-validator/references/handoff.md). Those describe the pre-enhancement behavior that section 4 must migrate; this document does not claim they already implement the new ownership split.

Delivery of this document fulfills the specification-writing task. It changes no skill package, installs no skill or dependency, runs no skill validation/testing campaign, and implements no enforcement mechanism. The subsequent implementation must preserve the confirmed design decisions and use validator-owned assessment for both testing and validation.
