# Authorized regeneration

Read this reference before revising an existing generated package. Use the selected import or specification-build mode for the new contract, then compare the last successful generated baseline against the current destination and new generated candidate. The prior successful evidence and explicit revision authorization are both required.

For a specification revision after explicit adoption, read [adoption.md](adoption.md). Its verified published managed snapshot supplies B for the first revision only. Use schema-2 origin references and `revision-spec-v2`; after success, use the last successful generated N for later B while preserving the original adoption reference. Adoption never replaces a valid generated baseline or erases failed attempts. Schema-1 generated history keeps the existing path below.

## Establish B, C, and N

- **B:** Last successful generated baseline bytes, verified against the preceding successful provenance.
- **C:** Current destination bytes, including unrelated user files.
- **N:** New generated candidate bytes, staged in this run's evidence directory.

Absence is a value distinct from an empty file. Do not construct B from current files or from a failed/partially applied run. Record the prior provenance and its digest, generated ownership, the captured active-baseline pointer, and the new contract. Missing or invalid baseline evidence produces `INVALID_EVIDENCE`.

Store four separate, disjoint snapshot directories for B, C, N, and the actual destination after application. The complete revision record and baseline projection shapes are in [evaluator-contracts.md](evaluator-contracts.md). The projection cites the full preceding provenance; it does not replace it.

## Compute the proposed result

Apply these rules in order to every path in the union of B, C, and N:

| Condition | Action |
| --- | --- |
| N proposes a path occupied in C that was not previously owned | `CONFLICT`, including identical bytes. |
| `C = B` | `USE_NEW`: proposed result is N. |
| `C = N` | `KEEP_CURRENT`. |
| `N = B` | `KEEP_CURRENT`, retaining the user change. |
| Otherwise | `CONFLICT`. |

Unrelated C-only files remain `retained_user`. A computed result omitting a required artifact conflicts. An unchanged owned obsolete file can be removed; a modified obsolete file conflicts. Do not silently merge competing changes or choose another target name to avoid a collision.

The evidence helper calculates a proposal from prepared bounded snapshots:

```text
python -B -X utf8 "<builder>/scripts/build_evidence.py" revision-plan --snapshot-root "<snapshot>" --request "evidence/revision-request.json"
```

The request uses the revision metadata in the machine contract without `rows`; the current and after snapshots must initially match because this is a preview. This helper produces rows and planned/conflict status as JSON on stdout. Exit 0 is a plan, exit 1 identifies conflicts or missing required proposed artifacts, and exit 2 identifies invalid input/execution. A missing required N artifact returns `SPEC_GAPS` with `MISSING_INPUT`; record it as a gap rather than treating it as a complete revision plan. Capture a returned plan as `revision-plan.json`. It does not write the destination, publish a baseline, or broker framework mutations.

Record each row's ownership, actual B/C/N hashes or null, action, and reason. Candidate evaluation and this proposal must finish before destination edits. On a conflict, retain candidate evidence and leave the destination unchanged. Resolve the specific conflict through recorded user direction or corrected inputs, then recompute against the unchanged last successful B.

## Apply ordinary authorized edits

Before the first destination edit, recheck type, existence, and bytes for all affected paths against C. A mismatch produces a conflict with no destination writes. Check resolved absolute write/remove paths remain within the selected destination. Links, junctions, excluded content, or file/directory collisions require resolution, not broader traversal.

Apply the proposed edits using the available terminal/file tools under the existing authorization. Immediately before each mutation, recheck that path again. If a later path changes or a write fails, stop remaining mutations. Record the real `applied_paths` delta, capture the actual after snapshot, and label the run `PARTIAL`. Do not claim package-wide atomicity, automatic rollback, successful readback, or baseline advancement.

For a retry, keep B from the last successful run, use actual current C, and generate N for the corrected request. Link the previous partial delta. Files already applied may satisfy `C = N`; a partial run does not become a new baseline by being present on disk.

## Evaluate readback and publish development evidence

After successful edits, capture the complete destination after snapshot. Evaluate the delivered package using the revision profile, run required structural/script/task checks, and read back the resulting files. An `APPLIED` record with evaluation and readback success can first retain `baseline_advanced: false` while the successful pointer is prepared.

Only after those results may the active development baseline pointer identify the current run and N's generated digests. Capture its actual before/after bytes and the final revision observation; a published record must show the real advanced pointer. Keep generated N and delivered after separate when a user change was retained.

Write complete provenance and the final report with prior-run links, concrete results, and actual evidence digests. The pointer and local checks remain agent-writable development evidence; compiled Rust alone owns future framework validation, mutation, phase state, and acceptance.
