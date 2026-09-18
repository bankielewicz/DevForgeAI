---
id: DFF-WORKER-FEAS-01
version: 1.0.0
status: specified-nonproduction-feasibility
implementation_readiness: ready-for-offline-harness
native_trial_readiness: blocked-on-profile-and-explicit-trial-selection
updated: 2026-09-15
---

# Codex worker feasibility contract

[Runtime owner](architecture.md) · [MVP scope](../mvp/scope.md) · [Coding handoff](../../../plan/framework-worker-coding-handoff.md) · [Discovery and identities](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/framework-worker-contract/20260915T151300Z/verification.md)

## 1. Selected outcome and claim

Build one standalone Rust experimental harness that starts a Codex app-server child, submits at most one turn, collects attributed events, and stops the owned process tree. First qualify its protocol, persistence and process handling against a deterministic Rust peer. Later, an explicitly selected native trial can test the installed Codex/Pro profile. No model trial is authorized by this contract or its coding handoff.

This unit addresses the worker boundary of MVP-03 and MVP-06, with bounded evidence handling from MVP-05. It supplies prerequisites for MC-03, MC-08, MC-09 and MC-10; it does **not** satisfy those complete MVP scenarios. It has no scheduler, repair loop, protected acceptance, production deployment or installed service. Rust owns dispatch during the harness invocation. The process must remain foreground; returning from it ends ownership and terminates its child tree. The production engine's lifetime remains a separate decision.

