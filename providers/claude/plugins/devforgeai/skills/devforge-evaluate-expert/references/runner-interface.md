# The case runner and its graders

`scripts/run_cases.py` executes authored evaluation cases and writes per-case observations. `scripts/graders.py` holds the deterministic assertions it dispatches to. Together they are the framework's permitted Python evaluation artifacts: a JSONL runner and deterministic graders that produce raw outputs and metrics.

Read this before using them, because the thing that makes them permitted is a boundary that is easy to erase by accident.

## What makes this evidence and not a gate

Some grader assertions check facts a structural gate would also check. The difference is role, not subject matter.

| Property | A gate (not implemented here) | These graders |
| --- | --- | --- |
| Where an assertion comes from | A fixed rule catalogue applied to every package | Only a `case_id` in an authored case file. A fact nobody wrote a case for is simply not observed |
| Aggregation | One outcome per rule, then a package-wide `overall`, under a precedence rule | **None.** No `overall`, no coverage summary, no counts, no percentage, anywhere in the output |
| Exit status | Candidate passed / failed / could not run | This program produced complete output / could not / crashed. Never the candidate |
| Vocabulary | `PASS` / `FAIL` / `COULD_NOT_RUN` | `MATCH` / `MISMATCH` / `INDETERMINATE`, deliberately disjoint |
| Downstream use | Permits or refuses a dependent action | Rows you cite while adjudicating separately |
| Effect on the missing capability | Would close it | Does not close it |

Three rules follow, and they are not negotiable:

1. **Never route P2 to the runner as a substitute for structural inspection.** The gap named in [missing DevForge CLI capabilities](missing-rust-capabilities.md) stays in the report even when every row matched.
2. **Never copy a row into a results record as an outcome.** `MATCH` is an observation about one assertion. Whether it supports `PASS` for a required check is your judgement, made against the results contract, and it is recorded as your judgement.
3. **Never read the exit status as a verdict.** Exit 0 means the file was written. It is entirely normal for a run full of `MISMATCH` rows to exit 0.

## Prerequisites

`/usr/bin/python3` 3.12, standard library only. No PyYAML, no third-party package, no package manager. No network, no subprocess, and no import or execution of candidate code. Exactly one file is written, at `--out`; nothing inside the candidate tree is ever written.

Because installation does not preserve executable bits, invoke through the interpreter as shown rather than executing the file directly.

## Interface

```text
python3 <installed-skill-root>/scripts/run_cases.py \
  --cases      /abs/path/cases.jsonl \
  --candidate  /abs/path/candidate-or-output-root \
  --out        /abs/path/run/observations.jsonl \
  [--mode source|installed] \
  [--case-id ID]... \
  [--help]
```

All paths absolute. `--out` must not exist, its parent must exist, and it must lie outside `--candidate`. `--mode` defaults to `source` and affects only assertions in cases that declare a mode. `--case-id` may be repeated to run a subset; unselected cases still appear as `SKIPPED` rows and the header records the selection, so a partial run cannot be mistaken for full coverage.

| Exit | Meaning |
| --- | --- |
| 0 | The program completed and wrote a complete observations file. Says nothing about any assertion. |
| 1 | Invalid invocation or unusable input: unreadable case file, unreadable candidate, malformed JSONL, unknown grader, unknown case id, `--out` that exists or sits inside the candidate. |
| 2 | Unexpected internal error. Never looks like a completed run. |

## Case file

One JSON object per line. Unknown keys and duplicate keys within a line are rejected, as are duplicate `case_id` values.

```text
{"case_id":"EX-C-003","tier":"C","title":"...","prompt":"...",
 "files":["fixtures/good/"],"candidate_subpath":"good/fixture-scope-note",
 "mode":"installed",
 "expectations":{"summary":"the statement this case tests, for a human reader"},
 "assertions":[{"assertion_id":"A1","grader":"path_absent",
                "args":{"path":"evals"},"expect":"absent"}]}
```

