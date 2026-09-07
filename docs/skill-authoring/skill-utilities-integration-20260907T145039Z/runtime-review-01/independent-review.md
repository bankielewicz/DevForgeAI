# Independent static runtime review

Decision: changes requested before runtime integration merge. Three findings: one high and two medium. This is static implementation review, not native validation, semantic evaluation, release acceptance, or human acceptance.

Reviewer: independently assigned agent `/root/runtime_review_01`; exact model identity is unknown because no exact model identifier was exposed to this reviewer. Review date: 2026-09-07. No author discussion or earlier review verdict was consulted. The report is the reviewer's sole authored artifact; candidate files were not edited. No native clients, test fixtures, builds, or evaluation runs were launched.

## Frozen scope and custody

Candidate: `/home/bryan/Projects/DevForge/worktrees/skill-utilities-runtime-20260907`.
HEAD and manifest base: `ddad934f359c108facaca2997bc4fe073df87540`.
Manifest: `manifest.json`, SHA-256 `80f40323103f394b2b7aafc17ebbac83413f0cd915c153791a25539a75ded876`.
All 88 manifest file hashes matched at entry, again near review completion, and immediately before report creation. This checks candidate custody, not correctness of archived validation evidence. Historical logs were hashed without being treated as fresh verification.

Requirements read: `framework/DevForgeAI/docs/skill-authoring/skill-builder-modernization-20260907T125046Z/runtime-integration-spec.md`, SHA-256 `af737fc3f1c7e19270e6a23d6df784f63065cdeb4447ee4a83f308c09e8d2a68`. This external requirements file is not included in the supplied candidate manifest; its digest was measured near report preparation and checked again before creation, rather than independently frozen before this review. Candidate `docs/integration/utility-runtime-contract.md` is manifest-bound at `d43d168a34da1a801c5914293269601e5fff8278f5ad3c6b6c4ea9d0df7cc71e`.

Read applicable candidate and report-repository AGENTS.md. Inspected the four tracked diffs, the three new utility runtime modules, the three utility test modules, the selected requirements and runtime contract, and relevant unchanged supervisor/hook/receipt code. `git diff --check` completed successfully. No claim is made that the required build, lint, unittest, demo, framework-validation, or native checks were executed by this reviewer.

Line references below are relative to the frozen candidate root.

## RUNTIME-001 — High: validator evidence obligations can be omitted while all phases complete

Locations: `runtime/delivery/utility_state.py:117-120`, `:143-161`, `:576-588`, `:801-812`; supporting existing fixture/test: `tests/test_utility_state.py:43-53` and `:338-347`.

Admission requires Enforced P1–P6/T01–T12 labels but does not require corresponding producer evidence or C/B/A outcome coverage. `gate_inputs` may be empty; the only per-phase predicate is the existence of any selected output or gate. Outputs may be plain text or arbitrary owner-selected JSON. Phase advancement checks only the allocated gates. Completion requires output coverage and emits the same COMPLETED receipt with an empty `gate_outcomes` mapping even when no deterministic-review, independent-review, native-prerequisite, or C/B/A result record exists.

This is more than missing semantic grading: the specification requires producer-bound independent review, separately retained planned C/B/A results and causes, and a distinction between incomplete reporting and required evidence satisfaction. The owner can bind an incomplete validator contract without any runtime rejection. Marking task names Enforced does not make their mechanical evidence mandatory. The generic receipt's limited scope avoids claiming release acceptance, but does not supply the missing incomplete-evidence distinction.

Minimal reproduction, statically traced and not executed: construct the existing `Fixture(root, "skill-validator")`; leave its default `gate_inputs=[]`, call `all_ready()`, then `utility.complete(f.state)`. `all_ready()` creates only worker JSON files. The existing test explicitly expects READY at line 347; complete accepts because all selected output paths are in `state.accepted`. The resulting receipt has all six accepted phases and no gate outcomes. No native-admission call is needed.

Requested repair: require a versioned validator evidence mapping at contract admission, including mandatory independent producers and separately identified C/B/A outcomes. Permit failure/incomplete reporting with explicit original causes without treating absent records as satisfied requirements. Add negative cases for omitted producer groups and omitted C/B/A outcomes, and a positive incomplete-report case whose outcome cannot be confused with full evidence satisfaction.

## RUNTIME-002 — Medium: native reservations admit later tiers without earlier-tier outcome evidence

Locations: `runtime/delivery/utility_state.py:511-541`, `:829-864`; `runtime/delivery/utility_evidence.py:95-115`.

