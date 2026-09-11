---
schema_version: "devforge.artifact/v1"
artifact_id: "SEVAL-E2-002"
artifact_type: "skill-evaluation-report"
project_id: "DevForgeAI"
revision: 2
status: draft
created_at_utc: "2026-09-10T19:51:28Z"
producer:
  skill: "independent evaluator (bootstrap, source-loaded rubric)"
  skill_revision: "no skill was installed, discovered or activated; focused re-evaluation of changed requirements only"
execution_ref: "worker E2, focused recheck of repair pass 1 under coordinator authorization"
upstream:
  - path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/validation/bootstrap-review-e2/evaluation-report.md"
    note: "SEVAL-E2-001, the review this supersedes"
evidence: []
supersedes: "SEVAL-E2-001 (bootstrap-review-e2/evaluation-report.md, candidate e52ac596)"
decision_ref: null
missing_inputs:
  - "Tiers A, B and C remain NOT_RUN; a repair pass cannot change that."
  - "R01-R04, R06, R07 and R10 were NOT re-adjudicated: the authorization covers R05, R08 and R09 only."
---

# Focused recheck - Claude `devforge-evaluate-expert`, repair pass 1

## Scope of this recheck

Authorized scope: **only** the changed requirements F-001…F-009, and **only** rubric criteria R05, R08 and R09.
Unchanged broad checks from SEVAL-E2-001 were deliberately not rerun. Regression coverage was limited to the
assertions that share code paths with a repair.

This supersedes SEVAL-E2-001 for the findings it rechecks. Everything SEVAL-E2-001 records about the bootstrap
route, the missing DevForge CLI capabilities and the native tiers still stands and is not restated in full.

## Candidate identity

- **New candidate:** `e101e76162976f2414035bbe542f0a34f8cc51be` (verified as HEAD), preceded by `b6a4bf7`
  which added only the E2 review directory (confirmed: `git diff --name-status e52ac59 b6a4bf7` touches nothing
  under `providers/`).
- **Supersedes:** `e52ac596cbf790dfa156d883852d392c512fdbcc`.
- **Changed under `providers/`:** 14 files, 422 insertions, 27 deletions. Ten modified, four added (all four are
  new regression fixtures). **No file was deleted**, and no file outside the candidate package and the author's
  authoring directory was touched.
- **Package size:** 54 files (28 runtime, 26 authored eval), up from 50.
- **Digests of the changed files at `e101e76`** (recomputed here; also in `scratch/changed-files-e101e76.txt`):

| File | sha256 |
| --- | --- |
| `SKILL.md` | `bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac` |
| `scripts/run_cases.py` | `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2` |
| `scripts/graders.py` | `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f` |
| `references/runner-interface.md` | `87c8942f2faa9c00c8746eeb51001ddccee3802c9f21a6e187d072251d4673e2` |
| `references/native-evaluation.md` | `7d4a8bda731c318dbbaf61127578bf84e02fc1970be9fe4015bfaa6d0adc7e6f` |
| `references/results-contract.md` | `ebac4e4c53f9a5d525e5edb1d331c4ee4c5736c26f18845090e7e3fd2d2c6af6` |
| `references/sources.md` | `d4bb9bb57aea8cc6185092a148204a7ac91dc7354952ce1018ea9230f4bc4f37` |
| `references/derivation.json` | `0c79f568af1be499a2eea8c99bb5e46f692e273876bc8691ac179508b338df04` |
| `evals/cases.jsonl` | `c31a7cb0a98fd33941fadb23c0fc63b1f274f07df15f850348acdf3b310f6be8` |
| `evals/fixtures/README.md` | `38d893a1da0e46d57de597bc48290bc4bdebc4e0d288a064844344e6b7d9c03d` |
| `evals/fixtures/defect-fenced-report/report/expert-evaluation-report.md` | `bddbde2ccf948150021cf29a84b09582224ba2972982f7f7edb93eaf8ac43ab6` |
| `evals/fixtures/defect-frontmatter-non-mapping/fixture-scope-note/SKILL.md` | `c590f4a65f214b6851412b5c05a34b7544019398e3bb96a448edc9c264ece33e` |
| `evals/fixtures/defect-mention-only/transcript/mention-only.json` | `22946cead53646150b173abd22ce6c60a41ed2cfc9605ee59adbac85e8c07cf9` |
| `evals/fixtures/good/transcript/positive-consultation.json` | `a2f5e827d322946bfd7cbd6e4831ae014a3b8b3787239de6ff1fb7058aeb1bba` |

