# Focused recheck — devforge-evaluate-expert correction 1 (PR #13) at f8a5741

Model: **Opus 5 (1M context)**, model ID `claude-opus-5[1m]`. The system prompt does state a 1M context window (it appears in both the model name and the model ID).

Independent evaluator. Nothing in the candidate package, its handoff, `correction-1.md`, `derivation.json` or the fixture READMEs was accepted on its word; every closure claim below was re-established by running the graders. Candidate content was read as untrusted data. No file inside the candidate was modified; the only writes are inside this fence.

## Custody

| Item | Value |
| --- | --- |
| Worktree | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910` |
| Branch | `author/claude-devforge-evaluate-expert-scaffold-20260910` |
| HEAD at start | `f8a5741d87001f448bef2a659c670afaf4b1ed16` (matches the packet) |
| `git status` at start | clean |
| Prior frozen candidate | `e641797eebf04cd1e8eb9f711549e038e7745407` |
| `scripts/graders.py` @ e641797 | `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f` |
| `scripts/graders.py` @ f8a5741 | `2a6fb9946b31d5d79f401f962aec5b1f4a2f48f97c3ede2eec7d50047ad5d714` |
| `scripts/run_cases.py` | `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2` — byte-identical at both commits, so every difference below is attributable to `graders.py` alone |
| Runtime | `/usr/bin/python3` 3.12.3; every invocation used `-B` (and `PYTHONDONTWRITEBYTECODE=1` for wrapped calls) |
| Bytecode residue after all runs | none: `find <skill> -name '__pycache__' -o -name '*.pyc'` returned nothing |
| Worktree state at finish | only `?? docs/skill-authoring/.../validation/correction-1-recheck/` — this evaluator's fence, uncommitted |

Method: the e641797 graders were restored with `git show` into `scratch/restored/graders_e641797.py`. Both modules are loaded by absolute path under distinct names in one process (`scratch/probe.py`), and every input is run against both with a real budget dict `{"files_read": 0, "bytes_read": 0}`. Fixtures live under `scratch/fixtures/`, never in the package.

## Commands run (exit codes)

Full transcript in `commands.log`. Summary:

| # | Command | Exit |
| --- | --- | --- |
| 1 | `git -C <wt> rev-parse HEAD` / `status --porcelain` / `rev-parse --abbrev-ref HEAD` | 0 |
| 2 | `git -C <wt> diff --stat e641797 f8a5741 -- .../scripts/run_cases.py` (empty output) | 0 |
| 3 | `git -C <wt> show e641797:.../scripts/graders.py > scratch/restored/graders_e641797.py` | 0 |
| 4 | `/usr/bin/python3 -B .../scripts/run_cases.py --cases evals/cases.jsonl --candidate evals/fixtures --out scratch/out/f8a5741-source.jsonl --mode source` → `wrote 21 case record(s)` | 0 |
| 5 | same with `--mode installed --out scratch/out/f8a5741-installed.jsonl` → `wrote 21 case record(s)` | 0 |
| 6 | `/usr/bin/python3 -B scratch/old-runner/run_cases.py --cases evals/cases.jsonl --candidate evals/fixtures --out scratch/out/e641797-graders-source.jsonl --mode source` (the same runner with the e641797 graders beside it) | 0 |
| 7 | `/usr/bin/python3 -B scratch/compare.py <frozen author-source.jsonl> scratch/out/f8a5741-source.jsonl source` | 0 |
| 8 | `/usr/bin/python3 -B scratch/compare.py <frozen author-installed.jsonl> scratch/out/f8a5741-installed.jsonl installed` | 0 |
| 9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B scratch/probe.py` — 39 inputs × 2 grader revisions | 0 |
| 10 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B scratch/probe2.py` — 3 precedence inputs × 2 revisions | 0 |
| 11 | `/usr/bin/python3 -B -c "import yaml; ..."` — PyYAML 6.0.3 ground truth for six frontmatter bodies (scratch only; the package still imports no third-party module) | 0 |
| 12 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B scratch/package-scan.py` — both grader revisions over the candidate's own 17 Markdown files and every Claude plugin `SKILL.md` | 0 |
| 13 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B scratch/verify-digests.py` — every sha256 in `references/derivation.json` | 0 |
| 14 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B scratch/verify-manifest.py` — every sha256 in the authoring `file-manifest.json` | 0 |
| 15 | `git -C <wt> show 69b6090:.../devforge-project-expert-creator/SKILL.md \| sha256sum` (manifest `builder_followed` pin) | 0 |
| 16 | language-policy greps over `graders.py` and `run_cases.py`, plus an aggregate-key scan over both observation files | 0 |
| 17 | `find <skill> -name '__pycache__' -o -name '*.pyc'` (no output) | 0 |

