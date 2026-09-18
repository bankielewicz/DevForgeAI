# Checkpoint 001: stale-source verification repaired, harness still in progress

Workspace and selected evidence/output locations are exactly those in context.md. Active goal is to proceed through the outstanding-work document; only OW-01/OW-02 implementation is being performed before Bryan's operator run. Do not mark the full goal complete after these preparation tasks.

## Current evidence

- Intake: 393 prior scoped bindings and 26 current-source bindings matched; no probe process was running. Root AGENTS.md and the selected document/receipt match the hashes in context.md.
- `attempts/01-red-stale-sources`: one meaningful failure against the unchanged legacy executor. The independent test first established all 26 current files match and old Sites is absent; legacy verification then required its removed historical install record.
- `operator-harness-001/approved-sources`: new read-only Rust profile-sources invocation, exit 0, empty stderr, no timeout. Raw inventory SHA256 remains d531c3b62b790c4df035916f26d848775597c4c198e688b17b62e0a3d0fd7268, exactly matching the selected 26-file proposal. Only ANTHROPIC_API_KEY was removed from the child copy; no parent/configuration change and no native Codex launch.
- New `operator-harness-001/diagnostic.py` separates immutable manifest checks from current installed inventory checks and checks fixture/junction preservation. `configuration.json` binds six seals, selected QA manifests, three prior evidence trees and documentation-scope bindings. `selection.md` records the current continuation and known source state. Old sources/executors/helpers remain untouched.
- `attempts/02-green-stale-sources` is retained as an unsuccessful green attempt: configuration incorrectly selected an absent optional binaries array in the development evidence manifest. Its source/configuration snapshots are retained. No assertion was weakened.
- `attempts/03-green-stale-sources`: the same focused test passed against the new module after removing only that nonexistent selector from its configuration. Its source/configuration/test snapshots are retained. This is a focused green only, not complete QA or complete OW-01.

## Remaining implementation

1. Implement complete prepare-only operation: immutable/current identity checks; fresh same-context Rust inventory; exact comparison; attributed review, diagnostics and request bindings; new exclusive prepared-packet paths; no native dispatch. Test changed/missing hashes, membership drift, fixture changes and no-launch behavior.
2. Implement explicit run-once composition using the unchanged recorder. Reserve the existing trial's launch latch before its prelaunch refresh/dispatch; reject occupied run/attempt/latch paths. Bind new final inputs, preserve every failure receipt and consume at most one native preflight. This functionality must be exercised only with synthetic peers during implementation.
3. Add live progress/output display without changing raw byte receipts, stdin lifetime or recorder bounds. Keep actual capture on the calling thread so KeyboardInterrupt cancellation semantics remain valid; console display must not block cleanup.
4. Add new root `Invoke-CodexWorkerDiagnostic.ps1`, default preparation-only and explicit `-RunOnce`. Preserve all existing scripts. It must invoke the new support module, not direct native Codex.
5. Complete meaningful isolated and integration tests, fresh inherited recorder tests, Pester PowerShell tests, and separate Python/PowerShell executed-line coverage. All operator runtime modules plus the unchanged recorder are in scope; target >=95% line and case floors without uncovered-code exclusions.
6. Prepare actual current inputs, verify preservation/readbacks, create changed-file/evidence identities and an operator handoff/command. OW-03 awaits Bryan's separate-console run; then inspect the actual evidence and assess OW-04/OW-05.

Python 3.10.11 and coverage 7.9.0 are installed; Pester 5.7.1 is available. No installation is needed. No current commands or subprocess handles are running. No native run, native attempt or launch latch has been created. Source changes are confined to the new support package and selected evidence root; the root entrypoint does not yet exist. Native Codex remains NOT_RUN for this candidate; framework acceptance remains NOT_EVALUATED.
