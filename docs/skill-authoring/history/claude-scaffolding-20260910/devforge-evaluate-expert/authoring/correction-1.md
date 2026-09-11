# devforge-evaluate-expert — correction 1

Model: **Opus 5 (1M context)**, model ID `claude-opus-5[1m]`. The system prompt
states a 1M context window (the model name carries "(1M context)" and the ID
carries the `[1m]` suffix).

Author: worker A2 (devforge-opus-author), acting under the coordinator's bounded
correction packet. This record is authoring evidence. It contains no validation
verdict, no self-issued PASS and no acceptance decision; those belong to the
independent evaluator and to compiled Rust in the DevForge CLI.

## Authorization and inputs

| Input | Identity |
| --- | --- |
| Task packet | `/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/correction-evaluate-expert.md` sha256 `c36a48540bfdc50a0261999d4b839154ed25764e8bd9bc25380981efc390a21e` |
| Coordinator disposition (authorization) | `/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/codex-review/coordinator-disposition-20260910.md` sha256 `a7aa1bdb501196b87dae59d82621a8269ec1700704f80b82d51406c9bb160f6f` |
| Candidate superseded | commit `e641797eebf04cd1e8eb9f711549e038e7745407` (verified `git status` clean and HEAD == origin before any write) |
| Worktree / branch | `worktrees/claude-scaffold-evaluate-expert-20260910` / `author/claude-devforge-evaluate-expert-scaffold-20260910` |

Both inputs live in the workspace `tmp/` tree, which is not a Git repository, so
they are bound by absolute path and digest rather than by revision. Neither was
modified. Both were treated as untrusted evidence: every defect was reproduced
against the `e641797` bytes before its change was applied, and nothing was
accepted on the reviewer's or the coordinator's word.

## What changed and why

Three founded defects, each a breach of a contract the package already published
in `references/runner-interface.md`. None of the three is a new requirement.

### CHG-101 / PR13-01 (MAJOR) — unsupported link representations reached MATCH

`references/runner-interface.md` promised `INDETERMINATE` per link for anything
outside the supported subset. The parser instead saw nothing at all, counted zero
links, and reported that every local destination resolved — a statement about
files it never opened.

Reproduced at `e641797` (`python3 -B`, module loaded by path, real budget dict,
scratch fixtures outside the package):

| Input | Before | After |
| --- | --- | --- |
| `[required](missing.md "title")` | MATCH `0 local, 0 external` | INDETERMINATE `line 6: an inline link destination outside the supported subset - a link title, internal whitespace, angle brackets or nested parentheses` |
| `<img src="missing.png">` alone | MATCH `0 local, 0 external` | INDETERMINATE `line 6: an HTML src= or href= resource attribute is outside the supported subset` |
| `[missing]: nothere.md` alone | MATCH `0 local, 0 external` | INDETERMINATE `line 6: a link reference definition is outside the supported subset` |
| `<a href="gone.md">go</a>` alone | MATCH `0 local, 0 external` | INDETERMINATE (HTML resource attribute) |
| control `[required](missing.md)` | MISMATCH `1 local` | MISMATCH `1 local` (unchanged) |
| control `[self](SKILL.md)` | MATCH `1 local` | MATCH `1 local` (unchanged) |
| control `[docs](https://example.com/x)` | MATCH `0 local, 1 external` | MATCH `0 local, 1 external` (unchanged) |
| control: titled link inside a fence | MATCH | MATCH (fenced lines still skipped) |

The disposition's own probe recorded MATCH "1 local" for the titled link; this
reproduction recorded MATCH "0 local, 0 external". Both are the same defect —
the link is not read — and the observed string differs only in whether another
link was present in the probe document. The fix does not change which number is
right; it stops the case reporting a match at all.

Change: three new patterns in `scripts/graders.py` name representations the
parser does not interpret — `INLINE_LINK_OPENER` (an inline-link opener that the
supported `INLINE_LINK` pattern does not also match), `REFERENCE_DEFINITION`
(`^\s{0,3}\[...\]:` followed by space or tab) and `HTML_RESOURCE_ATTR` (an HTML
tag carrying `src=` or `href=`). Each appends to the existing `unsupported` list
with its line number, which the grader already reports as `INDETERMINATE`. No
Markdown renderer was added and nothing attempts to resolve these destinations,
per the packet.

