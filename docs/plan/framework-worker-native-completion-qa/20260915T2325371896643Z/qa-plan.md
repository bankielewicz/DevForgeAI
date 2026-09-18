# Independent QA plan: native worker completion

## Identity and state

- Invocation: full independent QA run, currently in preparation.
- Plan status: `READY` for the offline campaign; live cases retain the explicit prerequisites below.
- Execution status: `IN_PROGRESS`.
- Candidate: frozen 48-entry source manifest `docs/plan/framework-worker-native-completion/20260915T2306060954875Z/candidate-manifest.json`, SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`.
- Governing contracts: DFF-WORKER-FEAS-01 v1.0.0, DFF-WORKER-NATIVE-01 v0.1.0, and DFF-WORKER-PREFLIGHT-01 v0.1.0 at the hashes in `context.md`.
- Selected platform: native Windows x64 only.
- Scope: NI-T05 and NI-T07 through NI-T12; regression of WF-01 through WF-20 with every specified subfixture; focused F-01 blocked-write/cancellation cleanup and F-02 typed-error-retention checks; formatting, Clippy, all-target tests, first-party executed-line coverage, CLI/error-path checks, and test-integrity inspection.
- Exclusion: acceptance-authority implementation and any protected acceptance decision.

## Entry and stop rules

Execution starts only after independent readback proves the frozen candidate, snapshot and specifications match. Before the first product command, QA inspects every frozen first-party Rust source, test, support binary, and QA helper for prohibited mock attributes, vacuous assertions, swallowed errors, fake integration boundaries, retries counted as tests, ignored/skipped cases, coverage suppression, and denominator manipulation.

A confirmed mock decorator/result gaming, a valid complete metric below 95%, or a confirmed critical authorization/security/data-preservation defect stops the whole campaign immediately. An ordinary mandatory failure keeps the verdict FAIL while other safe independent checks continue. A local harness/prerequisite gap blocks only dependents. Native denial, unavailable account/model, or profile conflict is a prerequisite outcome unless product behavior violates the contract.

## Requirements-to-tests matrix

| Case ID | Requirement | Expected observable behavior | Level | Readiness | Evidence |
| --- | --- | --- | --- | --- | --- |
| QA-ID-01 | NI-T05; preflight required pre-thread protocol and observations | Fresh source inventory and pinned executable identity are rechecked immediately before actual spawn. A valid live identity observation proceeds to owned spawn; synthetic alias or physical-byte drift rejects before spawn with exit 2 and no old-evidence mutation. | Rust unit/integration plus compiled preflight | READY offline; live positive observation depends on qualified source collection | raw receipts, journal, process trace, independent fixture manifest |
| QA-POL-01 | NI-T07; preflight fixed launch section | Exact compiled policy ID/digest/argv contains all 35 disables, is shell-free and native-only. Caller argv/config/profile/home/credential injection, peer schema v2, and policy mismatch reject before native spawn. | Unit/integration/compiled CLI | READY | policy bytes/hash, argv trace, negative inputs, raw streams |
| QA-REV-01 | NI-T08; preflight source-inventory section | Closed review v2 binds exact policy, inventory and profile sources. Old/unknown/missing/null/duplicate/wrong-type fields, incomplete coverage, added/mutated/reparse sources and stale digests block qualification. `profile-sources` reads no credential contents and has fixed roots/bounds. | Unit/integration/compiled CLI | READY offline; live source collection may produce a prerequisite denial | independent malformed records, inventory before/after manifests, raw streams |
| QA-EFF-01 | NI-T09; preflight required pre-thread protocol | Required RPC order and exact parameters are observed. Config, requirements, 35 feature disables plus the closed allowed-enabled list, hooks, plugins, installed apps, MCP state, pagination, unknown work/events and descendant accounting all fail closed. No `thread/start` or `turn/start` occurs in preflight. | Unit/integration/compiled peer and live preflight | READY offline; live portion depends on qualified source collection | independent trace oracle, negative cases, process accounting, journal |
| QA-PRO-01 | NI-T10; preflight required pre-thread protocol | Source/environment/sandbox/provider conflicts, inherited credential variable names, non-ChatGPT/non-Pro account, absent exact model/effort, rate-limit denial, malformed responses, or unexpected sandbox state prevent work. An unmeasurable rate-limit payload is explicitly recorded. Runtime inspection is repeated before a trial turn. | Unit/integration/live preflight and native run | READY offline; live portion depends on qualified source collection | redacted env-name projection, protocol trace, journal, raw streams |
| QA-NAT-01 | NI-T11 / WN-01 | Exactly one native server/thread/turn returns the exact contract JSON, emits no tool/delegation item, preserves fixture bytes and ends with a verified stopped tree. No retry. | Native compiled CLI | BLOCKED: frozen offline QA and successful live preflight | immutable fixture manifests, raw streams, journal, inspect output, process evidence |
| QA-NAT-02 | NI-T12 / WN-02 | Exactly one native server/thread/turn is interrupted after turn ID, an interrupted terminal event is observed and the tree is verified stopped. A completion race is INCONCLUSIVE and is not replayed. | Native compiled CLI | BLOCKED: frozen offline QA and successful live preflight | immutable fixture manifests, raw streams, journal, inspect output, process evidence |
| QA-WF-01..20 | Base section 8; NI-T06 regression dependency | Each of the 20 parent cases passes all contract-listed subfixtures; a parent counts once and any subfixture failure fails its parent. Real Job Object/process behavior remains required for WF-13..16. | Integration/compiled peer/process | READY | cargo output, retained per-case fixture traces, parent/subfixture accounting |
| QA-F01 | Blocking writer repair | A full child stdin pipe cannot bypass the deadline/cancellation budget; descendants stop and cleanup is verified. Contract deadline exit is 6, cancellation exit is 5. | Windows process integration | READY | focused test/independent trace, handle/process observations |
| QA-F02 | Typed error retention | Only contract-approved typed error fields reach journal/stdout; arbitrary provider data, secrets and unknown nested fields do not. | Integration/negative path | READY | crafted error payloads, byte scan of raw journal/stdout |
| QA-CLI-01 | Base/preflight terminal contracts | Closed command grammar, absolute paths, limits, exit codes, preflight terminal shape, profile-sources diagnostics, inspect idempotence and no replay match the contracts. | Compiled CLI | READY offline | exact argv/cwd/raw streams/exit/duration receipts |
| QA-INT-01 | QA integrity policy | No prohibited mock attribute, result gaming, hidden skip, retry inflation, fake native claim, unjustified coverage exclusion, or stale evidence binding exists in the frozen candidate or QA helpers. | Static semantic review plus sensitivity checks | READY | file inventory, source locations, helper review |
| QA-QUAL-01 | AGENTS / base section 9 | `cargo test --locked --offline --all-targets`, rustfmt and Clippy complete against exact frozen bytes; first-party executed-line coverage is at least 95%. | Build/static/test/coverage | READY | raw command receipts and llvm-cov JSON |

## WF parent and required subfixture inventory

The project-wide mandatory WF denominator is exactly 20 parents. Subfixtures are obligations within their parent and are also recorded individually so an omitted variant cannot hide behind a passing parent: WF-02(2), WF-03(4), WF-04(4), WF-05(early completion/early started/exact duplicate), WF-06(command/file/unknown request), WF-08(cumulative/absent), WF-09(unchanged/changed request), WF-10(after spawn intent/after turn intent), WF-12(partial/corrupt/gap/missing), WF-13(Ctrl+C/stdin), WF-15(ignore interrupt/cancel before IDs), WF-16(no response/oversized line/stderr flood), WF-17(invalid IDs/hash/path traversal or junction/overlap), WF-18(wrong/missing/extra), WF-19(fixture mutation/evidence-write failure), and WF-20(completion-first/cancel-first/cleanup timeout). WF-01, WF-07, WF-11 and WF-14 are single-scenario parents. Frozen test inspection must prove the concrete mapping rather than infer it from function names.

## Independent oracles

- Policy oracle: exact literal ordered argv from the selected policy contract and retained proposed-vector input, hashed independently from compiled source bytes.
- Protocol oracle: a QA-authored expected ordered method/parameter table from preflight lines 30-43, with explicit forbidden `thread/start`/`turn/start` during preflight. The oracle does not call product validators.
- Output oracle: strict parse and value/cardinality comparison against base section 8 expected JSON; no expected artifact is placed in native fixture write access.
- Cleanup oracle: independently held process handles/Job Object observations and bounded absence of live owned descendants; exit code alone is insufficient.
- Privacy oracle: byte-level canary fields in synthetic provider errors/config responses must be absent from all retained journals/stdout while allowed typed fields remain.
- Source oracle: independently enumerate frozen package bytes and eligible `src/**/*.rs` files, resolve paths before coverage inclusion, and compare pre/post hashes.

## Metrics declared before execution

1. Required Rust unit-test pass rate: every frozen `#[test]` function compiled into the package's library/unit targets, counted once. Failed, errored, ignored, skipped, blocked or unexecuted required unit tests are nonpasses. The exact frozen denominator will be published before commands run.
2. Project-wide required executable test rate: every frozen Rust test function across library and integration targets, counted once, reported separately from unit rate. This captures supplemental and regression functions without using them to inflate WF or NI case counts.
3. WF acceptance rate: 20 unique parents, separately reporting all required subfixture outcomes.
4. Selected native-readiness rate: seven unique groups, NI-T05 and NI-T07..12. Synthetic results can support NI-T05/07..10 but cannot pass NI-T11/12 or the live portions of NI-T05/09/10. Blocked/unexecuted groups are not passes.
5. Coverage: executed lines divided by every executable line in every frozen first-party `src/**/*.rs` file, including CLI, errors, native process, journal, policy, profile, inventory and oracle paths. No production source exclusions are allowed. Test/support/fixture code and dependency/generated code are outside this source denominator by contract. Branch coverage is reported separately if present.

