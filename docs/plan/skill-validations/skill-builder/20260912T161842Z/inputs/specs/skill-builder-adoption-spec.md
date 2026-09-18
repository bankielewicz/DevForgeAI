---
id: CODEX-SKILL-BUILDER-ADOPTION-SPEC-001
target: codex
status: approved
specification_version: "1.0"
recorded: "2026-09-12"
---

# Specification: Adopt Existing Codex Skills into Builder Provenance

## 1. Purpose and implementation boundary

Extend the development source `src/agents/skills/skill-builder/` with explicit adoption of an existing Codex skill that has no successful builder baseline. This enables a later authorized specification-based revision using the [skill-validator handoff](skill-validator-spec.md).

The current builder requires the last successful generated baseline for regeneration and correctly refuses to manufacture one from current files. This extension adds a separately typed observed adoption origin; it does not relax or reinterpret historical generated-baseline evidence.

This document was authorized as a companion design in the planning session. Saving it implements the specification-delivery plan only. A subsequent explicit implementation request is required to modify the builder. No operational `.agents`, `.claude`, `.codex`, personal skill, Git hook, CI configuration, or framework runtime is modified by this document task.

Implementation is an enhancement of the existing builder, not generation of a new skill named adoption. Use the current development source and repository instructions; do not feed this document to an unchanged builder as if it already implements adoption. The document intentionally has no `skill_name` lookup field, avoiding collision with ordinary skill build specifications.

## 2. Fixed decisions and requirement register

Adoption means: the user identifies an existing package and authorizes management of an explicit set of its paths; the builder records the observed starting bytes and their ownership boundary. It establishes neither historical authorship nor correctness. Existing defects may remain at adoption time.

| ID | Required behavior | Verification |
| --- | --- | --- |
| AD-001 | Select adoption only through explicit user direction, distinct from validation and revision. | Routing and unauthorized-write negative cases. |
| AD-002 | Record exact observed bytes, target identity, ownership selection, and unknown history honestly. | Snapshot/digest and false-history rejection cases. |
| AD-003 | Preserve all target files during adoption and unrelated files during later revision. | Before/after manifests and unowned-collision cases. |
| AD-004 | Introduce a typed adoption origin without forging schema-1 successful provenance. | Parser/schema negative cases and legacy regression suite. |
| AD-005 | Apply the existing three-way conflict semantics against the verified adopted origin. | Full comparison-table fixtures. |
| AD-006 | Retain failures and publish a generated baseline only after successful revision checks/readback. | Conflict, partial-application, and failed-readback trials. |
| AD-007 | Accept validator handoff as an input packet, not authority or build provenance. | Digest/identity/selection checks. |
| AD-008 | Extend machine evaluation and meaningful forward trials for the new behavior. | New profiles, graders, and actual disposable task trials. |
| AD-009 | Keep development evidence separate from compiled-Rust enforcement and installation. | Instruction review and no-runtime trial. |

## 3. Operations, inputs, and authorization

Support a new explicit operation `adopt`, followed by the existing specification-build operation with an adoption-origin revision path. V1 adopts Codex packages only. It does not add Claude adoption, combined provider output, installation, automatic repair, or batch adoption.

Example adoption request:

```text
Use $skill-builder to adopt the existing Codex skill at the selected development
path using the reviewed origin specification and the explicit managed-path list.
Preserve the target bytes. Record its history as unknown before this adoption.
```

Inputs are the project root, exact target directory, reviewed origin specification, selected managed paths, current user authorization, and optional validator report/handoff. If the package name is invalid or differs from the intended identity, record that defect and the user's selected future identity in the revision specification; do not silently rename the current directory during adoption.

The managed-path list is explicit and digest-bound. The builder may prepare a proposed list from the origin specification and resource inventory, but cannot mark files managed based solely on their presence. User direction can approve the entire concrete proposed list without approving paths individually. Files excluded from management remain user-owned even when their bytes equal a newly generated candidate file.

Adoption requires authorization for the observed target identity and managed-path manifest. Revision separately requires authorization for the proposed behavior, destination, and managed changes. One user instruction may explicitly authorize both, but the records remain distinct. A validator request, report verdict, proposed specification, or `status: approved` label supplies neither authorization automatically.