**Each detector was exercised alone**, because the grader reports only the first
unsupported representation it reaches: the shipped `EX-DEF-013` fixture carries
both an HTML attribute and a reference definition and can therefore evidence only
one of them per run. The isolated results are the rows above. That reporting
limit is now stated in `runner-interface.md` rather than left implicit.

### CHG-102 / PR13-02 (MINOR) — a nested fence closed the outer block early

The opening fence length was not kept, so a closing run of the same character
closed the block regardless of length. A four-backtick block quoting a
three-backtick example therefore ended at the inner example and put example-only
lines back into the document.

Reproduced at `e641797` over the packet's exact input: `fenced_lines()` marked
lines 5, 6, 7, 9, 10 and left line 8 (`result: PASS`) outside; with `result` as a
required field, `required_report_fields` returned MATCH `1 fields` for a field the
document states only inside an illustration. After the fix `fenced_lines()`
returns 5–10 and the grader returns MISMATCH `incomplete`.

Change: `fence_token()` and `scan_lines()` are one fence reader, consumed by both
`fenced_lines()` and `grade_package_relative_links`, so the two cannot drift
apart — the packet asked for one factored helper. A block closes only on a run of
the same character that is at least as long as the opening run, per CommonMark.
Fence lines themselves remain reported as inside, which preserves both callers'
prior skip behaviour exactly.

Not implemented and not claimed: CommonMark also forbids an info string on a
closing fence. That rule is outside the packet's scope and is not applied here.

### CHG-103 / PR13-03 (MINOR) — a colon-space plain scalar was stored as parsed

`read_frontmatter` returned status `parsed` for `description: means the user
experience: a schema`, and `frontmatter_fields` returned MATCH "every required
field is a populated scalar" — a value the format does not define, from a reader
whose own docstring says it never guesses a value.

Change: for an unquoted value the trailing ` #` comment is removed first, exactly
as YAML does, and the remainder is then tested for `: ` or a trailing `:`. Either
returns status `unsupported` naming the construct, so `frontmatter_fields` yields
`INDETERMINATE` / `unparsed` as documented.

The grader does not call this a defect, per the packet. The neutral reason text
says the restricted subset "declines to parse it and does not treat it as a
defect". The dated loader observation — Claude Code 2.1.268 was observed loading
such a description on 2026-09-10 — is recorded in the `runner-interface.md` limits
bullet rather than baked into a grader string that would be copied into
observation rows and go stale.

Behaviour after the fix, cross-checked against PyYAML 6.0.3 **in a scratch
harness outside the package** (the package still imports no third-party module):

| Frontmatter value | PyYAML 6.0.3 | Grader after fix |
| --- | --- | --- |
| `description: means the user experience: a schema` | ScannerError, mapping values not allowed here | INDETERMINATE `unparsed` |
| `description: foo:` | ScannerError, mapping values not allowed here | INDETERMINATE `unparsed` |
| `description: "means the user experience: a schema"` | parses | MATCH |
| `description: 'a: b'` | parses | MATCH |
| `description: foo # note: bar` | parses to `foo` | MATCH |
| `description: foo:bar` | parses unchanged | MATCH |
| `description: a plain description` | parses | MATCH |

The trailing-colon case was added on that evidence: PyYAML raises the same error
class for it, so it is the same YAML rule rather than a separate judgement.

## No self-inflicted regression in the package's own files

Before coding the detectors, every `.md`, `.json`, `.jsonl` and `.txt` file in the
package was scanned with prototype versions of all three new link detectors, with
fence tracking applied. **Zero hits.** After the correction the same scan reports
exactly three hits, all of them the two new fixtures that exist to be detected:

```text
HTML-RESOURCE      evals/fixtures/defect-html-and-reference-links/fixture-scope-note/SKILL.md:8
REF-DEFINITION     evals/fixtures/defect-html-and-reference-links/fixture-scope-note/SKILL.md:21
UNSUPPORTED-INLINE evals/fixtures/defect-titled-link/fixture-scope-note/SKILL.md:8
```

The package's own `SKILL.md` was graded with the corrected graders: frontmatter
`MATCH`, links `MATCH` with `26 local, 0 external`. Its description carries no
unquoted `: `, so the coupling the disposition records between the PR13-03 fix
and the devforge-design / devforge-release descriptions does not apply here.

