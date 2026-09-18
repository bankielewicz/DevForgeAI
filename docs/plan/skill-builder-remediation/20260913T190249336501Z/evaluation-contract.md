# Maintenance evaluation contract

Target is the development builder package; these tests are separate evidence resources, not a builder runtime permission to validate authored skills. `run_evaluation.py` executes `test_remediation.py` unittest assertions and emits one JSONL result per declared case. `evaluation-result.schema.json` defines rows. `expected-results.json` is written before execution. Fixtures are retained under trials/<attempt>; per-case pre/post manifests under trials/<attempt>/receipts. Failed setup is ERROR and cannot serve as red evidence.

Runtime: Python 3.10+ standard library; builder metadata checks additionally require existing PyYAML. Measurement requires installed coverage.py. Observed Windows environment: Python 3.10.11, coverage.py 7.9.0, PyYAML 6.0.2. No dependencies installed. Full environment/command identities are retained separately. Linux execution and its coverage are independently reported.

Reproduction from project root (use a fresh attempt each time):

```text
python -B -X utf8 docs/plan/skill-builder-remediation/20260913T190249336501Z/run_evaluation.py --attempt fresh-label
```

The `Regression` assertions are deterministic graders for record rejection, valid legacy compatibility, staging/target preservation, and excluded-file no-read behavior. Source helper observations are not complete native BAT outcomes. Every result binds the current package digest. The final artifact manifest binds runner, graders, schema, expected results, fixture receipts and output bytes; no self-referential manifest is used.

Historical tests copied into regression-01 are maintenance regressions with original source digests retained. They are not represented as a new independent audit. Final independent audit has separate ownership, fixtures, oracles and reports.