Preserve session authorization when it already covers the exact operation and bytes. Ask only for missing material decisions, such as an unresolved ownership list or a changed proposal. Do not add a repeated approval step to already-authorized work. The validator's selected review-before-repair policy remains binding for its handoffs.

Adopt development targets only under `src/agents/skills/<name>/` for this extension. A skill located in an operational directory may be inspected by the validator, but adopting it requires an explicitly authorized ordinary copy into the development target, with copy readback and identity recorded before adoption. No operational directory becomes a writable builder destination.

If a valid successful baseline already governs the target, use normal regeneration. If existing history is missing, malformed, contradictory, or points to different bytes, report that condition; do not silently use adoption to erase it. Adoption after known failed history requires explicit acknowledgement and preservation of that history. A failed attempt to revise a valid baseline retains that baseline and cannot be bypassed through re-adoption.

## 4. Adoption workflow

| Stage | Required work | Completion / failure behavior |
| --- | --- | --- |
| Intake | Resolve target/project, origin specification, current authorization, candidate managed-path list, and prior evidence. | Reject conflicting identity, inadequate authorization, operational targets, or unresolved ownership before target-affecting work. |
| Capture | Allocate `docs/plan/skill-adoptions/<name>/<run-id>/`; inventory target, snapshot all permitted files, and record managed versus retained paths. | Enforce existing traversal, links/junctions, exclusions, 2,000-file and 32-MiB limits. Preserve a partial capture if it fails; do not call it adopted. |
| Bind | Record original specification bytes/digest and authorization, snapshot manifest, managed subset, retained subset, known defects, and unknown historical origin. | Verify the subset partition and all bytes. Defects in the skill do not invalidate an accurately captured adoption. |
| Recheck | Re-read original target and specification and compare permitted file sets, sizes, and hashes with captured inputs. | Any drift produces `SOURCE_CHANGED` and no new active adoption pointer. |
| Verify | Execute the adoption evidence grader and read back its inputs and output. | Evidence errors prevent adoption publication; preserve failed attempts. |
| Publish | Write an external adoption pointer identifying the exact record and managed snapshot. | Recheck inputs immediately before publication, then read back the pointer. Report adoption recording separately from quality and future revision readiness. |

The target byte set stays unchanged throughout adoption. The adoption writer records only run evidence and its external pointer. Publication is an ordinary local file operation, not protected admission or package-wide atomicity. If pointer publication/readback fails, retain the record and mark publication incomplete; do not proceed with dependent revision.

Snapshot files are immutable by workflow convention, not filesystem enforcement. Rehash them on every use; refuse corruption. Keep adoption bytes permanently distinct from future generated baseline bytes.

## 5. Adoption record and pointer contracts

Use UTF-8 JSON, lowercase SHA-256 of raw bytes, normalized relative snapshot paths, duplicate-key and non-finite-value rejection, and the existing builder's boundary checks. Resolve references within the explicitly selected bounded evidence root; do not follow arbitrary paths from imported JSON.

`adoption-record.json` schema `1` contains these required fields:

| Field | Shape / meaning |
| --- | --- |
| `schema_version`, `record_kind` | `"1"`, `"adoption"`. |
| `run_id`, `target_name`, `target_root`, `project_root`, `captured_at_utc` | Actual identity and original resolved paths/time. |
| `historical_origin` | `"unknown"`; known prior evidence is linked separately rather than rewritten. |
| `snapshot_root`, `snapshot_manifest` | Bounded snapshot location and `{path, sha256}` reference to its complete permitted-file manifest. |
| `managed_paths`, `retained_user_paths` | Sorted, unique, disjoint relative paths whose union equals the observed snapshot file set. |
| `origin_spec` | `{path, sha256}` referencing a captured, reviewed specification; original resolved path is recorded in its input metadata. |
| `authorization` | `{instruction, target_root, managed_manifest_sha256, origin_spec_sha256}` with the actual user instruction. The managed manifest is stored separately and contains sorted path/size/hash rows. |
| `prior_evidence`, `quality_evidence` | Arrays of `{path, sha256}` references; empty only when none exists. Quality evidence may report defects or unperformed checks. |
| `source_readback` | Reference to a preceding observation containing before/after file rows and comparison outcome. |
| `recording_state` | `"ADOPTED"` after successful preliminary byte/partition checks and source readback; `"INCOMPLETE"` otherwise. ADOPTED describes recorded custody, not quality or final publication. The final evaluator checks these claims before pointer publication. |