**Integrity of this recheck:** the package manifest is byte-identical before and after every run
(`scratch/manifest-before.txt` vs `scratch/manifest-after.txt`, 54 files). **No `__pycache__` exists anywhere in
the package** after all runs. `git status` shows only this new recheck directory as untracked; `bootstrap-review-e2/`
was not modified. Nothing was committed.

## The F-004 fix rejects my own E2 case file - expected, and recorded

The new unknown-key allowlist rejects the whole of my E2 case file because case `E2-FM-004` deliberately carried
`bogus_unknown_key` as the F-004 probe:

```text
run_cases.py: unusable input: .../e2-cases-original.jsonl:5: unknown case key(s) 'bogus_unknown_key';
permitted keys are assertions, candidate_subpath, case_id, expectations, files, mode, notes, prompt, tier, title
```

Exit 1. **This is the fix working**, not a regression: the probe key is exactly what the allowlist exists to
catch, and the message names the file, the line and the permitted set. All subsequent runs used
`scratch/cases/e2-cases-stripped.jsonl`, identical except that the probe key is removed. No other key in any of
my 14 cases needed changing - `expectations` and `routed_to` are both in the assertion allowlist.

## Per-finding closure

| ID | Sev | Status | Evidence |
| --- | --- | --- | --- |
| **F-001** | MAJOR | **CLOSED** | `SKILL.md` +12 lines adding package-relative links. Recomputed transitive link closure: **26 of 28 runtime files reachable**, up from 18. All 8 previously-unreachable files are now linked at a phase - `evaluation-boundaries.md` in §Non-negotiable boundaries, `framework-context.md` in §Two roots, `test-cases.json` and the three contracts in P1, the contracts again in P3, and the two EVPLAN/EVREPORT templates in P6 with the SKILL-008 name mapping spelled out. The only two files not reached by a Markdown link are `scripts/run_cases.py` and `scripts/graders.py`, which the P2 command block names directly - explicitly excluded from F-001 when it was raised. No existing sentence was rewritten and no file was removed. |
| **F-002** | MAJOR | **CLOSED** | New `fenced_lines()` helper reuses the module's own `FENCE` regex and open/close discipline; `grade_required_report_fields` skips fenced lines. Rerun of my `E2-RPT-001` over the same fenced-report input: **MISMATCH `incomplete`, "missing or empty required field(s): Disposition"** (was MATCH "every required field is present and populated"). Identical in both modes. Regression: `EX-GOOD-002`, the populated-report fixture, still MATCH ×2. |
| **F-003** | MAJOR | **CLOSED, and verified against overshoot** | Consultation is now read only from events whose `type` is in `CONSULTATION_EVENT_TYPES` and whose identity field (`skill`/`resource`/`loaded`/`target`) holds the **exact** target name; free text is never searched. Rerun of `E2-NEG-002`: **MISMATCH `completed consulted=False`** (was MATCH `consulted=True`). I then wrote three new probes to check the fix did not simply stop detecting consultation: a genuine `{"type":"skill_loaded","skill":"devforge-evaluate-expert"}` still gives **MATCH `consulted=True`**; a negative-expectation case over a real `resource_read` gives **MISMATCH**; and a consultation-bearing event carrying *no* identity field gives **INDETERMINATE + COULD_NOT_RUN** rather than guessing either way. All three correct. Regression: `E2-NEG-001` still COULD_NOT_RUN on the timeout transcript. |
| **F-004** | MINOR | **CLOSED** | `CASE_KEYS` and `ASSERTION_KEYS` allowlists added, plus a required non-empty `assertions` list. My typo probe now exits **1**: `unknown case key(s) 'assertion'` with file, line and permitted set. A new probe of mine with `"assertions": []` also exits **1**: `case 'EMPTY-001' has an empty assertions list`. The documented sentence and the code now agree. |
| **F-005** | MINOR | **CLOSED** | `sys.dont_write_bytecode = True` set before the `import graders`, plus `-B` shown in both documented invocations (`SKILL.md` P2 and `runner-interface.md`). Verified the stronger way: I ran a fresh copy of `scripts/` **without** `-B` - the form that previously produced the cache - and **0 `__pycache__` directories** appeared. No `__pycache__` exists in the package after any run in this recheck. |
| **F-006** | MINOR | **CLOSED** | `native-evaluation.md` step 5 now carries an eight-row precedence table matching the documentation retrieved 2026-09-10, with `--add-dir` at 5 and plugin at 6, and `sources.md` restates the same eight in order. The `without_skill` rule now says "including 7 and 8, which are easy to forget precisely because nobody put them there deliberately". The author also added a correct point I had not made: plugin skills are namespaced, so a plugin copy coexists with a same-named copy rather than replacing it - two reachable copies in a discovery run, not one winner. |
| **F-007** | ADVISORY | **CLOSED (option (a) taken)** | New `non_mapping` frontmatter status. A sequence root, or a bare-scalar root, on the **first content line** returns MISMATCH; a later unmatched line still returns INDETERMINATE, which correctly preserves the "never invent a defect" posture for constructs the subset genuinely cannot read. Rerun of `E2-FM-003`: `frontmatter_fields` **MISMATCH `non-mapping-root`** and `name_folder_relation` **MISMATCH** (both were INDETERMINATE). Regression: `E2-FM-004`, the `description: >-` block scalar, is still INDETERMINATE - the disclosed limit is intact and was not over-hardened. |
| **F-008** | ADVISORY | **CLOSED, all four** | (a) `read_frontmatter` docstring now lists all five statuses including `duplicate` and the new `non_mapping`. (b) The disjointness claim is now scoped to *assertion* results, with an explicit paragraph explaining that case-level `execution_status` uses `COULD_NOT_RUN` deliberately. (c) `references/sources.md` is now declared in `new_in_this_package` (15 entries) **with a digest that matches its bytes**. (d) `SKILL.md` P6 now tells the reader that the templates' inherited `decision.json` paragraph is template text, not a record to create - and the template bytes were correctly left unedited. |
| **F-009** | ADVISORY | **CLOSED, both** | (a) `results-contract.md` replaces the "four extensions" sentence with a six-row table grouping all the additions by purpose - native case binding, installation identity, observed boundaries, input visibility, plan/workspace binding, deviations - and states outright that no VPR-2, Routine/Full, lineage or adoption-evidence field exists anywhere. (b) The author's `handoff.md` revision 2 now states **both** capability sentences verbatim (`grep -c` = 2, at lines 61-62), where revision 1 referred to them only by count. |

