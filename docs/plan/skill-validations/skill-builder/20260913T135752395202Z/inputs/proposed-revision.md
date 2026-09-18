---
id: REV-VALIDATOR-BUILDER-COMPAT-20260913T135752395202Z
skill_name: skill-validator
target: codex
status: proposed
---

# Proposed validator compatibility revision

This is a reviewable proposal, not authorization to edit or install. Target development package: `C:\Projects\DevForgeAI\src\agents\skills\skill-validator`. Its observed digest equals the loaded validator: `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1`. Builder compatibility target is `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2`.

Preserve the complete existing validator contract in the captured `inputs/skill-validator-adaptive-enhancement-spec.md` (SHA-256 `f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42`) and its linked builder interface specification (SHA-256 `8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59`). The following mandatory corrections resolve observed implementation disagreement; they do not introduce new schema versions or alter those specifications.

## Purpose, activation and exclusions

Continue standalone ordinary/adaptive skill validation, manual authoring-request intake, explicit full-set/subset intake, bounded semantic and behavioral assessment, origin reconstruction only on actual absence, and proposed revision handoff. Existing descriptions and automatic invocation remain. Installation, repairs during validation, inferred installed sets, production effects, automatic builder invocation and Rust enforcement remain excluded.

## Inputs, outputs and interfaces

Preserve all 14 shared schema documents and their meanings, existing authoring-v1 and schema-1 record conventions, and validator-specific supplemental schemas. New external references stay canonical absolute paths; schema-1 evidence stays run-relative. Missing/stale/ambiguous inputs retain specific observations and independent assessment scope. Preserve current CLI commands: observe snapshot/structure/readback/records, authoring_intake, and adaptive_observe package/intake-set/records. No arbitrary dispatcher, remote schema loader or builder executable dependency is added.

Keep the current origin/source/rule/check/finding/report/workflow/handoff artifacts. Helpers remain read-only except the explicitly documented snapshot. Raw observations retain helper identity; semantic results are separate run-bound records. Required FAIL precedes INCOMPLETE and PASS; subset results never imply full-set coverage.

## Mandatory behavior corrections

| ID | Required future behavior | Resources and acceptance |
| --- | --- | --- |
| VC-001 | Restrict review_updates to explicitly selected existing variants. Compare retained prior/current parent package identity, relevant project inputs and requirement statements. With changed relevant bytes and equivalent semantics, accept PROPOSED and reject NO_CHANGE. Without sufficient history, do not establish NO_CHANGE. Ordinary propose reduction remains unchanged. | scripts/adaptive_contracts.py; focused tests for changed-equivalent-proposed, changed-false-no-change, review-nonvariant, unchanged history and missing prior. |
| VC-002 | Resolve a bounded, unambiguous explicit parent requirement inventory from captured parent Markdown, including ordinary cores with an ID/Requirement table in SKILL.md and Requirement/Required behavior tables. Do not require references/adaptive-contract.md merely to inspect an older core. Preserve no-follow/aggregate capture limits; ambiguous inventories remain gaps. | scripts/adaptive_contracts.py; ordinary-parent positive and ambiguous/missing inventory negatives. |
| VC-003 | Accept equivalent LF and CRLF fenced devforgeai-requirements inventories without altering source bytes. Continue rejecting malformed, duplicate or empty inventories. | Parent index parser; LF/CRLF paired fixtures and raw-byte preservation. |
| VC-004 | For every delivered adaptive member, bind descriptor role to the selected proposal. For variants, bind exact parent name, digest and complete requirement-ID set to selected lineage. Keep independent descriptor validity checks. Reject wrong role or parent even when the package and descriptor are otherwise self-consistent. Preserve valid retained ordinary members. | set_authoring/intake; valid full-set, wrong-delivered-role and wrong-parent negatives plus eligible_subset regression. |
| VC-005 | Require every descriptor parent requirement ID to resolve in the linked contract's disposition map. At minimum reject a missing ID deterministically; semantic review still establishes retained/modified/removed meaning and authorized changes. Do not claim an ID occurrence proves consent or preservation. | descriptor reader and semantic route; missing-parent-disposition negative, complete map positive, unrelated textual mention semantic counterexample. |

## Workflow, capabilities and recovery

Keep current routed intake → origin → pinned rules → package/resource review → bounded trials → reduction/report → proposed handoff. Apply the corrected reader before dependent set assessment; invalid member inputs cannot supply trusted downstream handoffs. Continue independently scoped valid-member assessment only with explicit labeling. Preserve full membership and omissions, failed attempts, exact source readback, and report missing capabilities without installations. Python 3.10+/already available PyYAML and existing Codex CLI remain the supported local capabilities; GUI/MCP/plugins are not required.

No changes to source skills under assessment, real operational bindings, personal skills, operational copies, specifications, old evidence, hooks or CI. Development maintenance writes would be limited to the selected validator source and fresh evidence under a later explicit implementation request. Do not copy builder executable logic into validator; keep independent implementations and independent expected outcomes.

## Acceptance and delivery

Run the existing 229-test suite plus independent public-CLI differential fixtures retained in this run. All builder/validator responses must agree with the independently specified expected outcomes, not merely with each other. Both validators must accept the immutable existing real single-skill handoff and partial-set request used here. Preserve all extra-key/version/reference/reduction negatives. Run current installed structural checking, full text/resource observations with manual candidate adjudication, and exact source/specification readback.

In a fresh bounded cold validator task, provide an unlabelled wrong-role request and determine whether actual instruction-level review identifies the contract mismatch without repair. Preserve timeouts separately. Complete producer-to-consumer behavior and remaining prior builder cold cases remain distinct from successful intake. No package acceptance or installation claim follows from this revision.

No optional enhancements are proposed. Findings are proposed and not selected for implementation. A future maintenance request should assign `$skill-creator` to the validator edits and `$skill-validator` plus the independent harness to assessment, naming this exact proposal and selected digest. Known provenance must be rechecked then; this observed snapshot is not fabricated adoption. This validation task stops with evidence and this proposal.