The preceding source-readback observation is the evaluator input; the final evaluator result is stored outside its candidate root and linked from the adoption report. Do not embed a digest of that future result in its own input record. After evaluation, publish the separate pointer only on success. A standalone ADOPTED record without a verified published pointer cannot start revision. Freeze the evaluated record bytes; later final-evaluator failures are recorded in the report/publication state without rewriting the evaluated record to conceal the failed observation.

The external active pointer uses schema `2`:

```text
schema_version: "2"
run_id: actual recording run
target_name: selected identity
origin: {kind: "adopted", path: adoption-record.json, sha256: actual digest}
baseline: [{path: managed relative path, sha256: observed byte digest}]
```

After a successful generated revision, the pointer's origin kind becomes `generated` and references the actual successful provenance; baseline rows identify generated candidate bytes. Pointer files and their before/after snapshots stay outside the skill package. Store a new pointer in the owning evidence directory and retain previous pointer bytes; do not overwrite another run's history.

Never emit `result: COMPLETE`, `ownership: generated`, or a fake builder run for the adopted snapshot. Those terms remain reserved for their existing generated-build meanings. Snapshot completeness, adoption recording, skill quality, and revision authorization are separate fields/results.

## 6. Revision against an adoption origin

Let **A** be the managed adopted snapshot, **C** the current complete target, and **N** the new generated candidate. For the first revision, A supplies B in the existing three-way comparison, explicitly tagged `adopted`. A is read from verified adoption evidence; it is never reconstructed from C at retry time.

Use the same ordered conflict rules:

| Condition | Action |
| --- | --- |
| N proposes an occupied path not in the authorized managed set | CONFLICT, even if bytes match. |
| C equals B | USE_NEW, including removal when N omits an obsolete nonrequired managed path. |
| C equals N | KEEP_CURRENT. |
| N equals B | KEEP_CURRENT, preserving the user edit. |
| Otherwise | CONFLICT. |

Absence differs from empty content. A missing required candidate artifact conflicts. An unchanged obsolete managed file may be removed; a modified obsolete file conflicts. An unrelated C-only file stays `retained_user`. Proposed new files receive generated ownership only where absent in C and justified by the approved build contract. Ownership expansion over an occupied unowned file requires explicit resolution, never adoption by identical bytes.

Stage N and finish required checks before destination edits. Recheck the current target against captured C before the first write and each affected path immediately before its mutation. Stop on drift. On any later write failure, record actual changed paths and the after snapshot as PARTIAL; do not promise automatic rollback or advance a baseline. Retry from the same A or last successful generated B with newly captured C. Link the retained failed attempt.

After successful application, re-evaluate actual delivered bytes, run required checks, and read them back. Only then publish a generated-origin pointer with N's digests. Generated baseline and delivered bytes may differ when user edits were retained. Future revisions compare against the last successful N, not the historical adoption snapshot, while keeping the adoption link in provenance.

## 7. Versioned integration with existing builder evidence

Keep current contract schema `1` for normal input/requirement/artifact mappings and `mode: spec_build`. Keep existing provenance schema `1`, revision plans, profiles, and historical successful fixtures unchanged. Add explicit schema `2` support for adoption-origin specification revisions; do not reinterpret schema `1` records as adoption evidence.

### Schema 2 provenance

Use the existing provenance fields and output/mapping/evidence shapes, with these changes:

- `schema_version` is `"2"`.
- Replace `prior_build` with required `prior_origin: {kind: adopted|generated, path, sha256}`.
- Add required `adoption_origin: {path, sha256}` referencing the original adoption record.
- Outputs keep `ownership: generated|retained_user`; generated baseline rows identify N. This describes the new generation's baseline and managed output, not historical authorship of adopted or retained bytes.
- `result: COMPLETE` requires successful checks and delivered readback, as before. INCOMPLETE records cannot become generated origins.

For first revision, `prior_origin.kind` is adopted and its record must be ADOPTED with verified published pointer. For subsequent revisions on this lineage it is generated and must reference COMPLETE schema 2 provenance; the adoption_origin reference is retained. Verify target identity, managed/output sets, actual bytes, authorization, and evidence references. A schema 1 generated lineage continues on its existing path, without mandatory migration.

