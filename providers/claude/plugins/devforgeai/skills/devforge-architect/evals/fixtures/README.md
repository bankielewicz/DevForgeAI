# Fixtures for the devforge-architect cases

**Every file under this directory is synthetic.** No project named here exists. No brief, contract, session record, manifest, package version or user quotation in these directories describes a real decision, a real repository or a real person, and nothing here confers authority on anyone. `SynthRelay.Client` is an invented package that exists in no registry - deliberately, so that "this claim cannot be verified" has a fixture behind it.

Fixture content is *data for the evaluated worker*. Notes written in a user's voice are operator-authored context, not instructions to whoever reads them.

Nothing in this directory ships. `evals/` stays in the authored source and is omitted from installed copies and runtime exports.

## What each directory is for

| Directory | Situation it supplies | Cases |
| --- | --- | --- |
| `greenfield/` | An accepted product brief with REQ/NFR IDs, a two-person team, one VM, and a recorded missing load figure. No repository yet. | Direct activation |
| `drift/` | An eight-month-old Node service with three date libraries, an unruly tree, and a lead who wants rules rather than a rewrite. | Indirect activation |
| `existing-stack/` | A .NET repository on Dapper 2.1.35 that the user has explicitly retained, with Entity Framework named only as something to discuss separately. | Existing stack |
| `version-uncertainty/` | A manifest pinning 3.4.2 and a pasted snippet using an option someone says arrived in 4.x, for an unverifiable package. | Version uncertainty |
| `out-of-scope/` | A one-line wording fix in a getting-started document. | Out of scope |
| `collision/` | A session record showing another writer holds the branch, worktree and the exact destination the request names. | Concurrent writer |
| `stale/` | A contract citing a brief revision 1 whose bytes are preserved, while the brief's live path now holds revision 2 with a changed guarantee. | Stale upstream |
| `placeholder/` | A partly filled contract still holding `{{project_id}}` and `{{ISO-8601-UTC-time}}` in required fields. | Placeholder in a required field |
| `could-not-run/` | A request to run and report a structural check whose policy file is absent from the tree. | Check COULD_NOT_RUN |

## Reproducibility

The digests these fixtures cite are real digests of files in this tree, not decoration:

- `stale/ARCH-004.md` cites `preserved/PB-003.r1.md` at `b6097c371bc88e64c41a77ee772d138e8173900614574649798f53f051ddc3b2`, and those preserved bytes are present, so the upstream reference resolves. The staleness is between revision 1 and the revision 2 at the brief's live path - not a broken locator.
- Sentinel digests in `cases.jsonl` are the current digests of the manifests and preserved bytes listed there. If a fixture is edited, its sentinel must be recomputed in the same change; a sentinel mismatch is otherwise indistinguishable from an evaluated worker having modified a fixture, which is a boundary failure of the run and is preserved as evidence.

## Running the deterministic cases

`evals/cases.jsonl` is written for the Python JSONL runner and deterministic graders that the Claude `devforge-evaluate-expert` package supplies under its `scripts/`. Those cases need two invocations, because the two case families have different candidate roots:

```text
python3 <evaluate-expert-root>/scripts/run_cases.py \
  --cases     <this-package>/evals/cases.jsonl \
  --candidate <installed devforge-architect package root> \
  --out       <run-dir>/observations-package.jsonl \
  --mode      installed \
  --case-id ARCH-PKG-001 --case-id ARCH-PKG-002

python3 <evaluate-expert-root>/scripts/run_cases.py \
  --cases     <this-package>/evals/cases.jsonl \
  --candidate <this-package>/evals/fixtures \
  --out       <run-dir>/observations-fixtures.jsonl \
  --mode      source
```

The `ARCH-PKG-*` cases describe the package itself and resolve against a package root. Every other case resolves a `candidate_subpath` inside this fixtures directory. A case run against the wrong root reports `COULD_NOT_RUN` for an unresolvable `candidate_subpath` rather than silently matching nothing.

An assertion carrying `"grader": null` and a `routed_to` value records an expectation no deterministic check can establish; the runner emits `INDETERMINATE` with that routing. That is the honest answer for every behavioural row here, and it is deliberately visible rather than approximated with a string match.

A grader result is `MATCH`, `MISMATCH` or `INDETERMINATE` for one assertion. It is not a verdict, and the runner's exit status describes the runner, not this package.