## Regression fixtures and cases added

| Case | Fixture | Grader | Recorded result |
| --- | --- | --- | --- |
| `EX-DEF-012` | `defect-titled-link/` | `package_relative_links` | INDETERMINATE |
| `EX-DEF-013` | `defect-html-and-reference-links/` | `package_relative_links` | INDETERMINATE |
| `EX-DEF-014` | `defect-nested-fence-report/` | `required_report_fields` | MISMATCH `incomplete` |
| `EX-DEF-015` | `defect-frontmatter-colon-space/` | `frontmatter_fields` | INDETERMINATE `unparsed` |

Each is discriminating: run against the `e641797` graders, `EX-DEF-012`,
`EX-DEF-013` and `EX-DEF-014` would have returned MATCH, and `EX-DEF-015` would
have returned MATCH "every required field is a populated scalar".

`evals/evals.json` was not changed. It indexes tier-B acceptance cases and states
in its own `tier_note` that the runner's cases live in `cases.jsonl`, so it does
not index them.

## Commands run

All run from the worktree with absolute paths, `/usr/bin/python3` 3.12.3,
`-B` throughout. Outputs were written to the session scratchpad, never inside the
package.

| # | Command | Exit |
| --- | --- | --- |
| 1 | `git -C <worktree> status --short` / `rev-parse HEAD` / `rev-parse origin/<branch>` — clean, both `e641797` | 0 |
| 2 | Defect reproduction harness against the `e641797` graders (module loaded by path) | 0 |
| 3 | Prototype detector scan over every package `.md`/`.json`/`.jsonl`/`.txt` — 0 hits before, 3 after | 0 |
| 4 | PyYAML 6.0.3 cross-check of seven colon variants, scratch harness only | 0 |
| 5 | Per-construct verification harness after the fix (18 rows, table above) | 0 |
| 6 | `/usr/bin/python3 -B <skill>/scripts/run_cases.py --cases <skill>/evals/cases.jsonl --candidate <skill>/evals/fixtures --out <scratch>/final-source.jsonl --mode source` → `wrote 21 case record(s)` | **0** |
| 7 | `/usr/bin/python3 -B <skill>/scripts/run_cases.py --cases <skill>/evals/cases.jsonl --candidate <skill>/evals/fixtures --out <scratch>/final-installed.jsonl --mode installed` → `wrote 21 case record(s)` | **0** |
| 8 | Row-by-row diff of both runs against `validation/bootstrap-review-e2-recheck/scratch/out/author-{source,installed}.jsonl` | 0 |
| 9 | Digest verification over 100% of both JSON records | 0 |
| 10 | `find <skill> \( -name __pycache__ -o -name '*.pyc' \)` after both runs → 0 | 0 |

Exit 0 from the runner means the program wrote a complete observations file. It
says nothing about any assertion and is not a verdict on the candidate.

Run header identities (source mode), which match the manifest byte for byte:

```text
python_version 3.12.3
runner_identity  95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2
grader_identity  2a6fb9946b31d5d79f401f962aec5b1f4a2f48f97c3ede2eec7d50047ad5d714
case_file        6004e51170c001f1dcb1bcaabb034b08b74a680a4c11d02819d161ab9c089d11
case_count       21
```

Those identities are self-reported by the run. A protected manifest binding the
runner, graders, runtime and case inputs outside evaluated-agent write access is
still not implemented in the DevForge CLI, and this record does not close that.

## Suite results — all 21 cases, both modes