### Schema 2 revision plan

Keep current plan fields and semantics, except replace `prior_build` with `prior_origin` and add `adoption_origin`. B/C/N/after remain distinct bounded directories. For adoption-origin rows, use `ownership: adopted|generated|retained_user`: adopted names paths managed by A, generated names new generated paths; both use the managed three-way rules. After a successful generated origin, managed rows use generated. The difference is historical origin, not greater mutation authority.

`baseline_before` and `baseline_after` reference captured schema 2 pointers. The adopted before pointer must agree with A; a successfully advanced after pointer must agree with N and the new COMPLETE provenance. A conflict/planned/partial result cannot advance the active origin. Preserve existing `status`, `applied_paths`, `readback_passed`, `evaluation_passed`, `baseline_advanced`, and `retry_of` meanings. `retry_of` links must identify the same unchanged prior origin for a partial retry.

### New evidence interfaces

Extend `build_evidence.py` with `adoption-plan --snapshot-root <root> --request <request.json>` and schema-aware revision-plan support. The adoption-plan helper reads already captured snapshots and emits observed accounting/proposed adoption JSON to stdout; it does not publish pointers or edit targets. Its request includes identity, snapshot/spec references, managed paths, and authorization from section 5. Outputs account for every permitted file and reject missing, duplicate, unsafe, or unobserved managed paths. Preserve helper exit conventions: 0 valid observation, 1 evidence mismatch, 2 usage/access/execution error.

Register these additional profiles in the existing Python evaluator:

| Profile | Required graders | Meaning |
| --- | --- | --- |
| `adoption-v1` | `adoption_consistency` | Verify capture, managed/retained partition, authorization binding, readback, and absence of target mutation. Does not require the adopted skill to pass quality checks. |
| `revision-spec-v2` | `package_links`, `build_traceability_v2`, `revision_consistency_v2` | Verify schema 2 origin, generated provenance, requirement/output accounting, and actual three-way delta. |
| `routing-adoption-v1` | `routing_outcomes_v2` | Observe the existing routing classes plus `adoption` without changing the legacy routing grader's accepted values. |

Use grader params `{evidence: "evidence", destination: "destination"}` for adoption_consistency and build_traceability_v2, and `{path: "evidence/revision-plan.json"}` for revision_consistency_v2. Snapshot/evidence roots are bounded and disjoint as in existing interfaces. The adoption evidence directory contains the record, source readback, and referenced manifests/snapshots; destination is the after-observation target snapshot. Graders compare bytes, not model-written success flags. Implement shared validation without duplicating or weakening the legacy graders.

For routing_outcomes_v2, preserve params `{expected: "expected.jsonl", observed: "observed.jsonl"}` and existing row fields and bounds; add only `adoption` to the existing route values. Use independent observed classification, not copied expected answers. Continue exercising legacy routes in `builder-v2`; run `routing-adoption-v1` separately. A routing classification is not native activation evidence.

Keep the evaluator's current JSONL case shape, evidence schema `2`, profile binding, digest manifest, output boundary, and exit conventions. Add profiles/graders intentionally and rebuild the manifest only after source changes are reviewed. No case selects an arbitrary executable. Unknown schemas, profiles, and malformed pointers remain errors. Build-traceability v2 validates adoption metadata and the published-before pointer in addition to schema-1-equivalent requirement and output bindings; revision consistency v2 recomputes the managed delta and after-pointer rules.

## 8. Validator handoff behavior

The validator supplies observed origin, report, proposed revision specification, target snapshot/digest, findings, proposed managed boundaries, and review state. Verify all selected references and recheck the actual target. Treat `builder_readiness` as the validator's observation, not as authority or proof.

If adoption capability is absent, the validator still produces reviewable artifacts and marks adoption-dependent execution unavailable. If capability is present but authorization or a published adoption origin is absent, prepare the concrete adoption proposal under existing scope and request only the missing decision. Do not synthesize prior provenance, erase a failed run, or silently build into another name to avoid a collision.

Once adoption and revision are authorized, the builder creates its own digest-bound contract and follows its complete generation/evaluation workflow. The final builder report links the adoption origin, selected validator findings, actual implementation delta, retained user files, tests, conflicts, and before/after pointer states. Return the actual delivered package for a fresh validator run. No automatic repair loop or operational installation is added.

