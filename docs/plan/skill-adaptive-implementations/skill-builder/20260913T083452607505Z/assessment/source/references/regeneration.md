# Revisions and conflict preservation

Read known origin records, baseline pointers, manifests and baseline bytes before editing. Preserve legacy generated/adopted history; do not infer no history from a missing convenient pointer. A known missing, corrupt, conflicting or wrong-byte origin is unresolved evidence. A failed revision retains its preceding valid baseline; never adopt around it.

B is verified managed baseline, C is captured current and N is the staged candidate. For an observed first edit only, captured C supplies an explicitly observed B for authorized change_paths. For an authored prior, publication readback and the prior authoring record must match; quality is not required. For legacy history use its original reference root, hashes and success semantics, without rewriting any records.

For each authorized path, reject a proposed path occupied in C without prior ownership, even when bytes match (observed first edits are separately authorized to edit their named existing paths). Otherwise C=B selects N; C=N keeps C; N=B keeps the user's C; divergent edits conflict. Absence differs from an empty file. Preserve unrelated current paths. Removing a modified obsolete managed file conflicts. Never silently merge or rename around collisions.

Before the first write recheck all captured current bytes and original input references; recheck each changed path immediately before mutation. On drift stop remaining writes. Record actual applied_paths and after bytes as PARTIAL when any mutation occurred. Retain failed capture/publication attempts and start a fresh linked run for retries, using the last successful baseline. No automatic rollback.

Only successful delivery and complete readback can publish the next authoring baseline. Store generated baseline separately from actual delivered files to preserve retained user edits. Testing and validation remain NOT_PERFORMED; return the digest-bound manual handoff. Legacy COMPLETE states are never redefined by these new semantics.
