# QA remediation handoff to dev

## Selected candidate and authority

- QA run 20260914T191133863776Z, **FAIL**: C:/Projects/DevForgeAI/docs/plan/index-service-qa/20260914T184442947070Z/executions/20260914T191133863776Z/qa-report.md. Exact report/fix digests: handoff-manifest.json entries qa-report.md and qa-fix.md.
- Candidate: C:\Projects\DevForgeAI\devforgeai; C:/Projects/DevForgeAI/docs/plan/index-service-qa/20260914T184442947070Z/executions/20260914T191133863776Z/source-manifest.json, SHA25643b63b5a9496b9d5374996d274cf5b852e2301ba23a87490717c786f71790343. Fresh binaries in runtime-artifacts.json and ubuntu/completion.json.
- Governing spec: C:\Projects\DevForgeAI\docs\plan\devforgeai-index-service-mvp-spec.md, SHA25652d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4; AGENTS.md/QA floors bound by inputs.json.
- Project/environment: Windows11 x64 native checkout; Ubuntu26.04.1 SSH source-equivalent candidate at /home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai. Do not substitute remote spec or synchronize source silently.
- Remediation owner: dev. Selected confirmed defects: **QA-D01, QA-D02**. Repair is proposed for the user's next selected dev invocation; QA does not modify product code.
- Proposed scope: devforgeai/src and meaningful developer tests supporting confirmed fixes. Preserve unrelated source, original QA artifacts/oracles and all prior attempts. No installation, deployment, startup/systemd change, WSL wake, operational skill edit or framework acceptance.

## QA-D01 — Required tray provenance fields absent

- Violated requirement: selected specification DS-025, line 219 (use bound exact passage in plan criteria.json if line numbers drift): compact management window includes last reconciliation and current generation.
- Severity: P1 mandatory conformance failure. The user cannot see which committed generation/reconciliation the displayed index status describes.
- Verified implementation: devforgeai/src/tray.rs status_text (starts line 10); devforgeai/src/tray_windows.rs line 314 assigns status_text to native STATUS control. The renderer never reads current_generation or last_reconciliation. Service index.status supplies both (service.rs lines 429–430).
- Environment: Windows11 x64 Rust1.97.1; shared Rust renderer also executed on Ubuntu26.04.1 Rust1.93.1. No Linux tray requirement inferred.
- Fixture: qa_independent-coverage-v1.rs.txt, SHA25645e078b8aaba9d37e1a49d3163a238232e9cdf20260d7a9b0c39fecaeb4c9ce1; project p, generation GEN-QA-417, reconciliation1777777777 versus null. Required observations independently encoded before execution.
- Reproduction actually executed: isolated Windows/Ubuntu candidate copies contain the12 independent tests as tests/qa_independent.rs. Exact full coverage/test argv/cwd/env in attempts/coverage-002/receipt.json and ubuntu/attempts/coverage-002/receipt.json. qa_u06_tray_displays_current_generation and qa_u07_tray_displays_last_reconciliation both FAIL in each raw stdout.
- Focused reproduction for a later dev/retest invocation: from the selected isolated candidate after verifying fixture bytes, run `cargo test --locked --offline --test qa_independent qa_u06_tray_displays_current_generation -- --exact` and corresponding qa_u07_tray_displays_last_reconciliation. These filtered commands are proposed reproductions; this campaign's observed reproduction was the recorded full suite.
- Expected: actual current generation displayed; known reconciliation distinguishable from absent and represented clearly. Do not hardcode fixture strings; render actual service status.
- Actual: generation string absent; rendered text identical whether last_reconciliation is1777777777 or null. The [native screenshot](attempts/coverage-002/gui/tray-paused.bmp) shows coverage/freshness/counters with neither field.
- Root cause established for this defect: required response fields are omitted by status_text; call-site inspection and native screenshot connect formatter output to actual window.
- Required correction: display both fields, handle missing/unknown values honestly, preserve current state/counter/error/job rendering, keep native asynchronous behavior.
- Regression: meaningful known/unknown values, changing generations/times and actual native screenshot/readback; no weakened QA assertions or golden-output replacement. Complete appropriate dev red->green->refactor checks.
- QA closure: independently rerun both original oracles and affected native UI/regressions against corrected candidate, retain old failures. State remains OPEN until QA verifies.

## QA-D02 — Executed-line coverage below95% on both tested platforms

- Violated criterion: spec section1.4, DS-A19 and AGENTS.md mandatory >=95% executed-line first-party code per platform.
- Severity: P1 quality-floor failure. Windows2626/3442 =76.29285299244624%; Ubuntu2075/2786 =74.47954055994256%.816/711 lines not executed. WSL measurement absent, not0% measured.
- Reproduction actually executed: recorded cargo llvm-cov commands in attempts/coverage-002/receipt.json and ubuntu/attempts/coverage-002/receipt.json, with source hashes and native compiler/collector identities. Native raw JSON: coverage.json and ubuntu/coverage.json; metrics.json and uncovered-segments.json retain per-file totals and zero-count segment starts.
- Source denominator: all compiled devforgeai/src Rust behavior including binaries and native adapters. Exclude only tests/example/fixture support and generated/third-party dependencies. No first-party source suppression.
- Largest measured gaps: Windows cli.rs327, service.rs126, tray_windows.rs123, index.rs61, platform.rs61; Ubuntu cli.rs339, service.rs127, platform.rs66, index.rs55, tray.rs55. These are missing executed-line counts, not claims that every unexecuted line is defective.
- Root cause: incomplete meaningful exercise of first-party paths is measured; no single code defect or speculative algorithm is asserted. Details of each uncovered path require dev review.
- Required correction: add specification-aligned positive/negative/recovery tests over uncovered first-party behavior, fix any resulting product defects, and supply native reports >=95% independently. Do not remove uncovered files, add coverage suppressions, count setup tests as conformance, fabricate output or weaken assertions.
- Unit metric: declared component tests16/18 per measured platform (88.88888888888889%), with two failures caused by QA-D01. Fix that behavior; do not pad the denominator. Full required-unit completeness still needs QA review.
- Verification: native source/build-matched reports with integer counts, original exclusions, raw test/coverage output, child profile evidence, meaningful passing required cases and no failed mandatory scenario. Windows success cannot qualify WSL or standalone Linux.
- Dependencies: QA-D01 explains current unit failures; QA-G01..05 remain separate incomplete qualification work.

## Return contract and pending work

Return corrected source/build identity, changed-file manifest, each defect's repair/evidence references, red/green/refactor and regressions, raw coverage/unit counts with unchanged honest denominator, and platform/compatibility gaps. No self-issued QA closure. Preserve original tests/fixtures/evidence; only independent QA retest can mark VERIFIED_FIXED.

Pending gaps: unavailable WSL, explicitly excluded startup/systemd, alternate-principal and deterministic race/crash/overflow/full UI cases, incomplete benchmark CPU/RAM/idle/content-query metrics, complete integrity and historical TDD evidence review. These gaps are not fabricated confirmed product defects or permission to broaden effects.

## End-user invocation

The host skill catalog lists dev. Open C:\Projects\DevForgeAI on native Windows. Paste the complete prompt in dev-handoff.md; artifact identities are bound in handoff-manifest.json. Do not auto-send or invoke this handoff.
