# Codex PRD v2 / Architecture v4 contract update

Source authored and static validation passed. **Native qualification remains blocked.** The
270-trial campaign completed 111 trials, hit the native usage limit in four attempts and left
155 NOT_RUN. It also used two Codex executable versions despite freezing one. Manual observations
contain 15 passing and three failing scenarios. Publication does not establish qualification,
installation parity or owner acceptance.

This PR publishes source and four evidence files: this report,
[evaluation-summary.json](evaluation-summary.json),
[failure-categories.json](failure-categories.json) and the
[whole-folder SHA-256 manifest](evidence-sha256-manifest.json). Full native traces, candidate and
fixture snapshots, detailed reports, failed controls and consuming workspaces remain untracked
locally. The manifest inventories every file in that local evidence folder, including hidden files;
only the manifest itself is excluded to avoid a self-reference. It proves recorded byte identity,
not evaluation quality or availability of the omitted files in a clone.

## Candidate and source changes

- Branch: `codex/prd-spec-002-v2-20260929`.
- Baseline: `f69fee275860bcd68c6be632478552fa34d6f00b`, including the Codex Architecture v5 update.
- Frozen runtime digest: `3517d2ce0adfefb405faf11fb433e723e725e8fe68af92ba272dee13702b0f0f`.
- Frozen plan digest: `fdb5d33675ec1867290dfa148e39995cc543ee0732b152be42f6fafe66e34e47`.
- Original local freeze checkpoint: `b220dc771fed70a935ae234fc2e7bded41485dc9`; retained locally when
  the unpublished commit was amended to remove full evidence. Runtime bytes are unchanged.
- Versions: plugin 0.5.0; PRD SKL-002 v2 implementing SPEC-002 v2; Architecture SKL-003 v6
  implementing SPEC-003 v4.
- SPEC-002 authority digest: `7f387a178f153b745f67a0d7dab08f58622561faf303f95cd3a619f1eb101085`.
- SPEC-003 authority digest: `8d757078c85144ff8e790e5eec89335688a9bee1025c0c81a476894115c9e4f8`.

The [PRD skill](../../skills/prd/SKILL.md) and
[Architecture skill](../../skills/architecture/SKILL.md) now use the approved failure lifecycle,
bounded validation cycles and shared policy checks. The plugin manifest, affected templates,
references and provenance are aligned. The other runtime skills and approved authority bytes in
the task worktree are unchanged. Source tests and generators remain in the package.

| Contract | Resulting Codex behavior / adaptation |
|---|---|
| D-03 | Failed approved extensions stay in-review with approval cleared |
| D-04 | One initial check plus at most three actual repair/readback cycles, with every attempt reported |
| D-05 | Explicit none, no target yet, partial and unanswered quality states remain distinct; none does not waive policy |
| D-06 | Explicit new/extend choices satisfy the choice gate |
| D-07 | FRs cite promoted ideas; NFRs cite their actual source |
| D-08 | Historical authors/reviews/items/Change Log rows retained; add the tool if missing; new revision unreviewed. The VER-32 author-list conflict remains failed |
| D-09 | Shared validator uses exits 0/1/2, schema checks, calendar checks and SV-01..06; inability to validate applicable approved policy stops the workflow |
| Architecture ERR-05 | Failed accepted decisions return to proposed; failed supersession restores the old ADR byte-for-byte, clears replacement approval and supersedes, leaves dependent DECs open with no resolver and gives no readiness handoff |
| Provider interface | Namespaced invocation, ID-only inputs, loaded-skill-relative resources, Codex local preferences and question-tool/plain-text branches |
| Identity | `tool: codex`; supported identity only, otherwise unavailable with disclosure. Exact identity qualification stays open |

Policy/default references match between the two Codex skills. Their Claude differences are the
local preference path and question limits. Both validators and schema copies match the Claude
copies; schemas also match `src/schemas/`. Impossible dates are additional **calendar check**
errors, never schema errors. The PRD generator adds nine cases and VER-09/10 checks; Architecture
adds VER-17/18 and the manual VER-19 fixture. All 278 pre-existing automated case files are preserved.

## Results and incomplete coverage

| Scope | Planned | Completed | Behavior PASS | Behavior FAIL | Platform interrupted | NOT_RUN |
|---|---:|---:|---:|---:|---:|---:|
| PRD plugin | 87 | 56 | 51 | 5 | 2 | 29 |
| PRD baseline | 87 | 55 | 3 | 52 | 2 | 30 |
| Architecture plugin | 48 | 0 | 0 | 0 | 0 | 48 |
| Architecture baseline | 48 | 0 | 0 | 0 | 0 | 48 |
| Total | 270 | 111 | 54 | 57 | 4 | 155 |