`files` paths resolve relative to the `evals` directory and stay within it. `candidate_subpath` selects a subtree of `--candidate` for this case. `expectations.summary` is for people; no grader reads it. An assertion with `"grader": null` and a `routed_to` value records an expectation that no deterministic check can establish - the runner emits `INDETERMINATE` with the routing, which is the honest answer and is deliberately visible.

## Observations file

JSONL: one header record, then one record per case. There is no aggregate record.

The header carries `schema_version`, `created_at_utc`, `python_version`, `runner_identity`, `grader_identity`, `case_file` (each with a path and sha256), `candidate_root`, `mode`, `case_selection`, `case_count`, an `authority` string and a `custody_note`.

Those identities are **self-reported by the run**. That is why the custody note is there: a protected manifest binding them outside evaluated-agent write access is the second missing CLI capability, and a file describing itself is not that manifest.

Each case record carries `case_id`, `tier`, `execution_status` (`COMPLETED`, `COULD_NOT_RUN` or `SKIPPED`), an optional `cause`, an `assertions` list and `metrics` (`files_read`, `bytes_read`, `duration_ms`). Each assertion carries `assertion_id`, `grader`, `result`, `observed`, `reason` and an optional `evidence` locator.

## The graders

| Grader | Establishes | Boundary it holds |
| --- | --- | --- |
| `frontmatter_present` | Opening and closing `---` delimiters | A missing closing delimiter is `MISMATCH`, not a crash |
| `frontmatter_fields` | Required fields are populated scalars | **Restricted parser, no PyYAML.** Duplicate top-level key is `MISMATCH`; block scalars, nested maps, flow collections, anchors and merge keys are `INDETERMINATE` with the reason. It never guesses a value and never invents a defect it cannot establish |
| `name_folder_relation` | The frontmatter `name` and the folder name | Records both. Asserts equality only when the case sets `expect_equal`, because Claude's own naming rules make a difference legitimate |
| `package_relative_links` | Local Markdown destinations resolve inside the package | Supported subset only: inline links without nesting, entities or HTML. Anything outside it is `INDETERMINATE` per link, with the line number. External URLs are counted, never fetched |
| `path_present` / `path_absent` | A package-relative path exists or does not | Used for `evals` absence in installed mode and for referenced resources |
| `required_report_fields` | Named fields are present and populated | A field still holding a `{{placeholder}}` is `MISMATCH`, not a match |
| `claim_evidence_binding` | A self-reported outcome **and**, separately, whether its declared evidence resolves and hashes | Emits two facts. A file claiming `PASS` with null manifest, null transcript and empty evidence yields `observed: claimed='PASS' evidence=none` and `MISMATCH`. The claim is never adopted as the result |
| `transcript_completion` | A terminal completion event in the synthetic transcript shape, and whether a named target was consulted | No terminal completion sets the case to `COULD_NOT_RUN`; a negative-activation assertion can never match on an incomplete transcript. A real client transcript does not match this fixture shape and is `INDETERMINATE`, not an inference |
| `artifact_side_effect` | Declared sentinels still hash as expected; forbidden strings absent from a named artifact | Observes bytes. It does **not** judge whether a model resisted an embedded instruction - that reading is criterion R06 |

## Limits worth stating in a report

- The frontmatter reader covers a restricted top-level scalar subset. Real YAML that exceeds it returns `INDETERMINATE`, which is a gap in the observation, not a property of the candidate.
- The link parser is not a CommonMark renderer. Reference-style links, entity-encoded destinations and HTML attributes are reported as unsupported representations needing manual inspection.
- The transcript shape is a fixture format authored for these graders. It tests the grader; it is not native evidence, and synthetic transcripts never substitute for an observed run.
- Metrics are bounded reads of this program, not measurements of a client session.
- Nothing here observes discovery, activation, loading or output quality. Those are tiers A, B and C in [native evaluation](native-evaluation.md).

## Exercising the graders before trusting them

The fixtures under `evals/fixtures/` exist so a grader's classification can be checked against a known answer before it is used on a real candidate - a conforming package, one defect per directory, and two semantic defects that deliberately have no deterministic assertion at all. Running the authored cases against them is how you establish that the graders discriminate, and it is a test of the graders rather than an evaluation of anything.
