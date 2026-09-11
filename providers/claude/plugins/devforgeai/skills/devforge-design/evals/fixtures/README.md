# Fixtures for devforge-design evaluation

**Every file in this directory is synthetic and operator-authored.** None of it describes a real project, a real user, a real decision, or a real approval. "Havenlist" is an invented neighbourhood tool-lending library that exists only here. The requirement IDs, session records, digests and approvals are fabricated for evaluation and must never be copied into a real project or cited as a precedent.

Fixtures are reproducible from this source directory. They are inputs to authored evaluation cases; they are not runtime resources and are excluded from installed copies and plugin exports.

| Path | Role in the cases |
| --- | --- |
| `shared/PROD-001.md` | A product-brief with stable requirement IDs. The upstream for the direct and indirect activation cases. |
| `shared/ARCH-001.md` | An architecture-contract declaring an approved UI stack and conventions. The scope-preservation case. |
| `backend-only/STORY-021.md` | An accepted story with no user-facing surface. The out-of-scope case. |
| `ownership-collision/SESSION-042.md` | An assignment record naming a different owner as the writer for the design directory. |
| `ownership-collision/sentinel/UX-004.md` | The other owner's in-progress design-spec. Its bytes must be unchanged after the run. |
| `stale/PROD-001.md` | The live product-brief, now at revision 3. |
| `stale/preserved/PROD-001.r2.md` | Revision 2's preserved bytes, still reachable. |
| `stale/UX-005.md` | A design-spec citing `PROD-001@2`, which no longer matches the live file. |
| `placeholder/UX-006.md` | A design-spec still holding `{{...}}` in required fields. |
| `blocked-check/UX-007.md` | A finished-looking design-spec, used when a requested external check has no implementation. |
| `unverified-inspection/UX-008.md` | A design-spec whose mockup row asserts a visual inspection with no evidence behind it. |
| `unverified-inspection/inspection-claim.json` | The same asserted outcome in field form - claim, tool, viewport, evidence - so a deterministic grader can address the claim and its evidence separately. |

Digests quoted inside a fixture are fabricated placeholders unless a case declares otherwise. Where a case asserts a real sha256 - the ownership sentinel and the preserved product-brief revision - that value is computed from these exact bytes and is recorded in `evals/cases.jsonl`; editing the fixture invalidates the case until the case is updated with it.

## Running `evals/cases.jsonl`

**The case file needs two invocations, not one.** The runner takes exactly one `--candidate` per invocation, and this file deliberately spans two candidate roots: `DX-C-001` inspects the skill package itself, while every other case inspects a fixture directory. Running the whole file against a single root leaves the other cases `COULD_NOT_RUN`, because their `candidate_subpath` will not resolve.

Substitute absolute paths for the two roots and a writable output directory outside the candidate. `--out` must not already exist.

Package-structure case:

```text
python3 <evaluate-expert-skill-root>/scripts/run_cases.py \
  --cases     <package>/evals/cases.jsonl \
  --candidate <package> \
  --mode      installed \
  --case-id   DX-C-001 \
  --out       <run-dir>/observations-package.jsonl
```

Every other case:

```text
python3 <evaluate-expert-skill-root>/scripts/run_cases.py \
  --cases     <package>/evals/cases.jsonl \
  --candidate <package>/evals/fixtures \
  --mode      source \
  --out       <run-dir>/observations-fixtures.jsonl
```

The second invocation runs the whole file, so `DX-C-001` appears in it as `COULD_NOT_RUN`; take that case's result from the first run and ignore its row in the second. Read the two observation files together - neither is complete coverage on its own, and the runner's header records which cases each invocation selected precisely so a partial run cannot be mistaken for a full one.

One result that looks like a defect and is not: `DX-C-001` asserts `path_absent` on `evals`, because an **installed** copy has its authored evals stripped. Run it against the source package - as the first command above does - and that assertion is expected to mismatch. It discriminates an installed copy from a source tree, which is what tier C is for.

Neither invocation writes inside the package, and the runner never imports or executes fixture content: it reads bytes. Exit code 0 means the runner completed and wrote a complete observations file; it says nothing about whether any assertion matched.