The selected adapter is Codex CLI **0.154.0**, `app-server --listen stdio://`, using the captured non-experimental-field JSON schema. The command itself remains experimental and unsupported for production according to [official app-server documentation](https://learn.chatgpt.com/docs/app-server). Selecting stable protocol fields does not change that classification. [Non-interactive Codex](https://learn.chatgpt.com/docs/non-interactive-mode) is a documented alternative with JSONL events and saved authentication; this unit chooses app-server to investigate correlated turn cancellation and bidirectional permission requests. This is not a finding that `codex exec` cannot support a future adapter. The documented SDK recommendation for job automation also remains an alternative, not a selected non-Rust runtime dependency.

## 2. Connected path and upstream entry check

OrderDesk is fictional planning material. The following trace checks shared ownership; it does not authorize an OrderDesk implementation or decide its unresolved business semantics.

| Step | Producer -> consumer; exact obligation |
| --- | --- |
| Intake | User/project owner -> planner: select cancellation rule, checkout, applicable policy and existing defect/specification. Adequate brownfield input reuses these artifacts. |
| Business boundary | Owner -> design: define whether dispatch means queue admission, warehouse handoff or another event. Until answered, retain AMB-04/06; do not infer the production rule from code. |
| Design | Design -> development/QA: choose the order-state owner, atomic transition and externally observable responses. A useful synthetic example uses one linearization point: from `ready`, exactly one of cancel/dispatch wins; the loser receives conflict. This is a fixture rule only. |
| Development | Selected work -> candidate A plus valid Red/Green/regression evidence. Each evidence item binds source, tests, policy and host. |
| Independent QA | Requirements + candidate A -> race finding F1, with an independently supplied concurrent-operation oracle. A developer happy-path pass cannot close F1. |
| Repair | F1 -> candidate B and repair evidence. A later coverage request adds obligation V1 without removing F1. |
| Retest/recovery | Independent QA retests B. An interruption retains F1/V1 and known/uncertain effects; no automatic repeat of an uncertain external operation. |
| Delivery | Identified B, assessment and outstanding work -> truthful handoff. Required protected acceptance remains blocked on AMB-03/07. Deployment is separately selected. |

The worker harness connects development or assessment assignments to observations; it cannot choose business policy, close F1 or clear V1. The full loop remains unimplemented.

For a new-product request such as “make ordering easier,” the minimal entry record needs an attributed objective, intended users, selected project/root, constraints and permitted effects. Missing cancellation meaning or success criteria yields a specific question to its owner and a discovery handoff. No coding assignment is admitted for the missing behavior. Once sufficient requirements exist, both routes consume the same project/work/candidate/policy references. This resolves the planning entry check without designing upstream automation.

## 3. Code boundary and dependencies

Proposed destination: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe\`. Create its own `Cargo.toml` with `[workspace]`, package `devforgeai-codex-worker-probe` version `0.1.0`, Rust edition 2024 and minimum Rust 1.97.1. Do not add it to or edit the index workspace manifest/lockfile. No imports from `devforgeai_index` are required.

| Destination under that package | Responsibility |
| --- | --- |
| `src/main.rs`, `src/lib.rs` | Terminal entry, argument validation and public harness API |
| `src/request.rs` | Closed local request schema, identities and path checks |
| `src/protocol.rs` | Captured Codex wire subset and correlation |
| `src/runner.rs` | One-turn state machine, timers and event collection |
| `src/process_windows.rs` | Owned pipes, Windows Job Object and process lifetime |
| `src/journal.rs` | Append-only observations and read-only recovery |
| `src/oracle.rs` | Independent fixture comparison, never protected acceptance |
| `tests/protocol.rs`, `tests/recovery.rs`, `tests/process_windows.rs`, `tests/contract.rs` | Required offline cases below |
| `tests/support/peer.rs`, `tests/fixtures/` | Deterministic protocol peer and fixtures, distinct from runtime source |
| `Cargo.lock`, `README.md` | Exact resolved dependencies and terminal instructions |

Use `serde =1.0.229` with derive, `serde_json =1.0.151`, `sha2 =0.10.9`, `windows-sys =0.61.2` with the Win32 Foundation/Security/Threading/JobObjects/Pipes/IO/FileSystem bindings needed for the specified APIs, and dev dependency `tempfile =3.27.0`. These versions exist in the current index lockfile; this does not assert all features or dependencies are cached. Standard threads, channels and `Instant` suffice; no database, async runtime, HTTP client or model SDK is required. Resolve a separate lockfile offline first. A missing dependency is a setup gap, not a test failure or authorization to install.

Normative parents: AGENTS.md, DFF-01, DFF-03/04/08, DFF-RUNTIME-01, DFF-MVP-01/02 and DFF-EVAL-01. The [delivery manifest](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/framework-worker-contract/20260915T151300Z/delivery-manifest.json) binds exact files; [input manifest](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/framework-worker-contract/20260915T151300Z/inputs-before.json) preserves their discovery identities. Parent planning documents supply only relevant constraints, not additional deliverables. The captured [Codex schema manifest](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/framework-worker-contract/20260915T151300Z/schema-manifest.json) binds every upstream schema file. Do not silently regenerate it against a newer executable.

## 4. Proposed terminal and local data contracts

These commands are specified, **not currently implemented**:

```text
devforgeai-codex-worker-probe run --request <absolute-json-path>
devforgeai-codex-worker-probe inspect --run-dir <absolute-path> --after <u64> --limit <1..100>
```

`run` reads one UTF-8 JSON object, maximum 64 KiB, rejects unknown/duplicate fields and invalid types, and never interprets a shell command supplied in input. Exactly these required fields:

| Field | Type and rule |
| --- | --- |
| `schema_version` | Integer `1` |
| `project_id`, `checkout_id`, `work_id`, `run_id` | Strings matching `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`; distinct concepts, no inferred identity from a directory name |
| `candidate_sha256` | Lowercase 64-hex digest of the exact `task.json` bytes below |
| `checkout_root`, `run_dir`, `worker_executable` | Absolute existing native paths except `run_dir`, which must not exist; normalized and resolved before effects |
| `worker_sha256` | SHA-256 of selected executable bytes; mismatch rejects before spawn |
| `adapter` | `peer` or `codex-0.154.0-stdio` |
| `scenario` | `complete` or `cancel` |
| `profile` | `null` for peer; for Codex, closed object `{model, effort, review_ref, review_sha256}` with nonempty model/effort, absolute review path and SHA-256 |

`checkout_root` contains only `task.json` for the native fixture. Reject missing/extra files, symlinks, junctions/reparse points and a checkout/run directory that overlaps source, operational folders, user home or each other. Run evidence belongs under a new `docs/plan/framework-worker-trials/<run_id>/`; disposable task data belongs under that trial's separate `fixture/` sibling to `run/`. Tests use equivalent disjoint temporary roots. Bind the root layout before launch; every later file read rechecks containment. The native binary must resolve to the discovered Codex path and digest; peer executables must be the test-built peer supplied by the test driver. No arbitrary production project is admitted in v1.

Here, source/operational exclusions mean `src/`, `devforgeai/`, `.agents/`, `.codex/` and `.claude/` under the workspace, not the entire workspace ancestor. The user-home exclusion applies to native fixture/run roots; peer tests may use a fresh test-owned temporary subtree under the user's temp directory, with no access to credential/config roots. Resolve each parent and reject reparse components before creating the final run directory. Concurrent hostile filesystem replacement is not a protected boundary supplied by this prototype. For `peer`, the fixture may additionally contain `peer-case.txt`: an ASCII case selector `WF-01` through `WF-20`, optionally followed by a hyphen and a decimal subfixture index, plus LF. Spawn that test-built binary with the argument vector `--fixture-root`, absolute checkout path. The peer implements the fixed case/subfixture table in section 8; it accepts no shell script or arbitrary command. Native Codex receives only `app-server`, `--listen`, `stdio://`.

All native requests use fixed limits: one server, one thread, one turn, zero harness retries; total dispatch deadline 120 seconds from before spawn, including discovery/handshake. Each RPC response deadline is 10 seconds, capped by the remaining total. After any stop, allow 5 seconds for cooperative completion and 5 seconds for verified tree termination. Total upper bound is 130 seconds plus bounded local evidence finalization. Each incoming line is at most 1 MiB and total incoming stdout plus stderr at most 8 MiB. Excess ends dispatch with `output_limit`; it must not allocate unbounded memory. Drain stdout/stderr concurrently. Cancellation stdin accepts only `{"op":"cancel"}` plus LF, maximum 1 KiB; malformed control input stops with `invalid_control`. EOF is cancellation, so pipe-owning callers must keep stdin open until completion. Ctrl+C is cancellation too.

`scenario=cancel` additionally latches cancellation immediately after binding the turn ID, allowing WN-02 to run through the same terminal interface without a separate driver. `complete` adds no automatic cancellation. Tests may inject shorter monotonic deadlines through a library test constructor; the production request cannot extend or disable the fixed bounds. At least WF-16's native process watchdog variant exercises the production deadline.

Local output is UTF-8 JSONL. Each record contains `schema_version:1`, `run_id`, increasing `seq` starting at 1, UTC `observed_at`, monotonic `elapsed_ms`, `kind`, and `data`. Persist the exact record before emitting it. Allowed kinds: `admitted`, `spawn_intent`, `server_started`, `profile_checked`, `thread_bound`, `turn_intent`, `turn_bound`, `worker_event`, `stop_requested`, `process_exit`, `terminal`. `worker_event` records only supported typed payloads and observed IDs; no editable worker assertion becomes local state. Event timestamps are observations, not provider time or useful-progress percentages.

`terminal.data` contains `outcome`, `reason`, nullable `thread_id`/`turn_id`, `worker_exit_code`, `tree_stopped` (true/false/unknown), `fixture_unchanged`, `oracle` (`match`, `mismatch`, `not_evaluated`), `usage` (measured counters or null), and `open_work:[work_id]`. It never contains an acceptance flag. Successful fixture comparison does not complete framework work.

`outcome` is one of `completed`, `blocked`, `failed`, `cancelled`, `timed_out`, `cleanup_uncertain`; these map respectively to exit 0, 3, 4, 5, 6, 7. `reason` is a stable snake_case category from the failure path (for example `profile_unqualified`, `protocol_error`, `approval_required`, `output_limit`, `oracle_mismatch`, `evidence_write_failed`, `fixture_changed`, `user_cancel`, `deadline`, `cleanup_unknown`). `worker_exit_code` and `fixture_unchanged` are nullable when not observed; never report true/zero for a missing observation. `tree_stopped` uses JSON true, false or null (unknown).

Exit codes: 0 = complete turn, exact oracle match, unchanged fixture and verified stopped tree; 2 = invalid request/identity/path before spawn; 3 = prerequisite/profile/auth/model unavailable; 4 = protocol/provider/worker/output/evidence failure; 5 = requested cancellation, verified stopped tree; 6 = deadline reached, verified stopped tree; 7 = cleanup/effects uncertain. Evidence-write failure is 4 unless cleanup is uncertain (7). Fixture mutation is 4 even if the turn says completed. Cleanup uncertainty takes precedence over every other terminal status. Failure before a run directory can be created emits one diagnostic JSON object to stderr, without inventing a retained journal.

`inspect` performs no spawn, network, repair, append or deletion. It returns one JSON object: `run_id`, up to `limit` committed events with `seq > after`, `next_after` (last returned seq, otherwise unchanged), and `state`. `after=0` starts reading; a value beyond the last committed event is invalid. Partial trailing bytes are reported separately as `truncated_tail` and never treated as an event. Interior corruption or sequence gaps are `evidence_corrupt`. Repeated reads are identical for unchanged bytes and cannot restart work.

`state` is the verified terminal outcome, `admitted` when no spawn intent exists, or `interrupted_unknown` for a nonterminal record with spawn intent. It never infers current process liveness. Reading an actively written journal returns only the last complete prefix; its nonterminal state is still an observation, not a crash diagnosis. If evidence is missing/corrupt, return `evidence_incomplete`/`evidence_corrupt` and exit 4. A sound inspection returns exit 0 regardless of the historical worker outcome; the outcome stays in the returned state.

## 5. Wire protocol and observed state

Use JSONL over owned stdin/stdout with no `jsonrpc` field, numeric client request IDs allocated monotonically from 1, and a separate server-request ID namespace. Never infer a turn ID from the request ID. All field types below are bound to the captured 0.154.0 schemas, including snake-case `text_elements` if supplied.

1. Create the process inside the owned Job Object, then send `initialize` with `clientInfo:{name:"devforgeai_worker_probe",version:"0.1.0"}` and `capabilities:{experimentalApi:false}`. Await its matching response, then send `initialized` with empty params.
2. Protocol preflight calls `account/read` with `refreshToken:false`; accept only `account.type=chatgpt` and `planType=pro`. Do not retain email/account identifiers. `model/list` with bounded pagination (maximum ten pages of 100) must contain the explicitly selected model and effort. Missing, denied or stale selection is exit 3. Never choose a substitute model. Read rate limits once where available; inability to measure is recorded, not an invented zero. A reported exhausted limit blocks dispatch. No login/logout/token-refresh, credit-reset or credit-purchase method is permitted. The peer exercises this identical code path using synthetic account responses and fixed `test-model`/`test-effort` when local profile is null; it never contacts an account. Only the native adapter requires the external operator review.
3. Send `thread/start` with selected model, `modelProvider:"openai"`, fixture cwd, `sandbox:"read-only"`, `approvalPolicy:"never"`, `approvalsReviewer:"user"`, and `ephemeral:true`. Do not override instructions or configuration. Check response cwd/model/provider/approval fields and `sandbox.type=readOnly`, `networkAccess=false`. Any effective discrepancy blocks `turn/start`. Bind returned thread ID. The profile review described below is also mandatory; a legacy sandbox response alone does not prove all tools are isolated.
4. Persist `turn_intent`, then send `turn/start` with thread ID, selected `model`, `effort`, fixture cwd, `approvalPolicy:"never"`, `approvalsReviewer:"user"`, `sandboxPolicy:{type:"readOnly",networkAccess:false}`, and a single text input containing the exact prompt in section 8. Set `outputSchema` to the closed expected-result shape described there. Bind the returned turn ID and reconcile `turn/started` if it arrives first. Buffer at most 32 pre-response notifications; reject conflicting IDs. No second `turn/start` is allowed, including after an ambiguous response.
5. Correlate `item/started`, `item/completed`, `item/agentMessage/delta`, `turn/started`, `turn/completed`, and `thread/tokenUsage/updated` to the selected IDs. Retain bounded unknown notifications as method/size observations; never treat them as completion. Known notifications with malformed fields or wrong IDs fail. `turn/completed` must have a supported `turn.status`: `completed`, `interrupted` or `failed`; `inProgress` is not terminal. Completion before an outstanding start response may be buffered within the same bound and reconciled when it arrives.
6. On a complete turn, compare the completed final agent message against the independent expected JSON, rather than trusting deltas or prose. Use completed `agentMessage` items with phase `final_answer`; if phase is absent/null, accept only a turn with exactly one completed agentMessage. Deduplicate the same item ID seen in item/completed and turn/completed; conflicting content is a protocol error. Require exactly one final result object. Any tool/delegation item fails the native no-tool fixture even if its output matches. Failure/provider errors are observations with the original structured error category, not automatically product defects. A JSON-RPC error on a required RPC ends the attempt. Unknown response IDs, conflicting duplicates or invalid JSON fail; exact duplicate response/terminal observations do not create another state transition.
7. On cancellation with known IDs send `turn/interrupt` once with `{threadId,turnId}`. Its `{}` response acknowledges the request only. Wait for `turn/completed` with `interrupted`, or until the five-second grace ends. Before IDs are known, set a cancellation latch, suppress all future starts, and terminate after the grace. An acknowledgement never proves the child tree is stopped. If completion was durably recorded before cancellation, retain completion; if the stop latch was recorded first, a later completed event cannot clear it.

Any command/file approval request receives the captured response `{"decision":"cancel"}` using that server-request ID and latches `approval_required`. The harness grants no approval, permission extension or persistent rule. Unknown requests, user-input requests, attestation requests and externally managed token-refresh requests get JSON-RPC method-not-supported error `-32601`, then stop; do not implement ad hoc handlers. No `process/*`, `command/exec`, `thread/shellCommand`, config-write, login or external-token method is allowed. The peer must independently check the complete outbound trace.

## 6. Permissions, subscription and process lifetime

Native execution requires a separate user-selected trial request naming model/effort, the 120-second bound and fixture. Before that trial, an operator must review the installed effective profile for this cwd and retain a sanitized record bound by `review_ref`/digest. The record identifies Codex executable, applicable instruction/config/rule sources, native sandbox availability, hook trust, enabled external tools and provider. All applicable source digests must match at launch. Reject a missing review, changed profile, API credentials in child environment, custom provider, active non-sandbox hook/external-tool path, or inability to establish the required read-only/no-tool-network boundary. Do not read or copy credential stores; Codex alone owns its existing ChatGPT login. Do not set another `CODEX_HOME`, bypass rules or change operational config to make the profile pass.

The exact installed effective profile has **not** been inspected or qualified in this planning session. AMB-01/02/16 remain open for native execution. If the reviewed profile cannot meet these conditions, stop with `profile_unqualified`; another contract/profile selection is required. An editable review record is an operator prerequisite, not a protected security principal or acceptance receipt. Automatic verification of arbitrary Codex configuration semantics is outside this unit; the adapter only verifies the reviewed source identities and observable protocol fields.

The review JSON is closed and requires `schema_version:1`, `reviewer` (nonempty attribution), `trial_selection_ref` (nonempty reference to actual user selection), `codex_sha256`, `checkout_root`, `model`, `effort`, `profile_sources` (array of closed `{path,sha256}` records for every applicable instruction/config/rule file), and `findings` (closed object with boolean `native_read_only_available`, `no_external_tool_or_hook_effects`, `codex_managed_chatgpt`, `no_custom_provider`). Every finding must be true, all identity fields must match the request, source paths must be absolute, and no entry may duplicate another resolved file. Unknown values block. The reviewer owns completeness of source discovery; runtime digest checking cannot prove that an omitted source does not exist. This explicit limitation prevents treating the review as automated policy enforcement.

Use an unnamed, non-inheritable Windows Job Object with kill-on-last-handle-close. Atomically attach the app-server process during creation using `PROC_THREAD_ATTRIBUTE_JOB_LIST`; do not create an uncontained process and attach later. Limit inherited handles to the intended pipes, hide the window and disable breakaway. If nested jobs or sandbox children are incompatible, fail before dispatch without relaxing containment. [Microsoft documents job lifetime](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) and [atomic job attachment](https://devblogs.microsoft.com/oldnewthing/20230209-00/?p=107812).

Every exit closes the worker input and stops the owned job. Require process-handle signalling and zero active job processes within the teardown bound, using held handles rather than a later PID lookup. Rust owner crash must close the only job handle. Never kill a process discovered solely from a stored PID. A Job Object controls lifetime, not file/network security; sandbox/profile qualification is separate. Unexpected external effects cannot be rolled back by termination and remain uncertain.

Usage comes from the selected thread/turn's `thread/tokenUsage/updated`: retain latest `total` and `last`, never sum repeated cumulative counters. Missing counters are null/`NOT_MEASURED`. Do not convert account-wide usage into job usage, promise a token cap, infer cost, or discard a rate-limit failure. Elapsed time is the enforceable harness limit; provider-internal retries are observed within it, never counted as new harness trials.

## 7. Persistence and interruption

Use one new run directory and one journal, not a new database topology. Persist `request.json`, fixture byte digest, executable/profile identities and a `journal.jsonl`. Create with exclusive semantics; an existing run directory returns `run_exists` and never starts or resumes work. Each transition is one complete JSONL record followed by `sync_all` before its related dispatch side effect. A single journal owns state; terminal state is derived from its last complete record. Optional stdout/report copies are derivatives, never competing state.

Before spawn, persist `spawn_intent`; before turn dispatch, persist `turn_intent`. A crash between intent and observation produces `interrupted_unknown` on inspection. No replay or auto-resume is allowed even if the request probably did not reach Codex. An operator may later select a fresh run with a new ID after reconciliation; preserve the old one. A durable terminal before a lost CLI response is returned by inspection without resubmission. Missing fixture/request/profile references make inspection incomplete, not successful recovery. A terminal with corrupted/missing evidence is not a valid match.

Retain owned inputs and sanitized observations. Never log auth responses wholesale, environment values, email addresses, credentials or free-form config. Auth events are reduced to mode/plan; unexpected messages retain method/type/length and rejection reason rather than unknown payloads. Task-only agent text and approved typed event data may be retained within limits. Capture stderr as a bounded sanitized diagnostic stream; redact credential-like values before persistence and retain byte counts/digest for omitted data, not the secret bytes. This prototype cannot guarantee arbitrary third-party diagnostics are secret-free; native profile review must address that risk before capture.

Cleanup means stopping the process tree and closing handles. Do not delete trial evidence, credential/session stores, old attempts or the fixture automatically. Verify `task.json` bytes and fixture inventory unchanged after each attempt. Codex's own permitted auth refresh/diagnostic bookkeeping remains a separately observed host effect; `ephemeral` is not a promise of zero host writes.

## 8. Fixture and independent oracles

The native fixture is a small data-evaluation task, not a product repair or benchmark. Create `task.json` as UTF-8 without BOM with **exactly** this single line followed by LF:

Published fixture artifacts: [task](fixtures/codex-worker-v1/task.json), [prompt](fixtures/codex-worker-v1/prompt.txt), [expected result](fixtures/codex-worker-v1/expected.json), and [output schema](fixtures/codex-worker-v1/output-schema.json). Their hashes are in the delivery manifest. These are specification data, not executed trials.

```json
{"schema_version":1,"rule":"Only ready orders can transition; the first action wins and every later action conflicts.","cases":[{"id":"A","initial":"ready","actions":["cancel","dispatch"]},{"id":"B","initial":"ready","actions":["dispatch","cancel"]},{"id":"C","initial":"dispatched","actions":["cancel"]}]}
```

Prompt, exact UTF-8 text with LF at the end, embedding the fixture line in place of `<TASK_BYTES>`:

```text
Evaluate this synthetic OrderDesk transition table. Return only JSON with a results array; each entry has id, final_state and outcomes. A winning cancel produces cancelled and a winning dispatch produces dispatched; winning outcome is applied, all later or non-ready actions produce conflict. Preserve input order. Do not call tools, delegate work, modify files or access other data. This is a data exercise, not permission to operate OrderDesk.
<TASK_BYTES>
```

The independent expected JSON is:

```json
{"results":[{"id":"A","final_state":"cancelled","outcomes":["applied","conflict"]},{"id":"B","final_state":"dispatched","outcomes":["applied","conflict"]},{"id":"C","final_state":"dispatched","outcomes":["conflict"]}]}
```

Parse strictly, reject duplicate/extra keys and require these arrays in this order; object key order/JSON whitespace are immaterial. The output schema requires only `results`, an array of objects requiring string `id`, string `final_state`, and string-array `outcomes`, with `additionalProperties:false` at both object levels. The oracle then checks exact values/cardinality. Freeze fixture, prompt and expected bytes/digests before tests; runtime worker input receives no expected-result artifact. Expected outputs live in the independent verifier, outside fixture write access. This tests correct data output, not actual OrderDesk transaction concurrency.

Required offline inventory: **20 mandatory cases**, each counted once per candidate. `WF-01..08` belong in `tests/protocol.rs`, `WF-09..12` in `tests/recovery.rs`, `WF-13..16` in `tests/process_windows.rs`, `WF-17..20` in `tests/contract.rs`. Use Rust test names `wf_01` through `wf_20`.

| ID | Independent stimulus and required result |
| --- | --- |
| WF-01 | Peer checks handshake ordering, exact allowed methods/fields and one turn; emits valid completed output. Exit 0 and expected result match. |
| WF-02 | Peer returns approval policy `on-request` or sandbox `workspaceWrite` (both subfixtures required). No turn sent; exit 3. |
| WF-03 | Peer returns no account, API account, Plus account and absent model/effort (all required). No turn; exit 3; no credential/login fallback. |
| WF-04 | Wrong thread/turn IDs, malformed JSON, conflicting duplicate response and unknown response ID (all required). Exit 4, no second dispatch. |
| WF-05 | Completion/started notification before start response, plus an exact duplicate. One correlated result and one terminal only. |
| WF-06 | Command/file approvals and unknown server request (all required). Exact cancellation/error response, no accept/rule write, exit 4 with reason. |
| WF-07 | Peer sends `failed` with usage-limit category. Exit 4, preserve category and open work; spawn count one. |
| WF-08 | Repeated cumulative usage, then a separate absent-usage run. Latest counters once; absent null. Never sum or invent zero. |
| WF-09 | Existing run directory with exact/changed request (both). Reject before spawn, all prior bytes unchanged. |
| WF-10 | Crash after spawn intent and after turn intent (both). Inspect unknown/incomplete, zero redispatch and no stored-PID kill. |
| WF-11 | Durable terminal then lost stdout response. Repeated inspect returns the same terminal; pagination boundaries retain every event once. |
| WF-12 | Trailing partial JSON, interior corrupt record, sequence gap and missing input (all). Distinct incomplete/corrupt results; zero mutation. |
| WF-13 | Peer launches a descendant holding pipes; Ctrl+C and stdin cancellation (both). Both handles signal, job empty, exit 5 within grace/teardown bounds. |
| WF-14 | Force-kill the harness while its peer and grandchild run. Independent test-held handles signal within 5 seconds. No orphan, no PID inference. |
| WF-15 | Peer ignores interrupt, plus cancellation before thread/turn IDs. Forced tree teardown succeeds; no late start, exit 5. |
| WF-16 | Peer never responds, emits oversized line and floods stderr (all). Correct deadline/output-limit reason; bounded memory/output and no live child. |
| WF-17 | Invalid IDs/hash, path traversal/junction and overlapping roots (all). Exit 2 before worker launch and unchanged outside sentinels. |
| WF-18 | Wrong output, missing output and extra output keys despite completed turn (all). Exit 4, oracle mismatch; summary cannot override. |
| WF-19 | Peer alters fixture; separate injected evidence-write failure. Exit 4, preserve actual failure, no success terminal, stop tree. |
| WF-20 | Completion/cancel ordering in both orders plus cleanup timeout. Journal order determines first stop/completion; unknown cleanup always exit 7. |

The peer is an external deterministic test dependency, not a stub replacing runner logic. Tests inspect its received messages and actual child handles. Parameter variants all must pass for their parent case to pass; retries do not inflate 20. Setup failures are not Red. Independent QA must write its own process/trace and negative-result checks from this contract; copying implementation predicates does not establish independence.

Native trial inventory, separately **two mandatory cases**, currently NOT_RUN: `WN-01` completes the exact fixture with no tool activity and verified unchanged files; `WN-02` sends cancel immediately on receipt of the turn ID and checks cancellation plus stopped tree. If the model finishes before the cancel is processed, retain the race as inconclusive for native interruption; do not rerun automatically or count it as a cancellation pass. Required but unavailable trials remain in the native denominator, with no demonstrated native pass rate until executed. Protocol peer tests do not qualify native Codex behavior.

## 9. TDD, QA and acceptance limits

Run native Windows tools in this Windows checkout. Discovery observed Windows 11 Pro 10.0.26200 x64, PowerShell 7.6.6, Rust/Cargo 1.97.1, rustfmt 1.9.0, Clippy 0.1.97 and cargo-llvm-cov 0.8.4. Local help/schema commands succeeded with Codex temp/PATH-alias access warnings; this does not demonstrate worker startup. WSL/Linux are not required engine hosts for this bounded unit and remain unqualified.

After creating the selected manifest and separate lockfile, planned commands from the package root are:

```powershell
cargo generate-lockfile --offline
cargo test --locked --offline --test protocol wf_01 -- --exact
cargo fmt --all -- --check
cargo clippy --locked --offline --all-targets -- -D warnings
cargo test --locked --offline --all-targets
cargo llvm-cov --locked --offline --all-targets --json --output-path <fresh-absolute-evidence-path>/coverage.json
```

First establish a compiling harness API/test seam, then execute each focused test and retain its behavioral Red before implementing that behavior. Missing crate/linker or compilation failure is not Red. Preserve Green and any affected refactor rerun. Freeze the QA candidate, required 20-case inventory and coverage denominator before the campaign. The commands above are future checks, not executions from this planning session.

Coverage denominator is every first-party executable line in this new package's `src/`, including native process, error, CLI, journal and oracle paths. Report branch coverage separately when available. Exclude only test/support fixtures and generated/vendor code, never uncovered runtime paths. Use the full llvm-cov JSON to enumerate file identities and calculate that denominator explicitly. Both executed-line coverage and required-case pass rate must independently be >=95%; all 20 mandatory cases and all subfixtures must pass. Record exact counts and raw percentage without rounding to a pass. Native two-case results remain separate; a missing native trial blocks native qualification even with 100% offline results. Index coverage is neither repaired nor relabeled by this package's metrics.

Every run records absolute cwd, executable/version/hash, argv, host/filesystem, start/end, exit code, case/subfixture identity, source/test/profile/schema digests and output paths. A separate independent QA request selects the frozen candidate and this contract; native trials need their own explicit selection. This harness issues observations only. Full framework acceptance, useful product delivery, adaptation and competitive ranking remain NOT_RUN.

## 10. Decision disposition

| AMB | Bounded disposition and remaining question |
| --- | --- |
| AMB-19 | Resolved for this unit: isolated Rust harness destination, dependencies, interfaces and offline oracles above. Production engine source contract remains separate. |
| AMB-16 | Resolved for investigation only: 0.154.0 stdio app-server; experimental/nonproduction. Which supported adapter can meet production dispatch/cancellation remains open. |
| AMB-01/02 | Version/schema discovered. Actual Pro authentication, selected model/effort, effective permissions and telemetry remain native-profile observations; no claim from this conversation's model. |
| AMB-04/06 | Brownfield/new-product entry traced. Actual OrderDesk dispatch definition, stakeholder authority and production policy remain open; synthetic fixture does not decide them. |
| AMB-05/17 | Local probe IDs, journal and no-replay behavior specified. General workflow identities, persistence, transaction topology and protected storage remain open. |
| AMB-09/15 | One-turn deadline/cancel/inspection bounded. Autonomous continuation and full workflow cold recovery remain open. |
| AMB-03/07 | Protected authority and principal independence remain open. This unit cannot pass MC-13 or issue protected acceptance. |
| AMB-08/12 | No test-policy migration or operational skill binding selected. Existing obligations remain unchanged. |
| AMB-18 | Pilot fixture/oracle/bounds fixed for feasibility; comparative cohort, repetition, ranking and qualified runner remain open. |

Other AMB questions remain with their owners. The overall framework is still not implementation-ready. This complete offline harness contract may be selected for coding now; native execution remains blocked on the explicitly identified profile/trial prerequisites, not on a redesign of all framework capabilities.
