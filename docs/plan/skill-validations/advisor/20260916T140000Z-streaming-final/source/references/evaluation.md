# Evaluation and runtime

Runtime: Python >=3.10, standard library only. The optional run launcher requires Windows PowerShell 5.1 or PowerShell 7. Authoring checks additionally use installed coverage.py (measured authoring version: 7.9.0) and PyYAML for the system skill-creator validator. No installation is performed by this package. Live review requires an authenticated native Claude executable advertising the execution profile in execution.md.

Required build artifacts: JSONL runner and deterministic grader in `evals/run_evaluation.py`, input fixtures with independent expected results in `evals/cases.jsonl`, [case schema](../evals/case.schema.json), request schema, this runtime declaration, tests, and `artifact-manifest.json`. Missing or altered artifacts invalidate prior evidence. The manifest hashes all package files except itself and generated caches; it records the external contract dependency separately without copying it.

Run from the repository root, with a fresh output directory:

```powershell
python -B -X utf8 -m unittest discover -s src/agents/skills/advisor/tests -v
python -B -X utf8 src/agents/skills/advisor/evals/run_evaluation.py --output docs/plan/advisor-evaluation/unique-run
```

On native Windows, also exercise `scripts/advisor.ps1` under both Windows PowerShell 5.1 and PowerShell 7 using a synthetic sibling Python runner. Required launcher cases cover exact argument forwarding for paths with spaces, Unicode and Windows-legal quote characters; default and explicit reasons; progress switch presence; stdout/stderr separation; child exit propagation; and pre-invocation failure exit 2. This test must not invoke Claude or depend on credentials.

The JSONL grader uses exact comparison against fixture expectations, including deterministic stream framing, failed-cost and synthetic environment fixtures. Environment fixtures never read the host environment or contain real credentials. Results retain one record per required fixture, including ERROR/FAIL; retries use new directories and never erase earlier attempts. No live model calls are used by the JSONL corpus. Unit tests use explicit simulated CLI results to exercise failures; subprocess tests separately execute real local Python child processes for safe progress, stream concurrency, timeout/cleanup observations, key exclusion/inheritance and parent preservation. Neither establishes live Claude confinement, detached process-tree cleanup, or reasoning quality.

Python coverage denominator: all first-party executable `.py` files in `scripts/` and `evals/`, including the streaming transport module. Exclude tests and fixtures only. Required baseline >=95% executed-line coverage; report branch coverage separately. The PowerShell launcher has a separate native executable case denominator under each required PowerShell runtime. Report PowerShell line coverage when a suitable collector is already available; otherwise report it as NOT_RUN and do not present the Python percentage as package-wide executed-line coverage. Required-case pass rate is >=95%, counting every declared Python, JSONL and launcher case once per required runtime, including skips/errors/unexecuted cases. Mandatory negative scenarios must pass independently of numeric floors. Preserve coverage data, machine-readable reports and launcher stdout/stderr/exit receipts in a new evidence directory.

Native qualification is separate: validate read access using a synthetic repository, contract delivery, supported model/effort, failure reporting, denied mutations/out-of-root reads, timeout recovery, progress rendering, and actual Codex skill routing. A successful single review qualifies only that exercised scenario. A native test's all-UNVERIFIED or unsupported output is a limitation, never a passing review. Preserve every native attempt and count its budget independently from deterministic tests. Do not send real repository content merely to validate installation.

All outputs are supporting evidence. Python cannot authorize mutations, waive gates, advance framework phases, or issue framework acceptance. Report source authoring, deterministic evidence, independent behavioral review, native qualification, installation, and framework acceptance separately.
