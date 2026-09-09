# Writing a ledger and handoff

Apply this procedure when persistence is requested or appropriate to the discussion. Keep unresolved choices explicit; do not turn bookkeeping gaps into invented facts.

## Assignment and storage

1. Recover the user's authorized output scope and the selected authority record, if supplied. Inspect existing target files and relevant ownership evidence. In Git work, compare the actual worktree, branch/detached state, and base against that assignment. Distinct concurrent writers require assigned distinct worktrees and branches; a new directory alone does not establish isolation. Do not allocate ownership, commit an initial base, change refs, or relax permissions to escape a mismatch.
2. For an observably assigned bootstrap writer, record the task authorization. Missing session or Git metadata is null plus a specific missing_inputs entry. Missing metadata alone neither proves exclusive ownership nor forbids useful discussion. Stop only writes whose authority or collision state is unresolved.
3. Use the existing artifact map and ledger. If none exists, use docs/devforge/ideas and docs/devforge/handoffs under the consuming project. Resolve project and authority stores separately. A permitted report outbox is distinct from permission to write the target: another owner's ledger claim stops ledger writes but does not revoke an explicitly authorized report destination. Bind a report to the supplied assignment as ownership evidence without claiming that it assigns the ledger to the reporting worker. If persistence is unavailable, return a truthful terminal handoff using the same tables; do not choose a substitute directory without authorization.

For a managed task, the external contract selects the exact output identities, revisions and destinations before admission. Use those selections; the default artifact map does not override them. A blocked or routed task requires an externally selected handoff-only contract. Do not switch modes, omit a required ledger, or choose an escape destination to satisfy a weaker gate. Read [managed-runtime.md](managed-runtime.md) when runtime context is active.

## Exact inputs and revisions

Before filling identity fields, classify each source from its own declared record or envelope. A `devforge.artifact/v1` envelope declares identity for that complete document. A native `receipt_id`, heading or row label, and a selector's target fields do not declare the containing document's framework identity. Preserve native receipts, plain notes and selectors in evidence with their own path, complete-byte SHA-256, real locator and scope. Where artifact metadata is required but absent, use `artifact_id: null` and `revision: null` and disclose the gap. Do not add an envelope or rewrite a frozen input to make a reference fit.

For example, these are four different source kinds:

| Source declares | Framework artifact identity | Preserve separately |
| --- | --- | --- |
| Own `devforge.artifact/v1` envelope with `IDEAS-017`, revision 2 | `IDEAS-017@2` | That document's own path/hash |
| Native `receipt_id: CHECK-017` in `check.json` | null / null | Native receipt locator `CHECK-017`, own path/hash, byte-check scope |
| Plain note titled `# Continuation [NEXT-017]` | null / null | Actual heading locator, own path/hash, continuation scope |
| `selection.json` containing a reference to `IDEAS-017@2` | null / null | Selector's own path/hash, then the separately resolved target reference |

A selector's target `artifact_id`, revision, path and digest describe the selected artifact, not the selector itself. Resolve that target's declared identity and complete bytes separately; keep both path/hash bindings. Apply this classification consistently in every repeated reference mapping, input/output table, missing-input explanation and saved response. In a table's artifact ID/revision cell, write, for example, "raw receipt; artifact ID/revision null"; identify `receipt_id CHECK-017` separately as a native locator. A correct null mapping must not become an invented identity in a later table or explanation.

Resolve each relevant upstream reference by artifact ID, revision, selected store/path, SHA-256 of complete bytes, and stable section IDs. If a current file conflicts with a pinned revision, use its preserved exact bytes or report staleness. Never label new bytes as the old revision. Preserve the old reference and identify the affected continuation; other brainstorming may proceed with uncertainty.

Use the selected interchange keys in artifact references, including execution_ref, upstream, and supersedes: `artifact_id`, `revision`, `store`, `path`, `sha256`, and `sections` for referenced stable sections. `store` is the selected alias `project` or `authority`; `path` is relative to that store's root, never an absolute native path. Verify that joining the selected root and path resolves the exact referenced bytes. Do not substitute `section_ids`, invent a store alias, or use a directory as the store value.

