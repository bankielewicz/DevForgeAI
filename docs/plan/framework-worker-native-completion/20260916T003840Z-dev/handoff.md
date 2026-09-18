# Independent QA retest handoff

The user explicitly selected this repair followed by a fresh independent retest. This handoff releases the frozen candidate for the selected QA-F-COV-01 offline retest; no further user confirmation is required.

- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Evidence: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T003840Z-dev`.
- Manifest: `candidate-manifest.json`, SHA-256 `c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e`, 53 files; compare live bytes and `candidate-snapshot/`.
- Contracts: the three exact paths/hashes in `inputs-manifest.json`; preserve all nine bound inputs.
- Baseline failure: original `...framework-worker-native-completion-qa\20260915T2325371896643Z\qa-report.md`; selected repair packet `...framework-worker-native-completion\20260916T000205Z-resume-audit\qa-fix.md` and `dev-invocation.md`.
- Defect resolution: QA-F-COV-01 is **FIX_REPORTED** only. Original 2,852/3,103; current developer 2,967/3,103 =95.61714469867869803416048985%. Runtime functions and original tests unchanged; 25 new required test functions.
- Required checks: full 114-function suite, 28 unit/86 integration, all WF-01–20/subfixtures, F-01/F-02, exact negative paths, rustfmt, locked/offline Clippy, doctest discovery and complete fresh first-party coverage. Independently declare your denominators before measuring.
- Full source: all `src/**/*.rs`, 12 files; no first-party exclusions. `lib.rs` has declarations and no executed-line records. Branch coverage is separately unmeasured.
- Raw developer records: `full-tests`, `final-fmt`, `final-clippy`, `doc-tests`, `full-coverage`; each includes exact cwd, argv, native exit, duration, streams and pre/post manifests. Raw coverage JSON and profiles are retained.
- Test integrity: examine `candidate.patch`, `developer-integrity-review.md`, all new tests and prior tests. Preserve earlier setup/formatting failures separately; do not inflate pass totals with focused or coverage repetitions.
- Retention: RT-03 creates a synthetic layout-bound fixture under `docs/plan/framework-worker-trials/RT-source-type-*`; bind new instances to exact attempt start/end times and retain their task bytes. All test subprocesses are synthetic peers or compiled local CLI operations.
- Return: independent scope-qualified verdict, QA-F-COV-01 resolution, raw counts/percentages, exact coverage numerator/denominator, source/input readback, integrity findings, required blocked/not-run native status and sealed artifacts.

Use a fresh timestamped directory under `docs/plan/framework-worker-native-completion-qa`. Do not edit candidate, tests, contracts or prior evidence. A valid metric below95%, result manipulation, or confirmed critical security/data-loss defect stops the assignment; preserve and hand back evidence, without another repair/retest loop.

Do not launch Codex, alter operational files/caches or provision acceptance authority. Native source/profile prerequisites remain unresolved. Framework acceptance is NOT_EVALUATED.
