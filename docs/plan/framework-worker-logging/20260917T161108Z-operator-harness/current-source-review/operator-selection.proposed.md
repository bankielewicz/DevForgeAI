# Proposed refreshed preparation selection — awaiting Bryan's review

This document is a review proposal, not an approval record or permission to launch. The selected native diagnostic is still the one previously approved by Bryan. Native Codex has not been launched for this corrected candidate.

## Concrete difference requiring review

The installed `C:\Users\bryan\.codex\config.toml` gained exactly this section during implementation:

```toml
[features.context_management]
experimental_mode = true
```

Its prior 27,374-byte SHA256 was `beb5cf499ca174940f8f5c91455e54b93d5c2a32f45e1837f5e134c0e10e99cd`; its current 27,430-byte SHA256 is `39d7a2d006e25cfe494cf349d124b18598542ac253a1f9a264fd75e89c7926ef`. Removing only the added section in memory reconstructs the exact approved hash. No installed configuration was restored or edited by this implementation.

The host also added the exact permission rule approved in this conversation for the offline Pester runner. `permission-rule-addition.json` proves that removing only that rule in memory reconstructs its previous hash. This already-authorized rule does not need another approval. The inventory comparison records both changes; the other entries and installed-file count remain unchanged.

## Preserve the stopped preparation and use the still-unused native attempt

A PowerShell mock failed to intercept a fully qualified Python executable in test attempt 11. The support program reached preparation, created `launch-invocation.json`, and stopped on configuration drift before source collection or native dispatch. Its `stop.json` records zero preflight invocations, and neither `native-001` nor `run` exists. The latch and every stop remain intact.

The repaired PowerShell tests intercept the explicit support function; a separate literal-argument test runs a synthetic Python file only. To continue after review, the proposed configuration binds the exact old latch and zero-dispatch stop. The implementation will preserve both and reserve `operator-harness-001/launch-invocation-after-preparation-stop.json` only when Bryan later runs `-RunOnce`. Any changed prior record, prior dispatch, occupied native run, or second reservation still stops execution. This does not add a native attempt or reset a failed native run.

## Requested decision in plain English

Approve preparing the already-selected diagnostic with the configuration currently on this computer, including the experimental context-management setting above. Keep the stopped preparation as evidence and allow a fresh reservation for the single native run that has not yet happened.

All previous limits remain: gpt-6-astra/high, debug/closed-v1, four false findings, the compiled v3 launch policy, child-only omission of ANTHROPIC_API_KEY, one native preflight, no retries, no thread/turn/model task, 120-second Rust and 145-second recorder bounds. Approval of this proposal will finalize preparation only. Bryan's separate console command remains the native execution step.