| Case | Tier | source: status / assertions | installed: status / assertions |
| --- | --- | --- | --- |
| `EX-GOOD-001` | C | COMPLETED / A1=MATCH; A2=MATCH; A3=MATCH; A4=MATCH; A5=MATCH | COMPLETED / A1=MATCH; A2=MATCH; A3=MATCH; A4=MATCH; A5=MATCH |
| `EX-GOOD-002` | C | COMPLETED / A1=MATCH; A2=MATCH | COMPLETED / A1=MATCH; A2=MATCH |
| `EX-GOOD-003` | A | COMPLETED / A1=MATCH | COMPLETED / A1=MATCH |
| `EX-DEF-001` | C | COMPLETED / A1=MISMATCH; A2=MISMATCH | COMPLETED / A1=MISMATCH; A2=MISMATCH |
| `EX-DEF-002` | C | COMPLETED / A1=MISMATCH | COMPLETED / A1=MISMATCH |
| `EX-DEF-003` | C | COMPLETED / A1=INDETERMINATE | COMPLETED / A1=INDETERMINATE |
| `EX-DEF-004` | C | COMPLETED / A1=MISMATCH | COMPLETED / A1=MISMATCH |
| `EX-DEF-005` | B | COMPLETED / A1=MATCH; A2=INDETERMINATE | COMPLETED / A1=MATCH; A2=INDETERMINATE |
| `EX-DEF-006` | C | COMPLETED / A1=MISMATCH | COMPLETED / A1=MISMATCH |
| `EX-DEF-007` | A | COULD_NOT_RUN / A1=INDETERMINATE | COULD_NOT_RUN / A1=INDETERMINATE |
| `EX-DEF-008` | C | COMPLETED / A1=INDETERMINATE | COMPLETED / A1=MISMATCH |
| `EX-SEM-001` | B | COMPLETED / A1=INDETERMINATE | COMPLETED / A1=INDETERMINATE |
| `EX-SEM-002` | B | COMPLETED / A1=INDETERMINATE | COMPLETED / A1=INDETERMINATE |
| `EX-DEF-009` | C | COMPLETED / A1=MISMATCH | COMPLETED / A1=MISMATCH |
| `EX-DEF-010` | A | COMPLETED / A1=MATCH | COMPLETED / A1=MATCH |
| `EX-GOOD-004` | A | COMPLETED / A1=MATCH | COMPLETED / A1=MATCH |
| `EX-DEF-011` | C | COMPLETED / A1=MISMATCH; A2=MISMATCH | COMPLETED / A1=MISMATCH; A2=MISMATCH |
| `EX-DEF-012` | C | COMPLETED / A1=INDETERMINATE | COMPLETED / A1=INDETERMINATE |
| `EX-DEF-013` | C | COMPLETED / A1=INDETERMINATE | COMPLETED / A1=INDETERMINATE |
| `EX-DEF-014` | C | COMPLETED / A1=MISMATCH | COMPLETED / A1=MISMATCH |
| `EX-DEF-015` | C | COMPLETED / A1=INDETERMINATE | COMPLETED / A1=INDETERMINATE |

`EX-DEF-007` is `COULD_NOT_RUN` by design: its transcript has no terminal
completion event, so the negative-activation assertion cannot be established.
`EX-DEF-008` differs between modes by design: its assertion declares
`mode: installed`. Neither is a failure of this correction.

The output contains no aggregate field: a grep for `overall`, `coverage`,
`pass_count`, `passed` and `percentage` over both observation files returned 0.

### Existing cases keep their prior outcomes — checked, not asserted

The 17 prior cases were not compared by exit status. Every
`(case_id, assertion_id) -> (execution_status, result, observed)` tuple from both
new runs was diffed against the frozen run recorded at
`validation/bootstrap-review-e2-recheck/scratch/out/author-{source,installed}.jsonl`,
whose header records grader `1b7a27a3…` and case file `c31a7cb0…` — the exact
pre-correction bytes.

| Mode | Baseline rows | Unchanged | Changed | Removed | Added |
| --- | --- | --- | --- | --- | --- |
| source | 25 | 25 | 0 | 0 | 4 |
| installed | 25 | 25 | 0 | 0 | 4 |

The four additions are `EX-DEF-012` to `EX-DEF-015` in both modes. No prior
assertion changed result or observed string.

## Digest regeneration and verification

Prior finding F-R01 was that repair pass 1 changed bytes without regenerating the
digests recording them. To avoid repeating it, digests were written last, in
dependency order: graders → cases → fixtures → README → runner-interface →
`references/derivation.json` → its own digest → `file-manifest.json`.

Digests updated in `references/derivation.json` (each prior value preserved in
that entry's `prior_sha256_chain` with locator `commit e641797…`, noted as
introduced at `e101e76`):

| File | repair pass 1 | correction 1 |
| --- | --- | --- |
| `scripts/graders.py` | `1b7a27a37e1f…` | `2a6fb9946b31…` |
| `references/runner-interface.md` | `87c8942f2faa…` | `045fbb1c8ecb…` |
| `evals/cases.jsonl` | `c31a7cb0a98f…` | `6004e51170c0…` |

