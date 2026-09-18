# Native-readiness implementation handoff

Development status: **PARTIAL**. Source is frozen for independent QA; the full native-readiness amendment is not complete. Framework acceptance: **NOT_EVALUATED**.

## Candidate and delivered behavior

Package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
Candidate: `candidate-manifest.json`, 36 files, SHA-256 `73ecd4a115b34f824e3e9eef3083866d89c5715cf0053919f9456ee8a4bbb7a8`. Byte copies are retained in `candidate-snapshot/`. `changes.json` records four modified and four added files; no original tests, historical fixture, lockfile or specification changed.

- `src/native_identity.rs` plus compiled-in `native-executable-identity.json` verify only the selected physical executable, exact two directory-junction tags/targets, and SHA-256. All verification errors normalize to `invalid_worker`; arbitrary identity records are not public inputs.
- Schema2 native intake requires the six typed profile fields, with no unknown/null/partial extension. Schema1 peer/native compatibility remains. Intake does not qualify a profile.
- Every schema2 review still fails qualification. A synthetic all-true review produces exit3/profile_unqualified with no spawn event. No restrictive argv is enabled.
- A final identity recheck exists in the future qualified schema2 launch branch. That branch is deliberately unreachable until NI-02 is implemented. Unit tests verify repeated-check byte/target drift; they do not prove native pre-spawn drift handling.

## Executed development evidence

Windows native x86_64, Rust/Cargo1.97.1, LLVM22.1.6, cargo-llvm-cov0.8.4. No Git metadata. Every command receipt binds argv, cwd, source manifest, exit, duration and output hashes.

- `10-identity-red/`: original code rejected the valid proposed v2 intake (`invalid_request`), 1/2 tests passed. Actual behavior failure, not setup error.
- `11-identity-green/`: both initial tests passed.
- `12-intermediate-regression/`: all then-present 52 tests passed, including the production 120-second watchdog.
- `13-identity-negative-red/`: repeated-junction mapping incorrectly admitted; eight other cases stopped in mklink fixture setup because of mixed Windows separators. Those setup failures are not product defects. Their outputs are preserved.
- `15-identity-negative-green/`: all nine synthetic filesystem tests passed after duplicate-mapping rejection and fixture repair, including actual directory symlink substitution.
- `14-profile-gate/`: three admission/schema/profile-gate tests passed, with no Codex app-server launch.
- `02-format/`, `03-clippy/`: frozen candidate passed formatting and Clippy with warnings denied.
- `04-coverage/`: frozen candidate **62/62** unique test functions passed; **1543/1602 executed first-party lines = 96.31710362047441%**. All eight executable `src` files included. Tests/support and dependencies are outside the source denominator; no uncovered production exclusions. LLVM export itself reported no extraneous file entries. Branch coverage NOT_RUN. See `metrics.json`, raw `coverage.json`, and retained `target/llvm-cov-target` data.
- `18-doctests/`: command passed with zero documentation tests present; no additional passing required cases claimed.

The final 62-test denominator is the original 50 functions plus 9 filesystem-unit functions and 3 intake/gate integration functions. Retries and subfixtures do not inflate that denominator. Development checks are evidence, not protected acceptance.

## Requirement accounting

| ID | Development observation | Full criterion status |
| --- | --- | --- |
| NI-T01 | Pinned physical identity admitted, alias never launched | PASS |
| NI-T02 | Alternate path/target/order, directory-symlink substitution rejected | PASS |
| NI-T03 | Missing physical bytes, bad digest/adapter/record rejected | PASS |
| NI-T04 | Strict path resolver unchanged; real extra-reparse/loop rejection and original path regressions passed | PASS |
| NI-T05 | Repeat-verification drift cases passed; actual native pre-spawn branch unexecuted | NOT_RUN / prerequisite blocked |
| NI-T06 | Original WF-01..20 and all original test functions, including F-01/F-02, passed | PASS |
| NI-T07 | No restrictive argv implemented or enabled | BLOCKED by version/effect qualification |
| NI-T08 | Unqualified v2 reviews fail closed; positive qualified review-policy behavior not implemented | BLOCKED |
| NI-T09 | Pinned parsing/feature state research available; runtime inactivity unproven | BLOCKED |
| NI-T10 | Original profile/credential/protocol regressions pass; actual selected Pro/model/effective-sandbox evidence missing | BLOCKED |
| NI-T11 | WN-01 not launched | NOT_RUN / prerequisite blocked |
| NI-T12 | WN-02 not launched | NOT_RUN / prerequisite blocked |

Complete NI criteria: **5/12 = 41.6666666667%** overall; **5/6 = 83.3333333333%** of the initially ready identity/offline group when NI-T05 is counted in full. These are below the full requirements floor, so no full amendment or native acceptance is claimed. The passing 62-function developer suite has a narrower meaning. Do not remove the blocked requirements from the full denominator.

## Concrete remaining dependency

`profile-research/compatibility.md` identifies why the original proposed launch policy cannot be approved. Pinned non-session probes establish configuration parsing and feature state, but do not establish inactive runtime integrations. The proposal lacks a global hook disable and several other effect-capable feature disables. The installed-profile `features list` command does not support strict-config.

`restrictive-launch-policy.next-proposed.json` supplies a reviewable replacement proposal adding thirteen explicit feature disables, keeping memory disable and the exact integration entries. It has a new policy ID and digest. It remains **PROPOSED_NOT_RUNTIME_QUALIFIED_DO_NOT_LAUNCH**, not executable policy. The initial draft is preserved separately; the revised `unknown_keys` text explicitly leaves strict runtime semantics unqualified.

Next implementation needs a bounded, typed pre-thread qualification contract: exact pinned RPC methods/response schemas, source-layer completeness rules, required disabled states, errors/limits, evidence redaction, process observations and cleanup. Validate those against the retained 0.154.0 protocol schemas before implementing a compiled preflight. Current-documentation method names are proposals until that validation exists. A no-thread preflight must never be presented as either selected native trial.

After the prerequisite is resolved: implement and independently QA the exact policy and review-v2 binding; regenerate fixture-specific reviews/requests; then execute one selected WN-01 and WN-02 each using `gpt-6-astra`/`high`, dispatch120s/rpc10s/grace5s/teardown5s/supervisor145s, no retries/substitutions. No old review or PASS may authorize changed bytes. Native races/denials remain non-passes.

Acceptance authority implementation/provisioning remains deferred under the selected native-first plan. An operator attestation by itself is not protected framework acceptance.