## 1. Defect closure, by execution

Each input was run against the graders at both commits in the same process. "Result" is the assertion row the grader returned.

| # | Input (coordinator's own reproduction input) | Grader | Result at e641797 | Result at f8a5741 | Closed |
| --- | --- | --- | --- | --- | --- |
| 1 | `[required](missing.md "title")` | `package_relative_links` | **MATCH** `0 local, 0 external` — "every local destination resolves inside the package" | **INDETERMINATE** — "line 6: an inline link destination outside the supported subset — a link title, internal whitespace, angle brackets or nested parentheses" | yes |
| 2 | `<img src="missing.png">` + `[missing]: nothere.md` | `package_relative_links` | **MATCH** `0 local, 0 external` | **INDETERMINATE** — "line 6: an HTML src= or href= resource attribute is outside the supported subset" | yes |
| 2a | `<img src="missing.png">` alone | `package_relative_links` | **MATCH** | **INDETERMINATE** (HTML detector) | yes |
| 2b | `[missing]: nothere.md` alone | `package_relative_links` | **MATCH** | **INDETERMINATE** (reference-definition detector) | yes |
| 3 | control `[required](missing.md)` | `package_relative_links` | **MISMATCH** "the local destination does not exist" | **MISMATCH**, byte-identical reason | control holds |
| 4 | four-backtick block quoting a three-backtick example | `required_report_fields` | **MATCH** `1 fields` for an example-only field | **MISMATCH** `incomplete` — "missing or empty required field(s): result" | yes |
| 5 | `description: means the user experience: a schema` | `frontmatter_fields` | **MATCH** `description,name` — "every required field is a populated scalar" | **INDETERMINATE** `unparsed`, reason names the mapping indicator and explicitly declines to call it a candidate defect | yes |

**PR13-01 CLOSED, PR13-02 CLOSED, PR13-03 CLOSED.** Both of the two detectors that EX-DEF-013 names were exercised on their own (rows 2a and 2b), because the shipped fixture can only evidence one per run — see finding R1-007.

One observation discrepancy, recorded for the record and not a defect: the coordinator disposition's "Grader repro" row states that input 1 returned MATCH **"1 local"** at e641797. This evaluator's independent reproduction returned MATCH **"0 local, 0 external"** — the titled link is not matched by `INLINE_LINK` at all, so nothing is counted. The author's `derivation.json` CHG-101 records the same discrepancy. Either way the result at e641797 is MATCH, so the defect stands exactly as disposed; only the `observed` string differs.

PyYAML 6.0.3 ground truth used to judge row 5 and the scalar probes: `description: means the user experience: a schema` and `description: see the following:` both raise `ScannerError: mapping values are not allowed here`; `description: ratio 3:1 of cases` and `description: plain text # note: here` parse normally. The new INDETERMINATE is therefore justified for exactly the constructs PyYAML refuses, with the one exception in R1-001.

## 2. The four new cases, and the prior 17

Suite run at f8a5741, both modes, exactly as the package documents:

```
/usr/bin/python3 -B scripts/run_cases.py --cases evals/cases.jsonl --candidate evals/fixtures --out <scratch> --mode source     -> exit 0, wrote 21 case records
/usr/bin/python3 -B scripts/run_cases.py --cases evals/cases.jsonl --candidate evals/fixtures --out <scratch> --mode installed  -> exit 0, wrote 21 case records
```

Comparison against the frozen `validation/bootstrap-review-e2-recheck/scratch/out/author-{source,installed}.jsonl`, row by row on `(case_id, assertion_id, grader, result, observed, reason, evidence)` plus `execution_status`:

| Mode | Frozen cases | Current cases | Prior-case assertion rows changed | Cases removed | Cases added |
| --- | --- | --- | --- | --- | --- |
| source | 17 | 21 | **0** | 0 | EX-DEF-012..015 |
| installed | 17 | 21 | **0** | 0 | EX-DEF-012..015 |

No prior assertion row changed in either mode — not the result, not the observed string, not the reason text, not the evidence path.

The manifest's `correction_1.suite` prose asserts "25 baseline assertion rows". Counted independently: the frozen `author-source.jsonl` and `author-installed.jsonl` each hold 17 case records carrying **25** assertion rows; the two f8a5741 runs each hold 21 case records carrying **29**. 25 + 4 = 29, so the manifest's count is confirmed (`scratch/out/assertion-row-counts.txt`).

Do the four new cases discriminate? Each was re-run against the e641797 graders (command 6, the shipped runner with the old grader module beside it in scratch):

| Case | Assertion | e641797 graders | f8a5741 graders | Discriminates |
| --- | --- | --- | --- | --- |
| EX-DEF-012 | `package_relative_links` | MATCH `0 local, 0 external` | INDETERMINATE, "line 8: an inline link destination outside the supported subset" | yes |
| EX-DEF-013 | `package_relative_links` | MATCH `0 local, 0 external` | INDETERMINATE, "line 8: an HTML src= or href= resource attribute" | yes (HTML detector only — R1-007) |
| EX-DEF-014 | `required_report_fields` | MATCH `1 fields` | MISMATCH `incomplete` | yes |
| EX-DEF-015 | `frontmatter_fields` | MATCH `description,name` | INDETERMINATE `unparsed` | yes |

All four are permanent regressions in the intended sense: each fails against the pre-correction code.

## 3. Regression hunt on the changed code

39 paired probes in `scratch/probe.py` plus 3 in `scratch/probe2.py`, covering tilde fences, indented fences, longer and shorter closing fences, unclosed fence at EOF, info-string closers, tab-indented fences, image links, parenthesised and angle-bracket destinations, multiple links per line, the `MAX_LINKS` bound, and quoted / commented / trailing-colon / colon-without-space / URL / empty scalar values. Full output in `scratch/out/probe-run.txt` and `probe2-run.txt`.

**No new false MATCH was produced.** Every behaviour change introduced by correction 1 moves in the conservative direction (MATCH → INDETERMINATE, MATCH → MISMATCH, and in one case MISMATCH → INDETERMINATE — see R1-009). That is the result that decides the disposition below.

Nine findings, in `findings-recheck.json`:

| ID | Severity | New in correction 1? | Summary |
| --- | --- | --- | --- |
| R1-001 | MINOR | **yes** | `description: "a: b" # note` — valid YAML (`'a: b'` under PyYAML 6.0.3) — is now INDETERMINATE, and the reason text calls a quoted value "an unquoted plain scalar". The quote test at `graders.py:228` runs before the comment strip at `:235`, so the value never enters the quoted branch. |
| R1-002 | MINOR | **yes** | The three new detectors fire on prose and inline code spans that contain no link: `` `[label](path "title")` `` in prose, `` `<img src=...>` `` in prose, `[Note]: this is prose...`, and `data-src=`. All four were MATCH at e641797 and are INDETERMINATE at f8a5741. |
| R1-003 | MINOR | no (pre-existing) | `description: # placeholder` is reported MATCH "populated scalar" with the comment text stored as the value; PyYAML gives `None`. Same family as the defect PR13-03 closed, byte-identical at both commits. |
| R1-004 | MINOR | wording is new | `runner-interface.md:93` now promises INDETERMINATE for angle-bracket destinations. `[x](<references/present.md>)` — a valid link to a file that exists — returns MISMATCH "the local destination does not exist" at both commits. |
| R1-005 | ADVISORY | no | A closing fence carrying an info string still closes the block (CommonMark forbids it), so a false MATCH remains reachable. `derivation.json` CHG-102 discloses this verbatim; `runner-interface.md:95` does not. |
| R1-006 | ADVISORY | no | `FENCE`'s `^\s{0,3}` treats a leading tab as one column, so a tab-indented fence opens a block where CommonMark sees indented code. Conservative direction. |
| R1-007 | ADVISORY | **yes** | EX-DEF-013 names two detectors but can only evidence the HTML one (line 8 precedes the reference definition at line 21). Removing `REFERENCE_DEFINITION` would leave the suite output unchanged. |
| R1-008 | ADVISORY | no | When a document has both a broken supported link and an unsupported representation, the unsupported entry is discarded from the emitted result, not deferred. |
| R1-009 | ADVISORY | **yes** | The colon-space rule aborts the whole frontmatter block, so a readable `name` is lost too: `name_folder_relation` on the same bytes went from a determinable MISMATCH at e641797 to INDETERMINATE at f8a5741. |