The 0.8 threshold is unchanged: three binary repetitions require 3/3. No case reached 3/3.
All third PRD repetitions and all Architecture automated trials are NOT_RUN. The summary preserves
all 270 slots and 45 case results, plus the explicit missing-evidence lists. The four native
`usageLimitExceeded` attempts are `NOT_ASSESSED_PLATFORM_LIMIT`; their partial artifacts are not
behavior passes or failures. No unchanged native run was retried to erase a failure. No completed
semantic assessment is pending. Counts above are observations across mixed host versions and do
not establish a qualified fixed-host comparison.

Static validation passed: Plugin Creator and skill validators, all 156 package tests, schema and
version checks, shared byte identity, original-case preservation, generation consistency and
whitespace checks. Package tests include independent policy negatives, calendar/leap-day/null
cases, missing-library handling, provider adapter controls and interruption classification.

Manual checks sealed 18 scenarios: 15 PASS and three FAIL, covering 22 scoped obligations (19 PASS,
three FAIL). Passing observations include partial interview states, actual question-tool and full
plain-text branches, failed extensions, policy handling and both Architecture failure rollback
scenarios. The tool interview explicitly switched from Plan to Default before writing. Inherited
Architecture manual branches remain NOT_RUN; prior candidate results are not inherited.

## Open failures and evidence limits

- **Behavior:** the draft-brainstorm warning omitted undecided ideas in repetition one; it passed
  in repetition two, which does not erase the failure. Both manual stop/save attempts omitted the
  required save-choice offer, leaving the dependent yes/no branches unrun.
- **Specification conflict:** BEH-10 says to retain authors while adding the tool if missing;
  VER-32 requires the author list unchanged. The approved cross-provider fixture lacks `codex`.
  Both automated extension repetitions and the manual extension expectation remain failed.
  The manual scenario also recorded a recommendation mismatch. No specification or historical
  author-list grader was changed.
- **Identity:** both provenance repetitions failed, and 34 completed plugin trials retain open
  current-write identity. Honest unavailable disclosure does not satisfy BEH-10 qualification.
- **Host binding:** the plan froze 0.159.0, but 51 automated starts advertised 0.159.0 and 64
  advertised 0.159.1. All 18 manual sessions advertised 0.159.0. The launcher was checked only at
  matrix start and later changed target. The closing executable target/hash audit is FAIL.
  Advertised versions do not prove per-process binary hashes; the update mechanism is unknown.
  Future frozen runs need an immutable executable path and digest verification before each start.
- **Isolation:** one baseline listed shared `/tmp` names and metadata, including 59 other campaign
  directories. Two other broad searches did not execute after preceding Git failures. Two actors
  wrote the same auxiliary report path at different times; inspected programs read their own
  project inputs. Bounded trace review does not establish hermetic read isolation.
- **Preservation:** all 897 protected task-worktree inputs, the prompt and historical reports
  remained unchanged. Primary advanced from `7e87cf4b4858d9184b763afad631a17ab34a972f` to
  `7d9b2cc2220d76c5d69f64d0b361b2df677033a1`. Fourteen captured tracked files changed and six were
  added through recorded merged commits; untracked status also changed. The actor responsible
  is not established. Primary preservation is FAIL_PRIMARY_DRIFT; no reset or copy-back was made.

The [failure categories](failure-categories.json) separate behavior failures, specification
conflict, identity, platform interruptions, host drift, isolation, grader defects and missing
evidence. Retained grading views corrected null output, semantic focus files, a current-row
provider literal and implicit positive activation checks in baseline arms. A reporting correction
separated interrupted turns from behavior judgments. Original definitions, thresholds, failed
controls, native attempts and runtime bytes remain unchanged. Assessment was performed by the
root evaluator against separate sealed native actors; it is not independent of source authorship
and is not the owner's personal review.

## Local evidence and review boundary

Local-only relative paths such as `native/plan.json`, `native/summary.json`,
`native/closing-custody.json`, `native/native-host-audit.json`, `preservation-after.json` and
`primary-drift-investigation.json` are inventory identifiers in the manifest, not links to files
shipped in this PR. The complete original report and discrepancy notes are retained in
`local-reports/`. The detailed before/after hashes and all raw failures remain in the local folder.

The PR publishes only source and the four compact evidence files. Source/static checks, native
observations, complete qualification, Git publication, installation and owner acceptance remain
distinct. Installation/deployment is NOT_RUN and owner acceptance is PENDING.
