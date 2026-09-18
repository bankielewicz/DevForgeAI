# Independent QA retest selection

## Exact candidate and scope

Select DFF-WORKER-FEAS-01 version 1.0.0 at `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md`, with the original 30-entry delivery and 305-entry schema manifests in `docs/plan/framework-worker-contract/20260915T151300Z/`. The input-final-checks.json observations rechecked all 335 input entries and both index Cargo preservation identities.

Candidate package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.

Frozen source/test manifest: `C:\Projects\DevForgeAI\docs\plan\framework-worker-implementation\20260915T1544548240203Z\final-source-test-manifest.json`, SHA256 `177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604`, identical to `063-clippy/candidate.json`. This is the selected manifest. The earlier top-level source-test-manifest.json is an intermediate failed-compilation candidate, preserved rather than overwritten; do not select it.

Developer evidence: `C:\Projects\DevForgeAI\docs\plan\framework-worker-implementation\20260915T1544548240203Z`. Read delivery.md, final-test-inventory.json, coverage-05.json/summary, executions.jsonl, and development-notes.md. Verify current source bytes against the selected manifest before testing. Preserve this evidence; write independent findings and attempts into a distinct fresh absolute directory.

## Independent obligations

Execute all WF-01 through WF-20 and each required subfixture from section 8. Write independent protocol-trace assertions from the captured schema and request contracts, independent Windows held-handle lifecycle checks, and negative final-result tests. Do not copy the runner's predicates as the oracle. Inspect external peer assertions for missing branches, vacuous cases, premature exits, setup-only tests, ignored tests, or weakened deadlines. The production watchdog case intentionally takes 120 seconds plus bounded teardown.

Specifically retest buffered pre-response completion followed by conflicting observations; exact and conflicting duplicate events; interrupted acknowledgement versus actual stopped tree; cancellation before IDs without late starts; lost interrupt transport; evidence-write failures; process tree teardown after abrupt harness death; closed request/profile schemas; invalid and reparse paths; exact fixture preservation; cumulative usage sanitization; durable intents and read-only inspection after actual process exit. Check that native/private data are not accidentally retained through diagnostic or unknown-field paths.

Confirm atomic Job Object attachment, restricted inherited handles and no breakaway by inspecting implementation and independent child handles. Returned tree_stopped alone is not independent proof. Reproduce at least Ctrl+C, stdin cancellation and killed harness with a descendant holding pipes. Inspect the actual hidden-console driver and crash driver; inspect never uses a historical PID for mutation.

Measure all first-party executable src lines, including CLI, Windows, error and native-adapter paths. Require >=95% executed-line coverage and >=95% required-case pass rate independently; every mandatory case and subfixture must pass. Report raw counts, exclusions and branch measurement. Count each WF case once; retain retries without inflating the 20-case denominator. Developer results cannot close independent findings.

## Native and protection dependencies

WN-01/WN-02 remain NOT_RUN (0/2 demonstrated native passes). Do not launch Codex, authenticate, inspect live profile/account/configuration or run models under this handoff. A separate explicit native selection must name model/effort, sanitized digest-bound profile review and resource bound. Metadata-only admission observed that the captured launcher path has a reparse component, which current strict path admission rejects. Resolve that captured-executable identity/path dependency under the native selection before a launch; do not relax it or choose another executable silently.

The installed Pro account capability, effective no-tool/no-hook behavior, read-only native policy and native teardown remain unqualified. AMB-01/02/16 and production dispatch remain open. No API billing, extracted tokens, alternate model/provider, relaxed permissions or automatic retry is authorized. No historical independent finding is closed. Framework acceptance is NOT_EVALUATED; these prototype observations are not a protected authority response.

Windows is the selected offline host. Linux/WSL, production deployment, index repairs, operational installation and startup changes are unselected. Do not alter the index manifest/lockfile or operational copies.
