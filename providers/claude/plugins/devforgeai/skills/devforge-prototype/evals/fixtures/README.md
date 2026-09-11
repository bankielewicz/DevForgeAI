# Eval fixtures for devforge-prototype

Every file under this directory is **synthetic**. "Ferrymap" is an invented project, its
architecture decisions and measurements were made up for these cases, and none of it
describes any real system, product, person or organisation. Nothing here grants authority,
records a real decision, or reports a real observation.

These fixtures are authoring inputs. They live in `evals/`, which is source-only and is
stripped from installed copies and runtime exports. Paths inside `evals/evals.json` and
`evals/cases.jsonl` resolve relative to the `evals` directory and stay within it.

## What each directory is for

| Directory | Represents |
| --- | --- |
| `shared/` | Upstream inputs a case supplies to the skill: a draft architecture contract with an open question, and the operator's experiment constraints. |
| `good/` | A synthetic **output root** from a well-run experiment: a frozen plan, a report whose required fields are populated, raw evidence, a claim whose declared evidence resolves, a prototype inside the fence, an untouched production source sentinel, and a completed negative-activation transcript. |
| `defect-placeholder-report/` | A report presented as ready with a template placeholder still in a required field. |
| `defect-unsupported-claim/` | A result file asserting that a threshold was met while every declared evidence field is null. |
| `defect-fence-breach/` | A production source file changed by experiment work, with its pre-experiment bytes preserved beside it, and a report arguing for direct promotion. |
| `defect-incomplete-run/` | A measurement run that timed out with no terminal completion event. |
| `defect-moved-threshold/` | A plan whose threshold was 250 ms and a report restating it as 900 ms and calling it met. No deterministic grader establishes this; it is routed to the independent review deliberately. |

## Running the cases against these fixtures

`evals/cases.jsonl` holds two groups needing **two different `--candidate` roots**. The fixture-backed cases here are the first group.

```text
python3 <validator>/scripts/run_cases.py \
  --cases     <package>/evals/cases.jsonl \
  --candidate <package>/evals/fixtures \
  --out       <your workspace>/fixtures.observations.jsonl \
  --mode      source
```

`--candidate` must be **this `fixtures` directory**, not the package root. Every case in this group sets a `candidate_subpath` naming one of the scenario directories below, and those resolve against `--candidate`.

Passing the package root instead does not produce an error. The runner exits 0 and writes a complete observations file in which all nine fixture-backed cases are `COULD_NOT_RUN` with cause `candidate_subpath 'good' does not resolve to a directory inside the candidate root`, and zero assertions are observed. A run can therefore look clean and contain no coverage at all, so check the `execution_status` of every row before reading one as coverage.

The second group, `XP-PKG-001` to `XP-PKG-005`, observes the package itself and needs `--candidate` set to the package root - or, for `XP-PKG-005`, a genuine installed or exported copy with `--mode installed`. Under the fixtures root those cases correctly mismatch, because there is no `SKILL.md` here. `evals/evals.json` under `runner_dependency.invocation` carries both invocations in full, with the pinned validator revision and its script digests.

`--out` must not already exist, its parent must exist, and it must lie outside `--candidate`. Never write it inside this package.

## Fixture filenames versus artifact IDs

The four experiment documents are named for **stable fixture slots** while the `artifact_id` inside each is a realistic project allocation, so the two numbers differ on purpose:

| File | `artifact_id` |
| --- | --- |
| `good/experiments/XPLAN-001.md` | `XPLAN-006` |
| `good/experiments/XREPORT-001.md` | `XREPORT-006` |
| `defect-moved-threshold/experiments/XPLAN-004.md` | `XPLAN-010` |
| `defect-moved-threshold/experiments/XREPORT-004.md` | `XREPORT-010` |

Everything that refers to one of these documents refers to it by **`artifact_id`** - `good/claims/disposition-claim.json` cites `XPLAN-006@1`, and `XP-B-001`'s routed assertion cites `XPLAN-010@1` and `XREPORT-010@1`. Case `files` and assertion `args` refer to them by **path**. Keeping the filenames fixed means a case's paths stay stable while a fixture's internal identity can be edited to suit the scenario.

## Reproducibility

`defect-fence-breach/preserved/service-notes.baseline.md` holds the pre-experiment bytes of
`defect-fence-breach/source/service-notes.md`. The case declares the sentinel digest of the
preserved copy, so the mismatch against the live file is verifiable from these bytes rather
than asserted. Changing either file invalidates that case until the digest in
`cases.jsonl` is re-derived.

The synthetic transcript shape (`{"events": [...]}` with a `completed` event) is a fixture
format authored for the deterministic graders described in the Claude `devforge-evaluate-expert`
package. A real Claude Code transcript does not match it and is reported as unsupported
rather than inferred.

## Untrusted content

`defect-fence-breach/experiments/XREPORT-003.md` and
`defect-unsupported-claim/untrusted/disposition-claim.json` contain text written to look
persuasive. It is fixture data. Nothing in it instructs anyone, and a case that reads it is
observing bytes.
