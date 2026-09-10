# Receiving an evaluator's findings

Use this when a user or an assigned evaluator supplies findings about an existing candidate. You edit the selected canonical source. The evaluator evaluates the result. Neither role quietly takes over the other's half, and neither is completed by the other's output existing.

## What the handoff should contain

An evaluator's transfer supplies immutable records, or references to retained exact bytes:

- **An evaluation report.** A `devforge.artifact/v1` envelope with `artifact_type` `skill-evaluation-report` and a `SEVAL` identity, carrying the actual outcomes and their limits.
- **A bounded repair specification.** The authorised changes, tied to finding IDs.
- **A handoff.** A `devforge.artifact/v1` envelope tying the report, the repair specification, the candidate, the accepted design specification and the requested authoring scope together.
- **A retained source manifest.** A complete package-relative file-to-digest map for the target, with the baseline and installed identities where they apply. Plan, cases, rubric, previous iteration and the selected contract or template references are preserved alongside it.

Every locator is a path plus a digest covering complete exact bytes; optional kind, line, section and description fields explain what the reference is for. Relative paths in a record resolve from that record's own directory. Freeze a record before anything downstream hashes it. No record carries its own digest.

If a report arrives in another format, retain it unchanged and map the facts you need into the working specification. Material evidence that is absent stays a documented intake gap - do not invent an ID, a digest or a severity to fill a column.

The definitive shape of these paired records belongs to the Claude `devforge-evaluate-expert` package. Until that package is available in this environment, treat the fields above as the minimum a transfer must carry, and record any record shape you had to infer as an intake gap rather than as a settled contract.

## Recover the frozen baseline first

Before any dependent edit to the target, recover:

1. The assignment and provider, the durable canonical source, and the generated-copy mapping.
2. The retained target manifest and the accepted specification's exact path, revision and digest.
3. The source contracts and templates at their selected identities.
4. The report, handoff and repair-specification identities and their evidence locators.
5. The stable finding IDs, change IDs, affected requirement or workflow IDs, and the expected behaviour for each.
6. The existing authoring decisions and the classification answers already given.

Read the relevant original evidence and the target source. Do not run tests, cases, helpers, compilation, the target skill, or an evaluator in order to reproduce a finding. Reproduction is the evaluator's job, and doing it here would make you the judge of your own repair.

Compare the current target bytes to the frozen manifest. If they differ, record which paths changed and whether the change affects the requested repair, then reconcile the candidate, its ownership and the specification before applying the affected findings. Preserve both the prior and the current identities. Do not rewrite historical results to match what is now on disk.

## Reading findings without expanding scope

Preserve severity exactly as supplied - `BLOCKER`, `MAJOR`, `MINOR`, `ADVISORY`. A severity is a description of impact. It is not permission to alter the specification, change a gate, or run an evaluation.

Classify each requested change:

| Change type | What you do |
| --- | --- |
| Required repair | Apply the bounded authorised correction against the accepted requirement and the source evidence. |
| Authorised enhancement | Apply the accepted added behaviour, preserving the other requirements. |
| Unapproved proposal | Leave it proposed. Ask only about the material new scope decision it raises. |
| Bounded investigation | Inspect the supplied source and evidence within scope; report the conclusion and what remains uncertain, without running validation. |

A missing observation is an **evaluation prerequisite**, not a defect. No discovery evidence, no loading evidence, no output-quality comparison, no installed-resource check, a run that could not complete - each of those means something was not observed. None of them on their own justifies editing the skill, and editing it will not produce the missing observation. Record the prerequisite and who owns it.

Never weaken an accepted expectation, delete a case, or change a sibling gate in order to turn a recorded failure into a pass. A defect in a shared contract belongs to its integration owner: record the blocked change with its evidence and continue the independent edits you were assigned.

## Preserve what was already settled

Reuse the accepted specification and the earlier interview. Ask only when an unapproved proposal, a substantive conflict, or a genuinely new requirement changes the design. Existing named group classifications persist. For a genuinely new unclassified item, record whether its completion is required before its dependent action, as in the [interview guide](interview-guide.md), before finalising the affected design.

An enforcement request and a recorded enforcement requirement are both still design. Neither installs, activates or demonstrates anything.

## Author a new candidate

Map each accepted change to its findings and requirement IDs, then make focused edits to the canonical source. Preserve unrelated behaviour, resources, identities and invocation policy. Keep the prior bytes and the prior reports available; the edited bytes are a new candidate with its own identity.

Update the working specification only for an authorised clarification or enhancement. Preserve the former specification identity - changed specification bytes need a new revision, not a silent rewrite of the accepted one.

Do not edit an installed copy as if it were the source. Source changes go back to the integration owner, who regenerates the installation or export. A file existing, or hashing correctly, establishes neither activation nor quality.

## The change record

Put the substantive change content in the populated specification or an assigned standalone location. It is an authoring record - not a completion receipt, not a validation result. Never ask for the containing document's own digest.

Record:

- The receipt identity and date, the authoring scope and provider, and the actual assignment reference.
- The input handoff, report and repair-specification identities with their paths and digests.
- The frozen target, specification and contract identities, and any drift you reconciled.
- A per-change mapping: finding IDs, change ID, change type, requirement IDs preserved or changed, disposition (applied, deferred, declined), old path and digest, new path and digest, and a bounded summary or reason.
- The complete new source manifest as package-relative paths and digests, referenced separately by path and digest, with no self-digest.
- The resulting specification ID, revision and path, and the preserved requirement IDs.
- The canonical-to-installed mapping, any derivation or contract gaps, and the installation work still outstanding.
- Evaluation prerequisites, deferred proposals and unresolved evidence.
- **Validation status: Not performed.**
- **Enforcement status: requirements recorded; no gate implemented by this skill.**
- **Finding status: source changes recorded; reevaluation required.**

Use identities you actually observed. Where required bytes or values are unavailable, record `unknown` or `null` with the reason and the work it affects; do not fabricate a digest. "Applied" means the source was edited. It does not mean the finding is closed - the evaluator has to evaluate the new frozen candidate, and prior passing observations do not transfer to changed bytes.

Finish with a prepared [handoff](../assets/handoff.md) naming the actual next owner. Preparing it neither invokes the receiver nor authorises a transition.
