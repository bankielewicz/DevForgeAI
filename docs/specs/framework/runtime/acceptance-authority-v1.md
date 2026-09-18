---
id: DFF-AUTHORITY-01
version: 0.1.0
status: proposed-bounded-implementation-contract
implementation_readiness: bounded-core-and-worker-adapter-specified-not-implemented
qualification: not-performed
updated: 2026-09-15
---

# Windows authority for operator-attested acceptance evidence

[Parent authority design](../../../plan/devforgeai-codex-rust-enforcement-design.md) · [Guardrails](../guardrails-and-rust-runtime.md) · [Decision register](../roadmap-and-decisions.md) · [Worker contract](codex-worker-feasibility-v1.md)

## 1. Outcome and limits

Implement one compiled-Rust local authority that accepts an immutable candidate/evidence bundle, authenticates separate operator approval of its provenance, independently evaluates an approved acceptance policy, commits a decision and returns a verifiable service-owned receipt. The first policy qualifies the Windows **offline worker harness** only. A later explicitly selected policy may require WN-01/WN-02; an offline receipt must never imply native/full-framework acceptance.

This is a bounded contract prepared at the user's request. The user explicitly selected **operator-attested evidence first** on 2026-09-15. No service, accounts, ACLs, policy installation, protected evidence or receipt has been created. This selection does not require automatically isolated QA execution. All service behavior, parsers, policy evaluation, mutation and receipt issuance are Rust. Python and model reports supply observations only.

Exclude worker dispatch, automatic testing, model access, generic phase scheduling, ordinary workspace mutation brokerage, skill-package semantic validation, remote evidence producers, deployment/merge authorization, Linux/WSL host qualification and signing for disconnected receipt consumers. No new dependency on an API account, Enterprise identity or cloud service.

Proposed independent Cargo workspace: `C:\Projects\DevForgeAI\devforgeai\authority`. Binaries `devforgeai-authority` (service) and `devforgeai-control` (client and explicit operator/provisioning modes), library for shared validation. These names are **specified interfaces, not installed commands**. Do not add the package to the index workspace or repurpose its database/service. Rust edition2024/MSRV1.97.1. Begin from pinned, discovered versions serde1.0.229, serde_json1.0.151, sha2 0.10.9, windows-sys0.61.2 and rusqlite0.40.2 with bundled SQLite. Discover cache, required Win32 features and lock resolution before implementation; dependency installation is separate. Service entry/IPC/ACL/SCM behavior belongs in Rust, not PowerShell policy code.

## 2. Trust decision: AMB-03 and AMB-07

### Host boundary (proposed bounded AMB-03 resolution)