**All nine findings closed. None still open.**

## New regression cases the author added

Four new runner cases and four new fixtures, one per behavioural repair, so each fix has a permanent guard.
I ran the author's file (now 17 cases, up from 13) in both modes; every new case behaves correctly and the
thirteen original cases keep their prior outcomes exactly:

| Case | Fixture | Guards | Observed |
| --- | --- | --- | --- |
| `EX-DEF-009` | `defect-fenced-report/` | F-002 | MISMATCH - `recommendation` and `behavior_status` present only inside a fence |
| `EX-DEF-010` | `defect-mention-only/` | F-003 | MATCH - prompt names the target to say *not* to use it; correctly not a consultation |
| `EX-GOOD-004` | `good/transcript/positive-consultation.json` | F-003 the other way | MATCH - a `skill_loaded` event naming the exact identity still establishes consultation |
| `EX-DEF-011` | `defect-frontmatter-non-mapping/` | F-007 | MISMATCH ×2 - sequence root, both graders |

Adding `EX-GOOD-004` is the right instinct: the failure mode a fix like F-003 invites is silently never
detecting anything again, and that case is what would catch it.

## Rubric recheck - R05, R08, R09 only

| ID | Was | Now | Basis |
| --- | --- | --- | --- |
| **R05** Runtime dependencies and resource delivery | FAIL | **PASS** | The FAIL rested entirely on the PASS anchor "required references and templates are routed from the installed entrypoint at the phase that needs them". All eight unrouted files are now linked at a named phase, and the two scripts are invoked from the P2 command block. Nothing else in this criterion had failed. |
| **R08** Prompt organisation and decision-relevant detail | FAIL | **PASS** | The FAIL anchor was "essential constraints are buried in an unreferenced resource". The permission matrix, the command-boundaries table and the EVPLAN/EVREPORT artifact mapping are now reachable, and the P6 paragraph states the SKILL-008 name mapping inline rather than leaving it only in a reference. `SKILL.md` grew from 143 to 151 lines - still far under the 500-line guidance - and no existing rule was duplicated or contradicted. |
| **R09** Observable checks and honest outcome reporting | FAIL | **PASS** | All three mechanisms that could turn absent evidence into a positive observation are fixed and verified in both directions: a fenced example no longer satisfies a required field; a mention no longer counts as a consultation while a genuine load still does, and an undecidable event blocks rather than guesses; a mistyped case key now fails loudly instead of reporting COMPLETED with zero assertions. The `INDETERMINATE`-never-softened posture survives - the block-scalar case is still INDETERMINATE. |

