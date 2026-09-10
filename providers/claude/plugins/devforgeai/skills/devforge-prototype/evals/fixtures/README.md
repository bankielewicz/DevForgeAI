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
