# Preserved QA setup attempts

## 00-freeze-audit — setup ERROR, no product conclusion

The recorder admitted the exact frozen candidate, but the PowerShell invocation constructed seven `--binding` values as two argv elements (`path`, then `::digest`). `freeze_audit.py` rejected the first malformed binding during argument parsing and exited 2. No candidate behavior ran. Candidate before/after manifests matched and no files changed.

Evidence: `00-freeze-audit/receipt.json`, `stdout.bin` and `stderr.bin`.

## Authorized correction

The QA-owned argv construction was corrected to format each path and digest as one string. The distinct `00a-freeze-audit` attempt then checked all 53 live files, all 53 snapshot files, the candidate manifest and 11 selected input bindings. It exited 0 with no errors. The original setup ERROR remains retained and is not counted as a product case or retry pass.

## Unrecorded policy-oracle discovery invocation

I invoked `independent_policy_oracle.py --help` while discovering its interface. The helper has no argument parser, so it executed the read-only policy check and printed a passing result instead of help. This was not a product test and wrote no files. It is not counted. The same helper is executed through the evidence recorder below; only that recorded attempt supports the QA result.

## 04-policy-oracle — recorder setup ERROR, no product conclusion

The recorder was given a stale Python 3.14 path. It failed while resolving the executable before spawning the oracle, so no product behavior ran and no receipt was produced. The partial directory retains the frozen pre-launch candidate manifest and empty streams. `Get-Command python` resolved the installed interpreter as `C:\Program Files\Python310\python.exe`; the corrected invocation uses distinct label `04a-policy-oracle`.

## 10-coverage-analysis — QA analyzer ERROR, raw product measurement retained

The first QA analyzer required every declared source file to appear in LLVM's file array and exited 1 because `src/lib.rs` was absent. The collector had completed successfully and its raw JSON remained unchanged. Readback established that `src/lib.rs` contains only a crate documentation comment and ten `pub mod <identifier>;` declarations, so LLVM correctly had no executable lines to report for it. The QA-only analyzer was narrowed to accept an omitted declared source only when every nonblank, noncomment line matches that exact module-declaration grammar. It records such a file as 0/0 and does not exclude it. The corrected analysis of the same raw JSON uses label `10a-coverage-analysis`; the product coverage suite was not rerun.

## Artifact-seal shell invocation — setup ERROR, no evidence change

The first direct PowerShell command quoted the Python executable without the call operator, producing a parser error before Python or `seal_manifest.py` ran. No artifact manifest was created or changed by that attempt. The corrected command used PowerShell's `&` call operator and created the final non-circular manifest after all bound report bytes were finalized.

## Artifact-seal external-fixture correction — first manifest bytes unavailable

The first successful seal indexed evidence-root files and coverage profiles but did not index the two retained external synthetic fixture files. I amended the QA-owned seal helper to add explicit external entries and reran it, which overwrote that first manifest before retaining its bytes or digest. This is an evidence-custody limitation; it did not alter product, raw test or raw coverage evidence. The resulting external-aware manifest was verified with zero errors and then preserved byte-for-byte as `artifact-manifest-pre-final.json` (SHA-256 `1a33c5a7e3840f9044aecd2ac7d2d9c7c7687e588786644ed7f098a27876958e`) before this note and the final seal. Its three later-modified referenced documents were reconstructed byte-for-byte under `pre-final-snapshot/` and verified against the digests in that preserved manifest: report `e736bdfb...`, attempt log `9353c494...` and handoff `96e754c2...`. Two preliminary QA-only reconstruction invocations corrected newline handling before all three expected hashes matched; no product or raw-result file was touched. The final manifest includes the preserved pre-final manifest and document snapshot, this disclosure and both external task files.