**R01-R04, R06, R07 and R10 were not re-adjudicated**, per the authorized scope. See the coordinator note below
about R07.

## New finding

### F-R01 - `derivation.json` carries seven stale destination digests, undisclosed

**Type:** defect. **Severity:** MINOR. **Location:** `references/derivation.json`, `derivations[].destination_sha256`
and `new_in_this_package[].sha256`.

**Evidence.** The repair pass edited ten package files and updated `derivation.json` substantially (+137 lines,
including a full `repair_pass_1` record and the newly declared `references/sources.md`). But the per-file digests
of the seven files the pass actually changed were not regenerated. Recomputed against bytes at `e101e76`:

| Path | Declared | Actual |
| --- | --- | --- |
| `SKILL.md` | `5f9769ddc394…` | `bdf665c7e180…` |
| `scripts/run_cases.py` | `d1fb18689eee…` | `95ca2abf77a5…` |
| `scripts/graders.py` | `7c03e7b21377…` | `1b7a27a37e1f…` |
| `references/runner-interface.md` | `a58c35dab0fd…` | `87c8942f2faa…` |
| `references/native-evaluation.md` | `b43680f963d5…` | `7d4a8bda731c…` |
| `references/results-contract.md` | `6e99ade182e4…` | `ebac4e4c53f9…` |
| `evals/cases.jsonl` | `b4b0c9314f43…` | `c31a7cb0a98f…` |

Every declared value is that file's digest at `e52ac59`. The `repair_pass_1` record mentions the words "digest"
or "sha256" **zero times**, so the staleness is undisclosed. The 18 **source** digests are unaffected and all 18
still match - they point at `docs/mvp` and Codex bytes that did not change. `references/sources.md`, newly
declared in this pass, carries a **correct** digest, which shows the omission is an oversight rather than a
policy.

**Impact.** `derivation.json` states its own purpose as "so a later reader can tell a deliberate refresh from
silent drift", and it is the provenance record that ships *inside* the installed package. A reader verifying the
package against it now gets seven mismatches and cannot distinguish this legitimate repair from tampering - the
exact discrimination the record exists to provide. It also sits awkwardly against the package's own
`results-contract.md` rule that "Changed bytes invalidate the observations that depended on them."

**Contained by three things**, which is why this is MINOR and not MAJOR: the author's `file-manifest.json` is
**54/54 current** (independently verified), so a correct per-file record does exist in the authoring evidence;
`repair_pass_1` documents every change in prose with its finding ID, files and verification; and no false
positive is produced anywhere.

