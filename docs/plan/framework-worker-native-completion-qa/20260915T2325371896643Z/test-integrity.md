# Frozen candidate test-integrity assessment

Candidate manifest: `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd` (48/48 live and snapshot entries independently matched).

## Result before execution

No prohibited mock decorator or confirmed result gaming was found. The offline campaign may proceed. This is a bounded Rust-package assessment, not a native-profile or framework-acceptance result.

## Inspection performed

- Inspected all 38 frozen Rust files, Cargo dependency declarations, all 89 physical `#[test]` attributes, module-path seams, support binaries, assertion helpers, and the QA capture/identity helpers.
- Resolved the four conditional attributes: each is `#[cfg(test)]` and includes private tests from an exact relative path. There are no unresolved dynamic attributes, procedural attribute macros, or macro definitions in the candidate.
- No `#[ignore]`, `#[should_panic]`, Rust coverage suppression, mock/fake/double dependency, `mockall`, `automock`, or analogous mock-generating attribute exists.
- Two textual gaming locators were benign: an invalid-input fixture literally uses scenario `retry`, and a process comment says never to queue a retry. Neither is a runner retry.
- Retention-only `let _ = ...keep()` calls preserve QA fixtures when `WF_TEST_EVIDENCE` is set. Test-owned junction cleanup deliberately ignores only removal errors during Drop; assertions execute before cleanup. These do not turn errors into passes.
- `unwrap_or_default` in the profile protocol helper reads optional evidence after the actual protocol result and process-stop assertions; privacy assertions still examine every retained file that exists. It does not replace a failed protocol result with success.
- The support peers are compiled external child processes with observed pipes/traces/handles. They are legitimate deterministic dependencies for offline protocol tests. They do not receive credit for live Codex, installed-profile, NI-T11 or NI-T12 behavior.
- The journal-only preflight recovery test deliberately constructs a record stream and proves only inspection/integrity behavior; it does not claim an app-server ran.
- Fixed policy tests use a literal contract-derived 35-feature vector and pinned record digest. The independent QA oracle will also compare the compiled JSON directly with the finalized contract.
- WF parent tests exercise all required variants through explicit loops/case selectors and fail their parent on any assertion. Subfixtures remain obligations within their parent and do not inflate the 20-parent denominator.
- F-01 uses real Windows pipes, descendant handles and bounded stop observations. F-02 injects byte canaries and scans journal/stdout; neither substitutes an in-memory mock for the claimed boundary.

## Unsafe/FFI review

Unsafe production code is limited to Windows handle/process APIs in `process_windows.rs`, native reparse inspection in `native_identity.rs`, and console control registration in `main.rs`. Handle construction uses owned RAII handles, process creation supplies an explicit inherited handle list and Job Object list, and the final candidate selects `DETACHED_PROCESS`. Job accounting checks cumulative and active processes so a short-lived descendant cannot disappear from the preflight decision. The planned Windows tests exercise actual process creation, cancellation and teardown. Static review does not by itself prove native lifecycle behavior; those tests remain required.

## Known proof limits

- Physical `#[test]` count is not the executable test denominator. The exact Cargo target/test list will be captured next and bound before the full run.
- Synthetic configuration/profile data proves fail-closed validators and projection behavior only. Actual installed source inventory and real endpoint behavior require the compiled source collector and, if qualified, live preflight.
- Successful offline results cannot satisfy NI-T05's actual pre-spawn positive observation, NI-T09/NI-T10 live profile portions, WN-01, or WN-02.
- Existing developer receipts are contextual only. Fresh QA commands and raw streams are required for this frozen candidate.

Evidence: `00-freeze-audit/`, `01-integrity-locators/`, `preparation-integrity-review.md`, and frozen candidate source at the bound manifest.

