"""Write factual developer handoff from retained evidence; no QA closure."""
import datetime
import json
from pathlib import Path
from record import ROOT, PROJECT, QA, digest

def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8-sig"))

metrics = read("metrics.json")
source = read("source-manifest.json")
builds = read("runtime-artifacts.json")["binaries"]
changes = read("changed-files.json")
baseline = read("coverage-red-native.json")["data"][0]["totals"]["lines"]
candidate_hash = digest(ROOT / "source-manifest.json")
build_hash = digest(ROOT / "runtime-artifacts.json")
assert not read("windows-process-readback.json")["processes"]
build_rows = "\n".join(f"| {Path(row['retained']).name} | {row['bytes']} | `{row['sha256']}` |" for row in builds)
coverage_rows = "\n".join(f"| {Path(row['path']).relative_to(PROJECT).as_posix()} | {row['covered']}/{row['count']} | {row['percent']:.6f}% |" for row in metrics["per_file"])
changed_rows = "\n".join(f"| {row['status']} | `{Path(row['path']).relative_to(PROJECT).as_posix()}` |" for row in changes)

delivery = f"""# Native Windows remediation handoff

Development status: **PARTIAL across the original multi-platform finding**. The selected Windows repair candidate is ready for independent QA retest: QA-D01's formatter and native display checks pass, and Windows line coverage now exceeds 95%. QA-D02's Ubuntu portion and WSL/full qualification remain unverified. Both QA findings remain **OPEN pending independent QA**. Framework acceptance: **NOT_EVALUATED**.

Project: `{PROJECT}`. Selected specification: `C:\\Projects\\DevForgeAI\\docs\\plan\\devforgeai-index-service-mvp-spec.md`, SHA256 `52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4`. Only QA-D01 and QA-D02 native Windows remediation was selected. Query-extension implementation and protected Rust authority implementation were not selected. No Git metadata was present.

## Candidate and build identity

Corrected [source manifest](source-manifest.json): SHA256 `{candidate_hash}`; {len(source['files'])} application source/test/configuration/resource files, excluding target build output. A byte-verified copy is retained under [candidate/](candidate/). [Changed files](changed-files.json) bind before/after bytes and hashes; [candidate.diff](candidate.diff) contains the focused source/test delta.

[Runtime manifest](runtime-artifacts.json): SHA256 `{build_hash}`. These freshly built release binaries are retained under [runtime/](runtime/). Release compilation passed against the exact coverage-tested source manifest. Native regression/UI executions used the separately identified instrumented debug binaries; release compilation alone is not native release qualification.

| Release binary | Bytes | SHA256 |
| --- | --- | --- |
{build_rows}

## Per-defect resolution map

| Finding / selected requirement | Correction and observed evidence | Retest disposition |
| --- | --- | --- |
| QA-D01 / DS-025 | `src/tray.rs::status_text` now renders actual per-project current generation and reconciliation time, explicitly labelled Unix seconds/UTC; missing or invalid fields display `unknown`. Existing coverage/freshness/counters/jobs/errors remain. Original QA assertions failed before repair and now pass unchanged. Developer cases cover multiple projects, changed values, null/missing/invalid values and zero. Native UI test compares both values to actual daemon `index.status`, and the screenshot shows both fields. | Windows developer checks PASS; QA must independently rerun both original oracles and native UI. Finding remains OPEN. |
| QA-D02 / section 1.4, DS-A19, AGENTS.md | Added meaningful CLI/IPC, storage, capture, parser, watcher, service, native UI and isolated registry tests. Final Windows executed lines **3314/3486 = 95.06597819850832%**. Original declared unit inventory is **18/18 = 100%**, without padding it with new tests. | Windows floor PASS in this run. Corrected candidate Ubuntu/WSL results NOT_RUN; no cross-platform closure. Finding remains OPEN. |

Native evidence: [screenshot](attempts/coverage-final-002/gui/tray-paused.bmp), [control text](attempts/coverage-final-002/gui/tray-status.txt), and [full test output](attempts/coverage-final-002/stdout.txt). Visual inspection confirmed readable generation and reconciliation fields in the management window. This does not constitute a complete native UI matrix.

## Red, green, refactor and QA evidence

Every retained attempt has exact argv, native cwd, environment overrides, source manifest, timestamps, exit status, stdout and stderr under `attempts/<id>/`. [executions.jsonl](executions.jsonl) indexes all attempts. No older evidence was overwritten.

| Stage/check | Attempt / executed command from application root | Observed result |
| --- | --- | --- |
| Red: original QA behavior | [red-qa-d01](attempts/red-qa-d01/receipt.json) | Exit 101; original generation/reconciliation assertions fail. |
| Red: developer provenance behavior | [red-tray-provenance](attempts/red-tray-provenance/receipt.json) | Exit 101; actual missing generation assertion fails. |
| Red: native coverage | [red-coverage-native](attempts/red-coverage-native/receipt.json), [raw JSON](coverage-red-native.json) | Exit 101; original two QA failures, {baseline['covered']}/{baseline['count']} = {baseline['percent']:.8f}% line coverage. This is the measured suite deficiency, not a fabricated product failure. |
| Green: tray | [green-tray](attempts/green-tray/receipt.json) | Exit 0; 12 unchanged QA cases and 3 tray cases pass. |
| Refactor | `bridge-refactor-native`, `boundary-refactor-002`, `watcher-refactor`, final suite | Explicit internal process/dispatch/watcher boundaries tested; affected assertions pass. |
| Full native test/coverage | [coverage-final-002](attempts/coverage-final-002/receipt.json) | Exit 0, 92 tests pass including 2 setup cases, 2 WSL cases ignored; line floor passes. |
| Formatting | [fmt-final](attempts/fmt-final/receipt.json): `cargo fmt --all -- --check` | Exit 0. |
| Static analysis | [clippy-final](attempts/clippy-final/receipt.json): `cargo clippy --locked --offline --all-targets -- -D warnings` | Exit 0. |
| Release build | [release-build](attempts/release-build/receipt.json): `cargo build --locked --offline --release` | Exit 0. |

Coverage command, executed from `{PROJECT}`:

```text
cargo llvm-cov --locked --offline --all-targets --ignore-run-fail --json --output-path C:/Projects/DevForgeAI/docs/plan/index-service-remediation/20260914T1950304158791Z/coverage-final-002.json --fail-under-lines 95 --ignore-filename-regex '[/\\\\](tests|examples|fixtures)[/\\\\]' -- --test-threads=1
```

`--ignore-run-fail` retains diagnostics on failures; it is not a pass override. Final raw stdout has no failed tests and the collector exits zero. [Raw coverage](coverage-final-002.json), [metrics](metrics.json), [test inventory](test-inventory.json), [retained profile manifest](attempts/coverage-final-002/profile-manifest.json), and [instrumented binary identities](attempts/coverage-final-002/instrumented-binaries.json) bind the actual observations. The binaries remain in the recorded target paths; raw profiles and merged profile data are copied into the attempt.

Executed-line denominator remains all 14 compiled first-party source files, including binaries and Windows adapters. Tests/examples/fixtures and dependency/generated code are excluded; no first-party file or behavior is suppressed. The denominator grew from 3442 to 3486 after the formatter and testability refactors. Branch coverage: NOT_RUN. The Windows margin is only 0.065978 percentage points; independent QA must measure fresh evidence rather than reuse this percentage.

| Compiled source file | Covered/lines | Percent |
| --- | --- | --- |
{coverage_rows}

Case counts are per unique final-candidate case, not summed retries: original declared component units 18/18; selected Windows product Cargo cases 90/90; complete observed Cargo product inventory including the two unexecuted WSL cases 90/92 (97.82608695652173%). Setup 2/2 is separate and receives no product/acceptance credit. This is not the complete specification-derived acceptance inventory. Prior QA's nine independent native CLI cases per host were not re-executed as that independent suite here; developer CLI regressions are current evidence.

## Change rationale and test boundaries

The only feature change is the two status fields. Three behavior-preserving refactors expose internal boundaries: bridge process construction accepts a private executable argument while its public wrapper still fixes `wsl.exe`; host dispatch permits deterministic worker-failure/deadline testing while production still uses `spawn_blocking`; the existing watcher callback is extracted for access-event/error/expired-owner checks. Other source additions only bind cfg(test) modules. Production diff was reviewed against the retained original candidate with `git diff --no-index` (exit 1 denotes differences; no repository or source mutation). Cargo manifest/lock, grammar resources and unrelated original files are unchanged.

Tests exercise typed errors, deadlines, exact bytes, mutation nonoccurrence, persistent state, actual pipe framing, actual owned child processes and UI controls. Added fixtures cover schema-zero backups and corruption, integrity failure, non-Unicode paths/junction exclusion, capture races, parser cancellation/deadlines, generation publication failures, poisoned locks, watcher invalidation, queue/stop behavior and CLI configuration/aliases. They do not hardcode product PASS output.

The bridge test uses a controlled Rust peer and never invokes WSL. The native registry test was explicitly approved: one volatile GUID-owned leaf, HKCU redirected only in a dedicated test process, real startup value type/bytes checked before and after via an unredirected handle, override restored, fixture removed and removal verified. No actual startup setting, systemd unit, operational skill or remote source was changed. This tests registry contracts, not real sign-in launch. Test preferences/paths and junctions are synthetic; owned child processes are joined/stopped. [Process readback](windows-process-readback.json) observed no DevForgeAI processes remaining.

## Preservation, limitations and continuation

Intake verified all 48 original candidate entries with no material drift; no old source was restored. Original QA manifest SHA256 `7681571d0e61f71b857fb57bf1bb466f902781a52a3e2c3fbf4d8f3794a2398b`, failed source-manifest SHA256 `43b63b5a9496b9d5374996d274cf5b852e2301ba23a87490717c786f71790343`. The exact qa-report.md, qa-fix.md and dev-handoff.md entries were verified against required/actual paths, bytes and digests before editing. [Preservation readback](preservation.json) rechecks 266 selected input/QA artifact entries and the copied independent QA oracle. The oracle copy is byte-identical to the supplied QA file. Thirty-four original application files are unchanged; 14 modified and 13 added files are accounted for below.

Earlier failing attempts remain visible. Initial sandbox ACL/IPC failures are environment errors, not valid behavior red results. Retained fixture corrections include an accepted literal glob changed to the intended invalid descending range, a canonical data path, a zero-match test filter corrected to the actual full name, an invalid-handle fixture corrected from the current-process pseudo-handle, and waiting for a modal dialog to close before issuing the next command. Previous below-threshold coverage runs, including 94.205393% immediately before the final isolated registry test, remain FAIL. Tests were not weakened to conceal product failures. No unresolved failure was observed in the final selected Windows suite; this run is not a full flakiness campaign.

Ubuntu and WSL tests/coverage on corrected bytes are NOT_RUN. The prior Ubuntu 74.48% result remains historical failed-candidate evidence; Windows success cannot replace it. QA-G01..05 remain with their original owners: WSL platform qualification; real startup/systemd; remaining alternate-principal/race/crash/overflow/UI cases; complete benchmark CPU/RAM/idle/content-query measurements; full integrity and historical TDD review. Additional developer tests provide evidence for selected paths but do not self-close those gaps. Full qualification INCOMPLETE, framework acceptance NOT_EVALUATED, no installation/deployment performed.

Original and resolved evidence destination are both `{ROOT}`, selected before production edits under the specification's distinct docs/plan run requirement. [Context](context.md) preserves the original literal destination and concrete bindings. [handoff-manifest.json](handoff-manifest.json) records required versus actual artifact paths/bytes/hashes; [verification.json](verification.json) records final readback, including retained candidate/build/profile bytes. The handoff manifest's own digest is returned after readback rather than embedded into itself.

Next owner: independent QA. Rebind the selected specification, this manifest, candidate and build identities; rerun the two original QA oracles, native provenance UI and fresh Windows coverage without altering their denominator. Arrange separately authorized Ubuntu/WSL qualification for the corrected candidate. [checkpoint.md](checkpoint.md) supplies safe continuation context. No QA finding has been marked VERIFIED_FIXED and no acceptance decision is issued.

## Changed application paths

| Status | Path relative to devforgeai |
| --- | --- |
{changed_rows}
"""
(ROOT / "delivery.md").write_text(delivery, encoding="utf-8")
checkpoint = f"""# Remediation checkpoint

Checkpoint recorded {datetime.datetime.now(datetime.timezone.utc).isoformat()}.

Selected project `{PROJECT}`; native Windows QA-D01/QA-D02 remediation under the selected MVP spec and user-provided exact QA handoff. [context.md](context.md) and [inputs.json](inputs.json) preserve the intake and authorization boundaries. Overall multi-platform development status PARTIAL; Windows developer remediation checks pass and are ready for independently selected QA retest.

Original literal and resolved output root: `{ROOT}`. Selection source: this run's pre-write selection of a distinct docs/plan directory under the selected spec; original QA input directory remains immutable. Output map/readback: context.md, handoff-manifest.json and verification.json.

Last verified candidate: source-manifest.json SHA256 `{candidate_hash}`. Release runtime manifest SHA256 `{build_hash}`. Retained source is candidate/, retained release binaries runtime/. Source manifests for coverage-final-002, release-build, fmt-final and clippy-final match exactly. tools.json binds native host/compiler/collector identities. changed-files.json and candidate.diff account for 27 owned application changes; prior source snapshot and QA artifacts retained unchanged.

Completed evidence: original two QA behavior failures reproduced, provenance repair and meaningful coverage tests added, final Windows 3314/3486 lines (95.06597819850832%), original declared units 18/18, product tests 90/90, release/fmt/Clippy pass. Native screenshot inspected. Full execution history and failures remain in executions.jsonl and attempts/. No tests need automatic replay merely to resume this handoff.

Pending: independent QA retest/closure for both findings; corrected-candidate Ubuntu/WSL verification; original QA-G01..05 qualification gaps. No remote synchronization, WSL invocation, installation or actual startup/systemd effects authorized by this checkpoint. The approved process-local volatile registry fixture restored HKCU and verified unchanged real startup bytes and fixture deletion. Branch coverage NOT_RUN; framework acceptance NOT_EVALUATED.

Owned processes: windows-process-readback.json contains an empty observed DevForgeAI process inventory after test cleanup. No known active owned daemon/job remains; unrelated processes were not stopped.

Resume procedure: reread current rules and selected spec; hash original QA inputs and corrected source/build/evidence; compare tool/platform, paths, permissions and process state. Report any drift without restoring source or overwriting old attempts. Invalidate only evidence dependent on changed bytes/platforms. Keep this run and use a fresh directory for independent retest. Next safe action is independent QA under the user's next selected scope; do not issue acceptance or self-close findings.
"""
(ROOT / "checkpoint.md").write_text(checkpoint, encoding="utf-8")
print(json.dumps({"delivery":str(ROOT / "delivery.md"), "checkpoint":str(ROOT / "checkpoint.md"), "source_sha256":candidate_hash, "build_manifest_sha256":build_hash}))