Illustrative shape only; replace values with observed input identities before use:

```yaml
upstream:
  - artifact_id: IDEAS-001
    revision: 1
    store: project
    path: docs/devforge/ideas/IDEAS-001.md
    sha256: "{{observed-complete-byte-sha256}}"
    sections: [IDEAS-SECTION-001]
```

Preserve existing input IDs and revisions exactly. If an input has no stable section IDs, use `sections: []`, disclose that absence in missing_inputs and the handoff, and describe the relevant heading and any real row IDs separately; never invent a source ID. A legacy selector may put row targets such as IDEA-001 and IDEA-002 in its `sections` field. Preserve that selector's bytes and selected rows, but do not copy row IDs into a new artifact's section-reference field. Record them outside the reference mapping, for example: "Selected row targets: IDEA-001, IDEA-002 under Ideas and alternatives; source has no stable section IDs; selector: <observed path and digest>." The same applies to an absent artifact ID/revision: use null and disclose the missing identity.

Assign stable IDs to newly authored output sections without editing frozen inputs to make a reference fit. The handoff asset supplies IDs in the heading form `## You are here [STATE-001]`; preserve its IDs and required headings/tables, and give any added section its own unique ID. These heading IDs can be cited in later artifact `sections` lists; row IDs remain separate row locators. Record selected roots, runtime absolute paths and any namespace-to-host mount map separately as execution/evidence location metadata, outside the artifact reference mappings. A report outbox can have a separate delivery locator without becoming a third provenance store.

Before revising an existing ledger, retain its complete prior bytes in existing version history or a collision-free snapshot inside the authorized artifact area. Verify that snapshot, then populate supersedes with the prior ID, revision, store/path and digest. Increment the same document ID's revision. Do not rewrite an adopted decision silently; retain its decision record and route an actual change to its owner. A revised document starts draft unless this exact revision has actual adoption authority.

In managed mode the runtime selects and preserves mutable-output baselines and their archives before admitting work. Use the actual retained archive for the prior revision binding; a baseline hash alone is not preservation. Keep immutable inputs separate from a ledger being revised, and do not modify selected archives. The current managed contract admits draft outputs only; an adopted source decision remains separately attributed and preserved.

## Envelope fields

The package templates contain the standard envelope. Fill every required field with observed facts:

| Field | Value |
| --- | --- |
| schema_version | devforge.artifact/v1 |
| artifact_id / artifact_type | Stable IDEAS or HANDOFF document ID; idea-ledger or handoff |
| project_id | Existing project identity; if unknown, use null and record the gap |
| revision / status | Positive integer; draft by default; status is not a gate outcome |
| created_at_utc | Actual UTC time for this revision |
| producer | devforge-brainstorm and the actual loaded SKILL.md digest or exact installed package revision; disclose the digest's scope |
| execution_ref | Selected session ID/revision, store, resolvable path and actual SHA-256; null plus missing_inputs when absent |
| upstream | Causal artifacts with artifact_id, revision, store, root-relative path, sha256, sections; empty for user-origin brainstorming without causal artifacts |
| evidence | Actual user-message locators, preserved conversation excerpts, source checks and observed receipts |
| supersedes | Preserved prior ID/revision/path/hash, or null |
| decision_ref | Actual adoption reference for this document, or null; one adopted idea need not make the whole ledger accepted |
| missing_inputs | Specific absent facts and consequential uncertainties, never filler |

When a session is supplied, expand execution_ref from the template's compact string into the reference mapping above to carry its selected location and digest; when absent, use null and disclose the gap. Preserve source attribution using row-level evidence or a saved faithful conversation excerpt with stable IDs when the terminal provides no durable message locator. An AI-authored source excerpt is a record of supplied words, not a new user decision. Do not fabricate message IDs, timestamps, session IDs, hashes, or external receipts.

