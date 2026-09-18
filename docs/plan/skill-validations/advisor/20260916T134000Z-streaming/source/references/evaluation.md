# Evaluation and runtime

Runtime: Python >=3.10, standard library only. Authoring checks additionally use installed coverage.py (measured authoring version: 7.9.0) and PyYAML for the system skill-creator validator. No installation is performed by this package. Live review requires an authenticated native Claude executable advertising the execution profile in execution.md.

Required build artifacts: JSONL runner and deterministic grader in `evals/run_evaluation.py`, input fixtures with independent expected results in `evals/cases.jsonl`, [case schema](../evals/case.schema.json), request schema, this runtime declaration, tests, and `artifact-manifest.json`. Missing or altered artifacts invalidate prior evidence. The manifest hashes all package files except itself and generated caches; it records the external contract dependency separately without copying it.

Run from the repository root, with a fresh output directory:

```powershell
python -B -X utf8 -m unittest discover -s src/agents/skills/advisor/tests -v
python -B -X utf8 src/agents/skills/advisor/evals/run_evaluation.py --output docs/plan/advisor-evaluation/unique-run
```

The JSONL grader uses exact comparison against fixture expectations, including synthetic environment fixtures for inherited and subscription modes, absent keys, case variants and unrelated entries. Environment fixtures never read the host environment or contain real credentials. Results retain one record per required fixture, including ERROR/FAIL; retries use new directories and never erase earlier attempts. No mocks or live model calls are used by the JSONL corpus. Unit tests use explicit simulated CLI results to exercise failures; subprocess tests separately execute real local Python child processes to verify key exclusion/inheritance and parent preservation. Neither establishes live Claude confinement or reasoning quality.

Coverage denominator: all first-party executable Python in `scripts/` and `evals/`. Exclude tests and fixtures only. Required baseline >=95% executed-line coverage; report branch coverage separately. Required-case pass rate >=95%, counting every declared case once including skips/errors/unexecuted cases. Mandatory negative scenarios must pass independently of numeric floors. Preserve the coverage data file and machine-readable report in a new evidence directory.

Native qualification is separate: validate read access using a synthetic repository, contract delivery, supported model/effort, failure reporting, denied mutations/out-of-root reads, timeout recovery, and actual Codex skill routing. A successful single review qualifies only that exercised scenario. A native test's all-UNVERIFIED or unsupported output is a limitation, never a passing review. Preserve every native attempt and count its budget independently from deterministic tests. Do not send real repository content merely to validate installation.

All outputs are supporting evidence. Python cannot authorize mutations, waive gates, advance framework phases, or issue framework acceptance. Report source authoring, deterministic evidence, independent behavioral review, native qualification, installation, and framework acceptance separately.
