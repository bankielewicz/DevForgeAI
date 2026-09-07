# Validator-to-builder handoff

Use this guide when a user or assigned validator supplies findings for an existing skill. This builder edits the selected canonical source; the validator evaluates the resulting candidate. Neither role silently takes over the other's responsibility.

## Expected handoff artifacts

The paired validator supplies immutable records or references to retained exact bytes:

- **verification-results.md:** a `devforge.artifact/v1` envelope with artifact_type `skill-evaluation-report` and a SEVAL identity, including actual outcomes and limits.
- **skill-enhancement-spec.md:** a `devforge.artifact/v1` envelope with local paired-utility artifact_type `skill-enhancement-spec` and a SENH identity. This is not a registered companion CLI schema.
- **handoff.md:** a `devforge.artifact/v1` envelope tying the report, enhancement specification, candidate, accepted design specification, and requested authoring scope together.
- Retained source manifest: complete package-relative file-to-SHA-256 mapping for the selected target, with baseline and installed identities where applicable. Preserve plan, cases, rubric, previous-iteration and selected contract/template path/hash references. A manifest or receipt never contains its own self digest.

Read [results-contract.md](results-contract.md) for the shared record fields when supplied in this package. Use the selected contract's actual schema; do not invent missing IDs or claim that a generic envelope is automatically accepted by the CLI.

If a report uses another format, retain it unchanged and map the needed facts into the working specification. Missing material evidence stays a documented intake gap.

## Recover the frozen baseline

Before any dependent target edit, recover:

1. The assignment/provider, durable canonical source and generated-copy mapping.
2. The retained target manifest and exact accepted specification path/revision/SHA-256.
3. The source contracts/templates and their selected identities.
4. Report/handoff/enhancement-spec identities and immutable evidence locators.
5. Stable finding IDs `F-###`, change IDs `CHG-###`, affected requirement/workflow IDs, and the expected behavior.
6. Existing authoring decisions, Optional/Enforced classifications and named group answers.

Read the relevant original evidence and target source. Do not execute tests, cases, helpers, compilation, target workflows, or a validator to reproduce a finding.

Compare current target bytes to the frozen manifest as authoring collision/provenance handling. If they differ, record the changed paths and whether they affect the requested repair. Reconcile the current candidate, ownership and specification before applying affected findings. Preserve both prior and current identities; do not rewrite historical results.

## Interpret findings without expanding scope

Preserve severity exactly as supplied: BLOCKER, MAJOR, MINOR, or ADVISORY. A severity label is not automatic permission to alter the specification, change a gate, or run an evaluation.

Classify each requested change as:

| Change type | Builder action |
|---|---|
| Required repair | Apply the bounded authorized correction against the accepted requirement and source evidence. |
| Authorized enhancement | Apply the accepted added behavior while preserving other requirements. |
| Unapproved proposal | Keep proposed; ask only about the material new scope decision. |
| Bounded investigation | Inspect supplied source/evidence within scope; report conclusions and remaining uncertainty without running validation. |

Missing native discovery, loading, output-quality, or installed-resource observations create **evaluation prerequisites**. They do not alone justify editing the skill. Never weaken an accepted expectation, remove a case, or modify a sibling gate to turn a recorded failure into a pass.

A contract defect belongs to its integration owner. Record the blocked change and evidence; continue independent assigned edits.

## Preserve settled Q&A and enforcement choices

Reuse the accepted specification and prior interview. Ask only when an unapproved proposal, substantive conflict, or genuinely new requirement changes the design. Existing named group classifications persist. For new unclassified workflows/phases/tasks, ask Optional or Enforced and record the answer before finalizing the affected design.

Hook changes remain proposals in the specification. Do not install, activate, execute or validate them. An enforcement request and a documented hook design remain distinct from actual enforced behavior.

## Author a new candidate

Map each accepted CHG entry to its F entries and requirement IDs, then make focused canonical-source edits. Preserve unrelated behavior, resources, identities and invocation policy. Keep prior target bytes/reports available and identify the new candidate separately.

Update the working specification only for authorized clarification or enhancement. Preserve the former accepted specification identity; changed spec bytes require a new revision/identity. Do not silently reinterpret frozen requirements.

Do not edit installed copies as the source. Return source changes for the integration owner to regenerate the appropriate installation/export. Source file presence or hashing cannot establish activation or quality.

## Builder change receipt

Include the receipt in the populated specification or an assigned standalone artifact location. Record:

- Receipt identity/date, authoring scope/provider and actual owner/assignment reference.
- Input handoff/report/enhancement-spec identities and path/SHA-256 references.
- Frozen target/specification/contract identities and any drift reconciliation.
- Per-change mapping:

| F IDs | CHG ID | Change type | Requirement IDs preserved/changed | Disposition | Old path and SHA-256 | New path and SHA-256 | Edit summary or reason |
|---|---|---|---|---|---|---|---|
| [F-###] | [CHG-###] | [Selected type] | [IDs] | [applied / deferred / declined] | [Identity; absent for new file] | [Identity; absent for removed file] | [Bounded result/reason] |

- Complete new source manifest with package-relative paths and SHA-256 values; separate path/hash reference to the manifest, without a self digest.
- New or unchanged specification identity and preserved requirement IDs.
- Canonical-to-installed mapping, derivation/contract gaps and installation work remaining.
- Evaluation prerequisites, deferred proposals and unresolved evidence.
- **Validation status: Not performed.**
- **Hook status: Design only** when applicable.
- **Finding status: Source changes recorded; reevaluation required.**

Use actual observed identities. If required bytes or identity values are unavailable, record null/unknown with the reason and impacted work; do not fabricate hashes. "Applied" means edited source, not validated remediation. The validator must evaluate the new frozen candidate separately; prior passing observations do not transfer automatically to changed bytes.