## 9. Implementation changes and acceptance

Update the development builder entrypoint and specification/regeneration/evidence references to route explicit adoption and describe the new typed origin. Extend helper/parser/grader/profile/schema resources and add focused tests. Preserve existing import/specification build behavior and native installation boundaries. Update routing evaluation with adoption positives and validation-only/spec-authoring/installation negatives.

Use synthetic fixtures and distinct evidence directories. Required scenarios:

| Case | Expected result |
| --- | --- |
| A01: valid existing skill, reviewed spec and managed list | Target unchanged; observed bytes and managed partition recorded; adopted pointer published after verification. |
| A02: skill with known structural/workflow defects | Adoption may succeed as recording; quality remains failed/incomplete and is not relabeled passed. |
| A03: validation-only request or unreviewed ownership list | No adoption publication or target mutation. |
| A04: unrelated file with identical candidate bytes | Conflict; no ownership inferred from equality. |
| A05: changed managed file and unchanged generated proposal | Keep current edit; generated baseline remains distinct from delivered bytes. |
| A06: source, spec, snapshot, or pointer digest changes | Reject dependent action; no pointer advancement; retain evidence. |
| A07: all ordered three-way branches and obsolete files | Exact expected delta including removals, preservation, and conflicts. |
| A08: mutation fails after an earlier file succeeds | PARTIAL with actual delta, no new baseline, retry bound to original origin. |
| A09: generated candidate passes but delivered readback/evaluation fails | No successful generated pointer publication. |
| A10: schema 1 provenance forged from adopted snapshot | Rejected; no fallback interpretation as legitimate generated history. |
| A11: subsequent successful revision | Uses last successful generated N, retains original adoption reference, preserves unrelated files. |
| A12: valid existing generated history or corrupt known history | Normal regeneration or explicit history error; no silent re-adoption. |
| A13: malformed JSON, duplicate paths, traversal, links, excessive snapshot | Evidence error before target mutation or origin publication. |
| A14: operational target selected | No operational write; request points to a separately authorized development-copy path. |
| A15: report says READY but references/authorization disagree | Builder independently refuses dependent action with the exact reason. |
| A16: interrupted or failed pointer publication | Recording/publication distinction retained; no dependent revision until verified publication. |

Run the existing builder regression suite using its current development path:

```text
python -B -X utf8 -m unittest discover -s src/agents/skills/skill-builder/tests -v
```

Run the installed Skill Creator structural check against the enhanced builder, existing explicit `builder-v2` evaluation, and the new adoption/revision/routing profiles with positive and deliberately negative cases. Preserve existing profiles and schema 1 historical behavior. Record exact commands, digests, actual outputs, errors, and retries. These checks are future implementation requirements and were not executed when authoring this document.

Complete the builder's existing required independent import, specification-build, and regeneration forward trials. Add an independent adoption-to-revision-to-revalidation handoff trial using a realistic synthetic skill with a known defect and unrelated user file. The worker must establish the adoption origin, honor review authorization, preserve the unrelated file, expose an injected conflict without mutation, and complete a separately authorized resolution using the same prior origin. Include a later generated-baseline revision to exercise lineage continuity. Do not embed intended answers or fixes in raw trial prompts.

The trial requirement authorizes independent agents during that future enhancement verification, not during this specification-writing task. An unavailable required trial leaves enhancement verification incomplete. Deterministic Python results do not qualify the compiled-Rust runtime or install any operational package.

## 10. Handoff and document status

This companion extension can be implemented separately from `skill-validator`. The validator's inspection, origin reconstruction, reports, and proposed specifications must remain usable before adoption support exists. First adoption-dependent repair requires the implemented, verified extension and the corresponding reviewed inputs.

Current integration references: [builder regeneration](../../.agents/skills/skill-builder/references/regeneration.md), [machine contracts](../../.agents/skills/skill-builder/references/evaluator-contracts.md), and [evaluation requirements](../../.agents/skills/skill-builder/references/evaluation.md). Recheck development source and evidence versions at implementation time; do not edit installed copies merely because these links locate the loaded instructions.

Document authoring and editorial review do not establish extension implementation, adoption of any real skill, successful forward trials, operational installation, or Rust qualification. All such execution remains NOT_PERFORMED in this document-delivery task.