Impact bound for R1-001/R1-002, measured rather than asserted (`scratch/out/package-scan.txt`): running both grader revisions over the candidate's own 17 Markdown documents and over all five Claude plugin `SKILL.md` files present in this worktree, **0 results changed**. The new false-INDETERMINATE family does not fire on any real document in this tree. It is a cost for future evaluated packages, not a present regression in this one.

Behaviours that were probed and are correct at both commits, recorded so they are not re-probed: tilde-opened blocks are not closed by a backtick run; a longer closing run closes; an unclosed fence at EOF swallows the remainder (documented); image links resolve and fail correctly; three links on one line are all counted and the broken one is named; the `MAX_LINKS` bound reports INDETERMINATE at 2049 counted links; quoted colon values, colons without a following space, URLs, comment-borne colons and empty values all answer as YAML does.

## 4. Documentation truthfulness and digests

`references/runner-interface.md` was read line by line against observed behaviour. The three changed rows and the two changed Limits bullets are truthful with one exception (R1-004, angle brackets) and two omissions (R1-005 info-string rule; R1-002 detector over-approximation). The newly added sentences that this evaluator confirmed by execution: "It reports the first one it reaches" (true), "A shortcut reference used in prose without a definition on its own line is not detected at all" (true — `[the required format]` with no `][` is undetected), and the frontmatter row's new `: `/trailing-`:` clause (true for every input PyYAML refuses).

Digest verification, 100 % of both files, recomputed with SHA-256 from the named bytes:

| File | Digest-bearing nodes | MATCH | MISMATCH | Declared null |
| --- | --- | --- | --- | --- |
| `references/derivation.json` | 64 | **61** | **0** | 3 (two section-reference destinations, one directory entry) |
| authoring `file-manifest.json` (tables) | 67 | **67** | **0** | 0 |
| authoring `file-manifest.json` (prose) | 3 | **3** | **0** | 0 |
| **Total** | **134** | **131** | **0** | **3** |

Breakdown of the 64 derivation nodes: 1 governing specification (verified at revision `c17e758`), 18 `destination_sha256` (16 checked against current bytes, 2 declared null), 18 `source.sha256` (10 verified via `git show c17e758:<path>`, 8 against the working-tree Codex sources the record names), 10 `prior_*_chain` entries (verified via `git show <commit>:<path>` at `e52ac59` and `e641797`), 15 `new_in_this_package` (14 current bytes, 1 directory null), 2 `correction_1` workspace pins (coordinator disposition `a7aa1bd…`, task packet `c36a485…`) verified by absolute path. Breakdown of the 67 manifest table digests: 28 runtime + 30 authored-eval (current bytes under the skill root), 4 authoring records, 5 governing inputs (verified at `base_commit c17e758`). The 3 prose digests are the two workspace pins (duplicated from derivation) and the `builder_followed` `SKILL.md` pin, verified at commit `69b6090`.

`file-manifest.json` declares `revision: 3`, `supersedes` commit `e641797` with `supersedes_chain` back to `e52ac59`, `validation_status: "Not performed."` and `behavioral_status: NOT_EVALUATED`. Completeness was checked independently of the digests: **58 paths listed = 58 files on disk** under the skill root, 0 unlisted and 0 missing. The `correction_1` block's `files_changed` / `files_added` lists match `git diff --name-status e641797 f8a5741` exactly for the package paths; the diff also carries the two authoring records (`authoring/correction-1.md` added, `authoring/file-manifest.json` modified), which sit outside the package and outside those lists by design. No repetition of F-R01 (stale digests) was found anywhere.

## 5. Language policy