Each applicable metric floor is 95% at full precision. Coverage collection includes all tests selected to contribute to the campaign and becomes final only after they have terminal results and llvm-cov returns usable JSON for the declared source inventory. No partial measurement triggers a numeric verdict.

## Command and evidence protocol

After freeze, every command attempt receives a unique directory containing: a before/after complete package manifest; executable path/hash; exact argv as an array; cwd; only explicit environment overrides; UTC start/end; monotonic duration; owned PID; native exit code; timeout/containment observations; and byte-exact `stdout.bin`/`stderr.bin` with sizes/hashes. Console summaries are derivative and never labelled raw. Cargo uses a QA-owned `CARGO_TARGET_DIR`; process fixtures use a QA-owned `WF_TEST_EVIDENCE` root. Commands are bounded and noninteractive.

Planned order after freeze: identity/spec readback; integrity inspection; frozen test enumeration; focused independent negative checks; complete locked offline tests; rustfmt; Clippy; complete llvm-cov collection. If those pass and no stop trigger exists, collect the real profile source inventory and execute one live preflight. Only a qualified preflight and operator review permit WN-01 once, then WN-02 once. A consumed native attempt is never silently retried.

## Checkpoint

No QA process or fixture is owned at this checkpoint. No product test has been launched. Next safe action is to receive the developer's frozen candidate manifest, verify exact source/specification identity, finalize the test-function and source denominators, inspect test integrity, and begin only the offline campaign.
