# Documents Updater evaluations

Eight imported cases cover SPEC-006 VER-01 through VER-08. The Codex generator is
`tests/make_documents_updater_evals.py` relative to the plugin root. Edit fixtures
and graders there and regenerate; do not edit generated cases directly. Claude source
fixtures and evaluation records remain unchanged.

## Run locally

From the repository root, with Python 3.11+, PyYAML for grading, and an already
authenticated Codex CLI:

```bash
python3 -B src/codex/devforgeai/tests/make_documents_updater_evals.py
python3 -B -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py' -v
python3 -B src/codex/devforgeai/tests/native_documents_updater_eval.py \
  --evidence /absolute/path/to/fresh-evidence --stage smoke --jobs 2
python3 -B src/codex/devforgeai/tests/native_documents_updater_eval.py \
  --evidence /absolute/path/to/fresh-evidence --stage matrix --jobs 4
python3 -B src/codex/devforgeai/tests/grade_documents_updater_eval.py \
  /absolute/path/to/fresh-evidence --stage matrix
```

The smoke stage runs two plugin trials; the matrix freezes 48 trials: eight cases,
three repeats, plugin and no-plugin arms. Reusing an existing stage is refused.
Failures and incomplete runs remain in the denominator. Native trials consume the
signed-in account's Codex allowance.

## What is measured

The driver starts ephemeral app-server threads and loads the candidate through
`skills/extraRoots/set`. It records the native catalog, prompts, complete protocol
stream, model identity, outputs, file hashes, and Git index/HEAD/ref states. Every
trial uses a unique temporary parent. Other skills, plugins, MCP servers and memories
are disabled for these child processes. No global configuration is changed.

Source regex and file-existence graders retain their meaning. Claude's
`tool_used: Skill` is replaced by observed reads of the candidate's SKILL.md.
Activation is a separate gate and does not inflate or depress baseline content scores.
The semantic unknown-baseline grader stays REVIEW_REQUIRED until a reviewer records
an evidence-backed assessment. A native question counts as visible output but is
retained separately from the final reply.

The source threshold is 0.8 per case on each of three runs. Reports also count fully
passing trials and every failed obligation: a threshold score never waives a failure.
Additional guards check exact file preservation in proposal/no-change cases, code and
Git-state preservation, and actual execution of the bundled checker.

## Recorded result

The 2026-09-28 Codex 0.158.0 run completed 48/48 trials. All 24 plugin trials
passed the source checks and preservation guards; 5/24 baseline trials did. Mean
content scores were 1.000 with the plugin and 0.690 without it. The 23 checker tests
and three supplemental native checks passed. VER-10–12 remain NOT_RUN.

After recording semantic assessments, summarize a complete matrix with
`python3 -B src/codex/devforgeai/tests/summarize_documents_updater_eval.py <evidence>`
from the repository root. It refuses missing trials and unreviewed semantic grades.

## Limits

These tests load skill source through the native Codex runtime; they do not exercise
marketplace installation or desktop selection. Temporary folders are isolated from
other trial folders, but this is not an OS-hermetic sandbox.

VER-09 is the checker unit suite. VER-10 through VER-12 require owner manual evidence
from real work sessions and the deployed skill; controlled supplemental cases cannot
replace them. See the [import report](../../DOCUMENTS-UPDATER-IMPORT-REPORT.md) for
the retained run results and discrepancies.