`file-manifest.json` updated `scripts/graders.py`, `references/runner-interface.md`
and `references/derivation.json` in `runtime_files_sha256`; `evals/cases.jsonl` and
`evals/fixtures/README.md` in `authored_eval_files_sha256`; added the four new
fixture files; and moved counts from 26 authored eval files / 54 total to 30 / 58.
Runtime file count is unchanged at 28.

Verification, run after all bytes were final, over **every** `sha256`,
`destination_sha256` and `*_sha256` value in both records — runtime files,
authored eval files, authoring records, governing inputs, derivation destinations,
derivation sources, the governing specification, the workspace authorization and
packet, and every historical `prior_sha256_chain` entry resolved through
`git show <commit>:<path>`:

```text
VERIFIED OK: 128   MISMATCH/MISSING: 0   null-by-design (directory / not-ported section): 3
```

The three nulls are `evals/fixtures/` (a directory has no digest) and the two
`missing-rust-capabilities.md (section: …)` pseudo-destinations that record
deliberately not-ported Codex scripts.

This manifest does not list `correction-1.md` or `handoff.md`. Both are written
after it and carry their own digests externally; listing either would record a
digest that goes stale on the next edit. The `_note` says so explicitly, so the
absence reads as deliberate rather than as an omission.

## Files changed

Inside `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/`:

- `scripts/graders.py` (modified)
- `references/runner-interface.md` (modified — only rows whose wording no longer
  matched behaviour, plus two limits bullets)
- `references/derivation.json` (modified — three digests, three prior-chain
  entries, new `correction_1` record)
- `evals/cases.jsonl` (modified — four cases appended; the 17 prior lines are
  byte-identical)
- `evals/fixtures/README.md` (modified — new "Fixtures added in correction 1"
  section)
- `evals/fixtures/defect-titled-link/fixture-scope-note/SKILL.md` (added)
- `evals/fixtures/defect-html-and-reference-links/fixture-scope-note/SKILL.md` (added)
- `evals/fixtures/defect-nested-fence-report/report/expert-evaluation-report.md` (added)
- `evals/fixtures/defect-frontmatter-colon-space/fixture-scope-note/SKILL.md` (added)
- `scripts/__pycache__/` (removed — gitignored build residue left inside the
  package by an external reproduction run; `git ls-files` reported 0 tracked
  files there, and no `__pycache__` or `.pyc` exists in the package after either
  suite run)

Inside `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/`:

- `file-manifest.json` (modified)
- `correction-1.md` (added — this file)

Nothing else in either repository was touched. `SKILL.md`, `scripts/run_cases.py`
and every asset are unchanged by this correction. No frozen evidence under
`validation/` was modified, repinned or rolled back; the E2 and E2-recheck
directories were read only.

## What was NOT run

| Work | Status | Cause |
| --- | --- | --- |
| Tier A — discovery and activation from an installed package in a fresh terminal | `NOT_RUN` | Outside the packet's scope. No installation, export, discovery probe or client session was performed. |
| Tier B — output quality against an `old_skill` or `without_skill` baseline | `NOT_RUN` | Outside the packet's scope. The 12 tier-B cases in `evals/evals.json` remain `AUTHORED_NOT_EXECUTED` / `NOT_RUN`, and that file's own execution boundary says authoring them is not permission to run them. |
| Tier C — installed-resource resolution against a real installed copy | `NOT_RUN` | The case suite was run against `evals/fixtures/`, which exercises the graders. Running the graders against fixtures is a test of the graders, not an evaluation of this package. |
| Behavioural status of this skill | `NOT_EVALUATED` | No terminal evaluation was recorded. |
| Validation of this correction | Not performed by the author | An author cannot supply the independent judgement of its own candidate. The packet routes this to a focused evaluator recheck of PR #13. |
| Structural inspection (S001–S013) and evidence reduction in the DevForge CLI | Still not implemented | Unchanged by this correction. A complete set of matching rows does not close it. |
| Protected-manifest custody for the evaluation runner | Still not implemented | Unchanged. The run header identities above are self-reported. |

## Out-of-fence items deliberately not touched

The disposition also founded PR14-01 (`devforge-design` description) and the same
defect in `devforge-release` (PR #19), and left the PR20 inverted sentinel open.
All three are on other branches and outside this fence. They were not edited,
and nothing here depends on them landing.
