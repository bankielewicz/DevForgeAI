# Independent adaptive contract checks

Final selected test file: `src/agents/skills/skill-validator/tests/test_postmvp_adaptive_quality.py`.

Command: `python -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests -p test_postmvp_adaptive_quality.py -v`.

Final observed result: 28 tests passed in 5.471 seconds (`attempt-007.log`). No production files or pre-existing tests were changed. These checks are supporting Python evidence, not full framework acceptance or native skill behavior qualification.

Independent assertions cover exact membership, changed-destination authorization, lineage dispositions, dependency failure propagation, descriptor and binding identities, late evidence drift, malformed authoring records, entrypoint JSON status/exit behavior, readback, capture limits, byte/token measurement boundaries, raw Unicode adjudication boundaries and invalid logical dimensions. Fixtures use real temporary files and no mocks or decorators.

Retained attempts:

- `attempt-001.log`: first 10 tests passed.
- `attempt-002.log`: 14 passed and one fixture setup error; Windows Path ordering disagreed with the contract's serialized string manifest ordering. Fixture rows were explicitly sorted by serialized path.
- `attempt-003.log`: expanded 15 tests passed.
- `attempt-004.log`: 18 passed and one incorrect test expectation; raw unresolved Unicode correctly produces INCOMPLETE, not OBSERVED. Assertion corrected to preserve the semantic-review boundary.
- `attempt-005.log`: 19 tests passed.
- `attempt-006.log`: 22 tests passed, adding complete authored custody chains and set assessment reduction/linkage checks.
- `attempt-007.log`: final 28 tests passed, adding aggregate capture limits, pending observation integrity, wrong input families, schema-family routing, parent inventory boundaries and prior-proposal drift.

No production defect was confirmed. `coverage.json` and `coverage-run.log` describe the earlier 15-test revision only and must not be cited as coverage of the final frozen test file. Aggregate final coverage belongs to the parent run's fresh full-suite measurement.
