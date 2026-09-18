---
id: OPERATIONAL-BUILDER-REVISION-20260913-001
skill_name: skill-builder
target: codex
status: proposed
---

# Complete proposed builder contract

This proposal applies only to the observed builder development package selected by this assessment. It is reviewable remediation, not permission to write or install. The supplied enhancement specification remains the complete approved two-package design; this contract restates the selected builder responsibilities and proposes three fixes without enlarging its scope.

## Purpose, activation and exclusions

Author one Codex development skill from conversational requirements, a selected Markdown specification, a Claude source package or a requested edit. Support explicit custody adoption separately. A clear current request authorizes proportionate creation/editing; preserve user-selected review boundaries. Do not trigger for standalone testing, validation, installation or standalone specification writing. Never invoke validator automatically or repair its findings without a later request.

## Inputs and defaults

Resolve the selected project, exact identity, operation and destination. Ask once for missing destination and show the resolved project/src/agents/skills parent recommendation and final skill directory; an already supplied location answers that question. Accept another development directory including paths with spaces. Discover routine facts and ask only consequential missing decisions. Existing valid identities are preserved, including names of exactly 64 characters. New identities use 1-64 lowercase letters/digits with single separating hyphens; resolve collisions explicitly.

Capture raw requirements, references and actual authorization before staging. Use authoring-contract-v1 with project_root, target_root, target_name, operation, run_id, authorization, history_review, change_paths, requirements, capabilities, expected_outputs, side_effects, inputs and known_issues; retain prior/legacy_root/retry_of where applicable. Require field types and reference shapes from the bundled contract schema before mutation, including known_issues as an array of strings. JSON rejects duplicate keys and nonfinite values. These checks interpret write-custody data, not authored-skill quality. Known contradictory or missing history is unresolved, not absence.

## Outputs and schemas

Produce contract and input captures, before/candidate/delivered manifests, B/C/N write plan, actual applied paths, managed and retained ownership, and an authoring-v1 record. Successful authoring uses AUTHORED; incomplete operations use PARTIAL or BLOCKED according to actual applied effects. Keep validation/testing NOT_PERFORMED unless an explicit separate result binds the exact delivered bytes. Publish authoring-baseline-v1 only after successful delivery and publication readback. Old schema-1/schema-2 COMPLETE records keep historical meanings and original bytes.

Return validation-request-v1 containing schema/record kind, originating run, project and actual target/name, target manifest/package digest, authoring record/specification references, changed paths, known issues, capabilities, outputs and side effects. Also return a human-readable validator invocation with exact request path/digest. This proposes assessment and grants no credentials, network, installation or external-write authority. Return destination, changes, history, unresolved issues and handoff to the user.

## Workflow and routing

1. Resolve operation, scope and development destination through SKILL.md and references/authoring.md. Selected specifications additionally use spec-build.md; Claude imports use conversion-rules.md; existing packages use regeneration.md; explicit adoption uses adoption.md.
2. Record the contract and verify all input shapes, safe roots and selected history before target writes. Begin a fresh run under the selected project docs/plan, disjoint from target and input roots. Capture exact bytes and observed history when no known baseline exists. Observation does not adopt or manage unrelated paths.
3. Stage changes in candidate. Use bundled initializer only for a fresh staging destination and refuse occupied locations. Use bundled UI helper or focused edits, preserving unrelated interface/policy/dependency fields. Resource directories, examples, scripts, references and assets serve concrete requirements; remove unused scaffold placeholders. Do not create automatic README/changelog/install/test trees.
4. Write clear purpose, activation, inputs/outputs, dependencies, effects, recovery and constraints. Keep essential routing in SKILL.md; put substantial conditional detail in references. Preserve useful existing structure, identities, supported metadata and output/domain contracts. Import decisions depend on supported target format, never on a checker restriction. Preserve supported compatibility metadata. Do not execute a checker, grader, generated helper, sample task, campaign or validator during authoring.
5. Resolve B/C/N for selected managed paths. Reject unowned collisions and divergent managed changes. Preserve unrelated current bytes. Recheck source inputs and captured target before first write and each changed path before mutation. Read back actual delivery and retain real applied deltas.
6. Retain all interrupted attempts and record-construction/publication failures. A malformed pre-write input blocks without target mutation. Any failure after applied writes produces durable PARTIAL evidence with actual paths and after observation; never label a changed target merely BLOCKED or claim rollback. Do not advance a failed baseline. Recovery requires a fresh linked run and the last verified successful baseline.
7. Publish successful authoring record, baseline, manual request and publication readback; return them and stop. Further authorized editing may use the untested authoring baseline. Explicit adoption remains custody-only and records adopted origin for later edits. Validator absence does not stop otherwise complete authoring.

