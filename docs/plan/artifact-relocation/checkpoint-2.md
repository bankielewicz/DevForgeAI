# Checkpoint 2: policy and retrieval

The four purpose classes, identity/location distinction, holds, project-selected
retention and local-only availability are documented in the artifact-retention
procedure and DFF-04/08/10. AGENTS loads that procedure only for relevant work.
No universal timer, cleanup, operational activation or collection relocation occurred.

## Verified results

- 58 current navigation links repaired across current specifications/handoffs.
- 40 link occurrences in three historical logs/notes intentionally left unchanged;
  the catalog maps their targets without rewriting those historical records.
- All 76 cataloged local files read back against SHA256/byte bindings.
- 56 files match historical Git blobs on published origin/main ancestry. Their
  immutable links use those exact commits, not a mutable branch or guessed snapshot.
- 20 files are explicitly LOCAL_ONLY; a remote reviewer needs access arranged with
  Bryan. Some differ from historical bytes and some were never tracked. No current
  qualification or content equivalence is inferred for those files.
- All 76 catalog anchors checked. Current reference replacement and preservation
  of the three historical documents verified. JSON parses and source diff reviewed.

The complete checkpoint-1 inventory remains unchanged. Detailed operator receipts
are retained locally under tmp/policy-001 in this checkpoint worktree. Native
product tests/coverage do not apply to these documentation changes. Independent QA
is NOT_RUN; framework acceptance is NOT_EVALUATED.

The artifact root has not yet been created in the primary checkout. A directory-local
ignore marker will be checked before storing payloads there; the proposed tracked
ignore rule is confined to this task branch until separately merged.