Native reservation checks prior P2/P3 PASS records and a PASS prerequisite gate, but does not check the requested attempt's tier against prior C/B/A observations. The plan permits any C, B, or A tier; the replay path verifies membership and duplicate attempt ID only. An A attempt can therefore be the first native reservation in P4 even when there are no C or B outcomes. Reserving C first also cannot establish its successful result: the state stores reservations but has no corresponding tier-result dependency predicate.

The specification requires normal native order C then B then A and blocks dependent execution when prerequisite observations are missing. This endpoint explicitly returns `native_launch_admitted=False` and `execution=NOT_RUN`, so this finding does not assert an actual native launch or authentication bypass. It is a defect in the reservation mechanism if it is used as the prepared admission interface for that required order.

Minimal reproduction, statically traced and not executed: use the native-admission test fixture, change its single plan attempt tier from C to A (with a consistent A attempt ID in plan and boundary record), update the pinned boundary/plan hashes before allocation, establish its existing P2/P3 gates, advance to P4, and request that A attempt. Every branch of `native_admission` and `_apply("native_admission")` admits it; none consumes a C or B result.

Requested repair: bind tier/case/arm/repetition dependencies to explicit producer-owned observations and refuse out-of-order reservations. If reservation is intentionally order-neutral, rename/document that narrower operation and add the separate enforced execution-admission gate before advertising this portion of the integration as complete. Preserve non-executing status until a separately authorized launcher exists.

## RUNTIME-003 — Medium: native client binary may be inside an attempt-writable root

Locations: `runtime/delivery/utility_evidence.py:43-73`, `:107-122`.

The client binary is hashed and checked separately from the `fixed` inputs. At the end of plan validation, roots are checked against each other and each item in `fixed`; the client path is never included in this exclusion. A regular single-link binary located under an attempt workspace or private client-state directory therefore passes `native_plan`. The worker for that attempt would be able to modify the very executable selected by the frozen plan. Rehashing it on a later controller call detects drift after the fact but does not establish the required source/executable boundary at admission.

This is limited to plan validation/reservation because the current supervisor refuses real native launch. It should nevertheless be fixed before a launcher relies on the accepted plan.

Minimal reproduction, statically traced and not executed: move the synthetic inert client in `NativePlanFixture` to `fixture.workspace / "client"`, preserve its regular single-link form, update the plan's client locator/digest before validation, then call `native_plan`. The hash checks pass and the final loop inspects only non-client fixed inputs. Neither workspace existence nor the producer's PASS boundary strings reject that overlap.

Requested repair: require the selected client executable to be outside every attempt-writable workspace/client-state root, and check any other executable or runtime roots relied on by the launcher under the same rule. Add negative cases for client-in-workspace and client-in-client-state. Filesystem boundary declarations must not override this directly observable collision.

## Mechanisms inspected without an additional reported finding

Checkpoint admission binds task, current phase, sequence, one-use challenge and contract digest. Journal replay validates its hash chain and reconstructs phase transitions; accepted outputs and gate evidence are reread against snapshots. Waiting consumes only a configured unresolved question; finite-choice matching and authoritative free-text interpretation bind the pending question, and unrelated messages retain waiting. Resume does not reset the configured deadline or correction count. Corrections exhaust to terminal failure; receipt publication uses exclusive creation, full-byte readback and subsequent artifact rechecks. Repeated completion rechecks existing outputs and receipt. These are static observations, not proof against every interleaving or filesystem failure.

The synthetic supervisor retains no-unconfined-fallback behavior and refuses non-synthetic launch before process admission. Utility gate and answer destinations are excluded from writable project/profile scope. Producer names in records are bindings, not authentication of a human/model identity; external execution custody remains unimplemented and is honestly limited in the source. Completion, receipt publication/readback, native completion, receiving invocation and semantic acceptance remain separately labeled.

## Coverage limits and follow-up

Review did not execute the suggested reproductions, full existing checks, fault injection, sandbox denial tests, concurrent-writer races, actual callbacks, delivery rendering or native C/B/A arms. Exact runtime callback configuration, authentication, duplicate-source exclusion, substantive skill behavior and receiving invocation remain unobserved. No conclusion about those properties follows from this review.

The three findings should receive focused negative tests and a fresh independent review against new frozen hashes after repairs. This report applies only to the manifest-bound candidate reviewed here and does not approve later bytes, merge, installation, deployment or human acceptance.