`scripts/graders.py` emits only `MATCH` (13 call sites), `MISMATCH` (22) and `INDETERMINATE` (11); the only occurrences of `PASS` are one docstring sentence at line 509 explaining that a self-claimed PASS is not adopted, and `verdict` is a local variable name inside `grade_package_relative_links` holding one of the three assertion constants. `run_cases.py` mentions the authority vocabulary only in prose that disclaims it. Case-level `execution_status` is `COMPLETED` / `COULD_NOT_RUN` / `SKIPPED` only. The exit status is `0` after a complete write regardless of any assertion result, `1` for unusable input, `2` for an internal fault — no aggregation into the exit code.

Scanned both observation files this recheck produced for aggregate keys (`overall`, `summary`, `passed`, `failed`, `coverage`, `percent`, `verdict`, `decision`, `accepted`, `score`, `total`) and for authority-vocabulary string values (`PASS`, `FAIL`, `NOT_APPLICABLE`): **none present** in either mode. Distinct assertion result values in both files: `INDETERMINATE`, `MATCH`, `MISMATCH`. The package contains exactly two `.py` files, both under `scripts/`. No admission, mutation permission or acceptance is claimed anywhere in the emitted evidence.

## Not run

| Item | Status | Cause |
| --- | --- | --- |
| Native tier C | **NOT_RUN** | Out of this packet's scope. No install, no `devforge isolate` boundary probe, no model execution was attempted. |
| Native tier B | **NOT_RUN** | Out of scope. `evals/evals.json` still carries `authoring_status: AUTHORED_NOT_EXECUTED`, `execution_status: NOT_RUN`. |
| Native tier A | **NOT_RUN** | Out of scope. Trigger queries were not exercised. |
| Semantic re-adjudication of SKILL.md, assets, references | **NOT_APPLICABLE** | Closed at e641797; the packet excludes reopening F-001..F-009 and F-R01. |
| DevForge CLI structural inspection (S001-S013), evidence reduction, protected runner manifest | **NOT_RUN** | Not implemented in the DevForge CLI; the package names both gaps and this recheck does not close them. Local script runs are local evidence, not isolated native evidence. |

## Disposition

**Correction 1: closed, per defect.**

| Defect | Disposition |
| --- | --- |
| PR13-01 unsupported link syntax reaching MATCH | **CLOSED** — titled links, HTML `src=`/`href=` and link reference definitions each produce INDETERMINATE with a line number; each detector demonstrated alone; the plain-link control is unchanged. |
| PR13-02 nested fence closing early | **CLOSED** — the CommonMark same-character, at-least-as-long closing rule is implemented in one shared reader used by both callers; the example-only field is now MISMATCH `incomplete`. |
| PR13-03 colon-space plain scalar accepted as parsed | **CLOSED** — INDETERMINATE `unparsed`, with a reason that declines to parse without calling the candidate defective, matching the disposition's requirement. |

Supporting conditions all hold: prior 17 cases unchanged in both modes (0 drifted rows), 4 new cases all discriminating, 131 of 134 digest-bearing nodes verified and 3 declared null, with 0 mismatches and 0 stale entries, manifest complete at 58/58 files, no bytecode written into the package, language policy intact.

**Package disposition: insufficient evidence.** Native tiers C, B and A are NOT_RUN, so no behavioural evidence exists for this package at any commit and readiness cannot be established here. Nothing found in this recheck argues for "revise": no new false MATCH was produced, every behaviour change moves conservatively (MATCH → INDETERMINATE, MATCH → MISMATCH, or MISMATCH → INDETERMINATE), and the two new MINOR false-INDETERMINATE findings (R1-001, R1-002) were measured to change **zero** results on real documents in this tree. Five items are worth a cheap follow-up, each with a one-to-three-line repair named in `findings-recheck.json`: **R1-003 first** — it is the only undisclosed false MATCH in the batch, a `description:` line carrying nothing but a comment is reported as a populated scalar when YAML reads it as null, which is the same family as the defect PR13-03 closed and is not mentioned in `runner-interface.md` — then R1-001, R1-002, R1-004 and R1-007. None of them undoes a closed defect or blocks the coordinator's next step, and R1-003 is byte-identical at both commits, so none changes the package disposition. This evaluator recommends; acceptance is not the evaluator's decision.
