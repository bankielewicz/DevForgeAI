# PASS — QA-F-COV-01 remediation and independent retest

**QA-F-COV-01 is VERIFIED_FIXED for the selected Windows x64 offline scope.** Development and fresh independent QA are complete. A preliminary QA artifact-index retention failure is disclosed below; complete historical-index retention is not claimed.

## Candidate and governing contracts

- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Frozen candidate manifest: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T003840Z-dev\candidate-manifest.json`, SHA-256 `c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e`, 53 files.
- Specifications under `C:\Projects\DevForgeAI\docs\specs\framework\runtime\`: `codex-worker-feasibility-v1.md`, `codex-worker-native-readiness-v1.md`, and `codex-worker-preflight-v1.md`. Exact unchanged hashes are bound in both developer and QA inputs manifests.
- Environment: native Windows 10.0.26200 x64, PowerShell 7.6.6, Rust/Cargo 1.97.1, cargo-llvm-cov 0.8.4, default package configuration, locked/offline dependencies. No Git metadata exists; source identity is manifest-bound.

## Remediation and findings

### QA-F-COV-01 — verified fixed

The original independent coverage result was 2,852/3,103 lines, 91.91105381888495%, below the mandatory 95% floor. That original FAIL and raw evidence remain in place.

The repair adds 25 requirement-derived test functions covering profile validation, source inventory bounds, protocol denial/pagination, runner/CLI errors and untrusted review bytes. Runtime function bodies and original assertions are unchanged. The only existing-file edits register a test peer in Cargo and a private test module in `profile_sources.rs`; five test/support files were added. Exact changes are retained in the developer `candidate.patch`.

The developer and independently executed QA collections both measured **2,967/3,103 lines =95.6171446986787%**. The increase is 115 exercised production lines with an unchanged denominator. No first-party behavior was excluded.

### Evidence-retention limitation

During QA sealing, a preliminary root-only artifact index was overwritten while adding the two external synthetic fixture records. Its earlier bytes and digest cannot be recovered. This is an observed custody failure, not a product defect or evidence of altered test results. The final report explicitly records it. Raw candidate, command, test, coverage and fixture evidence remains available and hash-verified.

The later external-aware index and the three subsequently changed document revisions are retained under QA `artifact-manifest-pre-final.json` and `pre-final-snapshot/`. The final manifest verifies 5,541/5,541 entries. This does not restore the missing first index or justify claiming complete index history.

Other retained setup errors involved argument/executable selection, LLVM's omission of module-only `lib.rs`, and root readback's initial external-fixture path check. Their corrections affected evidence helpers only; no product suite was rerun to improve a failing result. Root's original readback script and exact error are retained in this closure directory.

## Independent results

| Check | Result |
| --- | --- |
| Required executable tests | 114/114 — 100% |
| Unit / integration subsets | 28/28 and 86/86 |
| Selected offline requirements matrix | 33/33 |
| Mandatory WF parents / F-01 and F-02 | 20/20 and 2/2; subsets of the suite |
| Added test subset | 25/25 |
| Independent F-02 privacy supplement | 19/19 |
| Locked/offline build, formatting and Clippy | PASS |
| Documentation tests | Discovery passed; zero cases present |
| First-party executed-line coverage | 2,967/3,103 — 95.6171446986787%; no exclusions |
| Branch coverage | NOT_RUN; no instrumented branch denominator |
| Final independent source audit | 53/53 live files, 53/53 snapshot files, 11/11 QA inputs |
| Root final custody audit | 5,539 QA-root files +2 external fixtures, 53 candidate files and 9 developer inputs; zero mismatches |

All 12 source files were declared before collection; 11 have executable lines, and module-only `lib.rs` is recorded as 0/0. The QA raw coverage JSON is SHA-256 `dac80cc9483db8c833d1cc7377af588679da4d96616254004cbd714d24b36850`; 167 raw profiles are retained. Instrumented repetitions and focused runs do not inflate the required-case denominator.

Independent integrity review found no added skips, prohibited mocks, vacuous tests, weakened original assertions, source exclusions or result manipulation. Synthetic peers qualify offline protocol/process behavior only. No unresolved product defect was found in this selected retest.

## Remaining scope and handoff

No further product repair is required for QA-F-COV-01. Changed candidate bytes would require fresh qualification.

Native WN-01/WN-02 remain **0/2, NOT_RUN**, pending the existing installed-source and effective-profile prerequisites. This assignment did not change those inputs or consume native attempts. The previous full-readiness assessment remains 7/12; it was not remeasured as a native campaign here. Linux and tray behavior are outside this Windows worker defect retest.

Protected authority implementation/provisioning remains a separate deferred assignment. **Framework acceptance is NOT_EVALUATED and is not established.** No qualified compiled-Rust authority issued a protected receipt.

## Evidence

- Developer delivery: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T003840Z-dev\delivery.md`; developer artifact manifest SHA-256 `db85dcaea35608c8948568b50c745e70c304682efcc46d35116edd3901939fa5`.
- Independent report: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260916T003840Z-retest\qa-report.md`, SHA-256 `6b989e180f9e85cd475835aff72eb96ab780dffeb76a9352df6a21dd70eb5793`.
- Independent final artifact manifest: same QA root, `artifact-manifest.json`, SHA-256 `404cbff08f72b75402b4f5e11d01e032ea5b2311da006f2a114fd467f1391109`.
- Closure readbacks: this directory's `developer-seal-readback.json`, `independent-qa-readback.json`, `coverage-comparison.json`, and retained readback attempt notes/scripts.

These records are QA/development evidence, not protected framework authority.