**Smallest repair.** Regenerate those seven digest values and add one line to `repair_pass_1` recording that the
destination digests were refreshed in this pass. No content change. **Next owner:** the validator's author under
coordinator dispatch.

## Author disclosures verified

- **Builder-digest provenance correction — CONSISTENT, and independently confirmed.** The author discloses that
  revision 1 recorded the builder's `SKILL.md` as `342b8292…`, which was wrong: the digest had been taken from
  the builder worktree *after* E1's repair landed, while the bytes actually read were `69b6090`'s. I verified
  both halves directly against the builder worktree: `git show 69b6090:…/SKILL.md | sha256sum` →
  `1e9929a5713de1df05e2b0bbafdc49de388e74104e584f4ec77c237c35362a0e`, exactly the corrected value now recorded;
  `git show 4999f31:…/SKILL.md | sha256sum` → `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9`,
  exactly the value first recorded. The account is precisely right, the corrected digest is used throughout, and
  the reasoning offered (the read and the hash were separated in time) matches the byte evidence. The author also
  records assessing E1's `69b6090`→`4999f31` diff and concluding no re-authoring was required, keeping the
  builder reference at what was actually followed. Disclosing a self-inflicted provenance error unprompted, with
  the mechanism, is the behaviour this framework is trying to produce.
- **`handoff.md` revision 2** — verified: both capability statements now appear verbatim (F-009b).
- **`file-manifest.json`** — verified 54/54 current against bytes.

## Updated disposition

**insufficient evidence.**

Adjudicated by hand against `references/results-contract.md`. The three applicable FAILs that produced *revise*
in SEVAL-E2-001 are gone: R05, R08 and R09 now PASS on demonstrated, rerun evidence. With no applicable FAIL in
the rechecked scope, the governing rule becomes "otherwise a missing required observation gives **insufficient
evidence**" - and tiers **A, B and C remain NOT_RUN**, unchanged, because no installation, fresh session or
observed native boundary was available. A repair pass cannot supply those, and nothing in this recheck pretends
otherwise.

This is **not** *suitable for the stated scope*, and it is not acceptance, adoption or release. What changed is
that the candidate's demonstrated defects are gone; what has not changed is that its behaviour has never been
observed. **Behavioural status: `NOT_EVALUATED`.**

One MINOR defect (F-R01) is open and should be repaired before the next evaluation identity is frozen.

## For the coordinator

1. **R07 needs re-adjudication and is outside my authorized scope.** I passed R07 at `e52ac59` partly *because*
   16/16 destination and 18/18 source digests matched. F-R01 means seven destination digests no longer do. R07's
   PASS anchor asks that artifacts "bind to exact upstream bytes"; its FAIL anchor is "fabricates a digest or
   receipt", which these are not - they are stale, from a real prior revision. I have not moved R07, because the
   authorization named R05, R08 and R09 only. Please decide whether R07 is re-run.
2. **F-R01 severity.** I called it MINOR because a fully current manifest exists in the authoring evidence and no
   false positive results. A reader who weights the shipped provenance record more heavily could reasonably call
   it MAJOR.
3. **F-007 was resolved as option (a)**, the narrower classification, and the implementation is better scoped
   than my suggestion: only the *first content line* decides a non-mapping root, so genuinely unreadable
   constructs still return INDETERMINATE.
4. **Tiers A/B/C remain the only route to a behavioural claim.** Two repair passes have now improved this
   package without a single native observation. That gap is a DevForge integration-owner and operator
   dependency, not something the author can close.
5. The two missing DevForge CLI capabilities are unchanged, still recorded, and still closed by nothing here.

## Limits

Same bootstrap limits as SEVAL-E2-001: source-loaded rubric, nothing installed or activated, single reviewer not
blinded, author evidence treated as untrusted and independently re-derived where checkable. Additionally: this
recheck deliberately did **not** rerun unchanged broad checks, so its silence about an area is not a fresh
observation about that area - SEVAL-E2-001 remains the record for everything outside F-001…F-009 and R05/R08/R09.
