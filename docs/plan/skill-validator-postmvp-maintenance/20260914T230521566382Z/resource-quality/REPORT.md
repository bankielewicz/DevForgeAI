# Independent resource and record QA

Scope: SVE-02, SVE-03 and SVE-07 helper observations using real synthetic files. Added only `src/agents/skills/skill-validator/tests/test_postmvp_resource_quality.py`; no production files or existing tests modified by this reviewer. This is supporting-code QA, not native model-scenario or protected framework acceptance.

## Executed results

- Attempt 001: 24/24 tests passed, 0.599 seconds. Initial metadata, resources, malformed manifests/records and readback tests.
- Attempt 002: 24 passed, 1 failed, 0.633 seconds. Added independent quoted-inline-link oracle and reproduced RQ-01 before production repair.
- Attempt 003: 32/32 tests passed, 0.715 seconds, process exit 0. Includes unchanged RQ-01 oracle after parent agent's repair and additional record/assessment cases.

Command: `python -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests -p test_postmvp_resource_quality.py -v`. Executed from `C:\Projects\DevForgeAI` with native Windows Python. Streams retained in distinct `attempt-001.txt`, `attempt-002.txt`, and `attempt-003.txt`; attempt 001 shell pipeline did not explicitly propagate Python status, but unittest's retained output reports OK. Later commands explicitly exit with `$LASTEXITCODE`.

## RQ-01: quoted Markdown example falsely fails structure

Fixture body contains `Describe the Markdown syntax \`[label](not-an-actual-resource.md)\` to the user.` A code span is example text, not an active Markdown resource. Before repair, `observe.structure` returned required `resource_link: FAIL`, status MISMATCH and exit 1. The package text-resource checker already handled this example correctly. The discrepancy violated SVE-03's quoted-example requirement.

The parent agent repaired production code. The original independent oracle passed unchanged in attempt 003. All 32 tests passed together. RQ-01 is resolved for this fixture; broader complete-package coverage remains the parent agent's responsibility.

## Test design and limits

Assertions derive from supported metadata types, strict schema/identity validation, immutable byte readback, Markdown example versus live-link meaning, unknown applicability, and review-readiness prerequisites. Tests use temporary directories and actual byte content, with no mocking decorators or target-script execution. They check meaningful diagnostics and output fields, including invalid YAML, nested duplicate keys, optional configuration, resource links/anchors, Unicode secrecy, manifest drift, false completion claims and malformed evidence locators.

No native model trials or coverage measurement were run in this bounded subtask. Full-suite and measured coverage qualification are separate obligations. Historical failures and attempts remain preserved.