## Dependencies and side effects

Use Python 3.10+ for bundled custody/scaffolding; PyYAML is needed by specification lookup and metadata parsing. No personal skill-creator path dependency or dependency installation is introduced. Missing helper dependencies permit ordinary authoring tools where custody can still be honored; otherwise retain a concrete blocker. Operational .agents/.claude/.codex, installed/personal skills, hooks, CI, external systems and Rust implementation are excluded. Reject traversal, links/junctions and special files; apply the existing bounded 2000-file/32-MiB capture ceiling with disclosed exclusions. These are ordinary safeguards, not OS-enforced isolation or framework authority.

## Required fixes and acceptance

R-01 (mandatory): validate the contract before mutation and retain honest post-write failure evidence. A fixture with known_issues:null must be rejected before creating/changing target bytes; wrong types in other used fields must also fail safely. Inject a record/publication failure after a real applied path: preserve PARTIAL, exact applied paths/readback, and no usable new baseline. Retest ordinary creation, observed editing, conflict/drift and adoption.

R-02 (mandatory): preserve valid 64-character identity through begin/publish and align routed naming guidance. Editing a 64-character existing identity succeeds without rename; 63 and 64 are permitted, 65 remains rejected. Initializer and authoring must agree.

R-03 (mandatory): remove checker-gated metadata preservation from import instructions. An import with supported compatibility metadata preserves that field and its meaning without invoking a structural checker. Unsupported actual host fields require an explicit compatibility decision, not fabricated universal rules.

Retain all original AB-001 through AB-014 and applicable section 3-4 responsibilities. Validator owns execution of these quality and behavioral acceptance cases. Native activation, cold independent workflow execution, structural checks and helper cases are reported separately. The companion validator implementation is not part of this proposed builder patch.

## File mapping, preservation and decisions

scripts/authoring.py and schemas/authoring-contract.schema.json implement R-01/R-02 custody interpretation; preserve existing record versions. references/conversion-rules.md implements R-02/R-03 naming/metadata guidance. Update any directly inconsistent authoring/evidence/scaffolding references and package identity manifest only as required by these fixes. Preserve unrelated package files, licenses, metadata/domain contracts and every historical evidence byte. Test ownership remains with validator. No optional enhancements are selected.

Review must select these finding corrections and authorize the exact development target and managed paths. No verified target authoring/generated/adopted baseline was supplied to this isolated assessment. The loaded operational validator's handoff requires a verified baseline or explicitly authorized supported adoption before builder-ready execution; therefore readiness is BLOCKED while the proposal remains pending review. Do not silently invent history. A later explicit observed-edit request under an enhanced builder is a separate authorization/workflow decision.

Observed package digest: `df5204eb3ff53db0ff71d222bfab552170ca36950905ad9b49ea3fcbc9b6bb32`. Origin/specification: `inputs/enhancement-spec.md`, SHA-256 `43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14`.

Finding bindings: `F-f0530cf3fcd3c232b753ab5684fa985f2f106828295172e93a8d70ec1fb21224`, `F-e937af0918a0b6660b11c9f49d60032ecf560ead6da77080256499cbb7935402`, `F-65f77a3bc98cfc63f162cd1cbc0ca313ae81fb531b6e5754e0cb86e6ceb70a72`.
