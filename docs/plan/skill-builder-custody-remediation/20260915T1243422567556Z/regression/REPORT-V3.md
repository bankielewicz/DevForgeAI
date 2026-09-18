# Windows skill-builder regression and coverage

Final development-source Python regression: **319/319 required cases PASS (100%)**. All-source executed-line coverage: **2202/2302 = 95.65595134666%**. All eight shipped Python modules are measured, including the runtime asset; zero line exclusions. Branch coverage is reported separately below. This is executed maintenance evidence, not framework acceptance, installation, or native skill activation.

## Source and execution

The final three batches bind identical V3 package bytes, and each batch and combination verified source readback. `v3-combined/scope.json` records every source hash. The authoring helper SHA-256 is `76dbd505dfadb88cb15fc12f80584aa46fff7e5d3c67c04c122d7dce8ae415b2`.

Native Windows; PowerShell launched `C:\Program Files\Python310\python.exe` 3.10.11 with `-B -X utf8`; cwd `C:\Projects\DevForgeAI`, Windows C: filesystem. Existing coverage.py 7.9.0, PyYAML 6.0.2, jsonschema 4.24.0. No dependencies were installed.

| Final batch | Required / passed | Wall seconds | Exit |
| --- | --- | --- | --- |
| v3-legacy | 128 / 128 | 21.828 | 0 |
| v3-authoring-fixtures-02 | 133 / 133 | 75.641 | 0 |
| v3-adaptive-stage | 58 / 58 | 61.297 | 0 |

Each batch had a 120-second ceiling. The case sets are disjoint, with no retries or inherited base-case duplicates added to the denominator. `v3-combined/expected.json`, `results.jsonl`, and `independent-grade.json` bind the inventory, observed results, and independent reduction. `result.schema.json` validates each result row. No required cases failed, errored, skipped, or remained unexecuted in the final V3 collection.

## Coverage denominator and missing lines

| Shipped module | Executed / statements | Missing executable lines |
| --- | --- | --- |
| src/agents/skills/skill-builder/assets/adaptive-runtime/check_project_binding.py | 240 / 240 | None |
| src/agents/skills/skill-builder/scripts/adaptive.py | 414 / 431 | 171, 216, 217, 218, 219, 220, 273, 303, 304, 337, 339, 340, 347, 348, 401, 402, 490 |
| src/agents/skills/skill-builder/scripts/authoring.py | 574 / 600 | 69, 171, 220, 232, 234, 303, 313, 316, 330, 333, 336, 338, 341, 343, 373, 379, 381, 390, 393, 486, 487, 501, 513, 585, 586, 605 |
| src/agents/skills/skill-builder/scripts/build_evidence.py | 270 / 285 | 33, 51, 58, 61, 90, 91, 133, 134, 162, 204, 225, 231, 324, 325, 332 |
| src/agents/skills/skill-builder/scripts/custody.py | 352 / 386 | 67, 69, 74, 83, 85, 95, 98, 158, 162, 172, 174, 184, 197, 198, 207, 223, 224, 230, 287, 289, 294, 301, 385, 388, 391, 395, 402, 417, 421, 432, 437, 443, 446, 450 |
| src/agents/skills/skill-builder/scripts/generate_openai_yaml.py | 158 / 165 | 81, 95, 98, 99, 100, 186, 251 |
| src/agents/skills/skill-builder/scripts/init_skill.py | 141 / 142 | 206 |
| src/agents/skills/skill-builder/scripts/record_schema.py | 53 / 53 | None |

Branches: 940/1048 = 89.69465648855%. This separate measure does not replace the required executed-line floor.

## Earlier attempts retained

- qa-01, V1: 286 required cases, 262 passed. 105.844 seconds, no timeout. Coverage instrumentation changed direct-script import semantics; copied tests also initially lacked helper fixture search paths. Three retained assertions needed explicit adaptation for the newly earlier rejection boundary. These were harness/contract mismatches, not evidence of an unaffected product passing.
- qa-02, V1: 120.031-second collection timeout, incomplete coverage finalization. Most observed cases passed after instrumentation corrections. One real recovery-guidance defect remained: changed-origin rejection returned BLOCKED but omitted the required fresh-run instruction. Parent repaired that error message in V2. This failed assertion is retained as red evidence.
- qa-03-stage, V1: 30/30 focused cases passed in 15.735 seconds. This earlier source is not included in the final combined V3 coverage or pass denominator.
- Final V3 batches above re-execute every declared case against final source. No V1 coverage is included.

## Test integrity and limits

Retained historical tests and fixtures remain at their original paths; copied tests, source hashes and adaptations are recorded in retained-test-receipts.json, adaptations.md, each final batch test-snapshot/, scope.json, and retained-fixture-manifest.json. Fixtures are synthetic local trees. Assertions inspect real return values, destinations, byte preservation, stale-history rejection, schema/intake results, and publication readback. Existing Windows-only checks executed on Windows. The optional jsonschema dependency was available; the junction case executed instead of skipping.
Mocks inject explicit filesystem errors, capture limits, or competing-writer changes. They do not replace the acceptance oracle or produce canned passing authoring results. Runtime-original tests execute the actual shipped runtime asset, while the retained adaptive suite separately exercises copied runtime fixtures. No tests assert implementation source text. Diagnostic and output-format assertions supplement observable effects.
The coverage runner wraps genuine CLI execution with coverage_driver.py solely to preserve direct-script sys.path semantics under tracing. It records real command receipts and return codes. Executed-line coverage includes all first-party shipped Python files even when unimported; no uncovered module or line is omitted.
This report establishes Windows deterministic helper coverage and regression only. Linux coverage, native implicit activation, generated-skill outcomes and complete end-to-end workflow qualification are separate evidence owned by the parent task. Operational skill copies and source packages were not edited by this regression task.

## V3 repair and retained fixture corrections

V2 final-combined passed 318/318 with 2201/2299 lines but was superseded by the independently reproduced empty-directory defect. red-prewrite failed because first before_write stage drift left an occupied target despite BLOCKED; V3 defers target creation until after that check. The final V3 inventory includes this additional case, for 319 required cases.

v3-authoring initially passed 131/133: two callback fixtures assumed target creation before the callback. Their retained failures prompted setup corrections that explicitly create the competing destination; all original assertions remain. v3-authoring-fixtures-02 re-executes the entire affected subgroup. The final V3 combination uses v3-legacy, v3-authoring-fixtures-02 and v3-adaptive-stage only; all have identical source hashes. Earlier V1/V2 and failed V3 attempts remain separate.