Windows service name `DevForgeAIAuthority`; virtual service identity `NT SERVICE\DevForgeAIAuthority`, with a restricted service SID where supported by the selected service configuration. Avoid LocalSystem as the application identity. Service binary and approved client under `C:\Program Files\DevForgeAI\Authority\v1\`; protected state under `C:\ProgramData\DevForgeAI\Authority\v1\`. All concrete SIDs, owners, DACLs, image digests and service configuration are resolved into a provisioning manifest before installation. Unresolved SIDs fail installation; no account-name guessing.

Separate local operator account proposed: `DevForgeAIReviewer`, with a SID distinct from the evaluated account. A human signs into its separate Windows logon session to attest a bundle using the approved CLI. Never run an evaluated agent in that account. Bootstrap administrators approve the first code/policy, provision the identity and protect the installation. Administrator/kernel compromise and a malicious trusted operator are outside the claimed boundary. A renamed agent or another session using the evaluated SID is not independent.

No operator credential, reusable logon handle or signing key may enter the agent's environment, workspace or logs. A mere UAC elevation under the same evaluated SID is insufficient for the selected reviewer separation. The bootstrap admin must establish and verify the distinct account and session; Codex does not invent a protected identity from a JSON field.

Bootstrap manifest is a closed version1 record with `service_name`, `service_sid`, `service_image_path`, `service_image_sha256`, `client_image_path`, `client_image_sha256`, `state_root`, `operator_sids`, `project_roles`, `policy_manifests`, `qualification_manifest_sha256`. Each project_roles entry is `{project_id, uploader_sids, reader_sids}`; no wildcard SID/project grants. Operator SIDs cannot occur in evaluated uploader SID sets. Service checks these mappings for every operation, including reads; original-uploader ownership additionally applies to unfinished bundles. Policies are immutable entries `{policy_id,policy_sha256,path}` beneath the protected policy directory. Updating roles/policies/bootstrap requires the explicit admin provisioning mode, unavailable through agent IPC. The initially unqualified manifest has a null qualification digest and cannot issue authoritative ACCEPTED. Real SIDs and binary digests are resolved after build/account selection, validated by the provisioning CLI and reviewed before effects; the preparation record cannot invent those future values.

### Evidence provenance (proposed bounded AMB-07 resolution)

The operator reviews the immutable imported candidate, independent QA source/oracles, raw receipts and coverage. Through authenticated IPC, the operator attests the exact bundle root and policy digest. Attestation means: the operator accepts responsibility for the provenance and independent review recorded in that bundle. Rust then checks required observations and identities; an attestation is not permission to skip rules or force PASS.

Existing workspace evidence may be imported, but its bytes are **untrusted until attested**. A manifest or reviewer string alone cannot prove that a command ran or that QA was independent. The service must not label imported reports as service-executed observations. Receipts expose `provenance_mode="operator_attested_import"`. If the owner requires protected automatic QA, this increment remains insufficient: specify a separate unprivileged collector identity with protected expected fixtures/runner and an authenticated evidence channel before that stronger claim.

These scoped decisions do not globally close the roadmap's questions for every workflow/platform. Bootstrap installation and qualification remain pending until separately executed with observed denied-access evidence.

## 3. Protected assets and access

| Asset | Service | Operator | Evaluated agent |
| --- | --- | --- | --- |
| Approved binaries, bootstrap manifest, policy versions | Read/execute | Read/execute | Read/execute approved client only as provisioned; no writes |
| SQLite state, snapshots, attestation/decision audit | Read/write | Access through authenticated CLI | Access through allowed query/upload CLI only |
| Operator role mapping | Read | Read; changes require bootstrap admin | No writes |
| Workspace draft files/reports | No arbitrary filesystem access on request | Human may review before import | Ordinary draft access |

Bootstrap administrator owns protected directory roots and disables inherited agent-write permissions, including delete/rename/owner/DACL replacement paths. Service SID has required state writes, not code/policy writes. No Everyone/Users write grants. Include directories' parent permissions and replace/delete rights in tests; file read-only attributes are not protection. No copy of an accepted receipt in the workspace is authoritative.

Service accepts **byte uploads**, not arbitrary local paths to read with service privileges. Client may read workspace files under its own identity, rejecting path escapes/reparse points for reproducible packaging. Server never executes candidate code, test tools, scripts or commands. This avoids turning evidence import into privileged execution or an arbitrary-file-read broker.

## 4. IPC, authentication and resource bounds

Local named pipe `\\.\pipe\DevForgeAI.Authority.v1`. Use explicit DACL, remote-client rejection, first-instance protection and exact data/synchronize access rights; do not grant clients `FILE_CREATE_PIPE_INSTANCE` through generic write permissions. No TCP endpoint. Service registration, image path and bootstrap manifest are protected.

Each request frame is a little-endian u32 length followed by UTF-8 JSON. Maximum65536 bytes/frame; reject zero/oversized length before allocation. Schema has no duplicate/unknown keys, nonfinite numbers or trailing JSON. One outstanding operation per connection, no client-selected commands. Maximum8 connections and2 concurrent bundle uploads; extra clients receive `busy`. Idle frame timeout10 seconds; whole upload deadline300 seconds; per evaluation60 seconds; shutdown drain10 seconds then cancel uncommitted work. Cancellation does not erase committed decisions.

Server authenticates the Windows pipe client token for each request, checks an enabled exact SID/role, and always checks impersonation success. Identification-level token inspection is sufficient; never perform workspace/file operations while impersonating a request. Use RAII to revert impersonation; failure to obtain/revert required security context aborts processing. Claimed role/reviewer fields never supply identity.

Client authenticates the pipe server against the protected bootstrap manifest and SCM service registration: hold a process handle obtained from the connected pipe server PID; verify live process, expected service instance/token SID and approved protected image identity. Recheck connection on service restart. A PID/name alone is not authentication. If this cannot be established on the selected host, fail `authority_unavailable`; do not fall back to unverified workspace status.

Microsoft documents [pipe DACL/access-right pitfalls](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights), [impersonation failure semantics](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-impersonatenamedpipeclient), and [server process identification](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getnamedpipeserverprocessid). The combined verification above is this project's design and requires real host qualification.

## 5. Exact operations and records

Every request: closed object `{schema_version:1, request_id, operation, body}`. IDs are ASCII `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`, hashes are lowercase64-hex. Server derives caller SID. A request ID is scoped to authenticated SID: identical canonical payload returns the committed original response; different payload gives `request_conflict` with no mutation. Preserve request history, not latest-only deduplication.

| Operation / role | Closed body | Result |
| --- | --- | --- |
| `status` / agent or operator | `{}` | Service instance/build/policy IDs and qualified/unqualified availability; no secret state |
| `begin_bundle` / agent or operator | `{bundle_id, manifest_sha256, manifest_bytes}` | Creates temporary upload; manifest size1..1048576 bytes |
| `put_manifest_chunk` / original uploader | `{bundle_id, offset, bytes_base64}` | Sequential <=32768 decoded bytes; exact offset; duplicate identical chunks idempotent |
| `seal_manifest` / original uploader | `{bundle_id}` | Verifies complete manifest bytes/hash/schema before artifact upload |
| `put_chunk` / original uploader | `{bundle_id, artifact_id, offset, bytes_base64}` | Sequential <=32768 decoded bytes; exact offset; duplicate identical chunk idempotent, conflicting retry rejected |
| `seal_bundle` / original uploader | `{bundle_id}` | All bytes/digests/manifest valid; durable immutable bundle or detailed errors |
| `attest` / operator only | `{bundle_id, bundle_sha256, policy_sha256, assessment_sha256, independence_statement_sha256}` | Durable attestation over sealed bytes and exact imported assessment/statement artifacts; authenticated operator SID recorded |
| `evaluate` / agent or operator | `{bundle_id, bundle_sha256, policy_sha256, expected_revision}` | Rust recomputes predicates, commits decision and revision |
| `get_decision` / authorized project reader | `{decision_id}` | Full service-owned decision and receipt, bound to caller's permitted project |
| `revoke` / operator only | `{decision_id, expected_revision, reason}` | Durable revocation, <=1024-character reason; old decision preserved |

Manifest closed fields: `schema_version=1`, `bundle_id`, `project_id`, `candidate_id`, `candidate_manifest_artifact`, `policy_sha256`, `scope_id`, `artifacts`. Each artifact: `{artifact_id, relative_path, role, bytes, sha256}`. Roles limited to `candidate_source`, `candidate_manifest`, `case_inventory`, `test_observations`, `raw_command_receipt`, `raw_stdout`, `raw_stderr`, `coverage_llvm_json`, `coverage_raw`, `tool_identity`, `qa_assessment`, `independence_statement`, `supporting_specification`. Artifact paths use forward-slash relative UTF-8 paths; reject `..`, empty components, absolute/drive/UNC/device paths, Windows reserved device names, colon/alternate streams, case-insensitive collisions and trailing dots/spaces. Storage keys are validated artifact IDs, never client path concatenations.

Limits: <=4096 artifacts, <=256MiB each, <=2GiB total, <=1MiB manifest serialized data, uploaded through the explicit manifest-chunk operations before artifact upload. Empty files are permitted where role allows. No archives, extraction, executable loading, network refs, symlinks or hardlinks are accepted through the protocol. Missing bytes, extra files, mismatched digest or undeclared artifact reject seal. SHA-256 file checks are streaming. The bundle digest is SHA-256 over compact UTF-8 JSON of its closed manifest with lexicographically sorted object keys, artifact array sorted by artifact_id, integers decimal and no optional fields; raw file hashes remain hashes of original bytes. Reject any data that cannot round-trip under these canonical rules.

Client packaging reads immutable byte copies and sends them; a source change during collection requires a new candidate identity. The authority qualifies its sealed snapshot only. Current-workspace consumers must rehash their candidate before applying a decision; candidate B cannot borrow candidate A's receipt.

Response: `{schema_version:1, request_id, status, result, error}` with exactly one non-null result/error. Status `ok` or `error`; error `{code, field, message}` with bounded non-secret text. Error codes: invalid_request, unauthorized, busy, not_found, request_conflict, revision_conflict, digest_mismatch, upload_incomplete, resource_limit, provenance_missing, policy_mismatch, evidence_invalid, authority_unavailable, storage_error. Predicate failure is a successful evaluated result with decision `REJECTED`, not a transport error. Client process exits0 for successful command/ACCEPTED query;2 invalid input;3 unavailable/unauthorized;4 rejected or invalid evidence;5 revision/request conflict;6 timeout;7 uncertain persistence. No successful exit alone establishes acceptance; consumers inspect the bound decision.

## 6. Policy and independent Rust evaluation

Policy is installed only through separately authorized bootstrap/admin updates. Closed v1 policy: `{schema_version, policy_id, scope_id, required_platforms, required_cases, required_tools, eligible_source_paths, zero_executable_paths, excluded_source_paths, coverage_floor_basis_points, case_floor_basis_points, mandatory_cases, required_artifact_roles, accepted_provenance_modes}`. Every case has unique case_id, platform, oracle_id, required artifact IDs/roles and an approved observation-parser version. Actual concrete inventories are fixed from selected source/specification at policy approval, not supplied as a mutable denominator by the evaluated agent. Initial scope ID `worker-windows-offline-v1`; required platform `windows-x86_64`; floors9500 basis points. Every excluded/zero-line path has an operator-reviewed reason. No universal full-framework scope is implied.

The first policy uses the companion [worker evidence adapter](acceptance-worker-evidence-v1.md), which binds exact schemas, source/test/fixture inventories and predicate tables from the frozen retest evidence: all original WF-01..20 subfixtures, IQ-01..06 and RT-01/02 as28 declared groups;50 distinct Rust test functions as regression obligations;6 unit-level functions separately; complete original and repair negative stimuli. Its generated proposed inventory is approved at bootstrap, not taken from caller input during evaluation. Do not parse natural-language PASS prose as an oracle or infer missing subfixtures from one Cargo test name.

The evaluator, in this order, must:

1. Verify approved build/policy and protected-state availability; authenticate request, candidate, sealed bytes and revision.
2. Require a matching operator attestation and imported independence statement. Check receipt/source/test/fixture/spec/tool hashes and platform identities. Reject a self-authored reviewer name as authentication; attestation cannot change policy/case sets.
3. Validate all required files and typed schemas; bind command results to exact source and tools. Raw tool/test evidence is operator-attested, not proven by a JSON hash. No assumption that a trusted compiler version makes an arbitrary report true.
4. Calculate case results from approved deterministic observation parsers and complete required inventory; missing, blocked, failed, errored, skipped and unexecuted cases are not passes. Each case once; retries retained separately and cannot erase failures. Reject conflicting observations unless an approved policy explicitly distinguishes separate instrumented measurement from regression execution.
5. Parse complete LLVM line export; ensure every eligible executable source is represented or has an approved zero-executable declaration, exact path/hash bindings, counts consistent and no duplicate records. Sum `covered` and `count`; use overflow-checked integer cross-multiplication `covered*10000 >= count*9500`. Report branch data separately or NOT_RUN. Tool-origin truth rests on the attested collector execution, not a reimplementation of LLVM's instrumentation in the service.
6. Apply per-platform floors, unit-level and whole-case floors, all mandatory cases and unresolved defect/invariant conditions. A mandatory failure rejects even at99% aggregate. Missing measurement rejects acceptance with explicit reason; no rounding, estimate or denominator amendment. Native scope requires both WN results and interrupted-turn evidence, not merely exit5.
7. Commit the result, exact scope/identities, unmet predicates and receipt in one transaction. The operator cannot request `accept=true` or waive failed mandatory predicates.

Approved policy changes invalidate affected current qualification but preserve old decisions with old policy identity. Adding native obligations creates a new scope/policy; historical offline acceptance does not become native acceptance. No retroactive replacement of QA evidence or earlier failures.

## 7. Durable state, receipts and recovery

SQLite database under protected state; bundled library, foreign keys on, WAL, synchronous FULL, one serialized mutation writer, busy timeout5 seconds. Explicit schema_version1; unsupported versions fail startup with no migration. Migration/export/uninstall require future explicit contracts; do not drop unknown data. Readers use committed snapshots. Upload blobs are written to service-owned temporary files, flushed, digest-checked and moved within the same protected volume to immutable storage before bundle seal commits. Pending unreferenced blobs never imply acceptance. On restart reconcile temporary/incomplete uploads as interrupted, without replaying evaluate/attest or running anything from them.

One transaction commits request-id result, revision, attestation/decision/audit and receipt. A crash before commit yields no accepted state; a crash after commit and lost response returns the same decision for the same request. Corruption or durability error fails closed; no replacement empty database. Do not delete sealed evidence or accepted history automatically in v1; disk-full returns storage_error and blocks new mutations while safe existing reads remain available.

Receipt fields: `{schema_version:1, decision_id, project_id, scope_id, candidate_id, candidate_manifest_sha256, bundle_sha256, policy_id, policy_sha256, authority_build_sha256, qualification_manifest_sha256, provenance_mode, operator_sid, attestation_id, revision, required_platforms, case_metrics, coverage_metrics, decision, unmet_predicates, issued_at_utc, revoked}`. `decision` is ACCEPTED or REJECTED. Successful reads come only from authenticated live service. No offline signature is specified in v1: exported JSON is an informational copy and cannot be verified independently. A consumer without verified service access reports acceptance unavailable. Future portable signatures require a separate key-custody/verification contract.

Service may issue ACCEPTED only after bootstrap qualification manifest pins this exact build, policy, role mapping and installed host. A service cannot qualify itself from its own candidate report. Qualification operator approves the first build after independent tests and real denied-access checks. Unqualified development mode permits inspection/test fixtures only and labels every decision nonauthoritative; there must be no flag that lets the evaluated identity switch it into qualified mode.

## 8. Concrete qualification inventory

Declare exactly20 required groups for this authority slice, each with all listed subfixtures. Every security group mandatory; all platform-required cases mandatory. Full first-party source coverage >=95%, required unit-test and overall case pass rates>=95%, per Windows host and overall; no threshold waives mandatory failures. Before execution expand each group into immutable fixture inputs, expected outputs, platform/tool configuration and artifact paths. Until that fixture binding exists this is a specification inventory, not executed qualification.

| ID | Required observations |
| --- | --- |
| AU-01 | Valid attested exact bundle yields ACCEPTED for its explicit offline scope; no native/full-framework claim. |
| AU-02 | Agent SID cannot attest/revoke/approve policy; forged role/name/operator JSON fails. Distinct non-agent operator succeeds. |
| AU-03 | Agent attempts write/replace/delete/rename/DACL takeover of binaries, state, policy, snapshot and receipts fail under real Windows token. |
| AU-04 | Agent-created pipe impostor and stale service PID/instance fail client authentication; unauthorized client and remote connection reject. |
| AU-05 | Unknown/duplicate fields, malformed UTF-8/JSON, oversized frame, bad base64 and invalid chunk offset reject within bounds. |
| AU-06 | Traversal, ADS, reserved names, case collisions, linked source collection and privileged path-read injection fail without outside effects. |
| AU-07 | Candidate B, changed tests/fixtures/spec/tool digest, missing artifact or extra undeclared bytes cannot reuse candidate A evidence. |
| AU-08 | Missing attestation, altered bundle after attestation, same-SID reviewer session and wrong policy reject. |
| AU-09 | 94.999% line/case results reject; exact95% passes only without mandatory failure; zero/missing/overflow/duplicate counts reject. |
| AU-10 | Missing eligible source, excluded uncovered first-party file, absent raw collector report and cross-platform evidence reject. |
| AU-11 | Mandatory/security defect rejects despite aggregate floor; ignored/skipped/blocked/unexecuted cases counted once as nonpasses. |
| AU-12 | Original failure and successful retry cannot erase history/inflate case count; complete predeclared coverage run remains separate measurement. |
| AU-13 | Exact duplicate request returns same result; conflicting duplicate rejects; concurrent same-revision mutations commit at most one. |
| AU-14 | Crash mid-upload, after blob flush before seal and before attestation commit produces no acceptance; orphan state reported. |
| AU-15 | Crash before decision commit leaves no accepted state; after commit/lost response returns identical receipt on retry. |
| AU-16 | Disk-full, database corruption, unsupported schema and permission loss fail closed; no silent reset or partial accepted state. |
| AU-17 | Normal stop, competing instance, disconnect, timeout and cancellation obey resource bounds; committed evidence survives restart. |
| AU-18 | Workspace receipt forgery and edited exported JSON cannot satisfy client readback; revoked decision preserved and reported revoked. |
| AU-19 | Unqualified service/build/policy or mismatched bootstrap manifest cannot issue authoritative ACCEPTED; admin/operator separation demonstrated. |
| AU-20 | Native policy requires WN-01/WN-02 and interrupted-turn proof; offline-only receipt and completed-before-cancel race do not satisfy it. |

Independent QA must write negative oracles and use actual OS identities, service/pipe/ACLs and crash observations. Mock IPC or unit ACL objects cannot pass native protection groups. Do not install merely to turn these proposed rows green. Provisioning needs a reviewed effects manifest and authorization; run destructive permission/corruption fixtures only on explicitly disposable service state. Preserve all original worker evidence.

## 9. Delivery sequence and unresolved prerequisites

1. Owner selected operator-attested import on 2026-09-15. Preserve its stated trust limits; no automatic protected collector is required for this increment.
2. Implement the exact companion policy adapter schemas/fixtures from the independently retested worker bundle. No placeholder parser or text PASS search. Confirm the bound input manifest before coding and preserve it.
3. `$dev` implements the isolated core and local client with meaningful red/green/refactor tests; no service installation. Return source/build manifests, raw tests, full coverage and a provisioning **proposal** with concrete SID resolution checks/effects.
4. Independent `$qa` assesses core plus test integrity. Build/coverage success does not qualify Windows protection.
5. Bootstrap administrator reviews exact binaries, candidate/policy and provisioning effects, then separately authorizes account/service/ACL creation. Distinct operator identity and qualified client provenance are essential decisions, not agent-invented approval.
6. Independent QA executes AU native groups under the actual evaluated and operator tokens. Any failed protection invariant blocks qualification regardless of percentages. Trusted operator installs the exact qualification manifest through the bootstrap boundary only after evidence review.
7. Import/attest/evaluate the chosen candidate; retrieve decision from authenticated service. Preserve unresolved native work unless native scope was separately satisfied. No deployment or framework phase advance is implied by this acceptance-only service.

Current status: contract preparation only. AMB-03/07 have a concrete bounded resolution with operator-attested import explicitly selected. The companion adapter specifies the first policy binding; identities, approved policy and service are not provisioned, and no protected acceptance has occurred.
