# Independent retest selection — corrected worker probe

Candidate: C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe.

Candidate manifest: C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1834258428322Z-dev\candidate-manifest.json, SHA-256 `3f65ade36cf8186fe711da73f1a2794a17d7fb51e02bf66261e9bba0ce158e39`.

Read delivery.md, traceability.md, ownership-review.md, changed-files.json and build-identities.json here. Verify delivery-manifest.json entries and the candidate against current source before testing; report drift without restoring any bytes. Original findings/specification remain bound by ../20260915T1800141514833Z/handoff-manifest.json, SHA-256 `b40d23c3f5751881ca563bbd47c8ce82330420aed3e0e273c13f67f54017daf6`. Governing specification is docs/specs/framework/runtime/codex-worker-feasibility-v1.md, DFF-WORKER-FEAS-01 v1.0.0, SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`.

For a separately user-selected QA turn: use $qa on native Windows. Independently retest F-01/F-02 and M-01 with a fresh sibling evidence root. Preserve original WF-01..20, subfixtures, original supplemental cases and both >=95% floors. Review the new blocked-write/interrupt and malformed-error tests for meaningful behavior; independently hold child/descendant handles and inspect exact retained output. No native Codex launch, profile inspection, launcher identity change, installation or deployment is selected by this handoff.

F-01: require bounded server reply, ordinary RPC and interrupt writes under full-pipe backpressure; cancellation/invalid input and teardown remain responsive, with no retries after uncertain writes. Original stimulus now returns exit 6/deadline in 0.797 seconds and cancellation exit 5 in 0.531 seconds. Review the original QA helper's hard-coded deadline expected_exit=4 against spec §4 (deadline exit 6) and qa-fix.md (bounded failure/timeout/cancel). Its raw FAIL is retained in the Green evidence; no expected value has been altered. Decide the appropriate independent retest expectation explicitly before execution.

F-02: verify supported typed error categories and approved numeric details survive while unknown nested fields, malformed categories and noninteger RPC codes cannot retain synthetic markers in journal/stdout/diagnostics. Original private-error fixture now returns protocol_error with no marker retention. Use synthetic data only.

Developer evidence: 50/50 normal and instrumented tests, executed-line coverage 1420/1487 (95.49428379287156%), format/Clippy PASS. Original 26-group scope retains 25 PASS / 1 helper FAIL (96.15384615384616%). Both numeric floors pass; no all-checks QA PASS or independent closure is claimed. Native WN-01/02 and branch coverage NOT_RUN. Findings remain OPEN, framework acceptance NOT_EVALUATED.
