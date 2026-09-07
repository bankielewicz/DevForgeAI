# Independent static remediation review — revision 02

Assessment: the three original reproduction paths are closed in the revised mechanical implementation. No new actionable defect was identified in the five-file remediation scope. RUNTIME-002 is mitigated by denying B/A reservations, not by delivering a native scheduler. Original runtime-integration requirements remain incomplete. This assessment is not native validation, test execution, human acceptance, release acceptance, or permission to describe the integration as complete.

Reviewer: independently assigned agent `/root/runtime_review_01`; exact model identifier remains unknown. Date: 2026-09-07. The original independent report and its findings are retained unchanged. This follow-up reviewed remediation with knowledge of those findings; it is not a fresh blind review. Candidate code and tests were not edited. The reviewer's only new file is this exclusively created report.

## Custody and scope

Candidate root: `/home/bryan/Projects/DevForge/worktrees/skill-utilities-runtime-20260907`.
Frozen manifest: `runtime-review-02/manifest.json`, SHA-256 `9a7c8e1bbf5114cbe4e75b0d962fd57ed580416894ee667c75544f8e55aa9f2b`.
All 88 manifest-bound file hashes matched at review entry, near completion, and immediately before report creation. The report creation command also rechecks them after publication/readback and reports any mismatch to the assigning reviewer.

Only five manifest entries changed from revision 01: `runtime/delivery/utility_state.py`, `runtime/delivery/utility_evidence.py`, `tests/test_utility_state.py`, `tests/test_utility_native_admission.py`, and `docs/integration/utility-runtime-contract.md`. No manifest entries were removed. The unchanged manifest entries preserve the previously inspected dispatcher, supervisor, hooks, and Rust integration bytes.

Original report SHA-256 remains `ec6482775567e0f2edb6a8d1aa15b9de0a4f684deab50a985c369e056b700cee`.
External original requirements `runtime-integration-spec.md` remain SHA-256 `af737fc3f1c7e19270e6a23d6df784f63065cdeb4447ee4a83f308c09e8d2a68`; they are not part of the candidate manifest. Applicable AGENTS guidance was retained from the first review. `git diff --check` completed successfully. No build, unittest, sandbox, demo, native client or evaluation fixture was launched by this reviewer.

All following code locations are relative to the frozen candidate root.

## Original finding dispositions

### RUNTIME-001 — High in revision 01: mechanical omission path closed; full native evidence processing deferred

`utility_state.py:33-34` defines six mandatory validator gates. Admission at `:160-163` now requires each ID in its prescribed phase. Combined with the existing unique-ID and path checks, an empty gate list or omitted/moved required gate no longer admits a validator task. The selected external gate records continue to bind task, phase, producer and contract digest; `:587-599` consumes/snapshots them and retains their outcomes separately. Receipt generation at `:819-823` includes that outcome mapping.

Additionally, `_gate` at `:338-339` rejects native-C/native-B/native-A PASS and FAIL declarations because there is no authenticated execution-result importer. Thus the earlier outputs-only READY/COMPLETED reproduction is blocked at admission, and an owner-authored execution declaration cannot turn incomplete reporting into accepted native execution. Explicit NOT_RUN/COULD_NOT_RUN records preserve reporting without satisfying native execution requirements. COMPLETED continues to mean mechanical report/artifact custody completion; its limited scope and per-gate outcomes must be preserved by consumers.

The added omission test covers each mandatory gate (`tests/test_utility_native_admission.py:175-181`). The declared native-PASS test checks denial and absence of a receipt (`:183-198`). The incomplete-report path remains explicitly exercised in source (`:200-218`). These are inspected tests, not independently observed test passes. The PASS test does not separately enumerate FAIL or B/A, although the implementation's shared branch covers those IDs/outcomes statically.

Native evidence authenticity, per-attempt execution imports, actual C/B/A behavior, and full successful-evaluation processing remain unavailable. Closure of this concrete omission path does not certify those capabilities.

### RUNTIME-002 — Medium in revision 01: unsafe reservation path mitigated; requested scheduler functionality not delivered

The prospective/replayed native-admission reducer now rejects every attempt whose selected tier is not C (`utility_state.py:529-534`). This prevents an A or B reservation from being the first reservation, and also prevents later B/A reservations after a C reservation. Replaying the journal does not bypass that condition. The existing C reservation still requires prior passing independent gates and remains explicitly non-executing (`:848-875`).

`tests/test_utility_native_admission.py:154-173` adds separate B and A rejection cases. Their attempt ID remains C-01 while the selected tier changes; this correctly exercises the tier field rather than relying on ID naming.

Disposition is fail-closed mitigation, not completed C→B→A enforcement. There is no supported B/A reservation path, preceding-result authentication, launcher or running-attempt scheduler. No time/attempt budget for an executing native client is enforced by this mechanism. Revised documentation states these limits directly at `docs/integration/utility-runtime-contract.md:17-19`.

### RUNTIME-003 — Medium in revision 01: closed at static plan-validation level

`utility_evidence.py:50` preserves the canonical selected client path before subsequent loops reuse the generic path variable. At `:117-119`, plan validation rejects that client under any selected writable workspace or client-state root. This closes the missing-client exclusion while preserving the existing regular-file, digest, no-symlink and disjoint-root checks.

`tests/test_utility_native_admission.py:143-152` covers client-in-workspace and client-in-private-state using pinned regular inert files, so the test reaches the intended overlap predicate. No native launcher was used or demonstrated. The fix proves only the directly inspected plan predicate, not effective native filesystem isolation.

## Additional checks and limits

Required structured fields now reject empty lists/dictionaries as well as null/blank strings (`utility_state.py:304-313`). `tests/test_utility_state.py:172-184` targets both collection forms. False and zero remain accepted scalar values, which is appropriate for domain-valued fields and is stated in the revised contract. The utility output schema still selects required field names rather than a full domain type system or semantic validator; an output's substantive truth is not established by nonemptiness.

General external gate evidence may still reference a worker-project file (`utility_state.py:342-346`). This is not by itself a producer-boundary bypass: an externally owned gate pins the exact bytes reviewed, the runtime snapshots them and later rejects drift. It supports evidence referring to the candidate under review. It must not be described as authentication of execution or independent authorship. The new native executed-outcome denial preserves that distinction.

The five-file scope does not alter waiting/resume, correction reset rules, checkpoint challenges, journal publication, receipt publication/readback, callback dispatch or the supervisor's refusal to launch a non-synthetic process. The stricter gates do intentionally narrow admissible validator contracts: legacy outputs-only validator allocations and prior records that lack required gates are not compatible with this revised runtime. Any future migration/recovery requires separately bound authority rather than silently reusing old state.

Residual functionality required for full integration includes authenticated native result ingestion and C→B→A dependency enforcement, effective launcher/authentication/callback admission, real native execution and budget control, observed delivery, and separately authorized builder-to-validator receiving invocation. Fail-closed denial is appropriate while these are absent, but cannot be counted as their implementation or native conformance evidence.

## Conclusion and verification boundary

No additional blocking defect was found in the focused remediation delta. Original RUNTIME-001 and RUNTIME-003 reproduction paths are closed; RUNTIME-002's permissive path is blocked with functionality explicitly deferred. The revision is a mechanical foundation and incomplete-evidence reporting implementation, not a completed runtime integration.

This follow-up is static and scoped. Suggested negative tests were read but not run; concurrent filesystem races, process isolation, credentials, native hooks, rendering, skill behavior and human acceptance remain unobserved. The report does not replace the required owner-run checks or a separately frozen native allocation. Historical review-01 findings and limitations remain part of the record rather than being erased by this remediation.