Keep stable section IDs for downstream excerpts (FOCUS-001, IDEAS-SECTION-001, OPEN-SECTION-001, DECISIONS-001, NEXT-001 are initial choices). Keep row IDs IDEA, OPEN, DEC stable across revisions. Split/merge links and handoff backlinks are relationships, not automatically causal upstream edges. A handoff consumes the completed ledger; the ledger must not causally depend on that handoff.

## Observations and closeout

The handoff template applies unchanged in structure to successful, blocked and routed results. Fill its input/output, observed-verification and continuation tables with actual facts. A blocked target is not an output: mark it not produced and name the owner/conflict. A missing skill is not an invoked producer. For an accepted-decision change, preserve the accepted source, put any requested draft proposal in plain-language handoff/response content, and identify the missing change capability. Do not produce a framework change-request under brainstorm. In the continuation table, assign one immediate task to the actual user, assigned operator, or available skill, with prerequisites and observable completion evidence; recommendations do not allocate a new writer. Keep the copyable task consistent with that row.

Inspect attribution, uncertain claims, adoption scope, split/merge history, unresolved consequential decisions, and continuation readiness separately from structural checks. Each observed-verification Outcome cell contains exactly PASS, FAIL, NOT_RUN, COULD_NOT_RUN or NOT_APPLICABLE. Put the cause, scope and receipt location in the other columns. A check planned after the handoff is written is NOT_RUN as of its creation; neither intended code nor a planned receipt supports PASS. No current CLI schema or semantic gate is implied by this template.

Prepare the artifacts in this order:

1. Finish any ledger and read it back. In a managed brainstorm, do this during Record, submit the selected ledger path in the Record checkpoint, and wait for runtime admission to Focus before authoring the handoff. Bind the completed ledger's exact digest in the handoff's upstream and output table. List only completed task outputs; exclude the handoff itself. If none was produced, say why; a managed handoff-only task receives Focus directly from Recover.
2. Write the handoff with the facts observed so far, during the admitted Focus phase when managed. Describe content as ready or blocked as appropriate, but final delivery as pending. Mark the handoff's own later readback, hash check and external receipt publication NOT_RUN. Name their destination as planned, never already saved. This snapshot must remain true even if execution stops immediately afterward.
3. Inspect every repeated input/output digest, source attribution, Outcome cell and saved-file claim for consistency with the actual bytes and observations. Compute truthful artifact metadata where the handoff needs it; this does not make the model the final delivery verifier. Do not insert later self-verification, a self-digest or a self-receipt. If content needs correction, save the corrected final bytes within the current authority and any runtime correction limit; old observations cannot certify changed bytes.
4. In managed Focus, provide its checkpoint after doing the work above: the persisted selected handoff path and a useful next action, owner, completion evidence and non-goals. Required checks and receipt publication belong to the runtime's qualifying Stop callback; the model does not invoke advance/resume/complete/check/verify or the bundled receipt/check helpers. Follow the exact evidence and waiting rules in [managed-runtime.md](managed-runtime.md).
5. Report managed mechanical completion only from the runtime's separately delivered result, with its actual receipt path and full SHA-256. Keep native turn completion, receipt transport/rendering, current applicability, semantic quality and human acceptance separately stated. The handoff's creation-time NOT_RUN rows stay unchanged. If a saved final response is authorized, observe its bytes before claiming that it exists; do not imply that a receipt covers a later response unless that response is actually among its bound targets.

Without an active admitted runtime, deliver the authorized draft or terminal handoff and identify pending persistence or unverified delivery. A missing or failed runtime does not authorize a manual helper chain or a model-authored receipt. The bundled helper files are preserved resources; their presence supplies no observation that a check ran. The runtime's mechanical checks do not replace complete reference/attribution review, inspection of every table and prose claim, or human acceptance.

Retain ownership until the operator changes it. A recommendation is not authority to launch an absent skill or perform external actions.
