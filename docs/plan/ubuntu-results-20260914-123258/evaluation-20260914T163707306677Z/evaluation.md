# Standalone Ubuntu evidence evaluation

Result: **FAIL against the coverage requirement; full qualification remains incomplete.** This is an evidence review, not protected Rust-framework acceptance or a completed independent anti-gaming audit.

The received files establish execution on Ubuntu 26.04.1 LTS, VMware host me-VMware-Virtual-Platform, Linux 7.0.0-31-generic x86_64. Rust 1.93.1 uses LLVM 21.1.8; cargo-llvm-cov is 0.9.1. Standalone Ubuntu is now tested at this release. The repository owner explicitly replaced the standalone Ubuntu 24.04 target with Ubuntu 26.04.1 LTS on 2026-09-14. This campaign now matches the required standalone target. Windows and Ubuntu 24.04 WSL2 requirements remain unchanged.

| Check | Result |
| --- | --- |
| Source identity | All 48 files in the corrected manifest match the packaged candidate and current local application bytes. Bundle check reports 365 files OK. |
| Release build, formatting, Clippy | PASS: each command exited 0. |
| Regression | 36/36 raw cases passed, none failed or ignored. Includes one trivial setup-only assertion; 35 non-setup cases passed. |
| Coverage run tests | Same 36 unique cases passed; repeated execution adds no required-case credit. |
| Executed-line coverage | FAIL: 2066/2786 = 74.1564967695621%; required >=95%. Coverage command exited 1 after successfully writing its report. |
| Branch coverage | NOT_RUN: branch instrumentation absent. Zero branch entries do not constitute measured coverage. |
| Detailed required-case pass rate | NOT_ESTABLISHED. Implemented regression success does not cover all required acceptance subchecks. |
| Benchmark | Three release repetitions completed, fixture digest verified; external time/RSS observations retained. |
| Manual scenarios / formal independent QA | INCOMPLETE / PENDING. No exported playbook observations or complete manual evidence supplied. |

## Coverage remediation evidence

Denominator: 13 first-party executable source files compiled for Linux, including the Linux unsupported-tray entry path. Tests, examples, fixtures and dependencies were excluded by the recorded command; no further source exclusions were introduced in this review.

| Source | Covered / executable lines | Percent |
| --- | ---: | ---: |
| src/bin/devforgeai-indexd.rs | 13/14 | 92.85714285714286% |
| src/bin/devforgeai-tray.rs | 0/6 | 0.0% |
| src/bin/devforgeai.rs | 5/5 | 100.0% |
| src/cli.rs | 222/561 | 39.57219251336899% |
| src/client.rs | 59/83 | 71.08433734939759% |
| src/host.rs | 71/84 | 84.52380952380952% |
| src/index.rs | 430/490 | 87.75510204081633% |
| src/platform.rs | 105/171 | 61.40350877192983% |
| src/protocol.rs | 172/172 | 100.0% |
| src/service.rs | 659/786 | 83.84223918575063% |
| src/source_file.rs | 52/56 | 92.85714285714286% |
| src/storage.rs | 208/229 | 90.82969432314411% |
| src/tray.rs | 70/129 | 54.263565891472865% |

The CLI has 339 uncovered lines, service 127, platform 66, index 60 and shared tray logic 59. These are priorities for requirement-based tests and implementation review, not permission to exclude code or add vacuous assertions.

## Test integrity and scenario limits

The source still contains tests/harness.rs with only size_of::<u32>() == 4. It is setup evidence only and must receive no product-required-case credit. A scoped search found no mock decorators or coverage-bypass attributes in application source/tests/examples. This does not finish the required anti-gaming audit or prove every oracle is independent. The two Windows-only ignored WSL tests are not compiled on this Linux target and their scenarios receive no standalone Linux pass credit.

DS-A01 was run twice; both attempts remain retained, counted once when considering its supporting test. DS-A07 and DS-A15 reuse the protocol tests; DS-A02 and DS-A17 reuse one lifecycle test. Those repetitions are not additional unique passing cases. Every copied test command executed at least one test, but focused support does not qualify the whole scenario. In particular DS-A04 does not prove an OS crash at commit; DS-A07 lacks cross-account denial; DS-A11 lacks overflow and full convergence evidence; DS-A16's portable preferences test does not prove Linux systemd installation; DS-A18's fixture test alone is not a benchmark, although a separate benchmark was subsequently run. DS-A05 and DS-A06 are Windows-controller scenarios, NOT_APPLICABLE for this standalone campaign.

The user encountered two playbook usability defects: a missing rg produced a partial manifest without stopping preparation, and copy buttons supplied explanatory prose as executable commands for Windows-only scenarios. Preserve these as playbook defects; the resulting shell errors are not product runtime failures. They were shown in conversation, not captured by run_case. The initial 3-file manifest is retained. The corrected manifest and bundle verification were recorded after build/initial DS-A01 but before later tests. No final after-campaign source manifest or remote evidence-file checksum inventory was supplied; this review hashes received bytes and does not claim end-to-end remote attestation.

## Benchmark observations

| Repetition | Cold ms | Warm ms | 100-file edit ms | Status p95 microseconds |
| --- | ---: | ---: | ---: | ---: |
| 1 | 11125 | 2598 | 3030 | 726 |
| 2 | 11408 | 2620 | 2951 | 566 |
| 3 | 11016 | 2593 | 2963 | 725 |

Fixture: 10,000 files / 104,857,600 bytes, seed 20260913, four concurrent management-status readers, 10,000 text and 8,000 structural files in each repetition. GNU time reports 38.39 seconds user CPU, 14.49 seconds system CPU, 54.44 seconds wall time and 52,988 KiB maximum resident set size. The example's internal NOT_MEASURED resource field is supplemented by these external measurements. CPU model, total assigned VM RAM and sustained idle CPU are not supplied. This is management-status concurrency, not the companion code-query workload. It does not fully qualify DS-A18 or establish a cross-platform speed comparison.

## Disposition

Retain all submitted artifacts unchanged. Return the candidate for coverage and test-quality remediation; review missing behavior against the selected specification through red/green/refactor and fresh per-platform QA. No rerun of this unchanged candidate can be presumed to satisfy 95%. Apply the owner-authorized standalone Ubuntu 26.04.1 target; no separate standalone Ubuntu 24.04 run is required for this revised contract. The per-attempt ledger and received-file SHA-256 inventory are in evaluation.json.
