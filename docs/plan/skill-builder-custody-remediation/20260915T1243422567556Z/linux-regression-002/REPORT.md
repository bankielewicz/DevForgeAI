# Linux V3 regression and coverage

**319/319 required cases passed (100%). Executed-line coverage: 2202/2302 = 95.65595134665509%.** All eight shipped first-party Python files are included, with zero excluded lines. Branch coverage is 940/1048 = 89.69465648854961%. No final required cases failed, errored, skipped, or remained unexecuted.

The independent archive verification passed. All 47 source-file hashes match the final Windows V3 package and the current development package exactly. This report establishes deterministic helper evidence on Linux; it does not establish native implicit activation, generated-skill behavior, installation, or compiled-Rust framework acceptance.

## Execution platform and custody

WSL Ubuntu; `Linux-6.18.33.2-microsoft-standard-WSL2-x86_64-with-glibc2.39`. Executable `/usr/bin/python3`, Python 3.12.3, coverage.py 7.13.1. Commands used `-B -X utf8`. The suite working directory was `/tmp/devforgeai-regression-v3-same-process-002` on Linux's native `/tmp` filesystem. PowerShell invoked WSL; tests ran as Linux Python processes. Exact argument vectors, times and exits are retained in each process receipt.

Preparation copied a disposable test snapshot from the selected Windows development package and verified every package hash before and after the copy. It preserved the source and operational copies. Test fixtures and coverage collection stayed inside the Linux snapshot; completed artifacts were copied back to this report directory in the same WSL invocation. No dependencies were installed.

| Batch | Required / passed | Wall seconds | Exit |
| --- | --- | --- | --- |
| linux-legacy | 128 / 128 | 2.695813 | 0 |
| linux-authoring | 133 / 133 | 4.702371 | 0 |
| linux-adaptive-stage | 58 / 58 | 8.413150 | 0 |

Each suite subprocess had a 120-second execution ceiling; the outer orchestrator used 150 seconds per command. Every final batch completed below both ceilings. Batches have disjoint expected inventories, so each case is counted once.

## Independent archive checks

`verify_linux_archive.py` exited 0 after archival completed. It checked:

- Every JSONL observation against the result schema; exact expected-case membership and uniqueness; no missing or nonpassing cases.
- The combined inventory and observations against their original batch records.
- Each coverage file against the complete live package Python inventory; no file or line exclusions; totals independently summed from all eight module summaries.
- All 47 source hashes across the three Linux batches, the disposable snapshot receipt, final Windows V3 scope, and the current selected source.
- Each retained test-snapshot hash and all 75 newly constructed Linux fixture files against their preparation manifest.

Results and input hashes: [independent-archive-verification.json](independent-archive-verification.json). Primary evidence: [expected cases](regression/linux-combined/expected.json), [JSONL observations](regression/linux-combined/results.jsonl), [coverage](regression/linux-combined/coverage.json), [source scope](regression/linux-combined/scope.json), and [Linux preparation receipt](regression/linux-snapshot.json).

## Portable fixture adaptations

The Windows-only mixed-separator case became a Linux literal-path case covering native and forward POSIX paths, including Unicode and punctuation. The changed-stage recovery case executes its same origin/contract mutation on POSIX rather than skipping. These are explicit platform counterparts; this report does not claim Windows separator behavior was exercised by Linux. The existing filesystem-link test uses a Linux symlink.

Historical linked records contained absolute Windows paths. The Linux preparation built new synthetic proposal, selection, authored-member and set records at native paths using actual helper execution. The original negative test mutations and assertions remained unchanged. Seventy-five fixture files were hash-verified after collection. This avoids rewriting old evidence or treating rebased stale hashes as valid.

The two V3 before_write fault callbacks explicitly create their competing destination before simulating a writer or unavailable capture; their original state, applied-path, byte-preservation and diagnostic assertions remain intact. The corrected early callback boundary is separately covered by the new no-destination-on-stage-drift test.

## Retained failed harness attempt

The earlier `../linux-campaign-001` invoked preparation and later test launches in separate WSL invocations. Although preparation reported success, the later invocation could not find the `/tmp` launch script: all three commands exited 2 before tests ran. Those receipts and errors are retained as a harness failure with tests NOT_RUN. They are not included in the final pass denominator or coverage.

The final `run_linux_regression.py` kept preparation, three batches, combination, grading and copy-back in one WSL process. All three final batch exits, combination and grading were 0. Independent verification occurred only after the full archive, including fixture inputs, was present. No tests were rerun to produce this report.

## Per-file coverage and remaining unexecuted lines

| File | Covered / statements | Missing executable lines |
| --- | --- | --- |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/assets/adaptive-runtime/check_project_binding.py | 240 / 240 | None |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/scripts/adaptive.py | 414 / 431 | 171, 216, 217, 218, 219, 220, 273, 303, 304, 337, 339, 340, 347, 348, 401, 402, 490 |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/scripts/authoring.py | 574 / 600 | 69, 171, 220, 232, 234, 303, 313, 316, 330, 333, 336, 338, 341, 343, 373, 379, 381, 390, 393, 486, 487, 501, 513, 585, 586, 605 |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/scripts/build_evidence.py | 270 / 285 | 33, 51, 58, 61, 90, 91, 133, 134, 162, 204, 225, 231, 324, 325, 332 |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/scripts/custody.py | 352 / 386 | 67, 69, 74, 83, 85, 95, 98, 158, 162, 172, 174, 184, 197, 198, 207, 223, 224, 230, 287, 289, 294, 301, 385, 388, 391, 395, 402, 417, 421, 432, 437, 443, 446, 450 |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/scripts/generate_openai_yaml.py | 158 / 165 | 81, 95, 98, 99, 100, 186, 251 |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/scripts/init_skill.py | 141 / 142 | 206 |
| devforgeai-regression-v3-same-process-002/src/agents/skills/skill-builder/scripts/record_schema.py | 53 / 53 | None |

The reported line threshold is met despite the remaining listed lines; no exclusions were used. Platform results remain separate from native model-driven acceptance or protected framework decisions.
